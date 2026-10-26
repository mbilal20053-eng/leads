"""
AUDIT SCRIPT: Audit Unknown Business and Missing Business Name Placeholders
STRICT SAFETY NOTICE: AUDIT ONLY. READ-ONLY. NO MODIFICATIONS.

Scans all lead datasets across d:\\leads:
1. Exact matches of "Unknown Business" case-insensitively (including extra whitespace)
2. Exact matches of "Unknown"
3. Other placeholders: "N/A", "NA", "None", "Null", "-", ".", "Not Available", etc.
4. Blank or missing business name fields (NULL or empty string)
5. Total affected records and % of dataset
6. Duplicate records among affected leads
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

def audit_dataset(con, file_label, file_path, read_func, name_col, extra_cols=None):
    clean_path = file_path.replace("\\", "/")
    if not os.path.exists(file_path):
        return None
    
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    t0 = time.time()
    
    # Check if table/file is readable
    try:
        col_expr = f'"{name_col}"'
        read_expr = f"{read_func}('{clean_path}')" if "csv" not in read_func else f"{read_func}('{clean_path}', ignore_errors=true)"
        
        # Build query
        q = f"""
            SELECT 
                count(*) as total_rows,
                count(CASE WHEN lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown business' THEN 1 END) as exact_unknown_business,
                count(CASE WHEN lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown' THEN 1 END) as exact_unknown,
                count(CASE WHEN lower(trim(CAST({col_expr} AS VARCHAR))) IN ({PLACEHOLDER_SQL}) THEN 1 END) as placeholders,
                count(CASE WHEN {col_expr} IS NULL OR trim(CAST({col_expr} AS VARCHAR)) = '' THEN 1 END) as blank_missing,
                count(CASE WHEN 
                    lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown business'
                    OR lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown'
                    OR lower(trim(CAST({col_expr} AS VARCHAR))) IN ({PLACEHOLDER_SQL})
                    OR {col_expr} IS NULL 
                    OR trim(CAST({col_expr} AS VARCHAR)) = ''
                THEN 1 END) as total_affected
            FROM {read_expr}
        """
        row = con.execute(q).fetchone()
        total_rows = row[0]
        exact_ub = row[1]
        exact_unk = row[2]
        placeholders = row[3]
        blank_missing = row[4]
        total_affected = row[5]
        
        # Calculate duplicates among affected records if affected > 0
        dup_count = 0
        if total_affected > 0 and extra_cols:
            cols_clause = ", ".join([f'coalesce(CAST("{c}" AS VARCHAR), \'\')' for c in extra_cols])
            dup_q = f"""
                SELECT count(*) - count(DISTINCT ({cols_clause}))
                FROM {read_expr}
                WHERE 
                    lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown business'
                    OR lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown'
                    OR lower(trim(CAST({col_expr} AS VARCHAR))) IN ({PLACEHOLDER_SQL})
                    OR {col_expr} IS NULL 
                    OR trim(CAST({col_expr} AS VARCHAR)) = ''
            """
            dup_res = con.execute(dup_q).fetchone()
            dup_count = dup_res[0] if dup_res else 0
        elif total_affected > 0:
            dup_q = f"""
                SELECT count(*) - count(DISTINCT CAST({col_expr} AS VARCHAR))
                FROM {read_expr}
                WHERE 
                    lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown business'
                    OR lower(trim(CAST({col_expr} AS VARCHAR))) = 'unknown'
                    OR lower(trim(CAST({col_expr} AS VARCHAR))) IN ({PLACEHOLDER_SQL})
                    OR {col_expr} IS NULL 
                    OR trim(CAST({col_expr} AS VARCHAR)) = ''
            """
            dup_res = con.execute(dup_q).fetchone()
            dup_count = dup_res[0] if dup_res else 0
            
        elapsed = time.time() - t0
        pct = (total_affected / total_rows * 100) if total_rows > 0 else 0.0
        
        return {
            "label": file_label,
            "filename": os.path.basename(file_path),
            "size_mb": file_size_mb,
            "column_scanned": name_col,
            "total_rows": total_rows,
            "exact_unknown_business": exact_ub,
            "exact_unknown": exact_unk,
            "placeholders": placeholders,
            "blank_missing": blank_missing,
            "total_affected": total_affected,
            "pct_affected": pct,
            "duplicates_in_affected": dup_count,
            "scan_seconds": elapsed,
            "error": None
        }
    except Exception as e:
        return {
            "label": file_label,
            "filename": os.path.basename(file_path),
            "size_mb": file_size_mb,
            "column_scanned": name_col,
            "total_rows": 0,
            "exact_unknown_business": 0,
            "exact_unknown": 0,
            "placeholders": 0,
            "blank_missing": 0,
            "total_affected": 0,
            "pct_affected": 0.0,
            "duplicates_in_affected": 0,
            "scan_seconds": time.time() - t0,
            "error": str(e)
        }

def run_full_audit():
    print("=" * 110)
    print("STARTING AUDIT: UNKNOWN BUSINESS AND MISSING BUSINESS NAME PLACEHOLDERS")
    print("MODE: STRICT AUDIT ONLY (READ-ONLY, ZERO FILE OR DB MODIFICATIONS)")
    print("=" * 110)
    
    con = duckdb.connect()
    con.execute("PRAGMA threads=8;")
    con.execute("SET preserve_insertion_order=false;")
    
    datasets_to_scan = [
        # 1. Targeted Vertical CSVs
        ("Restaurants CSV", os.path.join(LEADS_DIR, "050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        ("Realtors CSV", os.path.join(LEADS_DIR, "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        ("Coaches CSV", os.path.join(LEADS_DIR, "166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        ("Musicians CSV", os.path.join(LEADS_DIR, "74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        ("Designers CSV", os.path.join(LEADS_DIR, "94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        ("Founders/Entrepreneurs CSV", os.path.join(LEADS_DIR, "b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        ("Photographers CSV", os.path.join(LEADS_DIR, "da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv"), "read_csv_auto", "name", ["name", "email", "phone"]),
        
        # 2. Commercial Real Estate B2B Registry
        ("Real Estate B2B (free-tier.csv)", os.path.join(LEADS_DIR, "free-tier.csv"), "read_csv_auto", "COMPANY", ["COMPANY", "ADDRESS", "PHONE_NUMBER", "Email"]),
        
        # 3. Master Locations
        ("Master Locations CSV", os.path.join(LEADS_DIR, "master-locations.csv"), "read_csv_auto", "store_name", ["store_name", "city", "coordinates"]),
        
        # 4. Open Company Sample
        ("Open Company Sample CSV", os.path.join(LEADS_DIR, "open_company_database_sample.csv"), "read_csv_auto", "company_name", ["company_name", "company_domain"]),
        
        # 5. Core Parquet Datasets
        ("B2B Decision Makers Parquet", os.path.join(LEADS_DIR, "b2b_executives.parquet"), "read_parquet", "name", ["name", "contact_name", "job_title", "address"]),
        ("Homeowners Parquet", os.path.join(LEADS_DIR, "homeowners.parquet"), "read_parquet", "name", ["name", "address", "city", "phone"]),
        ("Open Company Database Parquet", os.path.join(LEADS_DIR, "open_company_database.parquet"), "read_parquet", "name", ["name", "address", "city"]),
        ("Tech Stack Companies Parquet", os.path.join(LEADS_DIR, "tech_stack_companies.parquet"), "read_parquet", "name", ["name", "website", "category"]),
        ("GLEIF Golden Copy Parquet", os.path.join(LEADS_DIR, "gleif_goldencopy.parquet"), "read_parquet", "name", ["lei", "name", "city"]),
        ("SEC Company Facts Parquet", os.path.join(LEADS_DIR, "sec_company_facts.parquet"), "read_parquet", "name", ["cik", "name"]),
        ("Common Crawl Web Index Parquet", os.path.join(LEADS_DIR, "cc_web_index.parquet"), "read_parquet", "name", ["name", "website"]),
        
        # 6. Raw 18 B2B Executive Shards (free-tier 2 to 19)
    ]
    
    for i in range(2, 20):
        b2b_path = os.path.join(LEADS_DIR, f"free-tier ({i}).csv")
        datasets_to_scan.append((f"B2B Shard {i} (free-tier ({i}).csv)", b2b_path, "read_csv_auto", "Company Name", ["Company Name", "Full name", "Emails", "Phone numbers"]))
    
    # 7. Raw Homeowners CSV (free-tier (1).csv)
    # free-tier (1).csv has Residence_Type as the property designation
    datasets_to_scan.append(("Homeowners Raw CSV (free-tier (1).csv)", os.path.join(LEADS_DIR, "free-tier (1).csv"), "read_csv_auto", "Residence_Type", ["Residence_Type", "County", "City", "Area_Code_and_Phone"]))
    
    results = []
    
    for label, fpath, fn, col, extra_cols in datasets_to_scan:
        res = audit_dataset(con, label, fpath, fn, col, extra_cols)
        if res:
            results.append(res)
            print(f"Scanned {res['label']:<40} | Total: {res['total_rows']:>10,} | 'Unknown Business': {res['exact_unknown_business']:>6,} | 'Unknown': {res['exact_unknown']:>6,} | Placeholders: {res['placeholders']:>6,} | Blank: {res['blank_missing']:>6,} | Affected: {res['total_affected']:>8,} ({res['pct_affected']:>5.2f}%) | Dups in Affected: {res['duplicates_in_affected']:>6,}")
    
    # Check Data Legion CSV.GZ (28M rows)
    legion_path = os.path.join(LEADS_DIR, "data-legion-company-free-1.5.0_2026-10-15.csv.gz")
    if os.path.exists(legion_path):
        print(f"\nScanning Data Legion Compressed Dataset ({os.path.basename(legion_path)})...")
        legion_res = audit_dataset(con, "Data Legion Company Registry (GZ)", legion_path, "read_csv_auto", "name", ["name", "domain"])
        if legion_res:
            results.append(legion_res)
            print(f"Scanned {legion_res['label']:<40} | Total: {legion_res['total_rows']:>10,} | 'Unknown Business': {legion_res['exact_unknown_business']:>6,} | 'Unknown': {legion_res['exact_unknown']:>6,} | Placeholders: {legion_res['placeholders']:>6,} | Blank: {legion_res['blank_missing']:>6,} | Affected: {legion_res['total_affected']:>8,} ({legion_res['pct_affected']:>5.2f}%) | Dups in Affected: {legion_res['duplicates_in_affected']:>6,}")

    return results

if __name__ == "__main__":
    results = run_full_audit()
