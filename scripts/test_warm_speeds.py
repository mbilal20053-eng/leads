import time
import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

# Query 1 (warmup)
t0 = time.time()
res1 = lead_db.query_local_view_leads("v_all_unified", "all_local_unified", "Local Unified", page=1, page_size=50)
print(f"Query 1 (page 1): {len(res1['leads'])} rows in {time.time()-t0:.3f}s")

# Query 2 (page 4506545)
t0 = time.time()
res2 = lead_db.query_local_view_leads("v_all_unified", "all_local_unified", "Local Unified", page=4506545, page_size=50)
print(f"Query 2 (page 4506545): {len(res2['leads'])} rows in {time.time()-t0:.3f}s")

# Query 3 (page 100)
t0 = time.time()
res3 = lead_db.query_local_view_leads("v_all_unified", "all_local_unified", "Local Unified", page=100, page_size=50)
print(f"Query 3 (page 100): {len(res3['leads'])} rows in {time.time()-t0:.3f}s")

# Query 4 (page 500)
t0 = time.time()
res4 = lead_db.query_local_view_leads("v_all_unified", "all_local_unified", "Local Unified", page=500, page_size=50)
print(f"Query 4 (page 500): {len(res4['leads'])} rows in {time.time()-t0:.3f}s")
