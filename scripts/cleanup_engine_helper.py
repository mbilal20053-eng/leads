"""
FULL PORTFOLIO DATA VERIFICATION, CLEANUP & AUDIT ENGINE
STRICT ZERO-DESTRUCTION SAFETY:
- Original source files are NEVER modified, overwritten, or deleted.
- Cleaned files and exclusion logs are written strictly to d:\\leads\\cleaned_export\\
"""

import os
import sys
import time
import json
import hashlib
import duckdb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

LEADS_DIR = r"d:\leads"
EXPORT_DIR = r"d:\leads\cleaned_export"
os.makedirs(EXPORT_DIR, exist_ok=True)

PLACEHOLDER_LIST = [
    'n/a', 'na', 'none', 'null', 'nan', '-', '--', '---', '.', '..',
    'not available', 'unknown company', 'unnamed business', 'unnamed',
    'n / a', 'na.', 'n.a.', 'n.a', 'no name', 'nil', 'tbd', 'test',
    'unknown business', 'unknown'
]
PLACEHOLDER_SQL = ", ".join([f"'{p}'" for p in PLACEHOLDER_LIST])

def get_file_sha256(filepath, max_bytes=10*1024*1024):
    """Compute sha256 of first 10MB of file for fast verification before and after"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        chunk = f.read(max_bytes)
        h.update(chunk)
    return h.hexdigest()

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

def build_valid_name_sql(name_col):
    if not name_col:
        return "1=0"
    return f"""(
        "{name_col}" IS NOT NULL 
        AND length(trim(CAST("{name_col}" AS VARCHAR))) > 1 
        AND lower(trim(CAST("{name_col}" AS VARCHAR))) NOT IN ({PLACEHOLDER_SQL})
    )"""

print("Engine helper module initialized.")
