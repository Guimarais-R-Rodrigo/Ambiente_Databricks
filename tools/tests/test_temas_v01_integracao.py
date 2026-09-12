"""Regressões da composição V01 com a main V00/READMEs/Concierge.

São guardas de manutenção, não operação de widgets nem autorização de publicação.
Cada mutante exige o código específico que justifica a recusa.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/tests'))
import ci_local
import temas_v01_contract as contract
from test_readme_integracao import REQUIRED, duplicate_adrs, stage_errors
import test_temas_v01 as original_tests


class V01IntegrationTests(unittest.TestCase):
    def reject(self, code, callback, *args):
        with self.assertRaises(contract.ContractError) as caught:
            callback(*args)
        self.assertEqual(caught.exception.code, code)

    def registry(self):
        return contract.read_json(contract.PACKAGE / 'referencias_assets.json')

    def test_existing_gates_preserved(self):
        self.assertEqual(stage_errors(ci_local.ETAPAS), [])

    def test_each_missing_original_gate_is_detected(self):
        for name in REQUIRED:
            with self.subTest(stage=name):
                mutant = [stage for stage in ci_local.ETAPAS if stage[0] != name]
                self.assertIn(f'etapa ausente: {name}', stage_errors(mutant))

    def test_no_duplicate_adr_numbers(self):
        self.assertEqual(duplicate_adrs([p.name for p in (ROOT/'docs/decisions').glob('ADR-*.md')]), set())

    def test_shared_markdown_parser_is_used(self):
        import markdown_contract
        self.assertIs(contract.markdown_links, markdown_contract.markdown_links)
        self.assertIs(contract.anchors, markdown_contract.anchors)

    def test_registry_matches_authoritative_manifests(self):
        self.assertEqual(contract.check_asset_registry(self.registry()), 12)

    def test_registry_missing_entry_is_rejected(self):
        registry = self.registry()
        registry['sets']['editorial-v2-congelado'].pop()
        self.reject('ASSET_REGISTRY', contract.check_asset_registry, registry)

    def test_registry_rewritten_hash_is_rejected(self):
        registry = self.registry()
        registry['sets']['editorial-v2-congelado'][0]['sha256'] = '0' * 64
        self.reject('ASSET_REGISTRY', contract.check_asset_registry, registry)

    def test_registry_duplicate_entry_is_rejected(self):
        registry = self.registry()
        entries = registry['sets']['editorial-v2-congelado']
        entries.append(copy.deepcopy(entries[0]))
        self.reject('ASSET_REGISTRY', contract.check_asset_registry, registry)

    def test_registry_additional_set_is_rejected(self):
        registry = self.registry()
        registry['sets']['novo-conjunto-nao-aprovado'] = []
        self.reject('ASSET_REGISTRY', contract.check_asset_registry, registry)

    def test_registry_nonempty_assetless_set_is_rejected(self):
        registry = self.registry()
        registry['sets']['sem-assets'] = [copy.deepcopy(registry['sets']['editorial-v2-congelado'][0])]
        self.reject('ASSET_REGISTRY', contract.check_asset_registry, registry)

    def test_registry_empty_frozen_set_is_rejected(self):
        registry = self.registry()
        registry['sets']['editorial-v2-congelado'] = []
        self.reject('ASSET_REGISTRY', contract.check_asset_registry, registry)

    def document_fixture(self, root, content):
        package = root / 'docs/sprints/sistema_temas/V01'
        package.mkdir(parents=True)
        (package/'README.md').write_text(content, encoding='utf-8')
        (package/'destino.md').write_text('# Destino\n\n## Ação segura\n', encoding='utf-8')
        adr = root/'docs/decisions/ADR-0013-sistema-de-temas.md'
        adr.parent.mkdir(parents=True)
        adr.write_text('# ADR candidato\n', encoding='utf-8')
        return package

    def test_document_existing_encoded_anchor_is_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '# Entrada\n[Ação](destino.md#a%C3%A7%C3%A3o-segura)\n')
            self.assertEqual(contract.check_links(package, root), 1)

    def test_document_inexistent_anchor_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '[Próximo](destino.md#nao-existe)\n')
            self.reject('DOC_ANCHOR', contract.check_links, package, root)

    def test_document_inexistent_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '[Próximo](ausente.md)\n')
            self.reject('DOC_LINK', contract.check_links, package, root)

    def test_document_code_example_is_not_a_navigation_link(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '```md\n[Exemplo](ausente.md)\n```\n')
            self.assertEqual(contract.check_links(package, root), 0)

    def test_document_unsafe_scheme_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '[Executar](javascript:alert)\n')
            self.reject('DOC_LINK', contract.check_links, package, root)

    def test_document_escaping_checkout_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '[Fora](../../../../../fora.md)\n')
            self.reject('DOC_LINK', contract.check_links, package, root)

    def test_document_self_anchor_is_validated(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = self.document_fixture(root, '# Entrada\n[Próximo](#inexistente)\n')
            self.reject('DOC_ANCHOR', contract.check_links, package, root)

    def test_dictionary_displays_each_effect(self):
        schema = contract.read_json(contract.PACKAGE/'theme.schema.json')
        text = contract.dictionary(schema)
        for group in ('notebookTokens', 'editorialTokens'):
            for spec in schema['$defs'][group]['properties'].values():
                self.assertIn('**Efeito previsto:** ' + spec['x-hub']['effect'], text)

    def test_matrix_method_references_are_real(self):
        matrix = contract.read_json(contract.PACKAGE/'matriz_testes.json')
        # A matriz usa nomes do teste como âncoras, sem executar um teste duas vezes.
        serialized = json.dumps(matrix)
        import re
        for method in re.findall(r'test_[A-Za-z0-9_]+', serialized):
            self.assertTrue(hasattr(original_tests.ContractTests, method), method)

    def test_maintenance_guide_uses_integrated_v00_tools(self):
        text = (contract.PACKAGE/'GUIA_MANTENEDOR.md').read_text(encoding='utf-8')
        for name in ('test_inventario_visual.py', 'test_visual_legado_v00.py', 'test_baseline_visual_runner.py'):
            self.assertIn(name, text)
            self.assertTrue((ROOT/'tools/tests'/name).is_file())
        self.assertNotIn('temas_inventory.py', text)
        self.assertNotIn('test_temas_v00.py', text)

    def test_single_sprint_entrypoint(self):
        self.assertFalse((ROOT/'docs/sprints/temas').exists())
        entry = (ROOT/'docs/sprints/sistema_temas/README.md').read_text(encoding='utf-8')
        self.assertIn('V01/README.md', entry)
        self.assertIn('V01/GUIA_PRIMEIRO_USO.md', entry)

    def test_candidate_not_claimed_as_installed(self):
        checkpoint = (contract.PACKAGE/'CHECKPOINT_V01.md').read_text(encoding='utf-8')
        self.assertIn('O seletor de temas não está instalado', checkpoint)
        self.assertIn('Auditoria independente: PENDENTE', checkpoint)
        self.assertIn('NÃO HOMOLOGADOS', checkpoint)

    def test_direct_validation_dependencies_declared(self):
        dependencies = (ROOT/'tools/requirements-temas-dev.txt').read_text(encoding='utf-8')
        self.assertIn('jsonschema==', dependencies)
        self.assertIn('referencing==', dependencies)


if __name__ == '__main__':
    unittest.main(verbosity=2)
