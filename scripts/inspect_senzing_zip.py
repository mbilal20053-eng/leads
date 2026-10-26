"""
Inspect ODO_SENZING_20260305.zip archive contents and schema
"""
import os
import sys
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

zip_path = r"d:\leads\ODO_SENZING_20260305.zip"

print(f"Opening {zip_path} ({os.path.getsize(zip_path)/(1024*1024*1024):.2f} GB)...")

with zipfile.ZipFile(zip_path, 'r') as z:
    infolist = z.infolist()
    print(f"Total entries inside ZIP: {len(infolist):,}")
    
    # Check first 10 files
    sample_files = [info for info in infolist if not info.is_dir()][:10]
    total_uncompressed = sum(info.file_size for info in infolist)
    print(f"Total uncompressed size: {total_uncompressed / (1024*1024*1024):.2f} GB")
    
    print("\nFirst 10 files inside:")
    for sf in sample_files:
        print(f"  {sf.filename:<50} ({sf.file_size:,} bytes)")
        
    # Read first line from first file
    if sample_files:
        with z.open(sample_files[0]) as f:
            first_line = f.readline().decode('utf-8', errors='ignore')
            print(f"\nSample content from {sample_files[0].filename}:")
            print(f"  {first_line[:300]}")
