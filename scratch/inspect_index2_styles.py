import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
idx2 = root / "index2.html"
text = idx2.read_text(encoding="utf-8")

styles = re.findall(r"<style\b[^>]*>(.*?)</style>", text, re.S)
for i, s in enumerate(styles):
    print(f"=== STYLE BLOCK {i+1} (length: {len(s)}) ===")
    lines = s.strip().splitlines()
    print("First 10 lines:")
    for l in lines[:10]:
        print(" ", l)
    print("Last 10 lines:")
    for l in lines[-10:]:
        print(" ", l)
