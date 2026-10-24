import duckdb
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()
print("=== TOP STORES IN master-locations.csv ===")
try:
    res = con.execute("""
        SELECT store_name, count(*) as cnt 
        FROM read_csv_auto('d:/leads/master-locations.csv') 
        GROUP BY store_name 
        ORDER BY cnt DESC 
        LIMIT 20
    """).fetchall()
    for r in res:
        print(f"  {r[0]:<30}: {r[1]:,}")
except Exception as e:
    print("Error:", e)

print("\n=== OPEN COMPANY DATABASE SAMPLE SECTORS ===")
try:
    res = con.execute("""
        SELECT coalesce(industry, sector, 'Unknown') as ind, count(*) as cnt 
        FROM read_csv_auto('d:/leads/open_company_database_sample.csv', ignore_errors=true) 
        GROUP BY ind 
        ORDER BY cnt DESC 
        LIMIT 15
    """).fetchall()
    for r in res:
        print(f"  {r[0]:<30}: {r[1]:,}")
except Exception as e:
    print("Error:", e)

print("\n=== DATA LEGION INDUSTRIES ===")
try:
    res = con.execute("""
        SELECT coalesce(industry, 'Unknown') as ind, count(*) as cnt 
        FROM read_csv_auto('d:/leads/data-legion-company-free-1.5.0_2026-10-15.csv.gz', ignore_errors=true, sample_size=1000) 
        GROUP BY ind 
        ORDER BY cnt DESC 
        LIMIT 15
    """).fetchall()
    for r in res:
        print(f"  {r[0]:<30}: {r[1]:,}")
except Exception as e:
    print("Error:", e)
