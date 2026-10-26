import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()
ml_path = 'd:/leads/master-locations.csv'
res = con.execute(f"""
    SELECT 
        count(*) as total_rows, 
        count(distinct id) as unique_ids,
        count(distinct (store_name || '_' || coalesce(city, '') || '_' || coalesce(coordinates, ''))) as unique_locs
    FROM read_csv_auto('{ml_path}')
""").fetchall()

print("Master locations stats:", res)
sample = con.execute(f"SELECT * FROM read_csv_auto('{ml_path}') LIMIT 2").fetchall()
cols = [c[0] for c in con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{ml_path}')").fetchall()]
print("Columns:", cols)
