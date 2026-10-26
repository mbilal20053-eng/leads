import zipfile
import csv
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

f_gleif = r"d:\leads\20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip"
with zipfile.ZipFile(f_gleif, 'r') as z:
    name = z.namelist()[0]
    print(f"Reading {name}...")
    with z.open(name) as f:
        wrapper = io.TextIOWrapper(f, encoding='utf-8', errors='replace')
        reader = csv.reader(wrapper)
        header = next(reader)
        # Find key column indices
        col_indices = {}
        for target in ["LEI", "Entity.LegalName", "Entity.LegalAddress.City", "Entity.LegalAddress.Country", "Entity.LegalAddress.PostalCode", "Entity.LegalAddress.Region", "Entity.LegalAddress.FirstAddressLine", "Entity.EntityCategory", "Entity.EntityStatus"]:
            if target in header:
                col_indices[target] = header.index(target)
            else:
                # search case insensitive
                for idx, h in enumerate(header):
                    if target.lower() in h.lower():
                        col_indices[target] = idx
                        break
        print("Key column indices:", col_indices)
        
        count = 0
        with_country = 0
        with_city = 0
        with_postal = 0
        countries = {}
        for row in reader:
            count += 1
            if count <= 3:
                extracted = {k: row[v] if v < len(row) else '' for k, v in col_indices.items()}
                print(f"  Row {count}:", extracted)
            if count % 500000 == 0:
                print(f"  Processed {count:,} rows...")
        print(f"TOTAL GLEIF ENTITIES: {count:,}")
