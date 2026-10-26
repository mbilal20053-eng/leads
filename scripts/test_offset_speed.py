import time
import duckdb

con = duckdb.connect()

con.execute("""
CREATE OR REPLACE VIEW v_test AS
SELECT id, name FROM read_parquet('d:/leads/b2b_executives.parquet')
""")

t0 = time.time()
r = con.execute("SELECT id, name FROM v_test LIMIT 50 OFFSET 77200").fetchall()
elapsed = time.time() - t0
print(f"Retrieved {len(r)} rows at offset 77,200 in {elapsed*1000:.1f} milliseconds!")
