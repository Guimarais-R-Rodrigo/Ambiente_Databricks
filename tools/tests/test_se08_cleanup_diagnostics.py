"""Regressões do observador SE08. Doubles Win32 não são execução nativa."""
from __future__ import annotations

import ctypes as C
import gc
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import warnings

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill_enforcement import cleanup_diagnostics as diag


class FakeRM:
    """Double de protocolo; não reproduz handles do kernel Windows."""
    def __init__(self, failure=None, empty=False):
        self.failure, self.empty, self.calls = failure, empty, []

    def RmStartSession(self, session, flags, key):
        self.calls.append('start')
        C.cast(session, C.POINTER(C.c_uint32))[0] = 17
        return 5 if self.failure == 'start' else 0

    def RmRegisterResources(self, *args):
        self.calls.append('register')
        return 5 if self.failure == 'register' else 0

    def RmGetList(self, session, needed, count, buffer, reasons):
        self.calls.append('query')
        C.cast(needed, C.POINTER(C.c_uint32))[0] = 0 if self.empty else 1
        C.cast(count, C.POINTER(C.c_uint32))[0] = 0 if self.empty else 1
        buffer[0].process.pid = 123
        buffer[0].process.started.low = 9
        buffer[0].process.started.high = 2
        return 234 if self.failure == 'more_data' else (5 if self.failure == 'query' else 0)

    def RmEndSession(self, session):
        self.calls.append('end')
        return 6 if self.failure == 'end' else 0


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='sef-diag-unit-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.recorder = diag.Recorder(self.root/'events.jsonl')

    def rows(self):
        return [json.loads(l) for l in (self.root/'events.jsonl').read_text().splitlines()]

    def test_win32_abi_has_fixed_width_fields(self):
        self.assertEqual(C.sizeof(diag.FileTime), 8)
        self.assertEqual(C.sizeof(diag.UniqueProcess), 12)
        self.assertEqual(C.sizeof(diag.ProcessInfo), 668)
        self.assertEqual(diag.ProcessInfo.kind.offset, 652)

    def test_rm_matching_pid_has_creation_identity(self):
        api = FakeRM()
        r = diag.file_users([self.root/'stderr'], api=api)
        self.assertEqual(r['status'], 'MATCHES_REPORTED')
        self.assertEqual(r['processes'][0]['start_filetime'], (2 << 32) | 9)
        self.assertEqual(r['processes'][0]['pid'], 123)
        self.assertEqual(api.calls, ['start', 'register', 'query', 'end'])

    def test_empty_rm_is_not_proof_of_no_handles(self):
        r = diag.file_users([self.root/'stderr'], api=FakeRM(empty=True))
        self.assertEqual(r['status'], 'NO_MATCHES_REPORTED_NOT_PROOF_OF_NO_HANDLES')

    def test_failed_rm_start_does_not_close_unopened_session(self):
        api = FakeRM('start')
        self.assertEqual(diag.file_users([self.root/'stderr'], api=api)['status'], 'UNOBSERVABLE')
        self.assertEqual(api.calls, ['start'])

    def test_failed_registration_closes_own_session(self):
        api = FakeRM('register')
        self.assertEqual(diag.file_users([self.root/'stderr'], api=api)['status'], 'UNOBSERVABLE')
        self.assertEqual(api.calls, ['start', 'register', 'end'])

    def test_more_data_is_incomplete_without_retry(self):
        api = FakeRM('more_data')
        self.assertEqual(diag.file_users([self.root/'stderr'], api=api)['status'], 'INCOMPLETE_QUERY')
        self.assertEqual(api.calls.count('query'), 1)
        self.assertEqual(api.calls[-1], 'end')

    def test_query_error_is_incomplete_and_not_empty_success(self):
        self.assertEqual(diag.file_users([self.root/'stderr'], api=FakeRM('query'))['status'], 'INCOMPLETE_QUERY')

    def test_session_end_failure_is_visible(self):
        self.assertEqual(diag.file_users([self.root/'stderr'], api=FakeRM('end'))['status'], 'INCOMPLETE_SESSION_END')

    def test_unexpected_api_error_still_ends_session(self):
        api = FakeRM()
        with patch.object(api, 'RmGetList', side_effect=OSError('synthetic')):
            with self.assertRaises(OSError):
                diag.file_users([self.root/'stderr'], api=api)
        self.assertEqual(api.calls[-1], 'end')

    def test_job_snapshot_observes_only_supplied_job(self):
        class Accounting(C.Structure):
            _fields_ = [('ActiveProcesses', C.c_uint32), ('TotalProcesses', C.c_uint32),
                        ('TotalTerminatedProcesses', C.c_uint32)]
        calls = []
        def query(handle, kind, pointer, size, returned):
            calls.append((handle, kind))
            if kind == 1:
                value = C.cast(pointer, C.POINTER(Accounting)).contents
                value.ActiveProcesses, value.TotalProcesses = 2, 2
            elif kind == 3:
                value = C.cast(pointer, C.POINTER(diag.JobPids)).contents
                value.assigned, value.count = 2, 2
                value.pids[0], value.pids[1] = 123, 456
            return 1
        job = SimpleNamespace(handle=987, accounting=Accounting,
                              k=SimpleNamespace(QueryInformationJobObject=query))
        result = diag.job_snapshot(job)
        self.assertEqual(result['pid_list']['pids'], [123, 456])
        self.assertEqual(calls, [(987, 1), (987, 3)])

    def test_closed_job_is_not_zero_active_processes_proof(self):
        self.assertEqual(diag.job_snapshot(SimpleNamespace(handle=None)),
                         {'status': 'NO_OPEN_OWNED_JOB'})

    def test_query_size_is_limited(self):
        api = FakeRM()
        self.assertEqual(diag.file_users([], api=api)['status'], 'INVALID_TARGET_SET')
        self.assertEqual(api.calls, [])

    def test_restart_manager_accepts_exact_three_owned_stream_resources(self):
        api = FakeRM(empty=True)
        targets = [self.root/'stdout', self.root/'stderr', self.root/'child.json']
        result = diag.file_users(targets, api=api)
        self.assertEqual(result['resource_count'], 3)
        self.assertEqual(result['status'], 'NO_MATCHES_REPORTED_NOT_PROOF_OF_NO_HANDLES')
        rejected = diag.file_users([*targets, self.root/'extra'], api=FakeRM())
        self.assertEqual(rejected['status'], 'INVALID_TARGET_SET')

    def test_historical_native_failure_target_is_explicit(self):
        source = Path(diag.__file__).read_text(encoding='utf-8')
        self.assertIn("'keyboard-before-output'", source)
        self.assertIn("'test_keyboard_interrupt_before_first_output'", source)
        self.assertIn("Path(self.name)/'child.json'", source)

    def test_non_windows_provider_is_not_native_evidence(self):
        with patch.object(diag.os, 'name', 'posix'):
            self.assertEqual(diag.file_users(['unused'])['status'], 'NOT_APPLICABLE_NON_WINDOWS')

    def test_recorder_monotonic_sequence(self):
        self.recorder.emit('one')
        self.recorder.emit('two')
        rows = self.rows()
        self.assertEqual([r['sequence'] for r in rows], [1, 2])
        self.assertLessEqual(rows[0]['monotonic_ns'], rows[1]['monotonic_ns'])

    def test_recorder_cannot_overwrite_prior_journal(self):
        with self.assertRaises(FileExistsError):
            diag.Recorder(self.root/'events.jsonl')

    def test_recorder_errors_are_not_silently_lost(self):
        with patch.object(Path, 'open', side_effect=PermissionError('synthetic')):
            self.recorder.emit('fault')
        self.assertEqual(self.recorder.errors[0]['type'], 'PermissionError')

    def cert_double(self, fail_exit=False):
        class Temporary(tempfile.TemporaryDirectory):
            def __exit__(self, *args):
                if fail_exit:
                    raise PermissionError('synthetic pre-original-exit')
                return super().__exit__(*args)
        class Job:
            handle = None
            def assign(self, process): return None
            def terminate(self): return None
            def close(self): return None
        return SimpleNamespace(_ProcessTemporaryDirectory=Temporary, _WindowsJob=Job,
                               _persist_process_observation=lambda r: 'original-return')

    def test_hooks_restore_and_preserve_success_result(self):
        cert = self.cert_double()
        original = cert._ProcessTemporaryDirectory.__exit__
        with diag.observe(cert, self.recorder):
            with cert._ProcessTemporaryDirectory(dir=self.root) as name:
                Path(name, 'stderr').write_text('synthetic', encoding='utf-8')
            self.assertFalse(Path(name).exists())
        self.assertIs(cert._ProcessTemporaryDirectory.__exit__, original)
        self.assertIn('explicit_cleanup_end', [r['event'] for r in self.rows()])

    def test_process_records_not_rewritten_by_observer(self):
        cert = self.cert_double()
        record = {'result': 'INTERRUPTED', 'cleanup': 'FAILED', 'pid': None}
        original = dict(record)
        with diag.observe(cert, self.recorder):
            self.assertEqual(cert._persist_process_observation(record), 'original-return')
        self.assertEqual(record, original)

    def test_original_exception_propagates_unchanged(self):
        cert = self.cert_double(fail_exit=True)
        with diag.observe(cert, self.recorder):
            temp = cert._ProcessTemporaryDirectory(dir=self.root)
            with self.assertRaisesRegex(PermissionError, 'synthetic pre-original-exit'):
                with temp:
                    pass
            self.assertTrue(Path(temp.name).exists())
            temp.cleanup()  # Explicit test teardown, not diagnostic recovery.

    def test_implicit_finalizer_is_observed_not_disabled(self):
        cert = self.cert_double(fail_exit=True)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('always', ResourceWarning)
            with diag.observe(cert, self.recorder):
                def create_and_drop():
                    temp = cert._ProcessTemporaryDirectory(dir=self.root)
                    name = temp.name
                    try:
                        with temp:
                            Path(name, 'stderr').write_text('synthetic', encoding='utf-8')
                    except PermissionError:
                        self.assertTrue(Path(name).exists())
                    return name
                name = create_and_drop()
                gc.collect()
        events = self.rows()
        self.assertFalse(Path(name).exists())
        start = next(i for i, r in enumerate(events) if r['event'] == 'implicit_finalizer_begin')
        end = next(i for i, r in enumerate(events) if r['event'] == 'implicit_finalizer_end')
        self.assertLess(start, end)
        self.assertTrue(events[start]['snapshot']['lexists'])
        self.assertFalse(events[end]['snapshot']['lexists'])

    def test_existing_evidence_directory_rejected(self):
        with self.assertRaises(FileExistsError):
            diag.reserve_output(self.root, self.root/'repo')

    def test_internal_evidence_rejected(self):
        with self.assertRaisesRegex(ValueError, 'EXTERNAL'):
            diag.reserve_output(self.root/'new', self.root)

    def test_symlink_alias_rejected_before_reservation(self):
        alias = self.root/'alias'
        original = Path.is_symlink
        # Deterministic query double; the preflight separately observes native privilege.
        with patch.object(Path, 'is_symlink', lambda p: p == alias or original(p)):
            with self.assertRaisesRegex(ValueError, 'ALIAS'):
                diag.reserve_output(alias/'evidence', self.root/'repo')
        self.assertFalse(alias.exists())

    def test_preflight_does_not_elevate_on_symlink_failure(self):
        exc = PermissionError(13, 'synthetic symlink denial')
        exc.winerror = 1314
        with patch.object(Path, 'symlink_to', side_effect=exc):
            value = diag.preflight(self.root)
        self.assertTrue(all(v['status'] == 'BLOCKED' for v in value['symlinks'].values()))
        self.assertEqual(value['symlinks']['file']['error']['winerror'], 1314)

    def test_git_identity_from_real_synthetic_repository(self):
        repo = self.root/'repo'
        repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        subprocess.run(['git', '-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid',
                        'commit', '--allow-empty', '-qm', 'fixture'], cwd=repo, check=True)
        result = diag.git_identity(repo)
        self.assertEqual(len(result['sha']), 40)
        (repo/'dirty').write_text('x')
        with self.assertRaisesRegex(ValueError, 'CLEAN'):
            diag.git_identity(repo)


if __name__ == '__main__':
    unittest.main()
