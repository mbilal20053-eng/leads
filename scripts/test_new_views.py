import duckdb
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()

data_dir = r"d:\leads"

f_legion = os.path.join(data_dir, "data-legion-company-free-1.5.0_2026-10-15.csv.gz").replace("\\", "/")
f_open_comp = os.path.join(data_dir, "open_company_database_sample.csv").replace("\\", "/")
f_master_loc = os.path.join(data_dir, "master-locations.csv").replace("\\", "/")
f_apple_loc = os.path.join(data_dir, "apple-locations.csv").replace("\\", "/")

# 1. Test Data Legion View
print("Testing v_data_legion...")
con.execute(f"""
CREATE OR REPLACE VIEW v_data_legion AS
SELECT 
    'legion_' || legion_id as id,
    CAST(coalesce(name, 'Corporate Enterprise') AS VARCHAR) as name,
    'Executive Leadership' as contact_name,
    CAST(coalesce(type, 'Private') || ' (' || coalesce(size, '1-50') || ' employees)' AS VARCHAR) as job_title,
    CAST(coalesce(industry, 'Corporate Services') AS VARCHAR) as category,
    '' as address,
    '' as city,
    '' as state,
    '' as zip,
    'Global / Multi-National' as country,
    '' as phone,
    CASE WHEN domain IS NOT NULL AND length(trim(domain)) > 3 AND lower(trim(domain)) NOT IN ('', 'null', 'none', 'nan') THEN trim(domain) ELSE '' END as website,
    '' as email,
    CAST(coalesce(linkedin_url, '') AS VARCHAR) as socials,
    CASE WHEN domain IS NOT NULL AND length(trim(domain)) > 3 THEN 'A' ELSE 'B' END as tier,
    90 as score,
    'ENTERPRISE B2B PIPELINE' as opportunity,
    'Commercial partnership and enterprise services for ' || coalesce(name, 'organization') || ' in ' || coalesce(industry, 'corporate') || '.' as pitch,
    'Verified global company with LinkedIn presence and corporate domain.' as why,
    '🏢 Data Legion' as source_badge,
    'data_legion_companies' as source_id,
    '#6366f1' as source_color
FROM read_csv_auto('{f_legion}', ignore_errors=true, sample_size=1000)
""")
rows = con.execute("SELECT id, name, category, website, socials, source_badge FROM v_data_legion LIMIT 3").fetchall()
for r in rows:
    print("  ", r)

# 2. Test Open Company Database View
print("\nTesting v_open_company_db...")
con.execute(f"""
CREATE OR REPLACE VIEW v_open_company_db AS
SELECT 
    'ocd_' || row_number() over() as id,
    CAST(coalesce(company_name, 'Commercial Entity') AS VARCHAR) as name,
    'Corporate Executive' as contact_name,
    CAST(coalesce(status, 'Operating') || ' | ' || coalesce(business_model, 'B2B') || ' (' || coalesce(employees_range, '1-50') || ')' AS VARCHAR) as job_title,
    CAST(coalesce(industry, sector, 'Business & Commercial') AS VARCHAR) as category,
    '' as address,
    CAST(coalesce(city, '') AS VARCHAR) as city,
    CAST(coalesce(region, '') AS VARCHAR) as state,
    '' as zip,
    CAST(coalesce(country, 'Global') AS VARCHAR) as country,
    '' as phone,
    CASE WHEN company_domain IS NOT NULL AND length(trim(company_domain)) > 3 AND lower(trim(company_domain)) NOT IN ('', 'null', 'none', 'nan') THEN trim(company_domain) ELSE '' END as website,
    '' as email,
    CAST(coalesce(fliar_profile_url, '') AS VARCHAR) as socials,
    CASE WHEN company_domain IS NOT NULL AND length(trim(company_domain)) > 3 THEN 'A' ELSE 'B' END as tier,
    91 as score,
    'CORPORATE INTELLIGENCE AUDIT' as opportunity,
    'B2B expansion and growth optimization for ' || coalesce(company_name, 'company') || ' in ' || coalesce(industry, sector, 'commercial') || '.' as pitch,
    'Deep corporate profile from open company database with founding year and business model.' as why,
    '🌐 Open Company DB' as source_badge,
    'open_company_db' as source_id,
    '#06b6d4' as source_color
FROM read_csv_auto('{f_open_comp}', ignore_errors=true)
""")
rows = con.execute("SELECT id, name, category, website, city, country, source_badge FROM v_open_company_db LIMIT 3").fetchall()
for r in rows:
    print("  ", r)

# 3. Test Master Locations View
print("\nTesting v_master_locations...")
con.execute(f"""
CREATE OR REPLACE VIEW v_master_locations AS
SELECT 
    'loc_' || row_number() over() as id,
    CAST(upper(substr(store_name, 1, 1)) || substr(store_name, 2) || ' (' || coalesce(city, country, 'Location') || ')' AS VARCHAR) as name,
    'Store Manager / General Manager' as contact_name,
    CAST('Store ID: ' || coalesce(id, '') || ' | ' || coalesce(coordinates, '') AS VARCHAR) as job_title,
    CAST(CASE 
        WHEN lower(store_name) IN ('starbucks', 'subway', 'kfc', 'mcdonalds', 'wendys') THEN 'Restaurants & Dining Chains'
        WHEN lower(store_name) IN ('apple', 'walmart', 'target', 'costco', 'ikea', 'hm', 'zara', 'uniqlo', 'primark') THEN 'Retail & Commercial Chains'
        WHEN lower(store_name) IN ('home_depot', 'lowes') THEN 'Hardware & Home Improvement Chains'
        WHEN lower(store_name) IN ('wells_fargo') THEN 'Banking & Financial Branch'
        WHEN lower(store_name) IN ('crossfit') THEN 'Fitness & Health Centers'
        ELSE 'Commercial Retail Chain'
    END AS VARCHAR) as category,
    '' as address,
    CAST(coalesce(city, '') AS VARCHAR) as city,
    CAST(coalesce(region, '') AS VARCHAR) as state,
    CAST(coalesce(zip, '') AS VARCHAR) as zip,
    CAST(coalesce(country, country_code, 'Global') AS VARCHAR) as country,
    '' as phone,
    CAST(CASE 
        WHEN lower(store_name) = 'apple' THEN 'apple.com'
        WHEN lower(store_name) = 'starbucks' THEN 'starbucks.com'
        WHEN lower(store_name) = 'mcdonalds' THEN 'mcdonalds.com'
        WHEN lower(store_name) = 'subway' THEN 'subway.com'
        WHEN lower(store_name) = 'kfc' THEN 'kfc.com'
        WHEN lower(store_name) = 'walmart' THEN 'walmart.com'
        WHEN lower(store_name) = 'target' THEN 'target.com'
        WHEN lower(store_name) = 'home_depot' THEN 'homedepot.com'
        WHEN lower(store_name) = 'lowes' THEN 'lowes.com'
        WHEN lower(store_name) = 'wells_fargo' THEN 'wellsfargo.com'
        WHEN lower(store_name) = 'costco' THEN 'costco.com'
        WHEN lower(store_name) = 'ikea' THEN 'ikea.com'
        WHEN lower(store_name) = 'crossfit' THEN 'crossfit.com'
        ELSE store_name || '.com'
    END AS VARCHAR) as website,
    '' as email,
    '' as socials,
    'A' as tier,
    88 as score,
    'COMMERCIAL SITE AUDIT' as opportunity,
    'Commercial facilities, local marketing and supply services for ' || store_name || ' in ' || coalesce(city, country, 'region') || '.' as pitch,
    'Verified national/global chain commercial retail location.' as why,
    '🏬 Retail Locations' as source_badge,
    'master_locations' as source_id,
    '#f59e0b' as source_color
FROM read_csv_auto('{f_master_loc}', ignore_errors=true)
""")
rows = con.execute("SELECT id, name, category, website, city, country, source_badge FROM v_master_locations LIMIT 3").fetchall()
for r in rows:
    print("  ", r)

print("\nALL VIEWS VERIFIED SUCCESSFULLY!")
