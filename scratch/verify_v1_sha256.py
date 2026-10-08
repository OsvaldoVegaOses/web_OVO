import hashlib
from pathlib import Path

root = Path(r"c:\Users\osval\OneDrive - ONG Tren Ciudadano\digital skills\web_OVO")

initial_hashes = {
    "index.html": "dead87da88fab4549e7697b9e7600c0f8fa64b18d83af065db5f1dee6bfa01be",
    "proyectos/pac-arenillas-negras.html": "4b2827b5803d33321d198abd2ccd83b02a3fa9bffec6d9f1e364c20b3adb4181",
    "proyectos/medio-humano-desaladora-arica.html": "2a369115a607815965658fb97aaa49e8cb181451a18502828222abba3b4d30de",
    "proyectos/deslindes-rios-valparaiso.html": "8b83c5a14c2d8873e437abb8a87a5eaab16968026bf3b245819449df23069c4e",
    "proyectos/pac-la-florida.html": "e0472912bc251feaab5caa87eca4ecef8bb330b30f8852d5bfcc833f57062e87",
    "proyectos/plan-maestro-san-felipe.html": "7bcdcacde85c60d308c205821cdf731559b73fecd21f7972f2f0f71b825aeda4",
    "proyectos/medio-humano-horcon.html": "1c570e383b2775ae5f2aa94bd41891fccaa639203bd347f5d051eed811d1fd78",
    "style.css": "4534acf4bb30b9e7da5b375177c8191f38b3022179f278719a80f226a22ff387",
    "script.js": "ad095b921eb2f10d4feec8a92c79d80d0c2b741e500a09189ef93b30ae1838b0",
}

print("=== VERIFICACION DE INTEGRIDAD SHA-256 DE ARCHIVOS V1 ===")
all_ok = True
for rel, expected_h in initial_hashes.items():
    p = root / rel
    current_h = hashlib.sha256(p.read_bytes()).hexdigest()
    match = current_h == expected_h
    status = "INTACTO (PASS)" if match else "MODIFICADO (FAIL!)"
    print(f"{rel}:")
    print(f"  Inicial: {expected_h}")
    print(f"  Actual:  {current_h}")
    print(f"  Estado:  {status}\n")
    if not match:
        all_ok = False

if all_ok:
    print("CONCLUSION: TODOS LOS 9 ARCHIVOS V1 ESTAN 100% INTACTOS (0 BYTES MODIFICADOS).")
else:
    raise SystemExit("ERROR: ALGUN ARCHIVO V1 FUE MODIFICADO!")
