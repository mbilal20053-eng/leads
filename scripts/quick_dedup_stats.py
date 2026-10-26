import duckdb

con = duckdb.connect()

ho_stats = con.execute("""
    SELECT 
        count(*) as total,
        count(case when tier = 'A' then 1 end) as tier_a,
        count(case when tier = 'B' then 1 end) as tier_b,
        count(case when phone != '' then 1 end) as with_phone,
        count(case when website != '' then 1 end) as with_website,
        count(case when email != '' then 1 end) as with_email
    FROM read_parquet('d:/leads/homeowners.parquet')
""").fetchone()

ml_stats = con.execute("""
    SELECT 
        count(*) as total,
        count(case when lower(store_name) in ('apple', 'walmart', 'target') then 1 end) as tier_a,
        0 as tier_b,
        0 as with_phone,
        count(*) as with_website,
        0 as with_email
    FROM read_csv_auto('d:/leads/master-locations.csv')
""").fetchone()

print("Homeowners:", ho_stats)
print("Master Locations:", ml_stats)
