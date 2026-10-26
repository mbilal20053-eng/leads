"""
Test script for auditing all 4 missing conditions simultaneously
"""
import duckdb

con = duckdb.connect()

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

# Test on free-tier (2).csv
q = f"""
    WITH evaluated AS (
        SELECT 
            CASE WHEN 
                "Company Name" IS NULL 
                OR trim(CAST("Company Name" AS VARCHAR)) = '' 
                OR lower(trim(CAST("Company Name" AS VARCHAR))) = 'unknown business' 
                OR lower(trim(CAST("Company Name" AS VARCHAR))) = 'unknown' 
                OR lower(trim(CAST("Company Name" AS VARCHAR))) IN ({PLACEHOLDER_SQL})
            THEN 1 ELSE 0 END as missing_name,
            
            CASE WHEN NOT (
                ("Phone numbers" IS NOT NULL AND length(regexp_replace(CAST("Phone numbers" AS VARCHAR), '[^0-9]', '', 'g')) >= 7 AND regexp_replace(CAST("Phone numbers" AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000', '1111111', '1234567'))
                OR
                ("Mobile" IS NOT NULL AND length(regexp_replace(CAST("Mobile" AS VARCHAR), '[^0-9]', '', 'g')) >= 7 AND regexp_replace(CAST("Mobile" AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000', '1111111', '1234567'))
            ) THEN 1 ELSE 0 END as missing_phone,
            
            CASE WHEN NOT (
                "Emails" IS NOT NULL 
                AND length(trim(CAST("Emails" AS VARCHAR))) >= 6 
                AND lower(trim(CAST("Emails" AS VARCHAR))) LIKE '%@%.__%'
                AND lower(trim(CAST("Emails" AS VARCHAR))) NOT IN ('test@test.com', 'none@none.com', 'null@null.com', 'no@email.com')
            ) THEN 1 ELSE 0 END as missing_email,
            
            CASE WHEN NOT (
                "Company Website" IS NOT NULL 
                AND length(trim(CAST("Company Website" AS VARCHAR))) >= 4 
                AND lower(trim(CAST("Company Website" AS VARCHAR))) LIKE '%.__%'
                AND lower(trim(CAST("Company Website" AS VARCHAR))) NOT IN ('null', 'none', 'nan', 'n/a', 'na', 'http://', 'https://', 'www.', 'http', 'https')
            ) THEN 1 ELSE 0 END as missing_web,
            
            coalesce(CAST("Full name" AS VARCHAR), '') || '|' || coalesce(CAST("Job title" AS VARCHAR), '') || '|' || coalesce(CAST("Location" AS VARCHAR), '') as dedup_key
        FROM read_csv_auto('d:/leads/free-tier (2).csv', ignore_errors=true)
    )
    SELECT 
        count(*) as total_rows,
        sum(missing_name) as cnt_missing_name,
        sum(missing_phone) as cnt_missing_phone,
        sum(missing_email) as cnt_missing_email,
        sum(missing_web) as cnt_missing_web,
        sum(CASE WHEN missing_name=1 AND missing_phone=1 AND missing_email=1 AND missing_web=1 THEN 1 ELSE 0 END) as all_4_missing,
        count(DISTINCT CASE WHEN missing_name=1 AND missing_phone=1 AND missing_email=1 AND missing_web=1 THEN dedup_key END) as unique_matching_rows
    FROM evaluated
"""

row = con.execute(q).fetchone()
print("free-tier (2).csv test:")
print(f"Total Rows:             {row[0]:>10,}")
print(f"Missing Name:           {row[1]:>10,}")
print(f"Missing Phone:          {row[2]:>10,}")
print(f"Missing Email:          {row[3]:>10,}")
print(f"Missing Website:        {row[4]:>10,}")
print(f"All 4 Missing (Total):  {row[5]:>10,}")
print(f"All 4 Missing (Unique): {row[6]:>10,}")
print(f"Duplicates in Matching: {row[5] - row[6]:>10,}")
