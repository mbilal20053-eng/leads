import time
import duckdb

con = duckdb.connect()

# Create unified view of only the fast parquet & csv tables (16.2M rows)
views = [
    "d:/leads/b2b_executives.parquet",
    "d:/leads/homeowners.parquet",
    "d:/leads/gleif_goldencopy.parquet",
    "d:/leads/open_company_database.parquet",
    "d:/leads/tech_stack_companies.parquet",
    "d:/leads/sec_company_facts.parquet",
    "d:/leads/cc_web_index.parquet"
]

print("Testing direct parquet query speed:")
t0 = time.time()
res1 = con.execute("SELECT count(*) FROM read_parquet('d:/leads/b2b_executives.parquet')").fetchone()[0]
print(f"B2B Executives count: {res1:,} in {time.time()-t0:.3f}s")

t0 = time.time()
res2 = con.execute("SELECT id, name FROM read_parquet('d:/leads/b2b_executives.parquet') LIMIT 50 OFFSET 1000000").fetchall()
print(f"Offset 1,000,000 on Parquet: {len(res2)} rows in {time.time()-t0:.3f}s")

t0 = time.time()
res3 = con.execute("SELECT id, name FROM read_parquet('d:/leads/b2b_executives.parquet') LIMIT 50 OFFSET 10000000").fetchall()
print(f"Offset 10,000,000 on Parquet: {len(res3)} rows in {time.time()-t0:.3f}s")
