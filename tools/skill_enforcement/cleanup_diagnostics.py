#!/usr/bin/env python3
"""Diagnóstico SE08 opt-in; não é certifier nem correção de cleanup.

Executa UM caso por invocação, preservando seu resultado. Os hooks existem só
no processo diagnóstico, não alteram os fontes e não repetem remoções. Consultas
Restart Manager são opcionais, posteriores à falha e não fecham aplicações.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, ExitStack
import ctypes as C
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
FIELDS = ('invocation_id', 'pid', 'launcher_pid', 'result', 'error',
          'observed_exit_code', 'exit_after_cleanup', 'conventional_exit_code',
          'process_cleanup', 'temporary_cleanup', 'cleanup', 'temporary_directory',
          'temporary_directory_exists_after_cleanup', 'temporary_cleanup_exception')


def utc():
    return datetime.now(timezone.utc).isoformat()


def error_info(exc):
    return {'type': type(exc).__name__, 'message': str(exc),
            'errno': getattr(exc, 'errno', None), 'winerror': getattr(exc, 'winerror', None)}


def fs_snapshot(name):
    path = Path(name)
    result = {'directory': str(path), 'lexists': os.path.lexists(path), 'files': {}}
    for filename in ('stdout', 'stderr', 'child.json'):
        try:
            value = (path/filename).lstat()
            result['files'][filename] = {'size': value.st_size, 'mode': value.st_mode,
                                        'device': value.st_dev, 'inode': value.st_ino}
        except FileNotFoundError:
            result['files'][filename] = {'exists': False}
        except OSError as exc:
            result['files'][filename] = {'error': error_info(exc)}
    return result


class Recorder:
    def __init__(self, destination):
        self.path = Path(destination)
        # The caller must have exclusively reserved a new evidence directory.
        with self.path.open('x', encoding='utf-8'):
            pass
        self.sequence = 0
        self.errors = []

    def emit(self, event, **fields):
        self.sequence += 1
        row = {'sequence': self.sequence, 'event': event, 'utc': utc(),
               'monotonic_ns': time.monotonic_ns(), 'observer_pid': os.getpid(), **fields}
        try:
            with self.path.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        except (OSError, ValueError, TypeError) as exc:
            # Never replace the tested exception with an observer error.
            # The final diagnostic MUST be marked incomplete/nonzero.
            self.errors.append(error_info(exc))


class FileTime(C.Structure):
    _fields_ = [('low', C.c_uint32), ('high', C.c_uint32)]


class UniqueProcess(C.Structure):
    _fields_ = [('pid', C.c_uint32), ('started', FileTime)]


class ProcessInfo(C.Structure):
    # Fixed-width Win32 ABI, even when unit-tested on Linux (wchar_t differs).
    _fields_ = [('process', UniqueProcess), ('app', C.c_uint16*256),
                ('service', C.c_uint16*64), ('kind', C.c_int32),
                ('status', C.c_uint32), ('session', C.c_uint32), ('restartable', C.c_int32)]


def _restart_manager_api():
    dll = C.WinDLL('rstrtmgr', use_last_error=True)
    u32 = C.c_uint32
    declarations = {
        'RmStartSession': [C.POINTER(u32), u32, C.c_wchar_p],
        'RmRegisterResources': [u32, u32, C.POINTER(C.c_wchar_p), u32,
                                C.POINTER(UniqueProcess), u32, C.POINTER(C.c_wchar_p)],
        'RmGetList': [u32, C.POINTER(u32), C.POINTER(u32),
                      C.POINTER(ProcessInfo), C.POINTER(u32)],
        'RmEndSession': [u32],
    }
    for name, arguments in declarations.items():
        function = getattr(dll, name)
        function.argtypes, function.restype = arguments, u32
    return dll


def file_users(paths, *, api=None):
    """Uma consulta delimitada; vazio/erro nunca provam ausência de handles.

    Somente paths da invocação própria são passados pelo observador. A sessão
    transitória registra recursos no RM; não chama RmShutdown ou RmRestart.
    """
    if api is None and os.name != 'nt':
        return {'status': 'NOT_APPLICABLE_NON_WINDOWS'}
    values = [str(Path(p)) for p in paths]
    if not values or len(values) > 3:
        return {'status': 'INVALID_TARGET_SET'}
    api = _restart_manager_api() if api is None else api
    session, key = C.c_uint32(), C.create_unicode_buffer(33)
    result = {'status': 'UNOBSERVABLE', 'resource_count': len(values), 'processes': []}
    code = api.RmStartSession(C.byref(session), 0, key)
    result['start_code'] = code
    if code:
        return result
    try:
        names = (C.c_wchar_p*len(values))(*values)
        code = api.RmRegisterResources(session, len(values), names, 0, None, 0, None)
        result['register_code'] = code
        if code:
            return result
        capacity = 256
        buffer = (ProcessInfo*capacity)()
        needed, count, reasons = C.c_uint32(), C.c_uint32(capacity), C.c_uint32()
        code = api.RmGetList(session, C.byref(needed), C.byref(count), buffer, C.byref(reasons))
        result.update(query_code=code, needed=needed.value, returned=count.value,
                      reboot_reasons=reasons.value)
        if code or count.value > capacity:
            # ERROR_MORE_DATA is not an invitation to poll until a convenient list.
            result['status'] = 'INCOMPLETE_QUERY'
            return result
        result['processes'] = [
            {'pid': row.process.pid,
             'start_filetime': (row.process.started.high << 32) | row.process.started.low,
             'application_type': row.kind, 'application_status': row.status}
            for row in buffer[:count.value]
        ]
        result['status'] = ('MATCHES_REPORTED' if result['processes'] else
                            'NO_MATCHES_REPORTED_NOT_PROOF_OF_NO_HANDLES')
        return result
    finally:
        result['end_code'] = api.RmEndSession(session)
        if result['end_code']:
            result['status'] = 'INCOMPLETE_SESSION_END'


class JobPids(C.Structure):
    _fields_ = [('assigned', C.c_uint32), ('count', C.c_uint32), ('pids', C.c_size_t*256)]


def job_snapshot(job):
    if not getattr(job, 'handle', None):
        return {'status': 'NO_OPEN_OWNED_JOB'}
    info = job.accounting()
    ok = job.k.QueryInformationJobObject(job.handle, 1, C.byref(info), C.sizeof(info), None)
    if not ok:
        return {'status': 'UNOBSERVABLE', 'winerror': C.get_last_error()}
    result = {'status': 'OBSERVED', 'active': info.ActiveProcesses,
              'total': info.TotalProcesses, 'terminated': info.TotalTerminatedProcesses}
    pids = JobPids()
    ok = job.k.QueryInformationJobObject(job.handle, 3, C.byref(pids), C.sizeof(pids), None)
    if ok and pids.count <= 256:
        result['pid_list'] = {'status': 'OBSERVED', 'assigned': pids.assigned,
                              'pids': list(pids.pids[:pids.count])}
    else:
        result['pid_list'] = {'status': 'INCOMPLETE', 'assigned': pids.assigned,
                              'winerror': 0 if ok else C.get_last_error()}
    return result


@contextmanager
def observe(cert, recorder, *, query_file_users=False):
    """Hooks efêmeros. Sem detach de finalizer, alteração de timeout ou retry."""
    temporary = cert._ProcessTemporaryDirectory
    original_enter, original_exit = temporary.__enter__, temporary.__exit__
    original_cleanup, original_implicit = temporary.cleanup, temporary._cleanup
    original_persist = cert._persist_process_observation

    def enter(self):
        value = original_enter(self)
        recorder.emit('temporary_enter', path=str(value), snapshot=fs_snapshot(value))
        return value

    def leave(self, *args):
        caller = sys._getframe(1)
        streams = {name: getattr(caller.f_locals.get(name), 'closed', None)
                   for name in ('stdout', 'stderr')}
        del caller
        recorder.emit('temporary_exit_begin', path=self.name, stream_closed_flags=streams,
                      finalizer_alive=self._finalizer.alive, snapshot=fs_snapshot(self.name))
        try:
            value = original_exit(self, *args)
        except BaseException as exc:
            recorder.emit('temporary_exit_error', path=self.name, error=error_info(exc),
                          finalizer_alive=self._finalizer.alive, snapshot=fs_snapshot(self.name))
            if query_file_users and getattr(exc, 'winerror', None) == 32:
                try:
                    users = file_users([Path(self.name)/'stdout', Path(self.name)/'stderr'])
                except Exception as query_error:
                    users = {'status': 'UNOBSERVABLE', 'error': error_info(query_error)}
                recorder.emit('post_failure_file_users', path=self.name, observation=users,
                              warning='Post-failure snapshot; observer may perturb timing.')
            raise
        recorder.emit('temporary_exit_end', path=self.name, snapshot=fs_snapshot(self.name))
        return value

    def explicit(self):
        recorder.emit('explicit_cleanup_begin', path=self.name, finalizer_alive=self._finalizer.alive)
        try:
            return original_cleanup(self)
        finally:
            recorder.emit('explicit_cleanup_end', path=self.name,
                          finalizer_alive=self._finalizer.alive, snapshot=fs_snapshot(self.name))

    def implicit(cls, name, *args, **kwargs):
        recorder.emit('implicit_finalizer_begin', path=name, snapshot=fs_snapshot(name))
        try:
            return original_implicit(name, *args, **kwargs)
        finally:
            recorder.emit('implicit_finalizer_end', path=name, snapshot=fs_snapshot(name))

    def persist(record):
        try:
            return original_persist(record)
        finally:
            recorder.emit('process_record', record={k: record[k] for k in FIELDS if k in record})

    def wrap_job(method, original):
        def wrapped(self, *args, **kwargs):
            try:
                before = job_snapshot(self)
            except Exception as exc:
                before = {'status': 'UNOBSERVABLE', 'error': error_info(exc)}
            recorder.emit('job_' + method + '_begin', accounting=before)
            try:
                return original(self, *args, **kwargs)
            finally:
                try:
                    after = job_snapshot(self)
                except Exception as exc:
                    after = {'status': 'UNOBSERVABLE', 'error': error_info(exc)}
                recorder.emit('job_' + method + '_end', accounting=after)
        return wrapped

    with ExitStack() as stack:
        for name, replacement in (('__enter__', enter), ('__exit__', leave),
                                  ('cleanup', explicit), ('_cleanup', classmethod(implicit))):
            stack.enter_context(patch.object(temporary, name, replacement))
        stack.enter_context(patch.object(cert, '_persist_process_observation', persist))
        if os.name == 'nt':
            for name in ('assign', 'terminate', 'close'):
                stack.enter_context(patch.object(cert._WindowsJob, name,
                                    wrap_job(name, getattr(cert._WindowsJob, name))))
        yield


def git_identity(root):
    result = {}
    for key, args in (('root', ['rev-parse', '--show-toplevel']),
                      ('sha', ['rev-parse', 'HEAD']), ('tree', ['rev-parse', 'HEAD^{tree}']),
                      ('status', ['status', '--porcelain', '--untracked-files=all'])):
        process = subprocess.run(['git', *args], cwd=root, capture_output=True,
                                 text=True, encoding='utf-8', timeout=15, check=True)
        result[key] = process.stdout.strip()
    if Path(result['root']).resolve() != root.resolve():
        raise ValueError('GIT_ROOT_MISMATCH')
    if not all(re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', result[k]) for k in ('sha', 'tree')):
        raise ValueError('GIT_IDENTITY_INVALID')
    if result['status']:
        raise ValueError('WORKTREE_NOT_CLEAN')
    return result


def reserve_output(path, root):
    path = Path(os.path.abspath(path))
    if any(p.is_symlink() or getattr(p, 'is_junction', lambda: False)()
           for p in (path, *path.parents)):
        raise ValueError('EVIDENCE_ALIAS_REJECTED')
    if path == root.resolve() or root.resolve() in path.resolve().parents:
        raise ValueError('EVIDENCE_MUST_BE_EXTERNAL')
    path.mkdir(exist_ok=False)  # Existing empty folders are not reusable evidence.
    return path


def load_support(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def preflight(out):
    result = {'os': platform.platform(), 'python': sys.version, 'executable': sys.executable,
              'base_executable': getattr(sys, '_base_executable', None),
              'pythonpath_present': bool(os.environ.get('PYTHONPATH')), 'symlinks': {}}
    root = out/'symlink-control'
    root.mkdir()
    (root/'target-file').write_text('synthetic\n', encoding='utf-8')
    (root/'target-dir').mkdir()
    for kind in ('file', 'dir'):
        link = root/('link-' + kind)
        try:
            link.symlink_to(root/('target-' + kind), target_is_directory=(kind == 'dir'))
            result['symlinks'][kind] = {'status': 'CREATION_OBSERVED', 'is_symlink': link.is_symlink()}
        except OSError as exc:
            result['symlinks'][kind] = {'status': 'BLOCKED', 'error': error_info(exc)}
        finally:
            if link.is_symlink():
                link.unlink()  # Only our newly created link, never its target.
    result['windows_status'] = 'NATIVE' if os.name == 'nt' else 'NOT_WINDOWS_EVIDENCE'
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, choices=('preflight', 'never-ready', 'storage-finalizer'))
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--restart-manager', action='store_true', help='Consulta opcional após WinError32.')
    args = parser.parse_args(argv)
    before = git_identity(ROOT)
    out = reserve_output(args.out, ROOT)
    recorder = Recorder(out/'events.jsonl')
    summary = {'schema_version': '1.0', 'started_utc': utc(), 'case': args.case,
               'diagnostic_only': True, 'certifies_release': False, 'git_before': before,
               'environment': {'os': platform.platform(), 'python': sys.version, 'executable': sys.executable},
               'sources': {}, 'limitations': ['Hooks may perturb timing and object lifetime.',
               'Absence of WinError32 is NOT a correction certificate.',
               'Restart Manager reports resource users, not exhaustive kernel handles.']}
    sources = [Path(__file__), ROOT/'tools/skill_enforcement/certify_local.py',
               ROOT/'tools/tests/test_certify_local.py', ROOT/'tools/tests/test_certify_storage_cleanup.py']
    for path in sources:
        if path.is_file():
            summary['sources'][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (out/'initial.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    code = 2
    try:
        if args.case == 'preflight':
            summary['preflight'] = preflight(out)
            code = 0 if all(v['status'] == 'CREATION_OBSERVED'
                            for v in summary['preflight']['symlinks'].values()) else 2
        elif args.case == 'never-ready':
            if os.name != 'nt':
                raise ValueError('NATIVE_WINDOWS_REQUIRED_FOR_THIS_PROBE')
            support = load_support(ROOT/'tools/tests/test_certify_local.py', 'se08_diag_support')
            with patch.dict(os.environ, {'SEF_CERTIFIER_TEST_ARTIFACT_DIR': str(out/'fixtures')}):
                with observe(support.cert, recorder, query_file_users=args.restart_manager):
                    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
                        support.CertifierTests('test_never_ready_has_finite_diagnostic_and_cleanup')]))
            summary['test_result'] = {'tests': result.testsRun, 'failures': len(result.failures),
                                      'errors': len(result.errors), 'skips': len(result.skipped)}
            code = 0 if result.wasSuccessful() else 1
            (out/'processes.json').write_text(json.dumps(support.cert.PROCESS_RECORDS, indent=2), encoding='utf-8')
        else:
            storage = load_support(ROOT/'tools/tests/test_certify_storage_cleanup.py', 'se08_diag_storage')
            fixture = out/'synthetic-repo'
            fixture.mkdir()
            storage.support.git(fixture, 'init', '-q')
            storage.support.git(fixture, '-c', 'user.name=Synthetic', '-c',
                                'user.email=synthetic@example.invalid', 'commit', '--allow-empty', '-qm', 'fixture')
            case = out/'storage-case'
            case.mkdir()
            with observe(storage.cert, recorder):
                try:
                    storage.cli_probe('keyboard', 'gate', str(fixture), str(case), 'before_removal')
                except SystemExit as exc:
                    # Preserve the probe's external convention (usually 130), not PASS.
                    code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
            summary['probe_exit'] = code
    except Exception as exc:
        summary['error'] = error_info(exc)
        code = 2
    finally:
        try:
            after = git_identity(ROOT)
            summary['git_after'] = after
            if before != after:
                summary['identity_error'] = 'IDENTITY_CHANGED'
                code = 2
        except Exception as exc:
            summary['identity_error'] = error_info(exc)
            code = 2
        summary['observer_errors'] = recorder.errors
        if recorder.errors:
            code = 2
        summary.update(ended_utc=utc(), exit_code=code,
                       status='DIAGNOSTIC_ONLY_NOT_RELEASE_CERTIFICATION')
        (out/'diagnostic.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
