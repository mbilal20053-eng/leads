import os
import glob
import csv
import hashlib
import shutil
import zipfile
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"
backup_zip = r"C:\Users\billu\leads_original_backup_20261024.zip"
staging_dir = r"C:\Users\billu\cleaned_leads_staging"

print("=" * 80, flush=True)
print("  LEAD ENGINE PRO - VERIFIED EXACT DEDUPLICATION PIPELINE", flush=True)
print("=" * 80, flush=True)

# 1. Verify Backup Integrity
print("\n[STEP 1] Verifying Original Backup Archive...", flush=True)
if not os.path.exists(backup_zip):
    raise RuntimeError(f"FATAL: Backup file does not exist at {backup_zip}! Aborting.")

with zipfile.ZipFile(backup_zip, 'r') as zf:
    bad_file = zf.testzip()
    if bad_file:
        raise RuntimeError(f"FATAL: Backup zip corrupted on {bad_file}! Aborting.")
    namelist = zf.namelist()
    print(f"  Backup Verified OK: {len(namelist)} original files safely secured ({os.path.getsize(backup_zip)/(1024*1024):.1f} MB).", flush=True)

if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)
os.makedirs(staging_dir, exist_ok=True)

dedup_results = []
total_original_all = 0
total_removed_all = 0
total_remaining_all = 0

# ---------------------------------------------------------------------------
# Helper function to deduplicate a file with a given seen_set
# ---------------------------------------------------------------------------
def process_file(fpath, seen_set, description=""):
    global total_original_all, total_removed_all, total_remaining_all
    fname = os.path.basename(fpath)
    staged_path = os.path.join(staging_dir, fname)
    
    orig_rows = 0
    dups_removed = 0
    kept_rows = 0
    
    with open(fpath, 'r', encoding='utf-8', errors='replace', newline='') as infile, \
         open(staged_path, 'w', encoding='utf-8', errors='replace', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        try:
            header = next(reader)
            writer.writerow(header)
        except StopIteration:
            header = []
            
        for row in reader:
            orig_rows += 1
            norm_key = "\t".join(c.strip().lower() for c in row).encode('utf-8')
            h = hashlib.blake2b(norm_key, digest_size=16).digest()
            if h in seen_set:
                dups_removed += 1
            else:
                seen_set.add(h)
                writer.writerow(row)
                kept_rows += 1
                
    # Verify staged file
    with open(staged_path, 'r', encoding='utf-8', errors='replace', newline='') as fcheck:
        rcheck = csv.reader(fcheck)
        header_check = next(rcheck)
        actual_staged_rows = sum(1 for _ in rcheck)
        
    if actual_staged_rows != kept_rows:
        raise RuntimeError(f"Verification mismatch on {fname}: expected {kept_rows}, got {actual_staged_rows}!")
    if header_check != header:
        raise RuntimeError(f"Header mismatch on {fname}!")
        
    # Replace original file with verified staged file
    shutil.move(staged_path, fpath)
    
    total_original_all += orig_rows
    total_removed_all += dups_removed
    total_remaining_all += kept_rows
    
    dedup_results.append({
        "file": fname,
        "type": description,
        "original": orig_rows,
        "removed": dups_removed,
        "remaining": kept_rows
    })
    
    status_str = f"Removed {dups_removed:,} dups" if dups_removed > 0 else "0 dups (clean)"
    print(f"  [PROCESSED] {fname:<45}: Orig={orig_rows:<10,} {status_str:<22} Remaining={kept_rows:<10,}", flush=True)

# ---------------------------------------------------------------------------
# [STEP 2] Process B2B Shards (18 files with cross-shard deduplication)
# ---------------------------------------------------------------------------
print("\n[STEP 2] Deduplicating 18 B2B Executive Shards (Within-File + Cross-Shard)...", flush=True)
b2b_seen = set()
for i in range(2, 20):
    fpath = os.path.join(data_dir, f"free-tier ({i}).csv")
    if os.path.exists(fpath):
        process_file(fpath, b2b_seen, description="B2B Executive Shard")

# ---------------------------------------------------------------------------
# [STEP 3] Process Commercial Real Estate (free-tier.csv)
# ---------------------------------------------------------------------------
print("\n[STEP 3] Deduplicating Commercial Real Estate (free-tier.csv)...", flush=True)
cre_seen = set()
f_cre = os.path.join(data_dir, "free-tier.csv")
if os.path.exists(f_cre):
    process_file(f_cre, cre_seen, description="Commercial Real Estate")

# ---------------------------------------------------------------------------
# [STEP 4] Process Realtors (realtors.csv and clone realtors (1).csv)
# ---------------------------------------------------------------------------
print("\n[STEP 4] Deduplicating Realtors Directories...", flush=True)
realtor_seen = set()
f_r1 = os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv")
f_r2 = os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv")
if os.path.exists(f_r1):
    process_file(f_r1, realtor_seen, description="Realtors Primary")
if os.path.exists(f_r2):
    process_file(f_r2, realtor_seen, description="Realtors Duplicate Clone")

# ---------------------------------------------------------------------------
# [STEP 5] Process Residential Homeowners (free-tier (1).csv)
# ---------------------------------------------------------------------------
print("\n[STEP 5] Deduplicating Residential Homeowners (free-tier (1).csv)...", flush=True)
# For homeowners, rows with a phone number that have all 10 columns matching identically
# are true duplicate households. Demographic rows without a phone represent distinct homes in that zip.
def process_homeowners(fpath):
    global total_original_all, total_removed_all, total_remaining_all
    fname = os.path.basename(fpath)
    staged_path = os.path.join(staging_dir, fname)
    
    seen_phones = set()
    orig_rows = 0
    dups_removed = 0
    kept_rows = 0
    
    with open(fpath, 'r', encoding='utf-8', errors='replace', newline='') as infile, \
         open(staged_path, 'w', encoding='utf-8', errors='replace', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            orig_rows += 1
            phone = row[4].strip() if len(row) > 4 else ""
            if phone:
                norm_key = "\t".join(c.strip().lower() for c in row).encode('utf-8')
                h = hashlib.blake2b(norm_key, digest_size=16).digest()
                if h in seen_phones:
                    dups_removed += 1
                    continue
                seen_phones.add(h)
            
            writer.writerow(row)
            kept_rows += 1
            
    # Verify staged file
    with open(staged_path, 'r', encoding='utf-8', errors='replace', newline='') as fcheck:
        rcheck = csv.reader(fcheck)
        header_check = next(rcheck)
        actual_staged_rows = sum(1 for _ in rcheck)
        
    if actual_staged_rows != kept_rows:
        raise RuntimeError(f"Verification mismatch on {fname}: expected {kept_rows}, got {actual_staged_rows}!")
        
    shutil.move(staged_path, fpath)
    
    total_original_all += orig_rows
    total_removed_all += dups_removed
    total_remaining_all += kept_rows
    
    dedup_results.append({
        "file": fname,
        "type": "Homeowners & Residential",
        "original": orig_rows,
        "removed": dups_removed,
        "remaining": kept_rows
    })
    print(f"  [PROCESSED] {fname:<45}: Orig={orig_rows:<10,} Removed {dups_removed:<6,} dups Remaining={kept_rows:<10,}", flush=True)

f_ho = os.path.join(data_dir, "free-tier (1).csv")
if os.path.exists(f_ho):
    process_homeowners(f_ho)

# ---------------------------------------------------------------------------
# [STEP 6] Process Other Specialty Professional Directories
# ---------------------------------------------------------------------------
print("\n[STEP 6] Deduplicating Specialty Professional Directories...", flush=True)
spec_files = [
    "050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv",
    "166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv",
    "74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv",
    "94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv",
    "b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv",
    "da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv"
]
for fname in spec_files:
    fpath = os.path.join(data_dir, fname)
    if os.path.exists(fpath):
        s_seen = set()
        process_file(fpath, s_seen, description="Specialty Directory")

# Clean up staging dir
if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)

print("\n" + "=" * 80, flush=True)
print("  DEDUPLICATION COMPLETED SUCCESSFULLY", flush=True)
print("=" * 80, flush=True)
print(f"  TOTAL ORIGINAL ROWS ANALYZED: {total_original_all:,}", flush=True)
print(f"  TOTAL EXACT DUPLICATE ROWS REMOVED: {total_removed_all:,}", flush=True)
print(f"  TOTAL UNIQUE ROWS REMAINING: {total_remaining_all:,}", flush=True)
print("=" * 80, flush=True)

import json
report_path = os.path.join(data_dir, "repo", "deduplication_audit_report.json")
with open(report_path, "w", encoding="utf-8") as rf:
    json.dump({
        "backup_archive": backup_zip,
        "total_original": total_original_all,
        "total_removed": total_removed_all,
        "total_remaining": total_remaining_all,
        "files": dedup_results
    }, rf, indent=2)
print(f"Detailed audit report saved to {report_path}", flush=True)

