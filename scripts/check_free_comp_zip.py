import zipfile
import os

zip_path = r"d:\leads\free_company_dataset.csv.zip"
print("Checking free_company_dataset.csv.zip:")
if os.path.exists(zip_path):
    print("Size:", os.path.getsize(zip_path) / (1024*1024), "MB")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            print(f"  {info.filename}: compressed {info.compress_size/(1024*1024):.1f} MB, uncompressed {info.file_size/(1024*1024):.1f} MB")
