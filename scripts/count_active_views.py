import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

views = [
    ("v_b2b_executives", "b2b_executives"),
    ("v_homeowners", "homeowners"),
    ("v_open_company_db", "open_company_db"),
    ("v_tech_stack_leads", "tech_stack_leads"),
    ("v_master_locations", "master_locations"),
    ("v_realestate_b2b", "realestate_b2b"),
    ("v_realtors", "realtors"),
    ("v_entrepreneurs", "entrepreneurs"),
    ("v_designers", "designers"),
    ("v_coaches", "coaches"),
    ("v_restaurants", "restaurants"),
    ("v_photographers", "photographers"),
    ("v_musicians", "musicians"),
    ("v_gleif_goldencopy", "gleif_goldencopy"),
    ("v_sec_company_facts", "sec_company_facts"),
    ("v_cc_web_index", "cc_web_index")
]

print("Actual physical rows in each DuckDB view:")
total_fast = 0
for v, name in views:
    try:
        cnt = con.execute(f"SELECT count(*) FROM {v}").fetchone()[0]
        total_fast += cnt
        print(f"  {v:<25}: {cnt:>12,}")
    except Exception as e:
        print(f"  {v:<25}: ERROR {e}")

print(f"Sum of active indexed local views: {total_fast:,}")
