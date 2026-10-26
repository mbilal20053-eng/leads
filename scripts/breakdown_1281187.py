import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")
f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")

# Check exactly how many records in b2b_executives_cleaned have:
# 1) Genuine company name in CSV vs Person name fallback
# We can join b2b_executives_cleaned with b2b_raw_shards_consolidated_cleaned on id
q_breakdown = f"""
SELECT 
    count(*) as total_flagged_1281187,
    count(CASE WHEN r."Company Name" IS NOT NULL AND trim(r."Company Name") != '' THEN 1 END) as legitimate_biz_with_co_name_in_csv,
    count(CASE WHEN r."Company Name" IS NULL THEN 1 END) as ghost_records_missing_from_raw_cleaned
FROM (
    SELECT * FROM read_parquet('{f_exec_clean}')
    WHERE trim(lower(name)) = trim(lower(contact_name))
      AND (phone = '' OR phone IS NULL)
      AND (email = '' OR email IS NULL)
      AND (website = '' OR website IS NULL)
) e
LEFT JOIN read_parquet('{f_raw_clean}') r ON e.id = ('b2b_' || abs(hash(coalesce(r."Company Name", r."Full name", '') || coalesce(r."Job title", '') || coalesce(r."Location", ''))))
"""

res = con.execute(q_breakdown).fetchone()
print(f"Total flagged by Query A:                   {res[0]:,}")
print(f"Legitimate businesses with CSV Company Name: {res[1]:,}")
print(f"Ghost records missing from raw cleaned:     {res[2]:,}")
print(f"Check sum: {res[1] + res[2]:,}")
