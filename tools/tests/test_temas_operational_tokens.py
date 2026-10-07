"""Operational token documentation, independently checked against actual consumers.

These local checks do not render a browser, publish a theme or certify a workspace.
The historical dictionary and its tests remain unchanged.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / 'ambiente_databricks/.assistant'
sys.path.insert(0, str(ROOT / 'tools'))
import temas_v01_contract as contract
from markdown_contract import markdown_links


class OperationalTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = contract.read_json(contract.SCHEMA_PATH)
        cls.path = PRODUCT / 'hub_padroes/identidade_visual/TOKENS.md'
        cls.text = cls.path.read_text(encoding='utf-8')

    def block(self, group, key):
        heading = 'Notebook' if group == 'notebookTokens' else 'README e apresentação'
        section = self.text.split('## ' + heading + '\n', 1)[1].split('\n## ', 1)[0]
        return section.split('### `' + key + '`\n', 1)[1].split('\n### ', 1)[0]

    def test_historical_output_and_schema_are_frozen(self):
        historical = (contract.PACKAGE / 'TOKENS.md').read_bytes()
        self.assertEqual(contract.dictionary(self.schema).encode('utf-8'), historical)
        # Independent baseline digest, captured before the operational projection.
        self.assertEqual(hashlib.sha256(historical).hexdigest(),
                         '95ca81ba4f75c1fcf91c8fb4e9d009cab7d16e478eab47a5c41445f2c098e14c')
        from hub_snippets.visual.tema import tema
        self.assertEqual(hashlib.sha256(contract.SCHEMA_PATH.read_bytes()).hexdigest(), tema._SCHEMA_SHA)

    def test_complete_80_tokens_with_schema_contract_preserved(self):
        self.assertEqual(len(self.schema['$defs']['notebookTokens']['properties']), 48)
        self.assertEqual(len(self.schema['$defs']['editorialTokens']['properties']), 32)
        expected = [key for group in ('notebookTokens', 'editorialTokens')
                    for key in self.schema['$defs'][group]['properties']]
        self.assertEqual(re.findall(r'^### `([^`]+)`$', self.text, re.M), expected)
        for group in ('notebookTokens', 'editorialTokens'):
            for key, spec in self.schema['$defs'][group]['properties'].items():
                with self.subTest(group=group, token=key):
                    block = self.block(group, key)
                    meta = spec['x-hub']
                    self.assertIn(spec['description'], block)
                    self.assertIn('**Efeito definido:** ' + meta['effect'], block)
                    self.assertIn('**Unidade:** ' + meta['unit'], block)
                    self.assertIn('**Tipo:** ' + spec['type'], block)
                    self.assertIn('**Default de referência:** `' + json.dumps(spec['default'], ensure_ascii=False) + '`', block)
                    self.assertIn('**Edição de proposta:** ' + ', '.join(meta['editable_by']), block)
                    self.assertIn('**Contextos:** ' + ', '.join(meta['contexts']), block)
                    limits = {k: v for k, v in spec.items() if k not in {'type', 'description', 'default', 'x-hub'}}
                    self.assertIn('**Limites:** `' + json.dumps(limits, ensure_ascii=False) + '`', block)

    @staticmethod
    def literal_token_reads(path):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        return {node.slice.value for node in ast.walk(tree)
                if isinstance(node, ast.Subscript)
                and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str)
                and ((isinstance(node.value, ast.Name) and node.value.id == 'tokens')
                     or (isinstance(node.value, ast.Attribute) and node.value.attr == 'tokens'))}

    def test_direct_consumers_match_implementation_not_schema_plans(self):
        actual = {}
        for path in (PRODUCT / 'hub_snippets').rglob('*.py'):
            if path.name.startswith('exemplo_'):
                continue
            reads = self.literal_token_reads(path)
            if reads:
                actual[path.parent.relative_to(PRODUCT / 'hub_snippets').as_posix()] = reads
        declared = {path: set(keys) for path, (_label, keys) in contract._OPERATIONAL_READERS.items()}
        self.assertEqual(actual, declared)
        consumed = set().union(*actual.values())
        self.assertEqual(set(self.schema['$defs']['notebookTokens']['properties']) - consumed,
                         {'brand.accent', 'semantic.positive', 'semantic.neutral'})
        for key in ('brand.accent', 'semantic.positive', 'semantic.neutral'):
            self.assertIn('Sem leitura visual direta', self.block('notebookTokens', key))
        self.assertIn('segunda cor de palette.curves_legacy', self.block('notebookTokens', 'brand.accent'))

    def test_gallery_availability_uses_actual_disabled_controls(self):
        path = PRODUCT / 'hub_snippets/visual/theme_lab/theme_lab.py'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == '_NO_PREVIEW' for t in node.targets))
        disabled = ast.literal_eval(assignment.value.args[0])
        self.assertEqual(len(disabled), 18)
        self.assertEqual(disabled, contract._OPERATIONAL_NO_PREVIEW)
        for key in self.schema['$defs']['notebookTokens']['properties']:
            block = self.block('notebookTokens', key)
            self.assertIn('controle desabilitado' if key in disabled else 'Controle habilitado', block)
        app = (PRODUCT / 'hub_padroes/identidade_visual/databricks_app/app.py').read_text(encoding='utf-8')
        self.assertIn('disabled = not spec.preview_supported', app)
        self.assertIn('if spec.preview_supported', app)

    def test_aibi_classification_is_matrix_scope_not_native_import(self):
        mapping = contract.read_json(PRODUCT / 'hub_padroes/identidade_visual/aibi/aibi_mapping.json')
        self.assertEqual(len(mapping['mappings']), 48)
        for item in mapping['mappings']:
            block = self.block('notebookTokens', item['hub_token'])
            self.assertIn('`' + item['classification'] + '`; binding `' + item['binding_strategy'] + '`', block)
            self.assertIn(item['note'], block)
        self.assertIn('Nenhuma classificação equivale a importação nativa pronta', self.text)
        self.assertIn('export real, binding revisado e autorização específica', self.text)

    def test_editorial_support_preserves_renderer_limits(self):
        renderer = (ROOT / 'tools/readme_visuals/theme_assets.mjs').read_text(encoding='utf-8')
        color_keys = set(re.findall(r"'([a-z_]+)'", re.search(r'const COLOR_KEYS=\[(.*?)\];', renderer).group(1)))
        self.assertEqual({'editorial.' + key for key in color_keys}, contract._OPERATIONAL_EDITORIAL_COLORS)
        self.assertIn("values['font.family']==='editorial_inter'", renderer)
        self.assertIn("'--context','readme'", renderer)
        self.assertIn('lib.tokens.presets[c.render_targets[0]]', renderer)
        for key in ('canvas.width_px', 'canvas.height_px'):
            self.assertIn('não redimensiona figuras', self.block('editorialTokens', key))
        self.assertIn('recusa system_arial', self.block('editorialTokens', 'font.family'))
        self.assertIn('não garante um renderer de apresentações', self.text)
        # These fields are assigned in the bridge but not read by its renderers.
        source = (ROOT / 'tools/readme_visuals/lib.mjs').read_text(encoding='utf-8') + ''.join(
            p.read_text(encoding='utf-8') for p in (ROOT / 'tools/readme_visuals/archetypes').glob('*.mjs'))
        for key in contract._OPERATIONAL_EDITORIAL_INERT:
            self.assertNotIn(key, source)
            self.assertIn('sem leitura nos renderers atuais', self.block('editorialTokens', key))
        parametric = (ROOT / 'tools/readme_visuals/lib.mjs').read_text(encoding='utf-8') + ''.join(
            p.read_text(encoding='utf-8') for p in (ROOT / 'tools/readme_visuals/archetypes').glob('*.mjs')
            if p.name != 'signatures.mjs')
        actual_colors = {'editorial.' + key for key in re.findall(r'\bC\.([a-z_]+)', parametric)}
        self.assertEqual(contract._OPERATIONAL_EDITORIAL_COLORS - actual_colors,
                         {'editorial.atlas_core', 'editorial.dossier_fold'})
        for key in ('editorial.atlas_core', 'editorial.dossier_fold'):
            self.assertIn('congeladas e copiadas sem recoloração', self.block('editorialTokens', key))

    def test_operational_caveats_and_audience(self):
        self.assertIn('tabela pandas mantém a família fixa Segoe UI', self.block('notebookTokens', 'font.family'))
        self.assertIn('quantidade ímpar', self.text)
        self.assertIn('SHAP/Matplotlib e Kaplan–Meier', self.text)
        self.assertIn('não autenticação nem concessão de permissão', self.text)
        self.assertNotRegex(self.text, r'\bV\d{2}\b|PLANEJADO_V|tools/|docs/sprints/|ambiente_databricks/|\*\*Entrega:')
        self.assertNotIn('Nenhum controle abaixo está instalado', self.text)

    def test_operational_projection_is_reproducible_and_nonmutating(self):
        before = copy.deepcopy(self.schema)
        self.assertEqual(contract.operational_dictionary(self.schema), self.text)
        self.assertEqual(contract.operational_dictionary(self.schema), self.text)
        self.assertEqual(self.schema, before)
        for group in ('notebookTokens', 'editorialTokens'):
            changed = copy.deepcopy(self.schema)
            changed['$defs'][group]['properties']['undocumented.token'] = {}
            with self.assertRaisesRegex(ValueError, 'TOKEN_SUPPORT_COVERAGE'):
                contract.operational_dictionary(changed)

    def test_cli_has_distinct_stdout_modes_without_implicit_write(self):
        command = [sys.executable, '-B', str(ROOT / 'tools/temas_v01_contract.py')]
        paths = [self.path, contract.SCHEMA_PATH, contract.PACKAGE / 'TOKENS.md']
        before = {path: path.read_bytes() for path in paths}
        for flag, expected in [('--print-operational-dictionary', self.text.encode('utf-8')),
                               ('--print-dictionary', (contract.PACKAGE / 'TOKENS.md').read_bytes())]:
            result = subprocess.run(command + [flag], capture_output=True, cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, expected)
        conflict = subprocess.run(command + ['--print-dictionary', '--print-operational-dictionary'],
                                  capture_output=True, cwd=ROOT)
        self.assertEqual(conflict.returncode, 2)
        self.assertEqual(before, {path: path.read_bytes() for path in paths})

    def test_active_gate_rejects_drift_and_historical_projection(self):
        from temas_v02_check import check_layout
        self.assertEqual(check_layout()['status'], 'PASS_V02_LAYOUT')
        original = Path.read_text
        for mutant in (self.text.replace('brand.primary', 'brand.mutated', 1),
                       contract.dictionary(self.schema)):
            def read(path, *args, **kwargs):
                return mutant if path == self.path else original(path, *args, **kwargs)
            with self.subTest(mutant=mutant[:70]), patch.object(Path, 'read_text', read):
                with self.assertRaisesRegex(ValueError, 'V02_DICTIONARY'):
                    check_layout()

    def test_all_links_remain_inside_delivered_package(self):
        links = list(markdown_links(self.text))
        targets = {link[1] for link in links}
        self.assertTrue({'theme.schema.json', 'GUIA_OPERACIONAL.md', 'aibi/aibi_mapping.json',
                         'databricks_app/README.md', 'aibi/GUIA_PRIMEIRO_USO.md'} <= targets)
        for link in links:
            href = link[1]
            target = urlsplit(href)
            self.assertFalse(target.scheme, href)
            path = (self.path.parent / unquote(target.path)).resolve()
            self.assertTrue(path.is_relative_to(PRODUCT.resolve()), href)
            self.assertTrue(path.is_file(), href)


if __name__ == '__main__':
    unittest.main()
