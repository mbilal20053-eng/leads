"""
Stream through free_company_dataset.csv.zip and count total rows, missing names, missing websites, and all 4 missing.
"""
import gzip
import time
import os

p = r"d:\leads\free_company_dataset.csv.zip"
t0 = time.time()

PLACEHOLDER_SET = {
    'unknown business', 'unknown', 'tbd', 'n/a', 'na', 'none', 'null', 'nan',
    '-', '--', '---', '.', '..', 'not available', 'unknown company',
    'unnamed business', 'unnamed', 'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'test'
}

print(f"Streaming {p} ({os.path.getsize(p)/(1024*1024):.1f} MB)...")

total_rows = 0
missing_names = 0
missing_websites = 0
all_4_missing = 0

# Check first 5 million rows to benchmark and get exact stats
with gzip.open(p, "rt", encoding="utf-8", errors="ignore") as f:
    header = f.readline().strip().split(",")
    # Find indices
    name_idx = header.index("name")
    web_idx = header.index("website")
    
    for line in f:
        total_rows += 1
        parts = line.split(",")
        if len(parts) > max(name_idx, web_idx):
            name_val = parts[name_idx].strip().lower()
            web_val = parts[web_idx].strip().lower()
            
            is_name_missing = (not name_val) or (name_val in PLACEHOLDER_SET)
            is_web_missing = (not web_val) or (web_val in ('null', 'none', 'nan', 'n/a', 'na', 'http://', 'https://', 'www.')) or ('.' not in web_val) or (len(web_val) < 4)
            
            if is_name_missing:
                missing_names += 1
            if is_web_missing:
                missing_websites += 1
            if is_name_missing and is_web_missing:
                all_4_missing += 1
        
        if total_rows % 1000000 == 0:
            elapsed = time.time() - t0
            print(f"  Processed {total_rows:>10,} rows in {elapsed:>5.1f}s | Missing Names: {missing_names:>6,} | Missing Web: {missing_websites:>8,} | All 4 Missing: {all_4_missing:>6,}")
            # If we want a 5M sample or full stream
            if total_rows >= 5000000:
                break

elapsed = time.time() - t0
print("\nStream finished:")
print(f"Total Rows Checked:   {total_rows:>10,}")
print(f"Missing Names:        {missing_names:>10,} ({missing_names/total_rows*100:.4f}%)")
print(f"Missing Websites:     {missing_websites:>10,} ({missing_websites/total_rows*100:.2f}%)")
print(f"All 4 Missing:        {all_4_missing:>10,} ({all_4_missing/total_rows*100:.6f}%)")
