import sys
sys.path.insert(0, r"d:\leads\repo")
from gui import lead_db

files = lead_db.get_local_csv_datasets()
print(f"Total raw lead files found: {len(files)}")
for f in files:
    print(f['id'], f['count'])
