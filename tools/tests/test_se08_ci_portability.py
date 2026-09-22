"""Regressões dos instrumentos V02, sem simular a suíte de produto inteira.

Executa callbacks reais extraídos por AST com PureWindowsPath/PurePosixPath e
um subprocesso real para conferir a fronteira de isolamento do interpretador.
Não equivale à execução nativa Windows do CI ou ao contrato visual completo.
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


def methods():
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    return {node.name: node for cls in tree.body if isinstance(cls, ast.ClassDef)
            for node in cls.body if isinstance(node, ast.FunctionDef)}


class InstrumentPortabilityTests(unittest.TestCase):
    cases = (
        ('test_duplicate_schema_rejected', 'exists', 'V01/theme.schema.json', True),
        ('test_derived_fixture_drift_rejected', 'read', 'exemplos/legado_notebook.json', b'{}'),
        ('test_layout_changed_dictionary', 'read', 'identidade_visual/TOKENS.md', 'changed'),
        ('test_layout_changed_api', 'read', 'tema/__init__.py', ''),
        ('test_layout_changed_schema', 'read', 'identidade_visual/theme.schema.json', b'{}'),
    )

    def check_callback(self, path_class):
        for method, callback, suffix, expected in self.cases:
            with self.subTest(method=method, path_class=path_class.__name__):
                node = next(n for n in methods()[method].body
                            if isinstance(n, ast.FunctionDef) and n.name == callback)
                sentinel = object()
                calls = []
                def original(*args, **kwargs):
                    calls.append((args, kwargs))
                    return sentinel
                ns = {'original': original}
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), ns)
                matching = path_class('sandbox') / suffix
                self.assertEqual(ns[callback](matching), expected)
                self.assertEqual(calls, [])
                unrelated = path_class('sandbox') / ('unrelated-' + suffix.replace('/', '-'))
                self.assertIs(ns[callback](unrelated), sentinel)
                self.assertEqual(calls[0][0][0], unrelated)

    def test_real_callbacks_match_windows_paths(self):
        self.check_callback(PureWindowsPath)

    def test_real_callbacks_match_posix_paths(self):
        self.check_callback(PurePosixPath)

    def test_dependency_boundary_ignores_injected_pythonpath(self):
        """Usa os flags reais de cada teste V02, sem importar seu runtime."""
        with tempfile.TemporaryDirectory(prefix='sef-pythonpath-control-') as td:
            root = Path(td)
            (root/'sef_foreign_dependency.py').write_text('MARKER = True\n', encoding='utf-8')
            code = ("import importlib.util;"
                    "assert importlib.util.find_spec('sef_foreign_dependency') is None, 'PYTHONPATH_LEAK'")
            for name in ('test_missing_dependencies_reported_without_install',
                         'test_import_without_third_party_modules_or_platform'):
                with self.subTest(method=name):
                    run = next(n for n in ast.walk(methods()[name])
                               if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                               and isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess'
                               and n.func.attr == 'run')
                    # Execute exactly the argument prefix configured in the real test.
                    argv = eval(compile(ast.Expression(run.args[0]), str(SOURCE), 'eval'),
                                {'sys': sys, 'code': code, 'PRODUCT': root})
                    result = subprocess.run(argv, capture_output=True, text=True, timeout=15,
                                            cwd=root, env=dict(os.environ, PYTHONPATH=str(root)))
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_isolation_control_without_flags_detects_injection(self):
        with tempfile.TemporaryDirectory(prefix='sef-pythonpath-positive-') as td:
            Path(td, 'sef_foreign_dependency.py').write_text('MARKER = True\n', encoding='utf-8')
            code = ("import importlib.util;"
                    "assert importlib.util.find_spec('sef_foreign_dependency') is not None")
            result = subprocess.run([sys.executable, '-B', '-S', '-c', code],
                                    capture_output=True, text=True, timeout=15,
                                    env=dict(os.environ, PYTHONPATH=td))
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
