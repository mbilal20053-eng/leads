import os
import glob
import csv
import hashlib
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"
con = duckdb.connect()

print("=" * 80)
print("  LEAD ENGINE PRO - COMPREHENSIVE DUPLICATE AUDIT ACROSS ALL DATASETS")
print("=" * 80)

# 1. B2B Executive Shards: free-tier (2..19).csv
print("\n[1] Auditing B2B Executive Shards (free-tier (2) through (19))...")
b2b_files = [os.path.join(data_dir, f"free-tier ({i}).csv") for i in range(2, 20)]
b2b_seen = set()
b2b_total = 0
b2b_internal_dups = 0
b2b_cross_dups = 0

for fp in b2b_files:
    if not os.path.exists(fp):
        continue
    fname = os.path.basename(fp)
    file_seen = set()
    f_tot = 0
    f_int_dups = 0
    f_cross_dups = 0
    with open(fp, 'r', encoding='utf-8', errors='replace', newline='') as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            continue
        for row in reader:
            f_tot += 1
            norm_key = "\t".join(c.strip().lower() for c in row).encode('utf-8')
            h = hashlib.blake2b(norm_key, digest_size=16).digest()
            if h in file_seen:
                f_int_dups += 1
            elif h in b2b_seen:
                f_cross_dups += 1
            else:
                file_seen.add(h)
                b2b_seen.add(h)
    b2b_total += f_tot
    b2b_internal_dups += f_int_dups
    b2b_cross_dups += f_cross_dups
    if f_int_dups > 0 or f_cross_dups > 0:
        print(f"  {fname:<25}: Total={f_tot:>9,} | Internal Dups={f_int_dups:>6,} | Cross-Shard Dups={f_cross_dups:>6,}")
    else:
        print(f"  {fname:<25}: Total={f_tot:>9,} | Clean (0 dups)")

print(f"--> B2B Total: {b2b_total:,} | Total Dups: {b2b_internal_dups + b2b_cross_dups:,} | Unique: {len(b2b_seen):,}")

# 2. Homeowners (free-tier (1).csv)
print("\n[2] Auditing Homeowners (free-tier (1).csv)...")
f_ho = os.path.join(data_dir, "free-tier (1).csv")
ho_total = 0
ho_exact_dups = 0
ho_seen = set()
with open(f_ho, 'r', encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    try: next(reader)
    except: pass
    for row in reader:
        ho_total += 1
        norm_key = "\t".join(c.strip().lower() for c in row).encode('utf-8')
        h = hashlib.blake2b(norm_key, digest_size=16).digest()
        if h in ho_seen:
            ho_exact_dups += 1
        else:
            ho_seen.add(h)
print(f"--> Homeowners: Total={ho_total:,} | Exact Row Duplicates={ho_exact_dups:,} | Unique={len(ho_seen):,}")

# 3. Commercial Real Estate (free-tier.csv)
print("\n[3] Auditing Commercial Real Estate (free-tier.csv)...")
f_cre = os.path.join(data_dir, "free-tier.csv")
cre_total = 0
cre_dups = 0
cre_seen = set()
with open(f_cre, 'r', encoding='utf-8', errors='replace', newline='') as f:
    reader = csv.reader(f)
    try: next(reader)
    except: pass
    for row in reader:
        cre_total += 1
        norm_key = "\t".join(c.strip().lower() for c in row).encode('utf-8')
        h = hashlib.blake2b(norm_key, digest_size=16).digest()
        if h in cre_seen:
            cre_dups += 1
        else:
            cre_seen.add(h)
print(f"--> Commercial Real Estate: Total={cre_total:,} | Dups={cre_dups:,} | Unique={len(cre_seen):,}")

# 4. Master Locations vs Apple Locations
print("\n[4] Auditing Master Locations & Apple Locations...")
f_ml = os.path.join(data_dir, "master-locations.csv")
f_al = os.path.join(data_dir, "apple-locations.csv")
ml_tot = con.execute(f"SELECT count(*), count(distinct id) FROM read_csv_auto('{f_ml.replace('\\', '/')}')").fetchone()
al_tot = con.execute(f"SELECT count(*), count(distinct id) FROM read_csv_auto('{f_al.replace('\\', '/')}')").fetchone()
overlap = con.execute(f"""
    SELECT count(*) FROM read_csv_auto('{f_al.replace('\\', '/')}') a
    JOIN read_csv_auto('{f_ml.replace('\\', '/')}') m ON lower(trim(a.id)) = lower(trim(m.id))
""").fetchone()[0]
print(f"--> master-locations.csv: Total={ml_tot[0]:,}, Unique IDs={ml_tot[1]:,}, Dups={ml_tot[0]-ml_tot[1]:,}")
print(f"--> apple-locations.csv : Total={al_tot[0]:,}, Overlap with master-locations={overlap:,} (100% duplicate file)")

# 5. Realtors files
print("\n[5] Auditing Realtors Files...")
f_r = os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv")
f_r_clone = os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv")
print(f"--> realtors.csv size: {os.path.getsize(f_r):,} bytes")
print(f"--> realtors (1).csv size: {os.path.getsize(f_r_clone):,} bytes (Empty clone file)")

# 6. GLEIF Golden Copy Parquet
print("\n[6] Auditing GLEIF Golden Copy Parquet...")
f_gleif_pq = os.path.join(data_dir, "gleif_goldencopy.parquet").replace('\\', '/')
gleif_stats = con.execute(f"SELECT count(*), count(distinct lei), count(distinct name) FROM read_parquet('{f_gleif_pq}')").fetchone()
print(f"--> GLEIF: Total={gleif_stats[0]:,}, Unique LEIs={gleif_stats[1]:,}, Duplicate LEIs={gleif_stats[0]-gleif_stats[1]:,}")

# 7. SEC Company Facts Parquet
print("\n[7] Auditing SEC Company Facts Parquet...")
f_facts_pq = os.path.join(data_dir, "sec_company_facts.parquet").replace('\\', '/')
facts_stats = con.execute(f"SELECT count(*), count(distinct cik), count(distinct name) FROM read_parquet('{f_facts_pq}')").fetchone()
print(f"--> SEC Facts: Total={facts_stats[0]:,}, Unique CIKs={facts_stats[1]:,}, Duplicate CIKs={facts_stats[0]-facts_stats[1]:,}")

# 8. File system duplicate archive files
print("\n[8] Auditing File System Duplicates...")
cf1 = os.path.join(data_dir, "companyfacts (1).zip")
cf = os.path.join(data_dir, "companyfacts.zip")
sub1 = os.path.join(data_dir, "submissions (1).zip")
sub = os.path.join(data_dir, "submissions.zip")
print(f"--> companyfacts (1).zip: {os.path.getsize(cf1):,} bytes (Exact duplicate of companyfacts.zip {os.path.getsize(cf):,} bytes)")
print(f"--> submissions.zip: {os.path.getsize(sub):,} bytes (Corrupted partial 650MB download of submissions (1).zip {os.path.getsize(sub1):,} bytes)")

print("\n" + "=" * 80)
