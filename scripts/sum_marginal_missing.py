"""
Sum marginal missing counts across all 30 raw datasets from task-1649 log
"""
import re

log_p = r"C:\Users\billu\.gemini\antigravity-ide\brain\70ae1c2d-75bd-4185-9b93-4aa689e48930\.system_generated\tasks\task-1649.log"

with open(log_p, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

raw_rows = []
is_raw = False
for line in lines:
    if "--- SCANNING 30 RAW DATASETS ON DISK ---" in line:
        is_raw = True
        continue
    if "--- SCANNING 7 CONSOLIDATED PARQUET DATASETS ---" in line:
        is_raw = False
        continue
    if is_raw and "|" in line:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 8:
            lbl = parts[0]
            tot = int(re.search(r"Total:\s*([\d,]+)", parts[1]).group(1).replace(",", ""))
            m_name = int(re.search(r"M-Name:\s*([\d,]+)", parts[2]).group(1).replace(",", ""))
            m_phone = int(re.search(r"M-Phone:\s*([\d,]+)", parts[3]).group(1).replace(",", ""))
            m_email = int(re.search(r"M-Email:\s*([\d,]+)", parts[4]).group(1).replace(",", ""))
            m_web = int(re.search(r"M-Web:\s*([\d,]+)", parts[5]).group(1).replace(",", ""))
            all_4 = int(re.search(r"ALL 4 MISSING:\s*([\d,]+)", parts[6]).group(1).replace(",", ""))
            uniq = int(re.search(r"Unique:\s*([\d,]+)", parts[7]).group(1).replace(",", ""))
            raw_rows.append({
                "label": lbl, "tot": tot, "m_name": m_name, "m_phone": m_phone,
                "m_email": m_email, "m_web": m_web, "all_4": all_4, "uniq": uniq
            })

tot_rows = sum(r["tot"] for r in raw_rows)
tot_m_name = sum(r["m_name"] for r in raw_rows)
tot_m_phone = sum(r["m_phone"] for r in raw_rows)
tot_m_email = sum(r["m_email"] for r in raw_rows)
tot_m_web = sum(r["m_web"] for r in raw_rows)
tot_all_4 = sum(r["all_4"] for r in raw_rows)
tot_uniq = sum(r["uniq"] for r in raw_rows)
tot_dups = tot_all_4 - tot_uniq

print(f"Total Raw Datasets:        {len(raw_rows)}")
print(f"Total Rows:                {tot_rows:>12,}")
print(f"Missing/Placeholder Name:  {tot_m_name:>12,} ({tot_m_name/tot_rows*100:5.2f}%)")
print(f"Missing/Invalid Phone:     {tot_m_phone:>12,} ({tot_m_phone/tot_rows*100:5.2f}%)")
print(f"Missing/Invalid Email:     {tot_m_email:>12,} ({tot_m_email/tot_rows*100:5.2f}%)")
print(f"Missing/Invalid Website:   {tot_m_web:>12,} ({tot_m_web/tot_rows*100:5.2f}%)")
print(f"ALL 4 MISSING (Simultaneous): {tot_all_4:>10,} ({tot_all_4/tot_rows*100:5.2f}%)")
print(f"ALL 4 MISSING (Unique):       {tot_uniq:>10,}")
print(f"Duplicates in Matching:       {tot_dups:>10,}")
