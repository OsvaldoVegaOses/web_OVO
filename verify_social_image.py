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

expected_image = "https://osvaldovega.cl/assets/seo/osvaldo-vega-og.jpg"

errors = []

for path in pages:

    text = path.read_text(encoding="utf-8")

    print("\n" + "=" * 70)
    print(path.relative_to(root))
    print("=" * 70)

    checks = {
        "charset UTF-8":
            len(re.findall(
                r'<meta\s+charset=["\']?UTF-8["\']?',
                text,
                re.I
            )),

        "og:image":
            len(re.findall(
                r'<meta\s+property=["\']og:image["\']',
                text,
                re.I
            )),

        "og:image:width":
            len(re.findall(
                r'<meta\s+property=["\']og:image:width["\']',
                text,
                re.I
            )),

        "og:image:height":
            len(re.findall(
                r'<meta\s+property=["\']og:image:height["\']',
                text,
                re.I
            )),

        "og:image:alt":
            len(re.findall(
                r'<meta\s+property=["\']og:image:alt["\']',
                text,
                re.I
            )),

        "twitter:image":
            len(re.findall(
                r'<meta\s+name=["\']twitter:image["\']',
                text,
                re.I
            )),
    }

    for label, n in checks.items():
        state = "OK" if n == 1 else f"ERROR ({n})"
        print(f"{label}: {state}")

        if n != 1:
            errors.append(
                f"{path.name}: {label} aparece {n} veces"
            )

    m = re.search(
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)',
        text,
        re.I
    )

    actual = m.group(1) if m else None

    print("URL:", actual)

    if actual != expected_image:
        errors.append(
            f"{path.name}: og:image incorrecta: {actual}"
        )


image = root / "assets" / "seo" / "osvaldo-vega-og.jpg"

print("\n" + "=" * 70)
print("ARCHIVO OG")
print("=" * 70)

if image.exists():
    print("Existe: OK")
    print(f"Tamano: {image.stat().st_size / 1024:.1f} KB")
else:
    errors.append("No existe assets/seo/osvaldo-vega-og.jpg")
    print("Existe: ERROR")


print("\n" + "=" * 70)
print("RESULTADO")
print("=" * 70)

if errors:
    print(f"ERRORES: {len(errors)}")
    for e in errors:
        print(" -", e)
    raise SystemExit("OG SEO QA: FAIL")

print("ERRORES: 0")
print("OG SEO QA: PASS")
