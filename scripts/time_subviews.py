import time
import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

subviews = ["v_b2b_executives", "v_homeowners", "v_open_company_db", "v_tech_stack_leads", 
            "v_master_locations", "v_realestate_b2b", "v_realtors", "v_entrepreneurs", 
            "v_designers", "v_coaches", "v_restaurants", "v_photographers", 
            "v_musicians", "v_gleif_goldencopy", "v_sec_company_facts", "v_cc_web_index"]

print("Timing SELECT 1 FROM each subview:")
for sv in subviews:
    t0 = time.time()
    try:
        con.execute(f"SELECT * FROM {sv} LIMIT 5").fetchall()
        print(f"  {sv:<25}: {time.time()-t0:.3f}s")
    except Exception as e:
        print(f"  {sv:<25}: ERROR {e}")
