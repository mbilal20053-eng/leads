import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for item in sorted(os.listdir(r"d:\leads")):
    full = os.path.join(r"d:\leads", item)
    if os.path.isfile(full):
        sz = os.path.getsize(full)
        print(f"{item:<65} {sz:>14,} bytes ({sz/(1024*1024):>8.2f} MB)")
    else:
        print(f"[DIR] {item}")
