"""
READ-ONLY SCAN & AUDIT: FILTERING RECORDS WITH MISSING/PLACEHOLDER BUSINESS NAMES
BASED ON VALID CONTACT METHOD PRESERVATION RULES

Removal Rules:
Remove a record ONLY IF:
1. Business name is blank, missing, or a placeholder (Unknown Business, Unknown, TBD, N/A, No Name, Unnamed, Null, etc.)
AND
2. Has NONE of:
   - Valid phone number
   - Valid email address
   - Valid website URL or domain

PRESERVE if record has even ONE valid phone, email, or website.
STRICT AUDIT ONLY: ZERO MODIFICATIONS.
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

def build_phone_sql(cols):
    if not cols:
        return "1=0"
    clauses = []
    for c in cols:
        clauses.append(f"""(
            "{c}" IS NOT NULL 
            AND length(regexp_replace(CAST("{c}" AS VARCHAR), '[^0-9]', '', 'g')) >= 7 
            AND regexp_replace(CAST("{c}" AS VARCHAR), '[^0-9]', '', 'g') NOT IN ('0000000', '0000000000', '1111111', '1234567')
        )""")
    return " OR ".join(clauses)

def build_email_sql(cols):
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
    return " OR ".join(clauses)

def build_web_sql(cols):
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
    return " OR ".join(clauses)

def analyze_dataset(con, label, file_path, read_func, name_col, phone_cols, email_cols, web_cols):
    clean_path = file_path.replace("\\", "/")
    if not os.path.exists(file_path):
        return None
    
    t0 = time.time()
    read_expr = f"{read_func}('{clean_path}')" if "csv" not in read_func else f"{read_func}('{clean_path}', ignore_errors=true)"
    
    name_cond = f"""(
        "{name_col}" IS NULL 
        OR trim(CAST("{name_col}" AS VARCHAR)) = '' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) = 'unknown business' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) = 'unknown' 
        OR lower(trim(CAST("{name_col}" AS VARCHAR))) IN ({PLACEHOLDER_SQL})
    )"""
    
    p_sql = build_phone_sql(phone_cols)
    e_sql = build_email_sql(email_cols)
    w_sql = build_web_sql(web_cols)
    
    q = f"""
        SELECT 
            count(*) as total_rows,
            count(CASE WHEN {name_cond} THEN 1 END) as total_affected,
            count(CASE WHEN {name_cond} AND ({p_sql}) AND NOT ({e_sql}) AND NOT ({w_sql}) THEN 1 END) as phone_only,
            count(CASE WHEN {name_cond} AND ({e_sql}) AND NOT ({p_sql}) AND NOT ({w_sql}) THEN 1 END) as email_only,
            count(CASE WHEN {name_cond} AND ({w_sql}) AND NOT ({p_sql}) AND NOT ({e_sql}) THEN 1 END) as web_only,
            count(CASE WHEN {name_cond} AND (
                (({p_sql}) AND ({e_sql})) OR (({p_sql}) AND ({w_sql})) OR (({e_sql}) AND ({w_sql}))
            ) THEN 1 END) as multiple_contacts,
            count(CASE WHEN {name_cond} AND (({p_sql}) OR ({e_sql}) OR ({w_sql})) THEN 1 END) as has_at_least_one,
            count(CASE WHEN {name_cond} AND NOT ({p_sql}) AND NOT ({e_sql}) AND NOT ({w_sql}) THEN 1 END) as qualifies_for_removal
        FROM {read_expr}
    """
    
    row = con.execute(q).fetchone()
    elapsed = time.time() - t0
    
    total_rows = row[0]
    total_aff = row[1]
    p_only = row[2]
    e_only = row[3]
    w_only = row[4]
    multi = row[5]
    preserved = row[6]
    removal = row[7]
    
    pct_preserved = (preserved / total_aff * 100) if total_aff > 0 else 0.0
    pct_removal = (removal / total_aff * 100) if total_aff > 0 else 0.0
    pct_removal_dataset = (removal / total_rows * 100) if total_rows > 0 else 0.0
    
    return {
        "label": label,
        "filename": os.path.basename(file_path),
        "total_rows": total_rows,
        "total_affected": total_aff,
        "phone_only": p_only,
        "email_only": e_only,
        "web_only": w_only,
        "multiple_contacts": multi,
        "preserved_count": preserved,
        "pct_preserved": pct_preserved,
        "removal_count": removal,
        "pct_removal_of_affected": pct_removal,
        "pct_removal_of_dataset": pct_removal_dataset,
        "elapsed": elapsed
    }

def run_all():
    print("=" * 120)
    print("STARTING AUDIT: CONTACT FILTERING SIMULATION (AUDIT ONLY)")
    print("=" * 120)
    
    con = duckdb.connect()
    con.execute("PRAGMA threads=8;")
    con.execute("SET preserve_insertion_order=false;")
    
    datasets = [
        # Targeted Vertical CSVs
        ("Restaurants CSV", os.path.join(LEADS_DIR, "050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        ("Realtors CSV", os.path.join(LEADS_DIR, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        ("Coaches CSV", os.path.join(LEADS_DIR, "166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        ("Musicians CSV", os.path.join(LEADS_DIR, "74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        ("Designers CSV", os.path.join(LEADS_DIR, "94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        ("Founders CSV", os.path.join(LEADS_DIR, "b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        ("Photographers CSV", os.path.join(LEADS_DIR, "da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv"), "read_csv_auto", "name", ["phone"], ["email"], ["website"]),
        
        # Real Estate B2B
        ("Real Estate B2B (free-tier.csv)", os.path.join(LEADS_DIR, "free-tier.csv"), "read_csv_auto", "COMPANY", ["PHONE_NUMBER"], ["Email"], ["Email-Domain"]),
        
        # Open Company Sample
        ("Open Company Sample CSV", os.path.join(LEADS_DIR, "open_company_database_sample.csv"), "read_csv_auto", "company_name", [], [], ["company_domain"]),
        
        # Parquet files
        ("B2B Executives Parquet", os.path.join(LEADS_DIR, "b2b_executives.parquet"), "read_parquet", "name", ["phone"], ["email"], ["website"]),
        ("Tech Stack Parquet", os.path.join(LEADS_DIR, "tech_stack_companies.parquet"), "read_parquet", "name", [], [], ["website"]),
        ("GLEIF Parquet", os.path.join(LEADS_DIR, "gleif_goldencopy.parquet"), "read_parquet", "name", [], [], []),
        ("Open Company Parquet", os.path.join(LEADS_DIR, "open_company_database.parquet"), "read_parquet", "name", [], [], ["website"]),
    ]
    
    # Add the 18 raw B2B shards
    for i in range(2, 20):
        b2b_path = os.path.join(LEADS_DIR, f"free-tier ({i}).csv")
        datasets.append((
            f"B2B Shard {i} (free-tier ({i}).csv)", 
            b2b_path, 
            "read_csv_auto", 
            "Company Name", 
            ["Phone numbers", "Mobile"], 
            ["Emails"], 
            ["Company Website"]
        ))
        
    # Data Legion
    legion_path = os.path.join(LEADS_DIR, "data-legion-company-free-1.5.0_2026-10-15.csv.gz")
    if os.path.exists(legion_path):
        datasets.append((
            "Data Legion Company (GZ)", 
            legion_path, 
            "read_csv_auto", 
            "name", 
            [], 
            [], 
            ["domain"]
        ))
    
    results = []
    for label, fpath, fn, name_col, p_cols, e_cols, w_cols in datasets:
        res = analyze_dataset(con, label, fpath, fn, name_col, p_cols, e_cols, w_cols)
        if res:
            results.append(res)
            print(f"{res['label']:<35} | Total: {res['total_rows']:>10,} | Affected: {res['total_affected']:>9,} | Preserved: {res['preserved_count']:>8,} ({res['pct_preserved']:>5.1f}%) | Removal: {res['removal_count']:>8,} ({res['pct_removal_of_affected']:>5.1f}%)")
            sys.stdout.flush()

    return results

if __name__ == "__main__":
    results = run_all()
