import duckdb
import glob
import os

con = duckdb.connect()
con.execute("PRAGMA threads=8;")

print("=== B2B COUNTS RECONCILIATION ===")
cnt_exec_orig = con.execute("SELECT count(*) FROM read_parquet('d:/leads/b2b_executives.parquet')").fetchone()[0]
print(f"1. d:/leads/b2b_executives.parquet:                          {cnt_exec_orig:,}")

cnt_exec_clean = con.execute("SELECT count(*) FROM read_parquet('d:/leads/cleaned_export/b2b_executives_cleaned.parquet')").fetchone()[0]
print(f"2. d:/leads/cleaned_export/b2b_executives_cleaned.parquet:   {cnt_exec_clean:,}")

cnt_raw_clean = con.execute("SELECT count(*) FROM read_parquet('d:/leads/cleaned_export/b2b_raw_shards_consolidated_cleaned.parquet')").fetchone()[0]
print(f"3. d:/leads/cleaned_export/b2b_raw_shards_consolidated_cleaned.parquet: {cnt_raw_clean:,}")

shards = glob.glob('d:/leads/cleaned_export/b2b_shard_*_cleaned.parquet')
cnt_shards_sum = sum(con.execute(f"SELECT count(*) FROM read_parquet('{f.replace(chr(92), '/')}')").fetchone()[0] for f in shards)
print(f"4. Sum of 18 individual cleaned shards:                      {cnt_shards_sum:,} ({len(shards)} files)")

# Raw CSVs
csvs = [f"d:/leads/free-tier ({i}).csv" for i in range(2, 20)]
cnt_csvs_sum = con.execute(f"SELECT count(*) FROM read_csv_auto({csvs}, ignore_errors=true)").fetchone()[0]
print(f"5. Sum of 18 raw CSV shards:                                {cnt_csvs_sum:,}")

print("\n=== DIFFERENCES ===")
print(f"Difference (exec_cleaned - raw_cleaned):                     {cnt_exec_clean - cnt_raw_clean:,}")
print(f"Exclusions in exec_cleaned (exec_orig - exec_clean):         {cnt_exec_orig - cnt_exec_clean:,}")
print(f"Exclusions in raw_cleaned (csvs_sum - raw_clean):           {cnt_csvs_sum - cnt_raw_clean:,}")
print(f"Difference in exclusions:                                    {(cnt_csvs_sum - cnt_raw_clean) - (cnt_exec_orig - cnt_exec_clean):,}")
