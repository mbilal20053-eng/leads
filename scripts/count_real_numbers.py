import os
import glob
import duckdb

data_dir = r"d:\leads"
all_csvs = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
print(f"Direct CSV files in {data_dir}: {len(all_csvs)}")

con = duckdb.connect()

grand_total = 0
grand_phone = 0
grand_web = 0
grand_email = 0

file_stats = []

for f in all_csvs:
    fname = os.path.basename(f)
    clean_f = f.replace("\\", "/")
    try:
        desc = con.execute(f"SELECT * FROM read_csv_auto('{clean_f}', ignore_errors=true) LIMIT 1").description
        cols = [d[0] for d in desc]
        
        # Phone cols
        ph_cols = [c for c in cols if any(k in c.lower() for k in ["phone", "tel", "mobile"])]
        # Web cols
        web_cols = [c for c in cols if any(k in c.lower() for k in ["website", "domain", "url"]) or c.lower() == "web"]
        # Email cols
        em_cols = [c for c in cols if any(k in c.lower() for k in ["email", "mail"])]
        
        ph_cond = " OR ".join([f'("{c}" IS NOT NULL AND length(trim(CAST("{c}" AS VARCHAR))) > 5 AND lower(trim(CAST("{c}" AS VARCHAR))) NOT IN (\'null\', \'none\', \'nan\', \'n/a\', \'\', \'0\'))' for c in ph_cols]) if ph_cols else "1=0"
        web_cond = " OR ".join([f'("{c}" IS NOT NULL AND length(trim(CAST("{c}" AS VARCHAR))) > 3 AND lower(trim(CAST("{c}" AS VARCHAR))) NOT IN (\'null\', \'none\', \'nan\', \'n/a\', \'\') AND CAST("{c}" AS VARCHAR) LIKE \'%.%\')' for c in web_cols]) if web_cols else "1=0"
        em_cond = " OR ".join([f'("{c}" IS NOT NULL AND length(trim(CAST("{c}" AS VARCHAR))) > 5 AND lower(trim(CAST("{c}" AS VARCHAR))) NOT IN (\'null\', \'none\', \'nan\', \'n/a\', \'\') AND CAST("{c}" AS VARCHAR) LIKE \'%@%\')' for c in em_cols]) if em_cols else "1=0"
        
        q = f"""
            SELECT 
                count(*),
                count(CASE WHEN {ph_cond} THEN 1 END),
                count(CASE WHEN {web_cond} THEN 1 END),
                count(CASE WHEN {em_cond} THEN 1 END)
            FROM read_csv_auto('{clean_f}', ignore_errors=true)
        """
        row = con.execute(q).fetchone()
        tot, ph, web, em = row[0], row[1], row[2], row[3]
        
        grand_total += tot
        grand_phone += ph
        grand_web += web
        grand_email += em
        
        ph_p = (ph / tot * 100) if tot else 0
        web_p = (web / tot * 100) if tot else 0
        em_p = (em / tot * 100) if tot else 0
        
        file_stats.append({
            "file": fname,
            "total": tot,
            "phone": ph, "phone_pct": ph_p,
            "web": web, "web_pct": web_p,
            "email": em, "email_pct": em_p,
            "ph_cols": ph_cols,
            "web_cols": web_cols,
            "em_cols": em_cols
        })
        print(f"{fname:55} | Rows: {tot:7d} | Ph: {ph:7d} ({ph_p:5.1f}%) | Web: {web:7d} ({web_p:5.1f}%) | Email: {em:7d} ({em_p:5.1f}%)")
    except Exception as e:
        print(f"{fname}: ERROR: {e}")

print("=" * 80)
ph_gp = (grand_phone / grand_total * 100) if grand_total else 0
web_gp = (grand_web / grand_total * 100) if grand_total else 0
em_gp = (grand_email / grand_total * 100) if grand_total else 0
print(f"GRAND TOTAL ACROSS ALL {len(all_csvs)} FILES:")
print(f"Total Rows:     {grand_total:,}")
print(f"Phone Numbers:  {grand_phone:,} ({ph_gp:.2f}%)")
print(f"Websites:       {grand_web:,} ({web_gp:.2f}%)")
print(f"Emails:         {grand_email:,} ({em_gp:.2f}%)")
