"""Valida configuração local e planeja caminhos; não realiza operações remotas."""
from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit


class ConfigError(ValueError):
    """Configuração incompleta ou destino inseguro."""


FIELDS = {'schema_version', 'profile', 'expected_host', 'development_root', 'installation_root'}


def host(value: str) -> str:
    if not isinstance(value, str):
        raise ConfigError('HOST_INVALID')
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise ConfigError('HOST_INVALID') from exc
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or
            parsed.password or parsed.path not in ('', '/') or parsed.query or
            parsed.fragment or port not in (None, 443) or
            not re.fullmatch(r'[a-zA-Z0-9.-]+', parsed.hostname) or
            parsed.hostname.endswith('.invalid')):
        raise ConfigError('HOST_INVALID_OR_EXAMPLE')
    return 'https://' + parsed.hostname.lower()


def personal_path(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or '\\' in value or any(ord(c) < 32 for c in value):
        raise ConfigError('PATH_INVALID')
    path = PurePosixPath(value)
    if (not path.is_absolute() or str(path) != value or '..' in path.parts or
            len(path.parts) < 4 or path.parts[1] != 'Users' or
            any('EXEMPLO' in part.upper() or 'PREENCHER' in part.upper() for part in path.parts)):
        raise ConfigError('PERSONAL_ROOT_REQUIRED')
    return path


def validate(data: dict) -> dict:
    if not isinstance(data, dict) or set(data) != FIELDS or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ConfigError('CONFIG_SCHEMA')
    profile = data['profile']
    if not isinstance(profile, str) or not re.fullmatch(r'[\w.-]+', profile) or 'PREENCHER' in profile.upper():
        raise ConfigError('PROFILE_REQUIRED')
    expected = host(data['expected_host'])
    development = personal_path(data['development_root'])
    installation = personal_path(data['installation_root'])
    if development.is_relative_to(installation) or installation.is_relative_to(development):
        raise ConfigError('ROOTS_OVERLAP')
    if development.parts[2] != installation.parts[2]:
        raise ConfigError('PERSONAL_OWNER_MISMATCH')
    return dict(data, expected_host=expected)


def load(root: Path, profiles: Path | None = None) -> dict:
    relative = 'config/workspace.local.json'
    path = root / relative
    if any(p.is_symlink() or getattr(p, 'is_junction', lambda: False)()
           for p in (path, path.parent)):
        raise ConfigError('CONFIG_SYMLINK')
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', relative], cwd=root, capture_output=True)
    ignored = subprocess.run(['git', 'check-ignore', '-q', '--', relative], cwd=root, capture_output=True)
    if tracked.returncode != 1 or ignored.returncode != 0:
        raise ConfigError('CONFIG_MUST_BE_IGNORED_AND_UNTRACKED')
    try:
        data = validate(json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_fields))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError('CONFIG_MISSING_OR_INVALID; consulte config/README.md') from exc
    native = configparser.ConfigParser(interpolation=None)
    try:
        with (profiles or Path(os.environ.get('DATABRICKS_CONFIG_FILE', str(Path.home() / '.databrickscfg')))).open(encoding='utf-8') as stream:
            native.read_file(stream)
        actual = native.get(data['profile'], 'host')
    except (OSError, configparser.Error) as exc:
        raise ConfigError('NATIVE_PROFILE_MISSING_OR_INVALID') from exc
    if host(actual) != data['expected_host']:
        raise ConfigError('PROFILE_HOST_MISMATCH')
    override = os.environ.get('DATABRICKS_HOST')
    if override and host(override) != data['expected_host']:
        raise ConfigError('ENV_HOST_MISMATCH')
    return data


def unique_fields(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError('CONFIG_DUPLICATE_FIELD')
        result[key] = value
    return result


def plan(root: Path, data: dict, show_paths: bool = False) -> dict:
    source = root / 'ambiente_databricks'
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from simulado import inventory
    items = inventory(source, source=True)
    files = []
    for relative, item in sorted(items.items()):
        if item['object_type'] == 'DIRECTORY':
            continue
        record = {'source': 'ambiente_databricks/' + relative,
                  'object_type': item['object_type'],
                  'sha256': hashlib.sha256((source / relative).read_bytes()).hexdigest()}
        if show_paths:
            record['destination'] = data['installation_root'] + '/' + relative
        files.append(record)
    if not files:
        raise ConfigError('EMPTY_PAYLOAD')
    sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    dirty = bool(subprocess.run(['git', 'status', '--porcelain'], cwd=root, capture_output=True, text=True, check=True).stdout)
    result = {'status': 'PASS', 'scope': 'local plan only; remote NOT_RUN',
              'base_sha': sha, 'working_tree_dirty': dirty, 'files': files,
              'next': 'validate source, review release, then follow authorized backup/staging runbook'}
    if show_paths:
        result['development_root'] = data['development_root']
        result['installation_root'] = data['installation_root']
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--check', action='store_true')
    action.add_argument('--plan', action='store_true')
    parser.add_argument('--show-paths', action='store_true')
    args = parser.parse_args()
    try:
        root = Path(__file__).resolve().parents[2]
        data = load(root)
        result = plan(root, data, args.show_paths) if args.plan else {'status': 'PASS', 'scope': 'local config/profile host only; authentication and remote NOT_RUN'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('FAIL ' + (str(exc) if isinstance(exc, ConfigError) else 'LOCAL_READ_FAILED'))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
