"""
Audit 4 conditions on newly discovered Downloads files
"""
import os
import sys
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

con = duckdb.connect()

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

new_datasets = [
    ("Companies Filtered (Downloads)", r"C:\Users\billu\Downloads\companies_filtered_20261008_120127.csv", "name", [], [], []),
    ("Fitness Wellness Texas (Downloads)", r"C:\Users\billu\Downloads\fitness_wellness_texas_20261016_123305_crm.csv", "Business", ["Phone"], [], ["Website"]),
    ("Salon Leads Filtered (Downloads)", r"C:\Users\billu\Downloads\salon_leads_filtered.csv", "location_name", [], [], []),
    ("Leads - Leads 1 (Downloads)", r"C:\Users\billu\Downloads\leads - leads (1).csv", "Business", ["Phone"], ["Email"], []),
    ("Leads - Leads (Downloads)", r"C:\Users\billu\Downloads\leads - leads.csv", "Business", ["Phone"], ["Email"], []),
    ("Leads Export 899c (Downloads)", r"C:\Users\billu\Downloads\leads-export-2026-10-12-899c685d.csv", "Business Name", ["Phone"], ["Email"], []),
    ("Leads Export 20c2 (Downloads)", r"C:\Users\billu\Downloads\leads-export-2026-10-12-20c28f9d.csv", "Business Name", ["Phone"], ["Email"], []),
    ("Leads CSV (Downloads)", r"C:\Users\billu\Downloads\leads.csv", "Business", ["Phone"], ["Email"], []),
]

print("=" * 120)
print("AUDITING NEWLY DISCOVERED DOWNLOADS FILES (4 CONDITIONS)")
print("=" * 120)

for label, p, name_col, p_cols, e_cols, w_cols in new_datasets:
    clean_p = p.replace("\\", "/")
    
    name_clause = f"""(
        "{name_col}" IS NULL 
        OR trim(CAST("{name_col}" AS VARCHAR)) = '' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) = 'unknown business' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) = 'unknown' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) IN ({PLACEHOLDER_SQL})
    )""" if name_col else "1=1"
    
    valid_p = "(" + " OR ".join([f'("{c}" IS NOT NULL AND length(regexp_replace(CAST("{c}" AS VARCHAR), \'[^0-9]\', \'\', \'g\')) >= 7)' for c in p_cols]) + ")" if p_cols else "1=0"
    valid_e = "(" + " OR ".join([f'("{c}" IS NOT NULL AND length(trim(CAST("{c}" AS VARCHAR))) >= 6 AND lower(trim(CAST("{c}" AS VARCHAR))) LIKE \'%@%.__%\')' for c in e_cols]) + ")" if e_cols else "1=0"
    valid_w = "(" + " OR ".join([f'("{c}" IS NOT NULL AND length(trim(CAST("{c}" AS VARCHAR))) >= 4 AND lower(trim(CAST("{c}" AS VARCHAR))) LIKE \'%.__%\')' for c in w_cols]) + ")" if w_cols else "1=0"
    
    missing_p = f"NOT {valid_p}"
    missing_e = f"NOT {valid_e}"
    missing_w = f"NOT {valid_w}"
    
    all_4 = f"({name_clause} AND {missing_p} AND {missing_e} AND {missing_w})"
    
    q = f"""
        SELECT 
            count(*) as total,
            count(CASE WHEN {name_clause} THEN 1 END) as m_name,
            count(CASE WHEN {missing_p} THEN 1 END) as m_phone,
            count(CASE WHEN {missing_e} THEN 1 END) as m_email,
            count(CASE WHEN {missing_w} THEN 1 END) as m_web,
            count(CASE WHEN {all_4} THEN 1 END) as all_4_tot,
            count(DISTINCT CASE WHEN {all_4} THEN coalesce(CAST("{name_col}" AS VARCHAR), '') END) as all_4_uniq
        FROM read_csv_auto('{clean_p}', ignore_errors=true)
    """
    row = con.execute(q).fetchone()
    print(f"{label:<36} | Total: {row[0]:>8,} | M-Name: {row[1]:>6,} | M-Phone: {row[2]:>6,} | M-Email: {row[3]:>6,} | M-Web: {row[4]:>6,} | ALL 4: {row[5]:>6,} | Uniq: {row[6]:>6,}")
