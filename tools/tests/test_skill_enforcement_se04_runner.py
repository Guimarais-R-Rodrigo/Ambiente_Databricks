from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_fonte" / ".assistant"
SKILL = "hub-ml-eda-profissional"
SOURCE_SKILL = SOURCE_ASSISTANT / "skills" / SKILL
RUNNER_PATH = SOURCE_SKILL / "scripts" / "run.py"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))

runner_spec = importlib.util.spec_from_file_location("sef_se04_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(runner_spec)
assert runner_spec and runner_spec.loader
sys.modules[runner_spec.name] = runner
runner_spec.loader.exec_module(runner)


DEFAULT_CONTEXT = {
    "local_sample_required": True,
    "tabular_preview_required": True,
    "numeric_columns": 4,
    "numeric_distributions_requested": True,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": True,
}


class SkillEnforcementSE04RunnerTests(unittest.TestCase):
    def run_runner(self, *, context=None, result=None, numeric_columns=4):
        business_result = {"metric": 1} if result is None else result
        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(numeric_columns, "synthetic_schema"),
        ), mock.patch.object(
            runner,
            "_default_quick_profile",
            return_value=business_result,
        ):
            return runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT if context is None else context),
                assistant_root=SOURCE_ASSISTANT,
            )

    def test_release_manifest_protects_receipt_engine_and_matches_blobs(self):
        manifest = json.loads((SOURCE_SKILL / "release_manifest.json").read_text(encoding="utf-8"))
        roles = {item["role"]: item for item in manifest["artifacts"]}
        self.assertIn("receipt_engine", roles)
        self.assertEqual(
            "hub_scripts/skill_execution/receipt/__init__.py",
            roles["receipt_engine"]["path"],
        )
        for artifact in manifest["artifacts"]:
            target = SOURCE_ASSISTANT / artifact["path"]
            self.assertTrue(target.is_file(), artifact["path"])
            self.assertEqual(artifact["git_blob_sha1"], runner._git_blob_sha1(target))

    def test_r01_runner_emits_receipt_and_current_release_verifies_valid(self):
        payload = self.run_runner(result={"rows": 10, "columns": 4})
        self.assertEqual("PASS", payload["trace"]["status"])
        self.assertEqual([runner.PROTECTED_PRIMITIVE_ID], payload["trace"]["resources_completed"])
        self.assertIsInstance(payload["receipt"], dict)
        self.assertEqual("1.0", payload["receipt"]["receipt_version"])
        self.assertEqual("PASS", payload["receipt"]["canonical_compliance"])
        verification = runner.verify_receipt(
            payload,
            expected_run_id=payload["trace"]["run_id"],
            assistant_root=SOURCE_ASSISTANT,
        )
        self.assertEqual("VALID", verification["status"])
        self.assertTrue(verification["valid"])

    def test_r05_receipt_tamper_is_invalid(self):
        payload = self.run_runner()
        payload["receipt"]["writes_performed"] = True
        verification = runner.verify_receipt(payload, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("INVALID", verification["status"])
        self.assertFalse(verification["valid"])

    def test_r06_output_tamper_is_incompatible(self):
        payload = self.run_runner(result={"metric": 1})
        payload["result"] = {"metric": 999}
        verification = runner.verify_receipt(payload, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("INCOMPATIBLE", verification["status"])

    def test_r07_previous_run_receipt_is_stale_against_current_run(self):
        old = self.run_runner(result={"metric": 1})
        current = self.run_runner(result={"metric": 1})
        verification = runner.verify_receipt(
            old,
            expected_run_id=current["trace"]["run_id"],
            assistant_root=SOURCE_ASSISTANT,
        )
        self.assertEqual("STALE_REPLAYED", verification["status"])

    def test_r10_provenance_conflict_blocks_and_emits_no_receipt(self):
        context = dict(DEFAULT_CONTEXT, numeric_columns=0)
        payload = self.run_runner(context=context, numeric_columns=4)
        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertIsNone(payload["receipt"])
        self.assertEqual([], payload["trace"]["resources_completed"])

    def test_r12_primitive_failure_emits_no_receipt_and_no_completion(self):
        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(4, "synthetic_schema"),
        ), mock.patch.object(
            runner,
            "_default_quick_profile",
            side_effect=RuntimeError("synthetic failure"),
        ):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )
        self.assertEqual("FAIL", payload["trace"]["status"])
        self.assertIsNone(payload["receipt"])
        self.assertEqual([runner.PROTECTED_PRIMITIVE_ID], payload["trace"]["resources_called"])
        self.assertEqual([], payload["trace"]["resources_completed"])
        self.assertFalse(payload["trace"]["fallback_used"])

    def test_manual_output_without_receipt_is_absent_not_canonical(self):
        manual = {"result": {"metric": 1}}
        verification = runner.verify_receipt(manual, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("ABSENT", verification["status"])
        self.assertFalse(verification["valid"])
        self.assertFalse(runner.is_canonically_compliant(manual))

    def test_se05_postflight_is_separate_from_se04_runner(self):
        execution_dir = SOURCE_ASSISTANT / "hub_scripts" / "skill_execution"
        self.assertTrue((execution_dir / "postflight" / "__init__.py").is_file())
        self.assertTrue((SOURCE_SKILL / "scripts" / "run_enforced.py").is_file())
        self.assertTrue((SOURCE_SKILL / "scripts" / "postflight.py").is_file())
        self.assertFalse((execution_dir / "postflight.py").exists())
        runner_text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("build_postflight", runner_text)
        self.assertNotIn("completion_authorized", runner_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
