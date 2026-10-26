import time
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

print("Testing DuckDB query at offset 225,327,200...")
t0 = time.time()
try:
    r = con.execute("SELECT id, name FROM v_all_unified LIMIT 50 OFFSET 225327200").fetchall()
    print(f"Result count: {len(r)} in {time.time()-t0:.2f}s")
except Exception as e:
    print("Error:", e)
