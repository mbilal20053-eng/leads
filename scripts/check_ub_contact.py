import duckdb

con = duckdb.connect()

res = con.execute("""
    SELECT "Company Name", "Full name", "Job title", "Location", "Emails", "Mobile", "Phone numbers", "Company Website"
    FROM read_csv_auto('d:/leads/free-tier (9).csv', ignore_errors=true)
    WHERE lower(trim("Company Name")) = 'unknown business'
""").fetchall()

print("The 1 exact Unknown Business record:")
for r in res:
    print(r)
