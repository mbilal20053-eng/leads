import zipfile
import json
import csv
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Sample 5,000 SEC EDGAR files
f_sec = r"d:\leads\submissions (1).zip"
sec_total = 990359
sec_with_phone = 0
sec_with_city = 0
sec_with_state = 0
sec_with_sic = 0
sample_size = 5000

print("Sampling SEC submissions...")
with zipfile.ZipFile(f_sec, 'r') as zf:
    nl = [n for n in zf.namelist() if not n.startswith('__') and '-submissions-' not in n]
    step = len(nl) // sample_size
    sampled = nl[::step][:sample_size]
    for name in sampled:
        with zf.open(name) as f:
            try:
                data = json.load(f)
                phone = data.get('phone')
                if phone and len(str(phone).strip()) > 5:
                    sec_with_phone += 1
                addr = data.get('addresses', {}).get('business', {}) or data.get('addresses', {}).get('mailing', {})
                if addr.get('city'):
                    sec_with_city += 1
                if addr.get('stateOrCountry'):
                    sec_with_state += 1
                if data.get('sic'):
                    sec_with_sic += 1
            except:
                pass

print(f"SEC Submissions ({sec_total:,} total):")
print(f"  Phone coverage: {sec_with_phone / len(sampled) * 100:.1f}% (~{int(sec_total * sec_with_phone / len(sampled)):,} with phone)")
print(f"  City coverage:  {sec_with_city / len(sampled) * 100:.1f}% (~{int(sec_total * sec_with_city / len(sampled)):,} with city)")
print(f"  SIC coverage:   {sec_with_sic / len(sampled) * 100:.1f}% (~{int(sec_total * sec_with_sic / len(sampled)):,} with SIC category)")

# GLEIF: 3,472,837
# GLEIF has official LEI, legal name, city, country, postal code for 100% of entities!
# LEI registration gives official entity status (Active/Inactive), registration authority.
