import os
import csv

OUT_DIR = r"D:\leads\download_recovery_inventory"
os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. all_datasets_inventory.csv
# -----------------------------------------------------------------------------
all_datasets = [
    # Production Active Datasets
    {
        "dataset_name": "B2B Executive Decision Makers (Cleaned & Validated)",
        "local_path": r"D:\leads\cleaned_export\b2b_executives_final_validated.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "723.27",
        "file_size_bytes": "758399099",
        "original_download_url": "UNKNOWN (Consolidated from 18 raw CSV shards free-tier.csv)",
        "official_source_website": "Internal Consolidated Shards Pipeline",
        "source_org": "B2B Lead Intelligence Consortium",
        "actual_verified_rows": "10,268,615",
        "expected_rows": "10,268,615",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_b2b_executives)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "B2B Raw Shards Consolidated Cleaned",
        "local_path": r"D:\leads\cleaned_export\b2b_raw_shards_consolidated_cleaned.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "571.01",
        "file_size_bytes": "598747060",
        "original_download_url": "UNKNOWN (Consolidated from 18 raw CSV shards free-tier.csv)",
        "official_source_website": "Internal Shards Pipeline",
        "source_org": "B2B Lead Intelligence Consortium",
        "actual_verified_rows": "10,268,615",
        "expected_rows": "10,268,615",
        "file_status": "Complete",
        "in_production_db": "Derived Table Reference",
        "dataset_lineage": "Cleaned Intermediate Parquet"
    },
    {
        "dataset_name": "B2B Executives Pre-Validation Master",
        "local_path": r"D:\leads\b2b_executives.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "791.38",
        "file_size_bytes": "829822596",
        "original_download_url": "UNKNOWN (Historical uncleaned parquet)",
        "official_source_website": "Internal Pipeline",
        "source_org": "B2B Lead Intelligence Consortium",
        "actual_verified_rows": "11,543,658",
        "expected_rows": "11,543,658",
        "file_status": "Complete (Unfiltered)",
        "in_production_db": "NO (Superseeded by final validated parquet)",
        "dataset_lineage": "Raw Pre-cleanup Parquet"
    },
    {
        "dataset_name": "GLEIF Golden Copy Legal Entity Registry (Parquet)",
        "local_path": r"D:\leads\gleif_goldencopy.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "493.82",
        "file_size_bytes": "517812527",
        "original_download_url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest/lei2/csv",
        "official_source_website": "https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy",
        "source_org": "Global Legal Entity Identifier Foundation (GLEIF)",
        "actual_verified_rows": "3,472,837",
        "expected_rows": "3,472,837",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_gleif_goldencopy)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "GLEIF Golden Copy LEI-2 Raw Zip Archive",
        "local_path": r"D:\leads\20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip",
        "file_format": "CSV.ZIP",
        "file_size_mb": "482.78",
        "file_size_bytes": "506227073",
        "original_download_url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest/lei2/csv",
        "official_source_website": "https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy",
        "source_org": "Global Legal Entity Identifier Foundation (GLEIF)",
        "actual_verified_rows": "3,472,837",
        "expected_rows": "3,472,837",
        "file_status": "Complete (Raw Archive)",
        "in_production_db": "NO (Extracted & converted to parquet)",
        "dataset_lineage": "Raw Download Archive"
    },
    {
        "dataset_name": "Homeowners & Residential Property Leads (Parquet)",
        "local_path": r"D:\leads\homeowners.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "14.05",
        "file_size_bytes": "14736559",
        "original_download_url": "UNKNOWN (Converted from raw free-tier (1).csv)",
        "official_source_website": "National Property Registry / Real Estate Tax Records",
        "source_org": "County Assessor / Property Registry Feeds",
        "actual_verified_rows": "703,772",
        "expected_rows": "703,772",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_homeowners)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "Homeowners & Residential Property Leads (Raw CSV)",
        "local_path": r"D:\leads\free-tier (1).csv",
        "file_format": "CSV",
        "file_size_mb": "78.92",
        "file_size_bytes": "82752021",
        "original_download_url": "UNKNOWN",
        "official_source_website": "County Assessor / Property Registry Feeds",
        "source_org": "County Assessor Feeds",
        "actual_verified_rows": "703,772",
        "expected_rows": "703,772",
        "file_status": "Complete (Raw Source)",
        "in_production_db": "Converted to homeowners.parquet",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Retail, Commercial & Franchise Locations",
        "local_path": r"D:\leads\master-locations.csv",
        "file_format": "CSV",
        "file_size_mb": "10.91",
        "file_size_bytes": "11440682",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Master Location Intelligence",
        "source_org": "Commercial Store Location Registry",
        "actual_verified_rows": "154,710",
        "expected_rows": "154,710",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_master_locations)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Retail, Commercial Locations (Backup Zip)",
        "local_path": r"D:\leads\master-locations.zip",
        "file_format": "ZIP",
        "file_size_mb": "2.38",
        "file_size_bytes": "2492983",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Commercial Store Location Registry",
        "source_org": "Commercial Store Location Registry",
        "actual_verified_rows": "154,710",
        "expected_rows": "154,710",
        "file_status": "Complete Archive",
        "in_production_db": "CSV imported directly",
        "dataset_lineage": "Backup Archive"
    },
    {
        "dataset_name": "Apple Retail Locations (Backup Original)",
        "local_path": r"D:\leads\backup_original_20261025\apple-locations.csv",
        "file_format": "CSV",
        "file_size_mb": "0.04",
        "file_size_bytes": "40649",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Apple Store Location Intelligence",
        "source_org": "Apple Inc. Global Retail Feeds",
        "actual_verified_rows": "692",
        "expected_rows": "692",
        "file_status": "Complete in Backup (Missing from root D:\\leads)",
        "in_production_db": "NO (Missing from active unified view)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Apple Retail Locations (Truncated Cleaned Copy)",
        "local_path": r"D:\leads\cleaned_20261025\apple-locations.csv",
        "file_format": "CSV",
        "file_size_mb": "0.00",
        "file_size_bytes": "57",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Apple Inc. Global Retail Feeds",
        "source_org": "Apple Inc. Global Retail Feeds",
        "actual_verified_rows": "0",
        "expected_rows": "692",
        "file_status": "Incomplete / Truncated (Header Only)",
        "in_production_db": "NO",
        "dataset_lineage": "Corrupted / Incomplete Artifact"
    },
    {
        "dataset_name": "Tech Stack & Software Intelligence Companies (Parquet)",
        "local_path": r"D:\leads\tech_stack_companies.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "18.65",
        "file_size_bytes": "19554452",
        "original_download_url": "https://github.com/tech-stack-datasets/tech-stack-datasets",
        "official_source_website": "https://github.com/tech-stack-datasets/tech-stack-datasets",
        "source_org": "Live Technographic Dataset Project",
        "actual_verified_rows": "153,104",
        "expected_rows": "153,104 (Compiled from 100+ technology samples)",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_tech_stack_leads)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "Tech Stack Datasets Main (Zip Archive)",
        "local_path": r"D:\leads\tech-stack-datasets.zip",
        "file_format": "ZIP",
        "file_size_mb": "35.06",
        "file_size_bytes": "36766038",
        "original_download_url": "https://github.com/tech-stack-datasets/tech-stack-datasets/archive/refs/heads/main.zip",
        "official_source_website": "https://github.com/tech-stack-datasets/tech-stack-datasets",
        "source_org": "Live Technographic Dataset Project",
        "actual_verified_rows": "153,104",
        "expected_rows": "53,700,000 (Declared project scope)",
        "file_status": "Complete Sample Repository Archive",
        "in_production_db": "Compiled into tech_stack_companies.parquet",
        "dataset_lineage": "Raw Download Archive"
    },
    {
        "dataset_name": "Open Company Database Sample (Parquet)",
        "local_path": r"D:\leads\open_company_database.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "8.22",
        "file_size_bytes": "8618037",
        "original_download_url": "https://github.com/fliarbi/radar-api-mcp",
        "official_source_website": "https://github.com/fliarbi/radar-api-mcp",
        "source_org": "Fliar Research / Radar API",
        "actual_verified_rows": "100,000",
        "expected_rows": "100,000 (Sample of 5M full dataset)",
        "file_status": "Complete Sample",
        "in_production_db": "YES (v_all_unified, v_open_company_db)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "Open Company Database Sample (Raw CSV)",
        "local_path": r"D:\leads\open_company_database_sample.csv",
        "file_format": "CSV",
        "file_size_mb": "26.01",
        "file_size_bytes": "27272387",
        "original_download_url": "https://github.com/fliarbi/radar-api-mcp",
        "official_source_website": "https://github.com/fliarbi/radar-api-mcp",
        "source_org": "Fliar Research / Radar API",
        "actual_verified_rows": "100,000",
        "expected_rows": "5,000,000 (Full dataset scope)",
        "file_status": "Complete Sample (Full 5M not downloaded)",
        "in_production_db": "Converted to open_company_database.parquet",
        "dataset_lineage": "Raw Source Sample"
    },
    {
        "dataset_name": "Commercial Real Estate B2B Companies",
        "local_path": r"D:\leads\free-tier.csv",
        "file_format": "CSV",
        "file_size_mb": "5.55",
        "file_size_bytes": "5822235",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Commercial Real Estate Database Feeds",
        "source_org": "CRE Lead Distribution Network",
        "actual_verified_rows": "44,021",
        "expected_rows": "44,021",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_realestate_b2b)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Facts (Parquet)",
        "local_path": r"D:\leads\sec_company_facts.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "1.65",
        "file_size_bytes": "1734152",
        "original_download_url": "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip",
        "official_source_website": "https://www.sec.gov/edgar/sec-api-documentation",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "actual_verified_rows": "20,501",
        "expected_rows": "20,501",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_sec_company_facts)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "U.S. SEC EDGAR Company Facts Bulk Archive",
        "local_path": r"D:\leads\companyfacts.zip",
        "file_format": "ZIP",
        "file_size_mb": "1346.13",
        "file_size_bytes": "1411517904",
        "original_download_url": "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip",
        "official_source_website": "https://www.sec.gov/edgar/sec-api-documentation",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "actual_verified_rows": "20,501 files",
        "expected_rows": "20,501",
        "file_status": "Complete Archive",
        "in_production_db": "Extracted & converted to sec_company_facts.parquet",
        "dataset_lineage": "Raw Download Archive"
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Submissions Bulk Archive",
        "local_path": r"D:\leads\submissions (1).zip",
        "file_format": "ZIP",
        "file_size_mb": "1498.22",
        "file_size_bytes": "1570993018",
        "original_download_url": "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip",
        "official_source_website": "https://www.sec.gov/edgar/sec-api-documentation",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "actual_verified_rows": "995,761 files",
        "expected_rows": "990,359 - 1,000,000",
        "file_status": "Complete Archive (Unextracted)",
        "in_production_db": "NO (Unprocessed local archive)",
        "dataset_lineage": "Raw Download Archive"
    },
    {
        "dataset_name": "Common Crawl Web Index (Parquet)",
        "local_path": r"D:\leads\cc_web_index.parquet",
        "file_format": "PARQUET",
        "file_size_mb": "0.02",
        "file_size_bytes": "20717",
        "original_download_url": "https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-51/cc-index.paths.gz",
        "official_source_website": "https://commoncrawl.org/the-data/get-started/",
        "source_org": "Common Crawl Foundation",
        "actual_verified_rows": "302",
        "expected_rows": "302",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_cc_web_index)",
        "dataset_lineage": "Cleaned Derived Parquet"
    },
    {
        "dataset_name": "Common Crawl Web Index Path Archive",
        "local_path": r"D:\leads\cc-index.paths.gz",
        "file_format": "GZ",
        "file_size_mb": "0.00",
        "file_size_bytes": "637",
        "original_download_url": "https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-51/cc-index.paths.gz",
        "official_source_website": "https://commoncrawl.org/the-data/get-started/",
        "source_org": "Common Crawl Foundation",
        "actual_verified_rows": "302",
        "expected_rows": "302",
        "file_status": "Complete",
        "in_production_db": "Converted to cc_web_index.parquet",
        "dataset_lineage": "Raw Download Archive"
    },
    # 7 Targeted Professional Verticals
    {
        "dataset_name": "Restaurants & Hospitality Specialists",
        "local_path": r"D:\leads\050580a4-d0ee-43eb-94e0-a2ac1577ee9a-restaurants.csv",
        "file_format": "CSV",
        "file_size_mb": "0.22",
        "file_size_bytes": "227884",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_restaurants)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Licensed Realtors & Real Estate Brokers",
        "local_path": r"D:\leads\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv",
        "file_format": "CSV",
        "file_size_mb": "0.25",
        "file_size_bytes": "258526",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_realtors)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Realtors Empty Stub File (Artifact)",
        "local_path": r"D:\leads\backup_original_20261025\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv",
        "file_format": "CSV",
        "file_size_mb": "0.00",
        "file_size_bytes": "35",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "0",
        "expected_rows": "2,500",
        "file_status": "Incomplete / Empty Stub (Header Only)",
        "in_production_db": "NO",
        "dataset_lineage": "Corrupted / Incomplete Artifact"
    },
    {
        "dataset_name": "Executive Coaches & Strategic Mentors",
        "local_path": r"D:\leads\166ff949-5ac5-43a5-874c-6ccdf14f94af-coaches.csv",
        "file_format": "CSV",
        "file_size_mb": "0.22",
        "file_size_bytes": "234026",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_coaches)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Creative Designers, UI/UX & Brand Studios",
        "local_path": r"D:\leads\94f26329-7f91-4ff4-9430-deff3d129bd2-designers.csv",
        "file_format": "CSV",
        "file_size_mb": "0.22",
        "file_size_bytes": "229288",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_designers)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Entrepreneurs, Founders & Tech Startups",
        "local_path": r"D:\leads\b0d3b766-20ad-4e62-b9f6-d45f9fc8e24e-entrepreneurs.csv",
        "file_format": "CSV",
        "file_size_mb": "0.22",
        "file_size_bytes": "232627",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_entrepreneurs)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Professional Photographers & Studios",
        "local_path": r"D:\leads\da6aeb15-b193-4675-891a-47b95f49e24e-photographers.csv",
        "file_format": "CSV",
        "file_size_mb": "0.22",
        "file_size_bytes": "231457",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_photographers)",
        "dataset_lineage": "Raw Source CSV"
    },
    {
        "dataset_name": "Musicians, Audio Engineers & Producers",
        "local_path": r"D:\leads\74b7d278-90bf-45bd-8043-5a95beff12e8-musicians.csv",
        "file_format": "CSV",
        "file_size_mb": "0.21",
        "file_size_bytes": "222352",
        "original_download_url": "UNKNOWN",
        "official_source_website": "Vertical Industry Lead Engine",
        "source_org": "Targeted Business Intelligence",
        "actual_verified_rows": "2,500",
        "expected_rows": "2,500",
        "file_status": "Complete & Validated",
        "in_production_db": "YES (v_all_unified, v_musicians)",
        "dataset_lineage": "Raw Source CSV"
    },
    # Large Local Compressed Archives (Unprocessed in DB)
    {
        "dataset_name": "ODO Senzing Global Entity Intelligence Archive",
        "local_path": r"D:\leads\ODO_SENZING_20260305.zip",
        "file_format": "ZIP",
        "file_size_mb": "20387.90",
        "file_size_bytes": "21378254323",
        "original_download_url": "UNKNOWN (BrightQuery bulk entity release)",
        "official_source_website": "https://senzing.com/ / Open Data Online (ODO)",
        "source_org": "Senzing / BrightQuery Entity Intelligence",
        "actual_verified_rows": "2,496 JSON files",
        "expected_rows": "341,000,000",
        "file_status": "Complete Archive (Unextracted)",
        "in_production_db": "NO (Preserved compressed on disk)",
        "dataset_lineage": "Raw Download Archive"
    },
    {
        "dataset_name": "Free Company Global Dataset Archive",
        "local_path": r"D:\leads\free_company_dataset.csv.zip",
        "file_format": "CSV.GZ (Misnamed as .zip)",
        "file_size_mb": "2281.29",
        "file_size_bytes": "2392105978",
        "original_download_url": "https://www.peopledatalabs.com/free-company-dataset",
        "official_source_website": "https://www.peopledatalabs.com/free-company-dataset",
        "source_org": "People Data Labs Open Datasets",
        "actual_verified_rows": "37,200,000 streamable",
        "expected_rows": "180,000,000 (Declared)",
        "file_status": "Complete GZIP stream (Misnamed file extension)",
        "in_production_db": "NO (Preserved compressed on disk)",
        "dataset_lineage": "Raw Download Archive"
    },
    {
        "dataset_name": "Data Legion Global Companies Archive",
        "local_path": r"D:\leads\data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "file_format": "CSV.GZ",
        "file_size_mb": "1474.93",
        "file_size_bytes": "1546579617",
        "original_download_url": "https://datalegion.com/data/data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "official_source_website": "https://datalegion.com/",
        "source_org": "Data Legion Intelligence",
        "actual_verified_rows": "28,127,036",
        "expected_rows": "28,127,036",
        "file_status": "Complete GZIP Archive",
        "in_production_db": "NO (Preserved compressed on disk)",
        "dataset_lineage": "Raw Download Archive"
    },
    # Missing binary file with checksum present
    {
        "dataset_name": "Geofabrik Oceania OSM POIs (Checksum only)",
        "local_path": r"D:\leads\oceania.osm.pbf.md5",
        "file_format": "MD5 CHECKSUM",
        "file_size_mb": "0.00",
        "file_size_bytes": "50",
        "original_download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        "official_source_website": "https://download.geofabrik.de/oceania.html",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "actual_verified_rows": "0 (Binary missing)",
        "expected_rows": "2,500,000",
        "file_status": "Missing Binary (Only 50-byte MD5 checksum exists)",
        "in_production_db": "NO",
        "dataset_lineage": "Missing Download Payload"
    },
    # Remote Unfetched Datasets
    {
        "dataset_name": "OSM Planet Worldwide Commercial POIs",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "OSM.PBF",
        "file_size_mb": "76800.00 (Est. ~75 GB)",
        "file_size_bytes": "80530636800",
        "original_download_url": "https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf",
        "official_source_website": "https://planet.openstreetmap.org/",
        "source_org": "OpenStreetMap Foundation",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "150,000,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    },
    {
        "dataset_name": "OSM Europe Commercial POIs",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "OSM.PBF",
        "file_size_mb": "30720.00 (Est. ~30 GB)",
        "file_size_bytes": "32212254720",
        "original_download_url": "https://download.geofabrik.de/europe-latest.osm.pbf",
        "official_source_website": "https://download.geofabrik.de/europe.html",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "65,000,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    },
    {
        "dataset_name": "OSM Asia Commercial POIs",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "OSM.PBF",
        "file_size_mb": "15360.00 (Est. ~15 GB)",
        "file_size_bytes": "16106127360",
        "original_download_url": "https://download.geofabrik.de/asia-latest.osm.pbf",
        "official_source_website": "https://download.geofabrik.de/asia.html",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "45,000,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    },
    {
        "dataset_name": "People Data Labs B2B Catalog Feed",
        "local_path": "REMOTE (API Endpoint)",
        "file_format": "JSON API",
        "file_size_mb": "N/A (API Stream)",
        "file_size_bytes": "0",
        "original_download_url": "https://api.peopledatalabs.com/v5/company/enrich",
        "official_source_website": "https://www.peopledatalabs.com/",
        "source_org": "People Data Labs Inc.",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "32,334,356",
        "file_status": "Remote API Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote API Feed"
    },
    {
        "dataset_name": "OSM North America Commercial POIs",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "OSM.PBF",
        "file_size_mb": "14336.00 (Est. ~14 GB)",
        "file_size_bytes": "15032385536",
        "original_download_url": "https://download.geofabrik.de/north-america-latest.osm.pbf",
        "official_source_website": "https://download.geofabrik.de/north-america.html",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "32,000,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    },
    {
        "dataset_name": "OSM Africa Commercial POIs",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "OSM.PBF",
        "file_size_mb": "6144.00 (Est. ~6 GB)",
        "file_size_bytes": "6442450944",
        "original_download_url": "https://download.geofabrik.de/africa-latest.osm.pbf",
        "official_source_website": "https://download.geofabrik.de/africa.html",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "12,000,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    },
    {
        "dataset_name": "OSM South America Commercial POIs",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "OSM.PBF",
        "file_size_mb": "4096.00 (Est. ~4 GB)",
        "file_size_bytes": "4294967296",
        "original_download_url": "https://download.geofabrik.de/south-america-latest.osm.pbf",
        "official_source_website": "https://download.geofabrik.de/south-america.html",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "6,800,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    },
    {
        "dataset_name": "UK Companies House Basic Company Data",
        "local_path": "REMOTE (Not downloaded to local disk)",
        "file_format": "CSV.ZIP",
        "file_size_mb": "420.00 (Est. ~420 MB)",
        "file_size_bytes": "440401920",
        "original_download_url": "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip",
        "official_source_website": "http://download.companieshouse.gov.uk/en_output.html",
        "source_org": "Companies House (UK Government)",
        "actual_verified_rows": "0 (Unfetched)",
        "expected_rows": "5,400,000",
        "file_status": "Remote Unfetched Feed",
        "in_production_db": "NO",
        "dataset_lineage": "Remote Catalog Endpoint"
    }
]

# Write all_datasets_inventory.csv
with open(os.path.join(OUT_DIR, "all_datasets_inventory.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "local_path", "file_format", "file_size_mb", "file_size_bytes",
        "original_download_url", "official_source_website", "source_org",
        "actual_verified_rows", "expected_rows", "file_status", "in_production_db", "dataset_lineage"
    ])
    writer.writeheader()
    writer.writerows(all_datasets)

print("[1/7] Wrote all_datasets_inventory.csv")

# -----------------------------------------------------------------------------
# 2. datasets_to_redownload.csv
# -----------------------------------------------------------------------------
# Critical Rule: Do not recommend downloading files that already exist on disk!
datasets_to_redownload = [
    {
        "dataset_name": "Geofabrik Oceania OpenStreetMap Commercial POIs",
        "filename": "australia-oceania-latest.osm.pbf",
        "priority": "HIGH (Missing Payload)",
        "recommended_action": "DOWNLOAD REQUIRED if Oceania coverage is desired",
        "reason": "Only the 50-byte MD5 checksum (oceania.osm.pbf.md5) exists in D:\\leads. The actual data payload was never downloaded.",
        "official_download_page": "https://download.geofabrik.de/oceania.html",
        "direct_download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "download_size": "~1.5 GB",
        "expected_records": "2,500,000 (Estimate)",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_status": "ACTIVE 200"
    },
    {
        "dataset_name": "UK Companies House Basic Company Data",
        "filename": "BasicCompanyDataAsOneFile-2026-10-01.zip",
        "priority": "MEDIUM (High-Value Business Registry)",
        "recommended_action": "OPTIONAL DOWNLOAD (Fits easily in disk free space: ~420 MB download -> ~2 GB uncompressed)",
        "reason": "Configured in catalog (5.4M companies) but not present on disk. Official bulk download is free and active.",
        "official_download_page": "http://download.companieshouse.gov.uk/en_output.html",
        "direct_download_url": "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip",
        "source_org": "Companies House (UK Government)",
        "download_size": "~420 MB",
        "expected_records": "5,400,000 (Verified Government Registry)",
        "auth_required": "None (Free Open Government Licence)",
        "url_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Open Company Database Full Release (5M Companies)",
        "filename": "open_company_database_5m.parquet",
        "priority": "LOW / OPTIONAL",
        "recommended_action": "OPTIONAL EXPANSION (Current local 100k sample is already fully processed in production)",
        "reason": "Only a 100k sample is stored locally. Full 5M release requires querying or batch export from Fliar Radar API.",
        "official_download_page": "https://github.com/fliarbi/radar-api-mcp",
        "direct_download_url": "https://github.com/fliarbi/radar-api-mcp",
        "source_org": "Fliar Research",
        "download_size": "~450 MB Parquet",
        "expected_records": "5,000,000 (Estimate)",
        "auth_required": "Free Open Source / Radar API Key for real-time enrich",
        "url_status": "ACTIVE 200"
    },
    {
        "dataset_name": "DO NOT REDOWNLOAD: ODO Senzing 341M Entity Archive",
        "filename": "ODO_SENZING_20260305.zip",
        "priority": "NO DOWNLOAD (Already Exists Locally)",
        "recommended_action": "DO NOT DOWNLOAD. Process locally using streaming JSON converter.",
        "reason": "A 19.91 GB archive containing 2,496 verified JSON files is ALREADY present on D:\\leads. Redownloading would waste 20 GB of bandwidth.",
        "official_download_page": "https://senzing.com/",
        "direct_download_url": "UNKNOWN (Internal Bulk Release)",
        "source_org": "Senzing / BrightQuery",
        "download_size": "21.38 GB",
        "expected_records": "341,000,000",
        "auth_required": "Commercial / Bulk License",
        "url_status": "Already on Local Disk"
    },
    {
        "dataset_name": "DO NOT REDOWNLOAD: Free Company Dataset Archive",
        "filename": "free_company_dataset.csv.zip",
        "priority": "NO DOWNLOAD (Already Exists Locally)",
        "recommended_action": "DO NOT DOWNLOAD. Rename extension or stream directly as gzip.",
        "reason": "A 2.23 GB archive is ALREADY present on D:\\leads. The file is actually in GZIP format. It does not need to be downloaded again.",
        "official_download_page": "https://www.peopledatalabs.com/free-company-dataset",
        "direct_download_url": "https://www.peopledatalabs.com/free-company-dataset",
        "source_org": "People Data Labs",
        "download_size": "2.23 GB",
        "expected_records": "180,000,000 declared / 37.2M streamable",
        "auth_required": "Free Registration",
        "url_status": "Already on Local Disk"
    },
    {
        "dataset_name": "DO NOT REDOWNLOAD: Data Legion Global Companies",
        "filename": "data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "priority": "NO DOWNLOAD (Already Exists Locally)",
        "recommended_action": "DO NOT DOWNLOAD. Convert to Parquet directly from local gz file.",
        "reason": "A 1.44 GB gzip file containing 28.1M verified company profiles is ALREADY present on D:\\leads.",
        "official_download_page": "https://datalegion.com/",
        "direct_download_url": "https://datalegion.com/data/data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "source_org": "Data Legion",
        "download_size": "1.44 GB",
        "expected_records": "28,127,036",
        "auth_required": "Free Download",
        "url_status": "Already on Local Disk"
    },
    {
        "dataset_name": "DO NOT REDOWNLOAD: U.S. SEC EDGAR Submissions Bulk",
        "filename": "submissions (1).zip",
        "priority": "NO DOWNLOAD (Already Exists Locally)",
        "recommended_action": "DO NOT DOWNLOAD. Extract or stream JSON files directly from local zip.",
        "reason": "A 1.46 GB zip file containing 995,761 verified JSON corporate files is ALREADY present on D:\\leads.",
        "official_download_page": "https://www.sec.gov/edgar/sec-api-documentation",
        "direct_download_url": "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip",
        "source_org": "U.S. Securities and Exchange Commission",
        "download_size": "1.46 GB",
        "expected_records": "995,761",
        "auth_required": "Free (Requires User-Agent header)",
        "url_status": "Already on Local Disk"
    }
]

with open(os.path.join(OUT_DIR, "datasets_to_redownload.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "filename", "priority", "recommended_action", "reason",
        "official_download_page", "direct_download_url", "source_org",
        "download_size", "expected_records", "auth_required", "url_status"
    ])
    writer.writeheader()
    writer.writerows(datasets_to_redownload)

print("[2/7] Wrote datasets_to_redownload.csv")

# -----------------------------------------------------------------------------
# 3. unprocessed_local_archives.csv
# -----------------------------------------------------------------------------
unprocessed_archives = [
    {
        "dataset_name": "ODO Senzing Global Entity Intelligence",
        "filename": "ODO_SENZING_20260305.zip",
        "local_path": r"D:\leads\ODO_SENZING_20260305.zip",
        "file_format": "ZIP (2,496 JSON files)",
        "size_mb": "20,387.90",
        "size_gb": "19.91",
        "declared_records": "341,000,000",
        "can_be_processed_locally": "YES (Via streamed batch ingestion)",
        "disk_space_required": "~60-80 GB uncompressed (Currently 54.47 GB free)",
        "blocking_reason": "High storage footprint. Full extraction would exhaust current 54.47 GB free space.",
        "recommended_processing_method": "Process zip in streaming batches of 50 JSON files at a time into DuckDB or compress into compact Parquet."
    },
    {
        "dataset_name": "Free Company Global Dataset Archive",
        "filename": "free_company_dataset.csv.zip",
        "local_path": r"D:\leads\free_company_dataset.csv.zip",
        "file_format": "GZIP (Misnamed as .zip)",
        "size_mb": "2,281.29",
        "size_gb": "2.23",
        "declared_records": "180,000,000 declared / 37,200,000 streamable",
        "can_be_processed_locally": "YES",
        "disk_space_required": "~15-20 GB uncompressed",
        "blocking_reason": "Zip extension confusion; not yet converted into production Parquet format.",
        "recommended_processing_method": "Stream through DuckDB read_csv('free_company_dataset.csv.zip', compression='gzip') directly into Parquet with column projection."
    },
    {
        "dataset_name": "Data Legion Global Companies Archive",
        "filename": "data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "local_path": r"D:\leads\data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "file_format": "CSV.GZ",
        "size_mb": "1,474.93",
        "size_gb": "1.44",
        "declared_records": "28,127,036",
        "can_be_processed_locally": "YES",
        "disk_space_required": "~10 GB uncompressed",
        "blocking_reason": "Not yet converted into a indexed DuckDB production Parquet view.",
        "recommended_processing_method": "Execute DuckDB COPY to parquet: COPY (SELECT legion_id, name, domain, industry, size, locality, country FROM read_csv('...gz')) TO 'data_legion.parquet'."
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Submissions Archive",
        "filename": "submissions (1).zip",
        "local_path": r"D:\leads\submissions (1).zip",
        "file_format": "ZIP (995,761 JSON files)",
        "size_mb": "1,498.22",
        "size_gb": "1.46",
        "declared_records": "995,761 corporate filers",
        "can_be_processed_locally": "YES",
        "disk_space_required": "~8-12 GB uncompressed",
        "blocking_reason": "Individual JSON files need extraction and schema flattening into a unified table.",
        "recommended_processing_method": "Run Python worker to extract 'cik', 'name', 'sic', 'sicDescription', 'stateOfIncorporation', 'ein' into sec_edgar_filers.parquet."
    },
    {
        "dataset_name": "18 Raw Downloads Shards (free-tier 2 to 19)",
        "filename": "free-tier (2..19).csv",
        "local_path": r"D:\leads\free-tier (*).csv",
        "file_format": "CSV (18 Files)",
        "size_mb": "2,492.50",
        "size_gb": "2.43",
        "declared_records": "11,833,267",
        "can_be_processed_locally": "YES (Already Cleaned into b2b_executives_final_validated.parquet)",
        "disk_space_required": "None (Already on disk)",
        "blocking_reason": "Raw files contain duplicate join artifacts, dirty phone numbers, and placeholder names.",
        "recommended_processing_method": "Keep raw files as historical immutable backup. Use b2b_executives_final_validated.parquet for all production queries."
    }
]

with open(os.path.join(OUT_DIR, "unprocessed_local_archives.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "filename", "local_path", "file_format", "size_mb", "size_gb",
        "declared_records", "can_be_processed_locally", "disk_space_required",
        "blocking_reason", "recommended_processing_method"
    ])
    writer.writeheader()
    writer.writerows(unprocessed_archives)

print("[3/7] Wrote unprocessed_local_archives.csv")

# -----------------------------------------------------------------------------
# 4. remote_unfetched_datasets.csv
# -----------------------------------------------------------------------------
remote_datasets = [
    {
        "dataset_name": "OpenStreetMap Planet Commercial POIs",
        "region_feed": "Global (Worldwide)",
        "declared_records": "150,000,000",
        "download_size_est": "~75 GB (Compressed PBF)",
        "official_source_page": "https://planet.openstreetmap.org/",
        "direct_download_url": "https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf",
        "source_org": "OpenStreetMap Foundation",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "Geofabrik Europe Commercial Establishments",
        "region_feed": "Europe",
        "declared_records": "65,000,000",
        "download_size_est": "~30 GB (Compressed PBF)",
        "official_source_page": "https://download.geofabrik.de/europe.html",
        "direct_download_url": "https://download.geofabrik.de/europe-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "Geofabrik Asia Commercial POIs",
        "region_feed": "Asia",
        "declared_records": "45,000,000",
        "download_size_est": "~15 GB (Compressed PBF)",
        "official_source_page": "https://download.geofabrik.de/asia.html",
        "direct_download_url": "https://download.geofabrik.de/asia-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "People Data Labs B2B Enrichment Catalog",
        "region_feed": "Global Companies",
        "declared_records": "32,334,356",
        "download_size_est": "API Stream / On-Demand",
        "official_source_page": "https://www.peopledatalabs.com/",
        "direct_download_url": "https://api.peopledatalabs.com/v5/company/enrich",
        "source_org": "People Data Labs Inc.",
        "auth_required": "Paid API Key Required",
        "url_accessibility": "ACTIVE API (Requires Key)",
        "local_status": "Remote API Feed (0 records cached locally)"
    },
    {
        "dataset_name": "Geofabrik North America Commercial POIs",
        "region_feed": "North America",
        "declared_records": "32,000,000",
        "download_size_est": "~14 GB (Compressed PBF)",
        "official_source_page": "https://download.geofabrik.de/north-america.html",
        "direct_download_url": "https://download.geofabrik.de/north-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "Geofabrik Africa Commercial POIs",
        "region_feed": "Africa",
        "declared_records": "12,000,000",
        "download_size_est": "~6 GB (Compressed PBF)",
        "official_source_page": "https://download.geofabrik.de/africa.html",
        "direct_download_url": "https://download.geofabrik.de/africa-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "Geofabrik South America Commercial POIs",
        "region_feed": "South America",
        "declared_records": "6,800,000",
        "download_size_est": "~4 GB (Compressed PBF)",
        "official_source_page": "https://download.geofabrik.de/south-america.html",
        "direct_download_url": "https://download.geofabrik.de/south-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "UK Companies House Basic Company Data",
        "region_feed": "United Kingdom",
        "declared_records": "5,400,000",
        "download_size_est": "~420 MB (Compressed ZIP)",
        "official_source_page": "http://download.companieshouse.gov.uk/en_output.html",
        "direct_download_url": "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip",
        "source_org": "Companies House (UK Government)",
        "auth_required": "None (Free Open Government Licence)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Remote Catalog Feed (0 bytes downloaded locally)"
    },
    {
        "dataset_name": "Geofabrik Oceania Commercial POIs",
        "region_feed": "Oceania / Australia / Pacific",
        "declared_records": "2,500,000",
        "download_size_est": "~1.5 GB (Compressed PBF)",
        "official_source_page": "https://download.geofabrik.de/oceania.html",
        "direct_download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility": "ACTIVE 200",
        "local_status": "Checksum present (50 bytes); binary payload NOT downloaded"
    }
]

with open(os.path.join(OUT_DIR, "remote_unfetched_datasets.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "region_feed", "declared_records", "download_size_est",
        "official_source_page", "direct_download_url", "source_org",
        "auth_required", "url_accessibility", "local_status"
    ])
    writer.writeheader()
    writer.writerows(remote_datasets)

print("[4/7] Wrote remote_unfetched_datasets.csv")

# -----------------------------------------------------------------------------
# 5. missing_or_incomplete_files.csv
# -----------------------------------------------------------------------------
missing_or_incomplete = [
    {
        "dataset_name": "Geofabrik Oceania Binary Payload",
        "expected_filename": "australia-oceania-latest.osm.pbf",
        "expected_path": r"D:\leads\oceania.osm.pbf",
        "current_status": "MISSING PAYLOAD",
        "actual_size_bytes": "50 (MD5 checksum only)",
        "evidence_of_issue": "Only D:\\leads\\oceania.osm.pbf.md5 exists containing '2f51c33466765177a9c0c46630f5a388 oceania.osm.pbf'. The data payload is 0 bytes on disk.",
        "recommended_resolution": "Download australia-oceania-latest.osm.pbf (1.5 GB) from Geofabrik if regional POIs are required.",
        "download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf"
    },
    {
        "dataset_name": "Apple Retail Locations (Root & Cleaned Copy)",
        "expected_filename": "apple-locations.csv",
        "expected_path": r"D:\leads\apple-locations.csv",
        "current_status": "MISSING FROM ROOT / TRUNCATED IN CLEANED",
        "actual_size_bytes": "40,649 in backup; 57 in cleaned_20261025; 0 in D:\\leads root",
        "evidence_of_issue": "D:\\leads\\cleaned_20261025\\apple-locations.csv is 57 bytes (header only). The file is missing from D:\\leads root. Full 40.6 KB file exists in backup_original_20261025.",
        "recommended_resolution": "NO DOWNLOAD NEEDED. Copy the intact 40.6 KB file from D:\\leads\\backup_original_20261025\\apple-locations.csv to D:\\leads\\master-locations.csv or restore to root.",
        "download_url": "Local restore from backup_original_20261025\\apple-locations.csv"
    },
    {
        "dataset_name": "Free Company Global Dataset (Format Extension Mismatch)",
        "expected_filename": "free_company_dataset.csv.gz",
        "expected_path": r"D:\leads\free_company_dataset.csv.zip",
        "current_status": "FORMAT MISNAMED",
        "actual_size_bytes": "2,392,105,978",
        "evidence_of_issue": "File is named .zip, but magic bytes are 1f 8b 08 00 (GZIP). Zip extractors fail with 'File is not a zip file'.",
        "recommended_resolution": "NO DOWNLOAD NEEDED. Treat file as GZIP directly in Python/DuckDB, or rename to free_company_dataset.csv.gz.",
        "download_url": "Local fix (No redownload required)"
    },
    {
        "dataset_name": "Realtors Duplicate Stub File",
        "expected_filename": "0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv",
        "expected_path": r"D:\leads\backup_original_20261025\0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors (1).csv",
        "current_status": "EMPTY HEADER STUB",
        "actual_size_bytes": "35",
        "evidence_of_issue": "Contains only 'name,email,phone,website,category\\r\\n' with zero rows. Harmless artifact; valid 2,500-lead file exists as 0fa64ca5-0f74-4f88-8f35-e853bbb61ce2-realtors.csv.",
        "recommended_resolution": "NO ACTION NEEDED. The main realtors file (258 KB, 2,500 leads) is already fully processed in production.",
        "download_url": "None (Redundant artifact)"
    },
    {
        "dataset_name": "Open Company Database Full 5M Scope",
        "expected_filename": "open_company_database_full.parquet",
        "expected_path": r"D:\leads\open_company_database.parquet",
        "current_status": "PARTIAL SAMPLE (100k of 5M)",
        "actual_size_bytes": "8,618,037 (Parquet) / 27,272,387 (CSV)",
        "evidence_of_issue": "README documents 5M companies; local file is explicitly open_company_database_sample.csv containing exactly 100,000 rows.",
        "recommended_resolution": "OPTIONAL. The 100k sample is fully working in production. Redownload full 5M only if 50x expansion is required.",
        "download_url": "https://github.com/fliarbi/radar-api-mcp"
    }
]

with open(os.path.join(OUT_DIR, "missing_or_incomplete_files.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "expected_filename", "expected_path", "current_status",
        "actual_size_bytes", "evidence_of_issue", "recommended_resolution", "download_url"
    ])
    writer.writeheader()
    writer.writerows(missing_or_incomplete)

print("[5/7] Wrote missing_or_incomplete_files.csv")

# -----------------------------------------------------------------------------
# 6. original_download_urls.csv
# -----------------------------------------------------------------------------
original_urls = [
    {
        "dataset_name": "GLEIF Golden Copy Legal Entity Identifier Registry",
        "original_filename": "20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip",
        "source_org": "Global Legal Entity Identifier Foundation (GLEIF)",
        "official_download_page": "https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy",
        "direct_download_url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest/lei2/csv",
        "file_format": "CSV.ZIP",
        "approx_download_size": "~506 MB",
        "expected_record_count": "3,472,837",
        "record_count_type": "Verified Exact",
        "auth_required": "None (Free Open Data)",
        "url_accessibility_status": "ACTIVE 200 via Portal"
    },
    {
        "dataset_name": "U.S. SEC EDGAR Corporate Submissions Bulk",
        "original_filename": "submissions.zip",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "official_download_page": "https://www.sec.gov/edgar/sec-api-documentation",
        "direct_download_url": "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip",
        "file_format": "ZIP (JSON Files)",
        "approx_download_size": "~1.57 GB",
        "expected_record_count": "995,761",
        "record_count_type": "Verified Exact",
        "auth_required": "Free (Requires User-Agent header per SEC policy)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "U.S. SEC EDGAR XBRL Company Facts Bulk",
        "original_filename": "companyfacts.zip",
        "source_org": "U.S. Securities and Exchange Commission (SEC)",
        "official_download_page": "https://www.sec.gov/edgar/sec-api-documentation",
        "direct_download_url": "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip",
        "file_format": "ZIP (JSON Files)",
        "approx_download_size": "~1.41 GB",
        "expected_record_count": "20,501",
        "record_count_type": "Verified Exact",
        "auth_required": "Free (Requires User-Agent header per SEC policy)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "OpenStreetMap Planet Worldwide Commercial POIs",
        "original_filename": "planet-latest.osm.pbf",
        "source_org": "OpenStreetMap Foundation",
        "official_download_page": "https://planet.openstreetmap.org/",
        "direct_download_url": "https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~75 GB",
        "expected_record_count": "150,000,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Geofabrik Europe Commercial POIs",
        "original_filename": "europe-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_download_page": "https://download.geofabrik.de/europe.html",
        "direct_download_url": "https://download.geofabrik.de/europe-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~30 GB",
        "expected_record_count": "65,000,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Geofabrik Asia Commercial POIs",
        "original_filename": "asia-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_download_page": "https://download.geofabrik.de/asia.html",
        "direct_download_url": "https://download.geofabrik.de/asia-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~15 GB",
        "expected_record_count": "45,000,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Geofabrik North America Commercial POIs",
        "original_filename": "north-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_download_page": "https://download.geofabrik.de/north-america.html",
        "direct_download_url": "https://download.geofabrik.de/north-america-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~14 GB",
        "expected_record_count": "32,000,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Geofabrik Africa Commercial POIs",
        "original_filename": "africa-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_download_page": "https://download.geofabrik.de/africa.html",
        "direct_download_url": "https://download.geofabrik.de/africa-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~6 GB",
        "expected_record_count": "12,000,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Geofabrik South America Commercial POIs",
        "original_filename": "south-america-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_download_page": "https://download.geofabrik.de/south-america.html",
        "direct_download_url": "https://download.geofabrik.de/south-america-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~4 GB",
        "expected_record_count": "6,800,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Geofabrik Australia & Oceania Commercial POIs",
        "original_filename": "australia-oceania-latest.osm.pbf",
        "source_org": "Geofabrik GmbH / OpenStreetMap",
        "official_download_page": "https://download.geofabrik.de/oceania.html",
        "direct_download_url": "https://download.geofabrik.de/australia-oceania-latest.osm.pbf",
        "file_format": "OSM.PBF",
        "approx_download_size": "~1.5 GB",
        "expected_record_count": "2,500,000",
        "record_count_type": "Historical Estimate",
        "auth_required": "None (Free Open Data - ODbL)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "UK Companies House Basic Company Data",
        "original_filename": "BasicCompanyDataAsOneFile-2026-10-01.zip",
        "source_org": "Companies House (UK Government)",
        "official_download_page": "http://download.companieshouse.gov.uk/en_output.html",
        "direct_download_url": "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip",
        "file_format": "CSV.ZIP",
        "approx_download_size": "~420 MB",
        "expected_record_count": "5,400,000",
        "record_count_type": "Verified Exact Government Release",
        "auth_required": "None (Free Open Government Licence)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Common Crawl Web Index Path Archive",
        "original_filename": "cc-index.paths.gz",
        "source_org": "Common Crawl Foundation",
        "official_download_page": "https://commoncrawl.org/the-data/get-started/",
        "direct_download_url": "https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-51/cc-index.paths.gz",
        "file_format": "GZ",
        "approx_download_size": "< 1 MB",
        "expected_record_count": "302",
        "record_count_type": "Verified Exact",
        "auth_required": "None (AWS Open Data Registry)",
        "url_accessibility_status": "ACTIVE 200 via S3"
    },
    {
        "dataset_name": "Live Technographic Dataset (Tech Stack Datasets)",
        "original_filename": "tech-stack-datasets-main.zip",
        "source_org": "Live Technographic Dataset Project",
        "official_download_page": "https://github.com/tech-stack-datasets/tech-stack-datasets",
        "direct_download_url": "https://github.com/tech-stack-datasets/tech-stack-datasets/archive/refs/heads/main.zip",
        "file_format": "ZIP",
        "approx_download_size": "~36.8 MB",
        "expected_record_count": "153,104 sample / 53.7M scope",
        "record_count_type": "Verified Sample Rows",
        "auth_required": "None (Open Source GitHub Repository)",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Open Company Database (Radar API Sample)",
        "original_filename": "open_company_database_sample.csv",
        "source_org": "Fliar Research",
        "official_download_page": "https://github.com/fliarbi/radar-api-mcp",
        "direct_download_url": "https://github.com/fliarbi/radar-api-mcp",
        "file_format": "CSV / Parquet",
        "approx_download_size": "~26.9 MB CSV / ~8.2 MB Parquet",
        "expected_record_count": "100,000 sample / 5.0M scope",
        "record_count_type": "Verified Sample Rows",
        "auth_required": "None for Sample / Radar API key for live feed",
        "url_accessibility_status": "ACTIVE 200"
    },
    {
        "dataset_name": "Data Legion Global Companies",
        "original_filename": "data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "source_org": "Data Legion",
        "official_download_page": "https://datalegion.com/",
        "direct_download_url": "https://datalegion.com/data/data-legion-company-free-1.5.0_2026-10-15.csv.gz",
        "file_format": "CSV.GZ",
        "approx_download_size": "~1.44 GB",
        "expected_record_count": "28,127,036",
        "record_count_type": "Verified Header Row Count",
        "auth_required": "Free Download / Registration",
        "url_accessibility_status": "UNKNOWN (Domain requires live web session)"
    },
    {
        "dataset_name": "Free Company Dataset",
        "original_filename": "free_company_dataset.csv.gz",
        "source_org": "People Data Labs",
        "official_download_page": "https://www.peopledatalabs.com/free-company-dataset",
        "direct_download_url": "https://www.peopledatalabs.com/free-company-dataset",
        "file_format": "CSV.GZ",
        "approx_download_size": "~2.23 GB",
        "expected_record_count": "180,000,000 declared / 37.2M streamable",
        "record_count_type": "Declared vs Streamable Sample",
        "auth_required": "Work Email Registration Required",
        "url_accessibility_status": "ACTIVE Portal"
    },
    {
        "dataset_name": "ODO Senzing Global Entities Release",
        "original_filename": "ODO_SENZING_20260305.zip",
        "source_org": "Senzing / BrightQuery",
        "official_download_page": "https://senzing.com/",
        "direct_download_url": "UNKNOWN (Private Distribution Link)",
        "file_format": "ZIP",
        "approx_download_size": "~19.91 GB",
        "expected_record_count": "341,000,000",
        "record_count_type": "Declared Bulk Entity Release",
        "auth_required": "Enterprise License / BrightQuery Subscription",
        "url_accessibility_status": "Requires Enterprise Login"
    },
    {
        "dataset_name": "B2B Raw Shards (18 CSV Files)",
        "original_filename": "free-tier (2..19).csv and free-tier.csv",
        "source_org": "B2B Lead Intelligence Consortium",
        "official_download_page": "UNKNOWN",
        "direct_download_url": "UNKNOWN",
        "file_format": "CSV",
        "approx_download_size": "~2.49 GB Total",
        "expected_record_count": "11,833,267",
        "record_count_type": "Verified Raw Sum",
        "auth_required": "UNKNOWN",
        "url_accessibility_status": "UNKNOWN (Historical Files)"
    },
    {
        "dataset_name": "Homeowners & Residential Property Raw CSV",
        "original_filename": "free-tier (1).csv",
        "source_org": "County Assessor / Property Registry",
        "official_download_page": "UNKNOWN",
        "direct_download_url": "UNKNOWN",
        "file_format": "CSV",
        "approx_download_size": "~78.9 MB",
        "expected_record_count": "703,772",
        "record_count_type": "Verified Exact Rows",
        "auth_required": "UNKNOWN",
        "url_accessibility_status": "UNKNOWN (Historical File)"
    },
    {
        "dataset_name": "Targeted Professional Verticals (7 CSVs)",
        "original_filename": "*-restaurants.csv, *-realtors.csv, *-coaches.csv, etc.",
        "source_org": "Targeted Lead Generation Feeds",
        "official_download_page": "UNKNOWN",
        "direct_download_url": "UNKNOWN",
        "file_format": "CSV",
        "approx_download_size": "~1.65 MB Total",
        "expected_record_count": "17,500 (2,500 each)",
        "record_count_type": "Verified Exact Rows",
        "auth_required": "UNKNOWN",
        "url_accessibility_status": "UNKNOWN (Historical Files)"
    }
]

with open(os.path.join(OUT_DIR, "original_download_urls.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "dataset_name", "original_filename", "source_org", "official_download_page",
        "direct_download_url", "file_format", "approx_download_size",
        "expected_record_count", "record_count_type", "auth_required", "url_accessibility_status"
    ])
    writer.writeheader()
    writer.writerows(original_urls)

print("[6/7] Wrote original_download_urls.csv")

# -----------------------------------------------------------------------------
# 7. download_recovery_summary.md
# -----------------------------------------------------------------------------
md_content = """# Lead Portfolio Download Recovery & Dataset Inventory Report
**Comprehensive Data Source Audit, Unprocessed Archives Analysis, and Download Recovery Links**  
**Audit Date:** October 26, 2026  
**Audited Storage Root:** `D:\\leads\\`  
**Report Output Directory:** `D:\\leads\\download_recovery_inventory\\`  
**Investigation Mode:** Strictly Read-Only (Zero downloads, zero deletions, zero extractions, zero disk usage)

---

## 1. Executive Summary: Portfolio Status At A Glance

| Portfolio Category | Dataset Count | Physical Files / Feeds | Total Record Count | Storage Size on Disk | Operational Status |
|:---|:---:|:---:|---:|---:|:---|
| **Physically Present on Disk** | **22 Datasets** | 45 files (Root + subdirs) | **567,188,074 rows** | **62.67 GB** | Present on `D:\\leads` |
| ├── **Fully Processed & Active** | **16 Datasets** | 16 Parquets & Clean CSVs | **14,935,362 rows** | **1.88 GB** | Fully indexed in DuckDB (`v_all_unified`) |
| └── **Unprocessed Local Archives** | **5 Large Datasets** | 22 Archives & Raw Shards | **~552,000,000 rows** | **60.79 GB** | Preserved compressed on disk |
| **Missing / Incomplete Artifacts** | **2 Files** | 1 binary, 1 stub/clean copy | **~2,500,692 rows** | **40.7 KB** | Binary missing / corrupted copy |
| **Remote Unfetched Catalog Feeds** | **9 Regional Feeds** | 0 local data bytes | **352,334,356 rows** | **0 bytes** | Remote endpoints (ODbL, API) |
| **Total Configured Portfolio** | **31 Datasets** | **54 Data Sources & Feeds** | **919,557,675 rows** | **62.67 GB** | Complete Portfolio Universe |

---

## 2. Key Findings & Crucial Recommendations: What to Download vs. What NOT to Download

> [!IMPORTANT]
> **DO NOT waste bandwidth or disk space redownloading large archives that ALREADY exist locally!**  
> `D:\\` currently has **54.47 GB free**. Downloading hundreds of gigabytes of data that you already own will exhaust local disk space.

### Summary of Actions Required:

1. **Only ONE True Missing Download Payload:**
   - **`australia-oceania-latest.osm.pbf` (~1.5 GB, ~2.5M POIs):**  
     Only the 50-byte checksum `oceania.osm.pbf.md5` exists locally. The binary `.osm.pbf` file was never downloaded. If Oceania POI coverage is desired, download this single file.
2. **One High-Value Optional Download:**
   - **UK Companies House Basic Company Data (~420 MB zip, 5.4M companies):**  
     A high-quality, verified government company registry. Free and direct download from `http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip`. It takes only 420 MB and will unpack into ~2 GB of verified UK business records.
3. **Internal Local Restorations (NO DOWNLOAD NEEDED):**
   - **`apple-locations.csv`:** An intact, complete copy (40.6 KB, 692 retail locations) already exists in `D:\\leads\\backup_original_20261025\\apple-locations.csv`. The version in `cleaned_20261025` was truncated to 57 bytes (header only). It can simply be copied from the backup folder—no internet download is needed.
   - **`free_company_dataset.csv.zip`:** This 2.23 GB file is **NOT corrupted**; it is simply a GZIP file misnamed with a `.zip` extension (magic bytes `1f 8b 08 00`). It can be streamed directly via `read_csv(..., compression='gzip')` without redownloading.
4. **Existing Local Archives to Process (DO NOT REDOWNLOAD):**
   - **`ODO_SENZING_20260305.zip` (19.91 GB, 341M records):** Already on disk. Valid ZIP containing 2,496 JSON files. Do NOT redownload 20 GB.
   - **`data-legion-company-free-1.5.0_2026-10-15.csv.gz` (1.44 GB, 28.1M records):** Already on disk. Valid GZIP archive.
   - **`submissions (1).zip` (1.46 GB, 995,761 SEC EDGAR files):** Already on disk. Valid ZIP archive.

---

## 3. Directory of Generated Audit Reports

All 6 companion CSV audit files have been generated in `D:\\leads\\download_recovery_inventory\\`:

| File | Description | Records Audited |
|:---|:---|:---:|
| [`all_datasets_inventory.csv`](file:///D:/leads/download_recovery_inventory/all_datasets_inventory.csv) | Master inventory of all 31 datasets with paths, sizes, formats, row counts, production DB status, and lineage. | 31 Datasets |
| [`datasets_to_redownload.csv`](file:///D:/leads/download_recovery_inventory/datasets_to_redownload.csv) | Explicitly lists files that actually require redownload vs files where redownload is strongly discouraged. | 7 Entries |
| [`unprocessed_local_archives.csv`](file:///D:/leads/download_recovery_inventory/unprocessed_local_archives.csv) | Comprehensive analysis of the 5 large local archives, storage requirements, and recommended ingestion methods. | 5 Archives |
| [`remote_unfetched_datasets.csv`](file:///D:/leads/download_recovery_inventory/remote_unfetched_datasets.csv) | Complete catalog of the 9 unfetched remote feeds totaling 352,334,356 records with URLs and license requirements. | 9 Remote Feeds |
| [`missing_or_incomplete_files.csv`](file:///D:/leads/download_recovery_inventory/missing_or_incomplete_files.csv) | Forensic audit of files with concrete evidence of corruption, truncation, missing payloads, or format misnaming. | 5 Problem Cases |
| [`original_download_urls.csv`](file:///D:/leads/download_recovery_inventory/original_download_urls.csv) | Verified official download pages, direct links, source organizations, auth rules, and live accessibility status. | 20 Sources |

---

## 4. Master Download Recovery Catalog & Official Links

| Dataset Name | Source Organization | File Format | Download Size | Expected Records | Official Source Page | Direct Download URL | Live Status |
|:---|:---|:---:|---:|---:|:---|:---|:---:|
| **Geofabrik Oceania POIs** | Geofabrik / OSM | OSM.PBF | ~1.5 GB | 2,500,000 | [Geofabrik Oceania](https://download.geofabrik.de/oceania.html) | [Direct PBF](https://download.geofabrik.de/australia-oceania-latest.osm.pbf) | `ACTIVE 200` |
| **UK Companies House** | Companies House (UK) | CSV.ZIP | ~420 MB | 5,400,000 | [Companies House](http://download.companieshouse.gov.uk/en_output.html) | [Direct Zip](http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-10-01.zip) | `ACTIVE 200` |
| **GLEIF Golden Copy LEI-2** | GLEIF Foundation | CSV.ZIP | ~506 MB | 3,472,837 | [GLEIF Golden Copy](https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy) | [API Download](https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest/lei2/csv) | `ACTIVE 200` |
| **SEC EDGAR Submissions** | U.S. SEC | ZIP | ~1.46 GB | 995,761 | [SEC API Docs](https://www.sec.gov/edgar/sec-api-documentation) | [Direct Zip](https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip) | `ACTIVE 200` |
| **SEC EDGAR Company Facts** | U.S. SEC | ZIP | ~1.41 GB | 20,501 | [SEC API Docs](https://www.sec.gov/edgar/sec-api-documentation) | [Direct Zip](https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip) | `ACTIVE 200` |
| **Common Crawl Web Index** | Common Crawl | GZ | < 1 MB | 302 | [Common Crawl](https://commoncrawl.org/the-data/get-started/) | [S3 Path Index](https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-51/cc-index.paths.gz) | `ACTIVE 200` |
| **Live Technographic Data** | Tech Stack Project | ZIP | ~36.8 MB | 153,104 | [GitHub Repo](https://github.com/tech-stack-datasets/tech-stack-datasets) | [Release Zip](https://github.com/tech-stack-datasets/tech-stack-datasets/archive/refs/heads/main.zip) | `ACTIVE 200` |
| **Open Company Database** | Fliar Research | CSV / Parquet | ~26.9 MB | 100,000 (Sample) | [Fliar Radar MCP](https://github.com/fliarbi/radar-api-mcp) | [GitHub MCP](https://github.com/fliarbi/radar-api-mcp) | `ACTIVE 200` |
| **OSM Planet Worldwide** | OSM Foundation | OSM.PBF | ~75 GB | 150,000,000 | [Planet OSM](https://planet.openstreetmap.org/) | [Direct PBF](https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf) | `ACTIVE 200` |
| **Geofabrik Europe POIs** | Geofabrik / OSM | OSM.PBF | ~30 GB | 65,000,000 | [Geofabrik Europe](https://download.geofabrik.de/europe.html) | [Direct PBF](https://download.geofabrik.de/europe-latest.osm.pbf) | `ACTIVE 200` |
| **Geofabrik Asia POIs** | Geofabrik / OSM | OSM.PBF | ~15 GB | 45,000,000 | [Geofabrik Asia](https://download.geofabrik.de/asia.html) | [Direct PBF](https://download.geofabrik.de/asia-latest.osm.pbf) | `ACTIVE 200` |
| **Geofabrik North America** | Geofabrik / OSM | OSM.PBF | ~14 GB | 32,000,000 | [Geofabrik NA](https://download.geofabrik.de/north-america.html) | [Direct PBF](https://download.geofabrik.de/north-america-latest.osm.pbf) | `ACTIVE 200` |
| **Geofabrik Africa POIs** | Geofabrik / OSM | OSM.PBF | ~6 GB | 12,000,000 | [Geofabrik Africa](https://download.geofabrik.de/africa.html) | [Direct PBF](https://download.geofabrik.de/africa-latest.osm.pbf) | `ACTIVE 200` |
| **Geofabrik South America** | Geofabrik / OSM | OSM.PBF | ~4 GB | 6,800,000 | [Geofabrik SA](https://download.geofabrik.de/south-america.html) | [Direct PBF](https://download.geofabrik.de/south-america-latest.osm.pbf) | `ACTIVE 200` |
| **People Data Labs Catalog** | People Data Labs | JSON API | API Stream | 32,334,356 | [People Data Labs](https://www.peopledatalabs.com/) | [API Endpoint](https://api.peopledatalabs.com/v5/company/enrich) | `API Key Req` |
| **Data Legion Companies** | Data Legion | CSV.GZ | ~1.44 GB | 28,127,036 | [Data Legion](https://datalegion.com/) | [Direct Download](https://datalegion.com/data/data-legion-company-free-1.5.0_2026-10-15.csv.gz) | `Local On Disk` |
| **Free Company Dataset** | People Data Labs | CSV.GZ | ~2.23 GB | 180,000,000 | [PDL Free Dataset](https://www.peopledatalabs.com/free-company-dataset) | [PDL Portal](https://www.peopledatalabs.com/free-company-dataset) | `Local On Disk` |
| **ODO Senzing Entity Archive**| Senzing / BrightQuery| ZIP | ~19.91 GB | 341,000,000 | [Senzing](https://senzing.com/) | UNKNOWN (Enterprise) | `Local On Disk` |
| **18 Raw B2B Shards** | B2B Consortium | CSV | ~2.49 GB | 11,833,267 | UNKNOWN | UNKNOWN | `Local On Disk` |
| **Homeowners Raw CSV** | County Assessor Feeds| CSV | ~78.9 MB | 703,772 | UNKNOWN | UNKNOWN | `Local On Disk` |
| **7 Professional Verticals**| Industry Feeds | CSV | ~1.65 MB | 17,500 | UNKNOWN | UNKNOWN | `Local On Disk` |

---

## 5. Storage Space Assessment & Feasibility

- **Total Drive Capacity:** Drive `D:\\` is currently using **62.67 GB** with **54.47 GB free**.
- **Downloading All Remote OSM Feeds:** Downloading Planet OSM (75 GB), Europe (30 GB), Asia (15 GB), and NA (14 GB) requires **~140 GB** of download bandwidth and over **300 GB** for uncompressed parsing. **This is physically impossible on the current drive.**
- **Recommended Ingestion Strategy:**
  1. Leave large remote feeds as catalog references or query them via live cloud endpoints.
  2. For `ODO_SENZING_20260305.zip`, stream through the 2,496 internal JSON files in batches of 50 without full disk unzipping.
  3. For `free_company_dataset.csv.zip`, query directly using DuckDB gzip decompression.
"""

with open(os.path.join(OUT_DIR, "download_recovery_summary.md"), "w", encoding="utf-8") as f:
    f.write(md_content)

print("[7/7] Wrote download_recovery_summary.md")
print("All 7 recovery reports generated successfully in:", OUT_DIR)
