"""
Inspect sample records from ODO_SENZING_20260305.zip
"""
import zipfile
import json

zip_path = r"d:\leads\ODO_SENZING_20260305.zip"

with zipfile.ZipFile(zip_path, 'r') as z:
    infolist = [info for info in z.infolist() if not info.is_dir()]
    print(f"Reading from {infolist[0].filename}...")
    with z.open(infolist[0]) as f:
        count = 0
        has_name = 0
        has_phone = 0
        has_web = 0
        has_email = 0
        all_4_missing = 0
        for line in f:
            count += 1
            rec = json.loads(line.decode('utf-8', errors='ignore'))
            feats = rec.get("FEATURES", [])
            
            # Check features
            name = None
            phone = None
            email = None
            web = None
            
            for item in feats:
                if "NAME_ORG" in item:
                    name = item["NAME_ORG"]
                elif "NAME_FULL" in item and not name:
                    name = item["NAME_FULL"]
                if "PHONE_NUMBER" in item:
                    phone = item["PHONE_NUMBER"]
                if "EMAIL_ADDRESS" in item:
                    email = item["EMAIL_ADDRESS"]
                if "DOMAIN" in item or "WEBSITE" in item:
                    web = item.get("DOMAIN") or item.get("WEBSITE")
                    
            if name and name.strip() and name.lower() not in ('unknown', 'unknown business', 'null', 'n/a'):
                has_name += 1
            if phone and len(''.join(filter(str.isdigit, str(phone)))) >= 7:
                has_phone += 1
            if email and '@' in str(email):
                has_email += 1
            if web and '.' in str(web):
                has_web += 1
                
            if not name and not phone and not email and not web:
                all_4_missing += 1
                
            if count >= 10000:
                break
                
        print(f"Sampled {count:,} records:")
        print(f"  Has Name:  {has_name:>6,} ({has_name/count*100:.2f}%)")
        print(f"  Has Phone: {has_phone:>6,} ({has_phone/count*100:.2f}%)")
        print(f"  Has Email: {has_email:>6,} ({has_email/count*100:.2f}%)")
        print(f"  Has Web:   {has_web:>6,} ({has_web/count*100:.2f}%)")
        print(f"  All 4 Missing: {all_4_missing:>6,} ({all_4_missing/count*100:.2f}%)")
