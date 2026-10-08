import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
idx2 = root / "index2.html"
text = idx2.read_text(encoding="utf-8")

classes = [
    "experience-map",
    "featured-projects",
    "published-project-row",
    "current-project-grid",
]

for c in classes:
    m = re.findall(rf"\.{c}[^{{]*\{{([^}}]+)\}}", text)
    print(f"=== CSS RULES FOR .{c} ===")
    for rule in m:
        print(rule.strip().replace("\n", " "))
    # Find occurrences in HTML
    html_occurrences = len(re.findall(rf'class=["\'][^"\']*\b{c}\b[^"\']*["\']', text))
    print(f"HTML occurrences: {html_occurrences}\n")
