import time
import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

print("Testing DuckDB query on v_all_unified...")
t0 = time.time()
try:
    # Test page 1
    t1 = time.time()
    r1 = con.execute("SELECT id, name FROM v_all_unified LIMIT 50 OFFSET 0").fetchall()
    print(f"Page 1 (offset 0): {len(r1)} rows in {time.time()-t1:.3f}s")
    
    # Test page 1000
    t2 = time.time()
    r2 = con.execute("SELECT id, name FROM v_all_unified LIMIT 50 OFFSET 50000").fetchall()
    print(f"Page 1000 (offset 50000): {len(r2)} rows in {time.time()-t2:.3f}s")

    # Test what the total row count of v_all_unified ACTUALLY is!
    # Let's count each subview
    for sv in ["v_b2b_executives", "v_homeowners", "v_open_company_db", "v_tech_stack_leads", 
               "v_master_locations", "v_free_company_db", "v_realestate_b2b", "v_realtors", 
               "v_entrepreneurs", "v_designers", "v_coaches", "v_restaurants", 
               "v_photographers", "v_musicians", "v_gleif_goldencopy", "v_sec_company_facts", "v_cc_web_index"]:
        try:
            cnt = con.execute(f"SELECT count(*) FROM {sv}").fetchone()[0]
            print(f"  {sv}: {cnt:,}")
        except Exception as e:
            print(f"  {sv}: ERROR {e}")
            
except Exception as e:
    print("Error:", e)
