import os
import duckdb

con = duckdb.connect()

print("=" * 80)
print("CHECKING ROOT PARQUET DATASETS IN D:\\leads\\")
print("=" * 80)

root_parquets = [
    r'D:\leads\gleif_goldencopy.parquet',
    r'D:\leads\sec_company_facts.parquet',
    r'D:\leads\cc_web_index.parquet',
    r'D:\leads\homeowners.parquet',
    r'D:\leads\open_company_database.parquet',
    r'D:\leads\tech_stack_companies.parquet',
    r'D:\leads\b2b_executives.parquet'
]

for f in root_parquets:
    if os.path.exists(f):
        cnt = con.execute(f"SELECT count(*) FROM '{f}'").fetchone()[0]
        size_mb = os.path.getsize(f) / (1024 * 1024)
        print(f"[ACCESSIBLE] {os.path.basename(f)}")
        print(f"             Size: {size_mb:.2f} MB | Exact Rows: {cnt:,}")
    else:
        print(f"[MISSING] {os.path.basename(f)}")

print("\n" + "=" * 80)
print("INSPECTING free_company_dataset.csv.zip FORMAT")
print("=" * 80)

p = r'D:\leads\free_company_dataset.csv.zip'
if os.path.exists(p):
    size_mb = os.path.getsize(p) / (1024 * 1024)
    with open(p, 'rb') as fp:
        header = fp.read(64)
        print(f"Path: {p}")
        print(f"Size: {size_mb:.2f} MB")
        print(f"Magic bytes (hex): {header[:16].hex()}")
        print(f"First 64 bytes (raw): {header}")
