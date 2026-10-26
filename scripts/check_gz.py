import gzip

gz_path = r"d:\leads\free_company_dataset.csv.zip"
try:
    with gzip.open(gz_path, 'rb') as f:
        header = f.readline()
        print("Header:", header[:100])
        first_line = f.readline()
        print("First line:", first_line[:100])
        print("Successfully read as GZIP!")
except Exception as e:
    print("Error:", e)
