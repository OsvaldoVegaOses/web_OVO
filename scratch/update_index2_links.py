import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
idx2 = root / "index2.html"
content = idx2.read_text(encoding="utf-8")

print("=== ACTUALIZANDO index2.html ===")

# 1. Enlace a style-v2.css
if '<link rel="stylesheet" href="style-v2.css">' not in content:
    content = content.replace(
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="style.css">\n    <link rel="stylesheet" href="style-v2.css">'
    )
    print("Añadido: <link rel=\"stylesheet\" href=\"style-v2.css\">")

# 2. og:url para la variante experimental V2
old_og = '<meta property="og:url" content="https://osvaldovega.cl/">'
new_og = '<meta property="og:url" content="https://osvaldovega.cl/index2.html">'
if old_og in content:
    content = content.replace(old_og, new_og)
    print("Actualizado og:url a https://osvaldovega.cl/index2.html")

# 3. Enlaces a proyectos -> proyectos/*-v2.html
replacements = [
    ("proyectos/pac-arenillas-negras.html", "proyectos/pac-arenillas-negras-v2.html"),
    ("proyectos/medio-humano-desaladora-arica.html", "proyectos/medio-humano-desaladora-arica-v2.html"),
    ("proyectos/deslindes-rios-valparaiso.html", "proyectos/deslindes-rios-valparaiso-v2.html"),
    ("proyectos/pac-la-florida.html", "proyectos/pac-la-florida-v2.html"),
    ("proyectos/plan-maestro-san-felipe.html", "proyectos/plan-maestro-san-felipe-v2.html"),
    ("proyectos/medio-humano-horcon.html", "proyectos/medio-humano-horcon-v2.html"),
]

total_replaced = 0
for old_href, new_href in replacements:
    count = content.count(old_href)
    if count > 0:
        content = content.replace(old_href, new_href)
        print(f"Reemplazado ({count} veces): {old_href} -> {new_href}")
        total_replaced += count
    else:
        print(f"Alerta: {old_href} no encontrado")

print(f"Total enlaces a proyectos actualizados: {total_replaced}")

idx2.write_text(content, encoding="utf-8")
print(f"Guardado index2.html ({len(content)} caracteres, {idx2.stat().st_size} bytes)")
