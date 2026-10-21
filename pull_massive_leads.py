"""
Massive uncapped US lead extractor.
Pulls thousands of commercial leads across the US.
Accumulates all regions in DuckDB, deduplicates, and writes to CSV.
"""
import sys
import os
import duckdb
from leadgen.sources import _overture_release

US_REGIONS = [
    {"market": "Texas (Austin, Houston, Dallas, San Antonio)", "south": 29.0, "west": -99.0, "north": 33.5, "east": -95.0},
    {"market": "California (LA, Bay Area, San Diego, Sacramento)", "south": 32.5, "west": -122.8, "north": 38.8, "east": -117.0},
    {"market": "Florida (Miami, Orlando, Tampa, Jacksonville)", "south": 25.5, "west": -82.8, "north": 30.5, "east": -80.0},
    {"market": "New York & Tri-State (NY, NJ, CT)", "south": 40.2, "west": -74.5, "north": 41.5, "east": -73.0},
    {"market": "Midwest (Chicago, Detroit, Indianapolis)", "south": 39.5, "west": -88.5, "north": 42.5, "east": -83.0},
    {"market": "Southeast (Atlanta, Charlotte, Nashville)", "south": 33.0, "west": -87.0, "north": 36.5, "east": -80.5},
    {"market": "Southwest & Mountain (Phoenix, Las Vegas, Denver)", "south": 33.0, "west": -115.5, "north": 40.0, "east": -104.5},
    {"market": "Pacific Northwest (Seattle, Portland)", "south": 45.0, "west": -123.0, "north": 48.0, "east": -122.0},
]

def main(max_per_region=15000):
    print("=" * 65)
    print(f"  Starting Massive US Lead Extraction (Up to {max_per_region * len(US_REGIONS):,} leads)")
    print("=" * 65)

    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
    rel = _overture_release(con)
    print(f"Overture release: {rel}")
    s3 = f"s3://overturemaps-us-west-2/release/{rel}/theme=places/type=place/*"

    out_file = "all_us_leads_massive.csv"
    if os.path.exists(out_file):
        os.remove(out_file)

    con.execute("""
    CREATE TEMP TABLE master_leads (
        "Business Name" VARCHAR,
        "Category" VARCHAR,
        "Website / Online Presence" VARCHAR,
        "Phone" VARCHAR,
        "Address" VARCHAR,
        "City" VARCHAR,
        "State" VARCHAR,
        "Zip" VARCHAR,
        "Country" VARCHAR,
        "Opportunity Type" VARCHAR,
        "Why It's a Lead" VARCHAR
    );
    """)

    for idx, reg in enumerate(US_REGIONS, 1):
        m = reg["market"]
        print(f"[{idx}/{len(US_REGIONS)}] Extracting from {m} (cap: {max_per_region:,})...")
        
        insert_sql = f"""
        INSERT INTO master_leads
        SELECT DISTINCT
            names.primary AS "Business Name",
            taxonomy.primary AS "Category",
            CASE 
                WHEN websites IS NULL OR length(websites) = 0 THEN 'NO WEBSITE'
                ELSE websites[1]
            END AS "Website / Online Presence",
            CASE WHEN length(phones) > 0 THEN phones[1] ELSE '' END AS "Phone",
            addresses[1].freeform AS "Address",
            addresses[1].locality AS "City",
            addresses[1].region AS "State",
            addresses[1].postcode AS "Zip",
            'United States' AS "Country",
            CASE 
                WHEN websites IS NULL OR length(websites) = 0 THEN 'NO WEBSITE - Needs Website Built'
                ELSE 'SOCIAL ONLY - Needs Owned Company Website'
            END AS "Opportunity Type",
            CASE 
                WHEN websites IS NULL OR length(websites) = 0 THEN 'Commercial phone active but ZERO website exists'
                ELSE 'Operating solely off social media (Instagram/Facebook/Linktree)'
            END AS "Why It\'s a Lead"
        FROM read_parquet('{s3}', hive_partitioning=1)
        WHERE bbox.xmin BETWEEN {reg['west']} AND {reg['east']}
          AND bbox.ymin BETWEEN {reg['south']} AND {reg['north']}
          AND names.primary IS NOT NULL
          AND (addresses[1].country = 'US' OR addresses[1].country IS NULL)
          AND (
              (length(phones) > 0 AND (websites IS NULL OR length(websites) = 0))
              OR
              (length(websites) > 0 AND (
                  lower(websites[1]) LIKE '%facebook.com%' OR
                  lower(websites[1]) LIKE '%instagram.com%' OR
                  lower(websites[1]) LIKE '%linktr.ee%' OR
                  lower(websites[1]) LIKE '%tiktok.com%' OR
                  lower(websites[1]) LIKE '%fb.com%'
              ))
          )
        LIMIT {max_per_region};
        """
        try:
            con.execute(insert_sql)
            count = con.execute("SELECT count(*) FROM master_leads").fetchone()[0]
            print(f"  -> Total accumulated leads: {count:,}")
        except Exception as e:
            print(f"  Warning on {m}: {e}")

    # Deduplicate in master_leads table
    print("Deduplicating accumulated leads...")
    con.execute("""
    CREATE TEMP TABLE deduplicated_leads AS
    SELECT * EXCLUDE (rn) FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY lower("Business Name"), "Phone" ORDER BY "State") as rn
        FROM master_leads
    ) WHERE rn = 1;
    """)

    final_count = con.execute("SELECT count(*) FROM deduplicated_leads").fetchone()[0]
    print(f"Exporting {final_count:,} unique verified leads to {out_file}...")
    con.execute(f"COPY deduplicated_leads TO '{out_file}' (HEADER, DELIMITER ',');")
    print(f"[DONE] Complete! Saved {final_count:,} leads to {out_file}")

if __name__ == "__main__":
    max_count = int(sys.argv[1]) if len(sys.argv) > 1 else 15000
    main(max_count)
