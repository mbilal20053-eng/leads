import time
import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

t0 = time.time()
r = con.execute("SELECT * FROM v_all_unified LIMIT 50 OFFSET 100").fetchall()
print(f"Raw DuckDB query alone: {time.time()-t0:.3f}s")

t0 = time.time()
res = lead_db.query_local_view_leads("v_all_unified", "all_local_unified", "Local Unified", page=2, page_size=50)
print(f"Full query_local_view_leads: {time.time()-t0:.3f}s")
