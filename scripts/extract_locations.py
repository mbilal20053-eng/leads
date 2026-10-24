import zipfile
import os
import duckdb

p_zip = r"d:\leads\master-locations.zip"
dest = r"d:\leads\master-locations.csv"
if os.path.exists(p_zip):
    with zipfile.ZipFile(p_zip, "r") as zf:
        zf.extract("master-locations.csv", r"d:\leads")
    print("Extracted master-locations.csv successfully.")

if os.path.exists(dest):
    con = duckdb.connect()
    cnt = con.execute("SELECT count(*) FROM read_csv_auto('d:/leads/master-locations.csv')").fetchone()[0]
    print(f"master-locations.csv row count: {cnt:,}")
