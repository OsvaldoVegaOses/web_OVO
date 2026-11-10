import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'docs/recorridos-contacto-v1.1-manifiesto.json').read_text(encoding='utf-8'))
checks = [('https://osvaldovega.cl/' + entry['path'], entry['sha256']) for entry in manifest['archivos']]
index_sha = next(e['sha256'] for e in manifest['archivos'] if e['path'] == 'index.html')
checks += [('https://osvaldovega.cl/', index_sha), ('https://www.osvaldovega.cl/', index_sha)]
def verify(item):
    url, expected = item
    with urlopen(Request(url, headers={'Accept-Encoding': 'identity', 'Cache-Control': 'no-cache'}), timeout=30) as response:
        data = response.read()
        digest = hashlib.sha256(data).hexdigest()
        result = {'url': url, 'http': response.status, 'sha256': digest, 'matches': digest == expected}
        if '.html' in url or url.endswith('/'):
            result['tracking_once'] = data.count(b'contact-tracking.js') == 1 and data.count(b'openai-conversions.js') == 1
        return result
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(verify, checks))
evidence = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'checks': results,
            'pass': all(r['matches'] and r.get('tracking_once', True) for r in results)}
(root / 'docs/contacto-v11-verificacion-publica.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
print('Verificación pública:', 'PASS' if evidence['pass'] else 'FAIL', len(results), 'URLs')
raise SystemExit(0 if evidence['pass'] else 1)
