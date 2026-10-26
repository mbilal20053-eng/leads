# Universal Lead Importer & Custom Columns Guide

This document provides a comprehensive operational and technical guide for the **Universal File Importer**, **Custom Columns Engine**, and **Dataset Column Management System** in Lead Engine PRO.

---

## 1. Supported File Formats & Technical Capabilities

The ingestion engine automatically detects formats, encodings, and delimiters without requiring manual configuration:

| Format Category | Supported Extensions | Detection & Parsing Strategy | Special Capabilities |
|---|---|---|---|
| **Delimited Text** | `.csv`, `.tsv`, `.txt`, `.tab` | Auto-detects delimiters (`,`, `;`, `\t`, `\|`) and encodings (`UTF-8`, `UTF-8-SIG`, `CP1252`, `ISO-8859-1`) | Handles quoted multiline cells, unescaped commas, and tabs |
| **Excel Spreadsheets** | `.xlsx`, `.xlsm`, `.xls` | Modern (`openpyxl`) and legacy 97-2003 BIFF8 (`xlrd`) | Multi-worksheet discovery and interactive sheet picker |
| **JSON Records** | `.json`, `.jsonl`, `.ndjson` | JSON object array and newline-delimited stream parser | Automatic dot-path flattening for nested dictionary hierarchies |
| **XML Data** | `.xml` | Python `xml.etree.ElementTree` parser with entity bomb defenses | Automatic repeated row-element tag detection and child element flattening |
| **Parquet Columnar** | `.parquet`, `.pq` | High-performance DuckDB and PyArrow columnar reader | Direct columnar schema inspection, instant row estimation |
| **Compressed Archives** | `.zip` | ZipFile with path traversal (`../`) and decompression bomb defense | Contained file explorer; extracts and imports selected tabular files |
| **GZIP Archives** | `.gz`, `.csv.gz`, `.json.gz` | Streaming Python `gzip` decompressor | Seamless transparent decompression into staging pipeline |

### Unsupported or Invalid Files
Unsupported formats (e.g., `.pdf`, `.exe`, `.docx`, `.png`) and corrupted/encrypted archives are rejected with clear, human-readable error messages explaining supported extensions.

---

## 2. File Size Limits & Resource Safety

To ensure stable operation on both local machines and servers without exhausting memory:
- **Max File Upload Size**: 100 MB per file (configurable via `MAX_UPLOAD_SIZE_BYTES`).
- **Max ZIP Archive Limit**: Up to 500 MB uncompressed size with a maximum compression ratio of 100x to prevent ZIP bomb vulnerabilities.
- **Low RAM Streaming**: Large files are processed in streamed batches of 2,000 records directly into DuckDB and Apache Parquet, preventing out-of-memory crashes even when importing files with millions of rows.
- **Leading Zero Preservation**: Phone numbers (e.g. `07123 456789`), postal codes (e.g. `01234`), and corporate registration numbers are preserved as text and never converted into scientific notation (`1.23E+10`).

---

## 3. End-to-End Import Workflow

The universal import wizard provides a step-by-step workflow:

```text
Step 1: Enter Dataset Name
   │
   ▼
Step 2: Multi-File Upload & Format Inspection
   │  ├── Universal format badge display
   │  ├── Multi-sheet selection for Excel workbooks
   │  └── Contained file selector for ZIP archives
   ▼
Step 3: Column Mapping, Custom Columns & Spreadsheet Cell Editing
   │  ├── Column include/exclude toggle
   │  ├── Column display rename
   │  ├── Standard canonical field mapping (Name, Phone, Email, Website, etc.)
   │  ├── Data type detection & overrides (Text, Integer, Decimal, Boolean, Date)
   │  ├── Default fallback values for blank cells
   │  ├── [+ Add Custom Column]
   │  │   ├── Mode A: Same constant value for every row (e.g., country = "United Kingdom")
   │  │   └── Mode B: Individual row-by-row values via spreadsheet preview
   │  └── Interactive spreadsheet-style table with live cell editing
   ▼
Step 4: Atomic Ingestion & Real-Time Indexing
   │  ├── Configurable deduplication (skip exact, import all, new only, flag review)
   │  ├── Malformed row isolation into downloadable CSV rejection report
   │  └── Atomic commit to Parquet storage & DuckDB views
```

---

## 4. Custom Columns (Critical Feature)

Lead Engine PRO allows users to define dataset-specific custom fields during import:

### Mode A: Same Value for All Rows
- **Use Case**: Tagging an entire dataset with common geographic, source, or campaign attributes.
- **Example**: Add column `country` with value `United Kingdom`, or `lead_source` with value `Construction Directory 2026`.
- **Result**: Every imported record receives that value in the dataset.

### Mode B: Individual Row-by-Row Values
- **Use Case**: Adding custom attributes where each lead requires a distinct value.
- **Example**: Add column `industry` or `verification_status`.
- **Result**: Users can edit individual cells directly in the preview spreadsheet table. Row 1 can be `Construction`, Row 2 can be `Electrical Engineering`, Row 3 can remain blank.

### Blank Cell Preservation
Blank cells remain completely empty (`""` or `NULL`) and are never populated with fabricated or synthetic data.

---

## 5. Dataset-Specific Columns & Unified Database Architecture

Different datasets often have completely different attributes:
- **Dataset A (UK Companies)**: `company_name`, `website`, `country`, `registration_number`
- **Dataset B (US Restaurants)**: `business_name`, `website`, `phone`, `cuisine`, `opening_hours`

### Dual-View DuckDB Architecture
To support distinct schemas without breaking global queries:
1. **Canonical Standard View (`v_imp_{dataset_id}`)**:
   Projects the 22 canonical core fields (`id`, `name`, `contact_name`, `job_title`, `category`, `address`, `city`, `state`, `zip`, `country`, `phone`, `website`, `email`, `socials`, `tier`, `score`, `opportunity`, `pitch`, `why`, `source_badge`, `source_id`, `source_color`). This view seamlessly unions into `v_all_unified` across the entire 14.9M lead database without schema conflicts.
2. **Full Dataset-Specific View (`v_imp_{dataset_id}_full`)**:
   Contains all canonical fields, all custom columns (`registration_number`, `cuisine`, `opening_hours`), and an `extra_fields` JSON payload for dynamic custom schema queries.

---

## 6. Post-Import Dataset Column Management

From the **My Datasets** dashboard, clicking **⚙️ Columns** opens the interactive column management modal:

1. **View Attributes**: Lists all standard core fields and custom attributes for the dataset.
2. **Add Column to Existing Dataset**:
   - Scope option 1: **All leads in this dataset** (populates all existing rows with the specified default value).
   - Scope option 2: **Future imports only** (registers the column schema for subsequent imports).
3. **Rename Custom Column**: Safely renames the column in the Parquet storage and schema registry.
4. **Fill Column Values**:
   - Fill blank cells only with a user-specified value.
   - Batch overwrite all leads in the dataset with a user-specified value.
5. **Delete Custom Column**: Permanently removes the column from the dataset with confirmation warnings.
6. **Export with Custom Columns**: Generates a clean CSV containing all standard and dataset-specific fields, protected by formula injection sanitation (neutralizing dangerous prefixes like `=`, `+`, `-`, `@`).

---

## 7. Verification & Automated Test Coverage

The entire universal ingestion and custom column system is backed by automated tests in `tests/`:

- `tests/test_universal_importer.py` (12 comprehensive format and schema tests)
- `tests/test_importer_comprehensive.py` (13 deduplication, error isolation, and volume tests)
- `tests/test_api_column_endpoints.py` (REST API integration tests for all column management routes)

Run the automated test suite with:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
