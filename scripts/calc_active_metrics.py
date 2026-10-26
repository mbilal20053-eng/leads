import os
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure repo is in sys.path
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

print("=" * 80)
print("  ACCURATE METRICS FROM ACTIVE DUCKDB VIEWS")
print("=" * 80)

# Check homeowners
ho_stats = con.execute("""
    SELECT 
        count(*) as total,
        count(case when tier = 'A' then 1 end) as tier_a,
        count(case when tier = 'B' then 1 end) as tier_b,
        count(case when phone != '' then 1 end) as with_phone,
        count(case when website != '' then 1 end) as with_website,
        count(case when email != '' then 1 end) as with_email
    FROM v_homeowners
""").fetchone()
print(f"v_homeowners: Total={ho_stats[0]:,}, Tier A={ho_stats[1]:,}, Tier B={ho_stats[2]:,}, Phone={ho_stats[3]:,}, Web={ho_stats[4]:,}, Email={ho_stats[5]:,}")

# Check master_locations
ml_stats = con.execute("""
    SELECT 
        count(*) as total,
        count(case when tier = 'A' then 1 end) as tier_a,
        count(case when tier = 'B' then 1 end) as tier_b,
        count(case when phone != '' then 1 end) as with_phone,
        count(case when website != '' then 1 end) as with_website,
        count(case when email != '' then 1 end) as with_email
    FROM v_master_locations
""").fetchone()
print(f"v_master_locations: Total={ml_stats[0]:,}, Tier A={ml_stats[1]:,}, Tier B={ml_stats[2]:,}, Phone={ml_stats[3]:,}, Web={ml_stats[4]:,}, Email={ml_stats[5]:,}")

# Check all individual views in v_all_unified
print("\nIndividual subviews in v_all_unified:")
views = [
    "v_b2b_executives", "v_homeowners", "v_open_company_db", "v_tech_stack_leads", 
    "v_master_locations", "v_free_company_db", "v_realestate_b2b", "v_realtors", 
    "v_entrepreneurs", "v_designers", "v_coaches", "v_restaurants", 
    "v_photographers", "v_musicians", "v_gleif_goldencopy", "v_sec_company_facts", "v_cc_web_index"
]

tot_sub = 0
for v in views:
    try:
        cnt = con.execute(f"SELECT count(*) FROM {v}").fetchone()[0]
        tot_sub += cnt
        print(f"  {v:<25}: {cnt:>12,}")
    except Exception as e:
        print(f"  {v:<25}: ERROR {e}")

print(f"--> Sum of subviews: {tot_sub:,}")

# Check v_all_unified
uni_stats = con.execute("""
    SELECT 
        count(*) as total,
        count(case when tier = 'A' then 1 end) as tier_a,
        count(case when tier = 'B' then 1 end) as tier_b,
        count(case when phone != '' then 1 end) as with_phone,
        count(case when website != '' then 1 end) as with_website,
        count(case when email != '' then 1 end) as with_email
    FROM v_all_unified
""").fetchone()

print(f"\nv_all_unified: Total={uni_stats[0]:,}, Tier A={uni_stats[1]:,}, Tier B={uni_stats[2]:,}, Phone={uni_stats[3]:,}, Web={uni_stats[4]:,}, Email={uni_stats[5]:,}")
