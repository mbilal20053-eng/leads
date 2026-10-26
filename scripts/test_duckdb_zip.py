import duckdb
import os
import sys

con = duckdb.connect()
f = r"d:\leads\20261026-0000-gleif-goldencopy-lei2-golden-copy.csv.zip".replace("\\", "/")

# Check if duckdb can read zip
try:
    print("Testing read_csv on zip directly...")
    res = con.execute(f"SELECT * FROM read_csv('{f}') LIMIT 1").fetchall()
    print("Direct read success:", res)
except Exception as e:
    print("Direct read error:", e)
