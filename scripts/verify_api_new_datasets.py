import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

datasets = [
    "all_global",
    "all_local_unified",
    "data_legion_companies",
    "open_company_db",
    "master_locations",
    "b2b_executives",
    "homeowners",
    "realestate_b2b"
]

print("=== TESTING DASHBOARD API FOR NEW & EXISTING DATASETS ===")
for ds in datasets:
    try:
        url = f"http://127.0.0.1:5000/api/leads?dataset={ds}&page=1&page_size=10"
        req = urllib.request.urlopen(url, timeout=10)
        d = json.loads(req.read().decode("utf-8"))
        leads = d.get("leads", [])
        tot = d.get("total")
        name = d.get("dataset_name")
        first_lead = leads[0]["name"] if leads else "EMPTY"
        first_badge = leads[0].get("source_badge", "") if leads else ""
        print(f"[{ds:<22}] -> OK | Total={tot:,} | Leads Returned={len(leads)} | Sample: [{first_badge}] {first_lead}")
    except Exception as e:
        print(f"[{ds:<22}] -> ERROR: {e}")

# Check all_global page 1 source distribution
print("\n=== ALL_GLOBAL PAGE 1 DIVERSE COMPOSITION ===")
url = "http://127.0.0.1:5000/api/leads?dataset=all_global&page=1&page_size=50"
req = urllib.request.urlopen(url, timeout=10)
d = json.loads(req.read().decode("utf-8"))
leads = d.get("leads", [])
print(f"Total leads returned: {len(leads)}")
sources = {}
for l in leads:
    b = l.get("source_badge", "None")
    sources[b] = sources.get(b, 0) + 1
for s, cnt in sources.items():
    print(f"  {s:<32}: {cnt} leads")
