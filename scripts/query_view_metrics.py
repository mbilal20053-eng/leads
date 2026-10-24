import sys
import os
sys.path.insert(0, r"d:\leads\repo")
from gui.lead_db import GLOBAL_DUCKDB_CON, VIEW_MAP

con = GLOBAL_DUCKDB_CON.cursor()

views = [
    "v_all_unified",
    "v_b2b_executives",
    "v_homeowners",
    "v_realestate_b2b",
    "v_restaurants",
    "v_realtors",
    "v_coaches",
    "v_designers",
    "v_entrepreneurs",
    "v_photographers",
    "v_musicians"
]

print("EXACT DUCKDB VIEW METRICS:")
for v in views:
    try:
        q = f"""
        SELECT 
            count(*) as total,
            count(CASE WHEN tier = 'A' THEN 1 END) as tier_a,
            count(CASE WHEN tier = 'B' THEN 1 END) as tier_b,
            count(CASE WHEN phone IS NOT NULL AND length(trim(phone)) > 5 AND lower(trim(phone)) NOT IN ('null', 'none', 'nan', 'n/a', '', '0') THEN 1 END) as with_phone,
            count(CASE WHEN website IS NOT NULL AND length(trim(website)) > 3 AND lower(trim(website)) NOT IN ('null', 'none', 'nan', 'n/a', '') AND website LIKE '%.%' THEN 1 END) as with_website,
            count(CASE WHEN email IS NOT NULL AND length(trim(email)) > 5 AND lower(trim(email)) NOT IN ('null', 'none', 'nan', 'n/a', '') AND email LIKE '%@%' THEN 1 END) as with_email
        FROM {v}
        """
        row = con.execute(q).fetchone()
        tot, ta, tb, ph, web, em = row[0], row[1], row[2], row[3], row[4], row[5]
        ph_p = (ph / tot * 100) if tot else 0
        web_p = (web / tot * 100) if tot else 0
        em_p = (em / tot * 100) if tot else 0
        print(f"'{v}': (total={tot}, tier_a={ta}, tier_b={tb}, phone={ph} ({ph_p:.2f}%), web={web} ({web_p:.2f}%), email={em} ({em_p:.2f}%))")
    except Exception as e:
        print(f"Error querying {v}: {e}")
