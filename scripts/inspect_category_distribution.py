import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

con = lead_db.GLOBAL_DUCKDB_CON

print("=== CATEGORY DISTRIBUTION IN DUCKDB ===")

# Query all categories across v_all_unified
q = """
SELECT 
    CASE 
        WHEN category IS NULL OR trim(category) = '' OR lower(trim(category)) IN ('none', 'null', 'nan', 'undefined', 'n/a') THEN 'Uncategorized'
        ELSE trim(category)
    END as cat_name,
    count(*) as lead_count
FROM v_all_unified
GROUP BY 1
ORDER BY lead_count DESC;
"""

cats = con.execute(q).fetchall()
print(f"Total Category Groups: {len(cats)}")
print("\nTop 25 Categories:")
for c, cnt in cats[:25]:
    print(f"  {c:<45}: {cnt:>12,}")

uncat = [cnt for c, cnt in cats if c == 'Uncategorized']
print(f"\nUncategorized Leads: {uncat[0] if uncat else 0:,}")

# Let's also check for multi-category leads (e.g. semicolon, comma, slash separated)
slash_cats = [c for c, cnt in cats if '/' in c or ';' in c or ',' in c]
print(f"Categories with delimiters (slashes/commas/semicolons): {len(slash_cats)}")
