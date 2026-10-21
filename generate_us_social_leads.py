import os
import sys
import re
import csv
import time
import duckdb
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from leadgen.sources import _overture_release
from leadgen.verticals._common import is_social
from leadgen.quality import is_junk_name, normalize_phone

# Regional bounding boxes across major US economic and commercial hubs
US_REGIONS = [
    {"region": "Austin & Central TX", "state": "TX", "south": 30.1, "west": -98.0, "north": 30.6, "east": -97.5},
    {"region": "Los Angeles & Orange County, CA", "state": "CA", "south": 33.6, "west": -118.6, "north": 34.3, "east": -117.8},
    {"region": "New York Metro & Tri-State", "state": "NY", "south": 40.5, "west": -74.2, "north": 41.0, "east": -73.7},
    {"region": "Chicago & Cook County, IL", "state": "IL", "south": 41.6, "west": -88.0, "north": 42.1, "east": -87.5},
    {"region": "Miami & South Florida", "state": "FL", "south": 25.6, "west": -80.4, "north": 26.3, "east": -80.0},
    {"region": "Dallas - Fort Worth, TX", "state": "TX", "south": 32.5, "west": -97.4, "north": 33.1, "east": -96.6},
    {"region": "Houston Metro, TX", "state": "TX", "south": 29.6, "west": -95.6, "north": 30.1, "east": -95.1},
    {"region": "Atlanta Metro, GA", "state": "GA", "south": 33.6, "west": -84.6, "north": 34.0, "east": -84.2},
    {"region": "Phoenix Metro, AZ", "state": "AZ", "south": 33.3, "west": -112.3, "north": 33.7, "east": -111.9},
    {"region": "Seattle & King County, WA", "state": "WA", "south": 47.4, "west": -122.4, "north": 47.8, "east": -122.2},
    {"region": "Denver & Front Range, CO", "state": "CO", "south": 39.6, "west": -105.1, "north": 40.0, "east": -104.8},
    {"region": "San Francisco Bay Area, CA", "state": "CA", "south": 37.3, "west": -122.4, "north": 37.9, "east": -122.0},
]

EXCLUDE_CATEGORIES = {
    "elementary_school", "middle_school", "high_school", "school", "preschool",
    "place_of_worship", "church", "baptist_place_of_worship", "catholic_church",
    "cemetery", "police_station", "fire_station", "courthouse", "city_hall",
    "government_office", "embassy", "military_base", "mountain_bike_trail",
    "park", "playground"
}

def clean_social_url(url: str) -> str:
    if not url:
        return ""
    # Strip tracking parameters (?igsh=..., ?ref=...)
    u = url.split("?")[0].strip()
    return u

def extract_platform(url: str) -> str:
    low = url.lower()
    if "facebook.com" in low or "fb.com" in low:
        return "Facebook"
    if "instagram.com" in low:
        return "Instagram"
    if "linktr.ee" in low or "linktree.com" in low:
        return "Linktree"
    if "tiktok.com" in low:
        return "TikTok"
    if "twitter.com" in low or "x.com" in low:
        return "X (Twitter)"
    if "nextdoor.com" in low:
        return "Nextdoor"
    if "youtube.com" in low:
        return "YouTube"
    return "Social Page"

def format_category(cat: str) -> str:
    if not cat:
        return "Local Business"
    return cat.replace("_", " ").title()

def main():
    print("=" * 60)
    print("  Extracting US Businesses with Only Social Pages (No Real Website)")
    print("=" * 60)

    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
    release = _overture_release(con)
    print(f"Overture Release: {release}")

    s3 = f"s3://overturemaps-us-west-2/release/{release}/theme=places/type=place/*"

    all_leads = []
    seen = set()

    for idx, reg in enumerate(US_REGIONS, 1):
        r_name = reg["region"]
        print(f"[{idx}/{len(US_REGIONS)}] Querying {r_name}...")
        
        sql = f"""
        SELECT names.primary AS name,
               taxonomy.primary AS category,
               websites[1] AS website,
               CASE WHEN length(phones)>0 THEN phones[1] END AS phone,
               addresses[1].freeform AS address,
               addresses[1].locality AS city,
               addresses[1].region AS state,
               addresses[1].postcode AS zip,
               addresses[1].country AS country,
               brand.names.primary AS brand
        FROM read_parquet('{s3}', hive_partitioning=1)
        WHERE bbox.xmin BETWEEN {reg['west']} AND {reg['east']}
          AND bbox.ymin BETWEEN {reg['south']} AND {reg['north']}
          AND names.primary IS NOT NULL
          AND length(websites) > 0
          AND (
              lower(websites[1]) LIKE '%facebook.com%' OR
              lower(websites[1]) LIKE '%fb.com%' OR
              lower(websites[1]) LIKE '%instagram.com%' OR
              lower(websites[1]) LIKE '%linktr.ee%' OR
              lower(websites[1]) LIKE '%tiktok.com%' OR
              lower(websites[1]) LIKE '%twitter.com%' OR
              lower(websites[1]) LIKE '%x.com%'
          )
          AND (addresses[1].country = 'US' OR addresses[1].country IS NULL)
        LIMIT 45;
        """
        try:
            rows = con.execute(sql).fetchall()
        except Exception as e:
            print(f"  Warning on {r_name}: {e}")
            continue

        added = 0
        for r in rows:
            name, cat, site, phone, addr, city, state, zipcode, country, brand = r
            
            if is_junk_name(name):
                continue
            if cat in EXCLUDE_CATEGORIES:
                continue
            if not site or not is_social(site):
                continue

            # Deduplication key
            key = (name.strip().lower(), (phone or "").strip())
            if key in seen:
                continue
            seen.add(key)

            platform = extract_platform(site)
            clean_site = clean_social_url(site)
            clean_phone = normalize_phone(phone) or (phone or "")
            clean_state = state or reg["state"]
            clean_city = city or r_name.split("&")[0].split("-")[0].strip()
            
            score = 65
            if clean_phone:
                score += 5
            if addr:
                score += 5

            lead = {
                "Tier": "A",
                "Score": score,
                "Business Name": name.strip(),
                "Category": format_category(cat),
                "Platform": platform,
                "Social Page (No Owned Website)": clean_site,
                "Phone": clean_phone,
                "Address": addr or "",
                "City": clean_city,
                "State": clean_state,
                "Zip": zipcode or "",
                "Country": "United States",
                "Why It's a Lead": f"Only a {platform} presence; no owned company website",
                "Pitch / Suggested Opener": (
                    f"Running everything off {platform} — pitch a dedicated company website "
                    f"they own that ranks on Google and survives platform algorithm changes."
                )
            }
            all_leads.append(lead)
            added += 1

        print(f"  -> Added {added} qualified commercial leads (Total: {len(all_leads)})")

    # Sort leads by score descending, then state, then name
    all_leads.sort(key=lambda x: (-x["Score"], x["State"], x["City"], x["Business Name"]))

    # ──────────────── Export to CSV ────────────────
    csv_file = "us_social_only_leads.csv"
    fieldnames = list(all_leads[0].keys()) if all_leads else []
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_leads)

    print(f"\n[OK] Successfully saved {len(all_leads)} leads to CSV: {csv_file}")

    # ──────────────── Export to Styled XLSX ────────────────
    xlsx_file = "us_social_only_leads.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "US Social-Only Leads"

    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    tier_fill = PatternFill(start_color="E8F8EC", end_color="E8F8EC", fill_type="solid")
    border_thin = Side(border_style="thin", color="DDE2E8")
    cell_border = Border(top=border_thin, left=border_thin, right=border_thin, bottom=border_thin)

    # Headers
    for col_idx, h in enumerate(fieldnames, 1):
        c = ws.cell(row=1, column=col_idx, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)
        c.border = cell_border

    # Data rows
    for row_idx, lead in enumerate(all_leads, 2):
        for col_idx, h in enumerate(fieldnames, 1):
            val = lead[h]
            c = ws.cell(row=row_idx, column=col_idx, value=val)
            c.font = Font(name="Segoe UI", size=10)
            c.fill = tier_fill
            c.border = cell_border
            if h in ("Tier", "Score", "Platform", "State", "Zip", "Country"):
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif h in ("Phone",):
                c.alignment = Alignment(horizontal="left", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # Column widths
    for col in ws.columns:
        col_letter = col[0].column_letter
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

    ws.freeze_panes = "A2"
    wb.save(xlsx_file)
    print(f"[OK] Successfully saved styled Excel workbook: {xlsx_file}")

    # Also display top sample
    print(f"\nSample of top leads extracted across the US:")
    for lead in all_leads[:10]:
        print(f"  - [{lead['State']}] {lead['Business Name']} ({lead['Category']}) | {lead['Platform']}: {lead['Social Page (No Owned Website)']} | Phone: {lead['Phone']}")

if __name__ == "__main__":
    main()
