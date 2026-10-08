import re
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")
proyectos_dir = root / "proyectos"

mapping = [
    ("pac-arenillas-negras.html", "pac-arenillas-negras-v2.html"),
    ("medio-humano-desaladora-arica.html", "medio-humano-desaladora-arica-v2.html"),
    ("deslindes-rios-valparaiso.html", "deslindes-rios-valparaiso-v2.html"),
    ("pac-la-florida.html", "pac-la-florida-v2.html"),
    ("plan-maestro-san-felipe.html", "plan-maestro-san-felipe-v2.html"),
    ("medio-humano-horcon.html", "medio-humano-horcon-v2.html"),
]

print("=== GENERANDO LAS 6 PAGINAS V2 ===")

for orig_name, v2_name in mapping:
    orig_path = proyectos_dir / orig_name
    v2_path = proyectos_dir / v2_name

    orig_content = orig_path.read_text(encoding="utf-8")

    # 1. Copia base
    content = orig_content

    # 2. Reemplazo de enlaces a index.html -> index2.html
    # Preservando fragmentos (#inicio, #proyectos, #que-hago, #metodologia, #sobre-mi, #innovacion, #contacto)
    content = content.replace("../index.html", "../index2.html")

    # 3. Metadatos SEO para fase experimental
    # robots: noindex, follow
    content = re.sub(
        r'<meta\s+name=["\']robots["\']\s+content=["\']index,\s*follow["\']>',
        '<meta name="robots" content="noindex, follow">',
        content,
        flags=re.I
    )

    # Canonical se mantiene apuntando al V1 original:
    # <link rel="canonical" href="https://osvaldovega.cl/proyectos/{orig_name}">
    # Verificamos que contenga el canonical esperado
    expected_canonical = f'<link rel="canonical" href="https://osvaldovega.cl/proyectos/{orig_name}">'
    assert expected_canonical in content, f"Canonical no encontrado en {orig_name}"

    # og:url debe apuntar a la propia URL de V2
    orig_og_url = f'<meta property="og:url" content="https://osvaldovega.cl/proyectos/{orig_name}">'
    v2_og_url = f'<meta property="og:url" content="https://osvaldovega.cl/proyectos/{v2_name}">'
    assert orig_og_url in content, f"og:url no encontrado en {orig_name}"
    content = content.replace(orig_og_url, v2_og_url)

    # 4. Identificación interna de versión
    version_comment = f'<!-- Versión: V2 Experimental (Publicación Paralela OVO) -->\n    <meta name="version" content="v2-experimental">\n'
    content = content.replace('<!-- SEO técnico -->', f'<!-- SEO técnico -->\n    {version_comment}')

    v2_path.write_text(content, encoding="utf-8")
    print(f"Creado: {v2_name} ({len(content)} caracteres, {v2_path.stat().st_size} bytes)")

print("\nVerificación de archivos creados...")
for _, v2_name in mapping:
    p = proyectos_dir / v2_name
    assert p.exists(), f"Error: no existe {v2_name}"
    text = p.read_text(encoding="utf-8")
    assert "noindex, follow" in text
    assert "../index2.html" in text
    assert "../index.html" not in text
    assert f"proyectos/{v2_name}" in text
    print(f"  {v2_name}: OK (noindex, index2 links, canonical V1, og:url V2)")

print("\nTODAS LAS PAGINAS V2 CREADAS EXITOSAMENTE.")
