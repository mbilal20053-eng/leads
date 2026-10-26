"""
Count rows and check 4 missing conditions in free_company_dataset.csv.zip
"""
import gzip
import time

p = r"d:\leads\free_company_dataset.csv.zip"
print(f"Sampling {p}...")

t0 = time.time()
count = 0
header = None

with gzip.open(p, "rt", encoding="utf-8", errors="ignore") as f:
    header = f.readline().strip().split(",")
    print(f"Header: {header}")
    
    # Read first 100,000 rows to measure speed and inspect values
    sample_rows = []
    for line in f:
        count += 1
        if count <= 5:
            sample_rows.append(line.strip())
        if count >= 100000:
            break

elapsed = time.time() - t0
print(f"Read 100,000 rows in {elapsed:.2f} seconds ({100000/elapsed:,.0f} rows/sec)")
print("\nFirst 5 data rows:")
for sr in sample_rows:
    print(" ", sr[:160])
