import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

case_links = [
    'proyectos/pac-arenillas-negras.html',
    'proyectos/medio-humano-desaladora-arica.html',
    'proyectos/deslindes-rios-valparaiso.html',
    'proyectos/pac-la-florida.html',
    'proyectos/plan-maestro-san-felipe.html',
    'proyectos/medio-humano-horcon.html'
]

checks = {
    'Backup file exists': os.path.exists('index_dark_backup_2026-09-24.html'),
    'index.html body class index-editorial': '<body class="index-editorial">' in html,
    'Mailto link present': 'mailto:osvaldovegaoses@gmail.com' in html,
    'LinkedIn link present': 'https://www.linkedin.com/in/osvaldovegaoses' in html,
    'Mobile nav toggle present': 'id="nav-toggle"' in html,
}

for link in case_links:
    checks[f'Case link {link}'] = link in html

all_ok = True
for check, ok in checks.items():
    status = "OK" if ok else "FAILED"
    if not ok:
        all_ok = False
    print(f"{check}: {status}")

print("\nPROMOTED_INDEX_VERIFICATION:", "PASS" if all_ok else "FAIL")
