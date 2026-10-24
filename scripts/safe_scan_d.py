import os

print("Scanning D: drive directories...")
for item in os.listdir('d:/'):
    full_path = os.path.join('d:/', item)
    if os.path.isdir(full_path):
        try:
            children = os.listdir(full_path)
            print(f"Dir: {item} ({len(children)} items) -> {children[:6]}")
        except Exception as e:
            print(f"Dir: {item} -> Error: {e}")
    else:
        try:
            sz = os.path.getsize(full_path)
            print(f"File: {item} -> {sz / (1024*1024):.2f} MB")
        except Exception as e:
            print(f"File: {item} -> Error: {e}")
