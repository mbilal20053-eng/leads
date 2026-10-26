import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "http://127.0.0.1:5000"

def get(path):
    url = f"{base_url}{path}"
    req = urllib.request.urlopen(url, timeout=10)
    return json.loads(req.read().decode('utf-8'))

print("=" * 80)
print("  LEAD ENGINE PRO - FINAL SYSTEM METRICS VERIFICATION (POST-CORRECTION)")
print("=" * 80)

# 1. Dashboard Metrics
dash = get("/api/dashboard_metrics")
print("\n[1] /api/dashboard_metrics:")
print(f"  Total Portfolio     : {dash['total_portfolio']:,} (Expected: 918,282,632)")
print(f"  Local Records       : {dash['local_records']:,} (Expected: 224,052,222)")
print(f"  Unique Verified     : {dash['unique_verified_records']:,} (Expected: 224,052,222)")
print(f"  Duplicates Removed  : {dash['duplicates_removed']:,} (Expected: 410,339)")
print(f"  Dataset Count       : {dash['dataset_count']}")

assert dash['total_portfolio'] == 918282632, f"Mismatch: {dash['total_portfolio']}"
assert dash['local_records'] == 224052222, f"Mismatch: {dash['local_records']}"
assert dash['duplicates_removed'] == 410339, f"Mismatch: {dash['duplicates_removed']}"

# 2. Duplicates Summary
dup_sum = get("/api/duplicates/summary")
print("\n[2] /api/duplicates/summary:")
print(f"  Total Exact Removed : {dup_sum['total_exact_removed']:,}")
print(f"  Remaining Unique    : {dup_sum['remaining_unique']:,}")
assert dup_sum['total_exact_removed'] == 410339
assert dup_sum['remaining_unique'] == 224052222

# 3. Test Homeowners View
ho = get("/api/leads?dataset=homeowners&page=1&page_size=2")
print("\n[3] Homeowners View (/api/leads?dataset=homeowners):")
print(f"  Total Rows: {ho['total']:,} (Expected: 703,772)")
print(f"  Returned Leads: {len(ho['leads'])}")
print(f"  Sample: {ho['leads'][0]['name']} | Phone: {ho['leads'][0]['phone']}")
assert ho['total'] == 703772, f"Expected 703,772, got {ho['total']}"

# 4. Test Master Locations View
ml = get("/api/leads?dataset=master_locations&page=1&page_size=2")
print("\n[4] Master Locations View (/api/leads?dataset=master_locations):")
print(f"  Total Rows: {ml['total']:,} (Expected: 154,710)")
print(f"  Returned Leads: {len(ml['leads'])}")
print(f"  Sample: {ml['leads'][0]['name']} | Website: {ml['leads'][0]['website']}")
assert ml['total'] == 154710, f"Expected 154,710, got {ml['total']}"

# 5. Test Unified Local View
all_local = get("/api/leads?dataset=all_local_unified&page=1&page_size=2")
print("\n[5] Unified Local View (/api/leads?dataset=all_local_unified):")
print(f"  Total Rows: {all_local['total']:,} (Expected: 224,052,222)")
print(f"  Returned Leads: {len(all_local['leads'])}")
assert all_local['total'] == 224052222, f"Expected 224,052,222, got {all_local['total']}"

# 6. Test Global Master View
all_global = get("/api/leads?dataset=all_global&page=1&page_size=2")
print("\n[6] Global Master View (/api/leads?dataset=all_global):")
print(f"  Total Rows: {all_global['total']:,} (Expected: 918,282,632)")
print(f"  Returned Leads: {len(all_global['leads'])}")
assert all_global['total'] == 918282632, f"Expected 918,282,632, got {all_global['total']}"

# 7. Test B2B Executives View
b2b = get("/api/leads?dataset=b2b_executives&page=1&page_size=2")
print("\n[7] B2B Executives View (/api/leads?dataset=b2b_executives):")
print(f"  Total Rows: {b2b['total']:,} (Expected: 10,268,615)")
print(f"  Returned Leads: {len(b2b['leads'])}")
print(f"  Sample: {b2b['leads'][0]['name']} | Contact: {b2b['leads'][0].get('contact_name', '')}")
assert b2b['total'] == 10268615, f"Expected 10,268,615, got {b2b['total']}"

# 8. Test GLEIF Golden Copy View
gleif = get("/api/leads?dataset=gleif_goldencopy&page=1&page_size=2")
print("\n[8] GLEIF Golden Copy View (/api/leads?dataset=gleif_goldencopy):")
print(f"  Total Rows: {gleif['total']:,} (Expected: 3,472,837)")
assert gleif['total'] == 3472837

# 9. Test SEC EDGAR Public Facts
facts = get("/api/leads?dataset=sec_company_facts&page=1&page_size=2")
print("\n[9] SEC Facts View (/api/leads?dataset=sec_company_facts):")
print(f"  Total Rows: {facts['total']:,} (Expected: 20,501)")
assert facts['total'] == 20501

# 10. Test CC Web Index
cc = get("/api/leads?dataset=cc_web_index&page=1&page_size=2")
print("\n[10] Common Crawl Index View (/api/leads?dataset=cc_web_index):")
print(f"  Total Rows: {cc['total']:,} (Expected: 302)")
assert cc['total'] == 302

print("\n" + "=" * 80)
print("  ALL VERIFICATION TESTS PASSED 100% PERFECTLY!")
print("=" * 80)
