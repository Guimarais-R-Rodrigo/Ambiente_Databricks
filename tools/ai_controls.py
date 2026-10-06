"""Offline maintainer instruction contracts. No network, models, settings or installs.

--check is read-only. --generate writes only owned .claude/skills adapters.
--release enforces source-review freshness, not native-client certification.
--migration-freeze checks this campaign's immutable baseline; do not use this
flag as a permanent veto on future authorized product changes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

VERSION = '1.0.0'
SKILLS = ('forward-test-skills', 'publicar-free', 'render-simulado', 'replicar-trabalho', 'validar-assistant')
MAP = 'docs/ai/control-map.json'
REGISTRY = 'docs/ai/standards/registry.json'
BASELINE = 'docs/auditoria/2026-10-06_ai-instrucoes/baseline.json'
BASELINE_SHA256 = '9354ac85c5441dca40a59d5d8b73457895d200d685fb25cbd4ecfe9a93378fda'
MANIFEST = '.claude/skills/.generated.json'
EVIDENCE_DATA = {MAP, BASELINE, 'docs/auditoria/2026-10-06_ai-instrucoes/source-controls.json', 'docs/auditoria/2026-10-06_ai-instrucoes/traceability.json', 'docs/auditoria/2026-10-06_ai-instrucoes/reference-scan.json', 'docs/auditoria/2026-10-06_ai-instrucoes/traceability.csv'}
LEGACY = re.compile(r'\.claude/(?:CLAUDE\.md|rules/[\w.-]+\.md|context/[\w.-]+\.md|templates/[\w.-]+\.md|skills/README\.md)')
LINK = re.compile(r'\[[^\]\n]+\]\(([^\s)]+)(?:\s+"[^"]*")?\)')

class ContractError(ValueError):
    pass

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ContractError(f'JSON_MISSING_OR_INVALID: {path.name}: {exc}') from exc

def safe(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if not relative or rel.is_absolute() or '..' in rel.parts or '\\' in relative or str(rel) != relative:
        raise ContractError(f'UNSAFE_PATH: {relative}')
    candidate = root
    for part in rel.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ContractError(f'SYMLINK: {relative}')
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ContractError(f'OUTSIDE_ROOT: {relative}')
    return candidate

def inventory(root: Path) -> list[str]:
    results = []
    for args in (['--cached'], ['--others', '--exclude-standard']):
        proc = subprocess.run(['git', 'ls-files', '-z', *args], cwd=root, capture_output=True)
        if proc.returncode:
            raise ContractError('GIT_INVENTORY_FAILED')
        results.append([p.decode('utf-8') for p in proc.stdout.split(b'\0') if p])
    if not results[0]:
        raise ContractError('GIT_INVENTORY_EMPTY')
    return sorted({p for group in results for p in group if safe(root, p).is_file()})

def validate_skill_bytes(data: bytes, name: str, path: str) -> None:
    """Validate explicit UTF-8/LF two-string YAML subset, including folded scalars."""
    if b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
        raise ContractError(f'SKILL_ENCODING: {path}')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ContractError(f'SKILL_ENCODING: {path}') from exc
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise ContractError(f'FRONTMATTER: {path}')
    pairs = {}
    lines = match[1].splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        entry = re.fullmatch(r'([a-z][a-z-]*):[ ]*(.*)', line)
        if not entry:
            raise ContractError(f'FRONTMATTER: {path}')
        key, value = entry.groups()
        if key in pairs:
            raise ContractError(f'FRONTMATTER_DUPLICATE_KEY: {path}')
        index += 1
        if value in ('>-', '>', '|-', '|'):
            block = []
            while index < len(lines) and lines[index].startswith('  '):
                block.append(lines[index][2:])
                index += 1
            if not block:
                raise ContractError(f'FRONTMATTER_SCALAR: {path}')
            value = (' ' if value.startswith('>') else '\n').join(block)
        elif value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError as exc:
                raise ContractError(f'FRONTMATTER_SCALAR: {path}') from exc
        elif value.startswith("'"):
            if not value.endswith("'") or len(value) < 2 or "'" in value[1:-1].replace("''", ''):
                raise ContractError(f'FRONTMATTER_SCALAR: {path}')
            value = value[1:-1].replace("''", "'")
        elif value and (value[0] in '[]{}&*!|>@`%' or ': ' in value or ' #' in value or value.lower() in ('true', 'false', 'null', '~', 'yes', 'no', 'on', 'off', '.nan', '.inf', '-.inf') or re.fullmatch(r'[+-]?(?:[0-9][0-9_]*(?:\.[0-9_]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?|0[xob][0-9a-fA-F_]+', value)):
            raise ContractError(f'FRONTMATTER_SCALAR: {path}')
        if not isinstance(value, str):
            raise ContractError(f'FRONTMATTER_SCALAR: {path}')
        pairs[key] = value
    if pairs.get('name') != name or not pairs.get('description', '').strip() or set(pairs) != {'name', 'description'}:
        raise ContractError(f'SKILL_METADATA: {path}')
    if len(pairs['description']) > 1024:
        raise ContractError(f'SKILL_DESCRIPTION_BUDGET: {path}')

def frontmatter(path: Path, name: str) -> None:
    validate_skill_bytes(path.read_bytes(), name, str(path))

def expected_outputs(root: Path, control: dict) -> tuple[dict[str, bytes], dict]:
    adapters = control.get('adapters', [])
    allowed = {f'.agents/skills/{n}': f'.claude/skills/{n}' for n in SKILLS}
    if len(adapters) != len(SKILLS) or {a.get('source'): a.get('destination') for a in adapters} != allowed:
        raise ContractError('ADAPTER_INVENTORY: exactly five allowlisted mappings required')
    actual = {p.name for p in (root / '.agents/skills').iterdir() if p.is_dir() or p.is_symlink()}
    if actual != set(SKILLS):
        raise ContractError('SKILL_INVENTORY: exactly five canonical skills required')
    output, entries = {}, []
    for adapter in sorted(adapters, key=lambda x: x['source']):
        src, dst = adapter['source'], adapter['destination']
        base = safe(root, src)
        if not base.is_dir():
            raise ContractError(f'SKILL_MISSING: {src}')
        frontmatter(safe(root, src + '/SKILL.md'), base.name)
        sources = sorted(p for p in base.rglob('*') if p.is_file() or p.is_symlink())
        if not sources:
            raise ContractError(f'EMPTY_SOURCE: {src}')
        for file in sources:
            relative = file.relative_to(base).as_posix()
            source = src + '/' + relative
            target = dst + '/' + relative
            data = safe(root, source).read_bytes()
            safe(root, target)
            if relative == 'SKILL.md':
                end = data.find(b'\n---\n', 4) + 5
                header = f'\n<!-- GENERATED by tools/ai_controls.py v{VERSION}; source={source}; sha256={digest(data)}; transform=identity-body -->\n'.encode()
                data = data[:end] + header + data[end:]
                validate_skill_bytes(data, base.name, target)
            output[target] = data
            entries.append({'source': source, 'destination': target, 'source_sha256': digest(file.read_bytes()), 'output_sha256': digest(data), 'transform': 'frontmatter-preserved provenance comment' if relative == 'SKILL.md' else 'identity-bytes'})
    manifest = {'generator': 'tools/ai_controls.py', 'version': VERSION, 'entries': entries}
    output[MANIFEST] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    return output, manifest

def verify_ownership(root: Path, output: dict[str, bytes], control: dict) -> None:
    old_path = safe(root, MANIFEST)
    old = read_json(old_path) if old_path.exists() else None
    managed = {e['destination']: e['output_sha256'] for e in old.get('entries', [])} if old else control.get('adopted_outputs', {})
    if old:
        if old.get('generator') != 'tools/ai_controls.py' or not old.get('entries'):
            raise ContractError('OWNERSHIP_MANIFEST_INVALID')
        managed[MANIFEST] = digest(old_path.read_bytes())
    derived_root = safe(root, '.claude/skills')
    if derived_root.exists():
        extra_dirs = {p.name for p in derived_root.iterdir() if p.is_dir()} - set(SKILLS)
        if extra_dirs:
            raise ContractError('DERIVED_SKILL_INVENTORY')
    for name in SKILLS:
        target_dir = safe(root, '.claude/skills/' + name)
        if target_dir.exists():
            for file in target_dir.rglob('*'):
                relative = file.relative_to(root).as_posix()
                safe(root, relative)
                if file.is_file() and relative not in output:
                    raise ContractError(f'UNMANAGED_EXTRA: {relative}')
    for relative in output:
        path = safe(root, relative)
        if path.exists() and (not path.is_file() or managed.get(relative) != digest(path.read_bytes())):
            raise ContractError(f'UNMANAGED_OR_EDITED: {relative}')

def generate(root: Path) -> list[str]:
    control = read_json(safe(root, MAP))
    output, _ = expected_outputs(root, control)
    verify_ownership(root, output, control)  # All checks before first write.
    changed = []
    for relative, data in output.items():
        path = safe(root, relative)
        if not path.exists() or path.read_bytes() != data:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            changed.append(relative)
    return changed

def slug(title: str) -> str:
    return re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')

def anchors(text: str) -> set[str]:
    result, counts = set(), {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        base = slug(title)
        index = counts.get(base, 0)
        result.add(base + (f'-{index}' if index else ''))
        counts[base] = index + 1
    result.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    return result

def check_link(root: Path, origin: str, raw: str) -> None:
    if raw.startswith(('http:', 'https:', 'mailto:', 'data:')) or '<' in raw:
        return
    target, _, fragment = unquote(raw).partition('#')
    if target.startswith('/') or '\\' in target:
        raise ContractError(f'LINK_OUTSIDE_ROOT: {origin} -> {raw}')
    # Normalize lexical components without realpath/case canonicalization.
    parts = list(PurePosixPath(origin).parent.parts) if target else []
    for part in (PurePosixPath(target).parts if target else PurePosixPath(origin).parts):
        if part == '..':
            if not parts:
                raise ContractError(f'LINK_OUTSIDE_ROOT: {origin} -> {raw}')
            parts.pop()
        elif part != '.':
            parts.append(part)
    requested = '/'.join(parts)
    part_path = root
    for part in parts:
        if not part_path.is_dir():
            raise ContractError(f'LINK_MISSING: {origin} -> {raw}')
        names = {p.name for p in part_path.iterdir()}
        if part not in names:
            cause = 'LINK_CASE' if part.casefold() in {n.casefold() for n in names} else 'LINK_MISSING'
            raise ContractError(f'{cause}: {origin} -> {raw}')
        part_path /= part
    resolved = safe(root, requested)
    if not resolved.exists():
        raise ContractError(f'LINK_MISSING: {origin} -> {raw}')
    if fragment and resolved.is_file() and resolved.suffix.lower() == '.md':
        if fragment not in anchors(resolved.read_text(encoding='utf-8')):
            raise ContractError(f'ANCHOR_MISSING: {origin} -> {raw}')

def check_registry(root: Path, release: bool, today: dt.date) -> list[str]:
    registry = read_json(safe(root, REGISTRY))
    claims = registry.get('claims', [])
    if not claims:
        raise ContractError('CLAIMS_EMPTY')
    warnings, ids = [], set()
    for claim in claims:
        cid = claim.get('id')
        if not cid or cid in ids:
            raise ContractError('CLAIM_ID_INVALID')
        ids.add(cid)
        required = ('provider', 'product', 'surface', 'url', 'reviewed_at_utc', 'documented_version', 'installed_version', 'scope', 'kind', 'paraphrase', 'snapshot', 'snapshot_sha256', 'test_ids', 'owner', 'state')
        if any(k not in claim or claim[k] in ('', None, []) for k in required):
            raise ContractError(f'CLAIM_INCOMPLETE: {cid}')
        if not claim['url'].startswith('https://') or claim['state'] not in ('DOCUMENTED', 'OBSERVED', 'SUPPORTED'):
            raise ContractError(f'CLAIM_INVALID: {cid}')
        snapshot = safe(root, claim['snapshot'])
        if digest(snapshot.read_bytes()) != claim['snapshot_sha256']:
            raise ContractError(f'SNAPSHOT_HASH: {cid}')
        reviewed = dt.datetime.fromisoformat(claim['reviewed_at_utc'].replace('Z', '+00:00'))
        source = read_json(snapshot)
        if source.get('reviewed_at_utc') != claim['reviewed_at_utc'] or source.get('url') != claim['url'] or source.get('id') != cid:
            raise ContractError(f'REVIEW_BINDING: {cid}')
        age = (today - reviewed.date()).days
        if age < 0:
            raise ContractError(f'REVIEW_FUTURE: {cid}')
        if age > registry.get('stale_after_days', 30):
            if release:
                raise ContractError(f'CLAIM_STALE: {cid}')
            warnings.append(f'STALE: {cid}; current support claim requires official review')
        if claim['state'] == 'SUPPORTED' and not claim.get('observed_evidence'):
            raise ContractError(f'SUPPORT_WITHOUT_EVIDENCE: {cid}')
        if claim['state'] != 'DOCUMENTED':
            raise ContractError(f'PROMOTION_REQUIRES_VALIDATED_EVIDENCE_FORMAT: {cid}')
    return warnings

def check(root: Path, *, release: bool = False, migration_freeze: bool = False, today: dt.date | None = None) -> dict:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    paths = inventory(root)
    control = read_json(safe(root, MAP))
    output, manifest = expected_outputs(root, control)
    verify_ownership(root, output, control)
    for relative, data in output.items():
        path = safe(root, relative)
        if not path.is_file() or path.read_bytes() != data:
            raise ContractError(f'ADAPTER_DRIFT: {relative}')
    core_data = safe(root, 'AGENTS.md').read_bytes()
    if b'\r' in core_data or core_data.startswith(b'\xef\xbb\xbf'):
        raise ContractError('CORE_ENCODING')
    core = core_data.decode('utf-8')
    if len(core.splitlines()) > 150 or len(core.encode()) > 12288:
        raise ContractError('CORE_BUDGET')
    if '\r' in core or core.startswith('\ufeff'):
        raise ContractError('CORE_ENCODING')
    for needle in control.get('critical_invariants', []):
        if needle not in core:
            raise ContractError(f'CORE_INVARIANT_MISSING: {needle}')
    if not control.get('critical_invariants'):
        raise ContractError('CORE_INVARIANTS_EMPTY')
    if re.search(r'^\s*@|@[^\s`<>]*\.md\b', core, re.M):
        raise ContractError('CORE_IMPORT_NOT_PORTABLE')
    if re.search(r'(?:antes de (?:qualquer|toda)|sempre leia|leia sempre|obrigat[oó]ri[oa]|always read|before (?:every|any)).{0,150}(?:CHANGELOG|docs/sprints|docs/auditoria)', ' '.join(core.split()), re.I):
        raise ContractError('UNIVERSAL_HISTORY')
    if safe(root, 'CLAUDE.md').read_text() != '@AGENTS.md\n' or safe(root, 'GEMINI.md').read_text() != '@./AGENTS.md\n':
        raise ContractError('BOOTSTRAP_CONTRACT')
    for relative in control['retired_sources']:
        if (root / relative).exists():
            raise ContractError(f'LEGACY_LOADER_PRESENT: {relative}')
    requirements = control.get('requirements', [])
    covered = {r.get('control_id') for r in requirements}
    if covered != {f'C{i:02}' for i in range(1, 23)}:
        raise ContractError('REQUIREMENT_COVERAGE')
    for req in requirements:
        if any(not req.get(k) for k in ('id', 'source', 'obligation', 'target', 'load_condition', 'test_ids', 'disposition')):
            raise ContractError('REQUIREMENT_INCOMPLETE')
        for target in req['target'] if isinstance(req['target'], list) else [req['target']]:
            check_link(root, 'index.md', target)
    warnings = check_registry(root, release, today)
    if not set(control.get('evidence_data_files', [])) <= EVIDENCE_DATA:
        raise ContractError('EVIDENCE_EXCLUSION_NOT_ALLOWLISTED')
    exceptions = {(e['path'], e['line_sha256'], e['legacy_source']) for e in control.get('historical_exceptions', [])}
    seen_exceptions = set()
    for relative in paths:
        path = root / relative
        if path.suffix.lower() not in ('.md', '.py', '.json', '.yaml', '.yml', '.txt', '.toml', '.ini', '.cfg', '.csv'):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        # Self-describing JSON holds paths as data; every other match is classified.
        if relative in control.get('evidence_data_files', []):
            continue
        for line in text.splitlines():
            for legacy in LEGACY.findall(line):
                key = (relative, digest(line.encode()), legacy)
                if key not in exceptions:
                    raise ContractError(f'LEGACY_REFERENCE: {relative}: {legacy}')
                seen_exceptions.add(key)
        if relative == 'AGENTS.md' or relative.startswith(('docs/ai/', '.agents/skills/', '.claude/skills/')):
            for raw in LINK.findall(text):
                check_link(root, relative, raw)
    if exceptions - seen_exceptions:
        raise ContractError('STALE_HISTORICAL_EXCEPTION')
    baseline = read_json(safe(root, BASELINE))
    pairs = baseline.get('product_pairs', [])
    if not pairs or len(pairs) != baseline['product_pair_count']:
        raise ContractError('PRODUCT_INVENTORY_EMPTY_OR_INCOMPLETE')
    for pair in pairs:
        if safe(root, pair['source']).read_bytes() != safe(root, pair['mirror']).read_bytes():
            raise ContractError(f'PRODUCT_PARITY: {pair["source"]}')
    if migration_freeze:
        if digest(safe(root, BASELINE).read_bytes()) != BASELINE_SHA256:
            raise ContractError('BASELINE_EVIDENCE_CHANGED')
        if not baseline.get('protected'):
            raise ContractError('PROTECTED_INVENTORY_EMPTY')
        roots = baseline.get('protected_roots', [])
        if not roots:
            raise ContractError('PROTECTED_ROOTS_EMPTY')
        actual_product = set()
        for prefix in roots:
            base = safe(root, prefix)
            for file in base.rglob('*'):
                rel = file.relative_to(root)
                if '__pycache__' in rel.parts or any(p in rel.parts for p in ('.pytest_cache', '.ruff_cache')) or file.name == '.DS_Store' or file.suffix in ('.pyc', '.pyo'):
                    continue
                if file.is_file() or file.is_symlink():
                    safe(root, rel.as_posix())
                    actual_product.add(rel.as_posix())
        expected_product = {p for p in baseline['protected'] if any(p.startswith(prefix + '/') for prefix in roots)}
        if actual_product != expected_product:
            raise ContractError('PROTECTED_INVENTORY_CHANGED')
        for relative, expected in baseline['protected'].items():
            if digest(safe(root, relative).read_bytes()) != expected:
                raise ContractError(f'PROTECTED_CHANGED: {relative}')
    return {'status': 'PASS', 'scope': 'offline static contracts only; no native client certification', 'tracked_and_new_files': len(paths), 'canonical_skills': len(SKILLS), 'generated_files': len(manifest['entries']), 'requirements': len(requirements), 'core_lines': len(core.splitlines()), 'core_bytes': len(core.encode()), 'product_pairs': len(pairs), 'migration_freeze': migration_freeze, 'historical_matches': len(seen_exceptions), 'warnings': warnings}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--generate', action='store_true')
    parser.add_argument('--release', action='store_true')
    parser.add_argument('--migration-freeze', action='store_true')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        if args.generate and (args.release or args.migration_freeze):
            raise ContractError('CHECK_FLAGS_REQUIRE_CHECK')
        result = {'status': 'PASS', 'changed': generate(args.root.resolve())} if args.generate else check(args.root.resolve(), release=args.release, migration_freeze=args.migration_freeze)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ContractError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f'FAIL {exc}')
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
