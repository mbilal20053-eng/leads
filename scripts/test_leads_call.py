import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:5000/api/leads?dataset=all_global&page=1&page_size=50&search=&tier=all&state=all&country=all&major_category=all&category=all&crm_status=all&opportunity=all&has_phone=false&sort_by=&sort_dir=asc"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("Keys in response:", list(data.keys()))
    print("Total:", data.get("total"))
    leads = data.get("leads", [])
    print("Leads array length:", len(leads))
    for i, l in enumerate(leads[:5]):
        print(f"Lead #{i+1}: {l.get('name')} | Contact: {l.get('contact_name')} | Cat: {l.get('category')} | Source: {l.get('source_badge')}")
