import os
import glob
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"d:\leads"
con = duckdb.connect()

print("=" * 80)
print("  LEAD ENGINE PRO - EXACT FULL NAME DUPLICATE AUDIT")
print("=" * 80)

# 1. Gather all files in d:\leads
b2b_files = [os.path.join(data_dir, f"free-tier ({i}).csv").replace("\\", "/") for i in range(2, 20)]
valid_b2b = [p for p in b2b_files if os.path.exists(p)]

spec_files = [
    os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv").replace("\\", "/"),
    os.path.join(data_dir, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv").replace("\\", "/"),
    os.path.join(data_dir, "166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv").replace("\\", "/"),
    os.path.join(data_dir, "74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv").replace("\\", "/"),
    os.path.join(data_dir, "94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv").replace("\\", "/"),
    os.path.join(data_dir, "b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv").replace("\\", "/"),
    os.path.join(data_dir, "da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv").replace("\\", "/"),
    os.path.join(data_dir, "050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv").replace("\\", "/")
]
valid_spec = [p for p in spec_files if os.path.exists(p)]

print(f"Loaded {len(valid_b2b)} B2B Shard Files and {len(valid_spec)} Specialty Directory Files.")

# Create temporary table for B2B Full Names
con.execute("""
    CREATE TEMP TABLE all_names AS
    SELECT 
        lower(trim(CAST("Full name" AS VARCHAR))) AS clean_name,
        'b2b_shards' AS source_type
    FROM read_csv_auto(?, ignore_errors=true)
    WHERE "Full name" IS NOT NULL 
      AND length(trim(CAST("Full name" AS VARCHAR))) > 1
      AND lower(trim(CAST("Full name" AS VARCHAR))) NOT IN ('none', 'null', 'nan', 'n/a', '-', '--', 'undefined')
""", [valid_b2b])

# Add names from specialty files
for sf in valid_spec:
    fname = os.path.basename(sf)
    con.execute(f"""
        INSERT INTO all_names
        SELECT 
            lower(trim(CAST(name AS VARCHAR))) AS clean_name,
            '{fname}' AS source_type
        FROM read_csv_auto('{sf}', ignore_errors=true)
        WHERE name IS NOT NULL 
          AND length(trim(CAST(name AS VARCHAR))) > 1
          AND lower(trim(CAST(name AS VARCHAR))) NOT IN ('none', 'null', 'nan', 'n/a', '-', '--', 'undefined')
    """)

# Total records with valid names
total_valid_names = con.execute("SELECT count(1) FROM all_names").fetchone()[0]
total_distinct_names = con.execute("SELECT count(DISTINCT clean_name) FROM all_names").fetchone()[0]

# Aggregate duplicates
dup_stats = con.execute("""
    SELECT 
        count(1) AS unique_repeated_names,
        sum(cnt) AS total_records_with_repeated_names,
        sum(cnt - 1) AS excess_duplicate_records
    FROM (
        SELECT clean_name, count(1) AS cnt
        FROM all_names
        GROUP BY clean_name
        HAVING count(1) > 1
    )
""").fetchone()

unique_repeated = dup_stats[0] or 0
total_records_repeated = dup_stats[1] or 0
excess_records = dup_stats[2] or 0

print("\n" + "=" * 80)
print("  RESULTS ACROSS ALL DATABASE FILES & SHARDS")
print("=" * 80)
print(f"Total rows analyzed with a person / contact name : {total_valid_names:,}")
print(f"Total distinct (unique) names in the entire database : {total_distinct_names:,}")
print("-" * 80)
print(f"1. Number of UNIQUE names that appear more than once   : {unique_repeated:,}")
print(f"2. TOTAL records that have these repeated names       : {total_records_repeated:,}")
print(f"3. EXCESS duplicate records (occurrences beyond first) : {excess_records:,}")
print(f"   Repeat Rate (Excess Records / Total Valid Names)    : {(excess_records / total_valid_names * 100):.2f}%")
print("=" * 80)

# Top 25 Most Frequently Repeated Names
print("\nTOP 25 MOST FREQUENTLY REPEATED EXACT NAMES:")
print(f"{'#':<4} | {'Exact Full Name':<35} | {'Occurrences':<12}")
print("-" * 57)
top_names = con.execute("""
    SELECT clean_name, count(1) AS cnt
    FROM all_names
    GROUP BY clean_name
    HAVING count(1) > 1
    ORDER BY cnt DESC
    LIMIT 25
""").fetchall()

for i, (nm, cnt) in enumerate(top_names, start=1):
    display_name = nm.title()
    print(f"{i:<4} | {display_name:<35} | {cnt:<12,}")

# Also analyze B2B Shards alone vs Specialty
b2b_only_stats = con.execute("""
    SELECT 
        count(1) AS unique_repeated_names,
        sum(cnt) AS total_records_with_repeated_names,
        sum(cnt - 1) AS excess_duplicate_records
    FROM (
        SELECT clean_name, count(1) AS cnt
        FROM all_names
        WHERE source_type = 'b2b_shards'
        GROUP BY clean_name
        HAVING count(1) > 1
    )
""").fetchone()

print("\n" + "-" * 80)
print("BREAKDOWN: B2B EXECUTIVE DIRECTORY ALONE (18 Shards):")
print(f" - Unique names repeated > 1 time       : {b2b_only_stats[0]:,}")
print(f" - Total records with repeated names   : {b2b_only_stats[1]:,}")
print(f" - Excess duplicate records             : {b2b_only_stats[2]:,}")
print("=" * 80)
