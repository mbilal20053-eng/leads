import duckdb
import os
import time

print("=== GENERATING b2b_executives_final_validated.parquet ===")
start_t = time.time()

f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")
f_out = r"d:\leads\cleaned_export\b2b_executives_final_validated.parquet".replace("\\", "/")

if os.path.exists(f_out):
    print(f"ERROR: Destination {f_out} already exists! Exiting to protect data.")
    exit(1)

con = duckdb.connect()
con.execute("PRAGMA threads=8;")
con.execute("PRAGMA memory_limit='12GB';")

transform_query = f"""
SELECT 
    'b2b_' || abs(hash(coalesce("Company Name", "Full name", '') || coalesce("Job title", '') || coalesce("Location", ''))) as id,
    CAST(coalesce("Company Name", "Full name", 'B2B Enterprise') AS VARCHAR) as name,
    CAST(coalesce("Full name", '') AS VARCHAR) as contact_name,
    CAST(coalesce(nullif(trim("Job title"), '') || CASE WHEN "Sub Role" IS NOT NULL AND trim("Sub Role") != '' THEN ' (' || trim("Sub Role") || ')' ELSE '' END, 'Executive Decision Maker') AS VARCHAR) as job_title,
    CAST(coalesce("Company Industry", "Industry", 'Corporate Enterprise') AS VARCHAR) as category,
    CAST(coalesce("Location", '') AS VARCHAR) as address,
    CAST(coalesce("Locality", '') AS VARCHAR) as city,
    CAST(coalesce("Region", '') AS VARCHAR) as state,
    '' as zip,
    'United States' as country,
    CASE WHEN coalesce("Phone numbers", "Mobile") IS NOT NULL AND length(trim(CAST(coalesce("Phone numbers", "Mobile") AS VARCHAR))) > 6 AND lower(trim(CAST(coalesce("Phone numbers", "Mobile") AS VARCHAR))) NOT IN ('', 'null', 'none', 'nan', 'n/a', '0') THEN trim(CAST(coalesce("Phone numbers", "Mobile") AS VARCHAR)) ELSE '' END as phone,
    CASE WHEN "Company Website" IS NOT NULL AND length(trim(CAST("Company Website" AS VARCHAR))) > 3 AND lower(trim(CAST("Company Website" AS VARCHAR))) NOT IN ('', 'null', 'none', 'nan', 'n/a') AND CAST("Company Website" AS VARCHAR) LIKE '%.%' THEN trim(CAST("Company Website" AS VARCHAR)) ELSE '' END as website,
    CASE WHEN "Emails" IS NOT NULL AND length(trim(CAST("Emails" AS VARCHAR))) > 5 AND lower(trim(CAST("Emails" AS VARCHAR))) NOT IN ('', 'null', 'none', 'nan', 'n/a') AND CAST("Emails" AS VARCHAR) LIKE '%@%' THEN trim(CAST("Emails" AS VARCHAR)) ELSE '' END as email,
    CAST(coalesce("LinkedIn Url", '') AS VARCHAR) as socials,
    CASE 
        WHEN "Company Website" IS NOT NULL AND ("Phone numbers" IS NOT NULL OR "Emails" IS NOT NULL) THEN 'A'
        WHEN "Company Website" IS NOT NULL THEN 'A'
        ELSE 'B'
    END as tier,
    CASE 
        WHEN "Company Website" IS NOT NULL AND ("Phone numbers" IS NOT NULL OR "Emails" IS NOT NULL) THEN 92
        WHEN "Company Website" IS NOT NULL THEN 85
        ELSE 65
    END as score,
    CASE 
        WHEN "Company Website" IS NULL OR trim("Company Website") = '' THEN 'NO WEBSITE (Urgent Outreach Need)'
        ELSE 'B2B ENTERPRISE GROWTH AUDIT'
    END as opportunity,
    'B2B growth, digital conversion & sales acceleration for ' || coalesce("Company Name", "Full name", 'Enterprise') || ' in ' || coalesce("Company Industry", "Industry", 'Corporate') || '.' as pitch,
    'Verified corporate decision maker profile with executive title and direct communication channels.' as why,
    '💼 B2B Decision Makers' as source_badge,
    'b2b_executives' as source_id,
    '#3b82f6' as source_color
FROM read_parquet('{f_raw_clean}')
"""

print(f"Exporting transformed dataset from {f_raw_clean} to {f_out}...")
con.execute(f"COPY ({transform_query}) TO '{f_out}' (FORMAT PARQUET, COMPRESSION ZSTD);")

elapsed = time.time() - start_t
print(f"Export completed in {elapsed:.2f} seconds.")

# Verification
cnt = con.execute(f"SELECT count(*) FROM read_parquet('{f_out}')").fetchone()[0]
size_mb = os.path.getsize(f_out) / (1024 * 1024)
print(f"Created file: {f_out}")
print(f"Row count:    {cnt:,}")
print(f"File size:    {size_mb:.2f} MB")
