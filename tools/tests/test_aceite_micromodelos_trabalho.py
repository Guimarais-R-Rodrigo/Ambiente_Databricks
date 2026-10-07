"""Aceite do Hub extraído fora do checkout, com runtime Micromodelos integrado."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ACCEPTANCE = REPO / "tools" / "aceite_micromodelos_trabalho.py"
PRODUCT = REPO / "ambiente_databricks" / ".assistant" / "hub_micromodelos"


class ExtractedProductAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mm integrated package ")
        cls.base = Path(cls.temporary.name)
        cls.package = cls.base / "extracted hub"
        destination = cls.package / ".assistant" / "hub_micromodelos"
        entries = []
        for source in sorted(PRODUCT.rglob("*")):
            if not source.is_file() or "__pycache__" in source.parts:
                continue
            rel = source.relative_to(PRODUCT)
            target = destination / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            raw = source.read_bytes()
            target.write_bytes(raw)
            entries.append({"path": ".assistant/hub_micromodelos/" + rel.as_posix(),
                            "sha256": hashlib.sha256(raw).hexdigest(),
                            "bytes": len(raw), "object_type": "FILE"})
        cls.commit = "0" * 40
        manifest = {"schema_version": 2, "source_commit": cls.commit,
                    "worktree_dirty": False, "files": entries}
        raw = json.dumps(manifest, ensure_ascii=False).encode("utf-8")
        (cls.package / "MANIFEST.json").write_bytes(raw)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def _invoke(self, *flags: str, no_site: bool = False) -> tuple[int, dict]:
        command = [sys.executable]
        if no_site:
            command.append("-S")
        command += ["-B", str(ACCEPTANCE), "--package-root", str(self.package), *flags]
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment["PYTHONUTF8"] = "1"
        process = subprocess.run(command, cwd=self.base, env=environment,
                                 capture_output=True, text=True, timeout=90, check=False)
        self.assertEqual("", process.stderr, process.stderr)
        return process.returncode, json.loads(process.stdout)

    def test_integrated_synthetic_acceptance(self) -> None:
        code, report = self._invoke()
        self.assertEqual(0, code)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(self.commit, report["source_commit"])
        self.assertEqual(6, report["synthetic_summary"]["population"])
        self.assertEqual(4, report["synthetic_summary"]["score_count"])
        self.assertTrue(all(stage["status"] == "PASS" for stage in report["stages"]))
        self.assertEqual("NOT_RUN", report["limits"]["metadata_real"])
        self.assertEqual("NOT_EXECUTED", report["limits"]["publication"])

    def test_corrupt_module_fails_before_import(self) -> None:
        target = self.package / ".assistant/hub_micromodelos/execucao/execucao.py"
        raw = target.read_bytes()
        try:
            target.write_bytes(raw + b"\n# corruption\n")
            code, report = self._invoke()
            self.assertEqual(1, code)
            self.assertEqual("MICROMODELO_FILE_HASH_MISMATCH", report["stages"][0]["detail"])
            self.assertIsNone(report["synthetic_summary"])
        finally:
            target.write_bytes(raw)

    def test_missing_contract_fails_integrity(self) -> None:
        target = self.package / ".assistant/hub_micromodelos/contratos/micromodelo.schema.json"
        raw = target.read_bytes()
        try:
            target.unlink()
            code, report = self._invoke()
            self.assertEqual(1, code)
            self.assertEqual("MICROMODELO_FILE_MISSING", report["stages"][0]["detail"])
        finally:
            target.write_bytes(raw)

    def test_missing_dependency_stops_before_import(self) -> None:
        code, report = self._invoke(no_site=True)
        self.assertEqual(1, code)
        self.assertEqual("PASS", report["stages"][0]["status"])
        self.assertIn("MISSING_DEPENDENCIES", report["stages"][-1]["detail"])

    def test_destination_flags_do_not_connect(self) -> None:
        code, report = self._invoke("--testar-mlflow", "--testar-metadata")
        self.assertEqual(1, code)
        self.assertEqual("UNAVAILABLE", report["stages"][-1]["status"])
        self.assertIsNone(report["synthetic_summary"])


if __name__ == "__main__":
    unittest.main()
