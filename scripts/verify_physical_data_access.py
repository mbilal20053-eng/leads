import os
import glob
import duckdb
import zipfile

con = duckdb.connect()

print("=" * 80)
print("LIVE PHYSICAL DATA ACCESS & ROW COUNT VERIFICATION")
print("=" * 80)

# 1. Test Key Parquet & CSV files
files_to_test = [
    ('B2B Exec Cleaned Parquet', r'D:\leads\cleaned_export\b2b_executives_final_validated.parquet'),
    ('B2B Raw Consolidated Cleaned', r'D:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet'),
    ('GLEIF Golden Copy Parquet', r'D:\leads\cleaned_export\gleif_goldencopy.parquet'),
    ('SEC Company Facts Parquet', r'D:\leads\cleaned_export\sec_company_facts.parquet'),
    ('CC Web Index Parquet', r'D:\leads\cleaned_export\cc_web_index.parquet'),
    ('Raw Shard free-tier (1).csv', r'D:\leads\free-tier (1).csv'),
    ('Raw Shard free-tier (2).csv', r'D:\leads\free-tier (2).csv'),
    ('Master Locations CSV', r'D:\leads\master-locations.csv'),
    ('Restaurants CSV', r'D:\leads\050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv'),
    ('Realtors CSV', r'D:\leads\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv'),
    ('Open Company Sample CSV', r'D:\leads\open_company_database_sample.csv')
]

for label, p in files_to_test:
    if os.path.exists(p):
        size_mb = os.path.getsize(p) / (1024 * 1024)
        try:
            if p.endswith('.parquet'):
                cnt = con.execute(f"SELECT count(*) FROM '{p}'").fetchone()[0]
                cols = [c[0] for c in con.execute(f"DESCRIBE SELECT * FROM '{p}'").fetchall()[:4]]
                sample = con.execute(f"SELECT * FROM '{p}' LIMIT 1").fetchone()
            else:
                cnt = con.execute(f"SELECT count(*) FROM read_csv_auto('{p}', all_varchar=True)").fetchone()[0]
                cols = [c[0] for c in con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{p}', all_varchar=True)").fetchall()[:4]]
                sample = con.execute(f"SELECT * FROM read_csv_auto('{p}', all_varchar=True) LIMIT 1").fetchone()
            print(f"[ACCESSIBLE] {label}")
            print(f"             Path: {p}")
            print(f"             Size: {size_mb:.2f} MB | Exact Rows: {cnt:,}")
            print(f"             Columns (first 4): {cols}")
            print(f"             Sample data snippet: {str(sample)[:100]}...\n")
        except Exception as e:
            print(f"[ERROR READING] {label} ({p}): {e}\n")
    else:
        print(f"[NOT FOUND ON DISK] {label} ({p})\n")

print("=" * 80)
print("TESTING LARGE ARCHIVE ACCESS (ZIP / GZ)")
print("=" * 80)

# 2. Test large archives
archives_to_test = [
    ('ODO Senzing Zip Archive', r'D:\leads\ODO_SENZING_20260305.zip'),
    ('Free Company Dataset Zip', r'D:\leads\free_company_dataset.csv.zip'),
    ('Data Legion GZ Archive', r'D:\leads\data-legion-company-free-1.5.0_2026-10-15.csv.gz'),
    ('SEC Submissions Zip', r'D:\leads\submissions (1).zip'),
    ('Company Facts Zip', r'D:\leads\companyfacts.zip')
]

for label, p in archives_to_test:
    if os.path.exists(p):
        size_mb = os.path.getsize(p) / (1024 * 1024)
        size_gb = size_mb / 1024
        print(f"[PRESENT ON DISK] {label}")
        print(f"                 Path: {p}")
        print(f"                 File Size: {size_gb:.2f} GB ({size_mb:,.1f} MB)")
        if p.endswith('.zip'):
            try:
                with zipfile.ZipFile(p, 'r') as z:
                    names = z.namelist()[:3]
                    total_files = len(z.namelist())
                    print(f"                 Archive can be opened: YES (contains {total_files} internal files, sample: {names})")
            except Exception as e:
                print(f"                 Zip open test failed: {e}")
        elif p.endswith('.gz'):
            import gzip
            try:
                with gzip.open(p, 'rt', encoding='utf-8', errors='ignore') as gz:
                    header = [gz.readline().strip() for _ in range(2)]
                    print(f"                 GZ stream test: YES (Header: {header[0][:60]}...)")
            except Exception as e:
                print(f"                 GZ open test failed: {e}")
        print()
    else:
        print(f"[NOT FOUND ON DISK] {label} ({p})\n")
