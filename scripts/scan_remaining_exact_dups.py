import csv
import hashlib
import os

data_dir = r"d:\leads"

files = [
    "free-tier (1).csv",
    "050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv",
    "166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv",
    "74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv",
    "94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv",
    "b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv",
    "da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv"
]

for fname in files:
    fpath = os.path.join(data_dir, fname)
    if not os.path.exists(fpath):
        continue
    seen = set()
    total = 0
    dups = 0
    with open(fpath, 'r', encoding='utf-8', errors='replace', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            continue
        for row in reader:
            total += 1
            norm_key = "\t".join(col.strip().lower() for col in row).encode('utf-8')
            h = hashlib.blake2b(norm_key, digest_size=16).digest()
            if h in seen:
                dups += 1
            else:
                seen.add(h)
    print(f"{fname:45}: Total={total:,}, Dups={dups:,}, Unique={total - dups:,}")
