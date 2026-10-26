import zipfile
import json
import time
import os

t0 = time.time()
with zipfile.ZipFile(r"d:\leads\submissions (1).zip", "r") as zf:
    nl = [n for n in zf.namelist() if not n.startswith('__') and '-submissions-' not in n]
    print(f"Loaded {len(nl):,} filenames in {time.time()-t0:.2f}s")
    
    # fetch first page of 50
    t1 = time.time()
    leads = []
    for fname in nl[:50]:
        with zf.open(fname) as jf:
            d = json.load(jf)
            name = d.get('name')
            phone = d.get('phone')
            leads.append((name, phone))
    print(f"Fetched 50 leads in {time.time()-t1:.3f}s: sample {leads[:2]}")
