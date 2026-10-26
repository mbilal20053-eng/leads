import sys
sys.path.insert(0, r"D:\leads\repo")
from gui.lead_db import GLOBAL_DUCKDB_CON

def inspect_categories():
    print("=== CATEGORIES IN v_all_unified ===")
    r = GLOBAL_DUCKDB_CON.execute("SELECT count(distinct category), count(*) FROM v_all_unified").fetchone()
    print(f"Distinct Categories: {r[0]}, Total Rows: {r[1]:,}")
    top = GLOBAL_DUCKDB_CON.execute("SELECT category, count(*) FROM v_all_unified GROUP BY 1 ORDER BY 2 DESC LIMIT 5").fetchall()
    for cat, cnt in top:
        print(f"  {cat}: {cnt:,}")

    print("\n=== CATEGORIES IN v_data_legion ===")
    r2 = GLOBAL_DUCKDB_CON.execute("SELECT count(distinct category), count(*) FROM v_data_legion").fetchone()
    print(f"Distinct Categories: {r2[0]}, Total Rows: {r2[1]:,}")
    top2 = GLOBAL_DUCKDB_CON.execute("SELECT category, count(*) FROM v_data_legion GROUP BY 1 ORDER BY 2 DESC LIMIT 5").fetchall()
    for cat, cnt in top2:
        print(f"  {cat}: {cnt:,}")

    print("\n=== CATEGORIES IN v_free_company_db ===")
    # Quick sample or top
    top3 = GLOBAL_DUCKDB_CON.execute("SELECT category, count(*) FROM (SELECT category FROM v_free_company_db LIMIT 500000) GROUP BY 1 ORDER BY 2 DESC LIMIT 5").fetchall()
    for cat, cnt in top3:
        print(f"  {cat}: {cnt:,}")

if __name__ == "__main__":
    inspect_categories()
