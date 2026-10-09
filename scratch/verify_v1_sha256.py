#!/usr/bin/env python3
"""Verificacion de integridad SHA-256 de los 9 archivos base de V1.

Conserva dos referencias distintas para index.html:
  - HISTORICA:  hash registrado antes de la actualizacion del correo de contacto.
  - AUTORIZADA: hash registrado despues de la actualizacion autorizada.

Para los otros 8 archivos V1, la linea base no ha cambiado.

Comportamiento:
  - Compara cada archivo contra su LINEA BASE AUTORIZADA ACTUAL.
  - Si coincide con la autorizada y difiere de la historica, reporta como
    AUTORIZADO (no FAIL) y detalla el cambio conocido.
  - Si difiere de ambas referencias, reporta FAIL.
  - Si el archivo no existe, reporta FILE_NOT_FOUND (FAIL).
  - El resultado global es FAIL solo si hay diferencias no explicadas.

Nota de auditoria: No modifica hashes, no restaura archivos automaticamente.
"""

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# LINEAS BASE
# ---------------------------------------------------------------------------
# Para archivos con una unica referencia, el valor es un string de hash.
# Para archivos con cambio autorizado documentado, el valor es un dict con:
#   "historical"    : hash original registrado antes del cambio
#   "authorized"    : hash actual autorizado
#   "change"        : descripcion del cambio
#   "diff_verified" : True si se verifico diff byte a byte
# ---------------------------------------------------------------------------

BASELINES = {
    "index.html": {
        "historical": "dead87da88fab4549e7697b9e7600c0f8fa64b18d83af065db5f1dee6bfa01be",
        "authorized": "729fce9acdc6ec3cc38e23fe86999d0a01109e184c868096387ddd0c4107106a",
        "change": (
            "Actualizacion autorizada del correo de contacto: "
            "boton Escribeme modificado a mailto:contacto@osvaldovega.cl"
        ),
        # La version historica exacta no es recuperable desde el estado actual
        # del repositorio (no hay commit que preserve index.html pre-cambio).
        # El hash historico proviene de la ejecucion de verify_v1_sha256.py
        # antes del commit 17d6bc0. No se puede confirmar diff byte a byte.
        "diff_verified": False,
    },
    "proyectos/pac-arenillas-negras.html":
        "4b2827b5803d33321d198abd2ccd83b02a3fa9bffec6d9f1e364c20b3adb4181",
    "proyectos/medio-humano-desaladora-arica.html":
        "2a369115a607815965658fb97aaa49e8cb181451a18502828222abba3b4d30de",
    "proyectos/deslindes-rios-valparaiso.html":
        "8b83c5a14c2d8873e437abb8a87a5eaab16968026bf3b245819449df23069c4e",
    "proyectos/pac-la-florida.html":
        "e0472912bc251feaab5caa87eca4ecef8bb330b30f8852d5bfcc833f57062e87",
    "proyectos/plan-maestro-san-felipe.html":
        "7bcdcacde85c60d308c205821cdf731559b73fecd21f7972f2f0f71b825aeda4",
    "proyectos/medio-humano-horcon.html":
        "1c570e383b2775ae5f2aa94bd41891fccaa639203bd347f5d051eed811d1fd78",
    "style.css":
        "4534acf4bb30b9e7da5b375177c8191f38b3022179f278719a80f226a22ff387",
    "script.js":
        "ad095b921eb2f10d4feec8a92c79d80d0c2b741e500a09189ef93b30ae1838b0",
}


def get_ref(entry):
    """Devuelve (historical, authorized, change, diff_verified)."""
    if isinstance(entry, dict):
        return (
            entry["historical"],
            entry["authorized"],
            entry.get("change", ""),
            entry.get("diff_verified", False),
        )
    return entry, entry, "", True


def main():
    print("=" * 80)
    print("VERIFICACION DE INTEGRIDAD SHA-256 DE ARCHIVOS V1")
    print(f"Raiz del repositorio: {ROOT}")
    print("=" * 80)

    failures = []
    authorized_changes = []
    passes = []

    for rel, entry in BASELINES.items():
        hist_h, auth_h, change_desc, diff_ok = get_ref(entry)
        p = ROOT / rel

        if not p.exists():
            print(f"\n{rel}: [NO EXISTE (FAIL)]")
            failures.append((rel, "FILE_NOT_FOUND"))
            continue

        current_h = hashlib.sha256(p.read_bytes()).hexdigest()

        if current_h == auth_h:
            if auth_h != hist_h:
                status = "COINCIDE CON LINEA BASE AUTORIZADA"
                authorized_changes.append(rel)
            else:
                status = "INTACTO (PASS)"
            passes.append(rel)
        elif current_h == hist_h and auth_h != hist_h:
            status = "COINCIDE SOLO CON HISTORICA — sin cambio autorizado pendiente (FAIL)"
            failures.append((rel, f"solo coincide con historica: {current_h}"))
        else:
            status = "DIFERENTE DE AMBAS REFERENCIAS (FAIL)"
            failures.append((rel, f"difiere de autorizada ({auth_h}) y de historica ({hist_h}): actual={current_h}"))

        print(f"\n{rel}: [{status}]")
        if auth_h != hist_h:
            print(f"  SHA historico:   {hist_h}")
            print(f"  SHA autorizado:  {auth_h}")
            print(f"  SHA obtenido:    {current_h}")
            print(f"  Cambio conocido: {change_desc}")
            if not diff_ok:
                print("  ADVERTENCIA: version historica no recuperable; diff byte a byte NO verificado.")
        else:
            print(f"  SHA esperado:  {auth_h}")
            print(f"  SHA obtenido:  {current_h}")

    print("\n" + "=" * 80)
    print("RESUMEN INTEGRIDAD SHA-256 V1")
    print(f"Total archivos evaluados: {len(BASELINES)}")
    print(f"PASS (identicos a linea base):              {len(passes) - len(authorized_changes)}")
    print(f"PASS (cambio autorizado documentado):        {len(authorized_changes)}")
    print(f"FAIL (discrepancias no resueltas):           {len(failures)}")
    print("=" * 80)

    if authorized_changes:
        print("\nARCHIVOS CON CAMBIO AUTORIZADO DOCUMENTADO:")
        for r in authorized_changes:
            _, _, desc, diff_ok = get_ref(BASELINES[r])
            print(f"  - {r}: {desc}")
            if not diff_ok:
                print("    Diff byte a byte: NO VERIFICADO (historico no recuperable desde repo actual)")

    if failures:
        print("\nARCHIVOS CON DISCREPANCIA NO RESUELTA:")
        for rel, reason in failures:
            print(f"  - {rel}: {reason}")
        print("\nRESULTADO GLOBAL: FAIL")
        sys.exit(1)
    else:
        if authorized_changes:
            conclusion = (
                "Los 9 archivos V1 coinciden con la linea base autorizada actual.\n"
                "Se conserva el registro historico de la modificacion de index.html."
            )
        else:
            conclusion = "Los 9 archivos V1 son identicos a la linea base original."
        print(f"\n{conclusion}")
        print("\nRESULTADO GLOBAL: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
