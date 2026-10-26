"""
AUDIT: NO USEFUL BUSINESS INFORMATION (ALL 4 CONDITIONS TRUE SIMULTANEOUSLY)
STRICT AUDIT ONLY. READ-ONLY. NO MODIFICATIONS.

Conditions for matching:
1. Business/company name is missing, blank, or placeholder
2. Phone number is missing or invalid
3. Email address is missing or invalid
4. Website URL/domain is missing or invalid
Records where ALL FOUR conditions are true simultaneously contain NO useful business information.
"""

import os
import sys
import time
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

LEADS_DIR = r"d:\leads"

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

def build_valid_phone_sql(cols):
    if not cols:
        return "1=0"
    clauses = []
    for c in cols:
        clauses.append(f"""(
            "{c}" IS NOT NULL 
            AND length(regexp_replace(CAST("{c}" AS VARCHAR), '[^0-9]', '', 'g')) >= 7 
            AND regexp_replace(CAST("{c}" AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000', '1111111', '1234567')
        )""")
    return "(" + " OR ".join(clauses) + ")"

def build_valid_email_sql(cols):
    if not cols:
        return "1=0"
    clauses = []
    for c in cols:
        clauses.append(f"""(
            "{c}" IS NOT NULL 
            AND length(trim(CAST("{c}" AS VARCHAR))) >= 6 
            AND lower(trim(CAST("{c}" AS VARCHAR))) LIKE '%@%.__%'
            AND lower(trim(CAST("{c}" AS VARCHAR))) NOT IN ('test@test.com', 'none@none.com', 'null@null.com', 'no@email.com', 'admin@admin.com')
        )""")
    return "(" + " OR ".join(clauses) + ")"

def build_valid_web_sql(cols):
    if not cols:
        return "1=0"
    clauses = []
    for c in cols:
        clauses.append(f"""(
            "{c}" IS NOT NULL 
            AND length(trim(CAST("{c}" AS VARCHAR))) >= 4 
            AND lower(trim(CAST("{c}" AS VARCHAR))) LIKE '%.__%'
            AND lower(trim(CAST("{c}" AS VARCHAR))) NOT IN ('null', 'none', 'nan', 'n/a', 'na', 'http://', 'https://', 'www.', 'http', 'https')
        )""")
    return "(" + " OR ".join(clauses) + ")"

def audit_file_4_conditions(con, label, file_path, read_func, name_col, phone_cols, email_cols, web_cols, dedup_cols=None):
    clean_path = file_path.replace("\\", "/")
    if not os.path.exists(file_path):
        return None
    
    t0 = time.time()
    read_expr = f"{read_func}('{clean_path}')" if "csv" not in read_func else f"{read_func}('{clean_path}', ignore_errors=true)"
    
    name_clause = f"""(
        "{name_col}" IS NULL 
        OR trim(CAST("{name_col}" AS VARCHAR)) = '' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) = 'unknown business' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) = 'unknown' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) IN ({PLACEHOLDER_SQL})
    )""" if name_col else "1=1"
    
    valid_p = build_valid_phone_sql(phone_cols)
    valid_e = build_valid_email_sql(email_cols)
    valid_w = build_valid_web_sql(web_cols)
    
    missing_p = f"NOT {valid_p}"
    missing_e = f"NOT {valid_e}"
    missing_w = f"NOT {valid_w}"
    
    all_4_missing = f"({name_clause} AND {missing_p} AND {missing_e} AND {missing_w})"
    
    # Dedup expression
    if dedup_cols:
        dedup_expr = " || '|' || ".join([f'coalesce(CAST("{c}" AS VARCHAR), \'\')' for c in dedup_cols])
    else:
        dedup_expr = f'coalesce(CAST("{name_col}" AS VARCHAR), \'\')' if name_col else "'1'"
    
    q = f"""
        SELECT 
            count(*) as total_rows,
            count(CASE WHEN {name_clause} THEN 1 END) as missing_name,
            count(CASE WHEN {missing_p} THEN 1 END) as missing_phone,
            count(CASE WHEN {missing_e} THEN 1 END) as missing_email,
            count(CASE WHEN {missing_w} THEN 1 END) as missing_web,
            count(CASE WHEN {all_4_missing} THEN 1 END) as all_4_missing_total,
            count(DISTINCT CASE WHEN {all_4_missing} THEN {dedup_expr} END) as all_4_missing_unique
        FROM {read_expr}
    """
    
    row = con.execute(q).fetchone()
    elapsed = time.time() - t0
    
    total_rows = row[0]
    m_name = row[1]
    m_phone = row[2]
    m_email = row[3]
    m_web = row[4]
    all_4_tot = row[5]
    all_4_uniq = row[6]
    dups_in_matching = all_4_tot - all_4_uniq
    pct_of_file = (all_4_tot / total_rows * 100) if total_rows > 0 else 0.0
    
    return {
        "label": label,
        "filename": os.path.basename(file_path),
        "total_rows": total_rows,
        "missing_name": m_name,
        "missing_phone": m_phone,
        "missing_email": m_email,
        "missing_web": m_web,
        "all_4_missing_total": all_4_tot,
        "all_4_missing_unique": all_4_uniq,
        "dups_in_matching": dups_in_matching,
        "pct_of_file": pct_of_file,
        "name_col": name_col or "(None)",
        "phone_cols": phone_cols or ["(None)"],
        "email_cols": email_cols or ["(None)"],
        "web_cols": web_cols or ["(None)"],
        "elapsed": elapsed
    }

def run_audit():
    print("=" * 140)
    print("AUDIT: RECORDS WITH NO USEFUL BUSINESS INFORMATION (ALL 4 CONDITIONS TRUE SIMULTANEOUSLY)")
    print("MODE: STRICT AUDIT ONLY (READ-ONLY, ZERO FILE OR DATABASE MUTATIONS)")
    print("=" * 140)
    
    con = duckdb.connect()
    con.execute("PRAGMA threads=8;")
    con.execute("SET preserve_insertion_order=false;")
    
    datasets = [
        # 1. Targeted Vertical CSVs (7 files)
        ("Restaurants CSV", os.path.join(LEADS_DIR, "050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        ("Realtors CSV", os.path.join(LEADS_DIR, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        ("Coaches CSV", os.path.join(LEADS_DIR, "166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        ("Musicians CSV", os.path.join(LEADS_DIR, "74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        ("Designers CSV", os.path.join(LEADS_DIR, "94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        ("Founders CSV", os.path.join(LEADS_DIR, "b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        ("Photographers CSV", os.path.join(LEADS_DIR, "da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"], ["name", "email", "phone"]),
        
        # 2. Commercial Real Estate B2B
        ("Real Estate B2B (free-tier.csv)", os.path.join(LEADS_DIR, "free-tier.csv"), "read_csv_auto", "COMPANY", ["PHONE_NUMBER"], ["Email"], ["Email-Domain"], ["COMPANY", "ADDRESS", "PHONE_NUMBER", "Email"]),
        
        # 3. Raw Homeowners CSV (free-tier (1).csv)
        ("Homeowners CSV (free-tier (1).csv)", os.path.join(LEADS_DIR, "free-tier (1).csv"), "read_csv_auto", "Residence_Type", ["Area_Code_and_Phone"], [], [], ["Residence_Type", "County", "City", "Area_Code_and_Phone"]),
        
        # 4. Master Locations
        ("Master Locations CSV", os.path.join(LEADS_DIR, "master-locations.csv"), "read_csv_auto", "store_name", [], [], [], ["store_name", "city", "coordinates"]),
        
        # 5. Open Company Database Sample
        ("Open Company Sample CSV", os.path.join(LEADS_DIR, "open_company_database_sample.csv"), "read_csv_auto", "company_name", [], [], ["company_domain"], ["company_name", "company_domain"]),
    ]
    
    # 6. Add 18 B2B Shards (free-tier (2).csv to (19).csv)
    for i in range(2, 20):
        b2b_path = os.path.join(LEADS_DIR, f"free-tier ({i}).csv")
        datasets.append((
            f"B2B Shard {i} (free-tier ({i}).csv)", 
            b2b_path, 
            "read_csv_auto", 
            "Company Name", 
            ["Phone numbers", "Mobile"], 
            ["Emails"], 
            ["Company Website"],
            ["Full name", "Job title", "Location", "Emails", "Phone numbers", "Company Name"]
        ))
        
    # 7. Data Legion
    legion_path = os.path.join(LEADS_DIR, "data-legion-company-free-1.5.0_2026-10-15.csv.gz")
    if os.path.exists(legion_path):
        datasets.append((
            "Data Legion Company (GZ)",
            legion_path,
            "read_csv_auto",
            "name",
            [],
            [],
            ["domain"],
            ["name", "domain"]
        ))
        
    # 8. Parquets
    parquets = [
        ("B2B Executives Parquet", os.path.join(LEADS_DIR, "b2b_executives.parquet"), "read_parquet", "name", ["phone"], ["email"], ["website"], ["id", "name", "contact_name", "job_title", "address"]),
        ("Homeowners Parquet", os.path.join(LEADS_DIR, "homeowners.parquet"), "read_parquet", "name", ["phone"], ["email"], ["website"], ["id", "name", "address", "phone"]),
        ("Open Company Parquet", os.path.join(LEADS_DIR, "open_company_database.parquet"), "read_parquet", "name", [], [], ["website"], ["id", "name", "website"]),
        ("Tech Stack Parquet", os.path.join(LEADS_DIR, "tech_stack_companies.parquet"), "read_parquet", "name", [], [], ["website"], ["id", "name", "website"]),
        ("GLEIF Parquet", os.path.join(LEADS_DIR, "gleif_goldencopy.parquet"), "read_parquet", "name", [], [], [], ["lei", "name"]),
        ("SEC Company Facts Parquet", os.path.join(LEADS_DIR, "sec_company_facts.parquet"), "read_parquet", "name", [], [], [], ["cik", "name"]),
        ("CC Web Index Parquet", os.path.join(LEADS_DIR, "cc_web_index.parquet"), "read_parquet", "name", [], [], ["website"], ["id", "name", "website"]),
    ]
    
    results = []
    print(f"\n--- SCANNING {len(datasets)} RAW DATASETS ON DISK ---")
    for label, fpath, fn, name_col, p_cols, e_cols, w_cols, dedup_cols in datasets:
        res = audit_file_4_conditions(con, label, fpath, fn, name_col, p_cols, e_cols, w_cols, dedup_cols)
        if res:
            results.append(res)
            print(f"{res['label']:<34} | Total: {res['total_rows']:>10,} | M-Name: {res['missing_name']:>8,} | M-Phone: {res['missing_phone']:>8,} | M-Email: {res['missing_email']:>8,} | M-Web: {res['missing_web']:>8,} | ALL 4 MISSING: {res['all_4_missing_total']:>8,} ({res['pct_of_file']:>5.2f}%) | Unique: {res['all_4_missing_unique']:>8,}")
            sys.stdout.flush()

    pq_results = []
    print(f"\n--- SCANNING {len(parquets)} CONSOLIDATED PARQUET DATASETS ---")
    for label, fpath, fn, name_col, p_cols, e_cols, w_cols, dedup_cols in parquets:
        res = audit_file_4_conditions(con, label, fpath, fn, name_col, p_cols, e_cols, w_cols, dedup_cols)
        if res:
            pq_results.append(res)
            print(f"{res['label']:<34} | Total: {res['total_rows']:>10,} | M-Name: {res['missing_name']:>8,} | M-Phone: {res['missing_phone']:>8,} | M-Email: {res['missing_email']:>8,} | M-Web: {res['missing_web']:>8,} | ALL 4 MISSING: {res['all_4_missing_total']:>8,} ({res['pct_of_file']:>5.2f}%) | Unique: {res['all_4_missing_unique']:>8,}")
            sys.stdout.flush()

    return results, pq_results

if __name__ == "__main__":
    results, pq_results = run_audit()
