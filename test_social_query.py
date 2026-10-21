import duckdb
from leadgen.sources import _overture_release

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
release = _overture_release(con)
print("Release:", release)

s3 = f"s3://overturemaps-us-west-2/release/{release}/theme=places/type=place/*"

# Query Austin / Central Texas region
query = f"""
SELECT names.primary AS name,
       taxonomy.primary AS category,
       websites[1] AS website,
       CASE WHEN length(phones)>0 THEN phones[1] END AS phone,
       addresses[1].freeform AS address,
       addresses[1].locality AS city,
       addresses[1].region AS state,
       addresses[1].postcode AS zip,
       addresses[1].country AS country
FROM read_parquet('{s3}', hive_partitioning=1)
WHERE bbox.xmin BETWEEN -98.0 AND -97.5
  AND bbox.ymin BETWEEN 30.1 AND 30.6
  AND names.primary IS NOT NULL
  AND length(websites) > 0
  AND (
      lower(websites[1]) LIKE '%facebook.com%' OR
      lower(websites[1]) LIKE '%instagram.com%' OR
      lower(websites[1]) LIKE '%linktr.ee%' OR
      lower(websites[1]) LIKE '%tiktok.com%' OR
      lower(websites[1]) LIKE '%fb.com%'
  )
LIMIT 10;
"""

rows = con.execute(query).fetchall()
print(f"Found {len(rows)} leads:")
for r in rows:
    print(r)
