import duckdb
con = duckdb.connect()
res = con.execute("""
    SELECT 
        count(*),
        count(CASE WHEN "Phone numbers" IS NOT NULL AND length(trim(CAST("Phone numbers" AS VARCHAR))) > 0 THEN 1 END) as has_ph,
        count(CASE WHEN "Mobile" IS NOT NULL AND length(trim(CAST("Mobile" AS VARCHAR))) > 0 THEN 1 END) as has_mob,
        count(CASE WHEN ("Phone numbers" IS NOT NULL AND length(trim(CAST("Phone numbers" AS VARCHAR))) > 0) OR ("Mobile" IS NOT NULL AND length(trim(CAST("Mobile" AS VARCHAR))) > 0) THEN 1 END) as has_either,
        count(CASE WHEN "Emails" IS NOT NULL AND length(trim(CAST("Emails" AS VARCHAR))) > 0 THEN 1 END) as has_email,
        count(CASE WHEN "Company Website" IS NOT NULL AND length(trim(CAST("Company Website" AS VARCHAR))) > 0 THEN 1 END) as has_web
    FROM read_csv_auto('d:/leads/free-tier (2).csv', ignore_errors=true)
""").fetchone()
tot, ph, mob, either, em, web = res
print(f"Total: {tot:,}")
print(f"Phone numbers: {ph:,} ({ph/tot*100:.1f}%)")
print(f"Mobile: {mob:,} ({mob/tot*100:.1f}%)")
print(f"Either Mobile OR Phone: {either:,} ({either/tot*100:.1f}%)")
print(f"Emails: {em:,} ({em/tot*100:.1f}%)")
print(f"Company Website: {web:,} ({web/tot*100:.1f}%)")
