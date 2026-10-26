with open(r"d:\leads\repo\gui\static\app.js", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, 1):
        if "renderPagination" in line or "goToPage" in line:
            print(f"{idx}: {line.strip()}")
