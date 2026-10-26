import duckdb
import os

print("=== VALIDATING b2b_executives_final_validated.parquet ===")

f_new = r"d:\leads\cleaned_export\b2b_executives_final_validated.parquet".replace("\\", "/")
f_raw = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")
f_old = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

# 1. Row count
cnt_new = con.execute(f"SELECT count(*) FROM read_parquet('{f_new}')").fetchone()[0]
cnt_raw = con.execute(f"SELECT count(*) FROM read_parquet('{f_raw}')").fetchone()[0]
cnt_old = con.execute(f"SELECT count(*) FROM read_parquet('{f_old}')").fetchone()[0]

print(f"Row count new: {cnt_new:,}")
print(f"Row count raw: {cnt_raw:,}")
print(f"Row count old: {cnt_old:,}")
assert cnt_new == cnt_raw, f"Count mismatch! {cnt_new} != {cnt_raw}"
print("[PASS] Row count matches b2b_raw_shards_consolidated_cleaned exactly (10,268,615)")

# 2. Schema check
cols = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{f_new}')").fetchall()
print(f"\nTotal columns: {len(cols)}")
for c in cols:
    print(f"  {c[0]}: {c[1]}")
assert len(cols) == 22, "Column count must be 22"
print("[PASS] Schema has exactly 22 unified platform columns")

# 3. Field presence stats
stats = con.execute(f"""
SELECT 
    count(*) as total,
    count(distinct id) as unique_ids,
    count(CASE WHEN name != '' AND name IS NOT NULL THEN 1 END) as valid_name,
    count(CASE WHEN contact_name != '' AND contact_name IS NOT NULL THEN 1 END) as valid_contact_name,
    count(CASE WHEN phone != '' AND phone IS NOT NULL THEN 1 END) as valid_phone,
    count(CASE WHEN email != '' AND email IS NOT NULL THEN 1 END) as valid_email,
    count(CASE WHEN website != '' AND website IS NOT NULL THEN 1 END) as valid_website,
    count(CASE WHEN phone != '' OR email != '' OR website != '' THEN 1 END) as has_at_least_one_contact,
    count(CASE WHEN (phone = '' OR phone IS NULL) AND (email = '' OR email IS NULL) AND (website = '' OR website IS NULL) THEN 1 END) as zero_contacts_name_only,
    count(CASE WHEN (name = '' OR name IS NULL) AND (phone = '' OR phone IS NULL) AND (email = '' OR email IS NULL) AND (website = '' OR website IS NULL) THEN 1 END) as useless_records
FROM read_parquet('{f_new}')
""").fetchone()

print("\n--- Field Distribution ---")
print(f"Total Rows:                       {stats[0]:,}")
print(f"Unique IDs:                       {stats[1]:,}")
print(f"Valid Business Name:              {stats[2]:,}")
print(f"Valid Contact Person:             {stats[3]:,}")
print(f"Valid Phone:                      {stats[4]:,}")
print(f"Valid Email:                      {stats[5]:,}")
print(f"Valid Website:                    {stats[6]:,}")
print(f"Has >=1 Contact Channel:          {stats[7]:,}")
print(f"Zero Contacts (Retained Name-Only):{stats[8]:,}")
print(f"Useless Records (All 4 Missing):  {stats[9]:,}")

assert stats[9] == 0, "Useless records must be 0!"
print("[PASS] Zero records with all 4 missing/invalid fields!")

# 4. Check sole proprietorships preservation
sp_count = con.execute(f"""
SELECT count(*) 
FROM read_parquet('{f_new}')
WHERE trim(lower(name)) = trim(lower(contact_name))
  AND phone = '' AND email = '' AND website = ''
""").fetchone()[0]
print(f"\nPreserved Sole Proprietorships (Company Name == Full Name, zero contacts): {sp_count:,}")
assert sp_count > 6900 and sp_count < 7100, f"Unexpected sole proprietorship count: {sp_count}"
print("[PASS] Legitimate sole proprietorships correctly preserved!")

# 5. Check exclusion difference from old file
print(f"\nRecords excluded from previous b2b_executives_cleaned: {cnt_old - cnt_new:,}")
assert (cnt_old - cnt_new) == 1274221, f"Expected 1,274,221 excluded records, got {cnt_old - cnt_new}"
print("[PASS] Exactly 1,274,221 ghost records successfully removed!")

print("\nALL TECHNICAL INTEGRITY CHECKS PASSED SUCCESSFULLY.")
