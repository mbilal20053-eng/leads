import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

print("Testing DuckDB query on v_all_unified without where clause:")
try:
    r = con.execute("SELECT id, name, source_badge FROM v_all_unified LIMIT 5 OFFSET 0").fetchall()
    print("Page 1 (offset 0):", r)
except Exception as e:
    print("Error:", e)
