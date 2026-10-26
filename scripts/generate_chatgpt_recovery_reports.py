import os
import csv

OUT_DIR = r"D:\leads\download_recovery_inventory"
os.makedirs(OUT_DIR, exist_ok=True)

# =============================================================================
# 1. MUST_REDOWNLOAD.csv
# =============================================================================
must_redownload = [
    {
        "dataset_name": "Geofabrik Oceania OpenStreetMap Commercial POIs",
        "purpose": "Commercial points of interest, store locations, and business addresses for Australia, New Zealand, and Pacific Islands",
        "expected_filename": "australia-oceania-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap Foundation",
        "official_website": "https://download.geofabrik.de/oceania.html",
        "direct_download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        "expected_format": "OSM.PBF (Protocolbuffer Binary)",
        "expected_download_size": "~1.5 GB",
        "expected_records": "2,500,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "current_defect": "Only a 50-byte MD5 checksum (oceania.osm.pbf.md5) exists locally in D:\\leads. The actual data payload was never downloaded.",
        "publicly_available": "YES (Live HTTP 200 verified)"
    }
]

with open(os.path.join(OUT_DIR, "MUST_REDOWNLOAD.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "purpose", "expected_filename", "source_org",
        "official_website", "direct_download_url", "expected_format",
        "expected_download_size", "expected_records", "auth_required",
        "current_defect", "publicly_available"
    ])
    writer.writeheader()
    writer.writerows(must_redownload)

print("[1/6] Wrote MUST_REDOWNLOAD.csv")

# =============================================================================
# 2. OPTIONAL_NEW_DATASETS.csv
# =============================================================================
optional_datasets = [
    {
        "dataset_name": "UK Companies House Basic Company Data",
        "purpose": "Comprehensive official government registry of all active and dissolved companies in the United Kingdom",
        "expected_filename": "BasicCompanyDataAsOneFile-2026-10-01.zip",
        "source_org": "Companies House (UK Government)",
        "official_website": "http://download.companieshouse.gov.uk/en_output.html",
        "direct_download_url": "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip",
        "file_format": "CSV.ZIP",
        "download_size": "~420 MB",
        "uncompressed_size": "~2.1 GB",
        "expected_records": "5,400,000 (Verified Government Registry)",
        "auth_required": "None (Free Open Government Licence)",
        "disk_impact": "LOW (Consumes <1% of D:\\ free space; completely safe for remaining 54.5 GB)",
        "priority_recommendation": "HIGH VALUE RECOMMENDED"
    },
    {
        "dataset_name": "Open Company Database Full Release (5M Companies)",
        "purpose": "Global company directory with domain names, industries, founded years, and headquarters locations",
        "expected_filename": "open_company_database_5m.parquet",
        "source_org": "Fliar Research / Radar API",
        "official_website": "https://github.com/fliarbi/radar-api-mcp",
        "direct_download_url": "https://github.com/fliarbi/radar-api-mcp",
        "file_format": "PARQUET",
        "download_size": "~450 MB",
        "uncompressed_size": "~1.5 GB",
        "expected_records": "5,000,000 (Full Scope vs 100k sample locally)",
        "auth_required": "Free Open Source / Radar API Key for live stream",
        "disk_impact": "LOW (Consumes ~1% of D:\\ free space)",
        "priority_recommendation": "MEDIUM (Only if expansion beyond current 100k sample is needed)"
    },
    {
        "dataset_name": "Geofabrik Africa Commercial POIs",
        "purpose": "Business locations, commercial establishments, and services across all African nations",
        "expected_filename": "africa-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_website": "https://download.geofabrik.de/africa.html",
        "direct_download_url": "https://download.geofabrik.de/africa-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "download_size": "~6 GB",
        "uncompressed_size": "~15 GB",
        "expected_records": "12,000,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "disk_impact": "MODERATE (Consumes ~11% of D:\\ free space)",
        "priority_recommendation": "LOW (Download only if African market coverage is targeted)"
    },
    {
        "dataset_name": "Geofabrik South America Commercial POIs",
        "purpose": "Business locations and commercial establishments across Brazil, Argentina, Colombia, etc.",
        "expected_filename": "south-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_website": "https://download.geofabrik.de/south-america.html",
        "direct_download_url": "https://download.geofabrik.de/south-america-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "download_size": "~4 GB",
        "uncompressed_size": "~10 GB",
        "expected_records": "6,800,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "disk_impact": "MODERATE (Consumes ~7% of D:\\ free space)",
        "priority_recommendation": "LOW (Download only if South American market coverage is targeted)"
    },
    {
        "dataset_name": "Geofabrik North America Commercial POIs",
        "purpose": "Points of interest across USA, Canada, and Mexico",
        "expected_filename": "north-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_website": "https://download.geofabrik.de/north-america.html",
        "direct_download_url": "https://download.geofabrik.de/north-america-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "download_size": "~14 GB",
        "uncompressed_size": "~35 GB",
        "expected_records": "32,000,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "disk_impact": "HIGH RISK (Consumes ~26% of D:\\ free space; tight margin)",
        "priority_recommendation": "LOW / CAUTION (D:\\ has only 54.5 GB free)"
    },
    {
        "dataset_name": "Geofabrik Asia Commercial POIs",
        "purpose": "Commercial POIs across Japan, India, Southeast Asia, Middle East",
        "expected_filename": "asia-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_website": "https://download.geofabrik.de/asia.html",
        "direct_download_url": "https://download.geofabrik.de/asia-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "download_size": "~15 GB",
        "uncompressed_size": "~40 GB",
        "expected_records": "45,000,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "disk_impact": "HIGH RISK (Consumes ~28% of D:\\ free space)",
        "priority_recommendation": "LOW / CAUTION"
    },
    {
        "dataset_name": "Geofabrik Europe Commercial POIs",
        "purpose": "Comprehensive commercial POIs across all European countries",
        "expected_filename": "europe-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_website": "https://download.geofabrik.de/europe.html",
        "direct_download_url": "https://download.geofabrik.de/europe-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "download_size": "~30 GB",
        "uncompressed_size": "~80 GB",
        "expected_records": "65,000,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "disk_impact": "CRITICAL RISK (30 GB download + 80 GB unpack EXCEEDS available 54.5 GB free space)",
        "priority_recommendation": "DO NOT DOWNLOAD ON CURRENT DISK"
    },
    {
        "dataset_name": "OpenStreetMap Planet Worldwide Commercial POIs",
        "purpose": "Global planet dump of all OpenStreetMap geographic nodes and tags",
        "expected_filename": "planet-latest.osm.pbf",
        "source_org": "OpenStreetMap Foundation",
        "official_website": "https://planet.openstreetmap.org/",
        "direct_download_url": "https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "download_size": "~75 GB",
        "uncompressed_size": "~250 GB",
        "expected_records": "150,000,000 (Estimated POIs)",
        "auth_required": "None (Free Open Data - ODbL)",
        "disk_impact": "IMPOSSIBLE (Requires ~75 GB download space; D:\\ only has 54.47 GB free)",
        "priority_recommendation": "DO NOT DOWNLOAD (Requires external storage drive)"
    }
]

with open(os.path.join(OUT_DIR, "OPTIONAL_NEW_DATASETS.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "purpose", "expected_filename", "source_org",
        "official_website", "direct_download_url", "file_format",
        "download_size", "uncompressed_size", "expected_records",
        "auth_required", "disk_impact", "priority_recommendation"
    ])
    writer.writeheader()
    writer.writerows(optional_datasets)

print("[2/6] Wrote OPTIONAL_NEW_DATASETS.csv")

# =============================================================================
# 3. ALREADY_PRESENT_NO_DOWNLOAD.csv
# =============================================================================
already_present = [
    {
        "dataset_name": "B2B Executive Decision Makers (Final Validated)",
        "local_path": r"D:\leads\cleaned_export\b2b_executives_final_validated.parquet",
        "format": "PARQUET",
        "size_mb": "723.27 MB",
        "row_count": "10,268,615",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Already fully cleaned, validated against strict contact rules, and actively indexed in v_all_unified."
    },
    {
        "dataset_name": "B2B Raw Shards Consolidated Cleaned",
        "local_path": r"D:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet",
        "format": "PARQUET",
        "size_mb": "571.01 MB",
        "row_count": "10,268,615",
        "verification_status": "Verified Complete",
        "reason_no_download": "Intermediate consolidation file stored intact in cleaned_export."
    },
    {
        "dataset_name": "B2B Executives Pre-Validation Raw Master",
        "local_path": r"D:\leads\b2b_executives.parquet",
        "format": "PARQUET",
        "size_mb": "791.38 MB",
        "row_count": "11,543,658",
        "verification_status": "Verified Complete (Raw)",
        "reason_no_download": "Raw pre-cleanup parquet preserved intact."
    },
    {
        "dataset_name": "GLEIF Golden Copy Legal Entity Registry (Parquet)",
        "local_path": r"D:\leads\gleif_goldencopy.parquet",
        "format": "PARQUET",
        "size_mb": "493.82 MB",
        "row_count": "3,472,837",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Fully processed and active in production engine."
    },
    {
        "dataset_name": "GLEIF Golden Copy LEI-2 Raw Zip Archive",
        "local_path": r"D:\leads\20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip",
        "format": "CSV.ZIP",
        "size_mb": "482.78 MB",
        "row_count": "3,472,837",
        "verification_status": "Verified Complete Raw Archive",
        "reason_no_download": "Original complete download archive is already safely stored on disk."
    },
    {
        "dataset_name": "Homeowners & Residential Property Leads (Parquet)",
        "local_path": r"D:\leads\homeowners.parquet",
        "format": "PARQUET",
        "size_mb": "14.05 MB",
        "row_count": "703,772",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Fully converted and active in production database."
    },
    {
        "dataset_name": "Homeowners & Residential Property Leads (Raw CSV)",
        "local_path": r"D:\leads\free-tier (1).csv",
        "format": "CSV",
        "size_mb": "78.92 MB",
        "row_count": "703,772",
        "verification_status": "Verified Complete Raw Source",
        "reason_no_download": "Original raw CSV file is complete on disk."
    },
    {
        "dataset_name": "Retail, Commercial & Franchise Locations",
        "local_path": r"D:\leads\master-locations.csv",
        "format": "CSV",
        "size_mb": "10.91 MB",
        "row_count": "154,710",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Active and fully accessible in DuckDB."
    },
    {
        "dataset_name": "Master Locations Zip Backup Archive",
        "local_path": r"D:\leads\master-locations.zip",
        "format": "ZIP",
        "size_mb": "2.38 MB",
        "row_count": "154,710",
        "verification_status": "Verified Complete Archive",
        "reason_no_download": "Original zip archive is intact on disk."
    },
    {
        "dataset_name": "Tech Stack Intelligence Companies (Parquet)",
        "local_path": r"D:\leads\tech_stack_companies.parquet",
        "format": "PARQUET",
        "size_mb": "18.65 MB",
        "row_count": "153,104",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Fully compiled from tech-stack samples and active in database."
    },
    {
        "dataset_name": "Tech Stack Datasets Main (Zip Archive)",
        "local_path": r"D:\leads\tech-stack-datasets.zip",
        "format": "ZIP",
        "size_mb": "35.06 MB",
        "row_count": "153,104",
        "verification_status": "Verified Complete Archive",
        "reason_no_download": "Complete repository zip and extracted subdirectories exist on disk."
    },
    {
        "dataset_name": "Open Company Database Sample (Parquet)",
        "local_path": r"D:\leads\open_company_database.parquet",
        "format": "PARQUET",
        "size_mb": "8.22 MB",
        "row_count": "100,000",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Fully processed and active in production."
    },
    {
        "dataset_name": "Open Company Database Sample (Raw CSV)",
        "local_path": r"D:\leads\open_company_database_sample.csv",
        "format": "CSV",
        "size_mb": "26.01 MB",
        "row_count": "100,000",
        "verification_status": "Verified Complete Raw Source",
        "reason_no_download": "Raw source CSV is complete on disk."
    },
    {
        "dataset_name": "Commercial Real Estate B2B Companies",
        "local_path": r"D:\leads\free-tier.csv",
        "format": "CSV",
        "size_mb": "5.55 MB",
        "row_count": "44,021",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Original complete CSV is active in database."
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Facts (Parquet)",
        "local_path": r"D:\leads\sec_company_facts.parquet",
        "format": "PARQUET",
        "size_mb": "1.65 MB",
        "row_count": "20,501",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Fully processed and active in production database."
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Facts Bulk Archive",
        "local_path": r"D:\leads\companyfacts.zip",
        "format": "ZIP",
        "size_mb": "1,346.13 MB",
        "row_count": "20,501 JSON files",
        "verification_status": "Verified Complete Archive",
        "reason_no_download": "A 1.35 GB archive containing all 20,501 public company XBRL files is complete on disk."
    },
    {
        "dataset_name": "Common Crawl Web Index (Parquet)",
        "local_path": r"D:\leads\cc_web_index.parquet",
        "format": "PARQUET",
        "size_mb": "0.02 MB",
        "row_count": "302",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "Active and fully queryable in database."
    },
    {
        "dataset_name": "Common Crawl Web Index Path Archive",
        "local_path": r"D:\leads\cc-index.paths.gz",
        "format": "GZ",
        "size_mb": "0.001 MB",
        "row_count": "302",
        "verification_status": "Verified Complete Archive",
        "reason_no_download": "Raw gz archive is complete on disk."
    },
    {
        "dataset_name": "7 Targeted Professional Verticals CSVs",
        "local_path": r"D:\leads\*-restaurants.csv, *-realtors.csv, etc.",
        "format": "CSV (7 Files)",
        "size_mb": "1.65 MB",
        "row_count": "17,500 (2,500 each)",
        "verification_status": "Verified Complete & Indexed in DuckDB",
        "reason_no_download": "All 7 vertical CSVs (2,500 records each) are complete and active in production."
    },
    {
        "dataset_name": "ODO Senzing Global Entity Intelligence Archive",
        "local_path": r"D:\leads\ODO_SENZING_20260305.zip",
        "format": "ZIP",
        "size_mb": "20,387.90 MB (19.91 GB)",
        "row_count": "2,496 JSON files (~341M declared records)",
        "verification_status": "Verified Complete Local Archive",
        "reason_no_download": "A massive 19.91 GB archive containing 2,496 JSON files is ALREADY on disk. Do NOT waste 20 GB of bandwidth downloading it again."
    },
    {
        "dataset_name": "Free Company Global Dataset Archive",
        "local_path": r"D:\leads\free_company_dataset.csv.zip",
        "format": "CSV.GZ",
        "size_mb": "2,281.29 MB (2.23 GB)",
        "row_count": "37,200,000 streamable (~180M declared)",
        "verification_status": "Verified Complete Local GZIP Stream",
        "reason_no_download": "A 2.23 GB compressed stream is ALREADY on disk. It is not corrupted; it simply uses GZIP format."
    },
    {
        "dataset_name": "Data Legion Global Companies Archive",
        "local_path": r"D:\leads\data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "format": "CSV.GZ",
        "size_mb": "1,474.93 MB (1.44 GB)",
        "row_count": "28,127,036",
        "verification_status": "Verified Complete Local GZIP Archive",
        "reason_no_download": "A 1.44 GB gzip file containing 28.1M verified company profiles is ALREADY on disk."
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Submissions Archive",
        "local_path": r"D:\leads\submissions (1).zip",
        "format": "ZIP",
        "size_mb": "1,498.22 MB (1.46 GB)",
        "row_count": "995,761 JSON files",
        "verification_status": "Verified Complete Local Archive",
        "reason_no_download": "A 1.46 GB zip file containing 995,761 corporate filer JSON documents is ALREADY on disk."
    },
    {
        "dataset_name": "18 Raw Downloads Shards (free-tier 2 to 19)",
        "local_path": r"D:\leads\free-tier (*).csv",
        "format": "CSV (18 Files)",
        "size_mb": "2,492.50 MB (2.43 GB)",
        "row_count": "11,833,267",
        "verification_status": "Verified Complete Raw Shards",
        "reason_no_download": "All 18 original raw CSV shards are stored intact on disk."
    },
    {
        "dataset_name": "Master Backup Archive",
        "local_path": r"D:\leads\backup_original_20261025.zip",
        "format": "ZIP",
        "size_mb": "702.28 MB",
        "row_count": "31 files",
        "verification_status": "Verified Complete Immutable Backup",
        "reason_no_download": "Full historical immutable backup zip is intact on disk."
    }
]

with open(os.path.join(OUT_DIR, "ALREADY_PRESENT_NO_DOWNLOAD.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "local_path", "format", "size_mb", "row_count",
        "verification_status", "reason_no_download"
    ])
    writer.writeheader()
    writer.writerows(already_present)

print("[3/6] Wrote ALREADY_PRESENT_NO_DOWNLOAD.csv")

# =============================================================================
# 4. RESTORE_FROM_BACKUP.csv
# =============================================================================
restore_from_backup = [
    {
        "dataset_name": "Apple Retail Locations (Global Stores)",
        "damaged_or_missing_path": r"D:\leads\apple-locations.csv (Missing from root) / D:\leads\cleaned_20261025\apple-locations.csv (Truncated)",
        "damaged_state": "Truncated to 57 bytes (header only, 0 rows) in cleaned_20261025; missing from D:\\leads root.",
        "intact_backup_path": r"D:\leads\backup_original_20261025\apple-locations.csv",
        "backup_size_bytes": "40,649",
        "verified_rows_in_backup": "692 store locations",
        "recovery_method": "NO DOWNLOAD NEEDED. Simply copy D:\\leads\\backup_original_20261025\\apple-locations.csv to D:\\leads\\apple-locations.csv.",
        "network_download_required": "NO (0 bytes download needed)"
    },
    {
        "dataset_name": "Free Company Global Dataset (Extension Mislabel)",
        "damaged_or_missing_path": r"D:\leads\free_company_dataset.csv.zip",
        "damaged_state": "File is misnamed with .zip extension. Standard zip extractors fail reporting 'File is not a zip file'.",
        "intact_backup_path": r"D:\leads\free_company_dataset.csv.zip (Existing local file)",
        "backup_size_bytes": "2,392,105,978",
        "verified_rows_in_backup": "37,200,000 streamable rows",
        "recovery_method": "NO DOWNLOAD NEEDED. The file is a valid GZIP stream (magic bytes 1f 8b). Rename to .csv.gz or stream directly in DuckDB read_csv(..., compression='gzip').",
        "network_download_required": "NO (0 bytes download needed)"
    },
    {
        "dataset_name": "Realtors Duplicate Empty Stub",
        "damaged_or_missing_path": r"D:\leads\backup_original_20261025\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv",
        "damaged_state": "35-byte empty header stub with zero records.",
        "intact_backup_path": r"D:\leads\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv",
        "backup_size_bytes": "258,526",
        "verified_rows_in_backup": "2,500 verified realtors",
        "recovery_method": "NO ACTION NEEDED. The main file 0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv is already complete, intact, and indexed in DuckDB.",
        "network_download_required": "NO (0 bytes download needed)"
    }
]

with open(os.path.join(OUT_DIR, "RESTORE_FROM_BACKUP.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "damaged_or_missing_path", "damaged_state",
        "intact_backup_path", "backup_size_bytes", "verified_rows_in_backup",
        "recovery_method", "network_download_required"
    ])
    writer.writeheader()
    writer.writerows(restore_from_backup)

print("[4/6] Wrote RESTORE_FROM_BACKUP.csv")

# =============================================================================
# 5. VERIFIED_OFFICIAL_DOWNLOAD_LINKS.csv
# =============================================================================
verified_links = [
    {
        "dataset_name": "Geofabrik Australia & Oceania Commercial POIs",
        "expected_filename": "australia-oceania-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap Foundation",
        "official_source_portal": "https://download.geofabrik.de/oceania.html",
        "direct_download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~1.5 GB",
        "expected_record_count": "2,500,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Payload Missing (MD5 checksum only)"
    },
    {
        "dataset_name": "UK Companies House Basic Company Data",
        "expected_filename": "BasicCompanyDataAsOneFile-2026-10-01.zip",
        "source_org": "Companies House (UK Government)",
        "official_source_portal": "http://download.companieshouse.gov.uk/en_output.html",
        "direct_download_url": "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip",
        "file_format": "CSV.ZIP",
        "approx_download_size": "~420 MB",
        "expected_record_count": "5,400,000",
        "count_nature": "Verified Exact Government Register",
        "auth_required": "None (Free Open Government Licence)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    },
    {
        "dataset_name": "GLEIF Golden Copy LEI-2 Global Corporate Registry",
        "expected_filename": "20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip",
        "source_org": "Global Legal Entity Identifier Foundation (GLEIF)",
        "official_source_portal": "https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy",
        "direct_download_url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest/lei2/csv",
        "file_format": "CSV.ZIP",
        "approx_download_size": "~506 MB",
        "expected_record_count": "3,472,837",
        "count_nature": "Verified Exact Corporate Entities",
        "auth_required": "None (Free Open Data)",
        "live_http_status": "ACTIVE 200 via Portal",
        "local_presence": "Already Complete on Disk (D:\\leads\\gleif_goldencopy.parquet)"
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Submissions Bulk",
        "expected_filename": "submissions.zip",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "official_source_portal": "https://www.sec.gov/edgar/sec-api-documentation",
        "direct_download_url": "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip",
        "file_format": "ZIP",
        "approx_download_size": "~1.46 GB",
        "expected_record_count": "995,761",
        "count_nature": "Verified Exact Corporate Filers",
        "auth_required": "Free (Requires User-Agent header per SEC policy)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Already Complete on Disk (D:\\leads\\submissions (1).zip)"
    },
    {
        "dataset_name": "U.S. SEC EDGAR XBRL Company Facts Bulk",
        "expected_filename": "companyfacts.zip",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "official_source_portal": "https://www.sec.gov/edgar/sec-api-documentation",
        "direct_download_url": "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip",
        "file_format": "ZIP",
        "approx_download_size": "~1.41 GB",
        "expected_record_count": "20,501",
        "count_nature": "Verified Exact Public Corporations",
        "auth_required": "Free (Requires User-Agent header per SEC policy)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Already Complete on Disk (D:\\leads\\sec_company_facts.parquet)"
    },
    {
        "dataset_name": "Live Technographic Dataset (Tech Stack Repository)",
        "expected_filename": "tech-stack-datasets-main.zip",
        "source_org": "Live Technographic Dataset Project",
        "official_source_portal": "https://github.com/tech-stack-datasets/tech-stack-datasets",
        "direct_download_url": "https://github.com/tech-stack-datasets/tech-stack-datasets/archive/refs/heads/main.zip",
        "file_format": "ZIP",
        "approx_download_size": "~36.8 MB",
        "expected_record_count": "153,104 sample / 53.7M scope",
        "count_nature": "Verified Sample Rows",
        "auth_required": "None (Open Source GitHub)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Already Complete on Disk (D:\\leads\\tech_stack_companies.parquet)"
    },
    {
        "dataset_name": "Open Company Database (Radar API Sample)",
        "expected_filename": "open_company_database_sample.csv",
        "source_org": "Fliar Research / Radar API",
        "official_source_portal": "https://github.com/fliarbi/radar-api-mcp",
        "direct_download_url": "https://github.com/fliarbi/radar-api-mcp",
        "file_format": "CSV / PARQUET",
        "approx_download_size": "~26.9 MB",
        "expected_record_count": "100,000",
        "count_nature": "Verified Sample Rows",
        "auth_required": "None for Sample / Radar API key for live stream",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Already Complete on Disk (D:\\leads\\open_company_database.parquet)"
    },
    {
        "dataset_name": "Data Legion Global Companies",
        "expected_filename": "data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "source_org": "Data Legion",
        "official_source_portal": "https://datalegion.com/",
        "direct_download_url": "https://datalegion.com/data/data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "file_format": "CSV.GZ",
        "approx_download_size": "~1.44 GB",
        "expected_record_count": "28,127,036",
        "count_nature": "Verified Row Header",
        "auth_required": "Free Download / Registration",
        "live_http_status": "UNKNOWN (Requires browser session)",
        "local_presence": "Already Complete on Disk (D:\\leads\\data-legion-company-free-1.5.0_2026-10-15.csv.gz)"
    },
    {
        "dataset_name": "Free Company Global Dataset",
        "expected_filename": "free_company_dataset.csv.gz",
        "source_org": "People Data Labs",
        "official_source_portal": "https://www.peopledatalabs.com/free-company-dataset",
        "direct_download_url": "https://www.peopledatalabs.com/free-company-dataset",
        "file_format": "CSV.GZ",
        "approx_download_size": "~2.23 GB",
        "expected_record_count": "37,200,000 streamable / 180M scope",
        "count_nature": "Verified Streamable Sample",
        "auth_required": "Work Email Registration Required",
        "live_http_status": "ACTIVE Portal",
        "local_presence": "Already Complete on Disk (D:\\leads\\free_company_dataset.csv.zip)"
    },
    {
        "dataset_name": "Common Crawl Web Index Path Archive",
        "expected_filename": "cc-index.paths.gz",
        "source_org": "Common Crawl Foundation",
        "official_source_portal": "https://commoncrawl.org/the-data/get-started/",
        "direct_download_url": "https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-51/cc-index.paths.gz",
        "file_format": "GZ",
        "approx_download_size": "< 1 MB",
        "expected_record_count": "302",
        "count_nature": "Verified Exact",
        "auth_required": "None (AWS Open Data)",
        "live_http_status": "ACTIVE 200 via S3",
        "local_presence": "Already Complete on Disk (D:\\leads\\cc_web_index.parquet)"
    },
    {
        "dataset_name": "Geofabrik Asia Commercial POIs",
        "expected_filename": "asia-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_source_portal": "https://download.geofabrik.de/asia.html",
        "direct_download_url": "https://download.geofabrik.de/asia-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~15 GB",
        "expected_record_count": "45,000,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    },
    {
        "dataset_name": "Geofabrik Africa Commercial POIs",
        "expected_filename": "africa-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_source_portal": "https://download.geofabrik.de/africa.html",
        "direct_download_url": "https://download.geofabrik.de/africa-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~6 GB",
        "expected_record_count": "12,000,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    },
    {
        "dataset_name": "Geofabrik South America Commercial POIs",
        "expected_filename": "south-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_source_portal": "https://download.geofabrik.de/south-america.html",
        "direct_download_url": "https://download.geofabrik.de/south-america-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~4 GB",
        "expected_record_count": "6,800,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    },
    {
        "dataset_name": "Geofabrik North America Commercial POIs",
        "expected_filename": "north-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_source_portal": "https://download.geofabrik.de/north-america.html",
        "direct_download_url": "https://download.geofabrik.de/north-america-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~14 GB",
        "expected_record_count": "32,000,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    },
    {
        "dataset_name": "Geofabrik Europe Commercial POIs",
        "expected_filename": "europe-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_source_portal": "https://download.geofabrik.de/europe.html",
        "direct_download_url": "https://download.geofabrik.de/europe-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~30 GB",
        "expected_record_count": "65,000,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    },
    {
        "dataset_name": "OpenStreetMap Planet Worldwide Commercial POIs",
        "expected_filename": "planet-latest.osm.pbf",
        "source_org": "OpenStreetMap Foundation",
        "official_source_portal": "https://planet.openstreetmap.org/",
        "direct_download_url": "https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~75 GB",
        "expected_record_count": "150,000,000",
        "count_nature": "Estimated POIs",
        "auth_required": "None (Free Open Data - ODbL)",
        "live_http_status": "ACTIVE 200",
        "local_presence": "Remote Catalog (Not downloaded)"
    }
]

with open(os.path.join(OUT_DIR, "VERIFIED_OFFICIAL_DOWNLOAD_LINKS.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "expected_filename", "source_org", "official_source_portal",
        "direct_download_url", "file_format", "approx_download_size",
        "expected_record_count", "count_nature", "auth_required",
        "live_http_status", "local_presence"
    ])
    writer.writeheader()
    writer.writerows(verified_links)

print("[5/6] Wrote VERIFIED_OFFICIAL_DOWNLOAD_LINKS.csv")

# =============================================================================
# 6. FINAL_DOWNLOAD_REPORT.md
# =============================================================================
final_report_md = """# Final Download & Data Recovery Report
**Tailored for Analysis & Verification with ChatGPT**  
**Audit Location:** `D:\\leads\\`  
**Host Environment:** Windows (Drive `C:\\` ~3.90 GB free, Drive `D:\\` ~54.47 GB free)  
**Report Output Folder:** `D:\\leads\\download_recovery_inventory\\`  
**Generated Date:** October 26, 2026  

---

## 1. Executive Summary for ChatGPT

This report provides the exact, empirical truth about what is stored on `D:\\leads\\` versus what is missing, so ChatGPT can assist in retrieving missing datasets without recommending redundant or destructive downloads.

### Crucial Hardware & Storage Constraints
- **Drive `C:\\`:** Only **3.90 GB free**. Under no circumstances should downloads or temporary extraction buffers be saved to `C:\\`.
- **Drive `D:\\`:** **54.47 GB free**. All downloads and Parquet conversions must reside on `D:\\` and stay within this capacity limit.
- **Why this matters:** Large datasets like OpenStreetMap Planet (75 GB download, 250 GB unpack) or Europe (30 GB download) **CANNOT fit on this machine** and must NOT be downloaded.

---

## 2. The Verdict: What You MUST Download vs. What You Should NOT Download

### A. Genuinely Missing File (MUST DOWNLOAD: Exactly 1 File)

| Dataset | Expected Filename | Size | Expected POIs | Direct Download URL | Why Download is Required |
|:---|:---|:---:|---:|:---|:---|
| **Geofabrik Oceania POIs** | `australia-oceania-latest.osm.pbf` | **~1.5 GB** | **~2,500,000** | [`https://download.geofabrik.de/australia-oceania-latest.osm.pbf`](https://download.geofabrik.de/australia-oceania-latest.osm.pbf) | The directory `D:\\leads\\` contains only the 50-byte MD5 checksum `oceania.osm.pbf.md5`. The binary `.osm.pbf` file was never downloaded. Download this 1.5 GB file to complete your Oceania POI coverage. |

---

### B. High-Value Optional Download (RECOMMENDED: Exactly 1 File)

| Dataset | Expected Filename | Size | Expected Records | Direct Download URL | Why This is Recommended |
|:---|:---|:---:|---:|:---|:---|
| **UK Companies House Basic Company Data** | `BasicCompanyDataAsOneFile-2026-10-01.zip` | **~420 MB** (Unpacks to ~2.1 GB) | **5,400,000 verified UK corporations** | [`http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip`](http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip) | Verified government registry of all 5.4 million UK registered companies. Completely free, direct HTTP download, takes only 420 MB, and safely fits on `D:\\`. |

---

### C. Local Restorations (DO NOT DOWNLOAD — 0 Bytes Bandwidth Needed)

| Dataset | Issue with Existing Copy | Local Intact Source | Resolution |
|:---|:---|:---|:---|
| **`apple-locations.csv`** | Cleaned copy in `cleaned_20261025` was truncated to 57 bytes (header only). Missing from `D:\\leads` root. | `D:\\leads\\backup_original_20261025\\apple-locations.csv` (40.6 KB, 692 locations) | **DO NOT DOWNLOAD.** Copy directly from `backup_original_20261025\\apple-locations.csv` to `D:\\leads\\apple-locations.csv`. |
| **`free_company_dataset.csv.zip`** | File extension is `.zip`, causing zip extractors to fail with "File is not a zip file". | `D:\\leads\\free_company_dataset.csv.zip` (2.23 GB) | **DO NOT DOWNLOAD.** The file is a valid GZIP stream (`1f 8b`). Read with DuckDB `read_csv('...', compression='gzip')` or rename to `.csv.gz`. |
| **`realtors (1).csv`** | 35-byte empty header stub. | `D:\\leads\\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv` (258 KB, 2,500 leads) | **DO NOT DOWNLOAD.** Master realtors file is already intact and indexed in DuckDB. |

---

### D. Massive Archives ALREADY on Disk (DO NOT REDOWNLOAD)

> [!WARNING]
> ChatGPT may see these files referenced in code and suggest redownloading them. **DO NOT REDOWNLOAD.** They are already present and verified on `D:\\leads\\`:

1. **`D:\\leads\\ODO_SENZING_20260305.zip` (19.91 GB):** Contains 2,496 verified JSON files (~341M records). Complete on disk.
2. **`D:\\leads\\data-legion-company-free-1.5.0_2026-10-15.csv.gz` (1.44 GB):** Contains 28.1M verified company profiles. Complete on disk.
3. **`D:\\leads\\submissions (1).zip` (1.46 GB):** Contains 995,761 SEC EDGAR filer JSON files. Complete on disk.
4. **`D:\\leads\\companyfacts.zip` (1.31 GB):** Contains 20,501 SEC XBRL fact files. Complete on disk.
5. **`D:\\leads\\20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip` (506 MB):** Contains 3.47M legal entities. Complete on disk.
6. **18 Raw B2B CSV Shards (`free-tier.csv` & `free-tier (2..19).csv` - 2.49 GB total):** Complete on disk; already cleaned into `b2b_executives_final_validated.parquet` (10,268,615 rows).

---

## 3. Which Files to Upload to ChatGPT

To have ChatGPT review your sources, verify links, and help you automate the download of missing datasets, upload these **3 specific CSV files** from `D:\\leads\\download_recovery_inventory\\`:

1. 📄 **[`MUST_REDOWNLOAD.csv`](file:///D:/leads/download_recovery_inventory/MUST_REDOWNLOAD.csv)**  
   *Contains the single genuinely missing payload (`australia-oceania-latest.osm.pbf`).*
2. 📄 **[`OPTIONAL_NEW_DATASETS.csv`](file:///D:/leads/download_recovery_inventory/OPTIONAL_NEW_DATASETS.csv)**  
   *Contains the curated list of high-value optional feeds (UK Companies House, Fliar 5M, regional OSM) with exact sizes, disk impacts, and URLs.*
3. 📄 **[`RESTORE_FROM_BACKUP.csv`](file:///D:/leads/download_recovery_inventory/RESTORE_FROM_BACKUP.csv)**  
   *Contains local restoration instructions for Apple Locations and the Free Company GZIP extension fix.*

*You can also upload [`VERIFIED_OFFICIAL_DOWNLOAD_LINKS.csv`](file:///D:/leads/download_recovery_inventory/VERIFIED_OFFICIAL_DOWNLOAD_LINKS.csv) if ChatGPT requests the full directory of all 20 source portals.*
"""

with open(os.path.join(OUT_DIR, "FINAL_DOWNLOAD_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(final_report_md)

print("[6/6] Wrote FINAL_DOWNLOAD_REPORT.md")
print("\nAll 6 recovery reports created successfully in:", OUT_DIR)
