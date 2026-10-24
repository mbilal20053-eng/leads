import csv
import hashlib
import os

fpath = r"d:\leads\free-tier.csv"

seen = set()
total_rows = 0
dup_rows = 0

with open(fpath, 'r', encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        total_rows += 1
        norm_key = "\t".join(col.strip().lower() for col in row).encode('utf-8')
        h = hashlib.blake2b(norm_key, digest_size=16).digest()
        if h in seen:
            dup_rows += 1
        else:
            seen.add(h)

print(f"File: free-tier.csv")
print(f"Total data rows: {total_rows:,}")
print(f"Unique rows: {len(seen):,}")
print(f"Duplicate rows detected: {dup_rows:,}")
