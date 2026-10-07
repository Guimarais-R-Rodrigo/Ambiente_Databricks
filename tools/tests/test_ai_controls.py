"""Synthetic offline contracts and mutants. Never substitutes for native loaders."""
from __future__ import annotations
import datetime as dt
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('ai_controls', Path(__file__).resolve().parents[1] / 'ai_controls.py')
ai = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ai)

class AIControlsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ai controls with spaces ')
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.write('AGENTS.md', '# Contrato\nFonte única. Dados sintéticos. Autorização explícita.\n')
        self.write('CLAUDE.md', '@AGENTS.md\n')
        self.write('GEMINI.md', '@./AGENTS.md\n')
        self.write('docs/ai/README.md', '# Guia\n[Contrato](../../AGENTS.md#contrato)\n')
        for name in ai.SKILLS:
            self.write(f'.agents/skills/{name}/SKILL.md', f'---\nname: {name}\ndescription: Procedimento sintético {name}.\n---\n# Procedimento\n[Guia](../../../docs/ai/README.md)\n')
        self.write('.agents/skills/validar-assistant/resources/example.txt', 'resource bytes\n')
        self.write('ambiente_fonte/.assistant/example.txt', 'synthetic product\n')
        self.write('.artifacts/simulado/Users/usuario-free/.assistant/example.txt', 'synthetic product\n')
        self.write('ambiente_fonte/.assistant_instructions.md', 'synthetic instructions\n')
        self.write('.artifacts/simulado/Users/usuario-free/.assistant_instructions.md', 'synthetic instructions\n')
        from simulado import MARKER
        self.write('.artifacts/simulado/README_GERADO.md', MARKER)
        self.write('.gitignore', '.artifacts/\n')
        protected_roots = ['ambiente_fonte', '.artifacts/simulado']
        protected = {p.relative_to(self.root).as_posix(): ai.digest(p.read_bytes())
                     for prefix in protected_roots for p in (self.root / prefix).rglob('*') if p.is_file()}
        self.baseline = {'product_pair_count': 1,
            'product_pairs': [{'source': 'ambiente_fonte/.assistant/example.txt',
                               'mirror': '.artifacts/simulado/Users/usuario-free/.assistant/example.txt'}],
            'protected_roots': protected_roots, 'protected': protected}
        self.json(ai.BASELINE, self.baseline)
        self.baseline_sha = ai.digest((self.root / ai.BASELINE).read_bytes())
        self.write('historical-source.md', 'preserve obligation\n')
        subprocess.run(['git', 'add', 'historical-source.md'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@openai.com', 'commit', '-qm', 'Synthetic source evidence'], cwd=self.root, check=True)
        source_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root, text=True).strip()
        self.source = {'path': 'historical-source.md', 'sha': source_sha, 'line_start': 1, 'line_end': 1, 'quote': 'preserve obligation'}
        self.control = {'adapters': [{'source': f'.agents/skills/{name}', 'destination': f'.claude/skills/{name}'} for name in ai.SKILLS], 'adopted_outputs': {}, 'critical_invariants': ['Fonte única', 'Dados sintéticos', 'Autorização explícita'], 'retired_sources': ['.claude/'+'CLAUDE.md'], 'requirements': [{'id': f'R{i}', 'control_id': f'C{i:02}', 'source': dict(self.source), 'owner': 'tests', 'obligation': 'preserve obligation', 'target': 'AGENTS.md#contrato', 'load_condition': 'session', 'test_ids': ['T04'], 'disposition': 'migrated'} for i in range(1, 23)], 'historical_exceptions': [], 'evidence_data_files': [ai.MAP, ai.BASELINE]}
        extra = dict(self.control['requirements'][0], id='R1-extra')
        extra['source'] = dict(self.source)
        self.control['requirements'].append(extra)
        self.save_control()
        self.snapshot = {'id': 'TEST', 'url': 'https://example.org/official', 'reviewed_at_utc': '2026-10-06T00:00:00Z', 'paraphrase': 'fixture'}
        self.snapshot_path = 'docs/ai/standards/2026-10-06/TEST.json'
        self.json(self.snapshot_path, self.snapshot)
        self.claim = {'id': 'TEST', 'provider': 'Test', 'product': 'Synthetic', 'surface': 'Fixture', 'url': self.snapshot['url'], 'reviewed_at_utc': self.snapshot['reviewed_at_utc'], 'documented_version': 'fixture', 'installed_version': 'fixture', 'scope': 'fixture', 'kind': 'documented', 'paraphrase': 'fixture', 'snapshot': self.snapshot_path, 'snapshot_sha256': ai.digest((self.root / self.snapshot_path).read_bytes()), 'test_ids': ['T07'], 'owner': 'tests', 'state': 'DOCUMENTED'}
        self.save_registry()
        self.advance_traceability()
        self.native_entries = []
        for name, role in (('AGENTS.md', 'core'), ('CLAUDE.md', 'shim'), ('GEMINI.md', 'shim')):
            self.register_native(name, role)
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        ai.generate(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8', newline='\n')

    def json(self, name, obj):
        self.write(name, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

    def save_control(self):
        self.json(ai.MAP, self.control)

    def save_registry(self):
        self.json(ai.REGISTRY, {'stale_after_days': 30, 'claims': [self.claim]})

    def advance_traceability(self):
        path = self.root / ai.TRACEABILITY
        data = json.loads(path.read_text()) if path.exists() else {'schema_version': 1, 'active_version': 0, 'revisions': []}
        claims = json.loads((self.root / ai.REGISTRY).read_text())['claims']
        previous = data['revisions'][-1] if data['revisions'] else None
        revision = {'version': data['active_version'] + 1,
                    'previous_sha256': ai.canonical_digest(previous) if previous else None,
                    'reviewed_at_utc': '2026-10-06T00:00:00Z', 'owner': 'tests',
                    'reason': 'Explicit synthetic identity migration',
                    'requirements': [{'id': r['id'], 'identity_sha256': ai.canonical_digest(ai.requirement_identity(r))} for r in self.control['requirements']],
                    'claims': [{'id': c['id'], 'identity_sha256': ai.canonical_digest(ai.claim_identity(c))} for c in claims]}
        if previous:
            revision['changes'] = {}
            for group in ('requirements', 'claims'):
                old = {e['id']: e['identity_sha256'] for e in previous[group]}
                new = {e['id']: e['identity_sha256'] for e in revision[group]}
                revision['changes'][group] = {'added': sorted(new.keys() - old.keys()),
                    'removed': sorted(old.keys() - new.keys()),
                    'changed': sorted(k for k in new.keys() & old.keys() if new[k] != old[k])}
        data['active_version'] += 1
        data['revisions'].append(revision)
        self.json(ai.TRACEABILITY, data)

    def test_one_missing_obligation_with_control_still_covered_is_rejected(self):
        self.control['requirements'].pop()
        self.save_control()
        self.assertFails('REQUIREMENT_IDENTITY_INVENTORY')

    def test_duplicate_requirement_id_rejected(self):
        self.control['requirements'][-1]['id'] = self.control['requirements'][0]['id']
        self.save_control()
        self.assertFails('REQUIREMENT_ID_DUPLICATE')

    def test_requirement_owner_missing_or_whitespace_rejected(self):
        for owner in (None, '   '):
            self.control['requirements'][0]['owner'] = owner
            self.save_control()
            self.assertFails('REQUIREMENT_INCOMPLETE')

    def test_source_exact_quote_and_bounds_rejected(self):
        source = self.control['requirements'][0]['source']
        for change in ({'quote': 'invented quote'}, {'line_end': 2}, {'line_start': 0}, {'sha': '0' * 40}):
            with self.subTest(change=change):
                source.clear()
                source.update(self.source)
                source.update(change)
                self.save_control()
                self.assertFails('SOURCE_QUOTE_MISMATCH|SOURCE_SCHEMA|SOURCE_GIT_UNAVAILABLE')

    def test_forged_source_identity_even_with_exact_text_is_rejected(self):
        self.write('other-source.md', self.source['quote'] + '\n')
        subprocess.run(['git', 'add', 'other-source.md'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@openai.com', 'commit', '-qm', 'Other synthetic evidence'], cwd=self.root, check=True)
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root, text=True).strip()
        self.control['requirements'][0]['source'].update(sha=sha, path='other-source.md')
        self.save_control()
        self.assertFails('REQUIREMENT_IDENTITY_CHANGED')

    def test_historical_commit_and_blob_hash_encoding_supported(self):
        source = self.control['requirements'][0]['source']
        source['commit'] = source.pop('sha')
        source['sha256'] = ai.digest((self.root / source['path']).read_bytes())
        self.save_control()
        self.assertEqual(self.check()['status'], 'PASS')
        source['sha256'] = '0' * 64
        self.save_control()
        self.assertFails('SOURCE_BLOB_HASH')

    def test_obligation_semantic_change_requires_explicit_migration(self):
        self.control['requirements'][0]['obligation'] = 'Changed reviewed obligation'
        self.save_control()
        self.assertFails('REQUIREMENT_IDENTITY_CHANGED')
        self.advance_traceability()
        self.assertEqual(self.check()['status'], 'PASS')

    def test_valid_but_changed_requirement_correspondence_requires_migration(self):
        changes = {'target': 'docs/ai/README.md', 'owner': 'different owner',
                   'load_condition': 'different trigger', 'disposition': 'different disposition',
                   'test_ids': ['T99']}
        req = self.control['requirements'][0]
        original = dict(req)
        for key, value in changes.items():
            with self.subTest(field=key):
                req.clear()
                req.update(original)
                req[key] = value
                self.save_control()
                self.assertFails('REQUIREMENT_IDENTITY_CHANGED')
        self.advance_traceability()
        self.assertEqual(self.check()['status'], 'PASS')

    def test_nonempty_claim_owner_and_test_mapping_drift_rejected(self):
        for key, value in (('owner', 'different owner'), ('test_ids', ['T99'])):
            with self.subTest(field=key):
                original = self.claim[key]
                self.claim[key] = value
                self.save_registry()
                self.assertFails('CLAIM_IDENTITY_CHANGED')
                self.claim[key] = original

    def test_explicit_requirement_removal_migration_preserves_prior_revision(self):
        original = json.loads((self.root / ai.TRACEABILITY).read_text())['revisions'][0]
        self.control['requirements'].pop()
        self.save_control()
        self.advance_traceability()
        self.assertEqual(self.check()['status'], 'PASS')
        current = json.loads((self.root / ai.TRACEABILITY).read_text())
        self.assertEqual(original, current['revisions'][0])
        self.assertEqual(['R1-extra'], current['revisions'][1]['changes']['requirements']['removed'])
        current['revisions'][1]['changes']['requirements']['removed'] = []
        self.json(ai.TRACEABILITY, current)
        self.assertFails('TRACEABILITY_MIGRATION_DELTA')

    def test_traceability_previous_hash_and_duplicate_id_rejected(self):
        self.advance_traceability()
        data = json.loads((self.root / ai.TRACEABILITY).read_text())
        data['revisions'][1]['previous_sha256'] = '0' * 64
        self.json(ai.TRACEABILITY, data)
        self.assertFails('TRACEABILITY_REVISION_CHAIN')
        data['revisions'][1]['previous_sha256'] = ai.canonical_digest(data['revisions'][0])
        data['revisions'][1]['requirements'].append(data['revisions'][1]['requirements'][0])
        self.json(ai.TRACEABILITY, data)
        self.assertFails('TRACEABILITY_IDENTITY_INVALID')

    def test_claim_paraphrase_bound_to_snapshot(self):
        self.claim['paraphrase'] = 'Unsupported paraphrase'
        self.save_registry()
        self.assertFails('REVIEW_BINDING')

    def test_coherent_claim_change_still_requires_identity_migration(self):
        self.claim['paraphrase'] = self.snapshot['paraphrase'] = 'Reviewed changed paraphrase'
        self.json(self.snapshot_path, self.snapshot)
        self.claim['snapshot_sha256'] = ai.digest((self.root / self.snapshot_path).read_bytes())
        self.save_registry()
        self.assertFails('CLAIM_IDENTITY_CHANGED')
        self.advance_traceability()
        self.assertEqual(self.check()['status'], 'PASS')

    def test_claim_identity_replacement_rejected(self):
        self.claim['id'] = self.snapshot['id'] = 'NEW'
        self.json(self.snapshot_path, self.snapshot)
        self.claim['snapshot_sha256'] = ai.digest((self.root / self.snapshot_path).read_bytes())
        self.save_registry()
        self.assertFails('CLAIM_IDENTITY_INVENTORY')

    def register_native(self, name, role='scoped-rule', shadows=None):
        entry = {'path': name, 'mechanism': ai.native_mechanism(name), 'role': role,
                 'owner': 'tests', 'load_condition': 'synthetic scope',
                 'sha256': ai.digest((self.root / name).read_bytes()),
                 'review_reason': 'Explicit synthetic review', 'shadows': shadows or []}
        self.native_entries = [e for e in self.native_entries if e['path'] != name] + [entry]
        self.json(ai.NATIVE_ENTRIES, {'schema_version': 1, 'revision': 'test-v1', 'entries': self.native_entries})

    def test_unclassified_native_entries_rejected(self):
        for name in ('AGENTS.override.md', 'tools/AGENTS.md', '.claude/' + 'rules/synthetic-new.md', 'tools/CLAUDE.md', 'tools/GEMINI.md'):
            with self.subTest(name=name):
                self.write(name, 'Before any task read CHANGELOG.md in full.\n')
                self.assertFails('NATIVE_ENTRY_INVENTORY')
                (self.root / name).unlink()

    def test_legitimate_reviewed_scoped_rule_is_allowed(self):
        for name in ('tools/AGENTS.md', '.claude/' + 'rules/synthetic-new.md'):
            self.write(name, '# Scoped procedure\nUse the common contract and targeted tests.\n')
            self.register_native(name)
        self.assertEqual(self.check()['status'], 'PASS')

    def test_reviewed_entry_still_cannot_require_universal_history(self):
        name = 'tools/AGENTS.md'
        self.write(name, 'Before any task read CHANGELOG.md in full.\n')
        self.register_native(name)
        self.assertFails('UNIVERSAL_HISTORY')

    def test_changed_registered_rule_requires_review(self):
        name = 'tools/AGENTS.md'
        self.write(name, '# Safe scoped rules\n')
        self.register_native(name)
        self.write(name, '# Changed scoped rules\n')
        self.assertFails('NATIVE_ENTRY_CHANGED')

    def test_override_requires_explicit_shadow_classification(self):
        name = 'AGENTS.override.md'
        self.write(name, '# Reviewed override\nUse AGENTS.md as the common contract.\n')
        self.register_native(name, 'override')
        self.assertFails('NATIVE_SHADOW_DECLARATION')
        self.register_native(name, 'override', ['AGENTS.md'])
        self.assertEqual(self.check()['status'], 'PASS')

    def test_ignored_native_entry_cannot_bypass_inventory(self):
        self.write('.gitignore', '.artifacts/\nAGENTS.override.md\n')
        self.write('AGENTS.override.md', '# Ignored but loadable override\n')
        self.assertFails('NATIVE_ENTRY_INVENTORY')

    def test_duplicate_and_missing_native_manifest_entries_rejected(self):
        self.native_entries.append(self.native_entries[0])
        self.json(ai.NATIVE_ENTRIES, {'schema_version': 1, 'revision': 'test', 'entries': self.native_entries})
        self.assertFails('NATIVE_ENTRY_DUPLICATE')
        self.native_entries.pop()
        self.native_entries.pop()
        self.json(ai.NATIVE_ENTRIES, {'schema_version': 1, 'revision': 'test', 'entries': self.native_entries})
        self.assertFails('NATIVE_ENTRY_INVENTORY')

    def check(self, **kwargs):
        with patch.object(ai, 'BASELINE_SHA256', self.baseline_sha):
            return ai.check(self.root, today=dt.date(2026, 10, 6), **kwargs)

    def assertFails(self, reason, **kwargs):
        with self.assertRaisesRegex(ai.ContractError, reason):
            self.check(**kwargs)

    def tree(self):
        return {p.relative_to(self.root).as_posix(): ai.digest(p.read_bytes()) for p in self.root.rglob('*') if p.is_file() and '.git' not in p.relative_to(self.root).parts}

    def test_positive_check_is_read_only(self):
        before = self.tree()
        result = self.check(migration_freeze=True)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(before, self.tree())

    def test_second_generation_is_identical(self):
        before = self.tree()
        self.assertEqual(ai.generate(self.root), [])
        self.assertEqual(before, self.tree())

    def test_source_edit_can_update_owned_adapter(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text() + '\nUpdated source.\n')
        self.assertFails('ADAPTER_DRIFT')
        self.assertTrue(ai.generate(self.root))
        self.assertEqual(self.check()['status'], 'PASS')

    def test_edited_adapter_rejected_without_mutation(self):
        p = self.root / '.claude/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text() + '\nUnowned edit.\n')
        before = self.tree()
        self.assertFails('UNMANAGED_OR_EDITED')
        with self.assertRaisesRegex(ai.ContractError, 'UNMANAGED_OR_EDITED'):
            ai.generate(self.root)
        self.assertEqual(before, self.tree())

    def test_missing_resource_rejected(self):
        (self.root / '.claude/skills/validar-assistant/resources/example.txt').unlink()
        self.assertFails('ADAPTER_DRIFT')

    def test_missing_source_resource_is_not_deleted_silently(self):
        (self.root / '.agents/skills/validar-assistant/resources/example.txt').unlink()
        self.assertFails('UNMANAGED_EXTRA')

    def test_unmanaged_extra_blocks_all_writes(self):
        self.write('.claude/skills/validar-assistant/foreign.txt', 'do not overwrite\n')
        before = self.tree()
        with self.assertRaisesRegex(ai.ContractError, 'UNMANAGED_EXTRA'):
            ai.generate(self.root)
        self.assertEqual(before, self.tree())

    def test_missing_or_empty_adapter_inventory_fails(self):
        self.control['adapters'] = []
        self.save_control()
        self.assertFails('ADAPTER_INVENTORY')

    def test_destination_map_tampering_cannot_grant_write(self):
        self.control['adapters'][0]['destination'] = 'foreign'
        self.save_control()
        before = self.tree()
        with self.assertRaisesRegex(ai.ContractError, 'ADAPTER_INVENTORY'):
            ai.generate(self.root)
        self.assertEqual(before, self.tree())

    def test_traversal_map_rejected(self):
        self.control['adapters'][0]['destination'] = '../outside'
        self.save_control()
        self.assertFails('ADAPTER_INVENTORY')

    def test_source_symlink_rejected(self):
        p = self.root / '.agents/skills/validar-assistant/resources/example.txt'
        p.unlink()
        p.symlink_to(self.root / 'AGENTS.md')
        self.assertFails('SYMLINK')

    def test_destination_symlink_rejected(self):
        p = self.root / '.claude/skills/validar-assistant/resources/example.txt'
        p.unlink()
        p.symlink_to(self.root / 'AGENTS.md')
        before = self.tree()
        with self.assertRaisesRegex(ai.ContractError, 'SYMLINK'):
            ai.generate(self.root)
        self.assertEqual(before, self.tree())

    def test_ancestor_symlink_rejected(self):
        original = self.root / '.claude'
        original.rename(self.root / 'other')
        original.symlink_to(self.root / 'other', target_is_directory=True)
        self.assertFails('SYMLINK')

    def test_hardlink_external_output_and_manifest_block_all_writes(self):
        # Use the last output as well as the manifest to catch partial writes.
        for relative in ('.claude/skills/validar-assistant/SKILL.md', ai.MANIFEST):
            with self.subTest(relative=relative):
                path = self.root / relative
                external = tempfile.TemporaryDirectory(prefix='ai external sentinel ')
                self.addCleanup(external.cleanup)
                foreign = Path(external.name) / 'foreign-sentinel'
                foreign.hardlink_to(path)
                before_external = foreign.read_bytes()
                source = self.root / '.agents/skills/forward-test-skills/SKILL.md'
                original = source.read_bytes()
                source.write_bytes(original + b'\nAuthorized synthetic update.\n')
                before = self.tree()
                try:
                    with self.assertRaisesRegex(ai.ContractError, 'HARDLINK_OUTPUT'):
                        ai.generate(self.root)
                    self.assertEqual(before_external, foreign.read_bytes())
                    self.assertEqual(before, self.tree())
                finally:
                    foreign.unlink()
                    source.write_bytes(original)

    def test_hardlink_between_outputs_blocks_all_writes(self):
        for name in ('forward-test-skills', 'validar-assistant'):
            self.write(f'.agents/skills/{name}/shared.txt', 'identical resource\n')
        ai.generate(self.root)
        first = self.root / '.claude/skills/forward-test-skills/shared.txt'
        last = self.root / '.claude/skills/validar-assistant/shared.txt'
        last.unlink()
        last.hardlink_to(first)
        source = self.root / '.agents/skills/forward-test-skills/shared.txt'
        source.write_text('changed resource\n')
        before = self.tree()
        with self.assertRaisesRegex(ai.ContractError, 'HARDLINK_OUTPUT'):
            ai.generate(self.root)
        self.assertEqual(before, self.tree())

    def test_ancestor_symlink_generation_preserves_external_tree(self):
        original = self.root / '.claude'
        external = tempfile.TemporaryDirectory(prefix='ai external adapters ')
        self.addCleanup(external.cleanup)
        foreign = Path(external.name) / 'foreign-claude'
        original.rename(foreign)
        original.symlink_to(foreign, target_is_directory=True)
        source = self.root / '.agents/skills/forward-test-skills/SKILL.md'
        source.write_bytes(source.read_bytes() + b'\nSynthetic update.\n')
        before = {p.relative_to(foreign).as_posix(): p.read_bytes()
                  for p in foreign.rglob('*') if p.is_file()}
        with self.assertRaisesRegex(ai.ContractError, 'SYMLINK'):
            ai.generate(self.root)
        self.assertEqual(before, {p.relative_to(foreign).as_posix(): p.read_bytes()
                                for p in foreign.rglob('*') if p.is_file()})

    def test_safe_path_rejects_absolute_backslash_and_traversal(self):
        for name in ('../x', '/tmp/x', 'a\\b', 'a/../b', './a'):
            with self.subTest(name=name), self.assertRaisesRegex(ai.ContractError, 'UNSAFE_PATH'):
                ai.safe(self.root, name)

    def test_empty_git_inventory_fails(self):
        subprocess.run(['git', 'rm', '-r', '--cached', '-q', '.'], cwd=self.root, check=True)
        self.assertFails('GIT_INVENTORY_EMPTY')

    def test_new_untracked_control_is_scanned(self):
        self.write('new.md', 'See ' + '.claude/' + 'rules/retired.md\n')
        self.assertFails('LEGACY_REFERENCE')

    def test_duplicate_sixth_skill_rejected(self):
        self.write('.agents/skills/ghost/SKILL.md', '---\nname: ghost\ndescription: extra\n---\n')
        self.assertFails('SKILL_INVENTORY')

    def test_skill_name_mismatch_rejected(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text().replace('name: validar-assistant', 'name: wrong'))
        self.assertFails('SKILL_METADATA')

    def test_empty_description_rejected(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text().replace('description: Procedimento sintético validar-assistant.', 'description:'))
        self.assertFails('SKILL_METADATA')

    def test_permissions_not_portable_frontmatter(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text().replace('description:', 'allowed-tools: Bash\ndescription:'))
        self.assertFails('SKILL_METADATA')

    def test_core_line_budget_rejected(self):
        p = self.root / 'AGENTS.md'
        p.write_text(p.read_text() + '\n' * 151)
        self.assertFails('CORE_BUDGET')

    def test_core_byte_budget_rejected(self):
        p = self.root / 'AGENTS.md'
        p.write_text(p.read_text() + 'x' * 12289)
        self.assertFails('CORE_BUDGET')

    def test_missing_critical_invariant_rejected(self):
        p = self.root / 'AGENTS.md'
        p.write_text(p.read_text().replace('Dados sintéticos', 'Unrestricted data'))
        self.assertFails('CORE_INVARIANT_MISSING')

    def test_direct_history_import_rejected(self):
        p = self.root / 'AGENTS.md'
        p.write_text(p.read_text() + '\n@CHANGELOG.md\n')
        self.assertFails('CORE_IMPORT_NOT_PORTABLE')

    def test_transitive_history_import_rejected(self):
        self.write('CLAUDE.md', '@AGENTS.md\n@CHANGELOG.md\n')
        self.assertFails('BOOTSTRAP_CONTRACT')

    def test_universal_history_prose_rejected(self):
        p = self.root / 'AGENTS.md'
        p.write_text(p.read_text() + '\nAntes de qualquer tarefa leia CHANGELOG.md\n')
        self.assertFails('UNIVERSAL_HISTORY')

    def test_duplicate_legacy_bootstrap_rejected(self):
        self.write('.claude/'+'CLAUDE.md', 'Old mandatory rules\n')
        self.assertFails('LEGACY_LOADER_PRESENT')

    def test_incomplete_requirement_coverage_rejected(self):
        self.control['requirements'].pop(-2)
        self.save_control()
        self.assertFails('REQUIREMENT_COVERAGE')

    def test_missing_requirement_target_rejected(self):
        self.control['requirements'][0]['target'] = 'missing.md'
        self.save_control()
        self.assertFails('LINK_MISSING')

    def test_wrong_case_link_rejected(self):
        self.write('docs/ai/README.md', '# Guide\n[Core](../../agents.md)\n')
        self.assertFails('LINK_MISSING|LINK_CASE')

    def test_missing_anchor_rejected(self):
        self.write('docs/ai/README.md', '# Guide\n[Core](../../AGENTS.md#missing)\n')
        self.assertFails('ANCHOR_MISSING')

    def test_claim_missing_source_rejected(self):
        self.claim['url'] = ''
        self.save_registry()
        self.assertFails('CLAIM_INCOMPLETE')

    def test_date_only_refresh_rejected(self):
        self.claim['reviewed_at_utc'] = '2026-10-05T00:00:00Z'
        self.save_registry()
        self.assertFails('REVIEW_BINDING')

    def test_snapshot_drift_rejected(self):
        self.write(self.snapshot_path, '{}\n')
        self.assertFails('SNAPSHOT_HASH')

    def test_stale_warns_normal_and_blocks_release(self):
        self.claim['reviewed_at_utc'] = self.snapshot['reviewed_at_utc'] = '2026-08-01T00:00:00Z'
        self.json(self.snapshot_path, self.snapshot)
        self.claim['snapshot_sha256'] = ai.digest((self.root / self.snapshot_path).read_bytes())
        self.save_registry()
        self.assertTrue(self.check()['warnings'])
        self.assertFails('CLAIM_STALE', release=True)

    def test_claim_support_requires_observed_evidence(self):
        self.claim['state'] = 'SUPPORTED'
        self.save_registry()
        self.assertFails('SUPPORT_WITHOUT_EVIDENCE')

    def test_new_live_legacy_reference_rejected(self):
        self.write('docs/ai/new.md', 'Old path ' + '.claude/'+'rules/old.md\n')
        self.assertFails('LEGACY_REFERENCE')

    def test_historical_exception_exact_line_does_not_hide_new_line(self):
        line = 'Historical ' + '.claude/'+'rules/old.md'
        self.write('history.md', line+'\n')
        self.control['historical_exceptions'] = [{'path':'history.md', 'line_sha256':ai.digest(line.encode()), 'legacy_source':'.claude/'+'rules/old.md', 'reason':'dated historical evidence'}]
        self.save_control()
        self.assertEqual(self.check()['status'], 'PASS')
        self.write('history.md', line+'\nNew active ' + '.claude/'+'rules/old.md\n')
        self.assertFails('LEGACY_REFERENCE')

    def test_stale_exception_rejected(self):
        self.control['historical_exceptions'] = [{'path':'history.md', 'line_sha256':'0'*64, 'legacy_source':'old'}]
        self.save_control()
        self.assertFails('STALE_HISTORICAL_EXCEPTION')

    def test_runtime_one_side_changed_rejected(self):
        self.write('ambiente_fonte/.assistant/example.txt', 'mutated\n')
        self.assertFails('PRODUCT_PARITY')

    def test_runtime_both_sides_changed_fails_migration_freeze(self):
        self.write('ambiente_fonte/.assistant/example.txt', 'mutated\n')
        self.write('.artifacts/simulado/Users/usuario-free/.assistant/example.txt', 'mutated\n')
        self.assertFails('PROTECTED_CHANGED', migration_freeze=True)

    def test_runtime_and_manifest_hash_tampering_rejected(self):
        self.write('ambiente_fonte/.assistant/example.txt', 'mutated\n')
        self.write('.artifacts/simulado/Users/usuario-free/.assistant/example.txt', 'mutated\n')
        self.baseline['protected']['ambiente_fonte/.assistant/example.txt'] = ai.digest(b'mutated\n')
        self.json(ai.BASELINE, self.baseline)
        self.assertFails('BASELINE_EVIDENCE_CHANGED', migration_freeze=True)

    def test_product_inventory_empty_rejected(self):
        self.baseline['product_pairs'] = []
        self.json(ai.BASELINE, self.baseline)
        self.assertFails('PRODUCT_INVENTORY_EMPTY_OR_INCOMPLETE')

    def test_future_authorized_product_changes_not_frozen_by_normal_check(self):
        self.write('ambiente_fonte/.assistant/example.txt', 'authorized future change\n')
        self.write('.artifacts/simulado/Users/usuario-free/.assistant/example.txt', 'authorized future change\n')
        self.assertEqual(self.check()['status'], 'PASS')

    def test_added_runtime_both_sides_fails_freeze_inventory(self):
        self.write('ambiente_fonte/.assistant/new_runtime.py', 'pass\n')
        self.write('.artifacts/simulado/Users/usuario-free/.assistant/new_runtime.py', 'pass\n')
        self.assertFails('PROTECTED_INVENTORY_CHANGED', migration_freeze=True)

    def test_duplicate_frontmatter_key_rejected(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text().replace('name: validar-assistant', 'name: validar-assistant\nname: validar-assistant'))
        self.assertFails('FRONTMATTER_DUPLICATE_KEY')

    def test_invalid_yaml_frontmatter_rejected(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text().replace('description: Procedimento sintético validar-assistant.', 'description: [unterminated'))
        self.assertFails('FRONTMATTER_SCALAR')

    def test_folded_description_preserved(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text().replace('description: Procedimento sintético validar-assistant.', 'description: >-\n  Valid folded\n  description.'))
        ai.generate(self.root)
        self.assertEqual(self.check()['status'], 'PASS')

    def test_missing_image_resource_rejected(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_text(p.read_text() + '\n![Missing](resources/missing.png)\n')
        ai.generate(self.root)
        self.assertFails('LINK_MISSING')

    def test_duplicate_derived_skill_rejected(self):
        self.write('.claude/skills/ghost/SKILL.md', '---\nname: ghost\ndescription: extra\n---\n')
        self.assertFails('DERIVED_SKILL_INVENTORY')

    def test_map_cannot_exclude_arbitrary_live_file(self):
        self.control['evidence_data_files'].append('new.md')
        self.save_control()
        self.assertFails('EVIDENCE_EXCLUSION_NOT_ALLOWLISTED')

    def test_scan_rejects_untracked_symlink_before_read(self):
        (self.root / 'new.md').symlink_to(self.root / 'AGENTS.md')
        self.assertFails('SYMLINK')

    def test_case_mismatch_is_detected_lexically(self):
        self.write('docs/ai/README.md', '# Guide\n[Core](../../agents.md)\n')
        self.assertFails('LINK_CASE')

    def test_plain_numeric_descriptions_and_blank_string_rejected(self):
        path = self.root / '.agents/skills/validar-assistant/SKILL.md'
        original = path.read_text()
        for scalar in ('123', '1.2', "'   '"):
            with self.subTest(scalar=scalar):
                path.write_text(original.replace('description: Procedimento sintético validar-assistant.', 'description: ' + scalar))
                self.assertFails('FRONTMATTER_SCALAR|SKILL_METADATA')

    def test_crlf_source_skill_rejected_before_generation(self):
        p = self.root / '.agents/skills/validar-assistant/SKILL.md'
        p.write_bytes(p.read_bytes().replace(b'\n', b'\r\n'))
        before = self.tree()
        with self.assertRaisesRegex(ai.ContractError, 'SKILL_ENCODING'):
            ai.generate(self.root)
        self.assertEqual(before, self.tree())

    def test_crlf_core_rejected_on_actual_bytes(self):
        p = self.root / 'AGENTS.md'
        p.write_bytes(p.read_bytes().replace(b'\n', b'\r\n'))
        self.assertFails('CORE_ENCODING')

    def test_generated_frontmatter_validated(self):
        output, _ = ai.expected_outputs(self.root, self.control)
        for name in ai.SKILLS:
            path = '.claude/skills/' + name + '/SKILL.md'
            ai.validate_skill_bytes(output[path], name, path)

    def test_inline_history_imports_rejected(self):
        p = self.root / 'AGENTS.md'
        original = p.read_text()
        for extra in ('- @CHANGELOG.md', 'Leia @CHANGELOG.md antes de agir.'):
            with self.subTest(extra=extra):
                p.write_text(original + '\n' + extra + '\n')
                self.assertFails('CORE_IMPORT_NOT_PORTABLE')

    def test_multiline_mandatory_history_prose_rejected(self):
        p = self.root / 'AGENTS.md'
        p.write_text(p.read_text() + '\nAntes de qualquer tarefa,\nleia [histórico](CHANGELOG.md).\n')
        self.assertFails('UNIVERSAL_HISTORY')

    def test_fake_observed_evidence_cannot_promote_claim(self):
        for state in ('OBSERVED', 'SUPPORTED'):
            with self.subTest(state=state):
                self.claim['state'] = state
                self.claim['observed_evidence'] = 'missing-evidence.json'
                self.save_registry()
                self.assertFails('PROMOTION_REQUIRES_VALIDATED_EVIDENCE_FORMAT')

if __name__ == '__main__':
    unittest.main()
