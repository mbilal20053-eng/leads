import zipfile
import csv
import io
import os
import sys
import time
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

f_gleif = r"d:\leads\20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip"
out_parquet = r"d:\leads\gleif_goldencopy.parquet"

print("Starting GLEIF to Parquet conversion...")
t0 = time.time()

schema = pa.schema([
    ('id', pa.string()),
    ('lei', pa.string()),
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

writer = pq.ParquetWriter(out_parquet, schema, compression='snappy')

batch_size = 100000
batch = {k.name: [] for k in schema}

count = 0
with zipfile.ZipFile(f_gleif, 'r') as z:
    name = z.namelist()[0]
    with z.open(name) as f:
        wrapper = io.TextIOWrapper(f, encoding='utf-8', errors='replace')
        reader = csv.reader(wrapper)
        header = next(reader)
        
        # map columns
        lei_idx = header.index("LEI")
        name_idx = header.index("Entity.LegalName")
        city_idx = header.index("Entity.LegalAddress.City")
        country_idx = header.index("Entity.LegalAddress.Country")
        state_idx = header.index("Entity.LegalAddress.Region")
        zip_idx = header.index("Entity.LegalAddress.PostalCode")
        addr_idx = header.index("Entity.LegalAddress.FirstAddressLine")
        cat_idx = header.index("Entity.EntityCategory")
        status_idx = header.index("Entity.EntityStatus")
        
        for row in reader:
            count += 1
            lei = row[lei_idx] if lei_idx < len(row) else ''
            org_name = row[name_idx] if name_idx < len(row) else ''
            city = row[city_idx] if city_idx < len(row) else ''
            country = row[country_idx] if country_idx < len(row) else ''
            state = row[state_idx] if state_idx < len(row) else ''
            zip_code = row[zip_idx] if zip_idx < len(row) else ''
            addr = row[addr_idx] if addr_idx < len(row) else ''
            cat = row[cat_idx] if cat_idx < len(row) else 'Corporate Legal Entity'
            status = row[status_idx] if status_idx < len(row) else 'ACTIVE'
            
            # format values
            batch['id'].append(f"gleif_{lei}")
            batch['lei'].append(lei)
            batch['name'].append(org_name or f"Entity {lei}")
            batch['contact_name'].append("Authorized Legal Representative")
            batch['job_title'].append(f"Registered {cat.title()} ({status.title()})")
            batch['category'].append(cat.replace("_", " ").title() if cat else "Legal Entity")
            batch['address'].append(addr)
            batch['city'].append(city)
            batch['state'].append(state)
            batch['zip'].append(zip_code)
            batch['country'].append(country)
            batch['phone'].append("")
            batch['website'].append(f"https://search.gleif.org/#/record/{lei}")
            batch['email'].append("")
            batch['socials'].append(f"LEI: {lei}")
            batch['tier'].append('A' if status == 'ACTIVE' else 'B')
            batch['score'].append(93 if status == 'ACTIVE' else 75)
            batch['opportunity'].append("GLOBAL LEGAL ENTITY VERIFIED")
            batch['pitch'].append(f"Officially registered legal entity {org_name} (LEI {lei}). Global institutional and corporate compliance audit.")
            batch['why'].append(f"Verified Global Legal Entity Identifier Foundation (GLEIF) Level 1 record. Status: {status}.")
            batch['source_badge'].append("🏛️ GLEIF Legal Registry")
            batch['source_id'].append("gleif_goldencopy")
            batch['source_color'].append("#0284c7")
            
            if count % batch_size == 0:
                tbl = pa.Table.from_pydict(batch, schema=schema)
                writer.write_table(tbl)
                batch = {k.name: [] for k in schema}
                print(f"Written {count:,} records in {time.time()-t0:.1f}s...")

if batch['id']:
    tbl = pa.Table.from_pydict(batch, schema=schema)
    writer.write_table(tbl)

writer.close()
print(f"Successfully converted {count:,} GLEIF records to {out_parquet} ({os.path.getsize(out_parquet):,} bytes) in {time.time()-t0:.1f}s!")
