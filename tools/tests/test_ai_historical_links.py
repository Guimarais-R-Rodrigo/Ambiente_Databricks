"""Frozen hrefs require exact sources/targets; live or invented links never pass."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import historical_links as history

ROOT = Path(__file__).resolve().parents[2]


class HistoricalLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = json.loads((ROOT / history.MANIFEST).read_text(encoding="utf-8"))
        self.manifest["entries"] = [self.manifest["entries"][0]]
        self.entry = self.manifest["entries"][0]
        target = self.root / self.entry["source"]
        target.parent.mkdir(parents=True)
        target.write_bytes((ROOT / self.entry["source"]).read_bytes())
        real_git = history.git
        self.mock = patch.object(history, "git", side_effect=lambda root, *args: real_git(ROOT, *args))
        self.mock.start()
        self.addCleanup(self.mock.stop)

    def save(self):
        path = self.root / history.MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_exact_reference_recovers_original(self):
        self.save()
        self.assertEqual(history.load(self.root), {(self.entry["source"], self.entry["href"])})

    def test_changed_source_rejected(self):
        path = self.root / self.entry["source"]
        path.write_bytes(path.read_bytes() + b"altered\n")
        self.save()
        with self.assertRaisesRegex(ValueError, "SOURCE_CHANGED"):
            history.load(self.root)

    def test_invented_or_changed_values_rejected(self):
        original = copy.deepcopy(self.manifest)
        for key, value in (("href", "../../ambiente_fonte/inventado.md"),
                           ("target", "../../outside"), ("object_id", "0" * 40),
                           ("target_sha256", "0" * 64), ("source", "README.md")):
            with self.subTest(key=key):
                self.manifest = copy.deepcopy(original)
                self.manifest["entries"][0][key] = value
                self.save()
                with self.assertRaises(ValueError):
                    history.load(self.root)

    def test_duplicate_empty_and_other_revision_rejected(self):
        original = copy.deepcopy(self.manifest)
        for mutation in ("duplicate", "empty", "revision"):
            with self.subTest(mutation=mutation):
                self.manifest = copy.deepcopy(original)
                if mutation == "duplicate":
                    self.manifest["entries"].append(copy.deepcopy(self.entry))
                elif mutation == "empty":
                    self.manifest["entries"] = []
                else:
                    self.manifest["source_commit"] = "0" * 40
                self.save()
                with self.assertRaises(ValueError):
                    history.load(self.root)

    def test_live_target_is_not_historical_exception(self):
        target = self.root / self.entry["target"]
        target.parent.mkdir(parents=True)
        target.write_bytes(b"exists now")
        self.save()
        with self.assertRaisesRegex(ValueError, "NOT_NEEDED"):
            history.load(self.root)

    def test_git_unavailable_blocks(self):
        self.save()
        with patch.object(history, "git", side_effect=ValueError("HISTORICAL_GIT_UNAVAILABLE")):
            with self.assertRaisesRegex(ValueError, "GIT_UNAVAILABLE"):
                history.load(self.root)



class PlanHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = json.loads((ROOT / history.PLAN_MANIFEST).read_text(encoding="utf-8"))
        for entry in self.manifest["entries"]:
            path = self.root / entry["source"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / entry["source"]).read_bytes())
        real_git = history.git
        mocked = patch.object(history, "git", side_effect=lambda root, *args: real_git(ROOT, *args))
        mocked.start()
        self.addCleanup(mocked.stop)

    def save(self):
        path = self.root / history.PLAN_MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_exact_two_references_recover_real_blobs(self):
        self.save()
        self.assertEqual(history.load(self.root), history.PLAN_PAIRS)

    def test_real_checkout_preserves_thirty_old_pairs_and_adds_only_two(self):
        self.assertEqual(len(history.load_faxina(ROOT)), 30)
        self.assertEqual(history.load_plan(ROOT), history.PLAN_PAIRS)
        self.assertEqual(len(history.load(ROOT)), 34)

    def test_changed_source_or_source_hash_is_rejected(self):
        self.save()
        source = self.root / self.manifest["entries"][0]["source"]
        original = source.read_bytes()
        source.write_bytes(original + b"altered")
        with self.assertRaisesRegex(ValueError, "SOURCE_CHANGED"):
            history.load(self.root)
        source.write_bytes(original)
        self.manifest["entries"][0]["source_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(ValueError, "SOURCE_CHANGED"):
            history.load(self.root)

    def test_revision_target_blob_and_hash_mutations_are_rejected(self):
        original = copy.deepcopy(self.manifest)
        for key, value in (("source_commit", "HEAD"), ("target_commit", "HEAD"),
                           ("target", "MANUAL_TECNICO.md"), ("object_id", "0" * 40),
                           ("target_sha256", "0" * 64), ("schema_version", 2)):
            with self.subTest(key=key):
                self.manifest = copy.deepcopy(original)
                self.manifest[key] = value
                self.save()
                with self.assertRaises(ValueError):
                    history.load(self.root)

    def test_empty_duplicate_extra_source_and_invented_href_are_rejected(self):
        original = copy.deepcopy(self.manifest)
        for mutation in ("empty", "duplicate", "extra", "source", "href"):
            with self.subTest(mutation=mutation):
                self.manifest = copy.deepcopy(original)
                entries = self.manifest["entries"]
                if mutation == "empty":
                    self.manifest["entries"] = []
                elif mutation == "duplicate":
                    entries[1] = copy.deepcopy(entries[0])
                elif mutation == "extra":
                    entries.append(copy.deepcopy(entries[0]))
                elif mutation == "source":
                    entries[0]["source"] = "docs/handoffs/unapproved.md"
                else:
                    entries[0]["href"] = "../../../PLANO_HUB.md"
                self.save()
                with self.assertRaises(ValueError):
                    history.load(self.root)

    def test_restored_local_target_makes_ledger_stale(self):
        (self.root / "PLANO_HUB.md").write_bytes(b"restored")
        self.save()
        with self.assertRaisesRegex(ValueError, "NOT_NEEDED"):
            history.load(self.root)

    def test_missing_git_object_blocks_instead_of_accepting(self):
        self.save()
        with patch.object(history, "git", side_effect=ValueError("HISTORICAL_GIT_UNAVAILABLE")):
            with self.assertRaisesRegex(ValueError, "GIT_UNAVAILABLE"):
                history.load(self.root)

    def test_absent_ledger_does_not_authorize_any_pair(self):
        self.assertEqual(history.load_plan(self.root), set())

class AdapterHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.relative = 'docs/manutencao/referencias-historicas-adaptador.json'
        self.data = json.loads((ROOT / self.relative).read_text(encoding='utf-8'))
        for entry in self.data['entries']:
            target = self.root / entry['source']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / entry['source']).read_bytes())
        real_git = history.git
        mocked = patch.object(history, 'git', side_effect=lambda root, *args: real_git(ROOT, *args))
        mocked.start()
        self.addCleanup(mocked.stop)
        self.save()

    def save(self):
        path = self.root / self.relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.data), encoding='utf-8')

    def test_exact_recovery(self):
        self.assertEqual(history.load_claude(self.root), history.CLAUDE_PAIRS)

    def test_missing_pair_rejected(self):
        self.data['entries'].pop()
        self.save()
        with self.assertRaisesRegex(ValueError, 'SCHEMA'):
            history.load_claude(self.root)

    def test_changed_source_rejected(self):
        path = self.root / self.data['entries'][0]['source']
        path.write_bytes(path.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'SOURCE_CHANGED'):
            history.load_claude(self.root)

    def test_changed_target_hash_rejected(self):
        self.data['target_sha256'] = '0' * 64
        self.save()
        with self.assertRaisesRegex(ValueError, 'TARGET_CHANGED'):
            history.load_claude(self.root)

    def test_restored_adapter_makes_ledger_stale(self):
        path = self.root / history.CLAUDE_TARGET
        path.parent.mkdir(parents=True)
        path.write_text('synthetic', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'STALE'):
            history.load_claude(self.root)

    def test_unavailable_git_is_blocked(self):
        with patch.object(history, 'git', side_effect=ValueError('HISTORICAL_GIT_UNAVAILABLE')):
            with self.assertRaisesRegex(ValueError, 'GIT_UNAVAILABLE'):
                history.load_claude(self.root)


if __name__ == "__main__":
    unittest.main()
