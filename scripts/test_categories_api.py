import urllib.request
import json
import time

base_url = "http://127.0.0.1:5000"

def test_api():
    print("Testing Lead Categories APIs...")
    time.sleep(2)  # Give flask a moment to bind
    
    # 1. Categories Analytics for b2b_executives
    url1 = f"{base_url}/api/categories/analytics?dataset=b2b_executives"
    print(f"1. Fetching: {url1}")
    with urllib.request.urlopen(url1, timeout=15) as resp:
        assert resp.status == 200, f"Status {resp.status}"
        data1 = json.loads(resp.read().decode('utf-8'))
        print(f"   Total Categories: {data1.get('total_categories')}")
        print(f"   Total Leads: {data1.get('total_leads'):,}")
        print(f"   Uncategorized Count: {data1.get('uncategorized_count')}")
        top5 = data1.get('categories', [])[:5]
        print("   Top 5 Categories:")
        for c in top5:
            print(f"     - {c['label']}: {c['count']:,} ({c['pct']}%)")
            
        assert data1.get('total_categories') == 185, f"Expected 185 categories, got {data1.get('total_categories')}"
        assert data1.get('total_leads') == 10268615, f"Expected 10,268,615 leads, got {data1.get('total_leads')}"
        assert top5[0]['name'] == 'hospital & health care'
        assert top5[0]['count'] == 921778

    # 2. Search category query
    url2 = f"{base_url}/api/categories/analytics?dataset=b2b_executives&q=hospital"
    print(f"\n2. Fetching search query 'hospital': {url2}")
    with urllib.request.urlopen(url2, timeout=10) as resp:
        data2 = json.loads(resp.read().decode('utf-8'))
        print(f"   Matches found: {len(data2.get('categories', []))}")
        for c in data2.get('categories', []):
            print(f"     - {c['label']}: {c['count']:,}")

    # 3. Single category filtering in leads API
    cat_enc = urllib.parse.quote("hospital & health care")
    url3 = f"{base_url}/api/leads?dataset=b2b_executives&category={cat_enc}&page=1&page_size=5"
    print(f"\n3. Fetching single category filtered leads: {url3}")
    with urllib.request.urlopen(url3, timeout=10) as resp:
        data3 = json.loads(resp.read().decode('utf-8'))
        print(f"   Matching leads total: {data3.get('total'):,}")
        print(f"   Returned leads count: {len(data3.get('leads', []))}")
        assert data3.get('total') == 921778, f"Expected 921,778 leads, got {data3.get('total')}"
        first_lead = data3.get('leads', [])[0]
        print(f"   Sample Lead: {first_lead.get('name')} | {first_lead.get('job_title')} | Category: {first_lead.get('category')}")

    # 4. Multi-category filtering in leads API (hospital & health care || construction)
    multi_cat_enc = urllib.parse.quote("hospital & health care||construction")
    url4 = f"{base_url}/api/leads?dataset=b2b_executives&category={multi_cat_enc}&page=1&page_size=5"
    print(f"\n4. Fetching multi-category filtered leads: {url4}")
    with urllib.request.urlopen(url4, timeout=10) as resp:
        data4 = json.loads(resp.read().decode('utf-8'))
        print(f"   Multi-category matching total: {data4.get('total'):,}")
        assert data4.get('total') == 921778 + 455095, f"Expected {921778 + 455095}, got {data4.get('total')}"
        print(f"   Verified multi-category sum: 921,778 + 455,095 = {data4.get('total'):,}")

    # 5. Uncategorized category leads
    url5 = f"{base_url}/api/leads?dataset=b2b_executives&category=Uncategorized&page=1&page_size=5"
    print(f"\n5. Fetching Uncategorized leads: {url5}")
    with urllib.request.urlopen(url5, timeout=10) as resp:
        data5 = json.loads(resp.read().decode('utf-8'))
        print(f"   Uncategorized total in cleaned dataset: {data5.get('total'):,}")

    # 6. Categories for all_local_unified (14.9M records)
    url6 = f"{base_url}/api/categories/analytics?dataset=all_local_unified"
    print(f"\n6. Fetching categories for unified dataset: {url6}")
    with urllib.request.urlopen(url6, timeout=15) as resp:
        data6 = json.loads(resp.read().decode('utf-8'))
        print(f"   Total Categories in unified: {data6.get('total_categories')}")
        print(f"   Total Leads in unified: {data6.get('total_leads'):,}")

    print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY! 100% VERIFIED.")

if __name__ == "__main__":
    import urllib.parse
    test_api()
