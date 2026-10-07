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


if __name__ == "__main__":
    unittest.main()
