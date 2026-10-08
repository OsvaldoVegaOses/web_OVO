import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
idx2 = root / "index2.html"
text = idx2.read_text(encoding="utf-8")

for name in ["experience-map", "featured-projects", "published-project-row", "current-project-grid"]:
    print(f"==================== {name} ====================")
    # Find in CSS
    for m in re.finditer(rf"[^{{}}]*\.{name}[^{{}}]*\{{[^}}]+\}}", text):
        print("CSS:", m.group(0).strip())
    # Find in HTML snippet
    for m in re.finditer(rf"<[^>]*class=[\"\'][^\"\']*{name}[^\"\']*[\"\'][^>]*>", text):
        print("HTML tag:", m.group(0))
