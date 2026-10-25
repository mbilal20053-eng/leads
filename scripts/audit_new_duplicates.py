import os
import csv
import gzip
import hashlib
import duckdb
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"

print("=" * 80)
print("  LEAD ENGINE PRO - COMPREHENSIVE DUPLICATE AUDIT REPORT")
print("=" * 80)

# 1. Check exact duplicates within master-locations.csv and apple-locations.csv
f_master_loc = os.path.join(data_dir, "master-locations.csv")
f_apple_loc = os.path.join(data_dir, "apple-locations.csv")
f_open_comp = os.path.join(data_dir, "open_company_database_sample.csv")
f_legion = os.path.join(data_dir, "data-legion-company-free-1.5.0_2026-10-15.csv.gz")

con = duckdb.connect()

def audit_file_exact_dups(fpath, is_gz=False):
    fname = os.path.basename(fpath)
    total_rows = 0
    seen_hashes = set()
    dup_count = 0
    
    open_fn = gzip.open(fpath, 'rt', encoding='utf-8', errors='replace') if is_gz else open(fpath, 'r', encoding='utf-8', errors='replace')
    with open_fn as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return 0, 0, 0
        for row in reader:
            total_rows += 1
            norm_key = "\t".join(c.strip().lower() for c in row).encode('utf-8')
            h = hashlib.blake2b(norm_key, digest_size=16).digest()
            if h in seen_hashes:
                dup_count += 1
            else:
                seen_hashes.add(h)
                
    unique_rows = len(seen_hashes)
    return total_rows, dup_count, unique_rows

# Check newly added files
print("\n[PHASE 1] Auditing Newly Added Files for Exact Duplicate Rows...")

# Master locations
if os.path.exists(f_master_loc):
    tot, dups, uniq = audit_file_exact_dups(f_master_loc)
    print(f"  master-locations.csv             : Total={tot:,} | Exact Dups={dups:,} | Unique={uniq:,}")

# Apple locations
if os.path.exists(f_apple_loc):
    tot, dups, uniq = audit_file_exact_dups(f_apple_loc)
    print(f"  apple-locations.csv              : Total={tot:,} | Exact Dups={dups:,} | Unique={uniq:,}")

# Overlap between master-locations.csv and apple-locations.csv
if os.path.exists(f_master_loc) and os.path.exists(f_apple_loc):
    q = f"""
    SELECT count(*) 
    FROM read_csv_auto('{f_apple_loc.replace("\\", "/")}') a
    JOIN read_csv_auto('{f_master_loc.replace("\\", "/")}') m
      ON lower(trim(a.id)) = lower(trim(m.id))
    """
    overlap = con.execute(q).fetchone()[0]
    print(f"  -> Overlap between apple-locations.csv & master-locations.csv: {overlap:,} identical store records")

# Open Company Database
if os.path.exists(f_open_comp):
    tot, dups, uniq = audit_file_exact_dups(f_open_comp)
    print(f"  open_company_database_sample.csv : Total={tot:,} | Exact Dups={dups:,} | Unique={uniq:,}")

# Data Legion GZ (28M rows)
if os.path.exists(f_legion):
    print("  Auditing data-legion-company-free (28.1M rows, streaming hash)...")
    # Quick exact duplicate check via DuckDB count vs count(DISTINCT)
    q = f"""
    SELECT count(*), count(DISTINCT legion_id), count(DISTINCT lower(trim(name)) || '|' || coalesce(lower(trim(domain)), ''))
    FROM read_csv_auto('{f_legion.replace("\\", "/")}', ignore_errors=true, sample_size=1000)
    """
    row = con.execute(q).fetchone()
    tot_legion = row[0]
    uniq_ids = row[1]
    uniq_names_domains = row[2]
    dup_legion_ids = tot_legion - uniq_ids
    print(f"  data-legion.csv.gz (by ID)       : Total={tot_legion:,} | Duplicate IDs={dup_legion_ids:,} | Unique IDs={uniq_ids:,}")
    print(f"  data-legion.csv.gz (Name+Domain) : Unique={uniq_names_domains:,} | Repeated Name+Domain={tot_legion - uniq_names_domains:,}")

# Check existing 28 files status
print("\n[PHASE 2] Existing 28 Lead Databases Status (Previously Deduplicated)...")
import json
report_path = os.path.join(data_dir, "repo", "deduplication_audit_report.json")
if os.path.exists(report_path):
    with open(report_path, "r", encoding="utf-8") as rf:
        rep = json.load(rf)
    print(f"  Original Files Analyzed : {rep.get('total_original', 0):,}")
    print(f"  Exact Duplicates Removed: {rep.get('total_removed', 0):,}")
    print(f"  Unique Clean Records    : {rep.get('total_remaining', 0):,}")

print("\n" + "=" * 80)
print("  AUDIT COMPLETED (NO DATA MODIFIED)")
print("=" * 80)
