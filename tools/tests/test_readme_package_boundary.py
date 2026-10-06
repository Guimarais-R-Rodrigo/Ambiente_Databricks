"""Prova da fronteira de distribuição, incluindo mutantes discriminantes."""
from __future__ import annotations
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
        for path in ('tools/tests/runtime', 'ambiente_fonte/.assistant'):
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
        (root / 'ambiente_fonte/.assistant' / rel).unlink()
        self.assertIn('PROTECTED_RESOURCE:' + rel, boundary.check(root))

    def test_removed_fixture_fails(self):
        root = self.fixture()
        rel = 'skills/hub-ml-explainability/tests/linear_fixture.json'
        (root / 'ambiente_fonte/.assistant' / rel).unlink()
        self.assertIn('PROTECTED_RESOURCE:' + rel, boundary.check(root))

    def test_reintroduced_qa_fails(self):
        root = self.fixture()
        rel = 'ambiente_fonte/.assistant/hub_readmes_visual_assets/qa/validation.json'
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
            shutil.copytree(ROOT / 'ambiente_fonte/.assistant', isolated,
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
