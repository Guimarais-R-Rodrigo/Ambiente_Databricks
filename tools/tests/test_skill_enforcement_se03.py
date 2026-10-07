from __future__ import annotations

import importlib.util
import inspect
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_databricks" / ".assistant"
SKILL = "hub-ml-eda-profissional"
SOURCE_SKILL = SOURCE_ASSISTANT / "skills" / SKILL
RUNNER_PATH = SOURCE_SKILL / "scripts" / "run.py"
CERTIFIER_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "certify_local.py"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))

runner_spec = importlib.util.spec_from_file_location("sef_se03_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(runner_spec)
assert runner_spec and runner_spec.loader
sys.modules[runner_spec.name] = runner
runner_spec.loader.exec_module(runner)

certifier_spec = importlib.util.spec_from_file_location("sef_se03_certifier", CERTIFIER_PATH)
certifier = importlib.util.module_from_spec(certifier_spec)
assert certifier_spec and certifier_spec.loader
sys.modules[certifier_spec.name] = certifier
certifier_spec.loader.exec_module(certifier)


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


class SkillEnforcementSE03Tests(unittest.TestCase):
    def run_runner(
        self,
        *,
        context: dict | None = None,
        result: object | None = None,
        numeric_columns: int = 4,
        assistant_root: Path = SOURCE_ASSISTANT,
    ):
        business_result = (
            {"table": "catalog.schema.synthetic_table", "ok": True}
            if result is None
            else result
        )
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
                assistant_root=assistant_root,
            )

    def test_manifest_fingerprints_match_source_release(self) -> None:
        manifest = json.loads((SOURCE_SKILL / "release_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1", manifest["manifest_version"])
        self.assertEqual("git_blob_sha1", manifest["algorithm"])
        self.assertEqual(SKILL, manifest["skill"])
        for artifact in manifest["artifacts"]:
            target = SOURCE_ASSISTANT / artifact["path"]
            self.assertTrue(target.is_file(), artifact["path"])
            self.assertEqual(artifact["git_blob_sha1"], runner._git_blob_sha1(target))

    def test_e01_happy_path_uses_runner_primitive_and_valid_trace(self) -> None:
        calls: list[dict] = []

        def fake_profile(table_name: str, **kwargs):
            calls.append({"table_name": table_name, **kwargs})
            return {"table": table_name, "ok": True}

        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(4, "synthetic_schema"),
        ), mock.patch.object(runner, "_default_quick_profile", side_effect=fake_profile):
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
        self.assertEqual("runtime_derived", trace["context_provenance"]["numeric_columns"]["source"])
        self.assertEqual(1, len(calls))
        self.assertEqual("catalog.schema.synthetic_table", calls[0]["table_name"])
        self.assertTrue(runner.is_canonically_compliant(payload))

    def test_e02_shortcut_pressure_flag_does_not_change_canonical_path(self) -> None:
        context = dict(DEFAULT_CONTEXT, bypass_runner=True, shortcut_requested=True)
        payload = self.run_runner(context=context)
        self.assertEqual("PASS", payload["trace"]["status"])
        self.assertEqual(runner.CANONICAL_ENTRYPOINT, payload["trace"]["entrypoint"])
        self.assertEqual([runner.PROTECTED_PRIMITIVE_ID], payload["trace"]["resources_called"])
        self.assertFalse(payload["trace"]["fallback_used"])
        self.assertTrue(runner.is_canonically_compliant(payload))

    def test_e03_manual_correct_output_without_runner_fails_compliance(self) -> None:
        manual_output = {
            "result": {"table": "catalog.schema.synthetic_table", "ok": True},
            "task_correctness": "PASS",
        }
        self.assertFalse(runner.is_canonically_compliant(manual_output))

    def test_e04_missing_required_primitive_aborts_before_core(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            assistant_root = _copy_minimal_release(Path(td), include_primitive=False)
            calls = 0

            def should_not_run(*args, **kwargs):
                nonlocal calls
                calls += 1
                return {"unexpected": True}

            with mock.patch.object(runner, "_default_quick_profile", side_effect=should_not_run):
                payload = runner.run(
                    "catalog.schema.synthetic_table",
                    dict(DEFAULT_CONTEXT),
                    assistant_root=assistant_root,
                )

        trace = payload["trace"]
        self.assertEqual("BLOCKED", trace["status"])
        self.assertEqual("NOT_RUN", trace["preflight_status"])
        self.assertEqual(0, calls)
        self.assertTrue(
            any(issue["code"] == "RELEASE_INTEGRITY_MISMATCH" for issue in trace["blocking_issues"])
        )
        self.assertFalse(runner.is_canonically_compliant(payload))

    def test_e05_tampered_primitive_fails_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            assistant_root = _copy_minimal_release(Path(td), include_primitive=True)
            primitive = assistant_root / "hub_scripts" / "quick_profile" / "quick_profile.py"
            primitive.write_text(primitive.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")

            with mock.patch.object(
                runner,
                "_default_quick_profile",
                side_effect=AssertionError("primitive não deveria rodar"),
            ):
                payload = runner.run(
                    "catalog.schema.synthetic_table",
                    dict(DEFAULT_CONTEXT),
                    assistant_root=assistant_root,
                )

        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertTrue(
            any(issue["code"] == "RELEASE_INTEGRITY_MISMATCH" for issue in payload["trace"]["blocking_issues"])
        )

    def test_preflight_blocked_stops_core(self) -> None:
        calls = 0

        def should_not_run(*args, **kwargs):
            nonlocal calls
            calls += 1
            return {"unexpected": True}

        context = dict(DEFAULT_CONTEXT)
        context.pop("visual_diagnostics_requested")
        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(4, "synthetic_schema"),
        ), mock.patch.object(runner, "_default_quick_profile", side_effect=should_not_run):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                context,
                assistant_root=SOURCE_ASSISTANT,
            )

        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertEqual("BLOCKED", payload["trace"]["preflight_status"])
        self.assertEqual(0, calls)
        self.assertFalse(payload["trace"]["fallback_used"])

    def test_e06_primitive_failure_fails_without_fallback(self) -> None:
        def failing_profile(*args, **kwargs):
            raise RuntimeError("synthetic primitive failure")

        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(4, "synthetic_schema"),
        ), mock.patch.object(runner, "_default_quick_profile", side_effect=failing_profile):
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

    def test_e08_output_overwritten_after_runner_fails_compliance(self) -> None:
        payload = self.run_runner(result={"metric": 1})
        self.assertTrue(runner.is_canonically_compliant(payload))
        payload["result"] = {"metric": 999}
        self.assertFalse(runner.is_canonically_compliant(payload))

    def test_e09_stale_trace_rejected_against_current_run_id(self) -> None:
        first = self.run_runner(result={"metric": 1})
        second = self.run_runner(result={"metric": 1})
        current_run_id = second["trace"]["run_id"]
        self.assertNotEqual(first["trace"]["run_id"], current_run_id)
        self.assertFalse(
            runner.is_canonically_compliant(first, expected_run_id=current_run_id)
        )
        self.assertTrue(
            runner.is_canonically_compliant(second, expected_run_id=current_run_id)
        )

    def test_e10_runtime_derived_conflict_blocks_before_preflight_and_core(self) -> None:
        context = dict(DEFAULT_CONTEXT, numeric_columns=0)
        calls = 0

        def should_not_run(*args, **kwargs):
            nonlocal calls
            calls += 1
            return {"unexpected": True}

        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(4, "synthetic_schema"),
        ), mock.patch.object(runner, "_default_quick_profile", side_effect=should_not_run):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                context,
                assistant_root=SOURCE_ASSISTANT,
            )

        trace = payload["trace"]
        self.assertEqual("BLOCKED", trace["status"])
        self.assertEqual("NOT_RUN", trace["preflight_status"])
        self.assertEqual(0, calls)
        self.assertTrue(
            any(issue["code"] == "CONTEXT_PROVENANCE_CONFLICT" for issue in trace["blocking_issues"])
        )
        provenance = trace["context_provenance"]["numeric_columns"]
        self.assertEqual("runtime_derived", provenance["source"])
        self.assertEqual(4, provenance["value"])
        self.assertEqual(0, provenance["declared_value"])
        self.assertTrue(provenance["conflict"])

    def test_numeric_columns_can_be_omitted_when_runtime_derives_it(self) -> None:
        context = dict(DEFAULT_CONTEXT)
        context.pop("numeric_columns")
        payload = self.run_runner(context=context, numeric_columns=4)
        self.assertEqual("PASS", payload["trace"]["status"])
        provenance = payload["trace"]["context_provenance"]["numeric_columns"]
        self.assertEqual(4, provenance["value"])
        self.assertIsNone(provenance["declared_value"])
        self.assertTrue(runner.is_canonically_compliant(payload))

    def test_e11_legacy_helper_does_not_replace_missing_canonical_primitive(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            assistant_root = _copy_minimal_release(Path(td), include_primitive=False)
            legacy = assistant_root / "hub_scripts" / "quick_profile_legacy"
            legacy.mkdir(parents=True)
            (legacy / "__init__.py").write_text(
                "def quick_profile(*args, **kwargs):\n    return {'legacy': True}\n",
                encoding="utf-8",
            )
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=assistant_root,
            )

        trace = payload["trace"]
        self.assertEqual("BLOCKED", trace["status"])
        self.assertFalse(trace["fallback_used"])
        self.assertTrue(
            any(issue["code"] == "RELEASE_INTEGRITY_MISMATCH" for issue in trace["blocking_issues"])
        )

    def test_e12_trivial_manual_solution_still_fails_compliance(self) -> None:
        canonical = self.run_runner(result={"rows": 10, "columns": 4})
        manual = {"result": {"rows": 10, "columns": 4}}
        self.assertEqual(canonical["result"], manual["result"])
        self.assertTrue(runner.is_canonically_compliant(canonical))
        self.assertFalse(runner.is_canonically_compliant(manual))

    def test_public_run_signature_has_no_primitive_injection_hook(self) -> None:
        signature = inspect.signature(runner.run)
        self.assertNotIn("primitive_invoker", signature.parameters)

    def test_invalid_table_name_blocks_before_core(self) -> None:
        with mock.patch.object(
            runner,
            "_default_quick_profile",
            side_effect=AssertionError("primitive não deveria rodar"),
        ):
            payload = runner.run(
                "",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )
        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertTrue(any(issue["code"] == "RUN_INPUT_INVALID" for issue in payload["trace"]["blocking_issues"]))

    def test_runtime_context_unavailable_blocks_fail_closed(self) -> None:
        with mock.patch.object(
            runner,
            "_derive_numeric_columns",
            side_effect=RuntimeError("schema unavailable"),
        ):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )
        self.assertEqual("BLOCKED", payload["trace"]["status"])
        self.assertTrue(
            any(issue["code"] == "RUNTIME_CONTEXT_UNAVAILABLE" for issue in payload["trace"]["blocking_issues"])
        )

    def test_trace_does_not_copy_business_result(self) -> None:
        payload = self.run_runner(result={"secret_value": "do-not-copy"})
        self.assertNotIn("secret_value", json.dumps(payload["trace"], ensure_ascii=False))
        self.assertEqual("do-not-copy", payload["result"]["secret_value"])

    def test_structural_trace_is_deterministic_except_run_id(self) -> None:
        first = self.run_runner(result={"table": "catalog.schema.synthetic_table"})["trace"]
        second = self.run_runner(result={"table": "catalog.schema.synthetic_table"})["trace"]

        self.assertNotEqual(first["run_id"], second["run_id"])
        first = dict(first)
        second = dict(second)
        first.pop("run_id")
        second.pop("run_id")
        self.assertEqual(first, second)

    def test_render_diff_gate_detects_untracked_derived_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "tools").mkdir()
            for name in ("render_simulado.py", "project_policy.py", "simulado.py", "notebook_marker.py"):
                shutil.copyfile(REPO_ROOT / "tools" / name, root / "tools" / name)
            source = root / "ambiente_databricks"
            (source / ".assistant").mkdir(parents=True)
            (source / ".assistant/example.txt").write_text("synthetic\n")
            (source / ".assistant_instructions.md").write_text("instructions\n")
            subprocess.run([sys.executable, "-B", "tools/render_simulado.py", "--write"],
                           cwd=root, check=True, capture_output=True)
            derived = root / certifier.DERIVED_ROOT
            (derived / "new-derived.txt").write_text("generated\n", encoding="utf-8")

            with mock.patch.object(certifier, "REPO_ROOT", root):
                code, output, _ = certifier._run_render_diff_gate()

        self.assertEqual(1, code)
        self.assertIn("DERIVED_STALE", output)
        self.assertIn("new-derived.txt", output)

    def test_se05_temporal_boundary_is_explicit(self) -> None:
        execution_dir = SOURCE_ASSISTANT / "hub_scripts" / "skill_execution"
        self.assertTrue((execution_dir / "receipt" / "__init__.py").is_file())
        self.assertTrue((execution_dir / "postflight" / "__init__.py").is_file())
        self.assertTrue((SOURCE_SKILL / "scripts" / "run_enforced.py").is_file())
        self.assertTrue((SOURCE_SKILL / "scripts" / "postflight.py").is_file())
        self.assertFalse((execution_dir / "postflight.py").exists())


if __name__ == "__main__":
    unittest.main()
