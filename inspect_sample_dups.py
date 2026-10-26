import duckdb
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = duckdb.connect()
p = r"d:\leads\free-tier (2).csv".replace("\\", "/")

con.execute(f"""
    CREATE OR REPLACE TEMP TABLE t_test AS 
    SELECT 
        row_number() over() as row_id,
        "Full name", "Phone numbers", "Mobile", "Company Name", "Location", "Locality", "Region",
        regexp_replace(coalesce("Phone numbers", "Mobile", ''), '\\D', '', 'g') as norm_phone,
        lower(trim(coalesce("Full name", ''))) as norm_contact,
        lower(trim(coalesce("Location", "Locality", ''))) as norm_location
    FROM read_csv("{p}", all_varchar=true, ignore_errors=true)
""")

# Sample groups
samples = con.execute("""
    WITH dup_pc AS (
        SELECT norm_phone, norm_contact, count(*) as cnt, count(distinct norm_location) as distinct_locs
        FROM t_test
        WHERE norm_phone != '' AND length(norm_phone) >= 7 AND norm_contact != ''
        GROUP BY norm_phone, norm_contact
        HAVING count(*) > 1
    )
    SELECT * FROM dup_pc LIMIT 5
""").fetchall()

print("Sample Duplicate (Same Phone + Same Contact Name) Groups:")
for p, c, cnt, dlocs in samples:
    print(f"  • Contact: \"{c}\" | Phone: {p} | Count: {cnt} | Distinct Locations: {dlocs}")
    details = con.execute(f"SELECT \"Full name\", \"Company Name\", \"Location\", \"Phone numbers\", \"Mobile\" FROM t_test WHERE norm_phone='{p}' AND norm_contact='{c}'").fetchall()
    for row in details:
        print(f"      -> Name: {row[0]} | Co: {row[1]} | Loc: {row[2]} | Phone: {row[3]} | Mob: {row[4]}")
