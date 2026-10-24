import csv
import hashlib
import os

data_dir = r"d:\leads"

b2b_files = [os.path.join(data_dir, f"free-tier ({i}).csv") for i in range(2, 20)]
valid_b2b = [p for p in b2b_files if os.path.exists(p)]

seen = set()
total_b2b_rows = 0
total_b2b_dups = 0

print("Scanning B2B shards for exact duplicate rows (across all 17 columns)...", flush=True)

shard_stats = []

for fpath in valid_b2b:
    fname = os.path.basename(fpath)
    file_rows = 0
    file_dups = 0
    with open(fpath, 'r', encoding='utf-8', errors='replace', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            continue
        for row in reader:
            file_rows += 1
            total_b2b_rows += 1
            norm_key = "\t".join(col.strip().lower() for col in row).encode('utf-8')
            h = hashlib.blake2b(norm_key, digest_size=16).digest()
            if h in seen:
                file_dups += 1
                total_b2b_dups += 1
            else:
                seen.add(h)
    shard_stats.append((fname, file_rows, file_dups, file_rows - file_dups))
    print(f"  {fname:18}: {file_rows:,} rows, {file_dups:,} duplicate rows, {file_rows - file_dups:,} unique remaining (running total unique: {len(seen):,})", flush=True)

print("=" * 70, flush=True)
print(f"Total B2B Rows: {total_b2b_rows:,}", flush=True)
print(f"Total B2B Duplicate Rows Across All 18 Shards: {total_b2b_dups:,}", flush=True)
print(f"Total Unique B2B Rows Remaining: {len(seen):,}", flush=True)
