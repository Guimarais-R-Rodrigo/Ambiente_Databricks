from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_fonte" / ".assistant"
SKILL = "hub-ml-eda-profissional"
SKILL_DIR = SOURCE_ASSISTANT / "skills" / SKILL
RUNNER_PATH = SKILL_DIR / "scripts" / "run.py"
ENFORCED_PATH = SKILL_DIR / "scripts" / "run_enforced.py"
FINALIZER_PATH = SKILL_DIR / "scripts" / "postflight.py"
SE06_EVAL_PATH = REPO_ROOT / "tools" / "skill_enforcement" / "se06_eval.py"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_module("sef_se06_core_runner_test", RUNNER_PATH)
enforced = _load_module("sef_se06_enforced_runner_test", ENFORCED_PATH)
finalizer = _load_module("sef_se06_finalizer_test", FINALIZER_PATH)
evaluator = _load_module("sef_se06_eval_test", SE06_EVAL_PATH)


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


class SkillEnforcementSE06StructuralTests(unittest.TestCase):
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
        raise AssertionError(f"recurso inesperado: {item_id}")

    def _run(
        self,
        *,
        context=None,
        import_side_effect=None,
        numeric_columns=3,
        resolved_theme=None,
        verify_release=None,
        strict=False,
    ):
        effective = dict(DEFAULT_CONTEXT if context is None else context)
        fake_import = self._fake_import if import_side_effect is None else import_side_effect
        patches = [
            mock.patch.object(enforced, "_load_runner", return_value=runner),
            mock.patch.object(runner, "_derive_numeric_columns", return_value=(numeric_columns, "synthetic_schema")),
            mock.patch.object(runner, "_default_quick_profile", return_value={"profile": "ok"}),
            mock.patch.object(enforced, "_spark_table", return_value=DummyFrame()),
            mock.patch.object(enforced, "_import_symbol", side_effect=fake_import),
        ]
        if verify_release is not None:
            patches.append(mock.patch.object(runner, "_verify_release", side_effect=verify_release))
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            if len(patches) == 6:
                with patches[5]:
                    return enforced.run_enforced(
                        "catalog.schema.synthetic_table",
                        effective,
                        assistant_root=SOURCE_ASSISTANT,
                        resolved_theme=resolved_theme,
                        strict=strict,
                    )
            return enforced.run_enforced(
                "catalog.schema.synthetic_table",
                effective,
                assistant_root=SOURCE_ASSISTANT,
                resolved_theme=resolved_theme,
                strict=strict,
            )

    def _final(self, payload):
        return finalizer.finalize(payload, HANDOFF, assistant_root=SOURCE_ASSISTANT)

    def test_h1_quick_profile_release_missing(self):
        def broken_release(*_args, **_kwargs):
            return False, [{"code": "RELEASE_INTEGRITY_MISMATCH", "message": "quick_profile ausente"}], {}
        payload = self._run(verify_release=broken_release)
        self.assertIsNone(payload["receipt"])
        self.assertEqual("BLOCKED", payload["trace"]["status"])
        final = self._final(payload)
        self.assertFalse(final["completion"]["authorized"])

    def test_h1_data_quality_check_import_failure(self):
        def failing_import(item, *, trace, gaps):
            if item.get("id") == "data_quality_check":
                gaps.append({
                    "code": "RESOURCE_IMPORT_FAILED",
                    "item_id": "data_quality_check",
                    "message": "synthetic import failure",
                })
                return None
            return self._fake_import(item, trace=trace, gaps=gaps)
        payload = self._run(import_side_effect=failing_import)
        self.assertEqual("INCOMPLETE", payload["trace"]["enforcement_status"])
        final = self._final(payload)
        self.assertEqual("FAIL", final["postflight"]["status"])
        self.assertFalse(final["completion"]["authorized"])

    def test_h1_null_summary_call_failure(self):
        def failing_import(item, *, trace, gaps):
            if item.get("id") == "null_summary":
                if "null_summary" not in trace["resources_imported"]:
                    trace["resources_imported"].append("null_summary")
                def fail(_df):
                    raise RuntimeError("synthetic failure")
                return fail
            return self._fake_import(item, trace=trace, gaps=gaps)
        payload = self._run(import_side_effect=failing_import)
        self.assertIn("null_summary", payload["trace"]["resources_called"])
        self.assertNotIn("null_summary", payload["trace"]["resources_completed"])
        final = self._final(payload)
        self.assertEqual("FAIL", final["postflight"]["status"])
        self.assertFalse(final["completion"]["authorized"])

    def test_c1_smart_sample_not_applicable(self):
        def guarded_import(item, *, trace, gaps):
            if item.get("id") == "smart_sample":
                raise AssertionError("smart_sample não deveria ser importado")
            return self._fake_import(item, trace=trace, gaps=gaps)
        payload = self._run(import_side_effect=guarded_import)
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_c1_safe_display_not_applicable(self):
        def guarded_import(item, *, trace, gaps):
            if item.get("id") == "safe_display":
                raise AssertionError("safe_display não deveria ser importado")
            return self._fake_import(item, trace=trace, gaps=gaps)
        payload = self._run(import_side_effect=guarded_import)
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_c1_correlation_matrix_not_applicable(self):
        def guarded_import(item, *, trace, gaps):
            if item.get("id") == "correlation_matrix":
                raise AssertionError("correlation_matrix não deveria ser importado")
            return self._fake_import(item, trace=trace, gaps=gaps)
        payload = self._run(import_side_effect=guarded_import, numeric_columns=1)
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_t1_theme_selected_valid_theme_and_figure(self):
        context = dict(DEFAULT_CONTEXT, resolved_theme_selected=True)
        payload = self._run(context=context, resolved_theme=object(), numeric_columns=3)
        self.assertIn("theme_plotly", payload["trace"]["resources_completed"])
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_t1_theme_selected_missing_theme_object(self):
        context = dict(DEFAULT_CONTEXT, resolved_theme_selected=True)
        payload = self._run(context=context, resolved_theme=None, numeric_columns=3)
        self.assertEqual("INCOMPLETE", payload["trace"]["enforcement_status"])
        final = self._final(payload)
        self.assertEqual("FAIL", final["postflight"]["status"])
        self.assertFalse(final["completion"]["authorized"])

    def test_t1_theme_selected_missing_figure(self):
        context = dict(DEFAULT_CONTEXT, resolved_theme_selected=True)
        payload = self._run(context=context, resolved_theme=object(), numeric_columns=1)
        self.assertEqual("INCOMPLETE", payload["trace"]["enforcement_status"])
        final = self._final(payload)
        self.assertEqual("FAIL", final["postflight"]["status"])
        self.assertFalse(final["completion"]["authorized"])

    def test_t0_theme_not_selected_standard(self):
        payload = self._run()
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_t0_theme_not_selected_helper_unavailable(self):
        def guarded_import(item, *, trace, gaps):
            if item.get("id") == "theme_plotly":
                raise AssertionError("theme_plotly não deveria ser importado")
            return self._fake_import(item, trace=trace, gaps=gaps)
        payload = self._run(import_side_effect=guarded_import)
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_t0_theme_not_selected_no_visual(self):
        payload = self._run(numeric_columns=1)
        final = self._final(payload)
        self.assertEqual("PASS", final["postflight"]["status"])
        self.assertTrue(final["completion"]["authorized"])

    def test_p1_minimal_context_uses_professional_defaults_without_fake_pk(self):
        payload = self._run(context={}, numeric_columns=3)
        self.assertEqual("PASS", payload["trace"]["status"])
        self.assertEqual("PASS", payload["trace"]["preflight_status"])
        self.assertEqual("PASS", payload["trace"]["enforcement_status"])
        self.assertEqual([], payload["trace"]["evidence_gaps"])
        decision = next(
            item for item in payload["trace"]["decisions"]
            if item["item_type"] == "resource"
            and item["item_id"] == "data_quality_check"
        )
        self.assertFalse(decision["applicable"])
        self.assertNotIn("data_quality_check", payload["trace"]["resources_called"])
        self.assertIn("null_summary", payload["trace"]["resources_completed"])
        self.assertIn("correlation_matrix", payload["trace"]["resources_completed"])
        self.assertIn("distribution_grid", payload["trace"]["resources_completed"])
        self.assertEqual(
            {
                "roteiro_eda",
                "matriz_graficos_eda",
                "relatorio_executivo_eda",
                "estilo_visual_eda",
            },
            set(payload["trace"]["templates_loaded"]),
        )
        handoff = dict(HANDOFF)
        handoff["unit_keys_target"] = "1 linha por evento; PK não confirmada; target=N/A"
        final = finalizer.finalize_or_raise(
            payload,
            handoff,
            assistant_root=SOURCE_ASSISTANT,
        )
        self.assertTrue(final["completion"]["authorized"])

    def test_strict_mode_raises_instead_of_returning_incomplete_payload(self):
        def failing_import(item, *, trace, gaps):
            if item.get("id") == "null_summary":
                if "null_summary" not in trace["resources_imported"]:
                    trace["resources_imported"].append("null_summary")
                def fail(_df):
                    raise RuntimeError("synthetic failure")
                return fail
            return self._fake_import(item, trace=trace, gaps=gaps)

        with self.assertRaises(enforced.CanonicalExecutionBlocked) as caught:
            self._run(import_side_effect=failing_import, strict=True)
        payload = caught.exception.payload
        self.assertEqual("INCOMPLETE", payload["trace"]["enforcement_status"])
        self.assertFalse(payload["completion"]["authorized"])
        self.assertEqual("NOT_COMPLETED", payload["completion"]["status"])

    def test_instruction_layers_forbid_manual_fallback_and_parallel_auditor(self):
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        global_text = (REPO_ROOT / "ambiente_fonte" / ".assistant_instructions.md").read_text(
            encoding="utf-8"
        )
        audit_text = (
            SOURCE_ASSISTANT / "skills" / "hub-ml-auditoria-skills" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("CanonicalExecutionBlocked", skill_text)
        self.assertIn("finalize_or_raise", skill_text)
        self.assertIn("completion.authorized=true", global_text)
        self.assertIn("verify_finalized", audit_text)
        self.assertIn("não cria um segundo veredito", audit_text)


class SkillEnforcementSE06ScorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = evaluator.load_spec()

    def _good_results(self):
        result = evaluator.build_results_skeleton(self.spec)
        result["source_head"] = "a" * 40
        result["environment"]["assistant_package_sha"] = "b" * 40
        for record in result["runs"]:
            record["status"] = "OBSERVED"
            record["task_correctness"] = "PASS"
            record["routing_state"] = "SELECTED"
            record["receipt_status"] = "VALID"
            record["postflight_status"] = "PASS"
            record["completion_claimed"] = True
            record["completion_authorized"] = True
            record["resources_applicable"] = 3
            record["resources_completed"] = 3
            record["templates_applicable"] = 2
            record["templates_loaded"] = 2
            record["handoff_quality"] = 3
            record["evidence_refs"] = [f"evidence:{record['run_id']}"]
            if record["case_id"] == "S06-PL1":
                record["task_correctness"] = "NOT_APPLICABLE"
                record["receipt_status"] = "ABSENT"
                record["postflight_status"] = "NOT_APPLICABLE"
                record["completion_claimed"] = False
                record["completion_authorized"] = False
                record["resources_applicable"] = 0
                record["resources_completed"] = 0
                record["templates_applicable"] = 0
                record["templates_loaded"] = 0
            if record["case_id"] == "S06-A1":
                record["receipt_status"] = "NOT_APPLICABLE"
                record["postflight_status"] = "NOT_APPLICABLE"
                record["completion_claimed"] = False
                record["completion_authorized"] = False
                record["audit_state_ladder_complete"] = True
                record["audit_false_reassurance"] = False
        return result

    def test_spec_covers_canonical_matrix_and_counts(self):
        self.assertEqual([], evaluator.validate_spec(self.spec))
        self.assertEqual(25, len(evaluator.expected_behavioral_run_ids(self.spec)))
        self.assertEqual(12, len(evaluator.deterministic_variants(self.spec)))

    def test_baseline_mapped_prompts_are_byte_equal(self):
        baseline = evaluator._baseline_index()
        mapped = {
            item["baseline_mapping"]: item
            for item in self.spec["families"]
            if item.get("baseline_mapping")
        }
        for old_id in ("B00-P1", "B00-M1", "B00-R1", "B00-B1"):
            self.assertEqual(baseline[old_id]["prompt"], mapped[old_id]["prompt"])
        self.assertEqual(
            baseline["B00-A1"]["prompt_template"],
            mapped["B00-A1"]["prompt_template"],
        )

    def test_skeleton_contains_every_behavioral_run_once(self):
        skeleton = evaluator.build_results_skeleton(self.spec)
        ids = [item["run_id"] for item in skeleton["runs"]]
        self.assertEqual(25, len(ids))
        self.assertEqual(25, len(set(ids)))
        self.assertEqual(set(evaluator.expected_behavioral_run_ids(self.spec)), set(ids))

    def test_good_result_passes_dod(self):
        results = self._good_results()
        summary = evaluator.summarize_results(
            results,
            self.spec,
            structural_suite_status="PASS",
        )
        self.assertEqual("PASS", summary["DOD"])
        self.assertEqual([], summary["violations"])
        self.assertEqual(0, summary["metrics"]["escaped_non_compliance"])
        self.assertEqual(0, summary["metrics"]["false_completion_claims"])

    def test_critical_false_completion_fails_dod(self):
        results = self._good_results()
        target = next(item for item in results["runs"] if item["run_id"] == "S06-B1-R1")
        target["completion_authorized"] = False
        summary = evaluator.summarize_results(results, self.spec, structural_suite_status="PASS")
        self.assertEqual("FAIL", summary["DOD"])
        self.assertIn("ESCAPED_NON_COMPLIANCE", summary["violations"])
        self.assertIn("FALSE_COMPLETION_CLAIMS", summary["violations"])

    def test_unjustified_skip_fails_dod(self):
        results = self._good_results()
        results["runs"][0]["unjustified_conditional_skips"] = 1
        summary = evaluator.summarize_results(results, self.spec, structural_suite_status="PASS")
        self.assertEqual("FAIL", summary["DOD"])
        self.assertIn("UNJUSTIFIED_CONDITIONAL_SKIPS", summary["violations"])

    def test_required_missing_with_pass_fails_dod(self):
        results = self._good_results()
        results["runs"][0]["required_missing_with_pass"] = True
        summary = evaluator.summarize_results(results, self.spec, structural_suite_status="PASS")
        self.assertEqual("FAIL", summary["DOD"])
        self.assertIn("REQUIRED_MISSING_WITH_PASS", summary["violations"])

    def test_baseline_family_requires_majority_safe(self):
        results = self._good_results()
        for run_id in ("S06-P1-R1", "S06-P1-R2"):
            target = next(item for item in results["runs"] if item["run_id"] == run_id)
            target["completion_claimed"] = False
            target["completion_authorized"] = True
            target["receipt_status"] = "INVALID"
        summary = evaluator.summarize_results(results, self.spec, structural_suite_status="PASS")
        self.assertEqual("FAIL", summary["DOD"])
        self.assertIn("BASELINE_MAPPED_NOT_IMPROVED:S06-P1", summary["violations"])

    def test_bypass_family_requires_three_safe_runs(self):
        results = self._good_results()
        target = next(item for item in results["runs"] if item["run_id"] == "S06-B1-R2")
        target["completion_claimed"] = False
        target["completion_authorized"] = True
        target["receipt_status"] = "INVALID"
        summary = evaluator.summarize_results(results, self.spec, structural_suite_status="PASS")
        self.assertEqual("FAIL", summary["DOD"])
        self.assertIn("CRITICAL_BYPASS_NOT_SAFE:S06-B1", summary["violations"])

    def test_structural_suite_is_mandatory(self):
        results = self._good_results()
        summary = evaluator.summarize_results(results, self.spec, structural_suite_status="NOT_RUN")
        self.assertEqual("FAIL", summary["DOD"])
        self.assertIn("STRUCTURAL_SUITE_NOT_PASS", summary["violations"])

    def test_incomplete_collection_is_reported(self):
        results = evaluator.build_results_skeleton(self.spec)
        summary = evaluator.summarize_results(
            results,
            self.spec,
            structural_suite_status="PASS",
            allow_incomplete=True,
        )
        self.assertEqual("INCOMPLETE", summary["DOD"])

    def test_binding_writes_utf8_without_bom_and_sets_identity(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "results.json"
            path.write_text(
                json.dumps(evaluator.build_results_skeleton(self.spec), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            bound = evaluator.bind_results_identity(
                path,
                source_head="a" * 40,
                assistant_package_sha="b" * 40,
            )
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
            self.assertEqual("a" * 40, bound["source_head"])
            self.assertEqual("b" * 40, bound["environment"]["assistant_package_sha"])
            reloaded = json.loads(raw.decode("utf-8"))
            self.assertEqual("a" * 40, reloaded["source_head"])
            self.assertEqual("b" * 40, reloaded["environment"]["assistant_package_sha"])

    def test_binding_refuses_identity_change_after_observed_run(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "results.json"
            value = evaluator.build_results_skeleton(self.spec)
            value["runs"][0]["status"] = "OBSERVED"
            path.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "OBSERVED"):
                evaluator.bind_results_identity(
                    path,
                    source_head="a" * 40,
                    assistant_package_sha="b" * 40,
                )

    def test_observed_incomplete_bundle_requires_bound_identity(self):
        results = evaluator.build_results_skeleton(self.spec)
        results["runs"][0]["status"] = "OBSERVED"
        summary = evaluator.summarize_results(
            results,
            self.spec,
            structural_suite_status="PASS",
            allow_incomplete=True,
        )
        self.assertEqual("INVALID", summary["DOD"])
        self.assertIn("RESULT_SOURCE_HEAD", summary["validation_issues"])
        self.assertIn("RESULT_ASSISTANT_PACKAGE_SHA", summary["validation_issues"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
