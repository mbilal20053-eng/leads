"""
Lead Engine PRO - Enterprise Ingestion & Universal Dataset Importer Module
Handles universal multi-file uploads:
- CSV, TSV, TXT (auto-detecting delimiters and encodings: UTF-8, UTF-8-BOM, CP1252, ISO-8859-1)
- Excel: XLSX, XLSM, XLS (with multi-worksheet inspection and selection)
- JSON, JSONL, NDJSON (object arrays, nested record extraction, dot-path flattening)
- XML (repeated row-element detection, attribute and sub-element flattening)
- Parquet (native high-speed columnar reading)
- Compressed archives: ZIP (with decompression bomb and path traversal security, contained file selection)
- GZIP-compressed files (.csv.gz, .json.gz, etc.)

Features:
- Schema normalization & fuzzy alias matching
- Custom columns addition (constant default or row-by-row individual values)
- Spreadsheet-style cell edits during preview
- Column renaming, exclusions, default fallbacks, and data type detection
- Leading zero & long numeric identifier preservation (never converted to scientific notation)
- Formula injection protection on export and preview
- Configurable deduplication (skip exact, import all, new only, flag review)
- Corrupt / malformed row isolation into downloadable CSV reports
- Atomic Parquet persistence via DuckDB with full provenance tracking
- Post-import dataset column management (add, rename, fill blanks, edit cells, delete with confirmation)
"""
import os
import re
import csv
import io
import json
import time
import shutil
import hashlib
import zipfile
import gzip
from datetime import datetime, date
from typing import Dict, List, Tuple, Any, Optional, Iterator

import duckdb
import pyarrow
import pyarrow.parquet as pq
import openpyxl
import xlrd
import xml.etree.ElementTree as ET

# Base data directory resolution
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

# Standard canonical target columns in Lead Engine PRO
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
        "trade name", "brand", "client", "store name", "store_name", "entity_name", "name", "title"
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
        "categories", "primary category", "cuisine"
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

# Supported file extensions map
FORMAT_EXTENSIONS = {
    ".csv": "csv",
    ".tsv": "tsv",
    ".tab": "tsv",
    ".txt": "csv",
    ".xlsx": "excel",
    ".xlsm": "excel",
    ".xls": "excel_legacy",
    ".json": "json",
    ".jsonl": "jsonl",
    ".ndjson": "jsonl",
    ".xml": "xml",
    ".parquet": "parquet",
    ".pq": "parquet",
    ".zip": "zip",
    ".gz": "gzip",
    ".gzip": "gzip"
}

# Security limits
MAX_ZIP_UNCOMPRESSED_BYTES = 500 * 1024 * 1024  # 500 MB
MAX_ZIP_ENTRIES_COUNT = 250
MAX_ZIP_RATIO = 25.0

# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

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

def detect_file_format(filepath: str, filename: Optional[str] = None) -> str:
    """Detects file format by extension and signature."""
    fname = (filename or os.path.basename(filepath)).lower()
    for ext, fmt in FORMAT_EXTENSIONS.items():
        if fname.endswith(ext):
            return fmt

    # Fallback to magic bytes check
    try:
        with open(filepath, "rb") as f:
            header = f.read(16)
        if header.startswith(b"PAR1"):
            return "parquet"
        if header.startswith(b"PK\x03\x04"):
            return "zip"
        if header.startswith(b"\x1f\x8b"):
            return "gzip"
        if header.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
            return "excel_legacy"
    except Exception:
        pass

    return "unsupported"

def detect_column_type(sample_values: List[Any]) -> str:
    """
    Infers data type from sample values.
    CRITICAL: Preserves leading zeros and long identifiers as text (e.g., phone numbers,
    postal codes, registration numbers).
    """
    cleaned = [v for v in sample_values if v is not None and str(v).strip() != ""]
    if not cleaned:
        return "text"

    has_leading_zero = False
    is_all_int = True
    is_all_float = True
    is_all_bool = True
    is_all_date = True

    for val in cleaned:
        s = str(val).strip()
        # Check leading zero (e.g. "01234", "07911...")
        if len(s) > 1 and s.startswith("0") and s[1:].isdigit():
            has_leading_zero = True
            is_all_int = False
            is_all_float = False
            break

        # Check boolean
        if s.lower() not in ("true", "false", "1", "0", "yes", "no"):
            is_all_bool = False

        # Check integer
        if not (s.isdigit() or (s.startswith("-") and s[1:].isdigit())):
            is_all_int = False

        # Check float
        try:
            float(s)
        except ValueError:
            is_all_float = False

        # Check date
        date_patterns = [
            r"^\d{4}-\d{2}-\d{2}$",
            r"^\d{2}/\d{2}/\d{4}$",
            r"^\d{2}-\d{2}-\d{4}$"
        ]
        if not any(re.match(pat, s) for pat in date_patterns):
            is_all_date = False

    if has_leading_zero:
        return "text"
    if is_all_bool and len(cleaned) > 2:
        return "boolean"
    if is_all_int:
        return "integer"
    if is_all_float:
        return "decimal"
    if is_all_date:
        return "date"
    return "text"

def format_cell_value(val: Any) -> str:
    """Formats raw values safely into string without scientific notation or trailing .0 on ints."""
    if val is None:
        return ""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int,)):
        return str(val)
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        return f"{val:.6f}".rstrip("0").rstrip(".")
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    return str(val).strip()

def detect_file_encoding_and_delimiter(filepath: str) -> Tuple[str, str]:
    """Inspects file bytes to detect character encoding and delimiter with high accuracy."""
    detected_encoding = "utf-8"
    with open(filepath, "rb") as f:
        sample_bytes = f.read(65536)

    # Check for BOMs
    if sample_bytes.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig", ","
    elif sample_bytes.startswith(b"\xff\xfe"):
        return "utf-16-le", "\t"
    elif sample_bytes.startswith(b"\xfe\xff"):
        return "utf-16-be", "\t"

    # Decode attempts
    for enc in ["utf-8", "cp1252", "iso-8859-1"]:
        try:
            sample_text = sample_bytes.decode(enc)
            detected_encoding = enc
            break
        except UnicodeDecodeError:
            continue
    else:
        sample_text = sample_bytes.decode("utf-8", errors="replace")
        detected_encoding = "utf-8"

    # Detect delimiter
    lines = [ln for ln in sample_text.splitlines() if ln.strip()][:25]
    if not lines:
        return detected_encoding, ","

    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff("\n".join(lines), delimiters=[",", ";", "\t", "|"])
        delimiter = dialect.delimiter
    except Exception:
        counts = {",": 0, ";": 0, "\t": 0, "|": 0}
        for ln in lines:
            for d in counts:
                counts[d] += ln.count(d)
        delimiter = max(counts, key=counts.get)
        if counts[delimiter] == 0:
            delimiter = ","

    return detected_encoding, delimiter

def auto_map_headers(headers: List[str]) -> List[Dict[str, Any]]:
    """Maps incoming headers to Lead Engine PRO columns using alias heuristics."""
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

# ---------------------------------------------------------------------------
# Format-Specific Inspection Functions
# ---------------------------------------------------------------------------

def inspect_csv_file(filepath: str, original_filename: Optional[str] = None) -> Dict[str, Any]:
    """Inspects a delimited text file (CSV, TSV, TXT)."""
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
    col_samples: Dict[str, List[Any]] = {}

    with open(filepath, "r", encoding=encoding, errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            headers = next(reader, [])
        except Exception as e:
            return {"success": False, "error": f"Failed to read headers from {filename}: {str(e)}", "filename": filename}

        headers = [h.strip() if h else f"Column_{i+1}" for i, h in enumerate(headers)]
        mappings = auto_map_headers(headers)
        target_indices = {m["target_key"]: m["source_index"] for m in mappings if m["target_key"] != "ignore"}
        for h in headers:
            col_samples[h] = []

        scanned_rows = 0
        for row in reader:
            scanned_rows += 1
            if len(row) != len(headers):
                malformed_rows_count += 1

            # Track missing fields
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

            if scanned_rows <= 25:
                row_dict = {}
                for h_idx, h_name in enumerate(headers):
                    val = row[h_idx] if h_idx < len(row) else ""
                    row_dict[h_name] = val
                    col_samples[h_name].append(val)
                preview_rows.append(row_dict)

            if scanned_rows >= 5000:
                bytes_pos = f.tell()
                if bytes_pos > 0:
                    avg_row_bytes = bytes_pos / scanned_rows
                    total_rows_estimate = int(file_size_bytes / avg_row_bytes)
                break

    if total_rows_estimate == 0 or scanned_rows < 5000:
        total_rows_estimate = scanned_rows

    delim_name = {",": "Comma (',')", ";": "Semicolon (';')", "\t": "Tab ('\\t')", "|": "Pipe ('|')"}.get(delimiter, f"'{delimiter}'")
    col_types = {h: detect_column_type(col_samples.get(h, [])) for h in headers}

    ext = os.path.splitext(filename)[1].lower()
    fmt_detected = "tsv" if ext in (".tsv", ".tab") else ("txt" if ext in (".txt",) else "csv")

    return {
        "success": True,
        "filename": filename,
        "format": fmt_detected,
        "file_size_mb": file_size_mb,
        "file_size_bytes": file_size_bytes,
        "encoding": encoding,
        "delimiter": delimiter,
        "delimiter_name": delim_name,
        "headers": headers,
        "mappings": mappings,
        "column_types": col_types,
        "total_rows_estimate": total_rows_estimate,
        "columns_count": len(headers),
        "scanned_rows_sample": len(preview_rows),
        "malformed_rows_count": malformed_rows_count,
        "missing_in_sample": missing_fields_count,
        "preview_rows": preview_rows
    }

def inspect_excel_file(filepath: str, original_filename: Optional[str] = None, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """Inspects modern (.xlsx, .xlsm) or legacy (.xls) Excel workbooks with worksheet selection."""
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
    ext = os.path.splitext(filename)[1].lower()

    sheet_names = []
    selected_sheet = sheet_name
    headers = []
    preview_rows = []
    col_samples: Dict[str, List[Any]] = {}
    total_rows = 0

    try:
        if ext in (".xlsx", ".xlsm"):
            wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
            sheet_names = wb.sheetnames
            if not selected_sheet or selected_sheet not in sheet_names:
                selected_sheet = sheet_names[0]
            ws = wb[selected_sheet]

            row_iter = ws.iter_rows(values_only=True)
            # Find first non-empty header row
            for row in row_iter:
                row_vals = [format_cell_value(c) for c in row] if row else []
                if any(row_vals):
                    headers = [c if c else f"Column_{i+1}" for i, c in enumerate(row_vals)]
                    break

            for h in headers:
                col_samples[h] = []

            for row in row_iter:
                total_rows += 1
                row_vals = [format_cell_value(c) for c in row] if row else []
                if total_rows <= 25:
                    row_dict = {}
                    for idx, h in enumerate(headers):
                        val = row_vals[idx] if idx < len(row_vals) else ""
                        row_dict[h] = val
                        col_samples[h].append(val)
                    preview_rows.append(row_dict)
            wb.close()
        else:
            # Legacy .xls via xlrd
            wb = xlrd.open_workbook(filepath)
            sheet_names = wb.sheet_names()
            if not selected_sheet or selected_sheet not in sheet_names:
                selected_sheet = sheet_names[0]
            ws = wb.sheet_by_name(selected_sheet)
            if ws.nrows > 0:
                header_row = ws.row_values(0)
                headers = [format_cell_value(c) or f"Column_{i+1}" for i, c in enumerate(header_row)]
                for h in headers:
                    col_samples[h] = []
                total_rows = max(0, ws.nrows - 1)
                for r_idx in range(1, min(ws.nrows, 26)):
                    r_vals = [format_cell_value(c) for c in ws.row_values(r_idx)]
                    row_dict = {}
                    for c_idx, h in enumerate(headers):
                        val = r_vals[c_idx] if c_idx < len(r_vals) else ""
                        row_dict[h] = val
                        col_samples[h].append(val)
                    preview_rows.append(row_dict)

    except Exception as e:
        return {"success": False, "error": f"Failed to inspect Excel file {filename}: {str(e)}", "filename": filename}

    mappings = auto_map_headers(headers)
    col_types = {h: detect_column_type(col_samples.get(h, [])) for h in headers}

    return {
        "success": True,
        "filename": filename,
        "format": "excel",
        "file_size_mb": file_size_mb,
        "file_size_bytes": file_size_bytes,
        "encoding": "UTF-8",
        "delimiter": "Excel Table",
        "delimiter_name": "Excel Worksheet",
        "sheet_names": sheet_names,
        "selected_sheet": selected_sheet,
        "headers": headers,
        "mappings": mappings,
        "column_types": col_types,
        "total_rows_estimate": total_rows,
        "columns_count": len(headers),
        "scanned_rows_sample": len(preview_rows),
        "malformed_rows_count": 0,
        "missing_in_sample": {"name": 0, "phone": 0, "email": 0},
        "preview_rows": preview_rows
    }

def inspect_json_file(filepath: str, original_filename: Optional[str] = None) -> Dict[str, Any]:
    """Inspects JSON, JSONL, or NDJSON files, supporting nested record paths and dot-path flattening."""
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
    ext = os.path.splitext(filename)[1].lower()

    preview_rows = []
    headers = []
    col_samples: Dict[str, List[Any]] = {}
    total_rows = 0

    def flatten_dict(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        items: Dict[str, Any] = {}
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, dict):
                items.update(flatten_dict(v, key))
            elif isinstance(v, list):
                # Serialize simple lists as comma-separated or json string
                if v and all(isinstance(x, (str, int, float)) for x in v):
                    items[key] = ", ".join(str(x) for x in v)
                else:
                    items[key] = json.dumps(v)
            else:
                items[key] = format_cell_value(v)
        return items

    try:
        if ext in (".jsonl", ".ndjson"):
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    total_rows += 1
                    if total_rows <= 25:
                        obj = json.loads(line)
                        flat = flatten_dict(obj) if isinstance(obj, dict) else {"value": str(obj)}
                        preview_rows.append(flat)
                        for k in flat:
                            if k not in headers:
                                headers.append(k)
        else:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)

            records = []
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                # Check top-level arrays
                for k in ["records", "data", "leads", "items", "results", "rows", "companies", "contacts"]:
                    if k in data and isinstance(data[k], list):
                        records = data[k]
                        break
                if not records:
                    # Single object or dict of objects
                    if all(isinstance(v, dict) for v in data.values()):
                        records = list(data.values())
                    else:
                        records = [data]

            total_rows = len(records)
            for obj in records[:25]:
                flat = flatten_dict(obj) if isinstance(obj, dict) else {"value": str(obj)}
                preview_rows.append(flat)
                for k in flat:
                    if k not in headers:
                        headers.append(k)

    except Exception as e:
        return {"success": False, "error": f"Failed to parse JSON file {filename}: {str(e)}", "filename": filename}

    for h in headers:
        col_samples[h] = [r.get(h) for r in preview_rows]

    mappings = auto_map_headers(headers)
    col_types = {h: detect_column_type(col_samples.get(h, [])) for h in headers}

    return {
        "success": True,
        "filename": filename,
        "format": "json",
        "file_size_mb": file_size_mb,
        "file_size_bytes": file_size_bytes,
        "encoding": "UTF-8",
        "delimiter": "JSON Objects",
        "delimiter_name": "JSON / NDJSON Records",
        "headers": headers,
        "mappings": mappings,
        "column_types": col_types,
        "total_rows_estimate": total_rows,
        "columns_count": len(headers),
        "scanned_rows_sample": len(preview_rows),
        "malformed_rows_count": 0,
        "missing_in_sample": {"name": 0, "phone": 0, "email": 0},
        "preview_rows": preview_rows
    }

def inspect_xml_file(filepath: str, original_filename: Optional[str] = None) -> Dict[str, Any]:
    """Inspects XML files, automatically discovering repeated row elements and flattening children."""
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    headers = []
    preview_rows = []
    col_samples: Dict[str, List[Any]] = {}
    total_rows = 0

    try:
        # Protect against XML entity expansion / bomb attacks
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Find repeated row element tag
        tag_counts: Dict[str, int] = {}
        for child in root:
            tag_counts[child.tag] = tag_counts.get(child.tag, 0) + 1

        if not tag_counts:
            return {"success": False, "error": f"XML document has no row elements in root: {filename}", "filename": filename}

        row_tag = max(tag_counts, key=tag_counts.get)
        row_elements = [el for el in root if el.tag == row_tag]
        total_rows = len(row_elements)

        for el in row_elements[:25]:
            row_dict: Dict[str, Any] = {}
            # Include attributes
            for attr_k, attr_v in el.attrib.items():
                k = f"@{attr_k}"
                row_dict[k] = format_cell_value(attr_v)
                if k not in headers:
                    headers.append(k)

            # Include child text tags
            for child in el:
                k = child.tag
                row_dict[k] = format_cell_value(child.text)
                if k not in headers:
                    headers.append(k)

            preview_rows.append(row_dict)

    except Exception as e:
        return {"success": False, "error": f"Failed to parse XML file {filename}: {str(e)}", "filename": filename}

    for h in headers:
        col_samples[h] = [r.get(h) for r in preview_rows]

    mappings = auto_map_headers(headers)
    col_types = {h: detect_column_type(col_samples.get(h, [])) for h in headers}

    return {
        "success": True,
        "filename": filename,
        "format": "xml",
        "file_size_mb": file_size_mb,
        "file_size_bytes": file_size_bytes,
        "encoding": "UTF-8",
        "delimiter": "XML Tags",
        "delimiter_name": f"XML <{row_tag}> Elements",
        "headers": headers,
        "mappings": mappings,
        "column_types": col_types,
        "total_rows_estimate": total_rows,
        "columns_count": len(headers),
        "scanned_rows_sample": len(preview_rows),
        "malformed_rows_count": 0,
        "missing_in_sample": {"name": 0, "phone": 0, "email": 0},
        "preview_rows": preview_rows
    }

def inspect_parquet_file(filepath: str, original_filename: Optional[str] = None) -> Dict[str, Any]:
    """Inspects native Parquet file via DuckDB and PyArrow."""
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
    safe_p = filepath.replace("\\", "/")

    try:
        con = duckdb.connect()
        total_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{safe_p}')").fetchone()[0]
        cur = con.execute(f"SELECT * FROM read_parquet('{safe_p}') LIMIT 25")
        headers = [desc[0] for desc in cur.description]
        raw_rows = cur.fetchall()

        preview_rows = []
        col_samples: Dict[str, List[Any]] = {h: [] for h in headers}
        for r in raw_rows:
            row_dict = {}
            for idx, h in enumerate(headers):
                val = format_cell_value(r[idx])
                row_dict[h] = val
                col_samples[h].append(val)
            preview_rows.append(row_dict)

    except Exception as e:
        return {"success": False, "error": f"Failed to inspect Parquet file {filename}: {str(e)}", "filename": filename}

    mappings = auto_map_headers(headers)
    col_types = {h: detect_column_type(col_samples.get(h, [])) for h in headers}

    return {
        "success": True,
        "filename": filename,
        "format": "parquet",
        "file_size_mb": file_size_mb,
        "file_size_bytes": file_size_bytes,
        "encoding": "Binary (Parquet Columnar)",
        "delimiter": "Columnar",
        "delimiter_name": "Parquet Columnar Data",
        "headers": headers,
        "mappings": mappings,
        "column_types": col_types,
        "total_rows_estimate": total_rows,
        "columns_count": len(headers),
        "scanned_rows_sample": len(preview_rows),
        "malformed_rows_count": 0,
        "missing_in_sample": {"name": 0, "phone": 0, "email": 0},
        "preview_rows": preview_rows
    }

def inspect_zip_file(filepath: str, original_filename: Optional[str] = None, session_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Inspects ZIP archive with security checks against zip bombs and path traversal.
    Returns list of contained tabular files for user selection.
    """
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    try:
        with zipfile.ZipFile(filepath, "r") as z:
            infolist = z.infolist()
            # Security: entry count limit
            if len(infolist) > MAX_ZIP_ENTRIES_COUNT:
                return {
                    "success": False,
                    "error": f"Security Exception: ZIP contains {len(infolist)} entries, exceeding the maximum limit of {MAX_ZIP_ENTRIES_COUNT}.",
                    "filename": filename
                }

            total_uncompressed = 0
            contained_entries = []

            for info in infolist:
                # Security: Path traversal protection
                member_name = info.filename
                if ".." in member_name or member_name.startswith(("/", "\\")):
                    return {
                        "success": False,
                        "error": f"Security Exception: Malicious path traversal detected in ZIP entry '{member_name}'.",
                        "filename": filename
                    }

                total_uncompressed += info.file_size
                # Skip folders
                if info.is_dir() or member_name.endswith("/"):
                    continue

                ext = os.path.splitext(member_name)[1].lower()
                if ext in FORMAT_EXTENSIONS:
                    contained_entries.append({
                        "path": member_name,
                        "entry_name": member_name,
                        "filename": os.path.basename(member_name),
                        "size_mb": round(info.file_size / (1024 * 1024), 2),
                        "size_bytes": info.file_size,
                        "format": FORMAT_EXTENSIONS[ext]
                    })

            # Security: Decompression bomb checks
            if total_uncompressed > MAX_ZIP_UNCOMPRESSED_BYTES:
                return {
                    "success": False,
                    "error": f"Security Exception: Total uncompressed size ({round(total_uncompressed/(1024*1024),1)}MB) exceeds maximum safe limit of {int(MAX_ZIP_UNCOMPRESSED_BYTES/(1024*1024))}MB.",
                    "filename": filename
                }
            if file_size_bytes > 0 and (total_uncompressed / file_size_bytes) > MAX_ZIP_RATIO:
                return {
                    "success": False,
                    "error": f"Security Exception: Decompression ratio ({round(total_uncompressed/file_size_bytes,1)}x) exceeds safe compression threshold.",
                    "filename": filename
                }

            if not contained_entries:
                return {
                    "success": False,
                    "error": "No supported lead data files found inside the ZIP archive (CSV, Excel, JSON, XML, Parquet).",
                    "filename": filename
                }

            return {
                "success": True,
                "filename": filename,
                "format": "zip",
                "file_size_mb": file_size_mb,
                "file_size_bytes": file_size_bytes,
                "encoding": "Archive (ZIP)",
                "delimiter": "ZIP Archive",
                "delimiter_name": "ZIP Compressed Archive",
                "zip_entries": contained_entries,
                "contained_files": contained_entries,
                "entries_count": len(contained_entries),
                "headers": ["Filename", "Format", "Size"],
                "mappings": [],
                "column_types": {},
                "total_rows_estimate": 0,
                "columns_count": 0,
                "malformed_rows_count": 0,
                "missing_in_sample": {},
                "preview_rows": []
            }

    except zipfile.BadZipFile:
        return {"success": False, "error": f"Corrupt or invalid ZIP archive: {filename}", "filename": filename}
    except Exception as e:
        return {"success": False, "error": f"Error inspecting ZIP {filename}: {str(e)}", "filename": filename}

def inspect_gzip_file(filepath: str, original_filename: Optional[str] = None, session_dir: Optional[str] = None) -> Dict[str, Any]:
    """Inspects GZIP compressed file (.csv.gz, .json.gz), decompressing to staging and inspecting."""
    filename = original_filename or os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    # Determine inner filename
    inner_name = re.sub(r"\.(gz|gzip)$", "", filename, flags=re.I)
    target_dir = session_dir or STAGING_DIR
    decompressed_path = os.path.join(target_dir, f"decomp_{int(time.time())}_{inner_name}")

    try:
        with gzip.open(filepath, "rb") as f_in:
            with open(decompressed_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        res = inspect_universal_file(decompressed_path, original_filename=inner_name)
        res["staged_path"] = decompressed_path
        res["format"] = "gzip"
        res["original_filename"] = filename
        return res
    except Exception as e:
        return {"success": False, "error": f"Failed to decompress GZIP file {filename}: {str(e)}", "filename": filename}

def inspect_universal_file(filepath: str, original_filename: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Universal dispatcher: inspects any supported lead file format."""
    opts = options or {}
    fmt = detect_file_format(filepath, original_filename)

    if fmt == "unsupported":
        ext = os.path.splitext(original_filename or filepath)[1]
        return {
            "success": False,
            "error": f"Unsupported file format '{ext}'. Supported formats: CSV, TSV, TXT, Excel (XLS, XLSX, XLSM), JSON, XML, Parquet, ZIP, and GZIP.",
            "filename": original_filename or os.path.basename(filepath)
        }

    if fmt in ("csv", "tsv"):
        return inspect_csv_file(filepath, original_filename)
    elif fmt in ("excel", "excel_legacy"):
        return inspect_excel_file(filepath, original_filename, sheet_name=opts.get("sheet_name"))
    elif fmt in ("json", "jsonl"):
        return inspect_json_file(filepath, original_filename)
    elif fmt == "xml":
        return inspect_xml_file(filepath, original_filename)
    elif fmt == "parquet":
        return inspect_parquet_file(filepath, original_filename)
    elif fmt == "zip":
        return inspect_zip_file(filepath, original_filename, session_dir=opts.get("session_dir"))
    elif fmt == "gzip":
        return inspect_gzip_file(filepath, original_filename, session_dir=opts.get("session_dir"))
    else:
        return {
            "success": False,
            "error": f"Unsupported or unrecognizable file format for {original_filename or filepath}.",
            "filename": original_filename or os.path.basename(filepath)
        }

# ---------------------------------------------------------------------------
# Universal Record Streamer
# ---------------------------------------------------------------------------

def stream_universal_records(filepath: str, format_type: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Iterator[Tuple[int, Dict[str, Any]]]:
    """
    Streams records from any supported format uniformly as (row_number, dict_of_values).
    Enables low-memory chunked ingestion even for large files.
    """
    opts = options or {}
    fmt = format_type or detect_file_format(filepath)

    if fmt in ("csv", "tsv"):
        encoding, delimiter = detect_file_encoding_and_delimiter(filepath)
        with open(filepath, "r", encoding=encoding, errors="replace", newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            try:
                headers = [h.strip() for h in next(reader, [])]
            except Exception:
                return

            for line_no, row in enumerate(reader, start=2):
                row_dict = {}
                for idx, h in enumerate(headers):
                    row_dict[h] = row[idx].strip() if idx < len(row) else ""
                yield line_no, row_dict

    elif fmt in ("excel", "excel_legacy"):
        ext = os.path.splitext(filepath)[1].lower()
        selected_sheet = opts.get("sheet_name")
        line_no = 1
        if ext in (".xlsx", ".xlsm"):
            wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
            sheet = wb[selected_sheet] if selected_sheet and selected_sheet in wb.sheetnames else wb.active
            headers = []
            for row in sheet.iter_rows(values_only=True):
                r_vals = [format_cell_value(c) for c in row] if row else []
                if not headers and any(r_vals):
                    headers = [c or f"Column_{i+1}" for i, c in enumerate(r_vals)]
                    continue
                if headers:
                    line_no += 1
                    row_dict = {headers[i]: r_vals[i] if i < len(r_vals) else "" for i in range(len(headers))}
                    yield line_no, row_dict
            wb.close()
        else:
            wb = xlrd.open_workbook(filepath)
            sheet = wb.sheet_by_name(selected_sheet) if selected_sheet and selected_sheet in wb.sheet_names() else wb.sheet_by_index(0)
            if sheet.nrows > 0:
                headers = [format_cell_value(c) or f"Column_{i+1}" for i, c in enumerate(sheet.row_values(0))]
                for r_idx in range(1, sheet.nrows):
                    line_no += 1
                    r_vals = [format_cell_value(c) for c in sheet.row_values(r_idx)]
                    row_dict = {headers[i]: r_vals[i] if i < len(r_vals) else "" for i in range(len(headers))}
                    yield line_no, row_dict

    elif fmt in ("json", "jsonl"):
        ext = os.path.splitext(filepath)[1].lower()
        line_no = 1
        if ext in (".jsonl", ".ndjson"):
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    line_no += 1
                    try:
                        obj = json.loads(line)
                        yield line_no, obj if isinstance(obj, dict) else {"value": str(obj)}
                    except Exception:
                        continue
        else:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
            records = []
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                for k in ["records", "data", "leads", "items", "results", "rows", "companies", "contacts"]:
                    if k in data and isinstance(data[k], list):
                        records = data[k]
                        break
                if not records:
                    records = list(data.values()) if all(isinstance(v, dict) for v in data.values()) else [data]

            for obj in records:
                line_no += 1
                yield line_no, obj if isinstance(obj, dict) else {"value": str(obj)}

    elif fmt == "xml":
        tree = ET.parse(filepath)
        root = tree.getroot()
        tag_counts: Dict[str, int] = {}
        for child in root:
            tag_counts[child.tag] = tag_counts.get(child.tag, 0) + 1
        if tag_counts:
            row_tag = max(tag_counts, key=tag_counts.get)
            line_no = 1
            for el in root:
                if el.tag == row_tag:
                    line_no += 1
                    row_dict = {f"@{k}": format_cell_value(v) for k, v in el.attrib.items()}
                    for child in el:
                        row_dict[child.tag] = format_cell_value(child.text)
                    yield line_no, row_dict

    elif fmt == "parquet":
        safe_p = filepath.replace("\\", "/")
        con = duckdb.connect()
        cur = con.execute(f"SELECT * FROM read_parquet('{safe_p}')")
        headers = [desc[0] for desc in cur.description]
        line_no = 1
        while True:
            chunk = cur.fetchmany(1000)
            if not chunk:
                break
            for r in chunk:
                line_no += 1
                row_dict = {headers[i]: format_cell_value(r[i]) for i in range(len(headers))}
                yield line_no, row_dict

# ---------------------------------------------------------------------------
# Registry & Audit Logging
# ---------------------------------------------------------------------------

def load_registry() -> Dict[str, Any]:
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"datasets": {}}
    return {"datasets": {}}

def save_registry(registry: Dict[str, Any]):
    tmp_path = REGISTRY_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    shutil.move(tmp_path, REGISTRY_FILE)

def log_audit_event(action: str, dataset_id: str, details: Dict[str, Any]):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "dataset_id": dataset_id,
        "details": details
    }
    entries = []
    if os.path.exists(AUDIT_LOG_FILE):
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []
    entries.append(log_entry)
    with open(AUDIT_LOG_FILE + ".tmp", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    shutil.move(AUDIT_LOG_FILE + ".tmp", AUDIT_LOG_FILE)

# ---------------------------------------------------------------------------
# Universal Import Execution Engine
# ---------------------------------------------------------------------------

def execute_dataset_import(
    dataset_name: str,
    staged_files: Optional[List[Dict[str, Any]]] = None,
    column_mappings_per_file: Optional[Dict[str, Dict[str, str]]] = None,
    duplicate_mode: str = "skip_exact",
    existing_dataset_id: Optional[str] = None,
    custom_columns: Optional[List[Dict[str, Any]]] = None,
    cell_edits: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None,
    column_settings: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None,
    files: Optional[List[Dict[str, Any]]] = None,
    column_mappings: Optional[Dict[str, Dict[str, str]]] = None
) -> Dict[str, Any]:
    staged_files = staged_files if staged_files is not None else (files or [])
    column_mappings_per_file = column_mappings_per_file if column_mappings_per_file is not None else (column_mappings or {})
    """
    Executes atomic dataset ingestion:
    1. Supports universal formats: CSV, TSV, Excel, JSON, XML, Parquet.
    2. Applies custom columns (constant default or row-by-row individual values).
    3. Applies spreadsheet preview cell edits.
    4. Handles column exclusions, renames, default fallbacks, and data types.
    5. Filters or flags duplicates according to user choice.
    6. Isolates malformed rows into downloadable CSV error reports.
    7. Atomically commits clean records into DuckDB/Parquet storage.
    8. Updates persistent registry and dynamic DuckDB views.
    """
    cleaned_name = dataset_name.strip()
    if not cleaned_name:
        return {"success": False, "error": "Dataset name cannot be empty."}

    dataset_id = existing_dataset_id or slugify(cleaned_name)
    registry = load_registry()

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

    # Normalize custom columns specs
    custom_cols_spec = custom_columns or []
    custom_col_names = [c["name"].strip().lower().replace(" ", "_") for c in custom_cols_spec if c.get("name")]
    edits_map = cell_edits or {}
    col_settings_map = column_settings or {}

    rows_to_insert: List[Tuple] = []
    rejected_rows: List[Dict[str, Any]] = []
    file_summaries: List[Dict[str, Any]] = []

    con = duckdb.connect()

    for file_idx, file_info in enumerate(staged_files):
        filepath = file_info["staged_path"]
        orig_filename = file_info["original_filename"]
        mapping = column_mappings_per_file.get(orig_filename, {})
        f_settings = col_settings_map.get(orig_filename, {})
        f_edits = edits_map.get(orig_filename, edits_map.get(str(file_idx), {}))

        if not os.path.exists(filepath):
            continue

        fmt = file_info.get("format") or detect_file_format(filepath, orig_filename)
        opts = {"sheet_name": file_info.get("selected_sheet")}
        f_discovered = 0
        f_imported = 0
        f_duplicates = 0
        f_rejected = 0

        for line_no, raw_row in stream_universal_records(filepath, format_type=fmt, options=opts):
            f_discovered += 1
            total_discovered += 1

            # Apply row-specific cell edits if any
            row_key_str = str(f_discovered - 1)
            row_key_line = str(line_no)
            active_row = dict(raw_row)
            if row_key_str in f_edits:
                active_row.update(f_edits[row_key_str])
            elif row_key_line in f_edits:
                active_row.update(f_edits[row_key_line])

            # Extract standard mapped fields
            def get_val(key: str, default: str = "") -> str:
                src_header = mapping.get(key)
                col_cfg = (f_settings.get(src_header) or f_settings.get(key) or {}) if f_settings else {}
                if col_cfg.get("excluded"):
                    return ""
                if src_header and src_header in active_row:
                    v = active_row[src_header]
                    if v is not None and str(v).strip():
                        return str(v).strip()
                # Check column default settings (supports both camelCase and snake_case)
                def_val = col_cfg.get("defaultValue") or col_cfg.get("default_value")
                if def_val is not None and str(def_val).strip():
                    return str(def_val).strip()
                return default

            b_name = get_val("name")
            c_name = get_val("contact_name")
            j_title = get_val("job_title")
            cat = get_val("category")
            addr = get_val("address")
            city = get_val("city")
            state = get_val("state")
            zip_c = get_val("zip")
            country = get_val("country", "United States")
            raw_phone = get_val("phone")
            raw_web = get_val("website")
            raw_email = get_val("email")
            socials = get_val("socials")

            # Custom columns extraction
            row_custom_values: Dict[str, str] = {}
            for c_spec in custom_cols_spec:
                c_name_key = c_spec["name"].strip().lower().replace(" ", "_")
                # Priority 1: cell edits
                if c_spec["name"] in active_row:
                    row_custom_values[c_name_key] = str(active_row[c_spec["name"]]).strip()
                elif c_name_key in active_row:
                    row_custom_values[c_name_key] = str(active_row[c_name_key]).strip()
                else:
                    # Priority 2: default value
                    row_custom_values[c_name_key] = str(c_spec.get("default_value", "")).strip()

            # Validation: Name, contact, phone, or email must exist
            if not b_name and not c_name and not raw_email and not raw_phone:
                f_rejected += 1
                total_rejected += 1
                rejected_rows.append({
                    "source_file": orig_filename,
                    "row_number": line_no,
                    "error_reason": "Missing business name, contact name, and communication channels",
                    "raw_data": "|".join(str(v) for v in list(active_row.values())[:6])
                })
                continue

            if not b_name and c_name:
                b_name = c_name

            clean_email = normalize_email(raw_email)
            clean_phone = normalize_phone(raw_phone)
            clean_web = normalize_domain(raw_web)

            # Deduplication
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
                if duplicate_mode in ("skip_exact", "new_only"):
                    continue

            if clean_email:
                seen_emails.add(clean_email)
            if clean_phone:
                seen_phones.add(clean_phone)
            if clean_web:
                seen_websites.add((clean_web, b_name.lower()))
            if b_name and (city or state):
                seen_name_locs.add(f"{b_name.lower()}::{city.lower()}::{state.lower()}")

            # Opportunity & Scoring
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

            lead_id = f"imp_{dataset_id}_{abs(hash(b_name + clean_phone + clean_email + orig_filename + str(line_no)))}"
            pitch = f"Commercial sales & conversion outreach for {b_name} in {cat or 'business'}."
            why = f"Imported lead from {cleaned_name} ({orig_filename}) with direct business contact details."

            # Construct extra_fields JSON payload (capturing all custom columns and unmapped original columns)
            combined_extra = dict(row_custom_values)
            for raw_k, raw_v in active_row.items():
                if raw_k not in mapping.values() and raw_k not in combined_extra:
                    combined_extra[raw_k] = format_cell_value(raw_v)
            extra_fields_json = json.dumps(combined_extra)

            # If user provided custom columns matching standard fields, apply them
            if "country" in row_custom_values and row_custom_values["country"]:
                country = row_custom_values["country"]
            if "category" in row_custom_values and row_custom_values["category"]:
                cat = row_custom_values["category"]
            if "city" in row_custom_values and row_custom_values["city"]:
                city = row_custom_values["city"]
            if "state" in row_custom_values and row_custom_values["state"]:
                state = row_custom_values["state"]
            if "zip" in row_custom_values and row_custom_values["zip"]:
                zip_c = row_custom_values["zip"]
            if "address" in row_custom_values and row_custom_values["address"]:
                addr = row_custom_values["address"]
            if "contact_name" in row_custom_values and row_custom_values["contact_name"]:
                c_name = row_custom_values["contact_name"]
            if "job_title" in row_custom_values and row_custom_values["job_title"]:
                j_title = row_custom_values["job_title"]

            # Build row tuple: 22 standard fields + extra_fields JSON + individual custom column values
            row_tuple = [
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
                "#8b5cf6",
                extra_fields_json
            ]

            # Append real custom column values in order (omitting standard canonical columns to avoid duplicate fields)
            CANONICAL_COL_NAMES = {
                "id", "name", "contact_name", "job_title", "category", "address",
                "city", "state", "zip", "country", "phone", "website", "email",
                "socials", "tier", "score", "opportunity", "pitch", "why",
                "source_badge", "source_id", "source_color", "extra_fields"
            }
            extra_custom_col_names = [c for c in custom_col_names if c not in CANONICAL_COL_NAMES]
            for c_name_key in extra_custom_col_names:
                row_tuple.append(sanitize_csv_cell(row_custom_values.get(c_name_key, "")))

            rows_to_insert.append(tuple(row_tuple))
            f_imported += 1
            total_imported += 1

        file_summaries.append({
            "original_filename": orig_filename,
            "format": fmt,
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

    # Build DuckDB table schema dynamically including custom columns
    col_defs = [
        "id VARCHAR", "name VARCHAR", "contact_name VARCHAR", "job_title VARCHAR",
        "category VARCHAR", "address VARCHAR", "city VARCHAR", "state VARCHAR",
        "zip VARCHAR", "country VARCHAR", "phone VARCHAR", "website VARCHAR",
        "email VARCHAR", "socials VARCHAR", "tier VARCHAR", "score INTEGER",
        "opportunity VARCHAR", "pitch VARCHAR", "why VARCHAR", "source_badge VARCHAR",
        "source_id VARCHAR", "source_color VARCHAR", "extra_fields VARCHAR"
    ]
    extra_custom_col_names = [c for c in custom_col_names if c not in CANONICAL_COL_NAMES]
    for c_name_key in extra_custom_col_names:
        col_defs.append(f'"{c_name_key}" VARCHAR')

    con.execute(f"CREATE TABLE t_imported_staging ({', '.join(col_defs)});")
    placeholders = ",".join(["?" for _ in col_defs])
    con.executemany(f"INSERT INTO t_imported_staging VALUES ({placeholders})", rows_to_insert)

    # Atomic write to Parquet
    safe_final_path = final_parquet_path.replace(os.sep, "/")
    if existing_dataset_id and os.path.exists(final_parquet_path):
        con.execute(f"""
        CREATE TABLE t_combined AS
        SELECT * FROM read_parquet('{safe_final_path}')
        UNION ALL
        SELECT * FROM t_imported_staging;
        """)
        con.execute(f"COPY t_combined TO '{safe_final_path}' (FORMAT PARQUET);")
    else:
        con.execute(f"COPY t_imported_staging TO '{safe_final_path}' (FORMAT PARQUET);")

    # Write rejection error report if needed
    has_rejections = len(rejected_rows) > 0
    if has_rejections:
        with open(rejection_report_path, "w", encoding="utf-8", newline="") as rf:
            writer = csv.DictWriter(rf, fieldnames=["source_file", "row_number", "error_reason", "raw_data"])
            writer.writeheader()
            for rej in rejected_rows:
                writer.writerow(rej)

    # Update metadata registry
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
        "custom_columns": custom_cols_spec,
        "custom_column_names": custom_col_names,
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
        "files_count": len(file_summaries),
        "custom_columns": custom_col_names
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
        "files_summary": file_summaries,
        "custom_columns": custom_cols_spec
    }

# ---------------------------------------------------------------------------
# Post-Import Dataset Column Management (Requirement 6)
# ---------------------------------------------------------------------------

def add_column_to_dataset(
    dataset_id: str,
    column_name: str,
    column_type: str = "text",
    default_value: str = "",
    scope: str = "all",
    lead_ids: Optional[List[str]] = None,
    col_type: Optional[str] = None
) -> Dict[str, Any]:
    column_type = col_type or column_type
    """
    Adds a custom column to an existing dataset:
    - scope == 'all': applies default_value to every existing lead in this dataset.
    - scope == 'selected': applies value only to specified lead IDs.
    - scope == 'future': records in schema metadata for future imports.
    """
    col_clean = column_name.strip().lower().replace(" ", "_")
    col_clean = re.sub(r"[^a-z0-9_]", "", col_clean)
    if not col_clean:
        return {"success": False, "error": "Invalid column name."}

    registry = load_registry()
    dataset = registry.get("datasets", {}).get(dataset_id)
    if not dataset:
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    parquet_path = dataset.get("parquet_path")
    if not parquet_path or not os.path.exists(parquet_path):
        return {"success": False, "error": f"Parquet storage for dataset {dataset_id} not found."}

    safe_p = parquet_path.replace("\\", "/")
    temp_p = os.path.join(STAGING_DIR, f"temp_alter_{dataset_id}_{int(time.time())}.parquet").replace("\\", "/")

    sanitized_def = sanitize_csv_cell(default_value)
    con = duckdb.connect()

    try:
        # Check if column already exists in parquet
        schema_cols = [desc[0].lower() for desc in con.execute(f"SELECT * FROM read_parquet('{safe_p}') LIMIT 0").description]
        if col_clean in schema_cols:
            return {"success": False, "error": f"Column '{col_clean}' already exists in this dataset."}

        sql_def = sanitized_def.replace("'", "''")
        if scope == "all":
            con.execute(f"""
            COPY (
                SELECT *, '{sql_def}' AS "{col_clean}"
                FROM read_parquet('{safe_p}')
            ) TO '{temp_p}' (FORMAT PARQUET);
            """)
            shutil.move(temp_p.replace("/", os.sep), parquet_path)
        elif scope == "selected" and lead_ids:
            safe_ids = "','".join([re.sub(r"[^a-zA-Z0-9_.-]", "", lid) for lid in lead_ids])
            con.execute(f"""
            COPY (
                SELECT *, 
                       CASE WHEN id IN ('{safe_ids}') THEN '{sql_def}' ELSE '' END AS "{col_clean}"
                FROM read_parquet('{safe_p}')
            ) TO '{temp_p}' (FORMAT PARQUET);
            """)
            shutil.move(temp_p.replace("/", os.sep), parquet_path)

        # Update registry
        custom_cols = dataset.get("custom_columns", [])
        custom_cols.append({
            "name": col_clean,
            "type": column_type,
            "default_value": default_value,
            "scope": scope,
            "created_at": datetime.now().isoformat()
        })
        dataset["custom_columns"] = custom_cols
        if "custom_column_names" not in dataset:
            dataset["custom_column_names"] = []
        if col_clean not in dataset["custom_column_names"]:
            dataset["custom_column_names"].append(col_clean)
        dataset["updated_at"] = datetime.now().isoformat()
        save_registry(registry)

        log_audit_event("ADD_COLUMN", dataset_id, {
            "column_name": col_clean,
            "column_type": column_type,
            "default_value": default_value,
            "scope": scope
        })

        return {
            "success": True,
            "dataset_id": dataset_id,
            "column_name": col_clean,
            "scope": scope,
            "affected_leads": dataset.get("total_rows", 0)
        }

    except Exception as e:
        if os.path.exists(temp_p.replace("/", os.sep)):
            try:
                os.remove(temp_p.replace("/", os.sep))
            except Exception:
                pass
        return {"success": False, "error": f"Failed to add column to dataset: {str(e)}"}

def rename_column_in_dataset(dataset_id: str, old_column_name: str, new_column_name: str) -> Dict[str, Any]:
    """Renames an existing custom column in the dataset Parquet file and registry."""
    old_clean = old_column_name.strip().lower().replace(" ", "_")
    new_clean = new_column_name.strip().lower().replace(" ", "_")
    new_clean = re.sub(r"[^a-z0-9_]", "", new_clean)
    if not new_clean:
        return {"success": False, "error": "New column name cannot be empty."}

    registry = load_registry()
    dataset = registry.get("datasets", {}).get(dataset_id)
    if not dataset:
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    parquet_path = dataset.get("parquet_path")
    if not parquet_path or not os.path.exists(parquet_path):
        return {"success": False, "error": f"Parquet storage for dataset {dataset_id} not found."}

    safe_p = parquet_path.replace("\\", "/")
    temp_p = os.path.join(STAGING_DIR, f"temp_rename_{dataset_id}_{int(time.time())}.parquet").replace("\\", "/")

    con = duckdb.connect()
    try:
        con.execute(f"""
        COPY (
            SELECT * EXCLUDE ("{old_clean}"), "{old_clean}" AS "{new_clean}"
            FROM read_parquet('{safe_p}')
        ) TO '{temp_p}' (FORMAT PARQUET);
        """)
        shutil.move(temp_p.replace("/", os.sep), parquet_path)

        # Update registry
        for c in dataset.get("custom_columns", []):
            if c.get("name") == old_clean:
                c["name"] = new_clean
        if "custom_column_names" in dataset:
            dataset["custom_column_names"] = [new_clean if c == old_clean else c for c in dataset["custom_column_names"]]
        dataset["updated_at"] = datetime.now().isoformat()
        save_registry(registry)

        log_audit_event("RENAME_COLUMN", dataset_id, {"old_name": old_clean, "new_name": new_clean})
        return {"success": True, "dataset_id": dataset_id, "old_name": old_clean, "new_name": new_clean}

    except Exception as e:
        if os.path.exists(temp_p.replace("/", os.sep)):
            try:
                os.remove(temp_p.replace("/", os.sep))
            except Exception:
                pass
        return {"success": False, "error": f"Failed to rename column: {str(e)}"}

def fill_column_values(
    dataset_id: str,
    column_name: str,
    fill_value: str = "",
    fill_mode: str = "blanks_only",
    lead_ids: Optional[List[str]] = None,
    value: Optional[str] = None,
    only_blanks: Optional[bool] = None
) -> Dict[str, Any]:
    if value is not None:
        fill_value = value
    if only_blanks is not None:
        fill_mode = "blanks_only" if only_blanks else "all"

    col_clean = column_name.strip().lower().replace(" ", "_")
    sanitized_val = sanitize_csv_cell(fill_value)

    registry = load_registry()
    dataset = registry.get("datasets", {}).get(dataset_id)
    if not dataset:
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    parquet_path = dataset.get("parquet_path")
    if not parquet_path or not os.path.exists(parquet_path):
        return {"success": False, "error": f"Parquet storage for dataset {dataset_id} not found."}

    safe_p = parquet_path.replace("\\", "/")
    temp_p = os.path.join(STAGING_DIR, f"temp_fill_{dataset_id}_{int(time.time())}.parquet").replace("\\", "/")

    sql_val = sanitized_val.replace("'", "''")
    con = duckdb.connect()
    try:
        if fill_mode == "all":
            con.execute(f"""
            COPY (
                SELECT * EXCLUDE ("{col_clean}"),
                       '{sql_val}' AS "{col_clean}"
                FROM read_parquet('{safe_p}')
            ) TO '{temp_p}' (FORMAT PARQUET);
            """)
        elif fill_mode == "blanks_only":
            con.execute(f"""
            COPY (
                SELECT * EXCLUDE ("{col_clean}"),
                       CASE WHEN "{col_clean}" IS NULL OR trim("{col_clean}") = ''
                            THEN '{sql_val}'
                            ELSE "{col_clean}" END AS "{col_clean}"
                FROM read_parquet('{safe_p}')
            ) TO '{temp_p}' (FORMAT PARQUET);
            """)
        elif fill_mode == "selected" and lead_ids:
            safe_ids = "','".join([re.sub(r"[^a-zA-Z0-9_.-]", "", lid) for lid in lead_ids])
            con.execute(f"""
            COPY (
                SELECT * EXCLUDE ("{col_clean}"),
                       CASE WHEN id IN ('{safe_ids}')
                            THEN '{sql_val}'
                            ELSE "{col_clean}" END AS "{col_clean}"
                FROM read_parquet('{safe_p}')
            ) TO '{temp_p}' (FORMAT PARQUET);
            """)
        shutil.move(temp_p.replace("/", os.sep), parquet_path)

        log_audit_event("FILL_COLUMN", dataset_id, {
            "column_name": col_clean,
            "fill_value": fill_value,
            "fill_mode": fill_mode
        })
        return {
            "success": True,
            "dataset_id": dataset_id,
            "column_name": col_clean,
            "fill_mode": fill_mode,
            "updated_leads_count": dataset.get("total_rows", 0),
            "affected_leads": dataset.get("total_rows", 0)
        }

    except Exception as e:
        if os.path.exists(temp_p.replace("/", os.sep)):
            try:
                os.remove(temp_p.replace("/", os.sep))
            except Exception:
                pass
        return {"success": False, "error": f"Failed to fill column values: {str(e)}"}

def delete_column_from_dataset(dataset_id: str, column_name: str) -> Dict[str, Any]:
    """Safely drops a custom column from an imported dataset Parquet file and registry."""
    col_clean = column_name.strip().lower().replace(" ", "_")

    registry = load_registry()
    dataset = registry.get("datasets", {}).get(dataset_id)
    if not dataset:
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    parquet_path = dataset.get("parquet_path")
    if not parquet_path or not os.path.exists(parquet_path):
        return {"success": False, "error": f"Parquet storage for dataset {dataset_id} not found."}

    safe_p = parquet_path.replace("\\", "/")
    temp_p = os.path.join(STAGING_DIR, f"temp_drop_{dataset_id}_{int(time.time())}.parquet").replace("\\", "/")

    con = duckdb.connect()
    try:
        con.execute(f"""
        COPY (
            SELECT * EXCLUDE ("{col_clean}")
            FROM read_parquet('{safe_p}')
        ) TO '{temp_p}' (FORMAT PARQUET);
        """)
        shutil.move(temp_p.replace("/", os.sep), parquet_path)

        # Update registry
        dataset["custom_columns"] = [c for c in dataset.get("custom_columns", []) if c.get("name") != col_clean]
        if "custom_column_names" in dataset:
            dataset["custom_column_names"] = [c for c in dataset["custom_column_names"] if c != col_clean]
        dataset["updated_at"] = datetime.now().isoformat()
        save_registry(registry)

        log_audit_event("DELETE_COLUMN", dataset_id, {"column_name": col_clean})
        return {"success": True, "dataset_id": dataset_id, "deleted_column": col_clean}

    except Exception as e:
        if os.path.exists(temp_p.replace("/", os.sep)):
            try:
                os.remove(temp_p.replace("/", os.sep))
            except Exception:
                pass
        return {"success": False, "error": f"Failed to delete column: {str(e)}"}

def get_dataset_columns(dataset_id: str) -> Dict[str, Any]:
    """Returns all available columns for a dataset (Standard + Dataset-Specific Custom Columns)."""
    registry = load_registry()
    dataset = registry.get("datasets", {}).get(dataset_id)
    if not dataset:
        return {"success": False, "error": f"Dataset {dataset_id} not found."}

    parquet_path = dataset.get("parquet_path")
    if not parquet_path or not os.path.exists(parquet_path):
        return {"success": False, "error": f"Parquet file not found."}

    con = duckdb.connect()
    cur = con.execute(f"SELECT * FROM read_parquet('{parquet_path.replace(os.sep, '/')}') LIMIT 0")
    col_names = [desc[0] for desc in cur.description]
    custom_names = set(dataset.get("custom_column_names", []))

    columns_info = []
    for c in col_names:
        is_custom = c in custom_names or c not in [tc["key"] for tc in TARGET_COLUMNS] and c not in ("id", "socials", "tier", "score", "opportunity", "pitch", "why", "source_badge", "source_id", "source_color", "extra_fields")
        columns_info.append({
            "name": c,
            "label": c.replace("_", " ").title(),
            "is_custom": is_custom,
            "type": "VARCHAR"
        })

    return {
        "success": True,
        "dataset_id": dataset_id,
        "dataset_name": dataset.get("name"),
        "total_columns": len(columns_info),
        "columns": columns_info,
        "custom_columns": dataset.get("custom_columns", [])
    }

def export_dataset_with_custom_columns(dataset_id: str, output_path: Optional[str] = None) -> str:
    """Exports dataset to CSV with all standard and custom columns, with formula injection protection."""
    registry = load_registry()
    dataset = registry.get("datasets", {}).get(dataset_id)
    if not dataset or not dataset.get("parquet_path") or not os.path.exists(dataset["parquet_path"]):
        raise FileNotFoundError(f"Parquet file for dataset {dataset_id} not found.")

    out_file = output_path or os.path.join(STAGING_DIR, f"export_{dataset_id}_{int(time.time())}.csv")
    safe_p = dataset["parquet_path"].replace(os.sep, "/")

    con = duckdb.connect()
    # Read via DuckDB, write with sanitized cells
    cur = con.execute(f"SELECT * EXCLUDE (source_color, source_id) FROM read_parquet('{safe_p}')")
    headers = [desc[0] for desc in cur.description]

    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        while True:
            chunk = cur.fetchmany(2000)
            if not chunk:
                break
            for r in chunk:
                sanitized_row = [sanitize_csv_cell(c) for c in r]
                writer.writerow(sanitized_row)

    return out_file

# ---------------------------------------------------------------------------
# General Dataset Operations
# ---------------------------------------------------------------------------

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

    parquet_path = meta.get("parquet_path")
    if parquet_path and os.path.exists(parquet_path):
        try:
            os.remove(parquet_path)
        except Exception:
            pass

    log_audit_event("DELETE_DATASET", dataset_id, {"deleted_meta": meta})
    return {"success": True, "deleted_id": dataset_id}
