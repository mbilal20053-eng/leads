import duckdb

con = duckdb.connect()
f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")

# In b2b_executives_cleaned.parquet:
# Check contact channels
q = f"""
    SELECT 
        count(*) as total,
        count(CASE WHEN (phone IS NULL OR trim(phone) = '') AND (email IS NULL OR trim(email) = '') AND (website IS NULL OR trim(website) = '') THEN 1 END) as no_contact_channels,
        count(CASE WHEN trim(lower(name)) = trim(lower(contact_name)) AND (phone IS NULL OR trim(phone) = '') AND (email IS NULL OR trim(email) = '') AND (website IS NULL OR trim(website) = '') THEN 1 END) as person_name_only_no_contacts
    FROM read_parquet('{f_exec_clean}')
"""
res = con.execute(q).fetchone()
print(f"Total rows in b2b_executives_cleaned.parquet: {res[0]:,}")
print(f"Rows with NO phone, NO email, NO website:      {res[1]:,}")
print(f"Rows where Name==Contact & NO contacts:         {res[2]:,}")
