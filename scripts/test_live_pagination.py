import urllib.request
import json
import time

base = "http://127.0.0.1:5000"

def test_page(dataset, page):
    url = f"{base}/api/leads?dataset={dataset}&page={page}&page_size=50"
    t0 = time.time()
    res = json.loads(urllib.request.urlopen(url, timeout=10).read().decode('utf-8'))
    elapsed = time.time() - t0
    leads = res.get("leads", [])
    print(f"Dataset '{dataset}' | Page {page:>8} -> {len(leads)} leads returned in {elapsed:.3f}s (Total: {res.get('total'):,})")
    assert len(leads) == 50, f"Expected 50 leads, got {len(leads)}"

print("Testing live Flask pagination after fix:")
test_page("all_local_unified", 1)
test_page("all_local_unified", 2)
test_page("all_local_unified", 10)
test_page("all_local_unified", 500)
test_page("all_local_unified", 4506545)
test_page("all_local_unified", 4506546)

print("\nSUCCESS: All pages return 50 leads with zero delay and no empty tables!")
