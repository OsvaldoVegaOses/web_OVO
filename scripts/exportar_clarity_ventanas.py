"""Consulta Clarity para 24, 48 y 72 horas con un solo ingreso de token."""
import getpass
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

paths = {days: Path(f'clarity-{days * 24}h.json') for days in (1, 2, 3)}
existing = [str(path) for path in paths.values() if path.exists()]
if existing:
    sys.exit('Ya existen archivos de salida: ' + ', '.join(existing))
token = getpass.getpass('Token de Clarity: ').strip()
if not token:
    sys.exit('Token vacío; no se realizó ninguna llamada.')
for days, path in paths.items():
    query = urllib.parse.urlencode({'numOfDays': days, 'dimension1': 'URL'})
    request = urllib.request.Request(
        'https://www.clarity.ms/export-data/api/v1/project-live-insights?' + query,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        sys.exit(f'Consulta de {days * 24} horas: HTTP {exc.code}. Detenido sin reintentos.')
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        sys.exit(f'Consulta de {days * 24} horas falló ({type(exc).__name__}). Detenido sin reintentos.')
    with path.open('x', encoding='utf-8') as output:
        json.dump({'exportado_utc': datetime.now(timezone.utc).isoformat(),
                   'dias': days, 'dimension': 'URL', 'datos': data},
                  output, ensure_ascii=False, indent=2)
    print(f'Guardado: {path}', flush=True)
