"""
Comprehensive SQL Verification of the 1,274,221 Discrepancy
"""
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")
f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")
f_excl = r"d:\leads\cleaned_export\exclusion_log_full.parquet".replace("\\", "/")

# Exact breakdown query
q1 = f"""
    SELECT 
        count(*) as total_rows,
        count(CASE WHEN trim(lower(name)) = trim(lower(contact_name)) THEN 1 END) as name_is_contact_name,
        count(CASE WHEN phone = '' OR phone IS NULL THEN 1 END) as missing_phone,
        count(CASE WHEN email = '' OR email IS NULL THEN 1 END) as missing_email,
        count(CASE WHEN website = '' OR website IS NULL THEN 1 END) as missing_website,
        count(CASE 
            WHEN trim(lower(name)) = trim(lower(contact_name)) 
             AND (phone = '' OR phone IS NULL) 
             AND (email = '' OR email IS NULL) 
             AND (website = '' OR website IS NULL) 
            THEN 1 
        END) as person_name_masked_as_business_with_zero_contacts
    FROM read_parquet('{f_exec_clean}')
"""
res = con.execute(q1).fetchone()
print("Executive Cleaned Stats:")
print(f"Total Rows:                             {res[0]:,}")
print(f"Name == Contact Name:                   {res[1]:,}")
print(f"Missing Phone:                          {res[2]:,}")
print(f"Missing Email:                          {res[3]:,}")
print(f"Missing Website:                        {res[4]:,}")
print(f"Person Name As Business & Zero Contacts: {res[5]:,}")
