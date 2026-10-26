"""
Inspect SEC submissions (1).zip
"""
import zipfile
import json

zip_path = r"d:\leads\submissions (1).zip"

with zipfile.ZipFile(zip_path, 'r') as z:
    infolist = [info for info in z.infolist() if not info.is_dir()]
    print(f"Total submission files: {len(infolist):,}")
    
    # Check 5 files
    for sf in infolist[:5]:
        with z.open(sf) as f:
            data = json.loads(f.read().decode('utf-8', errors='ignore'))
            name = data.get("name")
            cik = data.get("cik")
            sic = data.get("sic")
            print(f"  {sf.filename:<20} | CIK: {cik:<10} | Name: {name:<40} | SIC: {sic}")
