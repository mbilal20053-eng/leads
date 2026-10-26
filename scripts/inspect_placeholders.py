import duckdb

con = duckdb.connect()

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

res = con.execute(f"""
    SELECT lower(trim(name)) as placeholder_val, count(*) as cnt
    FROM read_parquet('d:/leads/b2b_executives.parquet')
    WHERE lower(trim(name)) IN ({PLACEHOLDER_SQL})
    GROUP BY 1
    ORDER BY cnt DESC
""").fetchall()

print("Top placeholders in b2b_executives.parquet:")
for val, count in res:
    print(f"  {repr(val):<20}: {count:>6,}")
