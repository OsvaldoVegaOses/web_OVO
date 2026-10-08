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

GTM_ID = "GTM-NN64BQC5"
CLARITY_ID = "ypzia0e866"

gtm_head = f'''
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{GTM_ID}');</script>
    <!-- End Google Tag Manager -->
'''

clarity = f'''
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{CLARITY_ID}");
    </script>
    <!-- End Microsoft Clarity -->
'''

gtm_body = f'''
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
'''

for path in pages:

    if not path.exists():
        raise SystemExit(f"ERROR: no existe {path}")

    text = path.read_text(encoding="utf-8")

    # -----------------------------------------------------
    # LIMPIEZA PREVIA: hace el script idempotente
    # -----------------------------------------------------

    text = re.sub(
        r'\s*<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\s*',
        '\n',
        text,
        flags=re.I | re.S
    )

    text = re.sub(
        r'\s*<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->\s*',
        '\n',
        text,
        flags=re.I | re.S
    )

    text = re.sub(
        r'\s*<!-- Microsoft Clarity -->.*?<!-- End Microsoft Clarity -->\s*',
        '\n',
        text,
        flags=re.I | re.S
    )

    # -----------------------------------------------------
    # GTM + CLARITY EN HEAD
    #
    # Conservamos meta charset al principio.
    # Insertamos inmediatamente después de charset.
    # -----------------------------------------------------

    charset_match = re.search(
        r'(<meta\s+charset=["\']?UTF-8["\']?\s*/?>)',
        text,
        flags=re.I
    )

    if not charset_match:
        raise SystemExit(f"ERROR: falta meta charset UTF-8 en {path}")

    insertion = (
        charset_match.group(1)
        + "\n"
        + gtm_head
        + clarity
    )

    text = (
        text[:charset_match.start()]
        + insertion
        + text[charset_match.end():]
    )

    # -----------------------------------------------------
    # GTM NOSCRIPT: inmediatamente después de <body>
    # -----------------------------------------------------

    body_match = re.search(
        r'<body\b[^>]*>',
        text,
        flags=re.I
    )

    if not body_match:
        raise SystemExit(f"ERROR: falta <body> en {path}")

    insertion_body = (
        body_match.group(0)
        + "\n"
        + gtm_body
    )

    text = (
        text[:body_match.start()]
        + insertion_body
        + text[body_match.end():]
    )

    path.write_text(text, encoding="utf-8")

    print("OK:", path.relative_to(root))

print()
print("Clarity:", CLARITY_ID)
print("GTM:", GTM_ID)
print()
print("CLARITY + GTM IMPLEMENTADOS.")
