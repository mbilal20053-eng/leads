import duckdb

con = duckdb.connect()
count = con.execute("SELECT count(*) FROM read_parquet('d:/leads/homeowners.parquet')").fetchone()[0]
cols = [c[0] for c in con.execute("DESCRIBE SELECT * FROM read_parquet('d:/leads/homeowners.parquet')").fetchall()]
print(f"Rows: {count:,}")
print(f"Columns: {cols}")
sample = con.execute("SELECT * FROM read_parquet('d:/leads/homeowners.parquet') LIMIT 1").fetchall()
print("Sample:", sample)
