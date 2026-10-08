#!/usr/bin/env python3
"""Suite de verificación de navegación y enlaces V1/V2 para osvaldovega.cl.

Verifica:
1. Enlaces a proyectos en index.html apuntan exclusivamente a casos originales V1.
2. Enlaces a proyectos en index2.html apuntan exclusivamente a casos V2 (*-v2.html).
3. Enlaces de retorno en casos V1 apuntan a index.html.
4. Enlaces de retorno en casos V2 apuntan a index2.html.
5. Anclas internas (#fragmento) resuelven a identificadores válidos en el documento.
6. Enlaces de correo en index.html e index2.html usan contacto@osvaldovega.cl.
7. Recursos locales (fotos, css, scripts) existen físicamente en disco.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

V1_PROJECTS = [
    "pac-arenillas-negras.html",
    "medio-humano-desaladora-arica.html",
    "deslindes-rios-valparaiso.html",
    "pac-la-florida.html",
    "plan-maestro-san-felipe.html",
    "medio-humano-horcon.html",
]

V2_PROJECTS = [
    "pac-arenillas-negras-v2.html",
    "medio-humano-desaladora-arica-v2.html",
    "deslindes-rios-valparaiso-v2.html",
    "pac-la-florida-v2.html",
    "plan-maestro-san-felipe-v2.html",
    "medio-humano-horcon-v2.html",
]

def main():
    errors = []
    print("=" * 80)
    print("VERIFICACION DE NAVEGACION, AISLAMIENTO Y RECURSOS (V1 & V2)")
    print(f"Raíz del repositorio: {ROOT}")
    print("=" * 80)

    # 1. index.html (V1)
    idx_path = ROOT / "index.html"
    if not idx_path.exists():
        errors.append("index.html no existe")
    else:
        text = idx_path.read_text(encoding="utf-8")
        # Enlaces a proyectos en V1
        proy_links = re.findall(r'href=["\']([^"\']*proyectos/[^"\']*)["\']', text)
        print(f"\nindex.html (V1): {len(proy_links)} enlaces a proyectos encontrados")
        for link in proy_links:
            clean_link = link.split("#")[0]
            if "-v2.html" in clean_link:
                errors.append(f"index.html: Enlace V1 apunta indebidamente a variante V2: {link}")
            target_path = ROOT / clean_link
            if not target_path.exists():
                errors.append(f"index.html: Archivo destino no existe: {link}")

        # Enlace de contacto en V1
        mail_links = re.findall(r'href=["\']mailto:([^"\']+)["\']', text)
        if "contacto@osvaldovega.cl" not in mail_links:
            errors.append(f"index.html: Enlace mailto no usa contacto@osvaldovega.cl (encontrados: {mail_links})")
        else:
            print("  Botón de contacto en index.html: OK (mailto:contacto@osvaldovega.cl)")

    # 2. index2.html (V2)
    idx2_path = ROOT / "index2.html"
    if not idx2_path.exists():
        errors.append("index2.html no existe")
    else:
        text2 = idx2_path.read_text(encoding="utf-8")
        # Enlaces a proyectos en V2
        proy2_links = re.findall(r'href=["\']([^"\']*proyectos/[^"\']*)["\']', text2)
        print(f"\nindex2.html (V2): {len(proy2_links)} enlaces a proyectos encontrados")
        for link in proy2_links:
            clean_link = link.split("#")[0]
            if not clean_link.endswith("-v2.html"):
                errors.append(f"index2.html: Enlace V2 NO apunta a -v2.html: {link}")
            target_path = ROOT / clean_link
            if not target_path.exists():
                errors.append(f"index2.html: Archivo destino no existe: {link}")

        # Enlace de contacto en V2
        mail2_links = re.findall(r'href=["\']mailto:([^"\']+)["\']', text2)
        if "contacto@osvaldovega.cl" not in mail2_links:
            errors.append(f"index2.html: Enlace mailto no usa contacto@osvaldovega.cl (encontrados: {mail2_links})")
        else:
            print("  Botón de contacto en index2.html: OK (mailto:contacto@osvaldovega.cl)")

    # 3. Páginas de proyectos V1
    print("\n--- EVALUANDO CASOS V1 (RETORNOS A INDEX.HTML Y RECURSOS) ---")
    for f in V1_PROJECTS:
        p = ROOT / "proyectos" / f
        if not p.exists():
            errors.append(f"proyectos/{f}: Archivo no existe")
            continue
        text = p.read_text(encoding="utf-8")

        # Retornos no deben apuntar a index2
        bad_back = re.findall(r'href=["\']([^"\']*index2\.html[^"\']*)["\']', text)
        if bad_back:
            errors.append(f"proyectos/{f}: Contiene enlaces a index2.html (V2): {bad_back}")

        # Retornos deben apuntar a index.html
        good_back = re.findall(r'href=["\']([^"\']*index\.html[^"\']*)["\']', text)
        if len(good_back) < 7:
            errors.append(f"proyectos/{f}: Faltan enlaces de retorno a index.html ({len(good_back)})")

        # Anclas internas
        anchors = re.findall(r'href=["\']#([^"\']+)["\']', text)
        for a in set(anchors):
            if f'id="{a}"' not in text and f"id='{a}'" not in text and f'name="{a}"' not in text:
                errors.append(f"proyectos/{f}: Ancla #{a} sin destino en la página")

        # Recursos locales
        local_refs = re.findall(r'(?:src|href)=["\']((?:\.\./|Fotos_proyectos/|assets/)[^"\']+)["\']', text)
        for ref in local_refs:
            clean_ref = ref.split("?")[0].split("#")[0]
            resolved = (ROOT / "proyectos" / clean_ref).resolve()
            if not resolved.exists():
                errors.append(f"proyectos/{f}: Recurso no encontrado: {ref}")

        print(f"proyectos/{f}: OK (retornos V1: {len(good_back)}, anclas: {len(set(anchors))})")

    # 4. Páginas de proyectos V2
    print("\n--- EVALUANDO CASOS V2 (RETORNOS A INDEX2.HTML Y RECURSOS) ---")
    for f in V2_PROJECTS:
        p = ROOT / "proyectos" / f
        if not p.exists():
            errors.append(f"proyectos/{f}: Archivo no existe")
            continue
        text = p.read_text(encoding="utf-8")

        # Retornos no deben apuntar a index.html
        bad_back = re.findall(r'href=["\']([^"\']*index\.html[^"\']*)["\']', text)
        if bad_back:
            errors.append(f"proyectos/{f}: Contiene enlaces indebidos a index.html (V1): {bad_back}")

        # Retornos deben apuntar a index2.html
        good_back = re.findall(r'href=["\']([^"\']*index2\.html[^"\']*)["\']', text)
        if len(good_back) < 7:
            errors.append(f"proyectos/{f}: Faltan enlaces de retorno a index2.html ({len(good_back)})")

        # Anclas internas
        anchors = re.findall(r'href=["\']#([^"\']+)["\']', text)
        for a in set(anchors):
            if f'id="{a}"' not in text and f"id='{a}'" not in text and f'name="{a}"' not in text:
                errors.append(f"proyectos/{f}: Ancla #{a} sin destino en la página")

        # Recursos locales
        local_refs = re.findall(r'(?:src|href)=["\']((?:\.\./|Fotos_proyectos/|assets/)[^"\']+)["\']', text)
        for ref in local_refs:
            clean_ref = ref.split("?")[0].split("#")[0]
            resolved = (ROOT / "proyectos" / clean_ref).resolve()
            if not resolved.exists():
                errors.append(f"proyectos/{f}: Recurso no encontrado: {ref}")

        print(f"proyectos/{f}: OK (retornos V2: {len(good_back)}, anclas: {len(set(anchors))})")

    print("\n" + "=" * 80)
    print("RESUMEN NAVEGACION QA")
    print(f"Errores encontrados: {len(errors)}")
    print("=" * 80)

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
