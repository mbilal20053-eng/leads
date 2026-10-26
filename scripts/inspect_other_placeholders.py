import duckdb

con = duckdb.connect()

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

for ds_name, p, fn in [
    ("tech_stack_companies.parquet", "d:/leads/tech_stack_companies.parquet", "read_parquet"),
    ("gleif_goldencopy.parquet", "d:/leads/gleif_goldencopy.parquet", "read_parquet"),
    ("data-legion.csv.gz", "d:/leads/data-legion-company-free-1.5.0_2026-10-15.csv.gz", "read_csv_auto")
]:
    res = con.execute(f"""
        SELECT lower(trim(name)) as val, count(*) as cnt
        FROM {fn}('{p}')
        WHERE lower(trim(name)) IN ({PLACEHOLDER_SQL})
        GROUP BY 1
        ORDER BY cnt DESC
    """).fetchall()
    print(f"\nPlaceholders in {ds_name}:")
    for val, cnt in res:
        print(f"  {repr(val):<20}: {cnt:>5}")
