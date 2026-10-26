"""
PROVE EXACT NUMBERS: 1,274,221 GHOST RECORDS VS 6,966 LEGITIMATE SOLE PROPRIETORSHIPS
"""
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

f_exec_clean = r"d:\leads\cleaned_export\b2b_executives_cleaned.parquet".replace("\\", "/")
f_raw_clean = r"d:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet".replace("\\", "/")
f_excl = r"d:\leads\cleaned_export\exclusion_log_full.parquet".replace("\\", "/")

# Total rows in b2b_executives_cleaned
cnt_exec = con.execute(f"SELECT count(*) FROM read_parquet('{f_exec_clean}')").fetchone()[0]
# Total rows in b2b_raw_shards_consolidated_cleaned
cnt_raw = con.execute(f"SELECT count(*) FROM read_parquet('{f_raw_clean}')").fetchone()[0]
diff = cnt_exec - cnt_raw

print(f"b2b_executives_cleaned.parquet:              {cnt_exec:,}")
print(f"b2b_raw_shards_consolidated_cleaned.parquet: {cnt_raw:,}")
print(f"Exact Difference:                             {diff:,}")

# In exclusion_log_full.parquet, total B2B shard exclusions:
cnt_excl_shards = con.execute(f"SELECT count(*) FROM read_parquet('{f_excl}') WHERE dataset_id LIKE 'b2b_shard_%'").fetchone()[0]
print(f"Exclusion Log (B2B Shards):                  {cnt_excl_shards:,}")
print(f"Claimed b2b_executives exclusions:           822")
print(f"Expected difference (1,275,043 - 822):        {cnt_excl_shards - 822:,}")

# Check the overlap of the 1,281,187 rows with exclusion_log_full
q_match = f"""
    WITH excl AS (
        SELECT record_fingerprint
        FROM read_parquet('{f_excl}')
        WHERE dataset_id LIKE 'b2b_shard_%'
    ),
    exec_1281k AS (
        SELECT 
            id, name, contact_name, job_title, address,
            abs(hash(coalesce(contact_name, '') || coalesce(job_title, '') || coalesce(address, ''))) as fp
        FROM read_parquet('{f_exec_clean}')
        WHERE trim(lower(name)) = trim(lower(contact_name)) 
          AND (phone = '' OR phone IS NULL) 
          AND (email = '' OR email IS NULL) 
          AND (website = '' OR website IS NULL)
    )
    SELECT 
        count(*) as total_1281k,
        count(CASE WHEN x.record_fingerprint IS NOT NULL THEN 1 END) as in_exclusion_log,
        count(CASE WHEN x.record_fingerprint IS NULL THEN 1 END) as NOT_in_exclusion_log
    FROM exec_1281k e
    LEFT JOIN excl x ON e.fp = x.record_fingerprint
"""
res_match = con.execute(q_match).fetchone()
print(f"\nOf the 1,281,187 records:")
print(f"  Matches in Exclusion Log (True Ghost Records): {res_match[1]:,}")
print(f"  NOT in Exclusion Log (Legitimate Retained):    {res_match[2]:,}")
