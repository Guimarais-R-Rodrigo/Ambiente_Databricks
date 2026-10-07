from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_databricks" / ".assistant"
SKILL = "hub-ml-eda-profissional"
SKILL_DIR = SOURCE_ASSISTANT / "skills" / SKILL
RUNNER_PATH = SKILL_DIR / "scripts" / "run.py"
ENFORCED_PATH = SKILL_DIR / "scripts" / "run_enforced.py"
FINALIZER_PATH = SKILL_DIR / "scripts" / "postflight.py"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_module("sef_se05_core_runner_test", RUNNER_PATH)
enforced = _load_module("sef_se05_enforced_runner_test", ENFORCED_PATH)
finalizer = _load_module("sef_se05_finalizer_test", FINALIZER_PATH)


DEFAULT_CONTEXT = {
    "local_sample_required": False,
    "tabular_preview_required": False,
    "numeric_distributions_requested": False,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": False,
    "pk_columns": ["id"],
}

HANDOFF = {
    "sources_snapshot": "catalog.schema.synthetic_table @ synthetic",
    "unit_keys_target": "1 linha por id; chave=id; target=N/A",
    "quality_risks": ["fixture sintético"],
    "feature_candidates_leakage": ["não aplicável no fixture"],
    "filters_sample": "sem filtro; sem amostra local",
    "open_questions": [],
}


class DummyFrame:
    pass


class SkillEnforcementSE05RunnerTests(unittest.TestCase):
    def _fake_import(self, item, *, trace, gaps):
        item_id = str(item.get("id"))
        if item_id not in trace["resources_imported"]:
            trace["resources_imported"].append(item_id)

        if item_id == "data_quality_check":
            return lambda table_name, pk_columns, date_column=None: {"status": "pass", "score": 100}
        if item_id == "null_summary":
            return lambda df: DummyFrame()
        if item_id == "correlation_matrix":
            return lambda df: (object(), [])
        if item_id == "smart_sample":
            return lambda df, n=1000, seed=42: df
        if item_id == "safe_display":
            return lambda df, display_fn=None: display_fn(df) if display_fn else None
        if item_id == "distribution_grid":
            return lambda df: object()
        if item_id == "theme_plotly":
            return lambda fig, theme: fig
        if item_id == "quick_profile":
            return lambda *args, **kwargs: {"profile": "unused"}
        raise AssertionError(f"recurso inesperado no teste: {item_id}")

    def _run_enforced(self, *, context=None, import_side_effect=None):
        effective = dict(DEFAULT_CONTEXT if context is None else context)
        fake_import = self._fake_import if import_side_effect is None else import_side_effect
        with mock.patch.object(enforced, "_load_runner", return_value=runner), mock.patch.object(
            runner,
            "_derive_numeric_columns",
            return_value=(3, "synthetic_schema"),
        ), mock.patch.object(
            runner,
            "_default_quick_profile",
            return_value={"profile": "ok"},
        ), mock.patch.object(
            enforced,
            "_spark_table",
            return_value=DummyFrame(),
        ), mock.patch.object(
            enforced,
            "_import_symbol",
            side_effect=fake_import,
        ):
            return enforced.run_enforced(
                "catalog.schema.synthetic_table",
                effective,
                assistant_root=SOURCE_ASSISTANT,
                strict=False,
            )

    def test_l4_happy_path_authorizes_completion(self):
        payload = self._run_enforced()
        self.assertEqual("PASS", payload["trace"]["status"])
        self.assertEqual("PASS", payload["trace"]["enforcement_status"])
        self.assertEqual([], payload["trace"]["evidence_gaps"])
        self.assertEqual(enforced.ENFORCED_ENTRYPOINT, payload["trace"]["enforcement_entrypoint"])
        self.assertIsInstance(payload["receipt"], dict)
        self.assertIn("data_quality_check", payload["trace"]["resources_completed"])
        self.assertIn("null_summary", payload["trace"]["resources_completed"])
        self.assertIn("correlation_matrix", payload["trace"]["resources_completed"])
        self.assertEqual(
            {"roteiro_eda", "relatorio_executivo_eda"},
            set(payload["trace"]["templates_loaded"]),
        )

        finalized = finalizer.finalize(payload, HANDOFF, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("PASS", finalized["postflight"]["status"])
        self.assertTrue(finalized["postflight"]["completion_authorized"])
        self.assertEqual("COMPLETED", finalized["completion"]["status"])
        self.assertTrue(finalized["completion"]["authorized"])

        verification = finalizer.verify_finalized(finalized, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("VALID", verification["status"])
        self.assertTrue(verification["valid"])
        self.assertTrue(verification["completion_authorized"])
        self.assertTrue(verification["completion_claim_consistent"])

    def test_core_se04_payload_alone_cannot_finalize_l4(self):
        with mock.patch.object(runner, "_derive_numeric_columns", return_value=(3, "synthetic_schema")), mock.patch.object(
            runner,
            "_default_quick_profile",
            return_value={"profile": "ok"},
        ):
            payload = runner.run(
                "catalog.schema.synthetic_table",
                dict(DEFAULT_CONTEXT),
                assistant_root=SOURCE_ASSISTANT,
            )
        self.assertIsInstance(payload["receipt"], dict)
        finalized = finalizer.finalize(payload, HANDOFF, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("BLOCKED", finalized["postflight"]["status"])
        self.assertFalse(finalized["completion"]["authorized"])
        self.assertEqual("ENFORCED_ENTRYPOINT_MISSING", finalized["postflight"]["issues"][0]["code"])

    def test_missing_pk_columns_is_calibrated_to_not_applicable_in_se06(self):
        context = dict(DEFAULT_CONTEXT)
        context.pop("pk_columns")
        payload = self._run_enforced(context=context)
        self.assertIsInstance(payload["receipt"], dict)
        self.assertEqual("PASS", payload["trace"]["enforcement_status"])
        self.assertNotIn("data_quality_check", payload["trace"]["resources_called"])
        decision = next(
            item for item in payload["trace"]["decisions"]
            if item["item_type"] == "resource"
            and item["item_id"] == "data_quality_check"
        )
        self.assertFalse(decision["applicable"])
        self.assertEqual([], payload["trace"]["evidence_gaps"])
        handoff = dict(HANDOFF)
        handoff["unit_keys_target"] = "1 linha por evento; PK não confirmada; target=N/A"
        finalized = finalizer.finalize(payload, handoff, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("PASS", finalized["postflight"]["status"])
        self.assertTrue(finalized["completion"]["authorized"])

    def test_applicable_safe_display_without_renderer_fails_closed(self):
        context = dict(DEFAULT_CONTEXT, tabular_preview_required=True)
        payload = self._run_enforced(context=context)
        self.assertEqual("INCOMPLETE", payload["trace"]["enforcement_status"])
        self.assertTrue(
            any(
                item["code"] == "RESOURCE_RUNTIME_UNAVAILABLE"
                and item["item_id"] == "safe_display"
                for item in payload["trace"]["evidence_gaps"]
            )
        )
        finalized = finalizer.finalize(payload, HANDOFF, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("FAIL", finalized["postflight"]["status"])
        self.assertFalse(finalized["completion"]["authorized"])

    def test_helper_failure_is_called_not_completed_and_blocks_completion(self):
        def failing_import(item, *, trace, gaps):
            item_id = str(item.get("id"))
            if item_id not in trace["resources_imported"]:
                trace["resources_imported"].append(item_id)
            if item_id == "null_summary":
                def fail(_df):
                    raise RuntimeError("synthetic null_summary failure")
                return fail
            return self._fake_import(item, trace=trace, gaps=gaps)

        payload = self._run_enforced(import_side_effect=failing_import)
        self.assertIn("null_summary", payload["trace"]["resources_called"])
        self.assertNotIn("null_summary", payload["trace"]["resources_completed"])
        self.assertEqual("INCOMPLETE", payload["trace"]["enforcement_status"])
        finalized = finalizer.finalize(payload, HANDOFF, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("FAIL", finalized["postflight"]["status"])
        self.assertFalse(finalized["completion"]["authorized"])

    def test_successful_l4_is_pending_until_postflight(self):
        payload = self._run_enforced()
        self.assertEqual("PENDING_POSTFLIGHT", payload["completion"]["status"])
        self.assertFalse(payload["completion"]["authorized"])
        finalized = finalizer.finalize_or_raise(
            payload,
            HANDOFF,
            assistant_root=SOURCE_ASSISTANT,
        )
        self.assertEqual("COMPLETED", finalized["completion"]["status"])
        self.assertTrue(finalized["completion"]["authorized"])

    def test_finalize_or_raise_rejects_incomplete_handoff(self):
        payload = self._run_enforced()
        handoff = dict(HANDOFF)
        handoff.pop("quality_risks")
        with self.assertRaises(finalizer.CompletionNotAuthorized):
            finalizer.finalize_or_raise(
                payload,
                handoff,
                assistant_root=SOURCE_ASSISTANT,
            )

    def test_completion_claim_tamper_is_detected(self):
        payload = self._run_enforced()
        finalized = finalizer.finalize(payload, HANDOFF, assistant_root=SOURCE_ASSISTANT)
        self.assertTrue(finalized["completion"]["authorized"])
        finalized["completion"] = {
            "authorized": False,
            "status": "NOT_COMPLETED",
            "reason": "tampered",
        }
        verification = finalizer.verify_finalized(finalized, assistant_root=SOURCE_ASSISTANT)
        self.assertEqual("INVALID", verification["status"])
        self.assertFalse(verification["valid"])
        self.assertFalse(verification["completion_authorized"])
        self.assertIn("COMPLETION_CLAIM_MISMATCH", verification["issues"])

    def test_release_manifest_protects_all_se05_components(self):
        manifest = json.loads((SKILL_DIR / "release_manifest.json").read_text(encoding="utf-8"))
        roles = {item["role"]: item for item in manifest["artifacts"]}
        for role in (
            "contract",
            "skill_guidance",
            "runner",
            "enforced_runner",
            "postflight_finalizer",
            "preflight_engine",
            "receipt_engine",
            "postflight_engine",
            "protected_primitive",
        ):
            self.assertIn(role, roles)
        for artifact in manifest["artifacts"]:
            target = SOURCE_ASSISTANT / artifact["path"]
            self.assertTrue(target.is_file(), artifact["path"])
            self.assertEqual(artifact["git_blob_sha1"], runner._git_blob_sha1(target))


if __name__ == "__main__":
    unittest.main(verbosity=2)
