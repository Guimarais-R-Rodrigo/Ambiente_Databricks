"""Guarda estrutural V02; não publica nem importa dependências gráficas."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'ambiente_fonte/.assistant'))
from hub_snippets.visual.tema import tema
from api_publica import api_publica, conteudo_init
import temas_v01_contract as contract


def check_layout(root: Path = ROOT) -> dict:
    root = Path(root)
    product = root / 'ambiente_fonte/.assistant'
    pattern = product / 'hub_padroes/identidade_visual'
    obj = product / 'hub_snippets/visual/tema'
    required = [pattern/'theme.schema.json', pattern/'assets.json', pattern/'TOKENS.md',
                pattern/'README.md', pattern/'GUIA_OPERACIONAL.md', pattern/'ERROS.md',
                obj/'tema.py', obj/'__init__.py', obj/'README.md', obj/'exemplo_tema.py',
                root/'tools/tests/test_temas_v02.py']
    if any(not p.is_file() for p in required):
        raise ValueError('V02_INCOMPLETE: núcleo, documentação ou testes ausentes.')
    if (root/'docs/sprints/sistema_temas/V01/theme.schema.json').exists():
        raise ValueError('V02_DUPLICATE_SCHEMA: fonte anterior ainda ativa.')
    if hashlib.sha256((pattern/'theme.schema.json').read_bytes()).hexdigest() != tema._SCHEMA_SHA:
        raise ValueError('V02_SCHEMA_HASH: contrato 0.1.0 alterado sem revisão.')
    schema=tema._read_json(pattern/'theme.schema.json')
    if (pattern/'TOKENS.md').read_text(encoding='utf-8') != contract.dictionary(schema):
        raise ValueError('V02_DICTIONARY: referência diverge do schema.')
    fixtures=root/'docs/sprints/sistema_temas/V01/fixtures'
    names={'legado_notebook.json','legado_editorial.json','executivo_claro_exemplo.json','apresentacao_exemplo.json'}
    if {p.name for p in (pattern/'exemplos').glob('*.json')} != names:
        raise ValueError('V02_FIXTURES: referências ausentes ou adicionais.')
    for name in names:
        if (fixtures/name).read_bytes() != (pattern/'exemplos'/name).read_bytes():
            raise ValueError('V02_FIXTURE_DRIFT: cópia de referência editada independentemente.')
    registry=tema._read_json(root/'docs/sprints/sistema_temas/V01/referencias_assets.json')
    for entries in registry['sets'].values():
        for entry in entries:
            entry['path']=entry['path'].removeprefix('ambiente_fonte/.assistant/')
    if tema._read_json(pattern/'assets.json') != registry:
        raise ValueError('V02_ASSETS: manifesto não corresponde à fonte declarada.')
    if (obj/'__init__.py').read_text(encoding='utf-8') != conteudo_init('tema',api_publica(obj/'tema.py')):
        raise ValueError('V02_API: fachada não é exaustiva.')
    if contract.validate_theme is not tema._validate_theme:
        raise ValueError('V02_VALIDATOR: validação V01 não usa o núcleo comum.')
    manual=(product/'MANUAL_TECNICO.md').read_bytes()
    if manual != (root/'MANUAL_TECNICO.md').read_bytes():
        raise ValueError('V02_MANUAL: cópia raiz divergente.')
    if b'hub_snippets.visual.tema' not in manual:
        raise ValueError('V02_MANUAL: objeto não consta no catálogo canônico.')
    import ast
    tree=ast.parse((root/'tools/tests/test_temas_v02.py').read_text(encoding='utf-8'))
    tests=[node.name for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name.startswith('test_')]
    if not tests or 'test_import_without_third_party_modules_or_platform' not in tests or 'test_programmatic_cycle' not in tests:
        raise ValueError('V02_EMPTY_TESTS: testes críticos ausentes.')
    return {'status':'PASS_V02_LAYOUT','declared_test_methods':len(tests),
            'schema_sha256':tema._SCHEMA_SHA,'fixtures':len(names),
            'runtime_databricks':'NAO_HOMOLOGADO','publishing':'NAO_EXECUTADO'}


def main() -> int:
    try:
        print(json.dumps(check_layout(),ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError) as exc:
        print('FAIL:',str(exc));return 1

if __name__=='__main__':raise SystemExit(main())
