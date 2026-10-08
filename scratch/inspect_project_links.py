import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
v1_files = [
    "proyectos/pac-arenillas-negras.html",
    "proyectos/medio-humano-desaladora-arica.html",
    "proyectos/deslindes-rios-valparaiso.html",
    "proyectos/pac-la-florida.html",
    "proyectos/plan-maestro-san-felipe.html",
    "proyectos/medio-humano-horcon.html",
]

for rel in v1_files:
    p = root / rel
    text = p.read_text(encoding="utf-8")
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', text)
    index_hrefs = [h for h in hrefs if "index" in h]
    other_html = [h for h in hrefs if ".html" in h and "index" not in h]
    print(f"=== {rel} ===")
    print("  Index hrefs:", set(index_hrefs))
    print("  Other html hrefs:", set(other_html))
