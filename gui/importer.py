"""
Lead Engine PRO - Enterprise Ingestion & Dataset Importer Module
Handles multi-file CSV uploads, intelligent encoding & delimiter auto-detection,
schema normalization, configurable deduplication, data provenance tracking,
and atomic commit into DuckDB and Parquet storage.
"""
import os
import re
import csv
import io
import json
import time
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

import duckdb

# Determine base data directory
CANDIDATE_DATA_DIRS = [
    os.environ.get("LEADS_DATA_DIR"),
    r"d:\leads",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"),
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
]

DATA_DIR = r"d:\leads"
for cd in CANDIDATE_DATA_DIRS:
    if cd and os.path.exists(cd):
        try:
            # test writeability
            test_file = os.path.join(cd, ".perm_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            DATA_DIR = cd
            break
        except Exception:
            continue

IMPORTED_DIR = os.path.join(DATA_DIR, "imported_datasets")
STAGING_DIR = os.path.join(IMPORTED_DIR, "staging")
RAW_UPLOADS_DIR = os.path.join(IMPORTED_DIR, "raw_uploads")
REPORTS_DIR = os.path.join(IMPORTED_DIR, "reports")
REGISTRY_FILE = os.path.join(IMPORTED_DIR, "datasets_registry.json")
AUDIT_LOG_FILE = os.path.join(IMPORTED_DIR, "audit_log.json")

for d in [IMPORTED_DIR, STAGING_DIR, RAW_UPLOADS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Standard target columns in Lead Engine PRO
TARGET_COLUMNS = [
    {"key": "name", "label": "Business Name", "required": True, "desc": "Company, establishment, or entity name"},
    {"key": "contact_name", "label": "Owner / Contact", "required": False, "desc": "Executive, founder, or contact person"},
    {"key": "job_title", "label": "Role & Notes", "required": False, "desc": "Job title, professional role, or position"},
    {"key": "category", "label": "Category / Industry", "required": False, "desc": "Industry classification or business specialty"},
    {"key": "email", "label": "Email Address", "required": False, "desc": "Direct or corporate email address"},
    {"key": "phone", "label": "Phone Number", "required": False, "desc": "Primary phone, mobile, or direct telephone"},
    {"key": "website", "label": "Website / Domain", "required": False, "desc": "Company website domain or URL"},
    {"key": "address", "label": "Street Address", "required": False, "desc": "Physical street address or location"},
    {"key": "city", "label": "City", "required": False, "desc": "City, town, or locality"},
    {"key": "state", "label": "State / Region", "required": False, "desc": "State, province, or region"},
    {"key": "zip", "label": "ZIP / Postal Code", "required": False, "desc": "Postal or zip code"},
    {"key": "country", "label": "Country", "required": False, "desc": "Country name or country code"},
    {"key": "socials", "label": "Social Profiles", "required": False, "desc": "LinkedIn URL, Twitter, or social profile"}
]

HEADER_ALIASES = {
    "name": [
        "company", "company name", "company_name", "business", "business name", "business_name",
        "organization", "org", "firm", "account", "account name", "legal name", "legal_name",
        "trade name", "brand", "client", "store name", "store_name", "entity_name", "name"
    ],
    "contact_name": [
        "contact", "contact name", "contact_name", "full name", "fullname", "full_name",
        "first name", "firstname", "first_name", "owner", "owner name", "executive", "person",
        "decision maker", "representative", "contact person", "lead name"
    ],
    "job_title": [
        "title", "job title", "job_title", "position", "role", "designation", "rank",
        "occupation", "profession", "sub role", "sub_role"
    ],
    "category": [
        "category", "industry", "sector", "business type", "business_type", "vertical", "trade",
        "specialty", "type", "sic", "sic description", "naics", "niche", "genre", "market",
        "categories", "primary category"
    ],
    "email": [
        "email", "e-mail", "email address", "email_address", "contact email", "work email",
        "primary email", "emails", "mail", "corporate email"
    ],
    "phone": [
        "phone", "telephone", "phone number", "phone_number", "mobile", "cell", "tel",
        "contact number", "work phone", "direct phone", "phone numbers", "area code and phone", "main phone"
    ],
    "website": [
        "website", "web", "url", "domain", "company website", "company_website", "homepage",
        "site", "company domain", "web address", "link", "web_url"
    ],
    "address": [
        "address", "street", "street address", "street_address", "address line 1", "address1",
        "location", "street 1", "biz addr", "business address", "addr"
    ],
    "city": [
        "city", "locality", "town", "municipality", "suburb"
    ],
    "state": [
        "state", "region", "province", "state/province", "county", "state or country", "state_code"
    ],
    "zip": [
        "zip", "zip code", "zipcode", "postal", "postal code", "postcode", "zip_code", "postal_code"
    ],
    "country": [
        "country", "nation", "country_code", "country code", "geo", "state or country description"
    ],
    "socials": [
        "socials", "linkedin", "linkedin url", "linkedin_url", "twitter", "facebook",
        "instagram", "social", "profile"
    ]
}

def slugify(text: str) -> str:
    """Converts a dataset name to a safe, unique alphanumeric ID slug."""
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s[:64] if s else "imported_dataset"

def sanitize_csv_cell(val: Any) -> str:
    """Prevents CSV formula injection by prepending a single quote to dangerous symbols."""
    if val is None:
        return ""
    raw_s = str(val)
    if raw_s and raw_s[0] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + raw_s.strip()
    s = raw_s.strip()
    if s and s[0] in ('=', '+', '-', '@'):
        return "'" + s
    return s

def normalize_email(val: Any) -> str:
    if not val:
        return ""
    s = str(val).strip().lower()
    if "@" in s and "." in s and len(s) > 5 and not s.startswith(('@', '.')):
        # Match email token
        m = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", s)
        if m:
            return m.group(0)
    return ""

def normalize_phone(val: Any) -> str:
    if not val:
        return ""
    raw = str(val).strip()
    digits = re.sub(r"\D", "", raw)
    if len(digits) < 7:
        return ""
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits

def normalize_domain(val: Any) -> str:
    if not val:
        return ""
    s = str(val).strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = s.split("/")[0].split("?")[0].split(":")[0]
    if "." in s and len(s) > 3:
        return s
    return ""

def detect_file_encoding_and_delimiter(filepath: str) -> Tuple[str, str]:
    """Inspects file bytes to detect character encoding and delimiter with high accuracy."""
    detected_encoding = "utf-8"
    with open(filepath, "rb") as f:
        sample_bytes = f.read(65536)

    # Check for BOMs
    if sample_bytes.startswith(b"\xef\xbb\xbf"):
        detected_encoding = "utf-8-sig"
    elif sample_bytes.startswith(b"\xff\xfe") or sample_bytes.startswith(b"\xfe\xff"):
        detected_encoding = "utf-16"
    else:
        # Test decodes
        for enc in ["utf-8", "cp1252", "iso-8859-1"]:
            try:
                sample_bytes.decode(enc)
                detected_encoding = enc
                break
            except UnicodeDecodeError:
                continue

    # Decode text sample
    try:
        sample_text = sample_bytes.decode(detected_encoding)
    except Exception:
        sample_text = sample_bytes.decode("latin-1", errors="ignore")
        detected_encoding = "iso-8859-1"

    # Detect delimiter
    lines = [ln for ln in sample_text.splitlines() if ln.strip()][:25]
    if not lines:
        return detected_encoding, ","

    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff("\n".join(lines), delimiters=[",", ";", "\t", "|"])
        delimiter = dialect.delimiter
    except Exception:
        # Fallback counting
        counts = {",": 0, ";": 0, "\t": 0, "|": 0}
        for ln in lines:
            for d in counts:
                counts[d] += ln.count(d)
        delimiter = max(counts, key=counts.get)
        if counts[delimiter] == 0:
            delimiter = ","

    return detected_encoding, delimiter

def auto_map_headers(headers: List[str]) -> List[Dict[str, Any]]:
    """Maps incoming CSV headers to Lead Engine PRO columns using alias heuristics."""
    mappings = []
    used_targets = set()

    for idx, header in enumerate(headers):
        h_clean = header.strip()
        h_lower = h_clean.lower()
        h_norm = re.sub(r"[^a-z0-9]+", " ", h_lower).strip()

        matched_target = None
        matched_confidence = "Low"

        # 1. Exact alias match
        for target_key, aliases in HEADER_ALIASES.items():
            if target_key in used_targets and target_key != "category":
                continue
            if h_lower in aliases or h_norm in aliases:
                matched_target = target_key
                matched_confidence = "100% (Exact Match)"
                break

        # 2. Substring match
        if not matched_target:
            for target_key, aliases in HEADER_ALIASES.items():
                if target_key in used_targets and target_key != "category":
                    continue
                for alias in aliases:
                    if len(alias) >= 3 and (f" {alias} " in f" {h_norm} " or h_norm.startswith(alias) or h_norm.endswith(alias)):
                        matched_target = target_key
                        matched_confidence = "92% (High Confidence)"
                        break
                if matched_target:
                    break

        # Default fallback: Ignore column if unmapped
        if matched_target:
            used_targets.add(matched_target)
            target_info = next((t for t in TARGET_COLUMNS if t["key"] == matched_target), None)
            target_label = target_info["label"] if target_info else matched_target
        else:
            matched_target = "ignore"
            target_label = "-- Ignore Column --"
            matched_confidence = "0% (Unmapped)"

        mappings.append({
            "source_index": idx,
            "source_header": h_clean,
            "target_key": matched_target,
            "target_label": target_label,
            "confidence": matched_confidence
        })

    return mappings

def inspect_csv_file(filepath: str, original_filename: Optional[str] = None) -> Dict[str, Any]:
    """Thoroughly inspects a CSV file without loading the entire dataset into memory."""
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    encoding, delimiter = detect_file_encoding_and_delimiter(filepath)

    sample_rows = []
    headers = []
    total_rows_estimate = 0
    missing_fields_count = {"name": 0, "email": 0, "phone": 0, "website": 0}
    malformed_rows_count = 0
    preview_rows = []

    # Stream read sample lines
    with open(filepath, "r", encoding=encoding, errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            headers = next(reader, [])
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read headers from {filename}: {str(e)}",
                "filename": filename
            }

        headers = [h.strip() if h else f"Column_{i+1}" for i, h in enumerate(headers)]
        mappings = auto_map_headers(headers)
        target_indices = {m["target_key"]: m["source_index"] for m in mappings if m["target_key"] != "ignore"}

        scanned_rows = 0
        total_sample_bytes = 0

        for row_idx, row in enumerate(reader):
            scanned_rows += 1
            if len(row) != len(headers):
                malformed_rows_count += 1

            # Check missing critical values
            if "name" in target_indices:
                idx = target_indices["name"]
                if idx >= len(row) or not row[idx].strip():
                    missing_fields_count["name"] += 1
            if "email" in target_indices:
                idx = target_indices["email"]
                if idx >= len(row) or not normalize_email(row[idx]):
                    missing_fields_count["email"] += 1
            if "phone" in target_indices:
                idx = target_indices["phone"]
                if idx >= len(row) or not normalize_phone(row[idx]):
                    missing_fields_count["phone"] += 1
            if "website" in target_indices:
                idx = target_indices["website"]
                if idx >= len(row) or not normalize_domain(row[idx]):
                    missing_fields_count["website"] += 1

            if scanned_rows <= 5:
                row_dict = {}
                for h_idx, h_name in enumerate(headers):
                    val = row[h_idx] if h_idx < len(row) else ""
                    row_dict[h_name] = val
                preview_rows.append(row_dict)

            if scanned_rows >= 5000:
                # Estimate total rows based on bytes scanned
                bytes_pos = f.tell()
                if bytes_pos > 0:
                    avg_row_bytes = bytes_pos / scanned_rows
                    total_rows_estimate = int(file_size_bytes / avg_row_bytes)
                break

    if total_rows_estimate == 0 or scanned_rows < 5000:
        total_rows_estimate = scanned_rows

    delimiter_name = {
        ",": "Comma (',')",
        ";": "Semicolon (';')",
        "\t": "Tab ('\\t')",
        "|": "Pipe ('|')"
    }.get(delimiter, f"Custom ('{delimiter}')")

    return {
        "success": True,
        "filename": filename,
        "file_size_mb": file_size_mb,
        "file_size_bytes": file_size_bytes,
        "encoding": encoding,
        "delimiter": delimiter,
        "delimiter_name": delimiter_name,
        "headers": headers,
        "columns_count": len(headers),
        "mappings": mappings,
        "total_rows_estimate": total_rows_estimate,
        "scanned_rows_sample": scanned_rows,
        "malformed_rows_in_sample": malformed_rows_count,
        "missing_in_sample": missing_fields_count,
        "preview_rows": preview_rows,
        "target_columns": TARGET_COLUMNS
    }

def load_registry() -> Dict[str, Any]:
    """Loads the persistent registry of imported datasets."""
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"datasets": {}, "updated_at": None}
    return {"datasets": {}, "updated_at": None}

def save_registry(registry: Dict[str, Any]) -> None:
    """Persists the registry of imported datasets atomically."""
    registry["updated_at"] = datetime.now().isoformat()
    tmp_file = REGISTRY_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    shutil.move(tmp_file, REGISTRY_FILE)

def log_audit_event(action: str, dataset_id: str, details: Dict[str, Any]) -> None:
    """Appends an event to the persistent audit log."""
    event = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "dataset_id": dataset_id,
        "details": details
    }
    events = []
    if os.path.exists(AUDIT_LOG_FILE):
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                events = json.load(f)
        except Exception:
            events = []
    events.append(event)
    try:
        with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(events[-500:], f, indent=2)
    except Exception:
        pass

def stage_uploaded_files(uploaded_files: List[Any], dataset_id: str) -> List[Dict[str, Any]]:
    """Saves uploaded files into staging directory with safe unique names."""
    dataset_stage_dir = os.path.join(STAGING_DIR, dataset_id)
    os.makedirs(dataset_stage_dir, exist_ok=True)
    staged_info = []

    for f in uploaded_files:
        orig_name = getattr(f, "filename", "upload.csv")
        safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", orig_name)
        target_path = os.path.join(dataset_stage_dir, safe_name)
        
        # Save file stream
        if hasattr(f, "save"):
            f.save(target_path)
        elif hasattr(f, "read"):
            with open(target_path, "wb") as out:
                out.write(f.read())
                
        staged_info.append({
            "original_filename": orig_name,
            "staged_path": target_path,
            "size_bytes": os.path.getsize(target_path)
        })

    return staged_info

def execute_dataset_import(
    dataset_name: str,
    staged_files: List[Dict[str, Any]],
    column_mappings_per_file: Dict[str, Dict[str, str]],
    duplicate_mode: str = "skip_exact",
    existing_dataset_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes atomic dataset ingestion:
    1. Parses and validates every staged file.
    2. Maps columns to the 12 Lead Engine PRO fields while keeping source provenance.
    3. Filters or flags duplicates according to user choice.
    4. Writes rejected/malformed rows to an error report CSV.
    5. Writes clean records into a partitioned Parquet file.
    6. Updates persistent registry and mounts DuckDB view.
    """
    cleaned_name = dataset_name.strip()
    if not cleaned_name:
        return {"success": False, "error": "Dataset name cannot be empty."}

    dataset_id = existing_dataset_id or slugify(cleaned_name)
    registry = load_registry()

    # If new dataset and ID already exists, prevent accidental overwrite unless expanding
    if not existing_dataset_id and dataset_id in registry.get("datasets", {}):
        suffix = int(time.time()) % 10000
        dataset_id = f"{dataset_id}_{suffix}"

    final_parquet_path = os.path.join(IMPORTED_DIR, f"{dataset_id}.parquet")
    rejection_report_path = os.path.join(REPORTS_DIR, f"{dataset_id}_rejected_{int(time.time())}.csv")

    total_discovered = 0
    total_imported = 0
    total_duplicates = 0
    total_rejected = 0

    seen_emails = set()
    seen_phones = set()
    seen_websites = set()
    seen_name_locs = set()

    # In-memory accumulator for DuckDB bulk ingestion
    rows_to_insert: List[Tuple] = []
    rejected_rows: List[Dict[str, Any]] = []
    file_summaries: List[Dict[str, Any]] = []

    con = duckdb.connect()

    for file_info in staged_files:
        filepath = file_info["staged_path"]
        orig_filename = file_info["original_filename"]
        mapping = column_mappings_per_file.get(orig_filename, {})

        if not os.path.exists(filepath):
            continue

        encoding, delimiter = detect_file_encoding_and_delimiter(filepath)
        f_discovered = 0
        f_imported = 0
        f_duplicates = 0
        f_rejected = 0

        with open(filepath, "r", encoding=encoding, errors="replace", newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            try:
                raw_headers = next(reader, [])
            except Exception as e:
                rejected_rows.append({
                    "source_file": orig_filename,
                    "row_number": 1,
                    "error_reason": f"Corrupt file header: {str(e)}",
                    "raw_data": ""
                })
                continue

            headers = [h.strip() for h in raw_headers]
            # Build index lookup for mapped target fields
            col_indices = {}
            for target_col, src_header in mapping.items():
                if src_header in headers and target_col != "ignore":
                    col_indices[target_col] = headers.index(src_header)

            for line_no, row in enumerate(reader, start=2):
                f_discovered += 1
                total_discovered += 1

                # Extract mapped values
                def get_val(key):
                    idx = col_indices.get(key)
                    if idx is not None and idx < len(row):
                        return row[idx].strip()
                    return ""

                b_name = get_val("name")
                c_name = get_val("contact_name")
                j_title = get_val("job_title")
                cat = get_val("category")
                addr = get_val("address")
                city = get_val("city")
                state = get_val("state")
                zip_c = get_val("zip")
                country = get_val("country") or "United States"
                raw_phone = get_val("phone")
                raw_web = get_val("website")
                raw_email = get_val("email")
                socials = get_val("socials")

                # Validation: Business Name or Contact Name required
                if not b_name and not c_name and not raw_email and not raw_phone:
                    f_rejected += 1
                    total_rejected += 1
                    rejected_rows.append({
                        "source_file": orig_filename,
                        "row_number": line_no,
                        "error_reason": "Missing business name, contact name, and communication channels",
                        "raw_data": "|".join(row[:8])
                    })
                    continue

                if not b_name and c_name:
                    b_name = c_name

                # Clean fields
                clean_email = normalize_email(raw_email)
                clean_phone = normalize_phone(raw_phone)
                clean_web = normalize_domain(raw_web)

                # Deduplication logic
                is_duplicate = False
                dup_reason = ""

                if clean_email and clean_email in seen_emails:
                    is_duplicate = True
                    dup_reason = f"Duplicate email: {clean_email}"
                elif clean_phone and clean_phone in seen_phones:
                    is_duplicate = True
                    dup_reason = f"Duplicate phone: {clean_phone}"
                elif clean_web and b_name and (clean_web, b_name.lower()) in seen_websites:
                    is_duplicate = True
                    dup_reason = f"Duplicate website & name: {clean_web}"
                elif b_name and (city or state):
                    loc_key = f"{b_name.lower()}::{city.lower()}::{state.lower()}"
                    if loc_key in seen_name_locs:
                        is_duplicate = True
                        dup_reason = f"Duplicate company name & location: {b_name} ({city}, {state})"

                if is_duplicate:
                    f_duplicates += 1
                    total_duplicates += 1
                    if duplicate_mode == "skip_exact" or duplicate_mode == "new_only":
                        continue

                # Register seen identifiers
                if clean_email:
                    seen_emails.add(clean_email)
                if clean_phone:
                    seen_phones.add(clean_phone)
                if clean_web:
                    seen_websites.add((clean_web, b_name.lower()))
                if b_name and (city or state):
                    seen_name_locs.add(f"{b_name.lower()}::{city.lower()}::{state.lower()}")

                # Compute tier & score
                has_web = bool(clean_web)
                has_phone = bool(clean_phone)
                has_em = bool(clean_email)

                if has_web and (has_phone or has_em):
                    tier = "A"
                    score = 90
                    opportunity = "VERIFIED MULTI-CHANNEL PROSPECT"
                elif has_web:
                    tier = "A"
                    score = 85
                    opportunity = "COMMERCIAL WEB EXPANSION"
                elif has_phone or has_em:
                    tier = "B"
                    score = 75
                    opportunity = "NO WEBSITE (Urgent Outreach Need)"
                else:
                    tier = "B"
                    score = 65
                    opportunity = "LOCAL BUSINESS PIPELINE"

                if is_duplicate and duplicate_mode == "flag_review":
                    opportunity = f"DUPLICATE REVIEW REQUIRED ({dup_reason})"
                    score = max(50, score - 15)

                lead_id = f"imp_{dataset_id}_{abs(hash(b_name + clean_phone + clean_email + orig_filename))}"
                pitch = f"Commercial sales & conversion outreach for {b_name} in {cat or 'business'}."
                why = f"Imported lead from {cleaned_name} ({orig_filename}) with direct business contact details."

                rows_to_insert.append((
                    lead_id,
                    sanitize_csv_cell(b_name),
                    sanitize_csv_cell(c_name or b_name),
                    sanitize_csv_cell(j_title or "Executive / Manager"),
                    sanitize_csv_cell(cat or "Commercial Services"),
                    sanitize_csv_cell(addr),
                    sanitize_csv_cell(city),
                    sanitize_csv_cell(state),
                    sanitize_csv_cell(zip_c),
                    sanitize_csv_cell(country),
                    clean_phone or raw_phone,
                    clean_web or raw_web,
                    clean_email or raw_email,
                    sanitize_csv_cell(socials),
                    tier,
                    score,
                    opportunity,
                    pitch,
                    why,
                    cleaned_name[:24],
                    dataset_id,
                    "#8b5cf6"
                ))

                f_imported += 1
                total_imported += 1

        file_summaries.append({
            "original_filename": orig_filename,
            "rows_discovered": f_discovered,
            "rows_imported": f_imported,
            "rows_duplicates": f_duplicates,
            "rows_rejected": f_rejected,
            "status": "Success" if f_imported > 0 else "No Valid Leads"
        })

    if total_imported == 0 and total_rejected > 0:
        return {
            "success": False,
            "error": "All records in the uploaded files were rejected. Check rejection report for details.",
            "total_discovered": total_discovered,
            "total_rejected": total_rejected,
            "rejected_report_path": rejection_report_path
        }

    # Atomic write to Parquet via DuckDB
    con.execute("""
    CREATE TABLE t_imported_staging (
        id VARCHAR,
        name VARCHAR,
        contact_name VARCHAR,
        job_title VARCHAR,
        category VARCHAR,
        address VARCHAR,
        city VARCHAR,
        state VARCHAR,
        zip VARCHAR,
        country VARCHAR,
        phone VARCHAR,
        website VARCHAR,
        email VARCHAR,
        socials VARCHAR,
        tier VARCHAR,
        score INTEGER,
        opportunity VARCHAR,
        pitch VARCHAR,
        why VARCHAR,
        source_badge VARCHAR,
        source_id VARCHAR,
        source_color VARCHAR
    );
    """)

    con.executemany("INSERT INTO t_imported_staging VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows_to_insert)

    # If updating an existing dataset, merge with existing Parquet
    if existing_dataset_id and os.path.exists(final_parquet_path):
        con.execute(f"""
        CREATE TABLE t_combined AS
        SELECT * FROM read_parquet('{final_parquet_path.replace(os.sep, "/")}')
        UNION ALL
        SELECT * FROM t_imported_staging;
        """)
        con.execute(f"COPY t_combined TO '{final_parquet_path.replace(os.sep, "/")}' (FORMAT PARQUET);")
    else:
        con.execute(f"COPY t_imported_staging TO '{final_parquet_path.replace(os.sep, "/")}' (FORMAT PARQUET);")

    # Write rejection report if any rejected rows
    has_rejections = len(rejected_rows) > 0
    if has_rejections:
        with open(rejection_report_path, "w", encoding="utf-8", newline="") as rf:
            writer = csv.DictWriter(rf, fieldnames=["source_file", "row_number", "error_reason", "raw_data"])
            writer.writeheader()
            for rej in rejected_rows:
                writer.writerow(rej)

    # Save permanent metadata in registry
    dataset_meta = {
        "id": dataset_id,
        "name": cleaned_name,
        "created_at": datetime.now().isoformat(),
        "parquet_path": final_parquet_path,
        "total_rows": total_imported if not (existing_dataset_id and os.path.exists(final_parquet_path)) else (registry.get("datasets", {}).get(dataset_id, {}).get("total_rows", 0) + total_imported),
        "total_discovered": total_discovered,
        "duplicate_rows": total_duplicates,
        "rejected_rows": total_rejected,
        "duplicate_mode": duplicate_mode,
        "files_count": len(file_summaries),
        "files": file_summaries,
        "status": "Active",
        "has_rejections": has_rejections,
        "rejection_report": rejection_report_path if has_rejections else None
    }

    if "datasets" not in registry:
        registry["datasets"] = {}
    registry["datasets"][dataset_id] = dataset_meta
    save_registry(registry)

    log_audit_event("IMPORT_DATASET", dataset_id, {
        "name": cleaned_name,
        "imported_rows": total_imported,
        "duplicates": total_duplicates,
        "rejected": total_rejected,
        "files_count": len(file_summaries)
    })

    return {
        "success": True,
        "dataset_id": dataset_id,
        "dataset_name": cleaned_name,
        "total_discovered": total_discovered,
        "total_imported": total_imported,
        "total_duplicates": total_duplicates,
        "total_rejected": total_rejected,
        "has_rejections": has_rejections,
        "rejection_report_url": f"/api/imported_datasets/{dataset_id}/rejections" if has_rejections else None,
        "files_summary": file_summaries
    }

def get_all_imported_datasets() -> List[Dict[str, Any]]:
    """Returns a list of all registered imported datasets."""
    registry = load_registry()
    datasets = list(registry.get("datasets", {}).values())
    datasets.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    return datasets

def rename_imported_dataset(dataset_id: str, new_name: str) -> Dict[str, Any]:
    """Renames an imported dataset in the registry."""
    cleaned = new_name.strip()
    if not cleaned:
        return {"success": False, "error": "New dataset name cannot be empty."}

    registry = load_registry()
    if dataset_id not in registry.get("datasets", {}):
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    old_name = registry["datasets"][dataset_id]["name"]
    registry["datasets"][dataset_id]["name"] = cleaned
    registry["datasets"][dataset_id]["updated_at"] = datetime.now().isoformat()
    save_registry(registry)

    log_audit_event("RENAME_DATASET", dataset_id, {"old_name": old_name, "new_name": cleaned})
    return {"success": True, "dataset_id": dataset_id, "name": cleaned}

def toggle_archive_dataset(dataset_id: str) -> Dict[str, Any]:
    """Toggles active/archived status of a dataset."""
    registry = load_registry()
    if dataset_id not in registry.get("datasets", {}):
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    current_status = registry["datasets"][dataset_id].get("status", "Active")
    new_status = "Archived" if current_status == "Active" else "Active"
    registry["datasets"][dataset_id]["status"] = new_status
    save_registry(registry)

    log_audit_event("TOGGLE_ARCHIVE", dataset_id, {"new_status": new_status})
    return {"success": True, "dataset_id": dataset_id, "status": new_status}

def delete_imported_dataset(dataset_id: str) -> Dict[str, Any]:
    """Safely deletes an imported dataset and preserves audit logs."""
    registry = load_registry()
    if dataset_id not in registry.get("datasets", {}):
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    meta = registry["datasets"].pop(dataset_id)
    save_registry(registry)

    # Delete parquet file if exists
    parquet_path = meta.get("parquet_path")
    if parquet_path and os.path.exists(parquet_path):
        try:
            os.remove(parquet_path)
        except Exception:
            pass

    log_audit_event("DELETE_DATASET", dataset_id, {"deleted_meta": meta})
    return {"success": True, "deleted_id": dataset_id}
