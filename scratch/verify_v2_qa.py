import re
import os
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")

v2_projects = [
    ("pac-arenillas-negras-v2.html", "pac-arenillas-negras.html"),
    ("medio-humano-desaladora-arica-v2.html", "medio-humano-desaladora-arica.html"),
    ("deslindes-rios-valparaiso-v2.html", "deslindes-rios-valparaiso.html"),
    ("pac-la-florida-v2.html", "pac-la-florida.html"),
    ("plan-maestro-san-felipe-v2.html", "plan-maestro-san-felipe.html"),
    ("medio-humano-horcon-v2.html", "medio-humano-horcon.html"),
]

errors = []

print("=== VERIFICACION EXHAUSTIVA DE V2 ===")

# 1. index2.html
idx2_path = root / "index2.html"
idx2_text = idx2_path.read_text(encoding="utf-8")

# Check robots
if '<meta name="robots" content="noindex, follow">' not in idx2_text:
    errors.append("index2.html: Falta robots noindex, follow")

# Check canonical
if '<link rel="canonical" href="https://osvaldovega.cl/">' not in idx2_text:
    errors.append("index2.html: Canonical incorrecto (debe ser https://osvaldovega.cl/)")

# Check og:url
if '<meta property="og:url" content="https://osvaldovega.cl/index2.html">' not in idx2_text:
    errors.append("index2.html: og:url incorrecto (debe ser https://osvaldovega.cl/index2.html)")

# Check project links in index2.html
all_proy_links = re.findall(r'href=["\']([^"\']*proyectos/[^"\']*)["\']', idx2_text)
print(f"index2.html: {len(all_proy_links)} enlaces a proyectos encontrados")
for link in all_proy_links:
    if not link.endswith("-v2.html"):
        errors.append(f"index2.html: Enlace a proyecto no apunta a -v2.html: {link}")
    else:
        # Check target file exists
        target_path = root / link
        if not target_path.exists():
            errors.append(f"index2.html: Archivo destino no existe: {link}")

# Check 6 V2 projects
for v2_file, v1_file in v2_projects:
    p = root / "proyectos" / v2_file
    if not p.exists():
        errors.append(f"No existe archivo: {v2_file}")
        continue
    text = p.read_text(encoding="utf-8")

    # Check robots
    if '<meta name="robots" content="noindex, follow">' not in text:
        errors.append(f"{v2_file}: Falta noindex, follow")

    # Check canonical points to V1
    expected_canon = f'https://osvaldovega.cl/proyectos/{v1_file}'
    m_canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text)
    if not m_canon or m_canon.group(1) != expected_canon:
        errors.append(f"{v2_file}: Canonical incorrecto. Encontrado: {m_canon.group(1) if m_canon else 'None'}, esperado: {expected_canon}")

    # Check og:url points to V2
    expected_og = f'https://osvaldovega.cl/proyectos/{v2_file}'
    m_og = re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)', text)
    if not m_og or m_og.group(1) != expected_og:
        errors.append(f"{v2_file}: og:url incorrecto. Encontrado: {m_og.group(1) if m_og else 'None'}, esperado: {expected_og}")

    # Check no back links to index.html
    bad_back = re.findall(r'href=["\']([^"\']*index\.html[^"\']*)["\']', text)
    if bad_back:
        errors.append(f"{v2_file}: Contiene enlaces a index.html (V1): {bad_back}")

    # Check return links to index2.html
    good_back = re.findall(r'href=["\']([^"\']*index2\.html[^"\']*)["\']', text)
    if len(good_back) < 7:
        errors.append(f"{v2_file}: Menos de 7 enlaces de regreso a index2.html: {len(good_back)}")

    # Check H1 count
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', text, re.S)
    if len(h1s) != 1:
        errors.append(f"{v2_file}: Cantidad de H1 distinta de 1 ({len(h1s)})")

    # Check GTM and Clarity
    if "GTM-NN64BQC5" not in text:
        errors.append(f"{v2_file}: Falta GTM")
    if "ypzia0e866" not in text:
        errors.append(f"{v2_file}: Falta Clarity")

    # Check internal anchors (#...)
    anchors = re.findall(r'href=["\']#([^"\']+)["\']', text)
    for a in anchors:
        if f'id="{a}"' not in text and f"id='{a}'" not in text and f'name="{a}"' not in text:
            errors.append(f"{v2_file}: Ancla interna #{a} sin destino en la página")

    # Check local image/css/script references
    local_refs = re.findall(r'(?:src|href)=["\']((?:\.\./|Fotos_proyectos/|assets/)[^"\']+)["\']', text)
    for ref in local_refs:
        clean_ref = ref.split("?")[0].split("#")[0]
        # Resolve relative to proyectos/
        resolved = (root / "proyectos" / clean_ref).resolve()
        if not resolved.exists():
            errors.append(f"{v2_file}: Recurso no encontrado: {ref} -> {resolved}")

print(f"\nTotal errores encontrados en V2: {len(errors)}")
if errors:
    for e in errors:
        print(" -", e)
    raise SystemExit("V2 QA: FAIL")
else:
    print("V2 QA: PASS (Todos los controles de navegación, SEO, enlaces, imágenes y anclas pasaron exitosamente).")
