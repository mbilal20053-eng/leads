import time
import duckdb

con = duckdb.connect()

# Initialize views without v_free_company_db in the union
subviews = [
    "d:/leads/b2b_executives.parquet",
    "d:/leads/homeowners.parquet",
    "d:/leads/gleif_goldencopy.parquet",
    "d:/leads/open_company_database.parquet",
    "d:/leads/tech_stack_companies.parquet",
    "d:/leads/sec_company_facts.parquet",
    "d:/leads/cc_web_index.parquet"
]

con.execute(f"""
CREATE OR REPLACE VIEW v_fast_unified AS
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/b2b_executives.parquet')
UNION ALL
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/homeowners.parquet')
UNION ALL
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/gleif_goldencopy.parquet')
UNION ALL
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/open_company_database.parquet')
UNION ALL
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/tech_stack_companies.parquet')
""")

print("Testing query speeds at various offsets on v_fast_unified (16M rows):")
for off in [0, 100, 1000, 50000, 500000, 5000000, 15000000]:
    t0 = time.time()
    res = con.execute(f"SELECT id, name FROM v_fast_unified LIMIT 50 OFFSET {off}").fetchall()
    print(f"  Offset {off:>10,}: {len(res)} rows in {time.time()-t0:.3f}s")
