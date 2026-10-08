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

errors = []

for path in pages:

    text = path.read_text(encoding="utf-8")

    gtm_head = len(re.findall(
        r'GTM-NN64BQC5',
        text,
        re.I
    ))

    clarity = len(re.findall(
        r'ypzia0e866',
        text,
        re.I
    ))

    gtm_noscript = len(re.findall(
        r'googletagmanager\.com/ns\.html\?id=GTM-NN64BQC5',
        text,
        re.I
    ))

    # GTM ID debe aparecer:
    # 1 vez en script head
    # 1 vez en noscript
    gtm_ok = gtm_head == 2

    clarity_ok = clarity == 1
    noscript_ok = gtm_noscript == 1

    print()
    print(path.relative_to(root))
    print("  GTM referencias:", gtm_head, "OK" if gtm_ok else "ERROR")
    print("  Clarity:", clarity, "OK" if clarity_ok else "ERROR")
    print("  GTM noscript:", gtm_noscript, "OK" if noscript_ok else "ERROR")

    if not gtm_ok:
        errors.append(f"{path.name}: GTM referencias={gtm_head}")

    if not clarity_ok:
        errors.append(f"{path.name}: Clarity={clarity}")

    if not noscript_ok:
        errors.append(f"{path.name}: GTM noscript={gtm_noscript}")

print()
print("=" * 70)

if errors:
    print("ERRORES:", len(errors))
    for e in errors:
        print(" -", e)
    raise SystemExit("TRACKING QA: FAIL")

print("ERRORES: 0")
print("TRACKING QA: PASS")
