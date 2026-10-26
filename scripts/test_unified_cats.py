import sys
sys.path.insert(0, r"D:\leads\repo")
from gui.lead_db import GLOBAL_DUCKDB_CON
from gui import categories_service

def test_unified_aggregation():
    sql = """
    SELECT 
        CASE 
            WHEN category IS NULL OR trim(category) = '' OR lower(trim(category)) IN ('none', 'null', 'nan', 'undefined', 'n/a', '0') THEN 'Uncategorized'
            ELSE lower(trim(category))
        END as norm_cat,
        min(trim(category)) as sample_raw,
        count(*) as cnt
    FROM v_all_unified
    GROUP BY 1
    ORDER BY cnt DESC;
    """
    rows = GLOBAL_DUCKDB_CON.execute(sql).fetchall()
    total_leads = sum(r[2] for r in rows)
    print(f"Total Normalized Categories: {len(rows)}")
    print(f"Total Leads in v_all_unified: {total_leads:,}")
    print("\nTop 15 Categories in Unified Portfolio:")
    for norm_cat, sample_raw, cnt in rows[:15]:
        lbl = categories_service.format_category_label(sample_raw) if norm_cat != 'uncategorized' else 'Uncategorized'
        pct = (cnt / total_leads) * 100
        print(f"  {lbl:45} : {cnt:10,} ({pct:5.2f}%)")

if __name__ == "__main__":
    test_unified_aggregation()
