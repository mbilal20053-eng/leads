import duckdb
import glob
import os

con = duckdb.connect()
files = sorted(glob.glob("d:/leads/free-tier (*).csv"))
total = 0
for f in files:
    clean_f = f.replace("\\", "/")
    fname = os.path.basename(f)
    if fname == "free-tier (1).csv":
        continue
    cnt = con.execute(f"SELECT count(*) FROM read_csv_auto('{clean_f}', ignore_errors=true)").fetchone()[0]
    total += cnt
    print(f"{fname:<25}: {cnt:>10,}")

print(f"Total across free-tier (2) to (19): {total:,}")








