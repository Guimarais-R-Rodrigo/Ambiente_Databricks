"""Contrato da extração de QA/autoria: recursos runtime nunca são dispensados."""
from __future__ import annotations
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


FINGERPRINT_SCHEMA = 'core-tests-ast-v2'
CORE_PATH = 'tools/tests/runtime/test_core.py'
TYPE_PARAM_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
VISUAL_SUCCESSOR = 'tools/tests/runtime/visual_successor.json'
SUCCESSOR_FIGURE = 'tools/readme_visuals/qa/figures/raiz.02_arquitetura_ecossistema.json'


def check_visual_successor(root: Path, item: dict, source_commit: str, data: bytes) -> None:
    """Sucessão de três campos de uma figura, com predecessor Git e assets atuais.

    data já desfez somente o prefixo da fonte. O ledger não altera os hashes
    históricos nem dispensa integridade das demais figuras ou campos.
    """
    ledger = json.loads((root / VISUAL_SUCCESSOR).read_text(encoding='utf-8'),
                        object_pairs_hook=_unique_object)
    if (ledger['schema_version'] != 1 or ledger['source_commit'] != source_commit
            or ledger['source'] != item['source'] or ledger['destination'] != item['destination']
            or ledger['original_sha256'] != item['source_sha256']
            or ledger['label'] != 'ambiente_databricks/' or ledger['font_size'] != 32):
        raise ValueError('VISUAL_SUCCESSOR_PROVENANCE')
    # O checkout da ferramenta é owner da história Git; root também pode ser
    # uma cópia isolada de dados usada nos testes negativos.
    original = subprocess.run(['git', 'cat-file', 'blob', source_commit + ':' + item['source']],
                              cwd=ROOT, capture_output=True, check=False)
    if original.returncode or hashlib.sha256(original.stdout).hexdigest() != item['source_sha256']:
        raise ValueError('VISUAL_SUCCESSOR_PREDECESSOR')
    before = json.loads(original.stdout)
    current = json.loads(data)
    live = json.loads((root / item['destination']).read_text(encoding='utf-8'))
    if live['texts'][1]['text'] != ledger['label'] or live['texts'][1]['size'] != ledger['font_size']:
        raise ValueError('VISUAL_SUCCESSOR_LABEL')
    allowed = [['sha256'], ['svg_sha256'], ['texts', 1, 'width']]
    if [change['path'] for change in ledger['approved_changes']] != allowed:
        raise ValueError('VISUAL_SUCCESSOR_FIELDS')
    expected_bytes = original.stdout
    for change in ledger['approved_changes']:
        left, right = before, current
        for part in change['path'][:-1]:
            left, right = left[part], right[part]
        key = change['path'][-1]
        if left[key] != change['old'] or right[key] != change['new']:
            raise ValueError('VISUAL_SUCCESSOR_VALUE')
        old = json.dumps(change['old']).encode()
        new = json.dumps(change['new']).encode()
        if expected_bytes.count(old) != 1:
            raise ValueError('VISUAL_SUCCESSOR_AMBIGUOUS_REPLACEMENT')
        expected_bytes = expected_bytes.replace(old, new)
    if data != expected_bytes:
        raise ValueError('VISUAL_SUCCESSOR_UNAPPROVED_BYTES')
    product_assets = root / 'ambiente_databricks/.assistant/hub_readmes_visual_assets'
    for field, path_field in [('sha256', 'published'), ('svg_sha256', 'source')]:
        relative = current[path_field]
        if not isinstance(relative, str) or Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise ValueError('VISUAL_SUCCESSOR_ASSET_PATH')
        asset = product_assets / relative
        if asset.is_symlink() or hashlib.sha256(asset.read_bytes()).hexdigest() != current[field]:
            raise ValueError('VISUAL_SUCCESSOR_ASSET_MISMATCH')


def canonical_ast(value):
    """AST tipada; apenas posições e type_params vazio de definições são neutros.

    Python 3.12 acrescentou type_params. Ausência (3.11) e lista vazia (3.12)
    representam a mesma definição não genérica. Parâmetros reais e quaisquer
    outros campos permanecem no digest; metadados não previstos são recusados.
    """
    if isinstance(value, ast.AST):
        allowed = set(value._fields) | set(value._attributes)
        if set(vars(value)) - allowed or len(set(value._fields)) != len(value._fields):
            raise ValueError('UNEXPECTED_AST_METADATA')
        fields = []
        for field in sorted(value._fields):
            if not hasattr(value, field):
                raise ValueError('MISSING_AST_FIELD:' + field)
            item = getattr(value, field)
            if isinstance(value, TYPE_PARAM_NODES) and field == 'type_params' and item == []:
                continue
            fields.append([field, canonical_ast(item)])
        return ['ast', type(value).__name__, fields]
    if isinstance(value, list):
        return ['list', [canonical_ast(item) for item in value]]
    if value is None or value is Ellipsis or type(value) in (str, bytes, bool, int, float, complex):
        # Tipo explícito impede colisões como True == 1 == 1.0.
        return ['scalar', type(value).__name__, repr(value)]
    raise ValueError('UNEXPECTED_AST_VALUE:' + type(value).__name__)


def core_cases(path: Path) -> dict:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    cases = {}
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        if cls.name in cases:
            raise ValueError('DUPLICATE_CORE_CLASS:' + cls.name)
        methods = {}
        for method in cls.body:
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name.startswith('test_'):
                if method.name in methods:
                    raise ValueError('DUPLICATE_CORE_CASE:' + cls.name + '.' + method.name)
                methods[method.name] = canonical_ast(method)
        cases[cls.name] = methods
    if not any(cases.values()):
        raise ValueError('EMPTY_CORE_CASES')
    return cases


def core_signature(path: Path) -> str:
    return hashlib.sha256(json.dumps(core_cases(path), sort_keys=True,
                                     ensure_ascii=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_CONTRACT_KEY:' + key)
        result[key] = value
    return result


def validate_fingerprint(contract: dict, manifest: dict) -> dict:
    """Falha fechada: schema/proveniência conhecidos, sem fallback ao hash legado."""
    if set(contract) != {'source_commit', 'protected', 'core_case_count',
                         'core_assertion_ast_sha256', 'core_assertion_fingerprint'}:
        raise ValueError('PACKAGE_CONTRACT_FIELDS')
    fingerprint = contract['core_assertion_fingerprint']
    if not isinstance(fingerprint, dict) or set(fingerprint) != {'schema', 'sha256', 'provenance'}:
        raise ValueError('FINGERPRINT_FIELDS')
    if fingerprint['schema'] != FINGERPRINT_SCHEMA:
        raise ValueError('FINGERPRINT_SCHEMA')
    if not isinstance(fingerprint['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', fingerprint['sha256']):
        raise ValueError('FINGERPRINT_DIGEST')
    if type(contract['core_case_count']) is not int or contract['core_case_count'] <= 0:
        raise ValueError('CORE_CASE_COUNT')
    source = [item for item in manifest['files'] if item['destination'] == CORE_PATH]
    if len(source) != 1 or manifest['source_commit'] != contract['source_commit']:
        raise ValueError('FINGERPRINT_SOURCE')
    expected = {'source_commit': contract['source_commit'], 'source_path': source[0]['source'],
                'source_sha256': source[0]['source_sha256'],
                'legacy_ast_sha256': contract['core_assertion_ast_sha256'],
                'legacy_python': '3.12'}
    if fingerprint['provenance'] != expected:
        raise ValueError('FINGERPRINT_PROVENANCE')
    return fingerprint


def check(root: Path = ROOT) -> list[str]:
    try:
        contract = json.loads((root / 'tools/tests/runtime/package_contract.json').read_text(encoding='utf-8'),
                              object_pairs_hook=_unique_object)
        manifest = json.loads((root / 'tools/tests/runtime/relocation_manifest.json').read_text(encoding='utf-8'),
                              object_pairs_hook=_unique_object)
        fingerprint = validate_fingerprint(contract, manifest)
        moves = manifest['files']
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return ['PACKAGE_CONTRACT_INVALID:' + str(exc)]
    errors = []
    for relative, digest in contract['protected'].items():
        path = root / 'ambiente_databricks/.assistant' / relative
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f'PROTECTED_RESOURCE:{relative}')
    for item in moves:
        # source_commit/source/source_sha256 identificam a árvore congelada.
        # Somente a presença atual acompanha a renomeação autorizada da fonte.
        live_source = item['source']
        if live_source.startswith('ambiente_fonte/'):
            live_source = 'ambiente_databricks/' + live_source[len('ambiente_fonte/'):]
        if (root / live_source).exists():
            errors.append(f'MAINTAINER_FILE_IN_PAYLOAD:{live_source}')
        destination = root / item['destination']
        if not destination.is_file():
            errors.append(f'MOVED_RESOURCE_MISSING:{item["destination"]}')
        elif destination.is_symlink() or any(p.is_symlink() for p in destination.parents if p != root):
            errors.append(f'MOVED_RESOURCE_SYMLINK:{item["destination"]}')
        elif item['destination'] not in ('tools/tests/runtime/test_core.py', 'tools/readme_visuals/qa/validation.json'):
            data = destination.read_bytes()
            # Metadados QA apontam à fonte renomeada. Preserve o digest original
            # e aceite só esse delta textual reversível nas figuras realocadas;
            # qualquer outra alteração continua reprovando.
            if item['destination'].startswith('tools/readme_visuals/qa/figures/') and destination.suffix == '.json':
                data = data.replace(b'ambiente_databricks/', b'ambiente_fonte/')
            if hashlib.sha256(data).hexdigest() != item['source_sha256']:
                if item['destination'] == SUCCESSOR_FIGURE:
                    try:
                        check_visual_successor(root, item, manifest['source_commit'], data)
                    except (OSError, ValueError, KeyError, TypeError) as exc:
                        errors.append('VISUAL_SUCCESSOR_INVALID:' + str(exc))
                else:
                    errors.append(f'MOVED_RESOURCE_CHANGED:{item["destination"]}')
        elif item['destination'] == 'tools/readme_visuals/qa/validation.json':
            report = json.loads(destination.read_text(encoding='utf-8'))
            if report.get('status') != 'passed' or report.get('scope') != 'all' or report.get('failures'):
                errors.append('CURRENT_VISUAL_QA_NOT_PASS')
    path = root / CORE_PATH
    if path.is_file():
        try:
            cases = core_cases(path)
            if sum(map(len, cases.values())) != contract['core_case_count']:
                errors.append('CORE_CASE_COUNT_CHANGED')
            if core_signature(path) != fingerprint['sha256']:
                errors.append('CORE_CASES_OR_ASSERTIONS_CHANGED')
        except (OSError, ValueError, SyntaxError) as exc:
            errors.append('CORE_AST_INVALID:' + str(exc))
    return errors


if __name__ == '__main__':
    result = check()
    print(json.dumps({'status': 'FAIL' if result else 'PASS', 'errors': result}, indent=2))
    raise SystemExit(bool(result))
