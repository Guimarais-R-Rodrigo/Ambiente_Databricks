"""Lot5 narrow retirement, with original evidence and source exceptions retained."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/historico/mirror-retirement.json'


def digest_records(data):
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


class MirrorRetirementTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text())
        self.control = json.loads((ROOT / 'docs/ai/control-map.json').read_text())

    def test_only_seven_duplicate_mirror_exceptions_retired(self):
        manifest = self.manifest
        self.assertEqual((98, 91, 7), (manifest['before_records'], manifest['after_records'], manifest['retired_count']))
        current = self.control['historical_exceptions']
        self.assertEqual(len(current), 91)
        self.assertEqual(digest_records(current), manifest['remaining_records_sha256'])
        self.assertFalse(any(item['path'] == manifest['retired_path'] for item in current))
        self.assertEqual(len(manifest['retired_records']), 7)
        self.assertTrue(all(item['path'] == manifest['retired_path'] for item in manifest['retired_records']))

    def test_each_source_exception_retained_with_same_hash_origin_and_reason(self):
        source = 'ambiente_databricks/.assistant/hub_readmes_visual_assets/specs/visual_contracts.yaml'
        current = [item for item in self.control['historical_exceptions'] if item['path'] == source]
        def project(item, retired=False):
            return (item['line'], item['line_sha256'], item['legacy_source_sha256'] if retired else
                    hashlib.sha256(item['legacy_source'].encode()).hexdigest(), item['replacement'], item['category'], item['reason'])
        self.assertEqual(Counter(project(item) for item in current),
                         Counter(project(item, True) for item in self.manifest['retired_records']))
        text = (ROOT / source).read_text().splitlines()
        for item in current:
            self.assertEqual(hashlib.sha256(text[item['line'] - 1].encode()).hexdigest(), item['line_sha256'])
            self.assertIn(item['legacy_source'], text[item['line'] - 1])

    def test_no_old_mirror_tracking_or_symlink_alias(self):
        tracked = subprocess.check_output(['git', 'ls-files', '-z', '--', 'Novo_Ambiente_Simulado'], cwd=ROOT)
        self.assertEqual(b'', tracked)
        self.assertFalse((ROOT / 'Novo_Ambiente_Simulado').exists())
        self.assertFalse((ROOT / 'Novo_Ambiente_Simulado').is_symlink())
        self.assertNotIn('docs/historico/mirror-retirement.json', self.control['evidence_data_files'])

    def test_retained_removal_manifest_has_unique_paths_and_hashes(self):
        records = self.manifest['removed_generated_files']
        self.assertEqual(654, len(records))
        self.assertEqual(len(records), len({item['path'] for item in records}))
        for item in records:
            self.assertTrue(item['path'].startswith('Novo_Ambiente_Simulado/'))
            self.assertRegex(item['sha256'], r'^[a-f0-9]{64}$')
            self.assertGreaterEqual(item['bytes'], 0)
        self.assertEqual('de26c33410fb744c4cb618425188e758ab4fa6ff', self.manifest['base_commit'])


if __name__ == '__main__': unittest.main()
