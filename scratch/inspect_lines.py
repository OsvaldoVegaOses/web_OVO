from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
idx2 = root / "index2.html"
lines = idx2.read_text(encoding="utf-8").splitlines()

targets = ["experience-map", "featured-projects", "published-project-row", "current-project-grid"]

for t in targets:
    print(f"\n==================== TARGET: {t} ====================")
    for i, line in enumerate(lines):
        if t in line:
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            print(f"--- Line {i+1} ---")
            for j in range(start, end):
                print(f"{j+1}: {lines[j]}")
