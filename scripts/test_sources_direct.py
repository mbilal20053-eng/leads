import duckdb
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Test OSM query
PLANET_OSM_FILE = r"d:\leads\planet-daily.osm.pbf"
print("Checking OSM file exists:", os.path.exists(PLANET_OSM_FILE))

con = duckdb.connect()
try:
    con.execute("INSTALL spatial; LOAD spatial;")
    print("Spatial extension loaded.")
    clean_pbf = PLANET_OSM_FILE.replace("\\", "/")
    res = con.execute(f"SELECT id, tags['name'] FROM ST_ReadOSM('{clean_pbf}') LIMIT 3").fetchall()
    print("OSM query result:", res)
except Exception as e:
    print("OSM query failed with error:", e)

# 2. Test GLOBAL_DUCKDB_CON views
from gui.lead_db import get_duckdb_connection
try:
    g_con = get_duckdb_connection()
    print("Global duckdb connection initialized.")
    res_b2b = g_con.execute("SELECT id, name, category FROM v_b2b_executives LIMIT 3").fetchall()
    print("v_b2b_executives query result:", res_b2b)
except Exception as e:
    print("Global duckdb query failed with error:", e)
