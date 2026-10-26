import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\leads\repo\gui\templates\index.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, 1):
        if re.search(r"915|919|920", line):
            print(f"{idx}: {line.strip()}")
