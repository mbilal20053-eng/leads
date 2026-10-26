"""
Scan newly discovered datasets in C:\\Users\\billu\\Downloads
"""
import os
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()

new_files = [
    r"C:\Users\billu\Downloads\companies_filtered_20261008_120127.csv",
    r"C:\Users\billu\Downloads\fitness_wellness_texas_20261016_123305_crm.csv",
    r"C:\Users\billu\Downloads\salon_leads_filtered.csv",
    r"C:\Users\billu\Downloads\leads - leads (1).csv",
    r"C:\Users\billu\Downloads\leads - leads.csv",
    r"C:\Users\billu\Downloads\leads-export-2026-10-12-899c685d.csv",
    r"C:\Users\billu\Downloads\leads-export-2026-10-12-20c28f9d.csv",
    r"C:\Users\billu\Downloads\leads.csv"
]

print("=" * 110)
print("INSPECTING NEWLY DISCOVERED DATASETS IN DOWNLOADS")
print("=" * 110)

for p in new_files:
    fname = os.path.basename(p)
    clean_p = p.replace("\\", "/")
    if os.path.exists(p):
        try:
            desc = con.execute(f"SELECT * FROM read_csv_auto('{clean_p}', ignore_errors=true) LIMIT 1").description
            cnt = con.execute(f"SELECT count(*) FROM read_csv_auto('{clean_p}', ignore_errors=true)").fetchone()[0]
            cols = [d[0] for d in desc]
            print(f"File: {fname:<45} | Rows: {cnt:>10,} | Cols: {cols[:8]}")
        except Exception as e:
            print(f"File: {fname:<45} | ERROR: {e}")
    else:
        print(f"File: {fname:<45} | NOT FOUND")
