import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")
f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")

# Let's run Query A on b2b_executives_cleaned
q_a = f"""
SELECT 
    count(*) as total_exec_cleaned,
    count(CASE 
        WHEN trim(lower(name)) = trim(lower(contact_name)) 
         AND (phone = '' OR phone IS NULL) 
         AND (email = '' OR email IS NULL) 
         AND (website = '' OR website IS NULL) 
        THEN 1 
    END) as q_a_flagged
FROM read_parquet('{f_exec_clean}')
"""
res_a = con.execute(q_a).fetchone()
print(f"Total exec cleaned: {res_a[0]:,}")
print(f"Flagged by Query A: {res_a[1]:,}")

# Let's inspect the 6,966 records: records where name == contact_name AND phone=='' AND email=='' AND website==''
# BUT they were NOT excluded from raw shards! Meaning they ARE in b2b_raw_shards_consolidated_cleaned.parquet!
q_retained_in_raw = f"""
SELECT 
    count(*)
FROM read_parquet('{f_raw_clean}')
WHERE trim(lower(coalesce("Company Name", ''))) = trim(lower(coalesce("Full name", '')))
  AND trim(coalesce("Company Name", '')) != ''
  AND (trim(coalesce("Phone numbers", "Mobile", '')) = '' OR lower(trim(coalesce("Phone numbers", "Mobile", ''))) IN ('null', 'none', 'nan', 'n/a', '0'))
  AND (trim(coalesce("Emails", '')) = '' OR lower(trim(coalesce("Emails", ''))) IN ('null', 'none', 'nan', 'n/a'))
  AND (trim(coalesce("Company Website", '')) = '' OR lower(trim(coalesce("Company Website", ''))) IN ('null', 'none', 'nan', 'n/a'))
"""
cnt_retained = con.execute(q_retained_in_raw).fetchone()[0]
print(f"Legitimate businesses in raw cleaned where Company Name == Full name (and zero contacts): {cnt_retained:,}")

# Let's sample 10 of these records to see what they look like
q_sample = f"""
SELECT 
    "Full name", "Company Name", "Job title", "Industry", "Location"
FROM read_parquet('{f_raw_clean}')
WHERE trim(lower(coalesce("Company Name", ''))) = trim(lower(coalesce("Full name", '')))
  AND trim(coalesce("Company Name", '')) != ''
  AND (trim(coalesce("Phone numbers", "Mobile", '')) = '' OR lower(trim(coalesce("Phone numbers", "Mobile", ''))) IN ('null', 'none', 'nan', 'n/a', '0'))
  AND (trim(coalesce("Emails", '')) = '' OR lower(trim(coalesce("Emails", ''))) IN ('null', 'none', 'nan', 'n/a'))
  AND (trim(coalesce("Company Website", '')) = '' OR lower(trim(coalesce("Company Website", ''))) IN ('null', 'none', 'nan', 'n/a'))
LIMIT 10
"""
samples = con.execute(q_sample).fetchall()
print("\nSample records where Company Name == Full name:")
for s in samples:
    print(s)
