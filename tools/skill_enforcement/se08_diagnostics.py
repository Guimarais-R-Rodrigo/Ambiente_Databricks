"""Diagnóstico SE08 opt-in; nunca certifica release nem altera o certifier.

Casos Windows devem ser observados no Windows. Os hooks podem alterar timing.
Restart Manager consulta usuários dos arquivos; lista vazia não prova ausência
histórica de handles. Nenhuma API de shutdown/restart ou encerramento de processo
é chamada pelo observador. Os próprios testes mantêm seu cleanup original.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import gc
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
KEYS = ('result', 'cleanup', 'process_cleanup', 'temporary_cleanup', 'pid',
        'launcher_pid', 'observed_exit_code', 'exit_after_cleanup',
        'temporary_directory_exists_after_cleanup')


def utc():
    return datetime.now(timezone.utc).isoformat()


def record_fields(record):
    # Copiar apenas escalares; não reter objeto TemporaryDirectory ou traceback.
    return {k: record.get(k) for k in KEYS
            if record.get(k) is None or isinstance(record.get(k), (str, int, bool, float))}


def exception_fields(exc):
    return {'type': type(exc).__name__, 'message': str(exc),
            'errno': getattr(exc, 'errno', None), 'winerror': getattr(exc, 'winerror', None),
            'filename': getattr(exc, 'filename', None)}


def resource_users(files):
    """Consulta restrita aos FILEs informados; não usa nomes de apps no relatório."""
    if os.name != 'nt':
        return {'status': 'NOT_WINDOWS', 'users': [], 'absence_proven': False}
    import ctypes as c
    from ctypes import wintypes as w

    class UniqueProcess(c.Structure):
        _fields_ = [('pid', w.DWORD), ('started', w.FILETIME)]

    class ProcessInfo(c.Structure):
        _fields_ = [('process', UniqueProcess), ('app_name', w.WCHAR * 256),
                    ('service_name', w.WCHAR * 64), ('app_type', c.c_int),
                    ('app_status', w.ULONG), ('session_id', w.DWORD),
                    ('restartable', w.BOOL)]

    paths = [str(Path(p).resolve(strict=True)) for p in files]
    if not paths or len(paths) > 3 or any(not Path(p).is_file() for p in paths):
        return {'status': 'INVALID_RESOURCES', 'users': [], 'absence_proven': False}
    api = c.WinDLL('Rstrtmgr.dll')
    signatures = {
        'RmStartSession': [c.POINTER(w.DWORD), w.DWORD, w.LPWSTR],
        'RmRegisterResources': [w.DWORD, w.UINT, c.POINTER(w.LPCWSTR), w.UINT,
                                c.POINTER(UniqueProcess), w.UINT, c.POINTER(w.LPCWSTR)],
        'RmGetList': [w.DWORD, c.POINTER(w.UINT), c.POINTER(w.UINT),
                      c.POINTER(ProcessInfo), c.POINTER(w.DWORD)],
        'RmEndSession': [w.DWORD],
    }
    for name, args in signatures.items():
        fn = getattr(api, name); fn.argtypes = args; fn.restype = w.DWORD
    handle = w.DWORD(); key = c.create_unicode_buffer(33)
    result = {'status': 'QUERY_ERROR', 'users': [], 'absence_proven': False,
              'resources': paths, 'calls': [], 'scope': 'RESTART_MANAGER_SNAPSHOT'}
    rc = api.RmStartSession(c.byref(handle), 0, key)
    result['calls'].append({'api': 'RmStartSession', 'code': int(rc)})
    if rc:
        return result
    try:
        array = (w.LPCWSTR * len(paths))(*paths)
        rc = api.RmRegisterResources(handle, len(paths), array, 0, None, 0, None)
        result['calls'].append({'api': 'RmRegisterResources', 'code': int(rc)})
        if rc:
            return result
        needed, count, reasons = w.UINT(), w.UINT(), w.DWORD()
        rc = api.RmGetList(handle, c.byref(needed), c.byref(count), None, c.byref(reasons))
        result['calls'].append({'api': 'RmGetList.size', 'code': int(rc), 'needed': needed.value})
        if rc == 0 and needed.value == 0:
            result['status'] = 'QUERY_OK_NO_USERS_RETURNED'
            return result
        if rc != 234 or not 0 < needed.value <= 4096:
            return result
        capacity = needed.value; count.value = capacity
        users = (ProcessInfo * capacity)()
        rc = api.RmGetList(handle, c.byref(needed), c.byref(count), users, c.byref(reasons))
        result['calls'].append({'api': 'RmGetList.data', 'code': int(rc), 'count': count.value})
        if rc or count.value > capacity:
            result['status'] = 'QUERY_CHANGED_OR_FAILED'
            return result  # Sem loop até obter uma lista favorável.
        result['users'] = [{'pid': p.process.pid,
                            'creation_filetime': (p.process.started.dwHighDateTime << 32) |
                                                  p.process.started.dwLowDateTime,
                            'session_id': p.session_id, 'app_type': p.app_type}
                           for p in users[:count.value]]
        result['status'] = 'QUERY_OK'
        return result
    finally:
        rc = api.RmEndSession(handle)
        result['session_end_code'] = int(rc)
        if rc:
            result['status'] = 'SESSION_END_FAILED'


class Journal:
    def __init__(self, file):
        self.stream = Path(file).open('x', encoding='utf-8', newline='\n')
        self.events = 0
        self.errors = []

    def emit(self, event, **fields):
        try:
            data = dict(event=event, utc=utc(), monotonic=time.monotonic(),
                        observer_pid=os.getpid(), **fields)
            self.stream.write(json.dumps(data, ensure_ascii=True) + '\n')
            self.stream.flush()
            self.events += 1
        except (OSError, ValueError, TypeError) as exc:
            self.errors.append(exception_fields(exc))
            # Instrumentação não pode mascarar a exceção/exit do caso observado.

    def close(self):
        self.stream.close()


class CleanupObserver:
    def __init__(self, cert, journal, *, query_owners=False, case='unknown'):
        self.cert, self.journal = cert, journal
        self.query_owners, self.case = query_owners, case
        self.stack = ExitStack()

    def __enter__(self):
        td = tempfile.TemporaryDirectory
        explicit = td.cleanup
        finalizer = td.__dict__['_cleanup'].__func__
        original_exit = self.cert._ProcessTemporaryDirectory.__exit__
        journal = self.journal

        def relevant(name):
            return Path(name).name.startswith('sef-process-')

        def cleanup(obj):
            if relevant(obj.name):
                journal.emit('EXPLICIT_CLEANUP_ENTER', directory=obj.name)
            try:
                return explicit(obj)
            finally:
                if relevant(obj.name):
                    journal.emit('EXPLICIT_CLEANUP_EXIT', directory=obj.name,
                                 exists=os.path.lexists(obj.name))

        def automatic(cls, name, *args, **kwargs):
            if relevant(name):
                journal.emit('AUTOMATIC_FINALIZER_ENTER', directory=name)
            try:
                return finalizer(cls, name, *args, **kwargs)
            finally:
                if relevant(name):
                    journal.emit('AUTOMATIC_FINALIZER_EXIT', directory=name,
                                 exists=os.path.lexists(name))

        def observed_exit(obj, *args):
            name = str(obj.name)
            journal.emit('PROCESS_TEMP_EXIT_ENTER', directory=name,
                         finalizer_alive=getattr(getattr(obj, '_finalizer', None), 'alive', None),
                         record=record_fields(obj.record))
            try:
                return original_exit(obj, *args)
            except OSError as exc:
                journal.emit('PROCESS_TEMP_EXIT_ERROR', directory=name,
                             exception=exception_fields(exc), record=record_fields(obj.record))
                if self.query_owners and getattr(exc, 'winerror', None) == 32:
                    if self.case == 'storage-residue':
                        journal.emit('RESOURCE_USERS_NOT_QUERIED', reason='DECLARED_SYNTHETIC_FAULT')
                    else:
                        try:
                            target = Path(exc.filename).resolve(strict=True)
                            if target.parent != Path(name).resolve() or target.name not in ('stdout', 'stderr', 'child.json'):
                                raise ValueError('arquivo fora da pasta temporária observada')
                            users = resource_users([target])
                        except Exception as diagnostic_error:  # Falha do observador não mascara a original.
                            users = {'status': 'NOT_OBSERVABLE', 'error': exception_fields(diagnostic_error)}
                        journal.emit('RESOURCE_USERS_AFTER_FAILURE', result=users)
                raise
            finally:
                journal.emit('PROCESS_TEMP_EXIT_FINALLY', directory=name,
                             exists=os.path.lexists(name), record=record_fields(obj.record))

        self.stack.enter_context(patch.object(td, 'cleanup', cleanup))
        self.stack.enter_context(patch.object(td, '_cleanup', classmethod(automatic)))
        self.stack.enter_context(patch.object(self.cert._ProcessTemporaryDirectory, '__exit__', observed_exit))
        return self

    def __exit__(self, *args):
        return self.stack.__exit__(*args)


def git_identity(root):
    def run(*args):
        p = subprocess.run(['git', *args], cwd=root, capture_output=True, timeout=15, check=True)
        return p.stdout.decode('utf-8').strip()
    return {'head': run('rev-parse', 'HEAD'), 'tree': run('rev-parse', 'HEAD^{tree}'),
            'status': run('status', '--porcelain', '--untracked-files=all'),
            'shallow': run('rev-parse', '--is-shallow-repository')}


def reserve_output(value, root):
    path = Path(value).absolute()
    for parent in (path, *path.parents):
        junction = getattr(parent, 'is_junction', lambda: False)()
        if parent.is_symlink() or junction:
            raise ValueError('destino não pode passar por symlink/junction')
    path = path.resolve()
    if path == root.resolve() or root.resolve() in path.parents:
        raise ValueError('evidência deve ficar fora do repositório')
    path.mkdir(parents=False, exist_ok=False)
    return path


def load_case(file):
    name = 'se08_diagnostic_' + file.stem
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def capabilities(directory):
    target = directory / 'target'; target.mkdir()
    (target / 'file').write_bytes(b'synthetic')
    result = {'python': sys.version, 'executable': sys.executable,
              'base_executable': getattr(sys, '_base_executable', None),
              'venv': sys.prefix != sys.base_prefix,
              'pythonpath_present': bool(os.environ.get('PYTHONPATH')),
              'platform': platform.platform(), 'symlinks': []}
    for is_dir in (False, True):
        link = directory / ('dir-link' if is_dir else 'file-link')
        try:
            link.symlink_to(target if is_dir else target / 'file', target_is_directory=is_dir)
            result['symlinks'].append({'directory': is_dir, 'status': 'CREATED',
                                       'is_symlink': link.is_symlink()})
        except OSError as exc:
            result['symlinks'].append({'directory': is_dir, 'status': 'UNAVAILABLE',
                                       'exception': exception_fields(exc)})
        finally:
            if link.is_symlink():
                link.unlink()
    result['test_skips_added'] = False
    result['privileges_changed'] = False
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=('f04-never-ready', 'storage-residue', 'capabilities'), required=True)
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--evidence-dir', required=True)
    parser.add_argument('--query-resource-users', action='store_true',
                        help='Consulta Restart Manager após WinError32; sem shutdown/restart.')
    args = parser.parse_args(argv)
    before = git_identity(ROOT)
    if not re.fullmatch('[0-9a-f]{40}', args.expected_sha) or before['head'] != args.expected_sha or before['status']:
        parser.error('SHA divergente ou worktree suja; nenhum caso executado')
    directory = reserve_output(args.evidence_dir, ROOT)
    journal = Journal(directory / 'events.jsonl')
    summary = {'scope': 'DIAGNOSTIC_NOT_CERTIFICATION', 'case': args.case,
               'before': before, 'python': sys.version, 'platform': platform.platform(),
               'release_certified': False, 'case_exit': None, 'instrumentation_changes_timing': True}
    code = 2
    try:
        if args.case == 'capabilities':
            summary['capabilities'] = capabilities(directory)
            code = 0 if all(x['status'] == 'CREATED' for x in summary['capabilities']['symlinks']) else 1
        else:
            file = ROOT / 'tools/tests' / ('test_certify_local.py' if args.case == 'f04-never-ready' else 'test_certify_storage_cleanup.py')
            case = load_case(file)
            with CleanupObserver(case.cert, journal, query_owners=args.query_resource_users, case=args.case):
                if args.case == 'f04-never-ready':
                    with patch.dict(os.environ, {'SEF_CERTIFIER_TEST_ARTIFACT_DIR': str(directory / 'fixtures')}):
                        suite = unittest.TestSuite([case.CertifierTests('test_never_ready_has_finite_diagnostic_and_cleanup')])
                        result = unittest.TextTestRunner(verbosity=2).run(suite)
                        summary['tests'] = {'run': result.testsRun, 'failures': len(result.failures),
                                            'errors': len(result.errors), 'skips': len(result.skipped)}
                        code = 0 if result.wasSuccessful() else 1
                else:
                    # Diagnóstico do mesmo probe interno, não recertificação do método externo.
                    root = directory / 'synthetic-repo'; root.mkdir()
                    case.support.git(root, 'init', '-q')
                    case.support.git(root, '-c', 'user.name=Synthetic', '-c',
                                     'user.email=synthetic@example.invalid', 'commit', '--allow-empty', '-qm', 'fixture')
                    output = directory / 'probe'; output.mkdir()
                    try:
                        case.cli_probe('keyboard', 'gate', str(root), str(output), 'before_removal')
                    except SystemExit as exc:
                        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
                    summary['scope'] = 'DIRECT_STORAGE_FIXTURE_DIAGNOSTIC_NOT_TEST_CERTIFICATION'
                summary['case_exit'] = code
                journal.emit('CASE_RETURNED', case_exit=code)
                # Marca explicitamente esta observação adicional: não antecede o oráculo original.
                journal.emit('POST_CASE_GC_REQUESTED')
                gc.collect()
    finally:
        summary['case_exit'] = code
        try:
            summary['after'] = git_identity(ROOT)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            summary['after_error'] = exception_fields(exc)
        summary['journal_errors'] = journal.errors
        summary['journal_events'] = journal.events
        summary['identity_stable'] = summary.get('after') == before
        degraded = bool(journal.errors) or not summary['identity_stable']
        summary['observation_status'] = 'DEGRADED' if degraded else 'RECORDED'
        summary['wrapper_exit'] = code if code or not degraded else 2
        journal.close()
        (directory / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary['wrapper_exit']


if __name__ == '__main__':
    raise SystemExit(main())
