"""
Test contact validation on a sample of affected records in free-tier (2).csv and restaurants
"""
import duckdb

con = duckdb.connect()

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

# Test on 050580a4-restaurants.csv (45 affected rows)
q_rest = f"""
    SELECT 
        name,
        phone,
        email,
        website,
        CASE WHEN phone IS NOT NULL AND length(regexp_replace(CAST(phone AS VARCHAR), '[^0-9]', '', 'g')) >= 7 THEN 1 ELSE 0 END as has_phone,
        CASE WHEN email IS NOT NULL AND length(trim(CAST(email AS VARCHAR))) >= 6 AND lower(trim(CAST(email AS VARCHAR))) LIKE '%@%.__%' THEN 1 ELSE 0 END as has_email,
        CASE WHEN website IS NOT NULL AND length(trim(CAST(website AS VARCHAR))) >= 4 AND lower(trim(CAST(website AS VARCHAR))) LIKE '%.__%' THEN 1 ELSE 0 END as has_web
    FROM read_csv_auto('d:/leads/050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv', ignore_errors=true)
    WHERE 
        name IS NULL 
        OR trim(CAST(name AS VARCHAR)) = '' 
        OR lower(trim(CAST(name AS VARCHAR))) = 'unknown business'
        OR lower(trim(CAST(name AS VARCHAR))) = 'unknown'
        OR lower(trim(CAST(name AS VARCHAR))) IN ({PLACEHOLDER_SQL})
    LIMIT 10
"""

rows = con.execute(q_rest).fetchall()
print("Sample affected restaurants:")
for r in rows:
    print(r)
