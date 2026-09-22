"""Component tests of the real storage injection function, not a product gate.

The function is compiled from its AST so these GC controls do not start the
certifier or import/execute its test suite. Real TemporaryDirectory objects are
used; the certifier, process result and external exit are deliberate doubles.
Native Windows evidence and the full 9-method storage suite remain separate.
"""
from __future__ import annotations

import ast
import gc
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import warnings

SOURCE = Path(__file__).with_name('test_certify_storage_cleanup.py')


def load_probe(*, remove_retention=False):
    tree = ast.parse(SOURCE.read_text(encoding='utf8'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'cli_probe')
    if remove_retention:
        class Mutant(ast.NodeTransformer):
            def visit_Assign(self, node):
                if any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)
                       and t.value.id == 'retained_temporaries' for t in node.targets):
                    return ast.copy_location(ast.Pass(), node)
                return self.generic_visit(node)
        function = Mutant().visit(function)
    cert = SimpleNamespace(_persist_process_observation=lambda record: None)
    support = SimpleNamespace(main_cli_probe=None)
    namespace = dict(Path=Path, json=json, os=os, shutil=shutil, sys=sys,
                     tempfile=tempfile, mock=mock, cert=cert, support=support)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])),
                 str(SOURCE), 'exec'), namespace)
    return namespace['cli_probe'], cert, support


class StorageOracleLifetimeTests(unittest.TestCase):
    def run_probe(self, fault='before_removal', *, mutant=False, mode='keyboard'):
        probe, cert, support = load_probe(remove_retention=mutant)
        record = {'result': 'EXITED' if mode == 'normal' else 'INTERRUPTED',
                  'cleanup': 'FAILED', 'stdout': 'CLI_BEFORE_INTERRUPT'}
        seen = {}
        class SyntheticTemporary(tempfile.TemporaryDirectory):
            def __exit__(self, *args):
                # The actual injection reads the direct caller's local record.
                record = seen['record']
                return super().__exit__(*args)
        def fake_main(*args):
            try:
                with SyntheticTemporary(prefix='sef-process-') as directory:
                    seen['path'] = Path(directory)
                    (seen['path'] / 'stderr').write_bytes(b'SYNTHETIC-RESIDUE')
                    (seen['path'] / 'stdout').write_bytes(b'')
            except PermissionError as exc:
                seen['error'] = (type(exc).__name__, exc.errno, exc.winerror)
            # No traceback or object reference is retained here. This makes the
            # old failure deterministic, independent of the runtime's GC timing.
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', ResourceWarning)
                gc.collect()
            raise SystemExit(8 if mode == 'nonzero' else 130)
        seen['record'] = record
        support.main_cli_probe = fake_main
        with tempfile.TemporaryDirectory(prefix='sef-r2-oracle-test-') as output:
            out = Path(output)
            with self.assertRaises(SystemExit) as raised:
                probe(mode, 'gate', 'synthetic-unused-root', str(out), fault)
            oracle = json.loads((out / 'storage-oracles.json').read_text())
            copied = out / 'retained-temporary' / 'stderr'
            snapshot = copied.read_bytes() if copied.exists() else None
            self.assertFalse(seen['path'].exists(), 'test disposal must not leak')
        return raised.exception.code, oracle, snapshot, record, seen

    def test_gc_cannot_remove_retained_residue_before_oracle(self):
        code, oracle, snapshot, record, seen = self.run_probe()
        item = oracle['injections'][0]
        self.assertEqual(130, code)
        self.assertEqual(('PermissionError', 13, 32), seen['error'])
        self.assertTrue(item['exists_before_error'])
        self.assertTrue(item['exists_at_oracle'])
        self.assertTrue(item['test_owner_retained_at_oracle'])
        self.assertTrue(item['finalizer_alive_at_oracle'])
        self.assertTrue(item['test_disposal_after_oracle'])
        self.assertEqual(b'SYNTHETIC-RESIDUE', snapshot)
        self.assertEqual('FAILED', record['cleanup'])

    def test_retention_mutant_reproduces_disappearing_residue(self):
        code, oracle, snapshot, record, _ = self.run_probe(mutant=True)
        self.assertEqual(130, code)
        self.assertTrue(oracle['injections'][0]['exists_before_error'])
        self.assertFalse(oracle['injections'][0]['exists_at_oracle'])
        self.assertIsNone(snapshot)
        self.assertEqual('FAILED', record['cleanup'])

    def test_after_removal_is_not_misreported_as_retained(self):
        code, oracle, snapshot, record, _ = self.run_probe('after_removal')
        self.assertEqual(130, code)
        item = oracle['injections'][0]
        self.assertFalse(item['exists_before_error'])
        self.assertFalse(item['exists_at_oracle'])
        self.assertNotIn('test_owner_retained_at_oracle', item)
        self.assertIsNone(snapshot)
        self.assertEqual('FAILED', record['cleanup'])

    def test_no_fault_does_not_take_ownership(self):
        code, oracle, snapshot, _, seen = self.run_probe('none')
        self.assertEqual(130, code)
        self.assertEqual([], oracle['injections'])
        self.assertNotIn('error', seen)
        self.assertIsNone(snapshot)

    def test_nonzero_interruption_convention_is_unchanged(self):
        code, oracle, snapshot, record, _ = self.run_probe(mode='nonzero')
        self.assertEqual(8, code)
        self.assertTrue(oracle['injections'][0]['exists_at_oracle'])
        self.assertEqual(b'SYNTHETIC-RESIDUE', snapshot)
        self.assertEqual('INTERRUPTED', record['result'])

    def test_original_residue_assertions_are_not_removed(self):
        text = SOURCE.read_text(encoding='utf8')
        self.assertIn('self.assertTrue(oracle["injections"][0]["exists_at_oracle"])', text)
        self.assertIn('self.assertTrue(record["temporary_directory_exists_after_cleanup"])', text)
        self.assertNotIn('._finalizer.detach(', text)
        self.assertNotIn('ignore_errors=True', text)


if __name__ == '__main__':
    unittest.main()
