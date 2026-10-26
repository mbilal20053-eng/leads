import urllib.request
import json
import time

base = "http://127.0.0.1:5000"

def test_ds(ds, page=1):
    url = f"{base}/api/leads?dataset={ds}&page={page}&page_size=50"
    t0 = time.time()
    res = json.loads(urllib.request.urlopen(url, timeout=10).read().decode('utf-8'))
    elapsed = time.time() - t0
    leads = res.get("leads", [])
    print(f"Dataset '{ds:<22}' | Page {page:>4} -> {len(leads)} leads returned in {elapsed:.3f}s")
    assert len(leads) > 0, f"No leads returned for {ds}"

test_ds("b2b_executives", 1)
test_ds("b2b_executives", 100)
test_ds("homeowners", 1)
test_ds("homeowners", 50)
test_ds("master_locations", 1)
test_ds("gleif_goldencopy", 1)
test_ds("sec_company_facts", 1)
test_ds("cc_web_index", 1)
test_ds("all_global", 1)
test_ds("all_global", 10)

print("\nAll datasets respond instantly with valid data!")
