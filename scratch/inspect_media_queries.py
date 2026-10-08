import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
idx2 = root / "index2.html"
text = idx2.read_text(encoding="utf-8")

# Find all @media blocks
for m in re.finditer(r"@media\s*([^{]+)\{((?:[^{}]+|\{[^{}]*\})*)\}", text):
    media_query = m.group(1).strip()
    body = m.group(2)
    # Check if any of our classes or related elements are mentioned
    keywords = ["experience-map", "featured-projects", "published-project-row", "current-project-grid", "projects", "editorial-cases"]
    matches = [k for k in keywords if k in body]
    if matches:
        print(f"=== @media {media_query} (matches: {matches}) ===")
        print(body.strip())
        print()
