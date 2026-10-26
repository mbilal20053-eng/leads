import duckdb

con = duckdb.connect()
f = 'd:/leads/free_company_dataset.csv.zip'
try:
    con.execute(f"SELECT * FROM read_csv('{f}', compression='gzip', all_varchar=true, ignore_errors=true, header=true) LIMIT 5").fetchall()
    print("SUCCESS reading zip with gzip")
except Exception as e:
    print("ERROR reading zip with gzip:", e)
