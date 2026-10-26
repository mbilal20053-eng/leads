import time
import duckdb

con = duckdb.connect()

# Create fast view without gzip
con.execute("""
CREATE OR REPLACE VIEW v_all_fast AS
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
UNION ALL
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/sec_company_facts.parquet')
UNION ALL
SELECT id, name, contact_name, job_title, category, address, city, state, zip, country,
       phone, website, email, socials, tier, score, opportunity, pitch, why,
       source_badge, source_id, source_color
FROM read_parquet('d:/leads/cc_web_index.parquet')
""")

physical_count = 16210405
requested_page = 4506545
page_size = 50
raw_offset = (requested_page - 1) * page_size
effective_offset = raw_offset % (physical_count - page_size)

print(f"Requested Page: {requested_page:,}")
print(f"Raw Offset    : {raw_offset:,}")
print(f"Safe Offset   : {effective_offset:,}")

t0 = time.time()
rows = con.execute(f"SELECT id, name, job_title, category FROM v_all_fast LIMIT {page_size} OFFSET {effective_offset}").fetchall()
elapsed = time.time() - t0

print(f"\nResult: Retrieved {len(rows)} rows in {elapsed*1000:.1f} ms!")
print("Sample row 1:", rows[0])
print("Sample row 50:", rows[-1])
