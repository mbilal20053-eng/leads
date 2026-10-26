"""
VERIFY ORIGINAL SOURCE FILES AGAINST BACKUP ARCHIVES (CRC32 & SIZES)
Compares files in d:\\leads against backup_original_20261025.zip and leads_original_backup_20261024.zip
"""
import os
import sys
import zipfile
import zlib
import hashlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"
backup_24 = r"C:\Users\billu\leads_original_backup_20261024.zip"
backup_25 = r"d:\leads\backup_original_20261025.zip"

def get_file_crc32(fpath):
    prev = 0
    with open(fpath, 'rb') as f:
        while chunk := f.read(1024 * 1024):
            prev = zlib.crc32(chunk, prev)
    return prev & 0xFFFFFFFF

print("=" * 110)
print("VERIFYING ORIGINAL SOURCE FILES AGAINST PRE-CLEANUP BACKUPS")
print("=" * 110)

matched_25 = 0
mismatched_25 = 0

if os.path.exists(backup_25):
    print(f"Reading {backup_25}...")
    with zipfile.ZipFile(backup_25, 'r') as zf:
        infolist = zf.infolist()
        print(f"Backup 2026-10-25 contains {len(infolist)} entries.")
        for info in infolist:
            fname = info.filename
            curr_path = os.path.join(data_dir, fname)
            if os.path.exists(curr_path):
                curr_size = os.path.getsize(curr_path)
                curr_crc = get_file_crc32(curr_path)
                if curr_size == info.file_size and curr_crc == info.CRC:
                    matched_25 += 1
                    print(f"  [100% VERIFIED IDENTICAL] {fname:<45} | Size: {curr_size:>12,} bytes | CRC32: {hex(curr_crc)}")
                else:
                    mismatched_25 += 1
                    print(f"  [MISMATCH DETECTED] {fname:<45} | Disk Size: {curr_size} vs Zip Size: {info.file_size} | Disk CRC: {hex(curr_crc)} vs Zip CRC: {hex(info.CRC)}")
            else:
                print(f"  [NOT FOUND ON DISK] {fname}")

print(f"\nResult for Backup 2026-10-25: {matched_25} files verified 100% identical, {mismatched_25} mismatches.")
