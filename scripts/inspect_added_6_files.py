import os
import sys
import zipfile
import gzip
import io
import csv
import json
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"

files = [
    "20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip",
    "cc-index.paths.gz",
    "companyfacts (1).zip",
    "companyfacts.zip",
    "submissions (1).zip",
    "submissions.zip"
]

print("=== INSPECTING 6 ADDED FILES ===")

# 1. GLEIF
f_gleif = os.path.join(data_dir, files[0])
print(f"\n1. {files[0]} ({os.path.getsize(f_gleif):,} bytes)")
with zipfile.ZipFile(f_gleif, 'r') as zf:
    nl = zf.namelist()
    print("   Zip entries:", nl)
    first_csv = nl[0]
    with zf.open(first_csv) as f:
        wrapper = io.TextIOWrapper(f, encoding='utf-8', errors='replace')
        reader = csv.reader(wrapper)
        header = next(reader)
        print("   Header columns count:", len(header))
        print("   Sample columns:", header[:25])
        row1 = next(reader)
        print("   Row 1 snippet:", row1[:10])

# 2. CC-INDEX
f_cc = os.path.join(data_dir, files[1])
print(f"\n2. {files[1]} ({os.path.getsize(f_cc):,} bytes)")
with gzip.open(f_cc, 'rt', errors='ignore') as gz:
    cc_lines = [line.strip() for line in gz if line.strip()]
    print(f"   Total paths listed: {len(cc_lines)}")
    print("   Sample paths:", cc_lines[:3])

# 3 & 4. COMPANY FACTS
f_cf = os.path.join(data_dir, files[3])
print(f"\n3. {files[3]} ({os.path.getsize(f_cf):,} bytes)")
with zipfile.ZipFile(f_cf, 'r') as zf:
    nl = zf.namelist()
    print(f"   Total JSON files in zip: {len(nl):,}")
    # Inspect one json
    sample_file = nl[0]
    with zf.open(sample_file) as f:
        data = json.load(f)
        print(f"   Sample JSON ({sample_file}) keys:", list(data.keys()))
        print(f"   Entity name: {data.get('entityName')}, CIK: {data.get('cik')}")

# 5 & 6. SUBMISSIONS
f_sub1 = os.path.join(data_dir, files[4])
print(f"\n4. {files[4]} ({os.path.getsize(f_sub1):,} bytes)")
with zipfile.ZipFile(f_sub1, 'r') as zf:
    nl = zf.namelist()
    print(f"   Total entries in zip: {len(nl):,}")
    cik_files = [n for n in nl if not n.startswith('__') and not '-submissions-' in n]
    sub_chunk_files = [n for n in nl if '-submissions-' in n]
    print(f"   Primary CIK files: {len(cik_files):,}, Sub-filing shards: {len(sub_chunk_files):,}")
    # inspect one CIK JSON
    for test_n in cik_files[:5]:
        with zf.open(test_n) as f:
            try:
                sub_data = json.load(f)
                print(f"   Sample CIK file ({test_n}):")
                print("     Name:", sub_data.get('name'))
                print("     SIC:", sub_data.get('sic'), sub_data.get('sicDescription'))
                print("     Category:", sub_data.get('category'))
                print("     Fiscal Year End:", sub_data.get('fiscalYearEnd'))
                print("     State of Incorp:", sub_data.get('stateOfIncorporation'))
                print("     Phone:", sub_data.get('phone'))
                print("     Addresses:", sub_data.get('addresses'))
                print("     Tickers:", sub_data.get('tickers'))
                print("     Exchanges:", sub_data.get('exchanges'))
                print("     EIN:", sub_data.get('ein'))
                break
            except Exception as e:
                pass
