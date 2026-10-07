"""Reversible history retention and narrow legacy-reference exception regressions."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_ai_controls as fixture
import verify_concierge_history as recovery

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = 'docs/historico/changelog/2026-08-13_a_2026-10-06.md'
MANIFEST = 'docs/historico/changelog/manifest.json'
BASE = '126a2e125cca2251527f187a58696243414c6859'
ORIGINAL_HASH = 'f2ce1cb816ff02e4f68e71379f77c7552b8452fcbc0dcd8048af9e7b57ddee1e'
SNAPSHOT_HASH = '1369e890eda968fd18f1a605ffe187fc4d0ea04e6940e6420744765a96ddcfd2'
REBASINGS = (
    ('docs/sprints/skill_enforcement_rollout/PR_B1_SKILLS_SEM_CONTROLLER_2026-09-30.md',
     '../../sprints/skill_enforcement_rollout/PR_B1_SKILLS_SEM_CONTROLLER_2026-09-30.md'),
    ('docs/handoffs/2026-09-21_se07-auditoria-storage-cleanup.md',
     '../../handoffs/2026-09-21_se07-auditoria-storage-cleanup.md'),
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def recover_original(data):
    """Invert precisely the two audited href changes; reject every other delta."""
    if digest(data) != SNAPSHOT_HASH:
        raise ValueError('SNAPSHOT_CHANGED')
    for old, new in REBASINGS:
        before, after = ('](' + new + ')').encode(), ('](' + old + ')').encode()
        if data.count(before) != 1:
            raise ValueError('REBASE_OCCURRENCES')
        data = data.replace(before, after)
    if digest(data) != ORIGINAL_HASH:
        raise ValueError('RECOVERY_FAILED')
    return data


class HistoryRetentionTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = (ROOT / ARCHIVE).read_bytes()
        self.manifest = json.loads((ROOT / MANIFEST).read_text(encoding='utf-8'))

    def test_snapshot_recovers_exact_original_bytes(self):
        original = recover_original(self.snapshot)
        self.assertEqual(len(original), 306701)
        self.assertEqual(len(self.snapshot), 306703)
        self.assertEqual(len(original.splitlines()), 4501)
        self.assertEqual(self.manifest['source_commit'], BASE)
        self.assertEqual(self.manifest['original_sha256'], ORIGINAL_HASH)
        self.assertEqual(self.manifest['snapshot_sha256'], SNAPSHOT_HASH)
        self.assertEqual(self.manifest['snapshot_path'], ARCHIVE)
        self.assertEqual(self.manifest['entries_count'], 198)
        self.assertEqual([(x['old_href'], x['new_href']) for x in self.manifest['rebases']], list(REBASINGS))

    def test_all_198_entries_preserve_order_ranges_and_hashes(self):
        original = recover_original(self.snapshot)
        source_lines, snapshot_lines = original.splitlines(keepends=True), self.snapshot.splitlines(keepends=True)
        headings = [i + 1 for i, line in enumerate(source_lines) if re.match(rb'^## ', line)]
        entries = self.manifest['entries']
        self.assertEqual(len(headings), 198)
        self.assertEqual([e['line_start'] for e in entries], headings)
        self.assertEqual([e['id'] for e in entries], [f'C{i:03}' for i in range(1, 199)])
        for index, entry in enumerate(entries):
            with self.subTest(entry=entry['id']):
                start, end = entry['line_start'], entry['line_end']
                self.assertEqual(end, headings[index + 1] - 1 if index + 1 < len(headings) else 4501)
                self.assertEqual(source_lines[start-1].decode().strip()[3:], entry['title'])
                self.assertEqual(digest(b''.join(source_lines[start-1:end])), entry['original_sha256'])
                self.assertEqual(digest(b''.join(snapshot_lines[start-1:end])), entry['snapshot_sha256'])
        self.assertIn('R09', entries[-1]['title'])
        self.assertEqual(source_lines[:2], snapshot_lines[:2])

    def test_both_rebased_links_resolve_inside_repository(self):
        for old, new in REBASINGS:
            with self.subTest(href=new):
                target = ((ROOT / ARCHIVE).parent / new).resolve()
                self.assertTrue(target.is_relative_to(ROOT.resolve()))
                self.assertTrue(target.is_file())
                self.assertEqual(target, (ROOT / old).resolve())

    def test_byte_edit_entry_omission_and_reordering_are_rejected(self):
        entries = self.manifest['entries']
        lines = self.snapshot.splitlines(keepends=True)
        first, second = entries[0], entries[1]
        first_block = lines[first['line_start']-1:first['line_end']]
        second_block = lines[second['line_start']-1:second['line_end']]
        mutants = {
            'edit': self.snapshot.replace(b'# Changelog', b'# Changelog altered', 1),
            'omit': b''.join(lines[:2] + lines[first['line_end']:]),
            'reorder': b''.join(lines[:2] + second_block + first_block + lines[second['line_end']:]),
        }
        for label, mutant in mutants.items():
            with self.subTest(mutant=label), self.assertRaisesRegex(ValueError, 'SNAPSHOT_CHANGED'):
                recover_original(mutant)

    def test_exact_eleven_changelog_exceptions_migrated(self):
        control = json.loads((ROOT / fixture.ai.MAP).read_text(encoding='utf-8'))
        exceptions = control['historical_exceptions']
        self.assertFalse(any(e['path'] == 'CHANGELOG.md' for e in exceptions))
        migrated = [e for e in exceptions if e['path'] == ARCHIVE]
        self.assertEqual(len(migrated), 11)
        self.assertEqual(self.manifest['migrated_exception_count'], 11)
        self.assertEqual(self.manifest['historical_exception_total'], 98)
        self.assertEqual([
            {'line': e['line'], 'line_sha256': e['line_sha256'],
             'legacy_source_sha256': digest(e['legacy_source'].encode())}
            for e in migrated], self.manifest['migrated_exceptions'])
        for e in migrated:
            line = self.snapshot.decode().splitlines()[e['line']-1]
            self.assertEqual(digest(line.encode()), e['line_sha256'])
            self.assertIn(e['legacy_source'], line)

    def test_concierge_original_blobs_are_recoverable_without_retired_directory(self):
        manifest = json.loads((ROOT / 'docs/historico/concierge-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['source_commit'], BASE)
        self.assertEqual(len(manifest['entries']), 19)
        self.assertFalse((ROOT / 'novas_funcionalidades').exists())
        self.assertEqual(recovery.verify_manifest(ROOT, manifest), 19)

    def test_concierge_recovery_rejects_changed_hash_and_missing_blob(self):
        manifest = json.loads((ROOT / 'docs/historico/concierge-manifest.json').read_text(encoding='utf-8'))
        manifest['entries'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'HISTORY_BLOB_MISMATCH'):
            recovery.verify_manifest(ROOT, manifest)
        manifest['entries'][0]['path'] = 'novas_funcionalidades/missing.md'
        with self.assertRaisesRegex(ValueError, 'HISTORY_BLOB_UNAVAILABLE'):
            recovery.verify_manifest(ROOT, manifest)

    def test_concierge_recovery_rejects_empty_duplicate_and_unsafe_inventory(self):
        original = json.loads((ROOT / 'docs/historico/concierge-manifest.json').read_text(encoding='utf-8'))
        for label, change in (
            ('MANIFEST_COUNT_INVALID', {'entries': []}),
            ('MANIFEST_DUPLICATE_PATH', {'entries': [original['entries'][0]] * 19}),
            ('SOURCE_COMMIT_INVALID', {'source_commit': 'HEAD'}),
        ):
            with self.subTest(reason=label), self.assertRaisesRegex(ValueError, label):
                recovery.verify_manifest(ROOT, {**original, **change})
        original['entries'][0]['path'] = 'novas_funcionalidades/../Ambiente_Antigo/private.md'
        with self.assertRaisesRegex(ValueError, 'MANIFEST_PATH_INVALID'):
            recovery.verify_manifest(ROOT, original)


class HistoricalExceptionBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.case = fixture.AIControlsTests(methodName='runTest')
        self.case.setUp()
        self.addCleanup(self.case.tearDown)
        self.legacy = '.claude/' + 'rules/old.md'
        self.line = 'Dated historical statement: ' + self.legacy
        self.case.write(ARCHIVE, self.line + '\n')
        self.case.control['historical_exceptions'] = [{
            'path': ARCHIVE, 'line_sha256': digest(self.line.encode()),
            'legacy_source': self.legacy, 'reason': 'exact historical fixture',
        }]
        self.case.save_control()

    def test_exact_migrated_path_and_line_are_accepted(self):
        self.assertEqual(self.case.check()['historical_matches'], 1)

    def test_omitted_exception_fails(self):
        self.case.control['historical_exceptions'] = []
        self.case.save_control()
        self.case.assertFails('LEGACY_REFERENCE')

    def test_old_root_path_does_not_authorize_migrated_file(self):
        self.case.control['historical_exceptions'][0]['path'] = 'CHANGELOG.md'
        self.case.save_control()
        self.case.assertFails('LEGACY_REFERENCE')

    def test_changed_line_hash_fails(self):
        self.case.write(ARCHIVE, self.line + ' modified\n')
        self.case.assertFails('LEGACY_REFERENCE')

    def test_new_reference_in_same_snapshot_fails(self):
        self.case.write(ARCHIVE, self.line + '\nNew active instruction: ' + self.legacy + '\n')
        self.case.assertFails('LEGACY_REFERENCE')

    def test_same_allowed_line_in_another_history_file_fails(self):
        self.case.write('docs/historico/unapproved.md', self.line + '\n')
        self.case.assertFails('LEGACY_REFERENCE')

    def test_changed_legacy_origin_fails(self):
        self.case.control['historical_exceptions'][0]['legacy_source'] = '.claude/' + 'rules/other.md'
        self.case.save_control()
        self.case.assertFails('LEGACY_REFERENCE')

    def test_missing_line_leaves_rejected_stale_exception(self):
        self.case.write(ARCHIVE, 'Historical statement removed\n')
        self.case.assertFails('STALE_HISTORICAL_EXCEPTION')

    def test_blanket_history_exclusion_is_rejected(self):
        self.case.control['evidence_data_files'].append('docs/historico/')
        self.case.save_control()
        self.case.assertFails('EVIDENCE_EXCLUSION_NOT_ALLOWLISTED')


if __name__ == '__main__':
    unittest.main()
