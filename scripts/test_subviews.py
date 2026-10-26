import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

print("Testing query on v_all_unified...")
views = [
    "v_b2b_executives", "v_homeowners", "v_open_company_db", "v_tech_stack_leads", 
    "v_master_locations", "v_free_company_db", "v_realestate_b2b", "v_realtors", 
    "v_entrepreneurs", "v_designers", "v_coaches", "v_restaurants", 
    "v_photographers", "v_musicians", "v_gleif_goldencopy", "v_sec_company_facts", "v_cc_web_index"
]

print("Checking which subviews are in v_all_unified:")
for v in views:
    try:
        r = con.execute(f"SELECT count(*) FROM {v} LIMIT 1").fetchone()
        print(f"  {v}: OK")
    except Exception as e:
        print(f"  {v}: ERROR - {e}")
