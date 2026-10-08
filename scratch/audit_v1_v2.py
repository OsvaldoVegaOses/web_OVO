import hashlib
import os
import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")

print("=== AUDITORIA INICIAL ===")

v1_files = [
    "index.html",
    "proyectos/pac-arenillas-negras.html",
    "proyectos/medio-humano-desaladora-arica.html",
    "proyectos/deslindes-rios-valparaiso.html",
    "proyectos/pac-la-florida.html",
    "proyectos/plan-maestro-san-felipe.html",
    "proyectos/medio-humano-horcon.html",
    "style.css",
    "script.js",
]

print("\n--- HASHES SHA-256 INICIALES DE V1 ---")
hashes = {}
for rel in v1_files:
    fpath = root / rel
    if fpath.exists():
        h = hashlib.sha256(fpath.read_bytes()).hexdigest()
        hashes[rel] = h
        print(f"{rel}: {h}")
    else:
        print(f"ALERTA: No existe {rel}")

print("\n--- ARCHIVOS -v2 EXISTENTES ---")
v2_found = list(root.glob("**/*-v2*"))
print(f"Total encontrados: {len(v2_found)}")
for f in v2_found:
    print(f"  {f.relative_to(root)}")

print("\n--- ANALISIS DE index2.html ---")
idx2_path = root / "index2.html"
if idx2_path.exists():
    text2 = idx2_path.read_text(encoding="utf-8")
    print(f"Tamaño index2.html: {len(text2)} caracteres, {idx2_path.stat().st_size} bytes")

    # Titles and Meta
    title_m = re.search(r"<title>(.*?)</title>", text2, re.I)
    print("Title:", title_m.group(1) if title_m else "N/A")

    robots_m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+>', text2, re.I)
    print("Robots:", robots_m.group(0) if robots_m else "N/A")

    canon_m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+>', text2, re.I)
    print("Canonical:", canon_m.group(0) if canon_m else "N/A")

    og_url_m = re.search(r'<meta[^>]+property=["\']og:url["\'][^>]+>', text2, re.I)
    print("OG URL:", og_url_m.group(0) if og_url_m else "N/A")

    # Styles and Scripts
    for m in re.finditer(r'<link[^>]+rel=["\']stylesheet["\'][^>]+>', text2, re.I):
        print("Stylesheet:", m.group(0))

    for m in re.finditer(r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>', text2, re.I):
        print("Script src:", m.group(0))

    styles = re.findall(r"<style\b[^>]*>(.*?)</style>", text2, re.S)
    print(f"Tags <style> inline: {len(styles)}")
    if styles:
        print(f"Caracteres de CSS inline: {sum(len(s) for s in styles)}")

    # Proyectos links in index2.html
    print("\n--- ENLACES A PROYECTOS EN index2.html ---")
    proy_links = re.findall(r'href=["\']([^"\']*proyectos/[^"\']*)["\']', text2, re.I)
    for pl in proy_links:
        print(f"  {pl}")

    # All internal href links in index2.html
    print("\n--- TODOS LOS ENLACES (href) EN index2.html ---")
    all_links = re.findall(r'href=["\']([^"\']+)["\']', text2, re.I)
    for l in all_links:
        print(f"  {l}")

print("\n--- ANALISIS DE LAS 6 PAGINAS ORIGINALES ---")
for rel in v1_files[1:7]:
    p = root / rel
    t = p.read_text(encoding="utf-8")
    back_links = re.findall(r'href=["\']([^"\']*index[^"\']*)["\']', t, re.I)
    print(f"\n{rel}:")
    print(f"  Back links a index: {back_links}")
