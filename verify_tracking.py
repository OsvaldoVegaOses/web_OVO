#!/usr/bin/env python3
"""Suite de verificación de tracking estático para osvaldovega.cl — V1 y V2.

Verifica la presencia e integridad de Google Tag Manager (GTM-NN64BQC5)
y Microsoft Clarity (ypzia0e866) en las 14 páginas del portafolio.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent

PAGES = [
    # V1 (Oficial)
    "index.html",
    "proyectos/pac-arenillas-negras.html",
    "proyectos/medio-humano-horcon.html",
    "proyectos/plan-maestro-san-felipe.html",
    "proyectos/deslindes-rios-valparaiso.html",
    "proyectos/pac-la-florida.html",
    "proyectos/medio-humano-desaladora-arica.html",
    # V2 (Experimental)
    "index2.html",
    "proyectos/pac-arenillas-negras-v2.html",
    "proyectos/medio-humano-horcon-v2.html",
    "proyectos/plan-maestro-san-felipe-v2.html",
    "proyectos/deslindes-rios-valparaiso-v2.html",
    "proyectos/pac-la-florida-v2.html",
    "proyectos/medio-humano-desaladora-arica-v2.html",
]

GTM_ID = "GTM-NN64BQC5"
CLARITY_ID = "ypzia0e866"

def main():
    errors = []
    print("=" * 80)
    print("VERIFICACION DE TRACKING ESTATICO (GTM & CLARITY) — 14 PAGINAS")
    print(f"Raíz del repositorio: {ROOT}")
    print("=" * 80)

    for rel in PAGES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{rel}: Archivo no encontrado")
            continue

        text = path.read_text(encoding="utf-8")

        gtm_head_matches = len(re.findall(re.escape(GTM_ID), text, re.I))
        clarity_matches = len(re.findall(re.escape(CLARITY_ID), text, re.I))
        gtm_noscript_matches = len(re.findall(
            r'googletagmanager\.com/ns\.html\?id=' + re.escape(GTM_ID),
            text,
            re.I
        ))

        # GTM ID debe aparecer:
        # 1 vez en script head
        # 1 vez en noscript body
        gtm_ok = (gtm_head_matches == 2)
        clarity_ok = (clarity_matches == 1)
        noscript_ok = (gtm_noscript_matches == 1)

        status_str = "OK" if (gtm_ok and clarity_ok and noscript_ok) else "ERROR"
        print(f"\n{rel}: [{status_str}]")
        print(f"  GTM referencias: {gtm_head_matches} (esperado 2: script + noscript)")
        print(f"  Clarity:         {clarity_matches} (esperado 1)")
        print(f"  GTM noscript:    {gtm_noscript_matches} (esperado 1)")

        if not gtm_ok:
            errors.append(f"{rel}: GTM referencias incorrectas ({gtm_head_matches}, esperado 2)")
        if not clarity_ok:
            errors.append(f"{rel}: Clarity referencias incorrectas ({clarity_matches}, esperado 1)")
        if not noscript_ok:
            errors.append(f"{rel}: GTM noscript incorrecto ({gtm_noscript_matches}, esperado 1)")

    print("\n" + "=" * 80)
    print("RESUMEN TRACKING QA")
    print(f"Páginas evaluadas: {len(PAGES)}")
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
