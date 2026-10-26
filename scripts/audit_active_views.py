"""
Audit active DuckDB views in lead_db.py
STRICT AUDIT ONLY. NO MODIFICATIONS.
"""
import os
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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

views = [
    ("v_restaurants", "Restaurants"),
    ("v_realtors", "Realtors"),
    ("v_coaches", "Coaches"),
    ("v_musicians", "Musicians"),
    ("v_designers", "Designers"),
    ("v_entrepreneurs", "Founders / Entrepreneurs"),
    ("v_photographers", "Photographers"),
    ("v_realestate_b2b", "Commercial Real Estate B2B"),
    ("v_homeowners", "Homeowners & Residential"),
    ("v_b2b_executives", "B2B Executive Decision Makers"),
    ("v_all_unified", "UNIFIED LEADS ENGINE (All Sources Combined)")
]

print("=" * 110)
print("AUDITING UNIFIED PLATFORM VIEWS (v_all_unified and component views)")
print("=" * 110)

for vname, title in views:
    try:
        q = f"""
            SELECT 
                count(*) as total,
                count(CASE WHEN lower(trim(CAST(name AS VARCHAR))) = 'unknown business' THEN 1 END) as exact_ub,
                count(CASE WHEN lower(trim(CAST(name AS VARCHAR))) = 'unknown' THEN 1 END) as exact_unk,
                count(CASE WHEN lower(trim(CAST(name AS VARCHAR))) IN ({PLACEHOLDER_SQL}) THEN 1 END) as placeholders,
                count(CASE WHEN name IS NULL OR trim(CAST(name AS VARCHAR)) = '' THEN 1 END) as blank_missing,
                count(CASE WHEN 
                    lower(trim(CAST(name AS VARCHAR))) = 'unknown business'
                    OR lower(trim(CAST(name AS VARCHAR))) = 'unknown'
                    OR lower(trim(CAST(name AS VARCHAR))) IN ({PLACEHOLDER_SQL})
                    OR name IS NULL 
                    OR trim(CAST(name AS VARCHAR)) = ''
                THEN 1 END) as total_affected
            FROM {vname}
        """
        row = con.execute(q).fetchone()
        tot = row[0]
        ub = row[1]
        unk = row[2]
        ph = row[3]
        bm = row[4]
        aff = row[5]
        pct = (aff / tot * 100) if tot > 0 else 0.0
        
        # Check duplicates in affected records
        dup_cnt = 0
        if aff > 0:
            dup_q = f"""
                SELECT count(*) - count(DISTINCT id)
                FROM {vname}
                WHERE 
                    lower(trim(CAST(name AS VARCHAR))) = 'unknown business'
                    OR lower(trim(CAST(name AS VARCHAR))) = 'unknown'
                    OR lower(trim(CAST(name AS VARCHAR))) IN ({PLACEHOLDER_SQL})
                    OR name IS NULL 
                    OR trim(CAST(name AS VARCHAR)) = ''
            """
            dup_res = con.execute(dup_q).fetchone()
            dup_cnt = dup_res[0] if dup_res else 0
            
        print(f"{title:<45} | Total: {tot:>10,} | 'Unknown Business': {ub:>6,} | 'Unknown': {unk:>6,} | Placeholders: {ph:>6,} | Blank: {bm:>6,} | Total Affected: {aff:>8,} ({pct:>5.2f}%) | Dups: {dup_cnt:>6,}")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error querying {vname}: {e}")
