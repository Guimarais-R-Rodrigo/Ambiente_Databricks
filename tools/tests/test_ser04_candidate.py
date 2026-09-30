from __future__ import annotations

import copy
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SER04CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request = json.loads((SKILL / "fixtures/ks_separated_request.json").read_text(encoding="utf-8"))
        cls.preflight = load("_ser04_test_preflight", SKILL / "scripts/preflight.py")
        cls.runner = load("_ser04_test_runner", SKILL / "scripts/run.py")
        cls.verifier = load("_ser04_test_verifier", SKILL / "scripts/verify.py")

    def test_fixed_combinatorial_oracle_and_receipt(self):
        # For n=m=4 with disjoint ordered supports, D=1. Exactly two
        # of C(8,4) label assignments achieve D=1 under H0.
        p_oracle = 2 / math.comb(8, 4)
        payload = self.runner.run(self.request, run_id="SER04-KS-ORACLE-1")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        self.assertAlmostEqual(payload["result"]["statistic_D"], 1.0)
        self.assertAlmostEqual(payload["result"]["p_value"], p_oracle)
        self.assertEqual(payload["result"]["decision"], "REJECT_H0")
        self.assertIsNone(payload["result"]["confidence_interval"])
        self.assertTrue(self.verifier.verify(
            payload, expected_request=self.request, expected_run_id="SER04-KS-ORACLE-1",
            expected_statistic=1.0, expected_p_value=p_oracle)["valid"])

    def test_interleaved_distributions_do_not_reject_h0(self):
        request = copy.deepcopy(self.request)
        request.update(reference=[1, 3, 5, 7], comparison=[2, 4, 6, 8])
        payload = self.runner.run(request, run_id="SER04-INTERLEAVED")
        self.assertEqual("PASS", payload["status"], payload)
        # D=1/4 is the minimal possible ECDF distance for these sample sizes:
        # every labeling has D >= 1/4, so the exact two-sided tail is one.
        self.assertEqual("DO_NOT_REJECT_H0", payload["result"]["decision"])
        self.assertTrue(self.verifier.verify(
            payload, expected_request=request, expected_run_id="SER04-INTERLEAVED",
            expected_statistic=0.25, expected_p_value=1.0)["valid"])

    def test_preflight_rejects_unsupported_design_and_invalid_samples(self):
        changes = (
            {"synthetic": False},
            {"independence": "PAIRED"},
            {"multiple_testing": "UNCORRECTED_TWENTY_TESTS"},
            {"reference": [1, 1, 2, 3]},
            {"comparison": [2, 5, 6, 7]},
            {"reference": [2**53 + i for i in range(4)],
             "comparison": [2**53 + i for i in range(4, 8)]},
            {"alpha": float("nan")},
            {"alpha": 0.0},
            {"extra": "unknown"},
        )
        for change in changes:
            with self.subTest(change=change):
                request = copy.deepcopy(self.request)
                request.update(change)
                result = self.preflight.preflight(request)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertFalse(result["helper_called"])
                self.assertIsNone(result["sef"])

    def test_float64_precision_loss_blocks_before_helper_call(self):
        request = copy.deepcopy(self.request)
        request["reference"] = [2**53 + i for i in range(4)]
        request["comparison"] = [2**53 + i for i in range(4, 8)]
        payload = self.runner.run(request, run_id="SER04-PRECISION-1")
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertIn("REFERENCE:FLOAT64_PRECISION_LOSS", payload["preflight"]["issues"])
        self.assertEqual(payload["trace"]["resources_called"], [])
        self.assertIsNone(payload["receipt"])
    def test_verifier_rejects_replay_and_tampered_oracle(self):
        payload = self.runner.run(self.request, run_id="SER04-KS-REPLAY-1")
        self.assertEqual(payload["status"], "PASS", payload["trace"]["blocking_issues"])
        oracle = 2 / math.comb(8, 4)
        bad_run = self.verifier.verify(payload, expected_request=self.request,
                                       expected_run_id="SER04-OTHER",
                                       expected_statistic=1.0, expected_p_value=oracle)
        self.assertFalse(bad_run["valid"])
        bad_oracle = self.verifier.verify(payload, expected_request=self.request,
                                          expected_run_id="SER04-KS-REPLAY-1",
                                          expected_statistic=0.5, expected_p_value=oracle)
        self.assertFalse(bad_oracle["valid"])
        altered = copy.deepcopy(payload)
        altered["result"]["p_value"] = 0.9
        tampered = self.verifier.verify(altered, expected_request=self.request,
                                        expected_run_id="SER04-KS-REPLAY-1",
                                        expected_statistic=1.0, expected_p_value=oracle)
        self.assertFalse(tampered["valid"])

    def test_verify_cli_requires_payload_and_reports_validation(self):
        run_id = "SER04-CLI-ROUNDTRIP-1"
        payload = self.runner.run(self.request, run_id=run_id)
        self.assertEqual("PASS", payload["status"], payload["trace"]["blocking_issues"])
        script = SKILL / "scripts/verify.py"
        with tempfile.TemporaryDirectory() as tmp:
            request_path = Path(tmp) / "request.json"
            payload_path = Path(tmp) / "payload.json"
            request_path.write_text(json.dumps(self.request), encoding="utf-8")
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            def invoke(*extra: str):
                return subprocess.run(
                    [sys.executable, "-B", str(script), "--payload", str(payload_path),
                     "--request", str(request_path), "--run-id", run_id,
                     "--expected-statistic", "1", "--expected-p-value", str(1 / 35),
                     *extra], capture_output=True, text=True, encoding="utf-8")

            valid = invoke()
            self.assertEqual(0, valid.returncode, valid.stderr)
            self.assertEqual("VALID", json.loads(valid.stdout)["status"])
            self.assertTrue(json.loads(valid.stdout)["valid"])

            missing_payload = subprocess.run(
                [sys.executable, "-B", str(script), "--request", str(request_path),
                 "--run-id", run_id, "--expected-statistic", "1",
                 "--expected-p-value", str(1 / 35)],
                capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(0, missing_payload.returncode)

            payload_path.write_text('{"status":"PASS","status":"PASS"}', encoding="utf-8")
            duplicate = invoke()
            self.assertEqual(1, duplicate.returncode)
            self.assertFalse(json.loads(duplicate.stdout)["valid"])

            payload_path.write_text(json.dumps(payload), encoding="utf-8")
            wrong_oracle = subprocess.run(
                [sys.executable, "-B", str(script), "--payload", str(payload_path),
                 "--request", str(request_path), "--run-id", run_id,
                 "--expected-statistic", "0.5", "--expected-p-value", str(1 / 35)],
                capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(1, wrong_oracle.returncode)
            self.assertIn("TRUSTED_ORACLE_MISMATCH:statistic_D",
                          json.loads(wrong_oracle.stdout)["issues"])


if __name__ == "__main__":
    unittest.main()
