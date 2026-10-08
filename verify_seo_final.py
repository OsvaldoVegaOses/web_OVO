#!/usr/bin/env python3
"""Suite de verificación SEO para osvaldovega.cl — V1 (Oficial) y V2 (Experimental).

Verifica metadatos SEO, directivas robots, canónicos, Open Graph, sitemap y robots.txt.
Diseñado para ser portable y ejecutable desde cualquier entorno sin rutas absolutas.
"""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent

OG_IMAGE_URL = "https://osvaldovega.cl/assets/seo/osvaldo-vega-og.jpg"

V1_PAGES = {
    "index.html": "https://osvaldovega.cl/",
    "proyectos/pac-arenillas-negras.html": "https://osvaldovega.cl/proyectos/pac-arenillas-negras.html",
    "proyectos/medio-humano-horcon.html": "https://osvaldovega.cl/proyectos/medio-humano-horcon.html",
    "proyectos/plan-maestro-san-felipe.html": "https://osvaldovega.cl/proyectos/plan-maestro-san-felipe.html",
    "proyectos/deslindes-rios-valparaiso.html": "https://osvaldovega.cl/proyectos/deslindes-rios-valparaiso.html",
    "proyectos/pac-la-florida.html": "https://osvaldovega.cl/proyectos/pac-la-florida.html",
    "proyectos/medio-humano-desaladora-arica.html": "https://osvaldovega.cl/proyectos/medio-humano-desaladora-arica.html",
}

V2_PAGES = {
    "index2.html": {
        "canonical": "https://osvaldovega.cl/",
        "og_url": "https://osvaldovega.cl/index2.html",
    },
    "proyectos/pac-arenillas-negras-v2.html": {
        "canonical": "https://osvaldovega.cl/proyectos/pac-arenillas-negras.html",
        "og_url": "https://osvaldovega.cl/proyectos/pac-arenillas-negras-v2.html",
    },
    "proyectos/medio-humano-horcon-v2.html": {
        "canonical": "https://osvaldovega.cl/proyectos/medio-humano-horcon.html",
        "og_url": "https://osvaldovega.cl/proyectos/medio-humano-horcon-v2.html",
    },
    "proyectos/plan-maestro-san-felipe-v2.html": {
        "canonical": "https://osvaldovega.cl/proyectos/plan-maestro-san-felipe.html",
        "og_url": "https://osvaldovega.cl/proyectos/plan-maestro-san-felipe-v2.html",
    },
    "proyectos/deslindes-rios-valparaiso-v2.html": {
        "canonical": "https://osvaldovega.cl/proyectos/deslindes-rios-valparaiso.html",
        "og_url": "https://osvaldovega.cl/proyectos/deslindes-rios-valparaiso-v2.html",
    },
    "proyectos/pac-la-florida-v2.html": {
        "canonical": "https://osvaldovega.cl/proyectos/pac-la-florida.html",
        "og_url": "https://osvaldovega.cl/proyectos/pac-la-florida-v2.html",
    },
    "proyectos/medio-humano-desaladora-arica-v2.html": {
        "canonical": "https://osvaldovega.cl/proyectos/medio-humano-desaladora-arica.html",
        "og_url": "https://osvaldovega.cl/proyectos/medio-humano-desaladora-arica-v2.html",
    },
}

def extract(pattern, text):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else None

def main():
    errors = []
    print("=" * 85)
    print("VERIFICACION SEO COMPLETA — V1 (OFICIAL) Y V2 (EXPERIMENTAL)")
    print(f"Raíz del repositorio: {ROOT}")
    print("=" * 85)

    # 1. VERIFICACION V1 (OFICIAL)
    print("\n--- 1. EVALUANDO PAGINAS V1 (OFICIALES - INDEX, FOLLOW) ---")
    for rel, expected_url in V1_PAGES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"[V1] {rel}: Archivo no existe")
            continue
        text = path.read_text(encoding="utf-8")

        canonical = extract(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text)
        og_url = extract(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)', text)
        image = extract(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)', text)
        robots = extract(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', text)
        title = extract(r'<title>(.*?)</title>', text)
        description = extract(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)', text)
        h1_matches = re.findall(r'<h1\b[^>]*>(.*?)</h1>', text, re.I | re.S)

        print(f"\n{rel}")
        print(f"  canonical:   {canonical}")
        print(f"  og:url:      {og_url}")
        print(f"  robots:      {robots}")
        print(f"  H1 count:    {len(h1_matches)}")
        print(f"  title:       {title[:50] + '...' if title and len(title) > 50 else title}")

        if canonical != expected_url:
            errors.append(f"[V1] {rel}: canonical incorrecto (esperado: {expected_url}, obtenido: {canonical})")
        if og_url != expected_url:
            errors.append(f"[V1] {rel}: og:url incorrecto (esperado: {expected_url}, obtenido: {og_url})")
        if image != OG_IMAGE_URL:
            errors.append(f"[V1] {rel}: og:image incorrecto ({image})")
        if robots != "index, follow":
            errors.append(f"[V1] {rel}: robots incorrecto (esperado 'index, follow', obtenido '{robots}')")
        if not title:
            errors.append(f"[V1] {rel}: Falta <title>")
        if not description:
            errors.append(f"[V1] {rel}: Falta meta description")
        if len(h1_matches) != 1:
            errors.append(f"[V1] {rel}: Debe tener exactamente un H1 (encontrados: {len(h1_matches)})")

        # Sin www en metadata SEO
        seo_fragments = re.findall(r'(?:canonical|og:url|og:image|twitter:image)[^>]+>', text, re.I)
        for fragment in seo_fragments:
            if "www.osvaldovega.cl" in fragment:
                errors.append(f"[V1] {rel}: Aparece 'www' en metadata SEO: {fragment}")

    # 2. VERIFICACION V2 (EXPERIMENTAL)
    print("\n--- 2. EVALUANDO PAGINAS V2 (EXPERIMENTALES - NOINDEX, FOLLOW) ---")
    for rel, meta in V2_PAGES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"[V2] {rel}: Archivo no existe")
            continue
        text = path.read_text(encoding="utf-8")

        canonical = extract(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text)
        og_url = extract(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)', text)
        robots = extract(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', text)
        title = extract(r'<title>(.*?)</title>', text)
        description = extract(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)', text)
        h1_matches = re.findall(r'<h1\b[^>]*>(.*?)</h1>', text, re.I | re.S)
        charset = extract(r'<meta\s+charset=["\']([^"\']+)', text)

        print(f"\n{rel}")
        print(f"  canonical:   {canonical}")
        print(f"  og:url:      {og_url}")
        print(f"  robots:      {robots}")
        print(f"  H1 count:    {len(h1_matches)}")
        print(f"  charset:     {charset}")

        if canonical != meta["canonical"]:
            errors.append(f"[V2] {rel}: canonical incorrecto (esperado hacia V1: {meta['canonical']}, obtenido: {canonical})")
        if og_url != meta["og_url"]:
            errors.append(f"[V2] {rel}: og:url incorrecto (esperado hacia V2: {meta['og_url']}, obtenido: {og_url})")
        if robots != "noindex, follow":
            errors.append(f"[V2] {rel}: robots incorrecto (esperado 'noindex, follow', obtenido '{robots}')")
        if not title:
            errors.append(f"[V2] {rel}: Falta <title>")
        if not description:
            errors.append(f"[V2] {rel}: Falta meta description")
        if len(h1_matches) != 1:
            errors.append(f"[V2] {rel}: Debe tener exactamente un H1 (encontrados: {len(h1_matches)})")
        if not charset or charset.lower() != "utf-8":
            errors.append(f"[V2] {rel}: Charset debe ser UTF-8 (obtenido: {charset})")

    # 3. VERIFICACION SITEMAP.XML
    print("\n--- 3. EVALUANDO SITEMAP.XML ---")
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        errors.append("sitemap.xml no existe")
    else:
        try:
            tree = ET.parse(sitemap_path)
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = [e.text.strip() for e in tree.findall(".//s:loc", ns) if e.text]
            expected_sitemap_urls = list(V1_PAGES.values())
            print(f"URLs en sitemap: {len(urls)}")

            if urls != expected_sitemap_urls:
                errors.append(f"sitemap.xml no coincide exactamente con las 7 URLs oficiales V1")
            v2_in_sitemap = [u for u in urls if "index2" in u or "-v2" in u]
            if v2_in_sitemap:
                errors.append(f"sitemap.xml contiene URLs V2 indebidas: {v2_in_sitemap}")
            if any("www.osvaldovega.cl" in u for u in urls):
                errors.append("sitemap.xml contiene referencias 'www'")
            print("sitemap.xml: OK (contiene exclusivamente las 7 URLs oficiales V1)")
        except Exception as exc:
            errors.append(f"sitemap.xml no es XML válido: {exc}")

    # 4. VERIFICACION ROBOTS.TXT
    print("\n--- 4. EVALUANDO ROBOTS.TXT ---")
    robots_path = ROOT / "robots.txt"
    if not robots_path.exists():
        errors.append("robots.txt no existe")
    else:
        robots_text = robots_path.read_text(encoding="utf-8")
        expected_sitemap_line = "Sitemap: https://osvaldovega.cl/sitemap.xml"
        if expected_sitemap_line not in robots_text:
            errors.append("robots.txt no apunta al sitemap canónico")
        # Verificar que no bloquee rastreo de V2
        if re.search(r'Disallow:\s*/.*(?:index2|-v2)', robots_text, re.I):
            errors.append("robots.txt contiene directivas Disallow bloqueando V2 (debe permitir rastreo para leer noindex)")
        print("robots.txt: OK (no bloquea V2 y apunta al sitemap)")

    # 5. RECURSO FISICO OG IMAGE
    print("\n--- 5. EVALUANDO RECURSO FISICO OG IMAGE ---")
    og_file = ROOT / "assets" / "seo" / "osvaldo-vega-og.jpg"
    if not og_file.exists():
        errors.append("Archivo físico falta: assets/seo/osvaldo-vega-og.jpg")
    else:
        print(f"assets/seo/osvaldo-vega-og.jpg: OK ({og_file.stat().st_size / 1024:.1f} KB)")

    print("\n" + "=" * 85)
    print("RESUMEN FINAL SEO QA")
    print(f"Páginas evaluadas: {len(V1_PAGES) + len(V2_PAGES)} (7 V1 + 7 V2)")
    print(f"Errores encontrados: {len(errors)}")
    print("=" * 85)

    if errors:
        for e in errors:
            print(f" - {e}")
        print("\nRESULTADO GLOBAL: FAIL")
        sys.exit(1)
    else:
        print("RESULTADO GLOBAL: PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
