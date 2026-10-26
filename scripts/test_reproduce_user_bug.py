import time
import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

print("Calling query_local_view_leads with page=4506545:")
t0 = time.time()
try:
    res = lead_db.query_local_view_leads(
        "v_all_unified", "all_local_unified", "Local Unified",
        page=4506545, page_size=50
    )
    print(f"Returned in {time.time()-t0:.2f}s:")
    print("  Total:", res.get("total"))
    print("  Leads returned:", len(res.get("leads", [])))
except Exception as e:
    print("Error:", e)
