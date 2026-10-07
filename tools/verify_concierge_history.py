"""Confere recuperação do protótipo retirado usando blobs Git e manifesto congelado.

Não restaura arquivos, executa código histórico nem consulta rede. Histórico raso
ou blob ausente bloqueia a prova; hashes e tamanhos divergentes reprovam.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'docs/historico/concierge-manifest.json'


def verify_manifest(root: Path, manifest: dict) -> int:
    """Verifica exatamente as identidades declaradas, sem depender da pasta retirada."""
    source = manifest['source_commit']
    if not re.fullmatch(r'[0-9a-f]{40}', source):
        raise ValueError('SOURCE_COMMIT_INVALID')
    entries = manifest['entries']
    if not entries or len(entries) != manifest['files_count']:
        raise ValueError('MANIFEST_COUNT_INVALID')
    paths = [entry['path'] for entry in entries]
    if len(set(paths)) != len(paths):
        raise ValueError('MANIFEST_DUPLICATE_PATH')
    for entry in entries:
        path = entry['path']
        parts = PurePosixPath(path).parts
        if not path.startswith('novas_funcionalidades/') or '..' in parts or '\\' in path:
            raise ValueError('MANIFEST_PATH_INVALID')
        recovered = subprocess.run(
            ['git', 'cat-file', 'blob', f'{source}:{path}'], cwd=root,
            capture_output=True, check=False,
        )
        if recovered.returncode:
            raise ValueError(f'HISTORY_BLOB_UNAVAILABLE: {source}:{path}; requer histórico Git completo')
        data = recovered.stdout
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError(f'HISTORY_BLOB_MISMATCH: {path}')
    return len(entries)


def main() -> int:
    try:
        manifest = json.loads((ROOT / MANIFEST).read_text(encoding='utf-8'))
        count = verify_manifest(ROOT, manifest)
    except (ValueError, KeyError, OSError) as exc:
        print(f'FAIL: {exc}')
        return 1
    print(f'PASS: {count} blobs recuperáveis; SHA-256 e tamanhos conferidos; nenhum arquivo restaurado')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
