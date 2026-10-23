import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import duckdb

files = {
    "restaurants": "d:/leads/050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv",
    "realtors": "d:/leads/0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv",
    "coaches": "d:/leads/166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv",
    "musicians": "d:/leads/74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv",
    "designers": "d:/leads/94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv",
    "entrepreneurs": "d:/leads/b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv",
    "photographers": "d:/leads/da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv",
    "realestate_b2b": "d:/leads/free-tier.csv"
}

con = duckdb.connect()
print("SCANNING FOR BAD WEBSITES:")
for name, p in files.items():
    clean_p = p.replace("\\", "/")
    web_col = "Email-Domain" if "realestate" in name else "website"
    bad_web = con.execute(f"""
        SELECT "{web_col}", count(*) 
        FROM read_csv_auto('{clean_p}', ignore_errors=true)
        WHERE "{web_col}" IS NOT NULL AND (
            "{web_col}" NOT LIKE '%.%' OR 
            lower(trim("{web_col}")) IN ('null', 'none', 'nan', 'n/a', '')
        )
        GROUP BY 1
    """).fetchall()
    if bad_web:
        print(f"  {name} bad websites ({len(bad_web)} entries): {bad_web[:5]}")
