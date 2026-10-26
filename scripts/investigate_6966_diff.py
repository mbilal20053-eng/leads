"""
INVESTIGATE 6,966 ROW DIFFERENCE BETWEEN 1,281,187 AND 1,274,221
"""
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")
f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")
f_excl = r"d:\leads\cleaned_export\exclusion_log_full.parquet".replace("\\", "/")

# In b2b_executives_cleaned.parquet:
# How many records have name == contact_name and no phone, no email, no website?
q_1281k = f"""
    SELECT count(*)
    FROM read_parquet('{f_exec_clean}')
    WHERE trim(lower(name)) = trim(lower(contact_name)) 
      AND (phone = '' OR phone IS NULL) 
      AND (email = '' OR email IS NULL) 
      AND (website = '' OR website IS NULL)
"""
cnt_1281k = con.execute(q_1281k).fetchone()[0]
print(f"cnt_1281k (name==contact_name & null phone/email/web in b2b_executives_cleaned): {cnt_1281k:,}")

# How many records in b2b_raw_shards_consolidated_cleaned have Company Name == Full name and no phone/email/web?
q_raw_same = f"""
    SELECT count(*)
    FROM read_parquet('{f_raw_clean}')
    WHERE trim(lower("Company Name")) = trim(lower("Full name"))
      AND ("Phone numbers" IS NULL OR "Phone numbers" = '')
      AND ("Emails" IS NULL OR "Emails" = '')
      AND ("Company Website" IS NULL OR "Company Website" = '')
"""
cnt_raw_same = con.execute(q_raw_same).fetchone()[0]
print(f"cnt_raw_same (Company Name == Full name in RAW cleaned shards): {cnt_raw_same:,}")

# Look at sample of records in b2b_raw_shards_consolidated_cleaned where Company Name == Full name:
sample_raw_same = con.execute(f"""
    SELECT "Full name", "Company Name", "Job title", "Location", "Phone numbers", "Emails", "Company Website"
    FROM read_parquet('{f_raw_clean}')
    WHERE trim(lower("Company Name")) = trim(lower("Full name"))
      AND length("Company Name") > 1
    LIMIT 10
""").fetchall()

print(f"\nSample of records in RAW cleaned where Company Name == Full name:")
for r in sample_raw_same:
    print(" ", r)

# Are there legitimate sole proprietorships where the company name was ACTUALLY the person's name in the raw CSV?
q_sole_prop = f"""
    SELECT count(*)
    FROM read_parquet('{f_raw_clean}')
    WHERE trim(lower("Company Name")) = trim(lower("Full name"))
      AND ("Phone numbers" IS NULL OR "Phone numbers" = '')
      AND ("Emails" IS NULL OR "Emails" = '')
      AND ("Company Website" IS NULL OR "Company Website" = '')
"""
print(f"\nLegitimate sole proprietorships in raw shards (Company Name literally equal to Full name in the CSV): {con.execute(q_sole_prop).fetchone()[0]:,}")

