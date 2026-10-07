"""Current read-only diagnostics; the frozen v1 self-test is not rewritten."""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import mm01_local_certify as cert

ROOT = Path(__file__).resolve().parents[2]


class MM01FrozenDiagnosticsTests(unittest.TestCase):
    def frozen_fixture(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for rel in cert.WORKFLOW_SOURCES:
            data = subprocess.check_output(
                ["git", "show", cert.WORKFLOW_PIN_ORIGIN_SHA + ":" + rel], cwd=ROOT)
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=Codex", "-c", "user.email=codex@openai.com",
                        "commit", "-qm", "Synthetic frozen workflow fixture"], cwd=root, check=True)

    def test_frozen_inputs_match_without_claiming_certification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.frozen_fixture(root)
            report = cert.diagnose_frozen_workflows(root)
            self.assertEqual("FROZEN_INPUTS_MATCH", report["status"])
            self.assertEqual("NOT_RUN", report["certification_status"])
            self.assertEqual("HISTORICAL_FROZEN", report["route_status"])
            self.assertEqual([], report["incompatible_workflows"])
            self.assertTrue(report["worktree_clean"])
            self.assertEqual(set(cert.WORKFLOW_SOURCES), set(report["workflows"]))
            self.assertEqual(len(cert.WORKFLOW_SOURCES), len(cert.check_workflow_drift(root)))

    def test_diagnostic_reports_every_drift_while_certification_still_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.frozen_fixture(root)
            for rel in cert.WORKFLOW_SOURCES:
                with (root / rel).open("a", encoding="utf-8") as stream:
                    stream.write("\n# Synthetic drift, not a new approved gate\n")
            report = cert.diagnose_frozen_workflows(root)
            self.assertEqual("INCOMPATIBLE_WITH_FROZEN_V1", report["status"])
            self.assertEqual(list(cert.WORKFLOW_SOURCES), report["incompatible_workflows"])
            self.assertFalse(report["worktree_clean"])
            self.assertTrue(all("FROZEN_BLOB_MISMATCH" in item["issues"]
                                for item in report["workflows"].values()))
            with self.assertRaisesRegex(cert.CertificationError, "--diagnose"):
                cert.check_workflow_drift(root)

    def test_missing_and_symlink_workflows_do_not_hide_other_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.frozen_fixture(root)
            missing, linked = cert.WORKFLOW_SOURCES[:2]
            (root / missing).unlink()
            (root / linked).unlink()
            (root / linked).symlink_to(root / cert.WORKFLOW_SOURCES[2])
            report = cert.diagnose_frozen_workflows(root)
            self.assertEqual([missing, linked], report["incompatible_workflows"])
            self.assertEqual(["WORKFLOW_MISSING_OR_NOT_FILE"], report["workflows"][missing]["issues"])
            self.assertEqual(["WORKFLOW_SYMLINK"], report["workflows"][linked]["issues"])
            self.assertIsNone(report["workflows"][linked]["actual_git_blob"])

    def test_diagnostic_cli_never_bootstraps_runs_or_writes_output(self):
        for incompatible, expected_exit in ((["synthetic"], 1), ([], 0)):
            with self.subTest(incompatible=incompatible), \
                    mock.patch.object(cert, "diagnose_frozen_workflows", return_value={
                        "incompatible_workflows": incompatible, "certification_status": "NOT_RUN"}), \
                    mock.patch.object(cert, "base_runtime_preflight", side_effect=AssertionError("bootstrap")), \
                    mock.patch.object(cert, "run_step", side_effect=AssertionError("execution")), \
                    mock.patch.object(cert.Path, "mkdir", side_effect=AssertionError("write")), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(expected_exit, cert.main(["--diagnose"]))
                self.assertEqual("NOT_RUN", json.loads(output.getvalue())["certification_status"])

    def test_describe_labels_frozen_plan_and_procedure(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, cert.main(["--describe"]))
        report = json.loads(output.getvalue())
        self.assertEqual("HISTORICAL_FROZEN", report["route_status"])
        self.assertEqual("NOT_RUN", report["certification_status"])
        self.assertTrue((ROOT / report["current_procedure"]).is_file())
        self.assertEqual(cert.WORKFLOW_PIN_ORIGIN_SHA, report["workflow_pin_origin_sha"])

    def test_inspection_modes_cannot_be_combined(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as result:
            cert.parse_args(["--describe", "--diagnose"])
        self.assertEqual(2, result.exception.code)


if __name__ == "__main__":
    unittest.main()
