"""
Compile exact verified totals from the audit scan of all datasets.
STRICT AUDIT ONLY. NO MODIFICATIONS.
"""

# Verified scan results from task-1435 (exact scans over all files)
raw_datasets = [
    {"name": "050580a4-restaurants.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 0, "blank": 45, "affected": 45, "dups": 0},
    {"name": "0fa64ca5-realtors.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 0, "blank": 21, "affected": 21, "dups": 0},
    {"name": "166ff949-coaches.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 0, "blank": 14, "affected": 14, "dups": 0},
    {"name": "74b7d278-musicians.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 1, "blank": 55, "affected": 56, "dups": 0},
    {"name": "94f26329-designers.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 0, "blank": 35, "affected": 35, "dups": 0},
    {"name": "b0d3b766-entrepreneurs.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 0, "blank": 47, "affected": 47, "dups": 0},
    {"name": "da6aeb15-photographers.csv", "type": "Raw Vertical CSV", "total": 2500, "ub": 0, "unk": 0, "ph": 0, "blank": 40, "affected": 40, "dups": 0},
    {"name": "free-tier.csv (CRE B2B)", "type": "Raw Real Estate CSV", "total": 44021, "ub": 0, "unk": 0, "ph": 3, "blank": 0, "affected": 3, "dups": 0},
    {"name": "free-tier (1).csv (Homeowners)", "type": "Raw Homeowners CSV", "total": 703772, "ub": 0, "unk": 0, "ph": 0, "blank": 0, "affected": 0, "dups": 0},
    {"name": "free-tier (2).csv", "type": "Raw B2B Shard CSV", "total": 1733407, "ub": 0, "unk": 88, "ph": 64, "blank": 373237, "affected": 373389, "dups": 12195},
    {"name": "free-tier (3).csv", "type": "Raw B2B Shard CSV", "total": 823614, "ub": 0, "unk": 79, "ph": 60, "blank": 173599, "affected": 173738, "dups": 2244},
    {"name": "free-tier (4).csv", "type": "Raw B2B Shard CSV", "total": 616512, "ub": 0, "unk": 22, "ph": 40, "blank": 132320, "affected": 132382, "dups": 2259},
    {"name": "free-tier (5).csv", "type": "Raw B2B Shard CSV", "total": 462388, "ub": 0, "unk": 13, "ph": 74, "blank": 87711, "affected": 87798, "dups": 960},
    {"name": "free-tier (6).csv", "type": "Raw B2B Shard CSV", "total": 546103, "ub": 0, "unk": 19, "ph": 213, "blank": 140087, "affected": 140319, "dups": 1361},
    {"name": "free-tier (7).csv", "type": "Raw B2B Shard CSV", "total": 1238583, "ub": 0, "unk": 55, "ph": 459, "blank": 291064, "affected": 291578, "dups": 4913},
    {"name": "free-tier (8).csv", "type": "Raw B2B Shard CSV", "total": 792758, "ub": 0, "unk": 28, "ph": 45, "blank": 157608, "affected": 157681, "dups": 5112},
    {"name": "free-tier (9).csv", "type": "Raw B2B Shard CSV", "total": 301225, "ub": 1, "unk": 12, "ph": 5, "blank": 65880, "affected": 65898, "dups": 450},
    {"name": "free-tier (10).csv", "type": "Raw B2B Shard CSV", "total": 513367, "ub": 0, "unk": 25, "ph": 120, "blank": 107373, "affected": 107518, "dups": 2144},
    {"name": "free-tier (11).csv", "type": "Raw B2B Shard CSV", "total": 440754, "ub": 0, "unk": 12, "ph": 23, "blank": 93794, "affected": 93829, "dups": 814},
    {"name": "free-tier (12).csv", "type": "Raw B2B Shard CSV", "total": 307656, "ub": 0, "unk": 35, "ph": 90, "blank": 99558, "affected": 99683, "dups": 1047},
    {"name": "free-tier (13).csv", "type": "Raw B2B Shard CSV", "total": 380171, "ub": 0, "unk": 12, "ph": 24, "blank": 70456, "affected": 70492, "dups": 1051},
    {"name": "free-tier (14).csv", "type": "Raw B2B Shard CSV", "total": 1438244, "ub": 0, "unk": 27, "ph": 46, "blank": 281163, "affected": 281236, "dups": 6671},
    {"name": "free-tier (15).csv", "type": "Raw B2B Shard CSV", "total": 302479, "ub": 0, "unk": 14, "ph": 15, "blank": 58730, "affected": 58759, "dups": 972},
    {"name": "free-tier (16).csv", "type": "Raw B2B Shard CSV", "total": 418718, "ub": 0, "unk": 14, "ph": 18, "blank": 92649, "affected": 92681, "dups": 854},
    {"name": "free-tier (17).csv", "type": "Raw B2B Shard CSV", "total": 583022, "ub": 0, "unk": 26, "ph": 126, "blank": 180111, "affected": 180263, "dups": 2353},
    {"name": "free-tier (18).csv", "type": "Raw B2B Shard CSV", "total": 340304, "ub": 0, "unk": 9, "ph": 16, "blank": 69783, "affected": 69808, "dups": 382},
    {"name": "free-tier (19).csv", "type": "Raw B2B Shard CSV", "total": 304353, "ub": 0, "unk": 25, "ph": 14, "blank": 54430, "affected": 54469, "dups": 430},
    {"name": "master-locations.csv", "type": "Raw Locations CSV", "total": 154710, "ub": 0, "unk": 0, "ph": 0, "blank": 0, "affected": 0, "dups": 0},
    {"name": "open_company_database_sample.csv", "type": "Raw Sample CSV", "total": 100000, "ub": 0, "unk": 0, "ph": 1, "blank": 0, "affected": 1, "dups": 0},
    {"name": "data-legion-company-free.csv.gz", "type": "Compressed Company CSV", "total": 28127036, "ub": 0, "unk": 0, "ph": 124, "blank": 0, "affected": 124, "dups": 3},
]

parquet_datasets = [
    {"name": "b2b_executives.parquet", "type": "Consolidated Parquet", "total": 11543658, "ub": 1, "unk": 515, "ph": 1452, "blank": 0, "affected": 1968, "dups": 0},
    {"name": "homeowners.parquet", "type": "Consolidated Parquet", "total": 703772, "ub": 0, "unk": 0, "ph": 0, "blank": 0, "affected": 0, "dups": 0},
    {"name": "open_company_database.parquet", "type": "Parquet", "total": 100000, "ub": 0, "unk": 0, "ph": 1, "blank": 0, "affected": 1, "dups": 0},
    {"name": "tech_stack_companies.parquet", "type": "Parquet", "total": 153104, "ub": 0, "unk": 0, "ph": 19, "blank": 0, "affected": 19, "dups": 2},
    {"name": "gleif_goldencopy.parquet", "type": "Parquet", "total": 3472837, "ub": 0, "unk": 0, "ph": 3, "blank": 0, "affected": 3, "dups": 0},
    {"name": "sec_company_facts.parquet", "type": "Parquet", "total": 20501, "ub": 0, "unk": 0, "ph": 0, "blank": 0, "affected": 0, "dups": 0},
    {"name": "cc_web_index.parquet", "type": "Parquet", "total": 302, "ub": 0, "unk": 0, "ph": 0, "blank": 0, "affected": 0, "dups": 0},
]

print("=" * 80)
print("TOTALS FOR RAW FILES ON DISK (30 Files):")
tot_raw = sum(d["total"] for d in raw_datasets)
ub_raw = sum(d["ub"] for d in raw_datasets)
unk_raw = sum(d["unk"] for d in raw_datasets)
ph_raw = sum(d["ph"] for d in raw_datasets)
blank_raw = sum(d["blank"] for d in raw_datasets)
aff_raw = sum(d["affected"] for d in raw_datasets)
dups_raw = sum(d["dups"] for d in raw_datasets)

print(f"Total Rows Scanned:            {tot_raw:>12,}")
print(f"Exact 'Unknown Business':      {ub_raw:>12,}")
print(f"Exact 'Unknown':               {unk_raw:>12,}")
print(f"Other Placeholders:            {ph_raw:>12,}")
print(f"Blank / Missing:               {blank_raw:>12,}")
print(f"Total Affected Records:        {aff_raw:>12,} ({aff_raw/tot_raw*100:.2f}%)")
print(f"Duplicates in Affected:        {dups_raw:>12,}")
print(f"Unique Affected Records:       {aff_raw - dups_raw:>12,}")

print("\n" + "=" * 80)
print("TOTALS FOR PARQUET DATASETS (7 Consolidated Datasets):")
tot_pq = sum(d["total"] for d in parquet_datasets)
ub_pq = sum(d["ub"] for d in parquet_datasets)
unk_pq = sum(d["unk"] for d in parquet_datasets)
ph_pq = sum(d["ph"] for d in parquet_datasets)
blank_pq = sum(d["blank"] for d in parquet_datasets)
aff_pq = sum(d["affected"] for d in parquet_datasets)
dups_pq = sum(d["dups"] for d in parquet_datasets)

print(f"Total Rows Scanned:            {tot_pq:>12,}")
print(f"Exact 'Unknown Business':      {ub_pq:>12,}")
print(f"Exact 'Unknown':               {unk_pq:>12,}")
print(f"Other Placeholders:            {ph_pq:>12,}")
print(f"Blank / Missing:               {blank_pq:>12,}")
print(f"Total Affected Records:        {aff_pq:>12,} ({aff_pq/tot_pq*100:.4f}%)")
print(f"Duplicates in Affected:        {dups_pq:>12,}")
