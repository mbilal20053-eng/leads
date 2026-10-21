import sys
import os
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import leadgen
from leadgen import get_vertical, run_pipeline
from leadgen.verticals._common import is_social

US_MARKETS = [
    ("Austin, TX", "austin_tx"),
    ("Phoenix, AZ", "phoenix_az"),
    ("Tampa, FL", "tampa_fl"),
    ("Sonoma County, CA", "sonoma_county_ca"),
    ("New York, NY", "New York, NY"),
    ("Los Angeles, CA", "Los Angeles, CA"),
    ("Chicago, IL", "Chicago, IL"),
    ("Miami, FL", "Miami, FL"),
    ("Atlanta, GA", "Atlanta, GA"),
    ("Seattle, WA", "Seattle, WA"),
    ("Denver, CO", "Denver, CO"),
    ("Houston, TX", "Houston, TX"),
]

vertical = get_vertical("social_only")
all_leads = []
seen_names = set()

print(f"Starting US search for businesses with only social pages across {len(US_MARKETS)} major US markets...")

for label, mkt in US_MARKETS:
    try:
        print(f"Querying {label}...")
        leads = run_pipeline(
            vertical,
            market=mkt,
            country="United States",
            sources=("overture", "osm"),
            limit=50,
            enrich=False,
            log=lambda m: None,
        )
        for lead in leads:
            # We want businesses that have ONLY a social page (Tier A)
            site = lead.get("website") or ""
            if is_social(site):
                key = (lead.get("name", "").strip().lower(), lead.get("phone", "").strip())
                if key not in seen_names and lead.get("name"):
                    seen_names.add(key)
                    all_leads.append(lead)
        print(f"  -> Total unique social-only leads found so far: {len(all_leads)}")
    except Exception as e:
        print(f"  Warning on {label}: {e}")

print(f"\nCompleted! Total social-only leads found in US: {len(all_leads)}")
