"""
Geocoding + market resolution with multi-country, state, and city support.

A "market" can be either a named entry in MARKETS (a bbox tuple) or a free-text
place name / structured (country, state, city) we geocode on the fly via Nominatim.
bbox order is (south, west, north, east) everywhere in this package.
"""
from __future__ import annotations

import requests

from .audit import UA

NOMINATIM = "https://nominatim.openstreetmap.org/search"

# Reusable named markets (south, west, north, east).
MARKETS: dict[str, tuple[float, float, float, float]] = {
    "sonoma_county_ca": (38.05, -123.55, 38.85, -122.35),
    "phoenix_az":       (33.20, -112.40, 33.85, -111.80),
    "tampa_fl":         (27.80, -82.65, 28.20, -82.30),
    "austin_tx":        (30.10, -97.95, 30.52, -97.55),
    "toronto_on":       (43.58, -79.64, 43.86, -79.12),
    "vancouver_bc":     (49.19, -123.27, 49.32, -123.02),
    "london_uk":        (51.28, -0.51, 51.69, 0.33),
    "sydney_au":        (-34.05, 150.65, -33.55, 151.35),
    "melbourne_au":     (-38.05, 144.75, -37.55, 145.35),
    "berlin_de":        (52.34, 13.08, 52.68, 13.76),
    "paris_fr":         (48.81, 2.22, 48.91, 2.47),
}

# Country name / alias to 2-letter uppercase ISO code
COUNTRY_CODES: dict[str, str] = {
    "united states": "US", "usa": "US", "us": "US", "u.s.": "US", "u.s.a.": "US", "america": "US",
    "canada": "CA", "ca": "CA", "can": "CA",
    "united kingdom": "GB", "uk": "GB", "great britain": "GB", "gb": "GB",
    "england": "GB", "scotland": "GB", "wales": "GB", "northern ireland": "GB",
    "australia": "AU", "au": "AU", "aus": "AU",
    "germany": "DE", "de": "DE", "deutschland": "DE",
    "france": "FR", "fr": "FR",
    "italy": "IT", "it": "IT", "italia": "IT",
    "spain": "ES", "es": "ES", "espana": "ES", "españa": "ES",
    "netherlands": "NL", "nl": "NL", "holland": "NL",
    "india": "IN", "in": "IN", "ind": "IN",
    "pakistan": "PK", "pk": "PK", "pak": "PK",
    "mexico": "MX", "mx": "MX",
    "brazil": "BR", "br": "BR", "brasil": "BR",
    "japan": "JP", "jp": "JP",
    "china": "CN", "cn": "CN",
    "new zealand": "NZ", "nz": "NZ",
    "ireland": "IE", "ie": "IE",
    "switzerland": "CH", "ch": "CH",
    "sweden": "SE", "se": "SE",
    "norway": "NO", "no": "NO",
    "denmark": "DK", "dk": "DK",
    "finland": "FI", "fi": "FI",
    "belgium": "BE", "be": "BE",
    "austria": "AT", "at": "AT",
    "portugal": "PT", "pt": "PT",
    "south africa": "ZA", "za": "ZA",
    "united arab emirates": "AE", "uae": "AE", "ae": "AE",
    "singapore": "SG", "sg": "SG",
    "saudi arabia": "SA", "sa": "SA",
    "turkey": "TR", "tr": "TR", "turkiye": "TR", "türkiye": "TR",
}

# 2-letter uppercase ISO code to standard country name
COUNTRY_NAMES: dict[str, str] = {
    "US": "United States", "CA": "Canada", "GB": "United Kingdom", "AU": "Australia",
    "DE": "Germany", "FR": "France", "IT": "Italy", "ES": "Spain", "NL": "Netherlands",
    "IN": "India", "PK": "Pakistan", "MX": "Mexico", "BR": "Brazil", "JP": "Japan",
    "CN": "China", "NZ": "New Zealand", "IE": "Ireland", "CH": "Switzerland",
    "SE": "Sweden", "NO": "Norway", "DK": "Denmark", "FI": "Finland", "BE": "Belgium",
    "AT": "Austria", "PT": "Portugal", "ZA": "South Africa", "AE": "United Arab Emirates",
    "SG": "Singapore", "SA": "Saudi Arabia", "TR": "Turkey",
}

US_STATES: dict[str, str] = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
    "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH",
    "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
    "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
}

CA_PROVINCES: dict[str, str] = {
    "ontario": "ON", "quebec": "QC", "british columbia": "BC", "alberta": "AB",
    "manitoba": "MB", "saskatchewan": "SK", "nova scotia": "NS", "new brunswick": "NB",
    "newfoundland and labrador": "NL", "prince edward island": "PE", "northwest territories": "NT",
    "yukon": "YT", "nunavut": "NU",
}

AU_STATES: dict[str, str] = {
    "new south wales": "NSW", "victoria": "VIC", "queensland": "QLD",
    "western australia": "WA", "south australia": "SA", "tasmania": "TAS",
    "australian capital territory": "ACT", "northern territory": "NT",
}


def normalize_country(country_str: str | None) -> tuple[str, str]:
    """Return (iso2_code_upper, full_name) e.g. ('CA', 'Canada') or ('', '')."""
    if not country_str:
        return "", ""
    s = str(country_str).strip()
    low = s.lower().replace(".", "").replace("-", " ")
    if low in COUNTRY_CODES:
        code = COUNTRY_CODES[low]
        return code, COUNTRY_NAMES.get(code, s)
    if len(s) == 2 and s.isalpha():
        code = s.upper()
        return code, COUNTRY_NAMES.get(code, code)
    return "", s


def normalize_state(state_str: str | None, country_code: str = "") -> str:
    """Return 2-3 letter uppercase state abbreviation if recognized, or cleaned original."""
    if not state_str:
        return ""
    s = str(state_str).strip()
    low = s.lower()
    cc = (country_code or "").upper()
    if cc == "US" or not cc:
        if low in US_STATES:
            return US_STATES[low]
        if s.upper() in US_STATES.values():
            return s.upper()
    if cc == "CA" or not cc:
        if low in CA_PROVINCES:
            return CA_PROVINCES[low]
        if s.upper() in CA_PROVINCES.values():
            return s.upper()
    if cc == "AU" or not cc:
        if low in AU_STATES:
            return AU_STATES[low]
        if s.upper() in AU_STATES.values():
            return s.upper()
    return s


def geocode_location(place: str = "", *, country: str = "",
                     state: str = "", city: str = "") -> dict | None:
    """Return geocoded location details for free-text or structured location.
    
    Returns {lat, lon, bbox=(s,w,n,e), display_name, country, country_code, state, city}
    or None if geocoding fails.
    """
    iso_code, country_full = normalize_country(country)
    # Build query string
    q_parts = []
    if city and city.strip():
        q_parts.append(city.strip())
    if state and state.strip():
        q_parts.append(state.strip())
    if country_full and country_full.strip():
        q_parts.append(country_full.strip())
    elif country and country.strip():
        q_parts.append(country.strip())
    
    query = ", ".join(q_parts) if q_parts else place.strip()
    if not query:
        return None

    params: dict = {"q": query, "format": "json", "limit": 1, "addressdetails": 1}
    if iso_code:
        params["countrycodes"] = iso_code.lower()

    try:
        r = requests.get(NOMINATIM, params=params,
                         headers={"User-Agent": UA}, timeout=10)
        if r.status_code != 200 or not r.json():
            # If countrycodes filter was too strict or place format differed, retry without countrycodes
            if "countrycodes" in params:
                params.pop("countrycodes")
                r = requests.get(NOMINATIM, params=params,
                                 headers={"User-Agent": UA}, timeout=10)
                if r.status_code != 200 or not r.json():
                    return None
            else:
                return None
        d = r.json()[0]
        bb = [float(x) for x in d["boundingbox"]]  # nominatim: [s, n, w, e]
        addr = d.get("address", {})
        
        c_code = (addr.get("country_code") or iso_code or "").upper()
        c_name = addr.get("country") or COUNTRY_NAMES.get(c_code, country_full or country)
        st_name = (addr.get("state") or addr.get("province") or
                   addr.get("region") or state or "")
        ct_name = (addr.get("city") or addr.get("town") or addr.get("village") or
                   addr.get("municipality") or city or "")

        return {
            "lat": float(d["lat"]), "lon": float(d["lon"]),
            "bbox": (bb[0], bb[2], bb[1], bb[3]),
            "display_name": d["display_name"],
            "country": c_name,
            "country_code": c_code,
            "state": normalize_state(st_name, c_code),
            "city": ct_name,
        }
    except Exception:
        return None


def geocode_city(place: str, *, country: str = "", state: str = "", city: str = "") -> dict | None:
    """Return {lat, lon, bbox=(s,w,n,e), display_name, ...} for a free-text place."""
    return geocode_location(place, country=country, state=state, city=city)


def resolve_market_details(market: str = "", *, country: str = "",
                           state: str = "", city: str = "") -> tuple[tuple[float, float, float, float], str, dict]:
    """Accept a named market key OR free-text/structured place.
    Return (bbox, label, details_dict).
    """
    key = (market or "").strip().lower()
    if key in MARKETS:
        # Infer standard location info for predefined keys
        s, w, n, e = MARKETS[key]
        c_code, c_name, st_val, ct_val = "US", "United States", "", ""
        if key.endswith("_ca") or "_ca" in key:
            c_code, c_name, st_val = "US", "United States", "CA"
        elif key.endswith("_az"):
            c_code, c_name, st_val, ct_val = "US", "United States", "AZ", "Phoenix"
        elif key.endswith("_fl"):
            c_code, c_name, st_val, ct_val = "US", "United States", "FL", "Tampa"
        elif key.endswith("_tx"):
            c_code, c_name, st_val, ct_val = "US", "United States", "TX", "Austin"
        elif key.endswith("_on"):
            c_code, c_name, st_val, ct_val = "CA", "Canada", "ON", "Toronto"
        elif key.endswith("_bc"):
            c_code, c_name, st_val, ct_val = "CA", "Canada", "BC", "Vancouver"
        elif key.endswith("_uk"):
            c_code, c_name, ct_val = "GB", "United Kingdom", "London"
        elif key.endswith("_au"):
            c_code, c_name = "AU", "Australia"
        elif key.endswith("_de"):
            c_code, c_name, ct_val = "DE", "Germany", "Berlin"
        elif key.endswith("_fr"):
            c_code, c_name, ct_val = "FR", "France", "Paris"

        info = {
            "bbox": (s, w, n, e),
            "display_name": market,
            "country": c_name,
            "country_code": c_code,
            "state": st_val,
            "city": ct_val,
        }
        return MARKETS[key], market, info

    geo = geocode_location(market, country=country, state=state, city=city)
    if not geo:
        raise ValueError(
            f"could not resolve market '{market or ', '.join(filter(None, [city, state, country]))}'. "
            f"Use a key in MARKETS ({sorted(MARKETS)}) or a place like 'Toronto, Canada' or 'Austin, Texas'."
        )
    return geo["bbox"], geo["display_name"], geo


def resolve_market(market: str = "", *, country: str = "",
                   state: str = "", city: str = "") -> tuple[tuple[float, float, float, float], str]:
    """Accept a named market key OR a free-text place. Return (bbox, label)."""
    bbox, label, _ = resolve_market_details(market, country=country, state=state, city=city)
    return bbox, label
