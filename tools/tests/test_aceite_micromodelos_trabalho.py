"""Aceite do artefato extraído, executado sem imports do checkout no subprocesso."""
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
sys.path.insert(0, str(REPO / "tools"))
import kit_micromodelos_trabalho as kit


class ExtractedPackageAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mm acceptance package ")
        cls.base = Path(cls.temporary.name)
        cls.package = cls.base / "extracted package"
        cls.package.mkdir()
        entries = kit._entries(REPO)
        for relative, raw in entries.items():
            destination = cls.package / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
        manifest = {
            "kind": kit.KIND, "version": kit.VERSION,
            "source_commit": "0" * 40, "e2_execution": "NOT_RUN",
            "files": {relative: {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}
                      for relative, raw in sorted(entries.items())},
        }
        (cls.package / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def _invoke(self, *flags: str, no_site: bool = False) -> tuple[int, dict]:
        command = [sys.executable]
        if no_site:
            command.append("-S")
        command += ["-B", str(self.package / "tools" / "aceite_micromodelos_trabalho.py"),
                    "--package-root", str(self.package), *flags]
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment["PYTHONUTF8"] = "1"
        process = subprocess.run(command, cwd=self.base, env=environment,
                                 capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual("", process.stderr, process.stderr)
        return process.returncode, json.loads(process.stdout)

    def test_complete_synthetic_acceptance_and_repeat_from_extracted_package(self) -> None:
        for _ in range(2):
            code, report = self._invoke()
            self.assertEqual(0, code)
            self.assertEqual("PASS", report["status"])
            self.assertEqual("0" * 40, report["source_commit"])
            self.assertEqual(6, report["synthetic_summary"]["population"])
            self.assertEqual(4, report["synthetic_summary"]["score_count"])
            self.assertTrue(all(stage["status"] == "PASS" for stage in report["stages"]))
            self.assertIn("metadata_discovery", {stage["name"] for stage in report["stages"]})
            self.assertEqual("NOT_RUN", report["limits"]["mlflow"])
            self.assertEqual("NOT_RUN", report["limits"]["metadata_real"])
            self.assertEqual("NOT_EXECUTED", report["limits"]["publication"])

    def test_notebook_style_run_without_shell_entrypoint(self) -> None:
        program = (
            "import json,sys; from pathlib import Path; "
            "root=Path(sys.argv[1]); sys.path.insert(0,str(root/'tools')); "
            "from aceite_micromodelos_trabalho import run; "
            "print(json.dumps(run(root),sort_keys=True))"
        )
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment["PYTHONUTF8"] = "1"
        process = subprocess.run([sys.executable, "-B", "-c", program, str(self.package)],
                                 cwd=self.base, env=environment, capture_output=True,
                                 text=True, timeout=60, check=False)
        self.assertEqual(0, process.returncode, process.stderr)
        self.assertEqual("PASS", json.loads(process.stdout)["status"])

    def test_corrupt_module_fails_integrity_before_import(self) -> None:
        target = self.package / "tools" / "micromodelo_mm09_lab.py"
        original = target.read_bytes()
        try:
            target.write_bytes(original + b"\n# corruption\n")
            code, report = self._invoke()
            self.assertEqual(1, code)
            self.assertEqual("FAIL", report["stages"][0]["status"])
            self.assertEqual("KIT_FILE_HASH_MISMATCH", report["stages"][0]["detail"])
            self.assertIsNone(report["synthetic_summary"])
        finally:
            target.write_bytes(original)

    def test_missing_module_fails_integrity(self) -> None:
        target = self.package / "tools" / "micromodelo_mm10_handoff.py"
        original = target.read_bytes()
        try:
            target.unlink()
            code, report = self._invoke()
            self.assertEqual(1, code)
            self.assertEqual("KIT_FILE_MISSING_OR_UNSAFE", report["stages"][0]["detail"])
        finally:
            target.write_bytes(original)

    def test_missing_dependency_reports_capability_without_importing_modules(self) -> None:
        code, report = self._invoke(no_site=True)
        self.assertEqual(1, code)
        self.assertEqual("PASS", report["stages"][0]["status"])
        self.assertIn("MISSING_DEPENDENCIES", report["stages"][-1]["detail"])
        self.assertIsNone(report["synthetic_summary"])

    def test_destination_flags_do_not_connect_or_claim_execution(self) -> None:
        code, report = self._invoke("--testar-mlflow", "--testar-metadata")
        self.assertEqual(1, code)
        self.assertEqual("UNAVAILABLE", report["stages"][-1]["status"])
        self.assertEqual("NOT_RUN", report["limits"]["mlflow"])
        self.assertEqual("NOT_RUN", report["limits"]["metadata_real"])
        self.assertIsNone(report["synthetic_summary"])


if __name__ == "__main__":
    unittest.main()
