import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

def test_api():
    print("Testing /api/leads?dataset=all_global...")
    url = "http://127.0.0.1:5000/api/leads?dataset=all_global&page=1&page_size=10"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print(f"Status: {response.status}")
        print(f"Total leads returned: {data.get('total')}")
        print(f"Stats total: {data.get('stats', {}).get('total')}")
        print(f"Dataset name: {data.get('dataset_name')}")
        print(f"Number of leads on page 1: {len(data.get('leads', []))}")
        if data.get('leads'):
            first_lead = data['leads'][0]
            print(f"Sample lead #1: Name='{first_lead.get('name')}', SourceBadge='{first_lead.get('source_badge')}', Cat='{first_lead.get('category')}'")

def test_html():
    print("\nTesting / for banner and headers...")
    url = "http://127.0.0.1:5000/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")
        banner_match = re.search(r'id="bannerTotalCount">([^<]+)<', html)
        if banner_match:
            print(f"Banner total count in HTML: {banner_match.group(1)}")
        else:
            print("Banner total count not found in HTML!")
        
        script_match = re.search(r'<script src="(/static/app.js[^"]+)"', html)
        if script_match:
            print(f"Script tag in HTML: {script_match.group(1)}")

        # Check th headers
        ths = re.findall(r'<th[^>]*>(.*?)</th>', html, re.DOTALL)
        clean_ths = [re.sub(r'<[^>]+>', '', t).strip() for t in ths]
        print(f"Table headers found ({len(clean_ths)}): {clean_ths}")

if __name__ == "__main__":
    test_api()
    test_html()
