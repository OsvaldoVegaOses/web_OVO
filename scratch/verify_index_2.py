import re

with open('index_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = {
    'index-editorial-prototype class on body': '<body class="index-editorial-prototype">' in html,
    '#F4F6F8 main background': '#F4F6F8' in html,
    '#07111F primary text': '#07111F' in html,
    'Georgia serif font': 'Georgia' in html,
    'Header sticky blur': 'backdrop-filter: blur' in html,
    'Hero eyebrow present': 'OSVALDO VEGA OSES · SOCIÓLOGO' in html,
    'Arenillas updated summary': 'Metodologías diferenciadas con comunidades' in html,
    'Desaladora updated summary': 'Desarrollo y actualización de una Línea de Base' in html,
    'Deslindes updated summary': 'Participación Ciudadana desarrollada en cuatro cauces' in html,
    'Dark transition at #innovacion': '#innovacion' in html and 'background-color: #07111F' in html,
    'Dark footer': 'footer#contacto' in html and 'background-color: #050B14' in html,
    'No check icons in tags override': 'display: none !important' in html,
    'Proceso 2x2 breakpoint': 'repeat(2, 1fr)' in html,
}

all_ok = True
for check, ok in checks.items():
    status = "OK" if ok else "FAILED"
    if not ok:
        all_ok = False
    print(f"{check}: {status}")

print("\nOVERALL_VERIFICATION:", "PASS" if all_ok else "FAIL")
