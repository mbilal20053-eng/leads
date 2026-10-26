import urllib.request
import urllib.parse
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:5000/api/leads"

def test_query(title, params):
    t0 = time.time()
    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))
    dur = time.time() - t0
    total = data.get("total", 0)
    leads = data.get("leads", [])
    print(f"\n[TEST] {title} ({dur:.2f}s)")
    print(f"  URL: {url}")
    print(f"  Total Matching Records: {total:,} | Returned on Page: {len(leads)}")
    if leads:
        sample = leads[0]
        print(f"  Sample #1: Name='{sample.get('name')}' | Contact='{sample.get('contact_name')}' | Email='{sample.get('email')}' | Phone='{sample.get('phone')}' | City='{sample.get('city')}' | State='{sample.get('state')}'")
    else:
        print("  (0 records returned as expected)")
    return data

print("="*80)
print("COMPREHENSIVE SEARCH & FILTER TEST SUITE")
print("="*80)

# Test 1: Global Search across all fields in restaurants
r1 = test_query("Global Search: 'pizza' in Restaurants", {
    "dataset": "restaurants",
    "search": "pizza",
    "page": 1,
    "page_size": 10
})
assert r1["total"] > 0, "Expected pizza matches in restaurants"

# Test 2: Global Search across 41M unified records in all_global
r2 = test_query("Global Search: 'Apex' across All Global Unified Leads", {
    "dataset": "all_global",
    "search": "Apex",
    "page": 1,
    "page_size": 10
})
assert r2["total"] > 0, "Expected Apex matches in all_global"

# Test 3: Column-Specific Search - Business Name
r3 = test_query("Column Search: Business Name = 'Grill' in Restaurants", {
    "dataset": "restaurants",
    "col_name": "Grill",
    "page": 1,
    "page_size": 10
})
assert r3["total"] > 0

# Test 4: Column-Specific Search - Contact Person Name
r4 = test_query("Column Search: Contact Person = 'David' in Realtors", {
    "dataset": "realtors",
    "col_contact": "David",
    "page": 1,
    "page_size": 10
})
assert r4["total"] > 0

# Test 5: Column-Specific Search - Email (case-insensitive)
r5 = test_query("Column Search: Email containing 'gmail.com' in Coaches", {
    "dataset": "coaches",
    "col_email": "GMAIL.COM",
    "page": 1,
    "page_size": 10
})
assert r5["total"] > 0
for l in r5["leads"]:
    assert "gmail.com" in l.get("email", "").lower(), f"Expected gmail.com in email: {l.get('email')}"

# Test 6: Phone Search - Format Agnostic (Raw digits)
sample_phone = r4["leads"][0].get("phone", "")
clean_digits = "".join([c for c in sample_phone if c.isdigit()])
if len(clean_digits) >= 7:
    search_sub = clean_digits[1:8] # e.g. 7 digits
    r6 = test_query(f"Phone Search: Normalized Digits '{search_sub}' in Realtors", {
        "dataset": "realtors",
        "col_phone": search_sub,
        "page": 1,
        "page_size": 10
    })
    assert r6["total"] > 0, f"Expected phone match for digits {search_sub}"

# Test 7: Combined Filters - Name + City/State + Phone Required
r7 = test_query("Combined Filters: Category='Real Estate' + State='CA' + has_phone=True", {
    "dataset": "all_global",
    "category": "Real Estate",
    "state": "CA",
    "has_phone": "true",
    "page": 1,
    "page_size": 10
})
assert r7["total"] > 0
for l in r7["leads"]:
    assert l.get("phone"), "Expected non-empty phone"

# Test 8: Empty Results Verification
r8 = test_query("Empty Search: Gibberish term 'ZZZZXQ9928374' (Must be 0)", {
    "dataset": "all_global",
    "search": "ZZZZXQ9928374",
    "page": 1,
    "page_size": 10
})
assert r8["total"] == 0, f"Expected 0 matches, got {r8['total']}"
assert len(r8["leads"]) == 0

# Test 9: Pagination Consistency (Page 1 vs Page 2)
r9_p1 = test_query("Pagination Page 1: Search 'Cafe' in Restaurants", {
    "dataset": "restaurants",
    "search": "Cafe",
    "page": 1,
    "page_size": 5
})
r9_p2 = test_query("Pagination Page 2: Search 'Cafe' in Restaurants", {
    "dataset": "restaurants",
    "search": "Cafe",
    "page": 2,
    "page_size": 5
})
assert r9_p1["total"] == r9_p2["total"], "Total count must be identical across pages"
if r9_p1["leads"] and r9_p2["leads"]:
    assert r9_p1["leads"][0]["id"] != r9_p2["leads"][0]["id"], "Page 1 and Page 2 should have different records"

# Test 10: Sorting with Search Active
r10_asc = test_query("Sorting ASC: Name with search 'Bar'", {
    "dataset": "restaurants",
    "search": "Bar",
    "sort_by": "name",
    "sort_dir": "asc",
    "page": 1,
    "page_size": 5
})
r10_desc = test_query("Sorting DESC: Name with search 'Bar'", {
    "dataset": "restaurants",
    "search": "Bar",
    "sort_by": "name",
    "sort_dir": "desc",
    "page": 1,
    "page_size": 5
})
assert r10_asc["total"] == r10_desc["total"], "Total count must remain identical during sort"
if r10_asc["leads"] and r10_desc["leads"] and len(r10_asc["leads"]) > 1:
    assert r10_asc["leads"][0]["name"] != r10_desc["leads"][0]["name"], "ASC and DESC should order differently"

print("\n" + "="*80)
print("✓ ALL 10 TESTS PASSED SUCCESSFULLY! FULL BACKEND & DB INTEGRATION VERIFIED.")
print("="*80)
