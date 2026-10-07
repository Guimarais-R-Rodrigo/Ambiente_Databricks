"""Prova da fronteira de distribuição, incluindo mutantes discriminantes."""
from __future__ import annotations
import ast
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import package_boundary as boundary


class PackageBoundaryTests(unittest.TestCase):
    def test_live_boundary_and_assertions_preserved(self):
        self.assertEqual([], boundary.check(ROOT))
        contract = json.loads((ROOT / 'tools/tests/runtime/package_contract.json').read_text())
        self.assertEqual(45, contract['core_case_count'])

    def fixture(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for path in ('tools/tests/runtime', 'ambiente_databricks/.assistant'):
            shutil.copytree(ROOT / path, root / path, ignore=shutil.ignore_patterns('__pycache__'))
        moves = json.loads((root / 'tools/tests/runtime/relocation_manifest.json').read_text())['files']
        for item in moves:
            dst = root / item['destination']
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / item['destination'], dst)
        return root

    def test_removed_runtime_svg_fails(self):
        root = self.fixture()
        contract = json.loads((root / 'tools/tests/runtime/package_contract.json').read_text())
        rel = next(p for p in contract['protected'] if p.endswith('.svg'))
        (root / 'ambiente_databricks/.assistant' / rel).unlink()
        self.assertIn('PROTECTED_RESOURCE:' + rel, boundary.check(root))

    def test_removed_fixture_fails(self):
        root = self.fixture()
        rel = 'skills/hub-ml-explainability/tests/linear_fixture.json'
        (root / 'ambiente_databricks/.assistant' / rel).unlink()
        self.assertIn('PROTECTED_RESOURCE:' + rel, boundary.check(root))

    def test_reintroduced_qa_fails(self):
        root = self.fixture()
        rel = 'ambiente_databricks/.assistant/hub_readmes_visual_assets/qa/validation.json'
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{}')
        self.assertIn('MAINTAINER_FILE_IN_PAYLOAD:' + rel, boundary.check(root))

    def test_removed_assertion_fails(self):
        root = self.fixture()
        path = root / 'tools/tests/runtime/test_core.py'
        path.write_text(path.read_text().replace('self.assertEqual(fmt_brl(1.999), "R$ 2,00")', 'pass'))
        self.assertIn('CORE_CASES_OR_ASSERTIONS_CHANGED', boundary.check(root))

    def test_changed_moved_build_input_fails(self):
        root = self.fixture()
        rel = 'tools/readme_visuals/assets/headers/src/copy.json'
        path = root / rel
        path.write_bytes(path.read_bytes() + b' ')
        self.assertIn('MOVED_RESOURCE_CHANGED:' + rel, boundary.check(root))

    def test_moved_build_input_symlink_fails(self):
        root = self.fixture()
        rel = 'tools/readme_visuals/assets/headers/src/copy.json'
        path = root / rel
        other = root / 'borrowed.json'
        path.rename(other)
        path.symlink_to(other)
        self.assertIn('MOVED_RESOURCE_SYMLINK:' + rel, boundary.check(root))

    def test_runtime_resources_without_maintainer_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            isolated = Path(tmp) / '.assistant'
            shutil.copytree(ROOT / 'ambiente_databricks/.assistant', isolated,
                            ignore=shutil.ignore_patterns('__pycache__'))
            code = '''import sys,json,pathlib
sys.path.insert(0,sys.argv[1])
from hub_snippets.visual.tema.tema import resolve_theme
root=pathlib.Path(sys.argv[1]); profiles=root/'hub_padroes/identidade_visual/exemplos'
files=sorted(profiles.glob('*.json'))
assert files, 'no themes found'
for p in files: resolve_theme(p.read_bytes())
from hub_snippets.constants.format_br import fmt_brl
assert fmt_brl(1.999) == "R$ 2,00"
print(len(files))
'''
            result = subprocess.run([sys.executable, '-I', '-c', code, str(isolated)],
                                    cwd=tmp, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertGreater(int(result.stdout.strip()), 0)


class CoreFingerprintTests(unittest.TestCase):
    def signature(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test_core.py'
            path.write_text(source, encoding='utf-8')
            return boundary.core_signature(path)

    def test_golden_digest_across_supported_interpreters(self):
        source = "class Cases:\n    def test_value(self):\n        assert True, 'valor'\n"
        self.assertEqual('c7d4b3ffd13b9445016ac9b8b6788b2c8f2cc5ecfe0954161ef6a7002e273c24', self.signature(source))

    def test_positions_comments_and_empty_type_params_are_neutral(self):
        source = "class Cases:\n    def test_value(self):\n        assert True, 'valor'\n"
        self.assertEqual(self.signature(source), self.signature('# comentário\n\n' + source))
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, boundary.TYPE_PARAM_NODES) and hasattr(node, 'type_params'):
                self.assertEqual([], node.type_params)
                self.assertNotIn('type_params', [field for field, _ in boundary.canonical_ast(node)[2]])

    def test_scalar_types_and_values_do_not_collide(self):
        values = [None, Ellipsis, True, 1, 1.0, '1', b'1', 1j, -0.0, 0.0]
        encoded = [json.dumps(boundary.canonical_ast(ast.Constant(value=value))) for value in values]
        self.assertEqual(len(values), len(set(encoded)))

    @unittest.skipUnless(sys.version_info >= (3, 12), 'PEP 695 syntax requires real Python 3.12+')
    def test_nonempty_type_params_are_semantic(self):
        for source in ('def f[T](): pass', 'async def f[T](): pass', 'class C[T]: pass'):
            with self.subTest(source=source):
                node = ast.parse(source).body[0]
                generic = boundary.canonical_ast(node)
                self.assertIn('type_params', [field for field, _ in generic[2]])
                renamed = ast.parse(source.replace('[T]', '[U]')).body[0]
                self.assertNotEqual(generic, boundary.canonical_ast(renamed))
                node.type_params = []
                self.assertNotEqual(generic, boundary.canonical_ast(node))

    def test_new_ast_fields_are_preserved(self):
        class FutureNode(ast.AST):
            _fields = ('body', 'type_params', 'new_semantics')
        first = FutureNode(body=[], type_params=[], new_semantics=1)
        second = FutureNode(body=[], type_params=[], new_semantics=2)
        self.assertNotEqual(boundary.canonical_ast(first), boundary.canonical_ast(second))
        self.assertIn('type_params', [field for field, _ in boundary.canonical_ast(first)[2]])

    def test_unexpected_ast_metadata_and_missing_fields_are_rejected(self):
        node = ast.parse('def test_x(): assert True').body[0]
        node.unexpected = 'metadata'
        with self.assertRaisesRegex(ValueError, 'UNEXPECTED_AST_METADATA'):
            boundary.canonical_ast(node)
        del node.unexpected
        del node.body
        with self.assertRaisesRegex(ValueError, 'MISSING_AST_FIELD:body'):
            boundary.canonical_ast(node)

    def test_changed_assertion_removed_test_and_async_mutations_change_digest(self):
        source = "class Cases:\n    def test_one(self):\n        assert 1 == 1\n    def test_two(self):\n        assert 2 == 2\n"
        original = self.signature(source)
        mutations = [source.replace('assert 1 == 1', 'assert 1 == 2'),
                     source.replace('assert 1 == 1', 'pass'),
                     source.replace('test_one', 'not_a_test'),
                     source.replace('def test_one', 'async def test_one'),
                     source.replace('test_one', 'test_renamed'),
                     source.replace('assert 2 == 2', 'assert 2 != 2')]
        for mutated in mutations:
            with self.subTest(mutated=mutated):
                self.assertNotEqual(original, self.signature(mutated))

    def test_duplicate_names_and_empty_suite_fail_closed(self):
        sources = [
            ('class C:\n    def test_x(self): assert True\nclass C: pass', 'DUPLICATE_CORE_CLASS'),
            ('class C:\n    def test_x(self): assert False\n    def test_x(self): assert True', 'DUPLICATE_CORE_CASE'),
            ('class C: pass', 'EMPTY_CORE_CASES'),
        ]
        for source, error in sources:
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                self.signature(source)

    def test_contract_metadata_fail_closed(self):
        contract = json.loads((ROOT / 'tools/tests/runtime/package_contract.json').read_text())
        manifest = json.loads((ROOT / 'tools/tests/runtime/relocation_manifest.json').read_text())
        for mutation in ('missing', 'unknown', 'version', 'digest', 'provenance', 'count', 'source'):
            changed = copy.deepcopy(contract)
            fingerprint = changed['core_assertion_fingerprint']
            if mutation == 'missing':
                del changed['core_assertion_fingerprint']
            elif mutation == 'unknown':
                fingerprint['accept_any_hash'] = True
            elif mutation == 'version':
                fingerprint['schema'] = 'unknown'
            elif mutation == 'digest':
                fingerprint['sha256'] = 'not-a-digest'
            elif mutation == 'provenance':
                fingerprint['provenance']['unexpected'] = 'metadata'
            elif mutation == 'count':
                changed['core_case_count'] = True
            else:
                changed['source_commit'] = '0' * 40
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                boundary.validate_fingerprint(changed, manifest)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_CONTRACT_KEY'):
            json.loads('{"schema": "unknown", "schema": "core-tests-ast-v2"}',
                       object_pairs_hook=boundary._unique_object)

    def test_frozen_source_migrates_to_same_digest(self):
        contract = json.loads((ROOT / 'tools/tests/runtime/package_contract.json').read_text())
        provenance = contract['core_assertion_fingerprint']['provenance']
        original = subprocess.run(
            ['git', 'show', provenance['source_commit'] + ':' + provenance['source_path']],
            cwd=ROOT, capture_output=True, check=True).stdout
        self.assertEqual(provenance['source_sha256'], hashlib.sha256(original).hexdigest())
        self.assertEqual(contract['core_assertion_fingerprint']['sha256'],
                         self.signature(original.decode('utf-8')))
        if sys.version_info[:2] == (3, 12):
            tree = ast.parse(original.decode('utf-8'))
            legacy = {c.name: {f.name: ast.dump(f, include_attributes=False) for f in c.body
                              if isinstance(f, ast.FunctionDef) and f.name.startswith('test_')}
                      for c in tree.body if isinstance(c, ast.ClassDef)}
            self.assertEqual(provenance['legacy_ast_sha256'],
                             hashlib.sha256(json.dumps(legacy, sort_keys=True).encode()).hexdigest())

    def test_frozen_migration_provenance(self):
        contract = json.loads((ROOT / 'tools/tests/runtime/package_contract.json').read_text())
        fingerprint = contract['core_assertion_fingerprint']
        self.assertEqual('62652bb85dbe70936d1bee99098ed87a556de7245ed83c7c2acbb85e87e663b8',
                         contract['core_assertion_ast_sha256'])
        self.assertEqual('b48baa202b292fb2070b8bbb207d0bbb0a1e27ec2e73b3398b9d67b094ce8491',
                         fingerprint['provenance']['source_sha256'])
        self.assertEqual('f76821ddb5fc879a9d95a2f2e614527079bcd58f69438a830c756f1dc09fb4c3',
                         boundary.core_signature(ROOT / boundary.CORE_PATH))


if __name__ == '__main__':
    unittest.main(verbosity=2)
