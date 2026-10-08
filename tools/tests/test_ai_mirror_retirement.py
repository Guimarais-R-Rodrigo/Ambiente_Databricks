"""Retirement lineage remains frozen; later cleanup has an exact, proven delta."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/historico/mirror-retirement.json'
BASE = '8dd8da57de89122241890b8b6b059fd2f9be25d0'
OLD_SOURCE = 'ambiente_fonte/.assistant/hub_readmes_visual_assets/specs/visual_contracts.yaml'
SOURCE = OLD_SOURCE.replace('ambiente_fonte/', 'ambiente_databricks/')
PROTOTYPE = 'novas_funcionalidades/skills/hub-ml-concierge/docs/fontes.md'


def digest_records(data):
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


class MirrorRetirementTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.control = json.loads((ROOT / 'docs/ai/control-map.json').read_text(encoding='utf-8'))
        self.base_control = json.loads(self.blob('docs/ai/control-map.json'))

    def blob(self, path):
        return subprocess.check_output(['git', 'cat-file', 'blob', f'{BASE}:{path}'], cwd=ROOT)

    def test_retirement_lineage_and_exact_later_cleanup(self):
        manifest = self.manifest
        self.assertEqual((98, 91, 7), (manifest['before_records'], manifest['after_records'], manifest['retired_count']))
        current = self.control['historical_exceptions']
        original = self.base_control['historical_exceptions']
        self.assertEqual(len(original), 91)
        self.assertEqual(digest_records(original), manifest['remaining_records_sha256'])
        retired = [item for item in original if item['path'] in (OLD_SOURCE, PROTOTYPE)]
        self.assertEqual(Counter(item['path'] for item in retired), Counter({OLD_SOURCE: 7, PROTOTYPE: 3}))
        # ADR-0031 also retired exactly one exception belonging to the deleted
        # locator. Keep the original retirement manifest frozen and prove this
        # later delta separately, without allowing unrelated records to vanish.
        locator = [item for item in original if item['path'] == 'PLANO_HUB.md']
        self.assertEqual(len(locator), 1)
        self.assertEqual(locator[0]['line'], 614)
        self.assertEqual(locator[0]['line_sha256'],
                         '2d792709ad83cb7e6debcf34ecc0366dde6302e7cb327e42f7ba4e339dc39ecc')
        self.assertFalse((ROOT / 'PLANO_HUB.md').exists())
        expected = [item for item in original if item['path'] not in (OLD_SOURCE, PROTOTYPE, 'PLANO_HUB.md')]
        self.assertEqual(current, expected)  # All other owners, hashes and reasons are unchanged.
        self.assertEqual(len(current), 80)
        self.assertFalse(any(item['path'] == manifest['retired_path'] for item in current))
        self.assertEqual(len(manifest['retired_records']), 7)
        self.assertTrue(all(item['path'] == manifest['retired_path'] for item in manifest['retired_records']))

    def test_seven_source_exceptions_migrate_to_canonical_owners_with_original_provenance(self):
        original = [item for item in self.base_control['historical_exceptions'] if item['path'] == OLD_SOURCE]
        def project(item, retired=False):
            return (item['line'], item['line_sha256'], item['legacy_source_sha256'] if retired else
                    hashlib.sha256(item['legacy_source'].encode()).hexdigest(), item['replacement'], item['category'], item['reason'])
        self.assertEqual(Counter(project(item) for item in original),
                         Counter(project(item, True) for item in self.manifest['retired_records']))
        before = self.blob(OLD_SOURCE).decode('utf-8').splitlines()
        after = (ROOT / SOURCE).read_text(encoding='utf-8').splitlines()
        routes = {'.claude/' + 'rules/genie-code-oficial.md': 'docs/ai/references/databricks-genie-code.md',
                  '.claude/' + 'rules/fonte-de-verdade.md': 'docs/ai/rules/fontes-e-derivados.md'}
        expected = self.blob(OLD_SOURCE).replace(b'ambiente_fonte/', b'ambiente_databricks/')
        for old, owner in routes.items():
            expected = expected.replace(old.encode(), owner.encode())
        self.assertEqual((ROOT / SOURCE).read_bytes(), expected)
        for item in original:
            index = item['line'] - 1
            self.assertEqual(hashlib.sha256(before[index].encode()).hexdigest(), item['line_sha256'])
            self.assertIn(item['legacy_source'], before[index])
            owner = routes[item['legacy_source']]
            self.assertIn(owner, item['replacement'])
            self.assertTrue((ROOT / owner).is_file())
            self.assertIn(owner, after[index])
            self.assertNotIn(item['legacy_source'], after[index])

    def test_three_prototype_exceptions_retire_with_recoverable_hashes(self):
        retired = [item for item in self.base_control['historical_exceptions'] if item['path'] == PROTOTYPE]
        self.assertEqual(len(retired), 3)
        manifest = json.loads((ROOT / 'docs/historico/concierge-manifest.json').read_text(encoding='utf-8'))
        entry = next(item for item in manifest['entries'] if item['path'] == PROTOTYPE)
        blob = subprocess.check_output(['git', 'cat-file', 'blob', f"{manifest['source_commit']}:{PROTOTYPE}"], cwd=ROOT)
        self.assertEqual(blob, self.blob(PROTOTYPE))
        self.assertEqual(hashlib.sha256(blob).hexdigest(), entry['sha256'])
        self.assertEqual(len(blob), entry['bytes'])
        lines = blob.decode('utf-8').splitlines()
        for item in retired:
            self.assertEqual(hashlib.sha256(lines[item['line'] - 1].encode()).hexdigest(), item['line_sha256'])
            self.assertIn(item['legacy_source'], lines[item['line'] - 1])
        self.assertFalse((ROOT / 'novas_funcionalidades').exists())

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
