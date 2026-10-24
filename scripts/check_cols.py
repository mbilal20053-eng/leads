import duckdb
import os
import glob

data_dir = r"d:\leads"
con = duckdb.connect()

csvs = glob.glob(os.path.join(data_dir, "*.csv"))
for c in csvs:
    clean_c = c.replace("\\", "/")
    try:
        cols = con.execute(f"SELECT * FROM read_csv_auto('{clean_c}') LIMIT 1").fetch_df().columns.tolist()
        fname = os.path.basename(c)
        print(f"{fname}: {cols[:6]}... (total {len(cols)} cols)")
    except Exception as e:
        print(f"Error reading {c}: {e}")
