import os
import glob
import duckdb

data_dir = r"d:\leads"
con = duckdb.connect()

print("=" * 80)
print("AUDITING EXACT ROW DUPLICATES (100% of all columns matching exactly)")
print("=" * 80)

# Check within each individual file
csv_files = sorted(glob.glob(os.path.join(data_dir, "*.csv")))

within_dups = {}
for f in csv_files:
    fname = os.path.basename(f)
    clean_f = f.replace("\\", "/")
    try:
        tot = con.execute(f"SELECT count(1) FROM read_csv_auto('{clean_f}', ignore_errors=true)").fetchone()[0]
        dist = con.execute(f"SELECT count(1) FROM (SELECT DISTINCT * FROM read_csv_auto('{clean_f}', ignore_errors=true))").fetchone()[0]
        diff = tot - dist
        if diff > 0:
            within_dups[fname] = (tot, dist, diff)
            print(f"[WITHIN-FILE DUP] {fname}: Total={tot:,}, Unique={dist:,}, Duplicate Rows={diff:,}")
    except Exception as e:
        print(f"Error checking {fname}: {e}")

if not within_dups:
    print("No within-file exact duplicate rows found (except free-tier.csv).")

# Check across B2B shards
b2b_files = [os.path.join(data_dir, f"free-tier ({i}).csv").replace("\\", "/") for i in range(2, 20)]
valid_b2b = [p for p in b2b_files if os.path.exists(p)]

print("\nChecking across all 18 B2B shards combined...")
tot_b2b = con.execute(f"SELECT count(1) FROM read_csv_auto({valid_b2b}, ignore_errors=true)").fetchone()[0]
dist_b2b = con.execute(f"SELECT count(1) FROM (SELECT DISTINCT * FROM read_csv_auto({valid_b2b}, ignore_errors=true))").fetchone()[0]
print(f"B2B Shards Total rows: {tot_b2b:,}")
print(f"B2B Shards Distinct rows (all 17 columns identical): {dist_b2b:,}")
print(f"B2B Shards Exact Duplicate rows across shards: {tot_b2b - dist_b2b:,}")

# Check realtors vs realtors (1)
r1 = os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv").replace("\\", "/")
r2 = os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv").replace("\\", "/")
tot_r = con.execute(f"SELECT count(1) FROM read_csv_auto(['{r1}', '{r2}'], ignore_errors=true)").fetchone()[0]
dist_r = con.execute(f"SELECT count(1) FROM (SELECT DISTINCT * FROM read_csv_auto(['{r1}', '{r2}'], ignore_errors=true))").fetchone()[0]
print(f"\nRealtors combined: Total={tot_r:,}, Distinct={dist_r:,}, Duplicate={tot_r - dist_r:,}")
