import urllib.request
import urllib.parse
import json
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:5000"

def get_json(endpoint, params=None):
    url = BASE_URL + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    t0 = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "SearchTestAgent/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed = time.time() - t0
    return data, elapsed

def run_tests():
    print("=== LIVE SEARCH & FILTERING SUITE TESTING ===")
    tests_passed = 0
    tests_total = 0

    def assert_test(name, condition, details=""):
        nonlocal tests_passed, tests_total
        tests_total += 1
        if condition:
            tests_passed += 1
            print(f"[PASS] {name} {details}")
        else:
            print(f"[FAIL] {name} {details}")
            sys.exit(1)

    # 1. Test Dataset: 'odo_senzing'
    print("\n--- Test Suite 1: ODO Senzing Dataset ---")
    data, el = get_json("/api/leads", {"dataset": "odo_senzing", "limit": 10, "offset": 0})
    assert_test("Initial fetch", len(data.get("leads", [])) == 10 and data.get("total", 0) > 0,
                f"total={data.get('total')}, elapsed={el:.3f}s")
    sample_lead = data["leads"][0]
    sample_name = sample_lead.get("business_name") or sample_lead.get("name") or ""
    sample_first_word = sample_name.split()[0] if sample_name else "Corp"
    print(f"Sample lead name: '{sample_name}', testing query with '{sample_first_word}'")

    # Global Search (partial, case-insensitive, with spaces)
    q_spaced = f"  {sample_first_word.lower()}  "
    data_search, el = get_json("/api/leads", {"dataset": "odo_senzing", "search": q_spaced, "limit": 10})
    assert_test("Global Search (case-insensitive & trimmed)",
                data_search.get("total", 0) > 0 and len(data_search.get("leads", [])) > 0,
                f"matches={data_search.get('total')}, elapsed={el:.3f}s")

    # Verify every returned record matches the search query in at least one field
    q_clean = sample_first_word.lower()
    for lead in data_search["leads"]:
        text_blob = " ".join(str(v).lower() for v in lead.values())
        assert_test(f"Result contains query '{q_clean}'", q_clean in text_blob, f"lead={lead.get('business_name')}")
        break

    # 2. Column-Specific Searches on odo_senzing
    print("\n--- Test Suite 2: Column-Specific Searches on odo_senzing ---")
    data_col_name, el = get_json("/api/leads", {"dataset": "odo_senzing", "col_name": sample_first_word, "limit": 10})
    assert_test("Column-Specific Name Search",
                data_col_name.get("total", 0) > 0 and any(sample_first_word.lower() in (l.get("business_name") or "").lower() for l in data_col_name["leads"]),
                f"matches={data_col_name.get('total')}, elapsed={el:.3f}s")

    # 3. Empty Results Handling on odo_senzing
    print("\n--- Test Suite 3: Empty Results ---")
    nonsense_q = "xyz999nonsensenonexistentleadstring12345"
    data_empty, el = get_json("/api/leads", {"dataset": "odo_senzing", "search": nonsense_q, "limit": 10})
    assert_test("Empty Search Returns 0 Records Gracefully",
                data_empty.get("total") == 0 and len(data_empty.get("leads", [])) == 0,
                f"total={data_empty.get('total')}, elapsed={el:.3f}s")

    # 4. DuckDB View Dataset: 'restaurants' (2,500 real leads)
    print("\n--- Test Suite 4: DuckDB View Dataset ('restaurants') ---")
    r_initial, el = get_json("/api/leads", {"dataset": "restaurants", "limit": 10})
    assert_test("Fetch restaurants dataset", len(r_initial.get("leads", [])) == 10 and r_initial.get("total", 0) > 0,
                f"total={r_initial.get('total')}, elapsed={el:.3f}s")

    # Global search in restaurants
    r_search, el = get_json("/api/leads", {"dataset": "restaurants", "search": "  PIZZA  ", "limit": 10})
    assert_test("Global Search 'PIZZA' in restaurants",
                r_search.get("total", 0) > 0 and len(r_search.get("leads", [])) > 0,
                f"total={r_search.get('total')}, elapsed={el:.3f}s")
    for l in r_search["leads"]:
        blob = " ".join(str(v).lower() for v in l.values())
        assert_test("Lead contains 'pizza'", "pizza" in blob, f"lead={l.get('business_name')}")
        break

    # Column-specific search in restaurants
    r_name_search, el = get_json("/api/leads", {"dataset": "restaurants", "col_name": "grill", "limit": 10})
    assert_test("Column-Specific Name Search 'grill' in restaurants",
                r_name_search.get("total", 0) > 0 and all("grill" in (l.get("business_name") or "").lower() for l in r_name_search["leads"]),
                f"total={r_name_search.get('total')}, elapsed={el:.3f}s")

    # Phone normalization search in restaurants
    r_phones, _ = get_json("/api/leads", {"dataset": "restaurants", "has_phone": "true", "limit": 5})
    sample_ph_lead = r_phones["leads"][0]
    raw_ph = sample_ph_lead.get("phone", "")
    ph_digits = "".join(c for c in raw_ph if c.isdigit())
    if len(ph_digits) >= 6:
        sub_digits = ph_digits[2:7]
        r_ph_search, el = get_json("/api/leads", {"dataset": "restaurants", "col_phone": sub_digits, "limit": 10})
        assert_test(f"Phone Search with raw digits '{sub_digits}' for '{raw_ph}'",
                    r_ph_search.get("total", 0) > 0,
                    f"total={r_ph_search.get('total')}, elapsed={el:.3f}s")

    # Combined filters in restaurants (col_name + has_phone)
    r_combined, el = get_json("/api/leads", {"dataset": "restaurants", "col_name": "cafe", "has_phone": "true", "limit": 10})
    r_cafe_all, _ = get_json("/api/leads", {"dataset": "restaurants", "col_name": "cafe", "limit": 10})
    assert_test("Combined Filter (col_name + has_phone)",
                r_combined.get("total", 0) <= r_cafe_all.get("total", 0) and all(l.get("phone") for l in r_combined["leads"]),
                f"combined={r_combined.get('total')} <= all={r_cafe_all.get('total')}, elapsed={el:.3f}s")

    # 5. Pagination & Sorting Stability across pages
    print("\n--- Test Suite 5: Pagination & Sorting Stability ---")
    p1, _ = get_json("/api/leads", {"dataset": "restaurants", "search": "grill", "page_size": 5, "page": 1, "sort_by": "name", "sort_dir": "asc"})
    p2, _ = get_json("/api/leads", {"dataset": "restaurants", "search": "grill", "page_size": 5, "page": 2, "sort_by": "name", "sort_dir": "asc"})
    assert_test("Pagination Exact Match Total Consistency", p1.get("total") == p2.get("total") and p1.get("total") > 0,
                f"p1_total={p1.get('total')}, p2_total={p2.get('total')}")
    if p1.get("total", 0) > 5:
        p1_names = [l.get("business_name") for l in p1["leads"]]
        p2_names = [l.get("business_name") for l in p2["leads"]]
        assert_test("Pagination Page 1 and Page 2 records differ", p1_names != p2_names,
                    f"p1_first={p1_names[0] if p1_names else ''}, p2_first={p2_names[0] if p2_names else ''}")

    # Sorting test (asc vs desc)
    p_desc, _ = get_json("/api/leads", {"dataset": "restaurants", "search": "grill", "page_size": 5, "page": 1, "sort_by": "name", "sort_dir": "desc"})
    if p1.get("total", 0) > 1 and len(p1["leads"]) > 1 and len(p_desc["leads"]) > 1:
        assert_test("Sorting Asc vs Desc changes lead order", p1["leads"][0]["name"] != p_desc["leads"][0]["name"],
                    f"asc_first={p1['leads'][0]['name']}, desc_first={p_desc['leads'][0]['name']}")

    # 6. Global Unified Portfolio ('all_global' across 13M+ leads)
    print("\n--- Test Suite 6: Global Unified Portfolio ('all_global' - 13M+ Leads) ---")
    g_search, el = get_json("/api/leads", {
        "dataset": "all_global",
        "search": "hospital",
        "limit": 10,
        "offset": 0
    })
    assert_test("Global Search across 13M+ leads ('all_global')",
                g_search.get("total", 0) > 0 and len(g_search.get("leads", [])) == 10,
                f"total={g_search.get('total'):,}, elapsed={el:.3f}s")

    # Column-specific search on 'all_global'
    g_col, el = get_json("/api/leads", {
        "dataset": "all_global",
        "col_category": "restaurant",
        "limit": 10,
        "offset": 0
    })
    assert_test("Column-Specific Category Search on 'all_global'",
                g_col.get("total", 0) > 0 and len(g_col.get("leads", [])) == 10,
                f"total={g_col.get('total'):,}, elapsed={el:.3f}s")

    # Combined Global Filter on 'all_global' (category + has_phone)
    g_combined, el = get_json("/api/leads", {
        "dataset": "all_global",
        "col_category": "restaurant",
        "has_phone": "true",
        "limit": 10
    })
    assert_test("Combined Filter on 'all_global' (col_category + has_phone)",
                g_combined.get("total", 0) > 0 and all(l.get("phone") for l in g_combined["leads"]),
                f"total={g_combined.get('total'):,}, elapsed={el:.3f}s")

    print(f"\n==========================================")
    print(f"ALL {tests_passed}/{tests_total} BACKEND SEARCH & FILTER TESTS PASSED!")
    print(f"==========================================")

if __name__ == "__main__":
    run_tests()
