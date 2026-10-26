"""
INVESTIGATE SPECIFIC INCONSISTENCIES FROM PREVIOUS AUDIT:
1. Fitness Wellness Texas (6 excluded vs 0 earlier)
2. GLEIF Golden Copy (50 excluded vs 3 earlier)
3. 822 b2b_executives exclusions vs 1,275,044 raw exclusions overlap
4. Double counting across source files, consolidated outputs, and views
5. 57,503,110 fully scanned figure breakdown
"""
import os
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()

print("=" * 110)
print("INVESTIGATING INCONSISTENCY 1: FITNESS WELLNESS TEXAS (6 EXCLUDED)")
print("=" * 110)

fw_path = r"C:\Users\billu\Downloads\fitness_wellness_texas_20261016_123305_crm.csv".replace("\\", "/")
# Check the 6 rows that lacked Business, Phone, Website
# Let's inspect rows where Business IS NULL or placeholder, Phone is invalid, Website is invalid
q_fw = f"""
    SELECT 
        "Tier", "Score", "Business", "Category", "City", "Phone", "Website"
    FROM read_csv_auto('{fw_path}', ignore_errors=true)
    WHERE (
        "Business" IS NULL 
        OR trim(CAST("Business" AS VARCHAR)) = '' 
        OR lower(trim(CAST("Business" AS VARCHAR))) IN ('unknown', 'unknown business', 'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..', 'tbd', 'test')
        OR length(trim(CAST("Business" AS VARCHAR))) <= 1
    )
    AND (
        "Phone" IS NULL 
        OR length(regexp_replace(CAST("Phone" AS VARCHAR), '[^0-9]', '', 'g')) < 7
    )
    AND (
        "Website" IS NULL 
        OR length(trim(CAST("Website" AS VARCHAR))) < 4
        OR lower(trim(CAST("Website" AS VARCHAR))) NOT LIKE '%.__%'
    )
"""
fw_rows = con.execute(q_fw).fetchall()
print(f"Found {len(fw_rows)} rows matching all 4 missing in Fitness Wellness Texas:")
for i, r in enumerate(fw_rows, 1):
    print(f"  Row {i}: Business='{r[2]}', Phone='{r[5]}', Website='{r[6]}', Category='{r[3]}', City='{r[4]}', Tier='{r[0]}'")

# Check if an export was actually made for fitness wellness texas
clean_fw_export = r"d:\leads\cleaned_export\fitness_tx_cleaned.parquet"
print(f"Was a cleaned export file generated for Fitness Wellness Texas? {os.path.exists(clean_fw_export)}")

print("\n" + "=" * 110)
print("INVESTIGATING INCONSISTENCY 2: GLEIF (50 EXCLUDED VS 3 EARLIER)")
print("=" * 110)

gleif_path = r"d:\leads\gleif_goldencopy.parquet".replace("\\", "/")
# Why did it report 50 excluded in dataset_before_after.csv?
# Let's check what query was run in execute_full_portfolio_audit_and_cleanup.py:
# In execute script:
# name = "name", phones = [], emails = [], webs = []
# valid_fields_sum = (CASE WHEN {v_name} THEN 1 ELSE 0 END + 0 + 0 + 0)
# So if name was NOT valid, valid_fields_sum was 0!
# Because phones, emails, webs were all empty!
# Let's inspect those rows where valid_name was false:
q_gleif = f"""
    SELECT lei, name, city, country
    FROM read_parquet('{gleif_path}')
    WHERE name IS NULL 
       OR length(trim(CAST(name AS VARCHAR))) <= 1
       OR lower(trim(CAST(name AS VARCHAR))) IN ('unknown', 'unknown business', 'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..', 'tbd', 'test')
"""
gleif_rows = con.execute(q_gleif).fetchall()
print(f"Total rows in GLEIF where name is missing/placeholder: {len(gleif_rows)}")
for i, r in enumerate(gleif_rows[:15], 1):
    print(f"  Row {i}: LEI='{r[0]}', Name='{r[1]}', City='{r[2]}', Country='{r[3]}'")

# Check what the earlier report of 3 matches was:
# Earlier script inspect_gleif_count.py checked specific placeholders
print("\n" + "=" * 110)
print("INVESTIGATING INCONSISTENCY 3: 822 B2B EXECUTIVES EXCLUSIONS VS 1,275,044 RAW EXCLUSIONS")
print("=" * 110)

b2b_pq_path = r"d:\leads\b2b_executives.parquet".replace("\\", "/")
excl_log_path = r"d:\leads\cleaned_export\exclusion_log_full.parquet".replace("\\", "/")

# Check the 822 rows in b2b_executives.parquet where all 4 are missing
q_b2b_822 = f"""
    SELECT count(*) 
    FROM read_parquet('{b2b_pq_path}')
    WHERE (
        name IS NULL 
        OR length(trim(CAST(name AS VARCHAR))) <= 1
        OR lower(trim(CAST(name AS VARCHAR))) IN ('unknown', 'unknown business', 'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..', 'tbd', 'test')
    )
    AND (phone IS NULL OR length(regexp_replace(CAST(phone AS VARCHAR), '[^0-9]', '', 'g')) < 7)
    AND (email IS NULL OR length(trim(CAST(email AS VARCHAR))) < 6 OR lower(trim(CAST(email AS VARCHAR))) NOT LIKE '%@%.__%')
    AND (website IS NULL OR length(trim(CAST(website AS VARCHAR))) < 4 OR lower(trim(CAST(website AS VARCHAR))) NOT LIKE '%.__%')
"""
cnt_822 = con.execute(q_b2b_822).fetchone()[0]
print(f"Count of all-4-missing in b2b_executives.parquet: {cnt_822}")

# Check overlap: b2b_executives.parquet was built from deduplicating free-tier (2) through (19)!
# Let's check how b2b_executives was created and whether the 822 records are a subset of the 1,275,043 raw exclusions
overlap_q = f"""
    WITH b2b_bad AS (
        SELECT 
            abs(hash(coalesce(contact_name, '') || coalesce(job_title, '') || coalesce(address, ''))) as fp
        FROM read_parquet('{b2b_pq_path}')
        WHERE (
            name IS NULL 
            OR length(trim(CAST(name AS VARCHAR))) <= 1
            OR lower(trim(CAST(name AS VARCHAR))) IN ('unknown', 'unknown business', 'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..', 'tbd', 'test')
        )
        AND (phone IS NULL OR length(regexp_replace(CAST(phone AS VARCHAR), '[^0-9]', '', 'g')) < 7)
        AND (email IS NULL OR length(trim(CAST(email AS VARCHAR))) < 6 OR lower(trim(CAST(email AS VARCHAR))) NOT LIKE '%@%.__%')
        AND (website IS NULL OR length(trim(CAST(website AS VARCHAR))) < 4 OR lower(trim(CAST(website AS VARCHAR))) NOT LIKE '%.__%')
    )
    SELECT count(*) 
    FROM b2b_bad b
    JOIN read_parquet('{excl_log_path}') e ON b.fp = e.record_fingerprint
"""
overlap_cnt = con.execute(overlap_q).fetchone()[0]
print(f"Overlap between 822 b2b_executives exclusions and raw exclusion log fingerprints: {overlap_cnt}")

print("\n" + "=" * 110)
print("INVESTIGATING INCONSISTENCY 4 & 5: FULLY SCANNED (57,503,110) VS UNIQUE SOURCES")
print("=" * 110)
# Sum of total_rows in dataset_before_after.csv
# Let's inspect the breakdown of the 57,503,110 figure
csv_report = r"d:\leads\cleaned_export\dataset_before_after.csv".replace("\\", "/")
ds_rows = con.execute(f"SELECT dataset_id, label, original_rows FROM read_csv_auto('{csv_report}')").fetchall()
tot_scanned = sum(r[2] for r in ds_rows)
print(f"Total rows summed in dataset_before_after.csv: {tot_scanned:,}")
for r in ds_rows:
    print(f"  {r[0]:<25} | {r[1]:<35} | {r[2]:>12,}")

