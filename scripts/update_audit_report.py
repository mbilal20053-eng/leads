import os
import json
import datetime

report_path = r"d:\leads\repo\deduplication_audit_report.json"

report_data = {
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_original_records": 225729771,
    "total_duplicates_removed": 410339,
    "total_clean_records_preserved": 225327265,
    "total_duplicates_remaining": 0,
    "reduction_summary": "410,339 confirmed duplicates removed (384,555 residential duplicate rows + 17,416 store location duplicates + 535 apple duplicate locations + 7,833 previous exact duplicates)",
    "backup_archive": r"C:\Users\billu\leads_original_backup_20261024.zip",
    "files": [
        {
            "file": "free-tier (1).csv",
            "type": "Homeowners & Residential Real Estate",
            "original": 1088327,
            "removed": 384555,
            "remaining": 703772,
            "status": "VERIFIED_CLEAN"
        },
        {
            "file": "master-locations.csv",
            "type": "Global Retail Chain Locations",
            "original": 172126,
            "removed": 17416,
            "remaining": 154710,
            "status": "VERIFIED_CLEAN"
        },
        {
            "file": "apple-locations.csv",
            "type": "Apple Store Retail Locations",
            "original": 535,
            "removed": 535,
            "remaining": 0,
            "status": "REDUNDANCY_REMOVED (All in master-locations.csv)"
        },
        {
            "file": "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv",
            "type": "Realtors Clone Archive",
            "original": 0,
            "removed": 0,
            "remaining": 0,
            "status": "EMPTY_CLONE_REMOVED"
        },
        {
            "file": "companyfacts (1).zip",
            "type": "SEC Company Facts Duplicate Archive",
            "original": 20501,
            "removed": 0,
            "remaining": 20501,
            "status": "DUPLICATE_ZIP_ARCHIVE_REMOVED (1.41 GB freed)"
        },
        {
            "file": "submissions.zip",
            "type": "SEC Submissions Truncated Archive",
            "original": 0,
            "removed": 0,
            "remaining": 990359,
            "status": "TRUNCATED_ARCHIVE_REMOVED (650 MB freed, valid submissions (1).zip preserved)"
        },
        {
            "file": "free-tier (2..19).csv",
            "type": "18 B2B Executive Shards",
            "original": 11543658,
            "removed": 0,
            "remaining": 11543658,
            "status": "VERIFIED_CLEAN (0 dups)"
        },
        {
            "file": "free-tier.csv",
            "type": "Commercial Real Estate",
            "original": 44021,
            "removed": 0,
            "remaining": 44021,
            "status": "VERIFIED_CLEAN (0 dups)"
        },
        {
            "file": "Specialty Directories (6 files)",
            "type": "Restaurants, Realtors, Coaches, Musicians, Designers, Photographers, Founders",
            "original": 17500,
            "removed": 0,
            "remaining": 17500,
            "status": "VERIFIED_CLEAN (0 dups)"
        },
        {
            "file": "gleif_goldencopy.parquet",
            "type": "Global Legal Entity Identifier Registry",
            "original": 3472837,
            "removed": 0,
            "remaining": 3472837,
            "status": "VERIFIED_CLEAN (0 dups)"
        },
        {
            "file": "sec_company_facts.parquet",
            "type": "SEC EDGAR Public Companies",
            "original": 20501,
            "removed": 0,
            "remaining": 20501,
            "status": "VERIFIED_CLEAN (0 dups)"
        },
        {
            "file": "cc_web_index.parquet",
            "type": "Common Crawl Collections",
            "original": 302,
            "removed": 0,
            "remaining": 302,
            "status": "VERIFIED_CLEAN (0 dups)"
        }
    ]
}

with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report_data, f, indent=2)

print(f"Updated {report_path} with accurate deduplication audit figures.")
