import re

with open('index_2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update comments
content = content.replace(
    'INDEX_2.HTML — EDITORIAL LIGHT PORTFOLIO & TECH TRANSITION',
    'INDEX.HTML — PORTAFOLIO PROFESIONAL EDITORIAL CLARO & TRANSICIÓN TECNOLÓGICA'
)

# 2. Replace prototype class name with clean production class name
content = content.replace('.index-editorial-prototype', '.index-editorial')
content = content.replace('<body class="index-editorial-prototype">', '<body class="index-editorial">')

# 3. Clean any temporary experiment text in comments if present
content = re.sub(r'/\* =+ EXPERIMENTO:.*?=\*/', '', content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY_PROMOTED_TO_INDEX_HTML")
