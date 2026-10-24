import os
import zipfile
import csv
import gzip
import duckdb
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"

p_zip = os.path.join(data_dir, "master-locations.zip")
if os.path.exists(p_zip):
    print("=== MASTER LOCATIONS ZIP ===")
    with zipfile.ZipFile(p_zip, "r") as zf:
        print("Zip entries:", zf.namelist())
        with zf.open("master-locations.csv") as f:
            import io
            wrapper = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
            r = csv.reader(wrapper)
            header = next(r)
            print("master-locations.csv Header:", header)
            print("Row 1:", next(r))
            print("Row 2:", next(r))

con = duckdb.connect()

p_comp = os.path.join(data_dir, "open_company_database_sample.csv").replace("\\", "/")
if os.path.exists(p_comp):
    c = con.execute(f"SELECT count(*) FROM read_csv_auto('{p_comp}', ignore_errors=true)").fetchone()[0]
    print(f"\nopen_company_database_sample count: {c:,}")

p_apple = os.path.join(data_dir, "apple-locations.csv").replace("\\", "/")
if os.path.exists(p_apple):
    c = con.execute(f"SELECT count(*) FROM read_csv_auto('{p_apple}', ignore_errors=true)").fetchone()[0]
    print(f"\napple-locations count: {c:,}")

p_legion = os.path.join(data_dir, "data-legion-company-free-1.5.0_2026-10-15.csv.gz").replace("\\", "/")
if os.path.exists(p_legion):
    print(f"\nQuerying data-legion-company-free count...")
    c = con.execute(f"SELECT count(*) FROM read_csv_auto('{p_legion}', ignore_errors=true)").fetchone()[0]
    print(f"data-legion total count: {c:,}")
