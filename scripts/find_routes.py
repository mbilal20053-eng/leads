with open(r"d:\leads\repo\gui\app.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, 1):
        if "@app.route" in line:
            print(f"{idx}: {line.strip()}")
