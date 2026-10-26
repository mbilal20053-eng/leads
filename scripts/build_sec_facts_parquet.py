import zipfile
import re
import os
import sys
import time
import pyarrow as pa
import pyarrow.parquet as pq

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

f_facts = r"d:\leads\companyfacts.zip"
out_parquet = r"d:\leads\sec_company_facts.parquet"

print("Starting FAST SEC Company Facts to Parquet conversion...")
t0 = time.time()

schema = pa.schema([
    ('id', pa.string()),
    ('cik', pa.string()),
    ('name', pa.string()),
    ('contact_name', pa.string()),
    ('job_title', pa.string()),
    ('category', pa.string()),
    ('address', pa.string()),
    ('city', pa.string()),
    ('state', pa.string()),
    ('zip', pa.string()),
    ('country', pa.string()),
    ('phone', pa.string()),
    ('website', pa.string()),
    ('email', pa.string()),
    ('socials', pa.string()),
    ('tier', pa.string()),
    ('score', pa.int32()),
    ('opportunity', pa.string()),
    ('pitch', pa.string()),
    ('why', pa.string()),
    ('source_badge', pa.string()),
    ('source_id', pa.string()),
    ('source_color', pa.string()),
])

batch = {k.name: [] for k in schema}

cik_pat = re.compile(r'"cik"\s*:\s*(\d+)')
name_pat = re.compile(r'"entityName"\s*:\s*"([^"]+)"')

with zipfile.ZipFile(f_facts, 'r') as z:
    nl = [n for n in z.namelist() if n.endswith('.json')]
    print(f"Scanning {len(nl):,} files...")
    for name in nl:
        with z.open(name) as jf:
            # Read first 500 bytes only!
            chunk = jf.read(500).decode('utf-8', errors='ignore')
            m_cik = cik_pat.search(chunk)
            m_name = name_pat.search(chunk)
            
            cik = m_cik.group(1) if m_cik else name.replace("CIK", "").replace(".json", "").lstrip("0")
            entity_name = m_name.group(1) if m_name else f"SEC Filer {cik}"
            
            batch['id'].append(f"sec_fact_{cik}")
            batch['cik'].append(str(cik))
            batch['name'].append(entity_name)
            batch['contact_name'].append("Chief Financial Officer / Controller")
            batch['job_title'].append(f"Public Reporting Entity (CIK: {str(cik).zfill(10)})")
            batch['category'].append("Public Corporation / SEC Reporting")
            batch['address'].append("")
            batch['city'].append("")
            batch['state'].append("")
            batch['zip'].append("")
            batch['country'].append("United States")
            batch['phone'].append("")
            batch['website'].append(f"https://www.sec.gov/edgar/browse/?CIK={cik}")
            batch['email'].append("")
            batch['socials'].append(f"CIK: {cik}")
            batch['tier'].append('A')
            batch['score'].append(95)
            batch['opportunity'].append("SEC PUBLIC DISCLOSURE AUDIT")
            batch['pitch'].append(f"Public company {entity_name} (CIK {cik}). Financial reporting automation, ESG disclosure and investor relations portal.")
            batch['why'].append("Verified SEC EDGAR public company with active GAAP XBRL disclosure filings.")
            batch['source_badge'].append("📊 SEC Public Facts")
            batch['source_id'].append("sec_company_facts")
            batch['source_color'].append("#d97706")

tbl = pa.Table.from_pydict(batch, schema=schema)
pq.write_table(tbl, out_parquet, compression='snappy')
print(f"Successfully converted {len(batch['id']):,} SEC public companies to {out_parquet} in {time.time()-t0:.2f}s!")
