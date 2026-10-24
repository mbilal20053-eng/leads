import urllib.request
import json

base = "http://127.0.0.1:5000/api/leads?dataset=all_global&page=1&page_size=10"

test_params = [
    "",
    "&tier=all",
    "&state=all",
    "&country=all",
    "&major_category=all",
    "&category=all",
    "&crm_status=all",
    "&opportunity=all",
    "&has_phone=false",
    "&sort_by=",
    "&sort_dir=asc",
]

full_url = base
for p in test_params:
    full_url += p
    with urllib.request.urlopen(full_url) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"With {p:<25}: leads count = {len(data.get('leads', []))}")
