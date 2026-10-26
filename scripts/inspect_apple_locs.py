import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()
al_path = 'd:/leads/apple-locations.csv'
ml_path = 'd:/leads/master-locations.csv'
res = con.execute(f"SELECT count(*), count(distinct id) FROM read_csv_auto('{al_path}')").fetchall()
print("Apple locations:", res)
overlap = con.execute(f"""
    SELECT count(*) FROM read_csv_auto('{al_path}') a
    JOIN read_csv_auto('{ml_path}') m ON lower(trim(a.id)) = lower(trim(m.id))
""").fetchall()
print("Overlap with master locations:", overlap)
