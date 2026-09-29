"""O pacote final deve rodar depois da extração, sem imports do checkout."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import kit_micromodelos_trabalho as kit


class MicromodelosWorkKitTests(unittest.TestCase):
    def _extract(self, base: Path) -> tuple[Path, Path, dict]:
        archive = base / "micromodelos.zip"
        with (patch.object(kit, "_identity", return_value="a" * 40),
              patch.object(kit, "_assert_commit_sources")):
            built = kit.build(archive)
        extracted = base / "pasta com espaços" / "pacote"
        extracted.mkdir(parents=True)
        with zipfile.ZipFile(archive) as bundle:
            for info in bundle.infolist():
                self.assertFalse(info.filename.startswith("/"))
                self.assertNotIn("..", Path(info.filename).parts)
            bundle.extractall(extracted)
        return archive, extracted, built

    def test_extracted_zip_has_closed_allowlist_and_runs_synthetic_acceptance(self):
        with tempfile.TemporaryDirectory(prefix="mm-kit-") as temp:
            base = Path(temp)
            archive, extracted, built = self._extract(base)
            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(set(bundle.namelist()),
                                 set(kit.RUNTIME_FILES) | {
                                     "runtime/" + rel.removeprefix("ambiente_fonte/.assistant/")
                                     for rel in kit.OPTIONAL_TRACKING
                                 } | set(kit.GENERATED_FILES) | {kit.MANIFEST})
            verified = kit.verify(extracted)
            self.assertEqual("PASS", verified["status"])
            self.assertEqual(built["source_commit"], verified["source_commit"])
            self.assertEqual(built["manifest_sha256"], verified["manifest_sha256"])
            self.assertFalse(any("Ambiente_Antigo" in name for name in
                                 zipfile.ZipFile(archive).namelist()))
            env = dict(os.environ)
            env["PYTHONPATH"] = ""
            env["PYTHONIOENCODING"] = "utf-8"
            runner = extracted / "tools/aceite_micromodelos_trabalho.py"
            result = subprocess.run(
                [sys.executable, "-B", str(runner), "--package-root", str(extracted)],
                cwd=base, env=env, capture_output=True, text=True,
                encoding="utf-8", timeout=60,
            )
            output = (result.stderr or "") + (result.stdout or "")
            self.assertEqual(0, result.returncode, output)
            self.assertNotIn(str(ROOT), output)
            self.assertEqual("PASS", kit.verify(extracted)["status"])

    def test_missing_corrupt_extra_and_cache_behavior(self):
        with tempfile.TemporaryDirectory(prefix="mm-kit-") as temp:
            _, extracted, _ = self._extract(Path(temp))
            target = extracted / "tools/micromodelo_mm01_contract.py"
            original = target.read_bytes()
            target.write_bytes(original + b"\n# changed\n")
            with self.assertRaisesRegex(ValueError, "KIT_FILE_HASH_MISMATCH"):
                kit.verify(extracted)
            target.write_bytes(original)
            target.unlink()
            with self.assertRaisesRegex(ValueError, "KIT_FILE_MISSING_OR_UNSAFE"):
                kit.verify(extracted)
            target.write_bytes(original)
            extra = extracted / "tools/unlisted.py"
            extra.write_text("print('unlisted')", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "KIT_EXTRA_OR_MISSING"):
                kit.verify(extracted)
            extra.unlink()
            cache = extracted / "tools/__pycache__"
            cache.mkdir()
            (cache / "micromodelo_mm01_contract.cpython-312.pyc").write_bytes(b"cache")
            self.assertEqual("PASS", kit.verify(extracted)["status"])

    def test_manifest_tamper_and_no_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="mm-kit-") as temp:
            archive, extracted, _ = self._extract(Path(temp))
            with self.assertRaisesRegex(FileExistsError, "KIT_OUTPUT_EXISTS"):
                kit.build(archive)
            manifest = extracted / "manifest.json"
            content = json.loads(manifest.read_text(encoding="utf-8"))
            content["files"].pop("tools/micromodelo_mm01_contract.py")
            manifest.write_text(json.dumps(content), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "KIT_MANIFEST_FILESET"):
                kit.verify(extracted)

    def test_rejects_symlinked_allowlisted_source(self):
        with tempfile.TemporaryDirectory(prefix="mm-kit-") as temp:
            root = Path(temp) / "fake-repo"
            for rel in (*kit.RUNTIME_FILES, *kit.OPTIONAL_TRACKING):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic", encoding="utf-8")
            target = root / kit.RUNTIME_FILES[0]
            target.unlink()
            external = Path(temp) / "outside.txt"
            external.write_text("outside", encoding="utf-8")
            try:
                target.symlink_to(external)
            except OSError:
                self.skipTest("symlink indisponível neste Windows")
            with self.assertRaisesRegex(ValueError, "KIT_SOURCE_UNSAFE"):
                kit._entries(root)

    def test_build_rejects_source_changed_after_git_status_check(self):
        with tempfile.TemporaryDirectory(prefix="mm-kit-race-") as temp:
            archive = Path(temp) / "changed.zip"
            original_entries = kit._entries(ROOT)
            raced_entries = dict(original_entries)
            raced_entries[kit.RUNTIME_FILES[0]] += b"\n# concurrent edit\n"
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            with (patch.object(kit, "_identity", return_value=commit),
                  patch.object(kit, "_entries", return_value=raced_entries)):
                with self.assertRaisesRegex(ValueError, "KIT_SOURCE_COMMIT_MISMATCH"):
                    kit.build(archive)
            self.assertFalse(archive.exists())


if __name__ == "__main__":
    unittest.main()
