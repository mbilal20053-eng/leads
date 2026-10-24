import os, sys, glob
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import duckdb

con = duckdb.connect()
files = sorted(glob.glob("d:/leads/*.csv"))

print("=" * 80)
print(f"{'FILE':35} | {'TOTAL':8} | {'PHONE':8} | {'% PHONE':8}")
print("=" * 80)

total_all = 0
phone_all = 0

for f in files:
    clean_f = f.replace("\\", "/")
    fname = os.path.basename(clean_f)
    try:
        desc = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{clean_f}', ignore_errors=true)").fetchall()
        cols = [d[0] for d in desc]
        col_l = {c.lower(): c for c in cols}
        ph_col = col_l.get("phone") or col_l.get("phone_number") or col_l.get("area_code_and_phone") or col_l.get("phone numbers")
        
        if ph_col:
            res = con.execute(f"""
                SELECT 
                    count(*),
                    count(CASE WHEN "{ph_col}" IS NOT NULL AND length(trim(CAST("{ph_col}" AS VARCHAR))) > 6 AND lower(trim(CAST("{ph_col}" AS VARCHAR))) NOT IN ('null', 'none', 'nan', 'n/a', '', '0') THEN 1 END)
                FROM read_csv_auto('{clean_f}', ignore_errors=true)
            """).fetchone()
            tot, ph = res[0], res[1]
            pct = (ph / tot * 100) if tot else 0
            print(f"{fname[:35]:35} | {tot:8,} | {ph:8,} | {pct:7.1f}%")
            total_all += tot
            phone_all += ph
        else:
            tot = con.execute(f"SELECT count(*) FROM read_csv_auto('{clean_f}', ignore_errors=true)").fetchone()[0]
            print(f"{fname[:35]:35} | {tot:8,} | {'NO COL':8} |    0.0%")
            total_all += tot
    except Exception as e:
        print(f"{fname[:35]:35} | ERROR: {e}")

print("=" * 80)
print(f"{'SUM OF ALL 28 CSV FILES':35} | {total_all:8,} | {phone_all:8,} | {phone_all/total_all*100:7.1f}%")
