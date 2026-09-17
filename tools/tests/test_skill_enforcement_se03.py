from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
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

runner_spec = importlib.util.spec_from_file_location("sef_se03_runner", RUNNER_PATH)
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


def _copy_minimal_release(root: Path, *, include_primitive: bool) -> Path:
    assistant_root = root / ".assistant"
    target_skill = assistant_root / "skills" / SKILL
    target_skill.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_SKILL, target_skill)

    source_engine = SOURCE_ASSISTANT / "hub_scripts" / "skill_execution"
    target_engine = assistant_root / "hub_scripts" / "skill_execution"
    target_engine.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_engine, target_engine)

    if include_primitive:
        source_primitive = SOURCE_ASSISTANT / "hub_scripts" / "quick_profile"
        target_primitive = assistant_root / "hub_scripts" / "quick_profile"
        shutil.copytree(source_primitive, target_primitive)

    return assistant_root


class SkillEnforcementSE03FirstSliceTests(unittest.TestCase):
    def test_manifest_fingerprints_match_source_release(self) -> None:
        manifest = json.loads((SOURCE_SKILL / "release_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1", manifest["manifest_version"])
        self.assertEqual("git_blob_sha1", manifest["algorithm"])
        self.assertEqual(SKILL, manifest["skill"])
        for artifact in manifest["artifacts"]:
            target = SOURCE_ASSISTANT / artifact["path"]
            self.assertTrue(target.is_file(), artifact["path"])
            self.assertEqual(artifact["git_blob_sha1"], runner._git_blob_sha1(target))

    def test_public_run_signature_has_no_primitive_injection_hook(self) -> None:
        import inspect

        signature = inspect.signature(runner.run)
        self.assertNotIn("primitive_invoker", signature.parameters)
        self.assertNotIn("invoker", signature.parameters)

    def test_e01_happy_path_uses_runner_primitive_and_valid_trace(self) -> None:
        calls: list[dict] = []

        def fake_profile(table_name: str, **kwargs):
            calls.append({"table_name": table_name, **kwargs})
            return {"table": table_name, "ok": True}

        with mock.patch.object(runner, "_default_quick_profile", side_effect=fake_profile):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )

        trace = payload["trace"]
        self.assertEqual("PASS", trace["status"])
        self.assertEqual("PASS", trace["preflight_status"])
        self.assertFalse(trace["fallback_used"])
        self.assertFalse(trace["writes_performed"])
        self.assertEqual([runner.PROTECTED_PRIMITIVE_ID], trace["resources_called"])
        self.assertEqual(1, len(calls))
        self.assertEqual("catalog.schema.synthetic_table", calls[0]["table_name"])
        self.assertTrue(runner.is_canonically_compliant(payload))

    def test_e04_missing_required_primitive_aborts_before_core(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            assistant_root = _copy_minimal_release(Path(td), include_primitive=False)
            with mock.patch.object(runner, "_default_quick_profile") as mocked_profile:
                payload = runner.run(
                    "catalog.schema.synthetic_table",
                    dict(DEFAULT_CONTEXT),
                    assistant_root=assistant_root,
                )
                mocked_profile.assert_not_called()

        trace = payload["trace"]
        self.assertEqual("BLOCKED", trace["status"])
        self.assertEqual("NOT_RUN", trace["preflight_status"])
        self.assertTrue(
            any(issue["code"] == "RELEASE_INTEGRITY_MISMATCH" for issue in trace["blocking_issues"])
        )
        self.assertFalse(runner.is_canonically_compliant(payload))

    def test_e05_tampered_primitive_fails_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            assistant_root = _copy_minimal_release(Path(td), include_primitive=True)
            primitive = assistant_root / "hub_scripts" / "quick_profile" / "quick_profile.py"
            primitive.write_text(primitive.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")

            with mock.patch.object(runner, "_default_quick_profile") as mocked_profile:
                payload = runner.run(
                    "catalog.schema.synthetic_table",
                    dict(DEFAULT_CONTEXT),
                    assistant_root=assistant_root,
                )
                mocked_profile.assert_not_called()

        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertTrue(
            any(issue["code"] == "RELEASE_INTEGRITY_MISMATCH" for issue in payload["trace"]["blocking_issues"])
        )

    def test_preflight_blocked_stops_core(self) -> None:
        context = dict(DEFAULT_CONTEXT)
        context.pop("visual_diagnostics_requested")

        with mock.patch.object(runner, "_default_quick_profile") as mocked_profile:
            payload = runner.run(
                "catalog.schema.synthetic_table",
                context,
                assistant_root=SOURCE_ASSISTANT,
            )
            mocked_profile.assert_not_called()

        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertEqual("BLOCKED", payload["trace"]["preflight_status"])
        self.assertFalse(payload["trace"]["fallback_used"])

    def test_e06_primitive_failure_fails_without_fallback(self) -> None:
        with mock.patch.object(
            runner,
            "_default_quick_profile",
            side_effect=RuntimeError("synthetic primitive failure"),
        ):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )

        trace = payload["trace"]
        self.assertEqual("FAIL", trace["status"])
        self.assertEqual([runner.PROTECTED_PRIMITIVE_ID], trace["resources_called"])
        self.assertFalse(trace["fallback_used"])
        self.assertTrue(
            any(issue["code"] == "REQUIRED_PRIMITIVE_FAILED" for issue in trace["blocking_issues"])
        )
        self.assertFalse(runner.is_canonically_compliant(payload))

    def test_e07_direct_call_without_runner_fails_compliance(self) -> None:
        manual_output = {"result": {"table": "catalog.schema.synthetic_table", "ok": True}}
        self.assertFalse(runner.is_canonically_compliant(manual_output))

    def test_invalid_table_name_blocks_before_core(self) -> None:
        with mock.patch.object(runner, "_default_quick_profile") as mocked_profile:
            payload = runner.run(
                "",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )
            mocked_profile.assert_not_called()

        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertTrue(any(issue["code"] == "RUN_INPUT_INVALID" for issue in payload["trace"]["blocking_issues"]))

    def test_trace_does_not_copy_business_result(self) -> None:
        with mock.patch.object(
            runner,
            "_default_quick_profile",
            return_value={"secret_value": "do-not-copy"},
        ):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )

        self.assertNotIn("secret_value", json.dumps(payload["trace"], ensure_ascii=False))
        self.assertEqual("do-not-copy", payload["result"]["secret_value"])

    def test_structural_trace_is_deterministic_except_run_id(self) -> None:
        def fake_profile(table_name: str, **kwargs):
            return {"table": table_name}

        with mock.patch.object(runner, "_default_quick_profile", side_effect=fake_profile):
            first = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )["trace"]
            second = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )["trace"]

        self.assertNotEqual(first["run_id"], second["run_id"])
        first = dict(first)
        second = dict(second)
        first.pop("run_id")
        second.pop("run_id")
        self.assertEqual(first, second)

    def test_se04_se05_artifacts_remain_absent(self) -> None:
        execution_dir = SOURCE_ASSISTANT / "hub_scripts" / "skill_execution"
        self.assertFalse((execution_dir / "receipt.py").exists())
        self.assertFalse((execution_dir / "postflight.py").exists())


if __name__ == "__main__":
    unittest.main()
