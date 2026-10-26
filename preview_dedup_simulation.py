import os
import glob
import csv
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = r"d:\leads"

def normalize_text(val):
    if not val:
        return ""
    # Strip whitespace, collapse multi-spaces, lowercase
    return re.sub(r"\s+", " ", str(val).strip().lower())

def normalize_phone(val):
    if not val:
        return ""
    # Extract only digits
    digits = re.sub(r"\D", "", str(val))
    # If 11 digits starting with 1 (US country code), strip 1 for 10-digit match
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits if len(digits) >= 7 else ""

def get_row_keys(row, header, fname):
    # Determine contact name and phone from header
    col_map = {col.lower(): i for i, col in enumerate(header)}
    
    # 1. Contact person name
    contact_name = ""
    for candidate in ["full name", "contact_name", "name", "contact"]:
        if candidate in col_map:
            contact_name = row[col_map[candidate]]
            break
    if not contact_name and "first name" in col_map and "last name" in col_map:
        fn = row[col_map["first name"]]
        ln = row[col_map["last name"]]
        contact_name = f"{fn} {ln}".strip()
    
    # 2. Phone number
    phone_val = ""
    for candidate in ["phone numbers", "mobile", "phone_number", "area_code_and_phone", "phone"]:
        if candidate in col_map:
            val = row[col_map[candidate]]
            if val and len(str(val).strip()) >= 7:
                phone_val = val
                break
                
    # 3. Normalized full row key (for Rule 1)
    norm_row_tuple = tuple(normalize_text(cell) for cell in row)
    
    # 4. Normalized phone and contact (for Rule 2)
    norm_phone = normalize_phone(phone_val)
    norm_contact = normalize_text(contact_name)
    
    # Address / location for safety preservation check
    address_val = ""
    for candidate in ["address", "location", "locality", "city"]:
        if candidate in col_map:
            address_val = row[col_map[candidate]]
            break
    norm_address = normalize_text(address_val)
    
    return norm_row_tuple, norm_phone, norm_contact, norm_address, contact_name, phone_val

def simulate_file_dedup(filepath):
    fname = os.path.basename(filepath)
    if os.path.getsize(filepath) == 0:
        return {
            "file": fname,
            "original_count": 0,
            "rule1_count": 0,
            "rule2_count": 0,
            "total_removed": 0,
            "final_count": 0,
            "rule1_samples": [],
            "rule2_samples": []
        }
        
    seen_exact_rows = set()
    # Map (norm_phone, norm_contact) -> first seen record info
    seen_phone_contact = {}
    
    original_count = 0
    rule1_count = 0
    rule2_count = 0
    
    rule1_samples = []
    rule2_samples = []
    
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return None
            
        for row in reader:
            if not row or not any(row):
                continue
            original_count += 1
            
            norm_row, norm_phone, norm_contact, norm_addr, raw_contact, raw_phone = get_row_keys(row, header, fname)
            
            # --- RULE 1: Exact Duplicate Row ---
            if norm_row in seen_exact_rows:
                rule1_count += 1
                if len(rule1_samples) < 3:
                    rule1_samples.append({
                        "row_num": original_count,
                        "contact": raw_contact,
                        "phone": raw_phone,
                        "row_preview": row[:5]
                    })
                continue  # Removed under Rule 1, do not double count
                
            # --- RULE 2: Same Phone AND Same Contact Name ---
            # "Remove duplicate records only when the phone number and contact person's name match.
            # If the same phone number belongs to different people, keep all their records."
            # Also preserve records if they have different addresses/locations
            is_rule2_dup = False
            if norm_phone and norm_contact and len(norm_contact) >= 3:
                phone_contact_key = (norm_phone, norm_contact)
                if phone_contact_key in seen_phone_contact:
                    prior_addr = seen_phone_contact[phone_contact_key]
                    # Check address preservation rule:
                    # "Preserve records with different business addresses, locations, or contact people when they represent legitimate separate leads."
                    if norm_addr and prior_addr and norm_addr != prior_addr:
                        # Different location/address: legitimate separate lead -> KEEP!
                        is_rule2_dup = False
                    else:
                        is_rule2_dup = True
                        rule2_count += 1
                        if len(rule2_samples) < 3:
                            rule2_samples.append({
                                "row_num": original_count,
                                "contact": raw_contact,
                                "phone": raw_phone,
                                "row_preview": row[:5]
                            })
                else:
                    seen_phone_contact[phone_contact_key] = norm_addr
                    
            if is_rule2_dup:
                continue  # Removed under Rule 2
                
            # If we reach here, row is KEPT!
            seen_exact_rows.add(norm_row)
            if norm_phone and norm_contact and len(norm_contact) >= 3:
                seen_phone_contact[(norm_phone, norm_contact)] = norm_addr

    total_removed = rule1_count + rule2_count
    final_count = original_count - total_removed
    
    return {
        "file": fname,
        "original_count": original_count,
        "rule1_count": rule1_count,
        "rule2_count": rule2_count,
        "total_removed": total_removed,
        "final_count": final_count,
        "rule1_samples": rule1_samples,
        "rule2_samples": rule2_samples
    }

def main():
    csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    print(f"Scanning and simulating deduplication across {len(csv_files)} files...\n")
    
    results = []
    total_orig = 0
    total_r1 = 0
    total_r2 = 0
    total_rem = 0
    total_fin = 0
    
    t0 = time.time()
    for f in csv_files:
        t_file = time.time()
        res = simulate_file_dedup(f)
        if not res:
            continue
        results.append(res)
        
        total_orig += res["original_count"]
        total_r1 += res["rule1_count"]
        total_r2 += res["rule2_count"]
        total_rem += res["total_removed"]
        total_fin += res["final_count"]
        
        dur = time.time() - t_file
        rem_pct = (res["total_removed"] / res["original_count"] * 100) if res["original_count"] > 0 else 0
        print(f"  [{res['file']}] Orig: {res['original_count']:,} | Rule1: {res['rule1_count']:,} | Rule2: {res['rule2_count']:,} | Removed: {res['total_removed']:,} ({rem_pct:.1f}%) | Clean: {res['final_count']:,} ({dur:.1f}s)")
        
    elapsed = time.time() - t0
    print("\n" + "="*80)
    print(f"TOTAL ORIGINAL RECORDS: {total_orig:,}")
    print(f"REMOVED UNDER RULE 1 (Exact Duplicate Rows): {total_r1:,}")
    print(f"REMOVED UNDER RULE 2 (Duplicate Phone + Same Contact Person): {total_r2:,}")
    print(f"TOTAL UNIQUE ROWS REMOVED: {total_rem:,}")
    print(f"TOTAL CLEAN RECORDS PRESERVED: {total_fin:,}")
    print(f"Time elapsed: {elapsed:.1f}s")
    print("="*80)

if __name__ == "__main__":
    main()
