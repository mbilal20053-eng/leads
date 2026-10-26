"""
CHECK IF b2b_executives.parquet IS A 1-TO-1 ROW-FOR-ROW ETL CONVERSION OF THE 18 SHARDS
"""
import duckdb
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()

f_exec_orig = r"d:\leads\b2b_executives.parquet".replace("\\", "/")

# Total rows in b2b_executives.parquet
cnt = con.execute(f"SELECT count(*) FROM read_parquet('{f_exec_orig}')").fetchone()[0]
print(f"Total rows in original b2b_executives.parquet: {cnt:,}")

# Check sample of b2b_executives.parquet
desc = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{f_exec_orig}')").fetchall()
print("Columns:")
for d in desc:
    print(f"  {d[0]}: {d[1]}")

# Check source_badge or source_id
print("\nDistinct source_badge values in b2b_executives.parquet:")
res_badge = con.execute(f"SELECT source_badge, count(*) FROM read_parquet('{f_exec_orig}') GROUP BY 1").fetchall()
for r in res_badge:
    print(f"  {r[0]}: {r[1]:,}")

