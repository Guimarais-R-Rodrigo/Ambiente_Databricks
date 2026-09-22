"""Regressões do observador SE08. Doubles Win32 não são execução nativa."""
from __future__ import annotations

import ctypes as C
from contextlib import nullcontext
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


    def test_r2_native_cases_name_both_observed_failures(self):
        self.assertEqual(diag.NATIVE_CASES, {
            'never-ready': 'test_never_ready_has_finite_diagnostic_and_cleanup',
            'before-output': 'test_keyboard_interrupt_before_first_output',
        })

    def test_r2_native_cases_refuse_non_windows(self):
        identity = {'root': str(diag.ROOT), 'sha': 'a'*40, 'tree': 'b'*40, 'status': ''}
        fake_os = SimpleNamespace(name='posix', environ=os.environ, path=os.path, getpid=os.getpid)
        for case in diag.NATIVE_CASES:
            output = self.root/case
            with patch.object(diag, 'os', fake_os), patch.object(diag, 'git_identity', return_value=identity), \
                 patch.object(diag, 'load_support') as loader:
                self.assertEqual(2, diag.main(['--case', case, '--out', str(output)]))
            loader.assert_not_called()
            report = json.loads((output/'diagnostic.json').read_text())
            self.assertIn('NATIVE_WINDOWS_REQUIRED', report['error']['message'])
            self.assertFalse(report['certifies_release'])

    def run_native_wiring_double(self, *, skip=False):
        # This test exercises dispatch, NOT Windows or the actual certifier.
        invoked = []
        class Case(unittest.TestCase):
            def test_keyboard_interrupt_before_first_output(case_self):
                invoked.append('before-output')
                if skip:
                    case_self.skipTest('SYNTHETIC_UNAVAILABLE_ENVIRONMENT')
        support = SimpleNamespace(cert=SimpleNamespace(PROCESS_RECORDS=[]), CertifierTests=Case)
        identity = {'root': str(diag.ROOT), 'sha': 'a'*40, 'tree': 'b'*40, 'status': ''}
        fake_os = SimpleNamespace(name='nt', environ=os.environ, path=os.path, getpid=os.getpid)
        out = self.root/'native-wiring-double'
        with patch.object(diag, 'os', fake_os), patch.object(diag, 'git_identity', return_value=identity), \
             patch.object(diag, 'load_support', return_value=support), \
             patch.object(diag, 'observe', return_value=nullcontext()):
            code = diag.main(['--case', 'before-output', '--out', str(out)])
        return code, invoked, json.loads((out/'diagnostic.json').read_text())

    def test_r2_before_output_dispatches_only_selected_case(self):
        code, invoked, report = self.run_native_wiring_double()
        self.assertEqual(0, code)
        self.assertEqual(['before-output'], invoked)
        self.assertEqual(1, report['test_result']['tests'])
        self.assertFalse(report['certifies_release'])
        self.assertEqual('test_keyboard_interrupt_before_first_output', report['selected_test'])

    def test_r2_skipped_native_case_is_not_success(self):
        code, invoked, report = self.run_native_wiring_double(skip=True)
        self.assertEqual(2, code)
        self.assertEqual(['before-output'], invoked)
        self.assertEqual(1, report['test_result']['skips'])
        self.assertFalse(report['certifies_release'])

    def test_r2_rm_failure_does_not_replace_original_winerror(self):
        cert = self.cert_double()
        original_error = PermissionError(13, 'SYNTHETIC_NATIVE_CODE_FOR_TEST_ONLY')
        original_error.winerror = 32
        def fail(self, *args):
            raise original_error
        with patch.object(cert._ProcessTemporaryDirectory, '__exit__', fail):
            with diag.observe(cert, self.recorder, query_file_users=True):
                temp = cert._ProcessTemporaryDirectory(dir=self.root)
                with patch.object(diag, 'file_users', side_effect=OSError('SYNTHETIC_RM_ERROR')) as query:
                    with self.assertRaises(PermissionError) as raised:
                        with temp:
                            pass
                query.assert_called_once()
                self.assertIs(original_error, raised.exception)
                temp.cleanup()
        events = self.rows()
        observation = next(row['observation'] for row in events if row['event'] == 'post_failure_file_users')
        self.assertEqual('UNOBSERVABLE', observation['status'])

    def test_r2_rm_is_disabled_without_explicit_option(self):
        cert = self.cert_double()
        error = PermissionError(13, 'SYNTHETIC_NATIVE_CODE_FOR_TEST_ONLY')
        error.winerror = 32
        def fail(self, *args):
            raise error
        with patch.object(cert._ProcessTemporaryDirectory, '__exit__', fail):
            with diag.observe(cert, self.recorder):
                temp = cert._ProcessTemporaryDirectory(dir=self.root)
                with patch.object(diag, 'file_users') as query:
                    with self.assertRaises(PermissionError):
                        with temp:
                            pass
                query.assert_not_called()
                temp.cleanup()


if __name__ == '__main__':
    unittest.main()
