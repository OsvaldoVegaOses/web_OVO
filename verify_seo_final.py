from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = Path(r"C:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")

pages = {
    "index.html": "https://osvaldovega.cl/",
    "proyectos/pac-arenillas-negras.html":
        "https://osvaldovega.cl/proyectos/pac-arenillas-negras.html",
    "proyectos/medio-humano-horcon.html":
        "https://osvaldovega.cl/proyectos/medio-humano-horcon.html",
    "proyectos/plan-maestro-san-felipe.html":
        "https://osvaldovega.cl/proyectos/plan-maestro-san-felipe.html",
    "proyectos/deslindes-rios-valparaiso.html":
        "https://osvaldovega.cl/proyectos/deslindes-rios-valparaiso.html",
    "proyectos/pac-la-florida.html":
        "https://osvaldovega.cl/proyectos/pac-la-florida.html",
    "proyectos/medio-humano-desaladora-arica.html":
        "https://osvaldovega.cl/proyectos/medio-humano-desaladora-arica.html",
}

og_image = "https://osvaldovega.cl/assets/seo/osvaldo-vega-og.jpg"

errors = []

for rel, expected_url in pages.items():
    path = root / rel
    text = path.read_text(encoding="utf-8")

    print("\n" + "=" * 85)
    print(rel)
    print("=" * 85)

    def extract(pattern):
        m = re.search(pattern, text, re.I | re.S)
        return m.group(1).strip() if m else None

    canonical = extract(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)'
    )

    og_url = extract(
        r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)'
    )

    image = extract(
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)'
    )

    robots = extract(
        r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)'
    )

    print("canonical:", canonical)
    print("og:url:   ", og_url)
    print("og:image: ", image)
    print("robots:   ", robots)

    if canonical != expected_url:
        errors.append(f"{rel}: canonical incorrecto")

    if og_url != expected_url:
        errors.append(f"{rel}: og:url incorrecto")

    if image != og_image:
        errors.append(f"{rel}: og:image incorrecto")

    if robots != "index, follow":
        errors.append(f"{rel}: robots incorrecto")

    # No queremos www en señales SEO absolutas
    seo_fragments = re.findall(
        r'(?:canonical|og:url|og:image|twitter:image)[^>]+>',
        text,
        re.I
    )

    for fragment in seo_fragments:
        if "www.osvaldovega.cl" in fragment:
            errors.append(f"{rel}: aparece www en metadata SEO")


# robots.txt
robots_path = root / "robots.txt"

if not robots_path.exists():
    errors.append("robots.txt no existe")
else:
    robots_text = robots_path.read_text(encoding="utf-8")

    expected_sitemap = "Sitemap: https://osvaldovega.cl/sitemap.xml"

    if expected_sitemap not in robots_text:
        errors.append("robots.txt no apunta al sitemap canónico")

    print("\nrobots.txt: OK")


# sitemap.xml
sitemap_path = root / "sitemap.xml"

if not sitemap_path.exists():
    errors.append("sitemap.xml no existe")
else:
    try:
        tree = ET.parse(sitemap_path)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        urls = [
            e.text.strip()
            for e in tree.findall(".//s:loc", ns)
            if e.text
        ]

        expected = list(pages.values())

        print("sitemap URLs:", len(urls))

        if urls != expected:
            errors.append("sitemap no coincide con las 7 URLs canónicas")

        if any("www.osvaldovega.cl" in u for u in urls):
            errors.append("sitemap contiene www")

    except Exception as exc:
        errors.append(f"sitemap XML inválido: {exc}")


# OG image física
og_file = root / "assets" / "seo" / "osvaldo-vega-og.jpg"

if not og_file.exists():
    errors.append("falta assets/seo/osvaldo-vega-og.jpg")
else:
    print(f"OG image física: OK ({og_file.stat().st_size / 1024:.1f} KB)")


print("\n" + "=" * 85)
print("SEO FINAL QA")
print("=" * 85)

if errors:
    print("ERRORES:", len(errors))
    for e in errors:
        print(" -", e)
    raise SystemExit("SEO FINAL QA: FAIL")

print("ERRORES: 0")
print("SEO FINAL QA: PASS")
