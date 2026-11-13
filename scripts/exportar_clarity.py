"""Exporta datos agregados de Clarity; solicita el token sin mostrarlo."""
import argparse
import getpass
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--dias', type=int, choices=(1, 2, 3), default=1)
parser.add_argument('--salida', type=Path, required=True)
args = parser.parse_args()
if args.salida.exists():
    sys.exit('La salida ya existe; elige otro archivo para no sobrescribirla.')
token = getpass.getpass('Token de Clarity: ').strip()
if not token:
    sys.exit('Token vacío; no se realizó ninguna llamada.')
query = urllib.parse.urlencode({'numOfDays': args.dias, 'dimension1': 'URL'})
request = urllib.request.Request(
    'https://www.clarity.ms/export-data/api/v1/project-live-insights?' + query,
    headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'},
)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
except urllib.error.HTTPError as exc:
    sys.exit(f'Clarity respondió HTTP {exc.code}; no se reintentó la llamada.')
except (urllib.error.URLError, TimeoutError, ValueError) as exc:
    sys.exit(f'No se pudo completar la exportación ({type(exc).__name__}); no se reintentó.')
args.salida.parent.mkdir(parents=True, exist_ok=True)
with args.salida.open('x', encoding='utf-8') as out:
    json.dump({'exportado_utc': datetime.now(timezone.utc).isoformat(),
               'dias': args.dias, 'dimension': 'URL', 'datos': data},
              out, ensure_ascii=False, indent=2)
print(f'Exportación guardada en {args.salida}')
