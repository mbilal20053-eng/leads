"""
Filter simulation on v_all_unified
"""
import sys
import duckdb

sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = duckdb.connect()
lead_db.init_lead_views(con, r"d:\leads")

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

phone_sql = """(
    phone IS NOT NULL 
    AND length(regexp_replace(CAST(phone AS VARCHAR), '[^0-9]', '', 'g')) >= 7 
    AND regexp_replace(CAST(phone AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000', '1111111', '1234567')
)"""

email_sql = """(
    email IS NOT NULL 
    AND length(trim(CAST(email AS VARCHAR))) >= 6 
    AND lower(trim(CAST(email AS VARCHAR))) LIKE '%@%.__%'
    AND lower(trim(CAST(email AS VARCHAR))) NOT IN ('test@test.com', 'none@none.com', 'null@null.com', 'no@email.com')
)"""

web_sql = """(
    website IS NOT NULL 
    AND length(trim(CAST(website AS VARCHAR))) >= 4 
    AND lower(trim(CAST(website AS VARCHAR))) LIKE '%.__%'
    AND lower(trim(CAST(website AS VARCHAR))) NOT IN ('null', 'none', 'nan', 'n/a', 'na', 'http://', 'https://', 'www.', 'http', 'https')
)"""

name_cond = f"""(
    name IS NULL 
    OR trim(CAST(name AS VARCHAR)) = '' 
    OR lower(trim(CAST(name AS VARCHAR))) = 'unknown business' 
    OR lower(trim(CAST(name AS VARCHAR))) = 'unknown' 
    OR lower(trim(CAST(name AS VARCHAR))) IN ({PLACEHOLDER_SQL})
)"""

q = f"""
    SELECT 
        count(*) as total_rows,
        count(CASE WHEN {name_cond} THEN 1 END) as total_affected,
        count(CASE WHEN {name_cond} AND ({phone_sql}) AND NOT ({email_sql}) AND NOT ({web_sql}) THEN 1 END) as phone_only,
        count(CASE WHEN {name_cond} AND ({email_sql}) AND NOT ({phone_sql}) AND NOT ({web_sql}) THEN 1 END) as email_only,
        count(CASE WHEN {name_cond} AND ({web_sql}) AND NOT ({phone_sql}) AND NOT ({email_sql}) THEN 1 END) as web_only,
        count(CASE WHEN {name_cond} AND (
            (({phone_sql}) AND ({email_sql})) OR (({phone_sql}) AND ({web_sql})) OR (({email_sql}) AND ({web_sql}))
        ) THEN 1 END) as multiple_contacts,
        count(CASE WHEN {name_cond} AND (({phone_sql}) OR ({email_sql}) OR ({web_sql})) THEN 1 END) as has_at_least_one,
        count(CASE WHEN {name_cond} AND NOT ({phone_sql}) AND NOT ({email_sql}) AND NOT ({web_sql}) THEN 1 END) as qualifies_for_removal
    FROM v_all_unified
"""

row = con.execute(q).fetchone()
print("v_all_unified filter simulation:")
print(f"Total Rows:                 {row[0]:>10,}")
print(f"Total Affected:             {row[1]:>10,}")
print(f"Phone Only:                 {row[2]:>10,}")
print(f"Email Only:                 {row[3]:>10,}")
print(f"Web Only:                   {row[4]:>10,}")
print(f"Multiple Contacts:          {row[5]:>10,}")
print(f"Preserved (At least one):   {row[6]:>10,} ({row[6]/row[1]*100:.2f}%)")
print(f"Qualifies for Removal:      {row[7]:>10,} ({row[7]/row[1]*100:.2f}%)")
