import os
import sys

sys.path.insert(0, r"D:\leads\repo")
from gui.lead_db import GLOBAL_DUCKDB_CON, VIEW_MAP, LOCAL_SOURCES

def inspect_all():
    print("=== DUCKDB TABLES & VIEWS ===")
    tables = GLOBAL_DUCKDB_CON.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    print(f"Total Tables/Views: {len(table_names)}")
    for t in sorted(table_names):
        try:
            cnt = GLOBAL_DUCKDB_CON.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            # Check if category column exists
            cols = [c[0] for c in GLOBAL_DUCKDB_CON.execute(f"DESCRIBE {t}").fetchall()]
            has_cat = 'category' in cols
            print(f"  {t:25} -> {cnt:,} rows | has_category: {has_cat}")
        except Exception as e:
            print(f"  {t:25} -> Error: {e}")

    print("\n=== VIEW_MAP MAPPINGS ===")
    for k, v in VIEW_MAP.items():
        print(f"  {k:25} -> view: {v[0]:20} | label: {v[1]}")

if __name__ == "__main__":
    inspect_all()
