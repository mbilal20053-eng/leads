"""
The pipeline: collect → dedupe → enrich → suppress → score → export.
Vertical-agnostic; all use-case specifics come from the Vertical object.
"""
from __future__ import annotations

import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .geo import (resolve_market, resolve_market_details, normalize_country,
                  normalize_state)
from .sources import (overture_collect, osm_collect, socrata_collect,
                      npi_collect, foursquare_collect, arcgis_collect)
from .suppression import norm, build_suppression_set
from .export import write_outputs
from .vertical import Vertical


def ensure_location_columns(columns: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Ensure ('State', 'state') and ('Country', 'country') are in columns after ('City', 'city')."""
    keys = [k for _, k in columns]
    if "state" in keys and "country" in keys:
        return columns
    new_cols = []
    has_city = any(k == "city" for _, k in columns)
    for h, k in columns:
        new_cols.append((h, k))
        if k == "city":
            if "state" not in keys:
                new_cols.append(("State", "state"))
            if "country" not in keys:
                new_cols.append(("Country", "country"))
    if not has_city:
        cur_keys = [k for _, k in new_cols]
        if "state" not in cur_keys:
            new_cols.append(("State", "state"))
        if "country" not in cur_keys:
            new_cols.append(("Country", "country"))
    return new_cols


def _matches_country(val: str | None, target: str | None) -> bool:
    if not target or not str(target).strip():
        return True
    if not val or not str(val).strip():
        return False
    t_code, t_name = normalize_country(str(target))
    v_code, v_name = normalize_country(str(val))
    if t_code and v_code and t_code == v_code:
        return True
    v_low = str(val).strip().lower()
    t_low = str(target).strip().lower()
    return v_low == t_low or v_low in t_low or t_low in v_low


def _matches_state(val: str | None, target: str | None, country_code: str = "") -> bool:
    if not target or not str(target).strip():
        return True
    if not val or not str(val).strip():
        return False
    t_norm = normalize_state(str(target), country_code)
    v_norm = normalize_state(str(val), country_code)
    if t_norm and v_norm and t_norm.upper() == v_norm.upper():
        return True
    v_low = str(val).strip().lower()
    t_low = str(target).strip().lower()
    return v_low == t_low or v_low in t_low or t_low in v_low


def _matches_city(val: str | None, target: str | None) -> bool:
    if not target or not str(target).strip():
        return True
    if not val or not str(val).strip():
        return False
    v_low = str(val).strip().lower()
    t_low = str(target).strip().lower()
    return v_low == t_low or t_low in v_low or v_low in t_low


def load_crm_names(path_or_text: str, *, is_text: bool = False) -> set[str]:
    """Normalized company names from an existing CRM export (CSV) so the pipeline
    never hands back a business the user already has.

    Reads the first column that looks like a company/business/name field; falls
    back to the first column. Accepts a file path or raw CSV text (is_text=True).
    """
    import csv
    import io
    if not path_or_text:
        return set()
    if is_text:
        f = io.StringIO(path_or_text)
    else:
        f = open(path_or_text, newline="", encoding="utf-8-sig", errors="replace")
    try:
        reader = csv.reader(f)
        rows = list(reader)
    finally:
        if not is_text:
            f.close()
    if not rows:
        return set()
    header = [h.strip().lower() for h in rows[0]]
    name_keys = ("company name", "company", "business", "business name", "brokerage",
                 "name", "account name", "organization")
    col = next((i for i, h in enumerate(header) if h in name_keys), 0)
    out: set[str] = set()
    for row in rows[1:]:
        if col < len(row):
            k = norm(row[col])
            if k:
                out.add(k)
    return out


def _dedupe(leads: list[dict]) -> list[dict]:
    """Collapse same-name duplicates (across sources) within one market."""
    seen: dict[str, dict] = {}
    for r in leads:
        key = norm(r.get("name", ""))
        if not key:
            continue
        if key in seen:
            # prefer the record that already has a website / more fields
            cur = seen[key]
            if not cur.get("website") and r.get("website"):
                cur["website"] = r["website"]
            if not cur.get("phone") and r.get("phone"):
                cur["phone"] = r["phone"]
        else:
            seen[key] = r
    return list(seen.values())


def run_pipeline(vertical: Vertical, market: str = "", *,
                 sources=("overture",), limit: int | None = None,
                 enrich: bool = True, enrich_cap: int | None = 150,
                 out_stem: str | None = None, config_override: dict | None = None,
                 exclude_names: set | None = None, demo: bool = False,
                 country: str | None = None, state: str | None = None, city: str | None = None,
                 log=print) -> list[dict]:
    """Run the full pipeline for one vertical in one market or location.

    sources: any of ("overture", "osm", "socrata", "npi", "foursquare", ...).
    enrich:  run the vertical's enrich_fn (fetches each business's site).
    enrich_cap: only enrich the top-N by collection order (cost control); None = all.
    out_stem: if set, also writes <stem>_crm.csv and <stem>.xlsx.
    config_override: shallow-merged over the vertical's config for THIS run only
                     (e.g. competitor seed URLs typed into the GUI). The shared
                     vertical object is never mutated.
    exclude_names: normalized company names to drop (e.g. the user's existing CRM)
                   — see load_crm_names(). Matches are removed, not just flagged.
    demo: if True, use bundled offline sample data + fixture enrichment (no network).
    country: optional country name or ISO code (e.g. 'Canada', 'CA', 'United States', 'US')
    state: optional state or province (e.g. 'Ontario', 'Texas', 'ON', 'TX')
    city: optional city name (e.g. 'Toronto', 'Austin')
    Returns the scored, sorted list of lead dicts. Output file paths, when written,
    are attached as run_pipeline.last_outputs = (csv_path, xlsx_path).
    """
    run_pipeline.last_outputs = None
    # Per-run config: copy so concurrent runs / the registry stay clean.
    cfg = dict(vertical.config)
    if config_override:
        cfg.update(config_override)

    target_country = (country or "").strip()
    target_state = (state or "").strip()
    target_city = (city or "").strip()

    # 1. COLLECT
    leads: list[dict] = []
    if demo:
        from .demo import demo_records
        leads = demo_records()
        log(f"DEMO MODE — using {len(leads)} bundled sample businesses (no network).")
        market_country_code = "US"
        market_country = "United States"
        market_state = ""
        market_city = ""
    else:
        # Build market description if omitted but city/state/country provided
        if not market and (target_city or target_state or target_country):
            parts = [p for p in (target_city, target_state, target_country) if p]
            market = ", ".join(parts)
        if not market:
            raise ValueError("a market, city, state, or country is required to run the pipeline.")

        bbox, label, geo_info = resolve_market_details(market, country=target_country,
                                                       state=target_state, city=target_city)
        market_country_code = geo_info.get("country_code", "")
        market_country = geo_info.get("country", "")
        market_state = geo_info.get("state", "")
        market_city = geo_info.get("city", "")

        loc_tags = []
        if target_country: loc_tags.append(f"country={target_country}")
        if target_state: loc_tags.append(f"state={target_state}")
        if target_city: loc_tags.append(f"city={target_city}")
        tag_str = f" [{', '.join(loc_tags)}]" if loc_tags else ""

        log(f"Market: {label}{tag_str}  bbox={tuple(round(x,3) for x in bbox)}")
        if "overture" in sources:
            try:
                try:
                    leads += overture_collect(bbox, vertical.overture_categories, limit, log,
                                             country=target_country or market_country_code)
                except TypeError:
                    leads += overture_collect(bbox, vertical.overture_categories, limit, log)
            except Exception as e:
                log(f"  Overture failed: {e}")
        if "osm" in sources and vertical.osm_tags:
            try:
                leads += osm_collect(bbox, vertical.osm_tags, log)
            except Exception as e:
                log(f"  OSM failed: {e}")
        if "socrata" in sources:
            try:
                leads += socrata_collect(label, limit=limit, log=log,
                                         datasets=cfg.get("socrata_datasets"))
            except Exception as e:
                log(f"  Socrata failed: {e}")
        if "npi" in sources:
            try:
                leads += npi_collect(label, limit=limit, log=log,
                                     taxonomies=cfg.get("npi_taxonomies"))
            except Exception as e:
                log(f"  NPI failed: {e}")
        if "foursquare" in sources:
            try:
                leads += foursquare_collect(bbox, vertical.overture_categories,
                                            limit, log)
            except Exception as e:
                log(f"  Foursquare failed: {e}")
        if "arcgis" in sources:
            try:
                leads += arcgis_collect(label, limit=limit, log=log,
                                        layers=cfg.get("arcgis_layers"))
            except Exception as e:
                log(f"  ArcGIS failed: {e}")
        # Extra no-key sources (lazy import so they're fully optional).
        if {"wikidata", "ckan", "localfile", "url_csv"} & set(sources):
            from .extra_sources import (wikidata_collect, ckan_collect,
                                        localfile_collect, url_csv_collect)
            if "wikidata" in sources:
                try:
                    leads += wikidata_collect(bbox, limit=limit, log=log)
                except Exception as e:
                    log(f"  Wikidata failed: {e}")
            if "ckan" in sources:
                try:
                    leads += ckan_collect(label, limit=limit, log=log)
                except Exception as e:
                    log(f"  CKAN failed: {e}")
            if "localfile" in sources and cfg.get("localfile_path"):
                try:
                    leads += localfile_collect(cfg["localfile_path"], limit=limit, log=log)
                except Exception as e:
                    log(f"  Local file failed: {e}")
            if "url_csv" in sources and cfg.get("url_csv"):
                try:
                    leads += url_csv_collect(cfg["url_csv"], limit=limit, log=log)
                except Exception as e:
                    log(f"  URL CSV failed: {e}")

    # Backfill missing location attributes from the resolved search location
    for r in leads:
        if not r.get("country") and market_country_code:
            r["country"] = market_country_code
        if not r.get("state") and market_state:
            r["state"] = market_state
        if not r.get("city") and market_city:
            r["city"] = market_city

    # Location filtering if requested
    if target_country:
        before = len(leads)
        leads = [r for r in leads if _matches_country(r.get("country"), target_country)]
        if before - len(leads):
            log(f"  filtered to country '{target_country}': {len(leads)}/{before} kept")
    if target_state:
        before = len(leads)
        leads = [r for r in leads if _matches_state(r.get("state"), target_state, market_country_code or target_country)]
        if before - len(leads):
            log(f"  filtered to state '{target_state}': {len(leads)}/{before} kept")
    if target_city and not demo:
        if target_city.lower() not in label.lower() and target_city.lower() not in market.lower():
            before = len(leads)
            leads = [r for r in leads if _matches_city(r.get("city"), target_city)]
            if before - len(leads):
                log(f"  filtered to city '{target_city}': {len(leads)}/{before} kept")
    elif target_city and demo:
        before = len(leads)
        leads = [r for r in leads if _matches_city(r.get("city"), target_city)]
        if before - len(leads):
            log(f"  filtered to city '{target_city}': {len(leads)}/{before} kept")

    # Drop permanently-closed businesses, then normalize phones (helps dialing +
    # cross-source dedupe identity).
    from .quality import cross_source_dedupe, normalize_phone, is_closed
    before = len(leads)
    leads = [r for r in leads if not is_closed(r)]
    if before - len(leads):
        log(f"  dropped {before - len(leads)} closed businesses")
    for r in leads:
        if r.get("phone"):
            r["phone"] = normalize_phone(r["phone"]) or r["phone"]
    log(f"Collected {len(leads)} raw; deduping across sources…")
    leads = cross_source_dedupe(leads)
    log(f"  {len(leads)} after dedupe")

    # 1a. drop businesses already in the user's CRM (never hand back a dupe)
    if exclude_names:
        before = len(leads)
        leads = [r for r in leads if norm(r.get("name", "")) not in exclude_names]
        log(f"  removed {before - len(leads)} already in your CRM ({len(exclude_names)} names)")

    # 1b. chain handling — verticals that don't keep chains drop branded records
    if not vertical.keep_chains:
        before = len(leads)
        leads = [r for r in leads if not (r.get("brand"))]
        log(f"  dropped {before - len(leads)} chain/branded records")

    # 2. SUPPRESSION (competitor clients) — build once, applied during scoring.
    # Skipped in demo mode: it fetches competitor sites, and demo must stay offline.
    suppressed: dict[str, str] = {}
    if vertical.suppression_fn and not demo:
        log("Building competitor-suppression set…")
        suppressed = vertical.suppression_fn(cfg) or {}

    # 3. ENRICH (per-business website visit) — parallel, capped
    if enrich and vertical.enrich_fn and demo:
        # Offline enrichment: feed bundled fixture HTML through the same hooks.
        from .demo import demo_html_for
        ctx = {"config": cfg, "demo_html": demo_html_for}
        log(f"Enriching {len(leads)} sample businesses from bundled pages…")
        for r in leads:
            try:
                vertical.enrich_fn(r, ctx)
            except Exception as e:
                r["enrich_error"] = str(e)
    elif enrich and vertical.enrich_fn:
        targets = leads if enrich_cap is None else leads[:enrich_cap]
        log(f"Enriching {len(targets)} businesses (parallel)…")
        ctx = {"config": cfg}
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(vertical.enrich_fn, r, ctx): r for r in targets}
            done = 0
            for f in as_completed(futs):
                try:
                    f.result()
                except Exception as e:
                    futs[f]["enrich_error"] = str(e)
                done += 1
                if done % 25 == 0:
                    log(f"  enriched {done}/{len(targets)}")

    # 4. SCORE (+ apply suppression flag) + opener
    for r in leads:
        key = norm(r.get("name", ""))
        if key in suppressed:
            r["suppressed"] = True
            r["suppressed_by"] = suppressed[key]
        s, tier, reasons = vertical.score(r)
        r["score"], r["tier"], r["why"] = s, tier, reasons
        if vertical.opener_fn:
            r["opener"] = vertical.opener_fn(r)
    leads.sort(key=lambda x: -x.get("score", 0))

    n = {"A": 0, "B": 0, "C": 0}
    for r in leads:
        n[r.get("tier", "C")] = n.get(r.get("tier", "C"), 0) + 1
    log(f"Scored {len(leads)} — A={n['A']} B={n['B']} C={n['C']}")

    # 5. EXPORT
    if out_stem:
        # Slugify only the filename; keep any directory the caller supplied intact.
        import os
        d, base = os.path.split(out_stem)
        stem = os.path.join(d, re.sub(r"[^a-z0-9]+", "_", base.lower()).strip("_"))
        cols = ensure_location_columns(vertical.columns)
        run_pipeline.last_outputs = write_outputs(leads, cols, stem, log)

    return leads
