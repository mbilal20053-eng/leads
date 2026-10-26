"""
Compile exact filter simulation numbers across all files.
"""

file_results = [
    {"label": "Restaurants CSV", "file": "050580a4-restaurants.csv", "total": 2500, "affected": 45, "preserved": 45, "removal": 0},
    {"label": "Realtors CSV", "file": "0fa64ca5-realtors.csv", "total": 2500, "affected": 21, "preserved": 21, "removal": 0},
    {"label": "Coaches CSV", "file": "166ff949-coaches.csv", "total": 2500, "affected": 14, "preserved": 14, "removal": 0},
    {"label": "Musicians CSV", "file": "74b7d278-musicians.csv", "total": 2500, "affected": 56, "preserved": 56, "removal": 0},
    {"label": "Designers CSV", "file": "94f26329-designers.csv", "total": 2500, "affected": 35, "preserved": 35, "removal": 0},
    {"label": "Founders CSV", "file": "b0d3b766-entrepreneurs.csv", "total": 2500, "affected": 47, "preserved": 47, "removal": 0},
    {"label": "Photographers CSV", "file": "da6aeb15-photographers.csv", "total": 2500, "affected": 40, "preserved": 40, "removal": 0},
    {"label": "Real Estate B2B (free-tier.csv)", "file": "free-tier.csv", "total": 44021, "affected": 3, "preserved": 3, "removal": 0},
    {"label": "Homeowners (free-tier (1).csv)", "file": "free-tier (1).csv", "total": 703772, "affected": 0, "preserved": 0, "removal": 0},
    {"label": "B2B Shard 2", "file": "free-tier (2).csv", "total": 1733407, "affected": 373389, "preserved": 163744, "removal": 209645},
    {"label": "B2B Shard 3", "file": "free-tier (3).csv", "total": 823614, "affected": 173738, "preserved": 100534, "removal": 73204},
    {"label": "B2B Shard 4", "file": "free-tier (4).csv", "total": 616512, "affected": 132382, "preserved": 57013, "removal": 75369},
    {"label": "B2B Shard 5", "file": "free-tier (5).csv", "total": 462388, "affected": 87798, "preserved": 43693, "removal": 44105},
    {"label": "B2B Shard 6", "file": "free-tier (6).csv", "total": 546103, "affected": 140319, "preserved": 74975, "removal": 65344},
    {"label": "B2B Shard 7", "file": "free-tier (7).csv", "total": 1238583, "affected": 291578, "preserved": 175812, "removal": 115766},
    {"label": "B2B Shard 8", "file": "free-tier (8).csv", "total": 792758, "affected": 157681, "preserved": 61717, "removal": 95964},
    {"label": "B2B Shard 9", "file": "free-tier (9).csv", "total": 301225, "affected": 65898, "preserved": 35441, "removal": 30457},
    {"label": "B2B Shard 10", "file": "free-tier (10).csv", "total": 513367, "affected": 107518, "preserved": 48802, "removal": 58716},
    {"label": "B2B Shard 11", "file": "free-tier (11).csv", "total": 440754, "affected": 93829, "preserved": 39819, "removal": 54010},
    {"label": "B2B Shard 12", "file": "free-tier (12).csv", "total": 307656, "affected": 99683, "preserved": 46424, "removal": 53259},
    {"label": "B2B Shard 13", "file": "free-tier (13).csv", "total": 380171, "affected": 70492, "preserved": 35281, "removal": 35211},
    {"label": "B2B Shard 14", "file": "free-tier (14).csv", "total": 1438244, "affected": 281236, "preserved": 140826, "removal": 140410},
    {"label": "B2B Shard 15", "file": "free-tier (15).csv", "total": 302479, "affected": 58759, "preserved": 23159, "removal": 35600},
    {"label": "B2B Shard 16", "file": "free-tier (16).csv", "total": 418718, "affected": 92681, "preserved": 46645, "removal": 46036},
    {"label": "B2B Shard 17", "file": "free-tier (17).csv", "total": 583022, "affected": 180263, "preserved": 90739, "removal": 89524},
    {"label": "B2B Shard 18", "file": "free-tier (18).csv", "total": 340304, "affected": 69808, "preserved": 42542, "removal": 27266},
    {"label": "B2B Shard 19", "file": "free-tier (19).csv", "total": 304353, "affected": 54469, "preserved": 29326, "removal": 25143},
    {"label": "Master Locations", "file": "master-locations.csv", "total": 154710, "affected": 0, "preserved": 0, "removal": 0},
    {"label": "Open Company Sample", "file": "open_company_database_sample.csv", "total": 100000, "affected": 1, "preserved": 1, "removal": 0},
    {"label": "Data Legion Company", "file": "data-legion-company-free.csv.gz", "total": 28127036, "affected": 124, "preserved": 124, "removal": 0},
]

print("=" * 80)
print("TOTALS ACROSS ALL 30 RAW FILES ON DISK:")
tot = sum(f["total"] for f in file_results)
aff = sum(f["affected"] for f in file_results)
pres = sum(f["preserved"] for f in file_results)
rem = sum(f["removal"] for f in file_results)

print(f"Total Records Scanned:           {tot:>12,}")
print(f"Total Affected Records:          {aff:>12,} ({aff/tot*100:.2f}%)")
print(f"Preserved (>= 1 Contact Method): {pres:>12,} ({pres/aff*100:.2f}% of affected)")
print(f"Qualifies for Removal (0 Contact):{rem:>12,} ({rem/aff*100:.2f}% of affected, {rem/tot*100:.2f}% of dataset)")

# B2B 18 Shards Alone
b2b_shards = [f for f in file_results if "B2B Shard" in f["label"]]
b2b_tot = sum(f["total"] for f in b2b_shards)
b2b_aff = sum(f["affected"] for f in b2b_shards)
b2b_pres = sum(f["preserved"] for f in b2b_shards)
b2b_rem = sum(f["removal"] for f in b2b_shards)

print("\n" + "=" * 80)
print("TOTALS FOR THE 18 B2B SHARDS ALONE (free-tier (2).csv to (19).csv):")
print(f"Total Rows:                      {b2b_tot:>12,}")
print(f"Affected (Blank/Placeholder Co): {b2b_aff:>12,} ({b2b_aff/b2b_tot*100:.2f}%)")
print(f"Preserved (>= 1 Contact Method): {b2b_pres:>12,} ({b2b_pres/b2b_aff*100:.2f}%)")
print(f"Qualifies for Removal (0 Contact):{b2b_rem:>12,} ({b2b_rem/b2b_aff*100:.2f}%)")
