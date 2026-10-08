# -*- coding: utf-8 -*-

from pathlib import Path
import re

root = Path(r"C:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")

pages = [
    root / "index.html",
    root / "proyectos" / "pac-arenillas-negras.html",
    root / "proyectos" / "medio-humano-horcon.html",
    root / "proyectos" / "plan-maestro-san-felipe.html",
    root / "proyectos" / "deslindes-rios-valparaiso.html",
    root / "proyectos" / "pac-la-florida.html",
    root / "proyectos" / "medio-humano-desaladora-arica.html",
]

image_url = "https://osvaldovega.cl/assets/seo/osvaldo-vega-og.jpg"

# Usamos escapes Unicode deliberadamente.
image_alt = (
    "Osvaldo Vega Oses \u2014 Soci\u00f3logo, "
    "Medio Humano y Participaci\u00f3n Ciudadana"
)

for path in pages:

    if not path.exists():
        raise SystemExit(f"ERROR: no existe {path}")

    text = path.read_text(encoding="utf-8")

    # Eliminar etiquetas previas para evitar duplicados.
    patterns = [
        r'\s*<meta\s+property=["\']og:image["\'][^>]*>\s*',
        r'\s*<meta\s+property=["\']og:image:width["\'][^>]*>\s*',
        r'\s*<meta\s+property=["\']og:image:height["\'][^>]*>\s*',
        r'\s*<meta\s+property=["\']og:image:alt["\'][^>]*>\s*',
        r'\s*<meta\s+name=["\']twitter:image["\'][^>]*>\s*',
        r'\s*<meta\s+name=["\']twitter:image:alt["\'][^>]*>\s*',
    ]

    for pattern in patterns:
        text = re.sub(pattern, "\n", text, flags=re.I)

    block = f'''
    <!-- Imagen social -->
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{image_alt}">
    <meta name="twitter:image" content="{image_url}">
    <meta name="twitter:image:alt" content="{image_alt}">
'''

    # Insertar inmediatamente antes de </head>
    if not re.search(r"</head>", text, re.I):
        raise SystemExit(f"ERROR: falta </head> en {path}")

    text = re.sub(
        r"</head>",
        block + "\n</head>",
        text,
        count=1,
        flags=re.I
    )

    path.write_text(text, encoding="utf-8")

    print("OK:", path.relative_to(root))

print()
print("OG/TWITTER IMAGE IMPLEMENTADO.")
