"""Contrato da extração de QA/autoria: recursos runtime nunca são dispensados."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def core_signature(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    cases = {c.name: {f.name: ast.dump(f, include_attributes=False) for f in c.body
                     if isinstance(f, ast.FunctionDef) and f.name.startswith('test_')}
             for c in tree.body if isinstance(c, ast.ClassDef)}
    return hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest()


def check(root: Path = ROOT) -> list[str]:
    contract = json.loads((root / 'tools/tests/runtime/package_contract.json').read_text())
    moves = json.loads((root / 'tools/tests/runtime/relocation_manifest.json').read_text())['files']
    errors = []
    for relative, digest in contract['protected'].items():
        path = root / 'ambiente_fonte/.assistant' / relative
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f'PROTECTED_RESOURCE:{relative}')
    for item in moves:
        if (root / item['source']).exists():
            errors.append(f'MAINTAINER_FILE_IN_PAYLOAD:{item["source"]}')
        destination = root / item['destination']
        if not destination.is_file():
            errors.append(f'MOVED_RESOURCE_MISSING:{item["destination"]}')
        elif destination.is_symlink() or any(p.is_symlink() for p in destination.parents if p != root):
            errors.append(f'MOVED_RESOURCE_SYMLINK:{item["destination"]}')
        elif item['destination'] not in ('tools/tests/runtime/test_core.py', 'tools/readme_visuals/qa/validation.json'):
            if hashlib.sha256(destination.read_bytes()).hexdigest() != item['source_sha256']:
                errors.append(f'MOVED_RESOURCE_CHANGED:{item["destination"]}')
        elif item['destination'] == 'tools/readme_visuals/qa/validation.json':
            report = json.loads(destination.read_text(encoding='utf-8'))
            if report.get('status') != 'passed' or report.get('scope') != 'all' or report.get('failures'):
                errors.append('CURRENT_VISUAL_QA_NOT_PASS')
    path = root / 'tools/tests/runtime/test_core.py'
    if path.is_file() and core_signature(path) != contract['core_assertion_ast_sha256']:
        errors.append('CORE_CASES_OR_ASSERTIONS_CHANGED')
    return errors


if __name__ == '__main__':
    result = check()
    print(json.dumps({'status': 'FAIL' if result else 'PASS', 'errors': result}, indent=2))
    raise SystemExit(bool(result))
