"""
Rediscover and catalog all data sources across the entire portfolio (919M+ scope).
STRICT AUDIT ONLY. READ-ONLY.
"""

import os
import sys
import glob
import zipfile
import gzip

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"d:\leads\repo")
from gui import app, lead_db

print("=" * 120)
print("REDISCOVERING ALL DATA SOURCES ACROSS PORTFOLIO (919M+ SCOPE)")
print("=" * 120)

# Check all candidate directories
candidate_dirs = [
    r"d:\leads",
    r"d:\leads\open-company-database",
    r"d:\leads\tech-stack-datasets",
    r"C:\Users\billu\Downloads\leads",
    r"C:\Users\billu\Downloads"
]

print("\n--- 1. PHYSICAL FILES IN D:\\LEADS AND CANDIDATE DIRS ---")
found_files = {}
for cdir in candidate_dirs:
    if os.path.exists(cdir):
        for root, dirs, files in os.walk(cdir):
            # Skip git and hidden
            if ".git" in root or ".gemini" in root:
                continue
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext in [".csv", ".parquet", ".gz", ".zip", ".pbf", ".json", ".jsonl", ".duckdb", ".db"]:
                    full_p = os.path.join(root, fname)
                    sz = os.path.getsize(full_p)
                    found_files[full_p] = {
                        "filename": fname,
                        "path": full_p,
                        "size_bytes": sz,
                        "size_mb": sz / (1024 * 1024),
                        "size_gb": sz / (1024 * 1024 * 1024),
                        "ext": ext
                    }

for p, info in sorted(found_files.items(), key=lambda x: x[1]['size_bytes'], reverse=True):
    print(f"  {info['filename']:<55} | {info['size_mb']:>9.1f} MB ({info['size_gb']:>6.2f} GB) | {p}")

print(f"\nTotal physical candidate data files found: {len(found_files)}")

# Check GLOBAL_SOURCES from app.py
print("\n--- 2. APP.PY / LEAD_DB.PY CONFIGURED GLOBAL SOURCES ---")
for s in app.GLOBAL_SOURCES:
    sid = s.get("id")
    name = s.get("name")
    cnt = s.get("count", 0)
    fpath = s.get("file", "")
    exists = os.path.exists(fpath) if fpath else False
    sz_str = f"{os.path.getsize(fpath)/(1024*1024):.1f} MB" if exists else "NOT FOUND ON DISK"
    print(f"  [{sid:<20}] Configured Count: {cnt:>12,} | File Exists: {str(exists):<5} ({sz_str}) | {name[:60]}")
