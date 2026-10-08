"""Offline maintainer instruction contracts. No network, models, settings or installs.

--check is read-only. --generate is retired; canonical skills are read directly.
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from markdown_links import markdown_destinations, is_remote_destination

VERSION = '2.0.0'
SKILLS = ('forward-test-skills', 'publicar-free', 'render-simulado', 'replicar-trabalho', 'validar-assistant', 'preparar-ambiente-trabalho', 'evoluir-hub', 'revisar-entrega')
MAP = 'docs/ai/control-map.json'
REGISTRY = 'docs/ai/standards/registry.json'
BASELINE = 'docs/auditoria/2026-10-06_ai-instrucoes/baseline.json'
BASELINE_SHA256 = '9354ac85c5441dca40a59d5d8b73457895d200d685fb25cbd4ecfe9a93378fda'
NATIVE_ENTRIES = 'docs/ai/native-entries.json'
TRACEABILITY = 'docs/ai/traceability-inventory.json'
EVIDENCE_DATA = {MAP, BASELINE, 'docs/auditoria/2026-10-06_ai-instrucoes/source-controls.json', 'docs/auditoria/2026-10-06_ai-instrucoes/traceability.json', 'docs/auditoria/2026-10-06_ai-instrucoes/reference-scan.json', 'docs/auditoria/2026-10-06_ai-instrucoes/traceability.csv'}
LEGACY = re.compile(r'\.claude/(?:CLAUDE\.md|rules/[\w.-]+\.md|context/[\w.-]+\.md|templates/[\w.-]+\.md|skills/README\.md)')

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

def check_skills(root: Path, control: dict) -> None:
    if control.get('adapters') or control.get('adopted_outputs'):
        raise ContractError('ADAPTERS_RETIRED')
    actual = {p.name for p in safe(root, '.agents/skills').iterdir() if p.is_dir() or p.is_symlink()}
    if actual != set(SKILLS):
        raise ContractError('SKILL_INVENTORY')
    for name in SKILLS:
        base = safe(root, '.agents/skills/' + name)
        frontmatter(safe(root, '.agents/skills/' + name + '/SKILL.md'), name)
        for file in base.rglob('*'):
            safe(root, file.relative_to(root).as_posix())


def generate(root: Path) -> list[str]:
    # Kept as a non-writing migration diagnostic for old callers.
    raise ContractError('GENERATOR_RETIRED: use --check; no adapters are generated')


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
    if is_remote_destination(raw):
        return
    target, _, fragment = raw.partition('#')
    target, fragment = unquote(target.partition('?')[0]), unquote(fragment)
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

def native_mechanism(relative: str) -> str | None:
    """Classify repository instruction candidates, not observed client support."""
    path = PurePosixPath(relative)
    name = path.name.casefold()
    if relative.startswith('.github/agents/') and name.endswith('.agent.md'):
        return 'copilot-custom-agent'
    if name in ('agents.md', 'agents.override.md'):
        return 'agents-override' if name == 'agents.override.md' else 'agents-directory'
    if name in ('claude.md', 'claude.local.md'):
        return 'claude-instructions'
    if name == 'gemini.md':
        return 'gemini-instructions'
    for family in ('.claude', '.grok', '.gemini'):
        parts = tuple(p.casefold() for p in path.parts)
        if any(parts[i:i + 2] == (family, 'rules') for i in range(len(parts) - 1)) and name.endswith('.md'):
            return 'provider-rules'
    return None


def universal_history(text: str) -> bool:
    flattened = ' '.join(text.split())
    return bool(re.search(r'(?:antes de (?:qualquer|toda)|sempre leia|leia sempre|obrigat[oó]ri[oa]|always read|before (?:every|any)).{0,150}(?:CHANGELOG|docs/sprints|docs/auditoria)', flattened, re.I)
                or re.search(r'@[^\s`<>]*(?:CHANGELOG|docs/sprints|docs/auditoria)', text, re.I))


def check_native_entries(root: Path, paths: list[str]) -> set[str]:
    manifest = read_json(safe(root, NATIVE_ENTRIES))
    if manifest.get('schema_version') != 1 or not manifest.get('revision'):
        raise ContractError('NATIVE_MANIFEST_SCHEMA')
    entries = manifest.get('entries')
    if not isinstance(entries, list) or not entries:
        raise ContractError('NATIVE_MANIFEST_EMPTY')
    # Ignoring a new instruction in Git must not hide it from the bootstrap gate.
    proc = subprocess.run(['git', 'ls-files', '--others', '--ignored', '--exclude-standard', '-z'], cwd=root, capture_output=True, check=True)
    ignored = [p.decode('utf-8') for p in proc.stdout.split(b'\0') if p]
    live = {p for p in paths + ignored if native_mechanism(p)
            and not p.startswith(('.artifacts/', 'Ambiente_Antigo/'))}
    declared = {}
    for entry in entries:
        if not isinstance(entry, dict) or any(not isinstance(entry.get(k), str) or not entry[k].strip()
                for k in ('path', 'mechanism', 'role', 'owner', 'load_condition', 'sha256', 'review_reason')):
            raise ContractError('NATIVE_ENTRY_INCOMPLETE')
        name = entry['path']
        if name in declared:
            raise ContractError(f'NATIVE_ENTRY_DUPLICATE: {name}')
        if entry['mechanism'] != native_mechanism(name) or entry['role'] not in ('core', 'shim', 'scoped-rule', 'override'):
            raise ContractError(f'NATIVE_ENTRY_CLASSIFICATION: {name}')
        if not isinstance(entry.get('shadows'), list):
            raise ContractError(f'NATIVE_SHADOW_DECLARATION: {name}')
        safe(root, name)
        declared[name] = entry
    if live != set(declared):
        raise ContractError(f'NATIVE_ENTRY_INVENTORY: unclassified={sorted(live - set(declared))}; absent={sorted(set(declared) - live)}')
    for name, entry in declared.items():
        data = safe(root, name).read_bytes()
        if universal_history(data.decode('utf-8')):
            raise ContractError(f'UNIVERSAL_HISTORY: {name}')
        if digest(data) != entry['sha256']:
            raise ContractError(f'NATIVE_ENTRY_CHANGED: {name}; review content and manifest together')
        expected_shadows = []
        if entry['mechanism'] == 'agents-override':
            sibling = str(PurePosixPath(name).with_name('AGENTS.md'))
            expected_shadows = [sibling] if sibling in live else []
            if entry['role'] != 'override':
                raise ContractError(f'NATIVE_ENTRY_CLASSIFICATION: {name}')
        if entry['shadows'] != expected_shadows:
            raise ContractError(f'NATIVE_SHADOW_DECLARATION: {name}')
    return live


def canonical_digest(value) -> str:
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def requirement_identity(req: dict) -> dict:
    source = req['source']
    return {'id': req['id'], 'control_id': req['control_id'], 'obligation': req['obligation'],
            'target': req['target'], 'owner': req['owner'], 'load_condition': req['load_condition'],
            'disposition': req['disposition'], 'test_ids': req['test_ids'],
            'source': {'sha': source.get('sha', source.get('commit')), 'path': source['path'],
                       'line_start': source['line_start'], 'line_end': source['line_end'],
                       'quote': source['quote']}}


def claim_identity(claim: dict) -> dict:
    return {k: claim[k] for k in ('id', 'provider', 'product', 'surface', 'url', 'kind', 'scope', 'paraphrase', 'owner', 'test_ids')}


def traceability_revision(root: Path) -> dict:
    manifest = read_json(safe(root, TRACEABILITY))
    revisions = manifest.get('revisions')
    if manifest.get('schema_version') != 1 or not isinstance(revisions, list) or not revisions:
        raise ContractError('TRACEABILITY_SCHEMA')
    previous = None
    for number, revision in enumerate(revisions, 1):
        if (revision.get('version') != number or
                any(not isinstance(revision.get(k), str) or not revision[k].strip()
                    for k in ('reviewed_at_utc', 'owner', 'reason')) or
                revision.get('previous_sha256') != (canonical_digest(previous) if previous else None)):
            raise ContractError('TRACEABILITY_REVISION_CHAIN')
        for group in ('requirements', 'claims'):
            values = revision.get(group)
            if not isinstance(values, list) or not values:
                raise ContractError('TRACEABILITY_INVENTORY_EMPTY')
            ids = set()
            for entry in values:
                if (not isinstance(entry, dict) or not isinstance(entry.get('id'), str)
                        or not entry['id'].strip() or entry['id'] in ids
                        or not isinstance(entry.get('identity_sha256'), str)
                        or not re.fullmatch(r'[0-9a-f]{64}', entry['identity_sha256'])):
                    raise ContractError('TRACEABILITY_IDENTITY_INVALID')
                ids.add(entry['id'])
            if previous:
                old = {e['id']: e['identity_sha256'] for e in previous[group]}
                new = {e['id']: e['identity_sha256'] for e in values}
                delta = {'added': sorted(new.keys() - old.keys()),
                         'removed': sorted(old.keys() - new.keys()),
                         'changed': sorted(k for k in new.keys() & old.keys() if new[k] != old[k])}
                if revision.get('changes', {}).get(group) != delta:
                    raise ContractError(f'TRACEABILITY_MIGRATION_DELTA: {group}')
        previous = revision
    if manifest.get('active_version') != len(revisions):
        raise ContractError('TRACEABILITY_ACTIVE_VERSION')
    return revisions[-1]


def check_identity_inventory(items: list[dict], expected: list[dict], identity, group: str) -> None:
    actual = {item['id']: canonical_digest(identity(item)) for item in items}
    wanted = {item['id']: item['identity_sha256'] for item in expected}
    if actual.keys() != wanted.keys():
        raise ContractError(f'{group}_IDENTITY_INVENTORY: missing={sorted(wanted.keys() - actual.keys())}; added={sorted(actual.keys() - wanted.keys())}')
    for key in actual:
        if actual[key] != wanted[key]:
            raise ContractError(f'{group}_IDENTITY_CHANGED: {key}; explicit versioned migration required')


def check_requirements(root: Path, control: dict, revision: dict) -> list[dict]:
    requirements = control.get('requirements', [])
    if not isinstance(requirements, list) or not requirements:
        raise ContractError('REQUIREMENT_COVERAGE')
    if {r.get('control_id') for r in requirements} != {f'C{i:02}' for i in range(1, 23)}:
        raise ContractError('REQUIREMENT_COVERAGE')
    ids, sources = set(), {}
    for req in requirements:
        if any(not isinstance(req.get(k), str) or not req[k].strip()
               for k in ('id', 'control_id', 'obligation', 'owner', 'load_condition', 'disposition')):
            raise ContractError('REQUIREMENT_INCOMPLETE')
        if req['id'] in ids:
            raise ContractError(f'REQUIREMENT_ID_DUPLICATE: {req["id"]}')
        ids.add(req['id'])
        if not isinstance(req.get('test_ids'), list) or not req['test_ids'] or any(not isinstance(t, str) or not t.strip() for t in req['test_ids']):
            raise ContractError(f'REQUIREMENT_TEST_IDS: {req["id"]}')
        targets = req.get('target')
        targets = [targets] if isinstance(targets, str) else targets
        if not isinstance(targets, list) or not targets or any(not isinstance(t, str) or not t for t in targets):
            raise ContractError(f'REQUIREMENT_TARGET: {req["id"]}')
        for target in targets:
            check_link(root, 'index.md', target)
        source = req.get('source')
        if not isinstance(source, dict):
            raise ContractError(f'SOURCE_SCHEMA: {req["id"]}')
        sha = source.get('sha', source.get('commit'))
        if (not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha)
                or ('sha' in source and 'commit' in source and source['sha'] != source['commit'])
                or not isinstance(source.get('path'), str) or not source['path']
                or not isinstance(source.get('quote'), str) or not source['quote']
                or type(source.get('line_start')) is not int or type(source.get('line_end')) is not int
                or not 1 <= source['line_start'] <= source['line_end']):
            raise ContractError(f'SOURCE_SCHEMA: {req["id"]}')
        safe(root, source['path'])
        key = (sha, source['path'])
        if key not in sources:
            kind = subprocess.run(['git', 'cat-file', '-t', sha], cwd=root, capture_output=True)
            data = subprocess.run(['git', 'show', sha + ':' + source['path']], cwd=root, capture_output=True)
            if kind.returncode or kind.stdout.strip() != b'commit' or data.returncode:
                raise ContractError(f'SOURCE_GIT_UNAVAILABLE: {req["id"]}; full source commit required')
            sources[key] = data.stdout
        data = sources[key]
        lines = data.decode('utf-8').splitlines()
        if source['line_end'] > len(lines) or '\n'.join(lines[source['line_start'] - 1:source['line_end']]) != source['quote']:
            raise ContractError(f'SOURCE_QUOTE_MISMATCH: {req["id"]}')
        if 'sha256' in source and digest(data) != source['sha256']:
            raise ContractError(f'SOURCE_BLOB_HASH: {req["id"]}')
    check_identity_inventory(requirements, revision['requirements'], requirement_identity, 'REQUIREMENT')
    return requirements


def check_registry(root: Path, release: bool, today: dt.date, revision: dict | None = None) -> list[str]:
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
        if any(not isinstance(claim.get(k), str) or not claim[k].strip() for k in required if k != 'test_ids') or not isinstance(claim.get('test_ids'), list) or not claim['test_ids'] or any(not isinstance(t, str) or not t.strip() for t in claim['test_ids']):
            raise ContractError(f'CLAIM_INCOMPLETE: {cid}')
        if not claim['url'].startswith('https://') or claim['state'] not in ('DOCUMENTED', 'OBSERVED', 'SUPPORTED'):
            raise ContractError(f'CLAIM_INVALID: {cid}')
        snapshot = safe(root, claim['snapshot'])
        if digest(snapshot.read_bytes()) != claim['snapshot_sha256']:
            raise ContractError(f'SNAPSHOT_HASH: {cid}')
        reviewed = dt.datetime.fromisoformat(claim['reviewed_at_utc'].replace('Z', '+00:00'))
        source = read_json(snapshot)
        if source.get('reviewed_at_utc') != claim['reviewed_at_utc'] or source.get('url') != claim['url'] or source.get('id') != cid or source.get('paraphrase') != claim['paraphrase']:
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
    revision = revision or traceability_revision(root)
    check_identity_inventory(claims, revision['claims'], claim_identity, 'CLAIM')
    return warnings

def check(root: Path, *, release: bool = False, migration_freeze: bool = False, today: dt.date | None = None) -> dict:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    paths = inventory(root)
    control = read_json(safe(root, MAP))
    check_skills(root, control)
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
    if safe(root, 'GEMINI.md').read_text() != '@./AGENTS.md\n':
        raise ContractError('BOOTSTRAP_CONTRACT')
    for relative in control['retired_sources']:
        if (root / relative).exists():
            raise ContractError(f'LEGACY_LOADER_PRESENT: {relative}')
    native_entries = check_native_entries(root, paths)
    revision = traceability_revision(root)
    requirements = check_requirements(root, control, revision)
    warnings = check_registry(root, release, today, revision)
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
                if legacy in native_entries:
                    continue  # Reviewed live extension, never a historical exception.
                key = (relative, digest(line.encode()), legacy)
                if key not in exceptions:
                    raise ContractError(f'LEGACY_REFERENCE: {relative}: {legacy}')
                seen_exceptions.add(key)
        if relative == 'AGENTS.md' or relative.startswith(('docs/ai/', '.agents/skills/', '.claude/skills/')):
            for raw in markdown_destinations(text):
                check_link(root, relative, raw)
    if exceptions - seen_exceptions:
        raise ContractError('STALE_HISTORICAL_EXCEPTION')
    from simulado import inventory as payload_inventory, parity_errors
    errors = parity_errors(root)
    if errors:
        raise ContractError('PRODUCT_PARITY: ' + '; '.join(errors))
    pairs = [name for name, item in payload_inventory(root / 'ambiente_databricks', source=True).items()
             if item['object_type'] != 'DIRECTORY']
    baseline = read_json(safe(root, BASELINE))
    if not baseline.get('product_pairs') or len(baseline['product_pairs']) != baseline['product_pair_count']:
        raise ContractError('PRODUCT_INVENTORY_EMPTY_OR_INCOMPLETE')
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
    return {'status': 'PASS', 'scope': 'offline static contracts only; no native client certification', 'tracked_and_new_files': len(paths), 'canonical_skills': len(SKILLS), 'generated_files': 0, 'requirements': len(requirements), 'core_lines': len(core.splitlines()), 'core_bytes': len(core.encode()), 'product_pairs': len(pairs), 'migration_freeze': migration_freeze, 'historical_matches': len(seen_exceptions), 'warnings': warnings}

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
