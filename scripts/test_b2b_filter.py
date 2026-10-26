"""
Test contact validation on affected records in free-tier (2).csv
"""
import duckdb

con = duckdb.connect()

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

# Phone condition (Phone numbers or Mobile)
phone_cond = """(
    ("Phone numbers" IS NOT NULL AND length(regexp_replace(CAST("Phone numbers" AS VARCHAR), '[^0-9]', '', 'g')) >= 7 AND regexp_replace(CAST("Phone numbers" AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000'))
    OR
    ("Mobile" IS NOT NULL AND length(regexp_replace(CAST("Mobile" AS VARCHAR), '[^0-9]', '', 'g')) >= 7 AND regexp_replace(CAST("Mobile" AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000'))
)"""

# Email condition
email_cond = """(
    "Emails" IS NOT NULL 
    AND length(trim(CAST("Emails" AS VARCHAR))) >= 6 
    AND lower(trim(CAST("Emails" AS VARCHAR))) LIKE '%@%.__%'
    AND lower(trim(CAST("Emails" AS VARCHAR))) NOT IN ('test@test.com', 'none@none.com', 'null@null.com', 'no@email.com')
)"""

# Website condition
web_cond = """(
    "Company Website" IS NOT NULL 
    AND length(trim(CAST("Company Website" AS VARCHAR))) >= 4 
    AND lower(trim(CAST("Company Website" AS VARCHAR))) LIKE '%.__%'
    AND lower(trim(CAST("Company Website" AS VARCHAR))) NOT IN ('null', 'none', 'nan', 'n/a', 'na', 'http://', 'https://')
)"""

q = f"""
    SELECT 
        count(*) as total_affected,
        count(CASE WHEN ({phone_cond}) AND NOT ({email_cond}) AND NOT ({web_cond}) THEN 1 END) as phone_only,
        count(CASE WHEN ({email_cond}) AND NOT ({phone_cond}) AND NOT ({web_cond}) THEN 1 END) as email_only,
        count(CASE WHEN ({web_cond}) AND NOT ({phone_cond}) AND NOT ({email_cond}) THEN 1 END) as web_only,
        count(CASE WHEN (({phone_cond}) AND ({email_cond})) OR (({phone_cond}) AND ({web_cond})) OR (({email_cond}) AND ({web_cond})) THEN 1 END) as multi_contact,
        count(CASE WHEN ({phone_cond}) OR ({email_cond}) OR ({web_cond}) THEN 1 END) as has_at_least_one,
        count(CASE WHEN NOT ({phone_cond}) AND NOT ({email_cond}) AND NOT ({web_cond}) THEN 1 END) as qualifies_for_removal
    FROM read_csv_auto('d:/leads/free-tier (2).csv', ignore_errors=true)
    WHERE 
        "Company Name" IS NULL 
        OR trim(CAST("Company Name" AS VARCHAR)) = '' 
        OR lower(trim(CAST("Company Name" AS VARCHAR))) = 'unknown business'
        OR lower(trim(CAST("Company Name" AS VARCHAR))) = 'unknown'
        OR lower(trim(CAST("Company Name" AS VARCHAR))) IN ({PLACEHOLDER_SQL})
"""

row = con.execute(q).fetchone()
print("free-tier (2).csv affected breakdown:")
print(f"Total Affected:             {row[0]:>10,}")
print(f"Phone Only:                 {row[1]:>10,}")
print(f"Email Only:                 {row[2]:>10,}")
print(f"Web Only:                   {row[3]:>10,}")
print(f"Multiple Contacts:          {row[4]:>10,}")
print(f"Has AT LEAST ONE Contact:   {row[5]:>10,} (PRESERVED)")
print(f"Has NO CONTACT AT ALL:      {row[6]:>10,} (QUALIFIES FOR REMOVAL)")
