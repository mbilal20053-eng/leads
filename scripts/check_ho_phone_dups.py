import csv
import hashlib

fpath = r"d:\leads\free-tier (1).csv"

seen_with_phone = set()
dups_with_phone = 0
total_with_phone = 0

seen_no_phone = set()
dups_no_phone = 0
total_no_phone = 0

with open(fpath, 'r', encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        phone = row[4].strip()
        norm_key = "\t".join(col.strip().lower() for col in row).encode('utf-8')
        h = hashlib.blake2b(norm_key, digest_size=16).digest()
        if phone:
            total_with_phone += 1
            if h in seen_with_phone:
                dups_with_phone += 1
            else:
                seen_with_phone.add(h)
        else:
            total_no_phone += 1
            if h in seen_no_phone:
                dups_no_phone += 1
            else:
                seen_no_phone.add(h)

print(f"Rows with phone: {total_with_phone:,}, Duplicates with phone: {dups_with_phone:,}")
print(f"Rows without phone: {total_no_phone:,}, Duplicates without phone: {dups_no_phone:,}")
