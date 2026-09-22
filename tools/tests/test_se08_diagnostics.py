"""Testa o observador; chamadas nativas Restart Manager NÃO são simuladas como PASS."""
from __future__ import annotations

import gc
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import weakref

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('se08_observer_under_test', ROOT / 'tools/skill_enforcement/se08_diagnostics.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='sef-observer-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.journal = d.Journal(self.root / 'events.jsonl')
        self.addCleanup(self.journal.close)

    def events(self):
        return [json.loads(x) for x in (self.root / 'events.jsonl').read_text().splitlines()]

    def cert(self, fail=False, error=None):
        parent = self.root
        class ProcessTemp(tempfile.TemporaryDirectory):
            def __init__(self):
                super().__init__(prefix='sef-process-', dir=parent)
                self.record = {'cleanup': 'COMPLETE', 'result': 'EXITED', 'pid': 7}
                (Path(self.name) / 'stderr').write_bytes(b'')
            def __exit__(self, *args):
                if fail:
                    self.record.update(cleanup='FAILED', temporary_cleanup='FAILED')
                    raise error if error is not None else PermissionError('synthetic-before-cleanup')
                return super().__exit__(*args)
        return SimpleNamespace(_ProcessTemporaryDirectory=ProcessTemp)

    def test_normal_cleanup_keeps_original_result(self):
        cert = self.cert()
        with d.CleanupObserver(cert, self.journal):
            with cert._ProcessTemporaryDirectory() as path:
                self.assertTrue(Path(path).exists())
        self.assertFalse(Path(path).exists())
        events = [e['event'] for e in self.events()]
        self.assertIn('EXPLICIT_CLEANUP_ENTER', events)
        self.assertNotIn('AUTOMATIC_FINALIZER_ENTER', events)
        self.assertNotIn('PROCESS_TEMP_EXIT_ERROR', events)

    def test_injected_exit_failure_and_automatic_finalizer_are_distinct(self):
        cert = self.cert(fail=True)
        with d.CleanupObserver(cert, self.journal):
            obj = cert._ProcessTemporaryDirectory(); path = obj.name
            ref = weakref.ref(obj)
            try:
                with obj:
                    pass
            except PermissionError:
                pass
            self.assertTrue(Path(path).exists())
            self.assertEqual('FAILED', obj.record['cleanup'])
            del obj
            gc.collect()
            self.assertIsNone(ref(), 'observador não deve reter o objeto temporário')
            self.assertFalse(Path(path).exists())
        events = [e['event'] for e in self.events()]
        self.assertLess(events.index('PROCESS_TEMP_EXIT_ERROR'), events.index('AUTOMATIC_FINALIZER_ENTER'))
        self.assertFalse(next(e for e in self.events() if e['event'] == 'AUTOMATIC_FINALIZER_EXIT')['exists'])

    def test_original_exception_identity_is_preserved(self):
        exc = PermissionError('exact-synthetic-error'); cert = self.cert(fail=True, error=exc)
        with d.CleanupObserver(cert, self.journal):
            obj = cert._ProcessTemporaryDirectory()
            with self.assertRaises(PermissionError) as caught:
                obj.__exit__(None, None, None)
            self.assertIs(caught.exception, exc)
            obj.cleanup()

    def test_owner_query_occurs_only_after_failure(self):
        exc = PermissionError('synthetic-native-shaped-error'); exc.winerror = 32
        cert = self.cert(fail=True, error=exc)
        with d.CleanupObserver(cert, self.journal, query_owners=True, case='f04-never-ready'):
            obj = cert._ProcessTemporaryDirectory(); exc.filename = str(Path(obj.name) / 'stderr')
            with patch.object(d, 'resource_users', return_value={'status': 'MOCK_ONLY', 'users': [{'pid': 123}]}) as query:
                with self.assertRaises(PermissionError):
                    obj.__exit__(None, None, None)
                query.assert_called_once()
            self.assertEqual('FAILED', obj.record['cleanup'])
            obj.cleanup()
        self.assertIn('RESOURCE_USERS_AFTER_FAILURE', [e['event'] for e in self.events()])

    def test_declared_storage_injection_is_not_queried_as_native(self):
        exc = PermissionError('SYNTHETIC_STORAGE_CLEANUP'); exc.winerror = 32
        cert = self.cert(fail=True, error=exc)
        with d.CleanupObserver(cert, self.journal, query_owners=True, case='storage-residue'):
            obj = cert._ProcessTemporaryDirectory()
            with patch.object(d, 'resource_users', side_effect=AssertionError('não consultar')):
                with self.assertRaises(PermissionError):
                    obj.__exit__(None, None, None)
            obj.cleanup()
        self.assertIn('RESOURCE_USERS_NOT_QUERIED', [e['event'] for e in self.events()])

    def test_query_error_does_not_replace_original_failure(self):
        exc = PermissionError('original'); exc.winerror = 32
        cert = self.cert(fail=True, error=exc)
        with d.CleanupObserver(cert, self.journal, query_owners=True):
            obj = cert._ProcessTemporaryDirectory(); exc.filename = str(Path(obj.name) / 'stderr')
            with patch.object(d, 'resource_users', side_effect=OSError('query-denied')):
                with self.assertRaises(PermissionError) as caught:
                    obj.__exit__(None, None, None)
                self.assertIs(caught.exception, exc)
            obj.cleanup()
        event = next(e for e in self.events() if e['event'] == 'RESOURCE_USERS_AFTER_FAILURE')
        self.assertEqual('NOT_OBSERVABLE', event['result']['status'])

    def test_unexpected_query_failure_does_not_mask_native_shaped_error(self):
        exc = PermissionError('original-unexpected'); exc.winerror = 32
        cert = self.cert(fail=True, error=exc)
        with d.CleanupObserver(cert, self.journal, query_owners=True):
            obj = cert._ProcessTemporaryDirectory(); exc.filename = str(Path(obj.name) / 'stderr')
            try:
                with patch.object(d, 'resource_users', side_effect=RuntimeError('diagnostic-bug')):
                    with self.assertRaises(PermissionError) as caught:
                        obj.__exit__(None, None, None)
                    self.assertIs(caught.exception, exc)
            finally:
                obj.cleanup()

    def test_hooks_are_restored(self):
        cert = self.cert()
        original = (tempfile.TemporaryDirectory.cleanup, tempfile.TemporaryDirectory.__dict__['_cleanup'], cert._ProcessTemporaryDirectory.__exit__)
        with d.CleanupObserver(cert, self.journal):
            pass
        self.assertEqual(original, (tempfile.TemporaryDirectory.cleanup, tempfile.TemporaryDirectory.__dict__['_cleanup'], cert._ProcessTemporaryDirectory.__exit__))

    def test_journal_error_does_not_raise_from_emit(self):
        self.journal.close()
        self.journal.emit('after-close')
        self.assertEqual(1, len(self.journal.errors))

    def test_record_snapshot_does_not_mutate_input(self):
        original = {'cleanup': 'FAILED', 'pid': 23, 'secret_unrelated': object()}
        snapshot = d.record_fields(original)
        snapshot['cleanup'] = 'changed'
        self.assertEqual('FAILED', original['cleanup'])
        self.assertNotIn('secret_unrelated', snapshot)

    def test_linux_does_not_claim_restart_manager_observed(self):
        resource = self.root / 'absent'
        with patch.object(d.os, 'name', 'posix'):
            result = d.resource_users([resource])
        self.assertEqual('NOT_WINDOWS', result['status'])
        self.assertFalse(result['absence_proven'])

    def test_output_inside_repo_is_rejected(self):
        with self.assertRaises(ValueError):
            d.reserve_output(str(self.root / 'inside'), self.root)
        self.assertFalse((self.root / 'inside').exists())

    def test_existing_output_is_not_overwritten(self):
        existing = self.root / 'existing'; existing.mkdir()
        (existing / 'sentinel').write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):
            d.reserve_output(str(existing), self.root / 'repo')
        self.assertEqual(b'preserve', (existing / 'sentinel').read_bytes())

    def test_main_refuses_wrong_sha_before_reserving_output(self):
        identity = {'head': 'a' * 40, 'tree': 'b' * 40, 'status': '', 'shallow': 'false'}
        out = self.root / 'not-created'
        with patch.object(d, 'git_identity', return_value=identity), patch.object(d, 'capabilities') as call:
            with self.assertRaises(SystemExit) as caught:
                d.main(['--case', 'capabilities', '--expected-sha', 'c' * 40, '--evidence-dir', str(out)])
            self.assertEqual(2, caught.exception.code)
            call.assert_not_called()
        self.assertFalse(out.exists())

    def test_main_capability_case_in_synthetic_git_fixture(self):
        import subprocess
        repo = self.root / 'repo'; repo.mkdir()
        def git(*args):
            return subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True).stdout.decode().strip()
        git('init', '-q')
        git('-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid',
            'commit', '--allow-empty', '-qm', 'fixture')
        head = git('rev-parse', 'HEAD'); out = self.root / 'capabilities-bundle'
        with patch.object(d, 'ROOT', repo):
            code = d.main(['--case', 'capabilities', '--expected-sha', head, '--evidence-dir', str(out)])
        summary = json.loads((out / 'summary.json').read_text())
        expected = 0 if all(x['status'] == 'CREATED' for x in summary['capabilities']['symlinks']) else 1
        self.assertEqual(expected, code)
        self.assertEqual(head, summary['before']['head'])
        self.assertEqual(summary['before'], summary['after'])
        self.assertFalse(summary['release_certified'])

    def test_main_cannot_return_zero_after_identity_change(self):
        before = {'head': 'a' * 40, 'tree': 'b' * 40, 'status': '', 'shallow': 'false'}
        after = dict(before, status='?? changed')
        out = self.root / 'identity-changed'
        with patch.object(d, 'git_identity', side_effect=[before, after]), patch.object(d, 'capabilities', return_value={'symlinks': []}):
            code = d.main(['--case', 'capabilities', '--expected-sha', 'a' * 40, '--evidence-dir', str(out)])
        summary = json.loads((out / 'summary.json').read_text())
        self.assertEqual(0, summary['case_exit'])
        self.assertNotEqual(0, code)
        self.assertFalse(summary['identity_stable'])

    def test_capability_probe_reports_not_hides_symlink_failure(self):
        with patch.object(Path, 'symlink_to', side_effect=PermissionError(13, 'synthetic-unavailable')):
            result = d.capabilities(self.root)
        self.assertEqual(['UNAVAILABLE', 'UNAVAILABLE'], [x['status'] for x in result['symlinks']])
        self.assertFalse(result['test_skips_added'])
        self.assertFalse(result['privileges_changed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
