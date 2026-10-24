import duckdb
con = duckdb.connect()

print("free-tier (1).csv columns:")
print(con.execute("SELECT * FROM read_csv_auto('d:/leads/free-tier (1).csv') LIMIT 1").fetch_df().columns.tolist())

print("\nfree-tier.csv columns:")
print(con.execute("SELECT * FROM read_csv_auto('d:/leads/free-tier.csv') LIMIT 1").fetch_df().columns.tolist())
