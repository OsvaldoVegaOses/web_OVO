"""Publicación controlada de archivos estáticos, con auditoría y respaldo."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
import uuid

def sha(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None

def atomic(path, data):
    metadata = path.stat() if path.exists() else None
    mode = metadata.st_mode & 0o777 if metadata else 0o644
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        name = stream.name
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(name, mode)
    if metadata and hasattr(os, 'chown'):
        os.chown(name, metadata.st_uid, metadata.st_gid)
    os.replace(name, path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('package', type=Path)
    parser.add_argument('--root', type=Path, default=Path('/var/www/html'))
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    package = json.loads(args.package.read_text(encoding='utf-8'))
    root = args.root.resolve(strict=True)
    if args.root.is_symlink():
        raise RuntimeError('Raíz inesperada')
    allowed = {'index.html', 'index2.html', 'style.css', 'openai-conversions.js', 'contact-tracking.js'}
    cases = ['pac-arenillas-negras', 'pac-la-florida', 'deslindes-rios-valparaiso', 'medio-humano-desaladora-arica', 'medio-humano-horcon', 'plan-maestro-san-felipe']
    allowed.update('proyectos/' + case + variant + '.html' for case in cases for variant in ['', '-v2'])
    if {entry['path'] for entry in package['files']} != allowed or len(package['files']) != len(allowed):
        raise RuntimeError('Lista de archivos inesperada')
    changes = []
    for entry in package['files']:
        target = root / entry['path']
        if target.is_symlink() or not target.resolve().is_relative_to(root):
            raise RuntimeError('Ruta inválida')
        before = target.read_bytes() if target.exists() else None
        after = base64.b64decode(entry['contents'], validate=True)
        if sha(before) != entry['before_sha256'] or sha(after) != entry['after_sha256']:
            raise RuntimeError('Estado cambió: ' + entry['path'])
        changes.append((entry['path'], target, before, after))
    if not args.apply:
        print(json.dumps({'status': 'audit_pass', 'files': len(changes)}))
        return
    backup_root = Path('/var/backups/ovo-contacto-v11')
    backup_root.mkdir(parents=True, exist_ok=True)
    lock = backup_root / '.lock'
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    operation = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8]
    backup = backup_root / operation
    written = []
    evidence = {'operation': operation, 'backup': str(backup), 'status': 'prepared',
                'files': [{k: v for k, v in e.items() if k != 'contents'} for e in package['files']]}
    try:
        backup.mkdir(mode=0o700)
        for name, target, before, after in changes:
            if before is not None:
                saved = backup / name
                saved.parent.mkdir(parents=True, exist_ok=True)
                saved.write_bytes(before)
        (backup / 'manifest.json').write_text(json.dumps(evidence, indent=2))
        try:
            for change in sorted(changes, key=lambda x: x[0].endswith('.html')):
                name, target, before, after = change
                if (target.read_bytes() if target.exists() else None) != before:
                    raise RuntimeError('Cambio concurrente: ' + name)
                atomic(target, after)
                written.append(change)
            for name, target, before, after in changes:
                if target.read_bytes() != after:
                    raise RuntimeError('Lectura posterior falló: ' + name)
            evidence['status'] = 'published'
        except BaseException:
            evidence['status'] = 'rolled_back'
            for name, target, before, after in reversed(written):
                if target.read_bytes() != after:
                    evidence['status'] = 'rollback_incomplete'
                elif before is None:
                    target.unlink()
                else:
                    atomic(target, before)
            raise
        finally:
            (backup / 'manifest.json').write_text(json.dumps(evidence, indent=2))
    finally:
        lock.unlink()
    print(json.dumps(evidence, indent=2))

if __name__ == '__main__':
    main()
