"""
DEEP INVESTIGATION: LINEAGE DISCREPANCY OF 1,274,221 ROWS BETWEEN
1. b2b_raw_shards_consolidated_cleaned.parquet (10,268,615 rows)
2. b2b_executives_cleaned.parquet (11,542,836 rows)

Strictly Read-Only. No modifications to any data.
"""
import os
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")
f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")
f_exec_orig = r"d:\leads\b2b_executives.parquet".replace("\\", "/")
f_excl_log = r"d:\leads\cleaned_export\exclusion_log_full.parquet".replace("\\", "/")

print("=" * 120)
print("LINEAGE & SCHEMA INVESTIGATION: 1,274,221 ROW DISCREPANCY")
print("=" * 120)

cnt_raw_clean = con.execute(f"SELECT count(*) FROM read_parquet('{f_raw_clean}')").fetchone()[0]
cnt_exec_clean = con.execute(f"SELECT count(*) FROM read_parquet('{f_exec_clean}')").fetchone()[0]
cnt_exec_orig = con.execute(f"SELECT count(*) FROM read_parquet('{f_exec_orig}')").fetchone()[0]
cnt_excl_log = con.execute(f"SELECT count(*) FROM read_parquet('{f_excl_log}')").fetchone()[0]

diff = cnt_exec_clean - cnt_raw_clean
print(f"b2b_raw_shards_consolidated_cleaned.parquet: {cnt_raw_clean:>12,}")
print(f"b2b_executives_cleaned.parquet:              {cnt_exec_clean:>12,}")
print(f"Difference:                                  {diff:>12,}")
print(f"Original b2b_executives.parquet:             {cnt_exec_orig:>12,}")
print(f"Exclusions in exclusion_log_full.parquet:    {cnt_excl_log:>12,}")
print(f"b2b_executives exclusions:                   {cnt_exec_orig - cnt_exec_clean:>12,}")

# Check 1: What are the columns in both files?
print("\n--- SCHEMA OF b2b_raw_shards_consolidated_cleaned.parquet ---")
desc_raw = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{f_raw_clean}')").fetchall()
for d in desc_raw:
    print(f"  {d[0]:<25}: {d[1]}")

print("\n--- SCHEMA OF b2b_executives_cleaned.parquet ---")
desc_exec = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{f_exec_clean}')").fetchall()
for d in desc_exec:
    print(f"  {d[0]:<25}: {d[1]}")

# Check 2: Check the mapping in b2b_executives.parquet
# How many rows in b2b_executives.parquet have name == contact_name?
name_eq_contact = con.execute(f"""
    SELECT count(*) 
    FROM read_parquet('{f_exec_clean}')
    WHERE trim(lower(name)) = trim(lower(contact_name)) AND length(contact_name) > 1
""").fetchone()[0]
print(f"\nRows in b2b_executives_cleaned where name == contact_name (Company Name was missing, so Full Name was used): {name_eq_contact:,}")

# Check 3: How many of the 1,275,044 excluded records are in b2b_executives_cleaned?
# Match exclusion_log_full by contact_name + location or ID
match_excl_in_exec = con.execute(f"""
    WITH excl AS (
        SELECT record_fingerprint
        FROM read_parquet('{f_excl_log}')
    ),
    exec AS (
        SELECT abs(hash(coalesce(contact_name, '') || coalesce(job_title, '') || coalesce(address, ''))) as fp
        FROM read_parquet('{f_exec_clean}')
    )
    SELECT count(*)
    FROM exec e
    JOIN excl x ON e.fp = x.record_fingerprint
""").fetchone()[0]
print(f"Excluded raw records present in b2b_executives_cleaned: {match_excl_in_exec:,}")

# Check 4: For the records in b2b_executives_cleaned that were excluded from raw shards:
# What do their phone, email, and website columns contain?
q_check_contacts = f"""
    WITH excl AS (
        SELECT record_fingerprint
        FROM read_parquet('{f_excl_log}')
    ),
    exec_with_fp AS (
        SELECT 
            name, contact_name, job_title, address, phone, email, website,
            abs(hash(coalesce(contact_name, '') || coalesce(job_title, '') || coalesce(address, ''))) as fp
        FROM read_parquet('{f_exec_clean}')
    )
    SELECT 
        count(*) as total_matched,
        count(CASE WHEN phone != '' AND length(regexp_replace(phone, '[^0-9]', '', 'g')) >= 7 THEN 1 END) as has_phone,
        count(CASE WHEN email != '' AND email LIKE '%@%.__%' THEN 1 END) as has_email,
        count(CASE WHEN website != '' AND website LIKE '%.__%' THEN 1 END) as has_website,
        count(CASE WHEN (phone = '' OR phone IS NULL) AND (email = '' OR email IS NULL) AND (website = '' OR website IS NULL) THEN 1 END) as no_contacts_at_all
    FROM exec_with_fp e
    JOIN excl x ON e.fp = x.record_fingerprint
"""
res_contacts = con.execute(q_check_contacts).fetchone()
print(f"\nBreakdown of the excluded raw records preserved in b2b_executives_cleaned:")
print(f"  Total Matched Records:          {res_contacts[0]:,}")
print(f"  Have Valid Phone:               {res_contacts[1]:,}")
print(f"  Have Valid Email:               {res_contacts[2]:,}")
print(f"  Have Valid Website:             {res_contacts[3]:,}")
print(f"  NO PHONE, NO EMAIL, NO WEBSITE: {res_contacts[4]:,}")

# Check 5: Inspect sample of these records
print("\nSample of records present in b2b_executives_cleaned that were excluded from raw shards:")
sample_rows = con.execute(f"""
    WITH excl AS (
        SELECT record_fingerprint
        FROM read_parquet('{f_excl_log}')
    ),
    exec_with_fp AS (
        SELECT 
            id, name, contact_name, job_title, address, city, state, phone, email, website,
            abs(hash(coalesce(contact_name, '') || coalesce(job_title, '') || coalesce(address, ''))) as fp
        FROM read_parquet('{f_exec_clean}')
    )
    SELECT e.name, e.contact_name, e.job_title, e.address, e.phone, e.email, e.website
    FROM exec_with_fp e
    JOIN excl x ON e.fp = x.record_fingerprint
    LIMIT 10
""").fetchall()

for i, r in enumerate(sample_rows, 1):
    print(f"  {i}. Name='{r[0]}' | Contact='{r[1]}' | Title='{r[2]}' | Loc='{r[3]}' | Phone='{r[4]}' | Email='{r[5]}' | Web='{r[6]}'")

