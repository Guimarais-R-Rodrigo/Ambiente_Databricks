"""Testa os predicados reais dos mocks V02 sem simular um runtime Windows.

PureWindowsPath demonstra a semântica do seletor, não a execução NTFS.
Os subprocessos de isolamento são reais e não importam bibliotecas do Hub.
"""
from __future__ import annotations

import ast
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).with_name('test_temas_v02.py')
TARGETS = {
    'test_duplicate_schema_rejected': 'V01/theme.schema.json',
    'test_derived_fixture_drift_rejected': 'exemplos/legado_notebook.json',
    'test_layout_changed_dictionary': 'identidade_visual/TOKENS.md',
    'test_layout_changed_api': 'tema/__init__.py',
    'test_layout_changed_schema': 'identidade_visual/theme.schema.json',
}
ISOLATED = ('test_missing_dependencies_reported_without_install',
            'test_import_without_third_party_modules_or_platform')


def method(name):
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    found = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(found) != 1:
        raise AssertionError(f'Método não único: {name}')
    return found[0]


def invocation_flags(name):
    calls = [n for n in ast.walk(method(name)) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == 'run'
             and isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess']
    if len(calls) != 1 or not isinstance(calls[0].args[0], ast.List):
        raise AssertionError('Esperada uma invocação subprocess.run explícita')
    argv = calls[0].args[0].elts
    end = next(i for i, n in enumerate(argv) if isinstance(n, ast.Constant) and n.value == '-c')
    return [ast.literal_eval(n) for n in argv[1:end]]


class V02PortabilityTests(unittest.TestCase):
    def check_selector(self, name):
        suffix = TARGETS[name]
        selectors = [n for n in ast.walk(method(name)) if isinstance(n, ast.Call)
                     and isinstance(n.func, ast.Attribute) and n.func.attr == 'endswith']
        self.assertEqual(1, len(selectors), name)
        expression = compile(ast.Expression(selectors[0]), str(SOURCE), 'eval')
        for cls in (PurePosixPath, PureWindowsPath):
            for tail, expected in ((suffix, True), (suffix + '.bak', False),
                                   (suffix.lower(), suffix == suffix.lower())):
                with self.subTest(method=name, path_kind=cls.__name__, tail=tail):
                    path = cls('sandbox') / tail
                    actual = eval(expression, {'__builtins__': {}, 'str': str}, {'path': path})
                    self.assertEqual(expected, actual)

    def test_duplicate_schema_selector(self):
        self.check_selector('test_duplicate_schema_rejected')

    def test_fixture_selector(self):
        self.check_selector('test_derived_fixture_drift_rejected')

    def test_dictionary_selector(self):
        self.check_selector('test_layout_changed_dictionary')

    def test_api_selector(self):
        self.check_selector('test_layout_changed_api')

    def test_schema_selector(self):
        self.check_selector('test_layout_changed_schema')

    def test_dependency_missing_invocation_is_isolated(self):
        flags = invocation_flags(ISOLATED[0])
        self.assertIn('-I', flags)
        self.assertIn('-S', flags)
        self.assertIn('-B', flags)

    def test_import_invocation_is_isolated(self):
        flags = invocation_flags(ISOLATED[1])
        self.assertIn('-I', flags)
        self.assertIn('-S', flags)

    def test_inherited_pythonpath_and_cwd_do_not_leak_into_probes(self):
        with tempfile.TemporaryDirectory(prefix='sef-isolation-') as td:
            root = Path(td)
            (root / 'sef_foreign_probe.py').write_text('MARKER = True\n', encoding='utf-8')
            env = dict(os.environ, PYTHONPATH=str(root))
            code = "import importlib.util;print(importlib.util.find_spec('sef_foreign_probe') is None)"
            control = subprocess.run([sys.executable, '-B', '-S', '-c', code], cwd=root,
                                     env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(0, control.returncode, control.stderr)
            self.assertEqual('False', control.stdout.strip(), 'controle precisa detectar contaminação')
            for name in ISOLATED:
                with self.subTest(method=name):
                    proc = subprocess.run([sys.executable, *invocation_flags(name), '-c', code],
                                          cwd=root, env=env, capture_output=True, text=True, timeout=15)
                    self.assertEqual(0, proc.returncode, proc.stderr)
                    self.assertEqual('True', proc.stdout.strip())


if __name__ == '__main__':
    unittest.main(verbosity=2)
