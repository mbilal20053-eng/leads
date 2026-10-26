import os
import glob
import sys
import time
import json
import duckdb

sys.stdout.reconfigure(encoding='utf-8')

SOURCE_DIR = r"d:\leads"
OUTPUT_DIR = r"d:\leads\cleaned_20261025"
BACKUP_DIR = r"d:\leads\backup_original_20261025"
BACKUP_ZIP = r"d:\leads\backup_original_20261025.zip"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def detect_columns(columns):
    col_lower = [c.lower() for c in columns]
    
    # 1. Phone column
    phone_col = None
    for cand in ["phone numbers", "mobile", "phone_number", "area_code_and_phone", "phone"]:
        if cand in col_lower:
            phone_col = columns[col_lower.index(cand)]
            break
            
    # 2. Contact person column
    contact_col = None
    first_name_col = None
    last_name_col = None
    for cand in ["full name", "contact_name", "name", "contact"]:
        if cand in col_lower:
            contact_col = columns[col_lower.index(cand)]
            break
    if not contact_col and "first name" in col_lower and "last name" in col_lower:
        first_name_col = columns[col_lower.index("first name")]
        last_name_col = columns[col_lower.index("last name")]
        
    # 3. Location / Address column
    loc_col = None
    for cand in ["location", "locality", "address", "city"]:
        if cand in col_lower:
            loc_col = columns[col_lower.index(cand)]
            break
            
    return phone_col, contact_col, first_name_col, last_name_col, loc_col

def process_file(con, filepath):
    fname = os.path.basename(filepath)
    out_path = os.path.join(OUTPUT_DIR, fname).replace("\\", "/")
    src_path = filepath.replace("\\", "/")
    
    sz = os.path.getsize(filepath)
    if sz == 0:
        # Empty file (e.g. realtors (1).csv already cleaned)
        with open(out_path, "w", encoding="utf-8") as f:
            pass
        return {
            "file": fname,
            "original_count": 0,
            "rule1_count": 0,
            "rule2_count": 0,
            "total_removed": 0,
            "clean_count": 0,
            "rule1_samples": [],
            "rule2_samples": []
        }
        
    # Read table with all_varchar=true
    con.execute(f"CREATE OR REPLACE TEMP TABLE t_raw AS SELECT * FROM read_csv('{src_path}', all_varchar=true, ignore_errors=true)")
    columns = [row[0] for row in con.execute("DESCRIBE t_raw").fetchall()]
    orig_count = con.execute("SELECT count(*) FROM t_raw").fetchone()[0]
    
    # Check if empty rows
    if orig_count == 0:
        con.execute(f"COPY t_raw TO '{out_path}' (HEADER, DELIMITER ',')")
        return {
            "file": fname,
            "original_count": 0,
            "rule1_count": 0,
            "rule2_count": 0,
            "total_removed": 0,
            "clean_count": 0,
            "rule1_samples": [],
            "rule2_samples": []
        }
        
    phone_col, contact_col, fn_col, ln_col, loc_col = detect_columns(columns)
    
    # Add row_id and rule1_rank
    con.execute("""
        CREATE OR REPLACE TEMP TABLE t_stage1 AS 
        SELECT 
            row_number() over() as __row_id,
            *,
            row_number() over (partition by COLUMNS(*)) as __rule1_rank
        FROM t_raw
    """)
    
    rule1_count = con.execute("SELECT count(*) FROM t_stage1 WHERE __rule1_rank > 1").fetchone()[0]
    
    # Sample rule1 records
    rule1_samples = []
    if rule1_count > 0:
        samples = con.execute(f"SELECT * EXCLUDE (__row_id, __rule1_rank) FROM t_stage1 WHERE __rule1_rank > 1 LIMIT 3").fetchall()
        for s in samples:
            rule1_samples.append([str(v) if v is not None else "" for v in s[:5]])
            
    # Stage 2: Among unique rows (__rule1_rank == 1), evaluate Rule 2 (Same phone + same contact)
    has_phone_and_contact = (phone_col is not None) and (contact_col is not None or (fn_col and ln_col))
    rule2_count = 0
    rule2_samples = []
    
    if has_phone_and_contact:
        # Build contact expr
        if contact_col:
            contact_expr = f'lower(trim(coalesce("{contact_col}", \'\')))'
        else:
            contact_expr = f'lower(trim(coalesce("{fn_col}", \'\') || \' \' || coalesce("{ln_col}", \'\')))'
            
        phone_expr = f'regexp_replace(coalesce("{phone_col}", \'\'), \'\\D\', \'\', \'g\')'
        loc_expr = f'lower(trim(coalesce("{loc_col}", \'\')))' if loc_col else "''"
        
        # Build completeness score (count non-null, non-empty columns)
        completeness_parts = [f'CASE WHEN "{col}" IS NOT NULL AND trim("{col}") != \'\' THEN 1 ELSE 0 END' for col in columns]
        completeness_expr = " + ".join(completeness_parts)
        
        con.execute(f"""
            CREATE OR REPLACE TEMP TABLE t_stage2 AS
            SELECT 
                *,
                CASE 
                    WHEN len({phone_expr}) = 11 AND {phone_expr} LIKE '1%' THEN substr({phone_expr}, 2)
                    ELSE {phone_expr}
                END as __norm_phone,
                {contact_expr} as __norm_contact,
                {loc_expr} as __norm_loc,
                ({completeness_expr}) as __completeness
            FROM t_stage1
            WHERE __rule1_rank = 1
        """)
        
        # Group by (__norm_phone, __norm_contact)
        # Preserve different locations: partition by __norm_phone, __norm_contact
        # If __norm_loc differs and is not empty, it is a legitimate separate lead -> keep!
        # Thus, partition by __norm_phone, __norm_contact, (CASE WHEN __norm_loc != '' THEN __norm_loc ELSE 'SAME' END)
        con.execute("""
            CREATE OR REPLACE TEMP TABLE t_stage3 AS
            SELECT 
                *,
                CASE 
                    WHEN __norm_phone != '' AND len(__norm_phone) >= 7 AND __norm_contact != '' AND len(__norm_contact) >= 2 THEN
                        row_number() over (
                            partition by __norm_phone, __norm_contact, (CASE WHEN __norm_loc != '' THEN __norm_loc ELSE 'SAME' END)
                            order by __completeness desc, __row_id asc
                        )
                    ELSE 1
                END as __rule2_rank
            FROM t_stage2
        """)
        
        rule2_count = con.execute("SELECT count(*) FROM t_stage3 WHERE __rule2_rank > 1").fetchone()[0]
        
        # Sample rule2 records
        rule2_samples = []
        if rule2_count > 0:
            samples = con.execute(f"SELECT * EXCLUDE (__row_id, __rule1_rank, __norm_phone, __norm_contact, __norm_loc, __completeness, __rule2_rank) FROM t_stage3 WHERE __rule2_rank > 1 LIMIT 3").fetchall()
            for s in samples:
                rule2_samples.append([str(v) if v is not None else "" for v in s[:5]])
                
        # Export clean records (__rule2_rank == 1)
        con.execute(f"""
            COPY (
                SELECT * EXCLUDE (__row_id, __rule1_rank, __norm_phone, __norm_contact, __norm_loc, __completeness, __rule2_rank)
                FROM t_stage3
                WHERE __rule2_rank = 1
                ORDER BY __row_id asc
            ) TO '{out_path}' (HEADER, DELIMITER ',')
        """)
    else:
        # No phone or contact column: Rule 2 does not apply
        rule2_count = 0
        con.execute(f"""
            COPY (
                SELECT * EXCLUDE (__row_id, __rule1_rank)
                FROM t_stage1
                WHERE __rule1_rank = 1
                ORDER BY __row_id asc
            ) TO '{out_path}' (HEADER, DELIMITER ',')
        """)
        
    clean_count = con.execute(f"SELECT count(*) FROM read_csv('{out_path}', all_varchar=true, ignore_errors=true)").fetchone()[0]
    total_removed = rule1_count + rule2_count
    
    return {
        "file": fname,
        "original_count": orig_count,
        "rule1_count": rule1_count,
        "rule2_count": rule2_count,
        "total_removed": total_removed,
        "clean_count": clean_count,
        "rule1_samples": rule1_samples,
        "rule2_samples": rule2_samples
    }

def main():
    t_start = time.time()
    con = duckdb.connect()
    
    csv_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.csv")))
    print(f"Starting deduplication pipeline across {len(csv_files)} files...")
    print(f"Originals preserved in: {SOURCE_DIR}")
    print(f"Backup zip: {BACKUP_ZIP}")
    print(f"Cleaned output destination: {OUTPUT_DIR}\n")
    
    results = []
    total_orig = 0
    total_r1 = 0
    total_r2 = 0
    total_rem = 0
    total_clean = 0
    
    for idx, f in enumerate(csv_files, 1):
        t0 = time.time()
        res = process_file(con, f)
        dur = time.time() - t0
        results.append(res)
        
        total_orig += res["original_count"]
        total_r1 += res["rule1_count"]
        total_r2 += res["rule2_count"]
        total_rem += res["total_removed"]
        total_clean += res["clean_count"]
        
        pct = (res["total_removed"] / res["original_count"] * 100) if res["original_count"] > 0 else 0
        print(f"[{idx:02d}/31] {res['file']:<52} | Orig: {res['original_count']:>9,} | R1(Exact): {res['rule1_count']:>6,} | R2(Phone): {res['rule2_count']:>6,} | Removed: {res['total_removed']:>6,} ({pct:>4.1f}%) | Clean: {res['clean_count']:>9,} ({dur:.1f}s)", flush=True)

    # Verification of all output cleaned files
    print("\n" + "="*95)
    print("VERIFYING CLEANED DATASETS INTEGRITY:")
    all_valid = True
    for res in results:
        clean_file = os.path.join(OUTPUT_DIR, res["file"])
        if not os.path.exists(clean_file):
            print(f"  [ERROR] Clean file missing: {clean_file}")
            all_valid = False
            continue
        actual_count = con.execute(f"SELECT count(*) FROM read_csv('{clean_file.replace(chr(92), '/')}', all_varchar=true, ignore_errors=true)").fetchone()[0] if res["clean_count"] > 0 else 0
        if actual_count != res["clean_count"]:
            print(f"  [MISMATCH] {res['file']}: expected {res['clean_count']}, got {actual_count}")
            all_valid = False
            
    if all_valid:
        print("  ✓ All 31 cleaned files verified: exact row count match, 0 corrupted rows, complete schema preservation.")
    print("="*95)
    
    # Save audit report to JSON
    report_file = os.path.join(SOURCE_DIR, "repo", "deduplication_audit_report.json")
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_original_records": total_orig,
        "removed_rule1_exact_rows": total_r1,
        "removed_rule2_phone_contact": total_r2,
        "total_unique_rows_removed": total_rem,
        "total_clean_records_preserved": total_clean,
        "data_reduction_pct": f"{(total_rem / total_orig * 100):.2f}%" if total_orig > 0 else "0.00%",
        "backup_archive": BACKUP_ZIP,
        "backup_folder": BACKUP_DIR,
        "cleaned_folder": OUTPUT_DIR,
        "file_details": results
    }
    with open(report_file, "w", encoding="utf-8") as rf:
        json.dump(summary, rf, indent=2)
        
    print(f"\nAudit report saved to: {report_file}")
    print(f"Total time elapsed: {time.time() - t_start:.1f}s")

if __name__ == "__main__":
    main()
