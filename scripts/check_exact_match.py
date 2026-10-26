import duckdb

con = duckdb.connect()
res = con.execute("""
    SELECT "Company Name", "Full name", "Job title", "Location", "Emails"
    FROM read_csv_auto('d:/leads/free-tier (9).csv', ignore_errors=true)
    WHERE lower(trim("Company Name")) = 'unknown business'
""").fetchall()

print("Exact match record in free-tier (9).csv:", res)
