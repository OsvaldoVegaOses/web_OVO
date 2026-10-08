#!/usr/bin/env python3
"""Verificación de integridad SHA-256 de los 9 archivos base de V1.

Comprueba que los archivos de V1 conserven sus huellas de la línea base.
Nota de auditoría: No modifica huellas esperadas ni restaura archivos automáticamente.
Si alguna comparación falla, reporta FAIL y el diff de hash.
"""

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

INITIAL_HASHES = {
    "index.html": "729fce9acdc6ec3cc38e23fe86999d0a01109e184c868096387ddd0c4107106a",  # actualizado: mailto contacto@osvaldovega.cl
    "proyectos/pac-arenillas-negras.html": "4b2827b5803d33321d198abd2ccd83b02a3fa9bffec6d9f1e364c20b3adb4181",
    "proyectos/medio-humano-desaladora-arica.html": "2a369115a607815965658fb97aaa49e8cb181451a18502828222abba3b4d30de",
    "proyectos/deslindes-rios-valparaiso.html": "8b83c5a14c2d8873e437abb8a87a5eaab16968026bf3b245819449df23069c4e",
    "proyectos/pac-la-florida.html": "e0472912bc251feaab5caa87eca4ecef8bb330b30f8852d5bfcc833f57062e87",
    "proyectos/plan-maestro-san-felipe.html": "7bcdcacde85c60d308c205821cdf731559b73fecd21f7972f2f0f71b825aeda4",
    "proyectos/medio-humano-horcon.html": "1c570e383b2775ae5f2aa94bd41891fccaa639203bd347f5d051eed811d1fd78",
    "style.css": "4534acf4bb30b9e7da5b375177c8191f38b3022179f278719a80f226a22ff387",
    "script.js": "ad095b921eb2f10d4feec8a92c79d80d0c2b741e500a09189ef93b30ae1838b0",
}

def main():
    print("=" * 80)
    print("VERIFICACION DE INTEGRIDAD SHA-256 DE ARCHIVOS V1")
    print(f"Raíz del repositorio: {ROOT}")
    print("=" * 80)

    mismatches = []
    passes = []

    for rel, expected_h in INITIAL_HASHES.items():
        p = ROOT / rel
        if not p.exists():
            print(f"\n{rel}: NO EXISTE (FAIL)")
            mismatches.append((rel, expected_h, "FILE_NOT_FOUND"))
            continue

        current_h = hashlib.sha256(p.read_bytes()).hexdigest()
        match = (current_h == expected_h)
        status = "INTACTO (PASS)" if match else "MODIFICADO (FAIL)"
        print(f"\n{rel}: [{status}]")
        print(f"  SHA esperado: {expected_h}")
        print(f"  SHA obtenido: {current_h}")

        if match:
            passes.append(rel)
        else:
            mismatches.append((rel, expected_h, current_h))

    print("\n" + "=" * 80)
    print("RESUMEN INTEGRIDAD SHA-256 V1")
    print(f"Total archivos evaluados: {len(INITIAL_HASHES)}")
    print(f"PASS: {len(passes)}")
    print(f"FAIL: {len(mismatches)}")
    print("=" * 80)

    if mismatches:
        print("\nARCHIVOS CON DISCREPANCIA RESPECTO DE LA LINEA BASE INICIAL:")
        for rel, exp, obt in mismatches:
            print(f" - {rel}:")
            print(f"     Esperado: {exp}")
            print(f"     Obtenido: {obt}")
        print("\nRESULTADO GLOBAL: FAIL")
        sys.exit(1)
    else:
        print("\nRESULTADO GLOBAL: PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
