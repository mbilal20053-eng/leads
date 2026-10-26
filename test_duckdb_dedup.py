import duckdb
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()
t0 = time.time()
p = r"d:\leads\free-tier (2).csv".replace("\\", "/")

# Load table
con.execute(f"""
    CREATE OR REPLACE TEMP TABLE t_test AS 
    SELECT 
        row_number() over() as row_id,
        *,
        regexp_replace(coalesce("Phone numbers", "Mobile", ''), '\\D', '', 'g') as norm_phone,
        lower(trim(coalesce("Full name", ''))) as norm_contact,
        lower(trim(coalesce("Location", "Locality", ''))) as norm_location
    FROM read_csv("{p}", all_varchar=true, ignore_errors=true)
""")

# Check phone + contact match
res = con.execute("""
    WITH dup_pc AS (
        SELECT norm_phone, norm_contact, count(*) as cnt
        FROM t_test
        WHERE norm_phone != '' AND length(norm_phone) >= 7 AND norm_contact != ''
        GROUP BY norm_phone, norm_contact
        HAVING count(*) > 1
    )
    SELECT count(*) as groups, coalesce(sum(cnt), 0) as affected_rows, coalesce(sum(cnt - 1), 0) as removable_rows
    FROM dup_pc
""").fetchone()

print(f"File: free-tier (2).csv")
print(f"Duplicate (Phone + Same Contact Person) Groups: {res[0]:,}")
print(f"Total Rows in these groups: {res[1]:,}")
print(f"Removable duplicate copies under Rule 2: {res[2]:,}")

# What if phone is same, but contact person is DIFFERENT?
diff_people = con.execute("""
    WITH shared_phone AS (
        SELECT norm_phone, count(distinct norm_contact) as distinct_people, count(*) as cnt
        FROM t_test
        WHERE norm_phone != '' AND length(norm_phone) >= 7 AND norm_contact != ''
        GROUP BY norm_phone
        HAVING count(distinct norm_contact) > 1
    )
    SELECT count(*) as phone_groups, sum(distinct_people) as total_people, sum(cnt) as total_records
    FROM shared_phone
""").fetchone()

print(f"\nSame Phone Shared by DIFFERENT People (Must KEEP): {diff_people[0]:,} phone groups ({diff_people[1]:,} distinct people across {diff_people[2]:,} records)")
