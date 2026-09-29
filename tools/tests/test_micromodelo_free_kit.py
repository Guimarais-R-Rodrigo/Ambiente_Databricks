"""Transporte Free executa isolado sem imports do checkout de desenvolvimento."""
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
import micromodelo_free_kit as kit


class FreeKitTests(unittest.TestCase):
    def test_build_and_execute_from_isolated_package(self):
        with tempfile.TemporaryDirectory(prefix="mm-free-kit-") as temp:
            output = Path(temp) / "package"
            built = kit.build(output)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("E1_PREPARED_SYNTHETIC", manifest["kind"])
            self.assertEqual("NOT_RUN", manifest["e1_execution"])
            self.assertEqual(set(manifest["files"]), {
                p.relative_to(output).as_posix() for p in output.rglob("*")
                if p.is_file() and p.name != "manifest.json"
            })
            with zipfile.ZipFile(built["zip"]) as archive:
                self.assertIn("RUN_FREE.py", archive.namelist())
            env = dict(os.environ)
            env["PYTHONPATH"] = ""
            run = subprocess.run([sys.executable, "-B", "RUN_FREE.py"], cwd=output,
                                 env=env, capture_output=True, text=True,
                                 encoding="utf-8", timeout=30)
            self.assertEqual(0, run.returncode, run.stderr)
            line = next(x for x in run.stdout.splitlines()
                        if x.startswith("SYNTHETIC_CODE_LAB "))
            result = json.loads(line.removeprefix("SYNTHETIC_CODE_LAB "))
            self.assertEqual({"TRUE": 1, "FALSE": 2, "INDETERMINADO": 3},
                             result["counts"])
            self.assertEqual("RECORD_SEPARATELY", result["environment_claim"])

    def test_never_overwrites_existing_output(self):
        with tempfile.TemporaryDirectory(prefix="mm-free-kit-") as temp:
            output = Path(temp) / "package"
            output.mkdir()
            with self.assertRaises(FileExistsError):
                kit.build(output)

    def test_product_transport_uses_exact_allowlist_and_rejects_links(self):
        with tempfile.TemporaryDirectory(prefix="mm-free-kit-source-") as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            for rel in (*kit.FILES, *kit.PRODUCT_FILES):
                source = root / rel
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text("synthetic", encoding="utf-8")
            extra = root / "ambiente_fonte/.assistant/hub_prompts/micromodelo_novo/segredo.txt"
            extra.write_text("nunca transportar", encoding="utf-8")
            with patch.object(kit, "ROOT", root):
                output = Path(temp) / "package"
                kit.build(output)
                self.assertFalse(any(p.name == "segredo.txt" for p in output.rglob("*")))
                listed = root / kit.PRODUCT_FILES[0]
                listed.unlink()
                try:
                    listed.symlink_to(extra)
                except OSError:
                    return  # criação de symlink pode estar desabilitada no Windows
                with self.assertRaisesRegex(FileNotFoundError, "KIT_SOURCE_UNSAFE"):
                    kit.build(Path(temp) / "package2")


if __name__ == "__main__":
    unittest.main()
