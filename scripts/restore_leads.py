import zipfile
import os
import sys

backup_zip = r"C:\Users\billu\leads_original_backup_20261024.zip"
target_dir = r"d:\leads"

print(f"Restoring all 28 CSV files from {backup_zip} into {target_dir}...", flush=True)

with zipfile.ZipFile(backup_zip, 'r') as zf:
    namelist = zf.namelist()
    for i, name in enumerate(namelist, 1):
        print(f"[{i}/{len(namelist)}] Restoring {name}...", flush=True)
        zf.extract(name, target_dir)

print("\nRestore completed successfully! Verifying files on disk...", flush=True)
files_on_disk = [f for f in os.listdir(target_dir) if f.endswith('.csv')]
print(f"Total CSV files restored in {target_dir}: {len(files_on_disk)}", flush=True)
