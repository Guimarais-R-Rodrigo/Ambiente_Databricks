"""SER03/SER05 candidate domain tests, with full-checkout integration separated.

Pure checks can run in a source overlay. SEFIntegrationTests requires the actual
complete checkout, canonical dependencies and matching release manifest.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
FIXTURES = ROOT / "tools/tests/fixtures/ser_b1"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


safra = load("b1_safra_preflight", ASSISTANT / "skills/hub-ml-analise-safra/scripts/preflight.py")
cross = load("b1_cross_preflight", ASSISTANT / "skills/hub-ml-cross-eda-ml/scripts/preflight.py")
runner = load("b1_safra_run", ASSISTANT / "skills/hub-ml-analise-safra/scripts/run.py")
verifier = load("b1_safra_verify", ASSISTANT / "skills/hub-ml-analise-safra/scripts/verify.py")
from hub_scripts.skill_execution.domain_context import ContextError, digest, validate_temporal_context, loads_strict
from hub_scripts.skill_execution.domain_context.release import blob, release_integrity


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class SafraDomainTests(unittest.TestCase):
    def setUp(self):
        self.req = fixture("vf_cumulative.json")["request"]

    def assert_blocked(self, req, reason=None):
        result = safra.validate_request(req)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertFalse(result["helper_called"])
        self.assertFalse(result["writes_performed"])
        if reason:
            self.assertIn(reason, " ".join(result["issues"]))

    def test_vf01_cumulative_and_event_fixtures(self):
        for name in ("vf_cumulative.json", "vf_events.json"):
            with self.subTest(name=name):
                request = fixture(name)["request"]
                result = safra.validate_request(request)
                self.assertEqual("PASS", result["status"], result)
                self.assertEqual(digest(request), result["request_sha256"])
                self.assertFalse(result["helper_called"])

    def test_vf02_reject_mob_negative_fractional_boolean_null_and_string(self):
        for mob in (-1, 0.5, True, None, "0", float("nan"), float("inf")):
            with self.subTest(mob=repr(mob)):
                data = copy.deepcopy(self.req); data["rows"][0]["mob"] = mob
                self.assert_blocked(data, "INTEGER_OUT_OF_RANGE")

    def test_vf02_reject_mob_incompatible_with_dates(self):
        self.req["rows"][0]["mob"] = 1
        self.assert_blocked(self.req, "MOB_CALENDAR_MISMATCH")

    def test_vf03_reject_nonbinary_target(self):
        for value in (2, -1, 0.0, 0.5, True, None, "1"):
            with self.subTest(value=repr(value)):
                data = copy.deepcopy(self.req); data["rows"][0]["target"] = value
                self.assert_blocked(data, "BINARY_INTEGER_REQUIRED")

    def test_vf04_reject_cumulative_decrease(self):
        self.req["rows"][4]["target"] = 0
        self.assert_blocked(self.req, "CUMULATIVE_DECREASE")

    def test_vf05_duplicate_identical_and_conflicting_rejected(self):
        for target in (0, 1):
            data = copy.deepcopy(self.req)
            duplicated = dict(data["rows"][0]); duplicated["target"] = target
            data["rows"].append(duplicated)
            self.assert_blocked(data, "DUPLICATE_ID_MOB")

    def test_vf06_missing_observation_is_not_zero_or_complete(self):
        before = copy.deepcopy(self.req)
        result = safra.validate_request(self.req)
        cell = next(x for x in result["coverage_grid"] if x["safra"] == "2026-01" and x["mob"] == 2)
        self.assertEqual("INCOMPLETE", cell["coverage_status"])
        self.assertEqual(1, cell["n_contratos_observados"])
        self.assertEqual(2, cell["n_contratos_safra"])
        self.assertEqual(before, self.req)

    def test_vf07_roster_not_observed_subset_defines_denominator(self):
        self.req["cohort_roster"].append({"id": "a3", "originated_at": "2026-01-01T00:00:00Z"})
        self.assert_blocked(self.req, "MOB0_INCOMPLETE")

    def test_vf07_origin_cannot_change_inside_unit(self):
        self.req["rows"][2]["originated_at"] = "2025-12-01T00:00:00Z"
        self.assert_blocked(self.req, "ORIGIN_ROSTER_MISMATCH")

    def test_vf08_quarterly_rejected_not_claimed_by_monthly_profile(self):
        self.req["periodicity"] = "QUARTER"
        self.assert_blocked(self.req, "UNSUPPORTED:periodicity")

    def test_vf09_immature_differs_from_incomplete(self):
        result = safra.validate_request(self.req)
        future = next(x for x in result["coverage_grid"] if x["safra"] == "2026-02" and x["mob"] == 2)
        self.assertEqual("IMMATURE", future["maturity"])
        self.assertEqual("IMMATURE", future["coverage_status"])
        incomplete = next(x for x in result["coverage_grid"] if x["safra"] == "2026-01" and x["mob"] == 2)
        self.assertEqual("MATURE", incomplete["maturity"])
        self.assertEqual("INCOMPLETE", incomplete["coverage_status"])

    def test_vf09_no_observations_not_false_zero(self):
        self.req["rows"] = [r for r in self.req["rows"] if r["mob"] != 2]
        result = safra.validate_request(self.req)
        self.assertEqual("PASS", result["status"])
        missing = next(x for x in result["coverage_grid"] if x["safra"] == "2026-01" and x["mob"] == 2)
        self.assertEqual("NO_OBSERVATIONS", missing["coverage_status"])
        self.assertNotIn("taxa", missing)

    def test_vf10_request_digest_covers_population_cutoff_and_semantics(self):
        first = safra.validate_request(self.req)["request_sha256"]
        for key, value in (("population_id", "other"), ("cutoff", "2026-04-01T00:00:00Z"), ("semantic_mode", "EVENT")):
            data = copy.deepcopy(self.req); data[key] = value
            result = safra.validate_request(data)
            self.assertEqual("PASS", result["status"], result)
            self.assertNotEqual(first, result["request_sha256"])

    def test_vf11_event_sequence_can_decrease_but_not_disappear_and_reenter(self):
        data = fixture("vf_events.json")["request"]
        self.assertEqual("PASS", safra.validate_request(data)["status"])
        data["rows"] = [r for r in data["rows"] if not (r["id"] == "a1" and r["mob"] == 1)]
        self.assert_blocked(data, "EVENT_GAP_WITH_REENTRY")

    def test_vf12_monetary_estimand_rejected(self):
        self.req["estimand"] = "MONETARY_LOSS"
        self.assert_blocked(self.req, "UNSUPPORTED:estimand")

    def test_invalid_rows_and_unknown_keys_fail_closed(self):
        for data in (None, [], {}, {**self.req, "hidden_override": True}, {**self.req, "rows": []}):
            with self.subTest(data_type=type(data).__name__):
                self.assert_blocked(data)

    def test_dates_naive_nonmonth_future_or_non_utc_rejected(self):
        for value in ("2026-01-01", "2026-01-02T00:00:00Z", "2026-04-01T00:00:00Z", "2026-01-01T00:00:00-03:00"):
            data = copy.deepcopy(self.req); data["rows"][0]["observed_at"] = value
            self.assert_blocked(data)

    def test_invalid_request_never_calls_canonical_primitive(self):
        self.req["rows"][0]["target"] = 2
        # This isolates only the preflight->primitive ordering; release validation
        # is covered independently and is not claimed by this mocked control.
        artifacts = {f"skills/{runner.SKILL}/execution_contract.json": "a"*40,
                     f"skills/{runner.SKILL}/scripts/run.py": "b"*40}
        with mock.patch.object(runner, "release_integrity", return_value={"manifest_sha256": "c"*64, "artifacts": artifacts}), mock.patch.object(runner, "_canonical_primitive") as primitive:
            result = runner.run(self.req, run_id="invalid-request-check")
        self.assertEqual("BLOCKED", result["status"])
        self.assertIsNone(result["receipt"])
        primitive.assert_not_called()

    def test_no_receipt_on_missing_release_manifest(self):
        with mock.patch.object(runner, "release_integrity", side_effect=ValueError("RELEASE_FILESET_MISMATCH")):
            result = runner.run(self.req, run_id="missing-release")
        self.assertEqual("BLOCKED", result["status"])
        self.assertIsNone(result["receipt"])
        self.assertFalse(result["trace"]["resources_called"])


class CrossDomainTests(unittest.TestCase):
    def setUp(self):
        self.context = fixture("ce_l2_temporal.json")["context"]

    def assert_blocked(self, context, reason=None):
        result = cross.validate_context(context)
        self.assertEqual("BLOCKED", result["status"], result)
        self.assertFalse(result["join_executed"])
        self.assertFalse(result["coverage_measured"])
        self.assertFalse(result["promotion_authorized"])
        if reason:
            self.assertIn(reason, " ".join(result["issues"]))

    def test_ce01_required_context_fields_block_if_missing(self):
        for key in self.context:
            with self.subTest(key=key):
                value = copy.deepcopy(self.context); value.pop(key)
                self.assert_blocked(value)

    def test_ce01_source_identity_declared_never_read(self):
        result = cross.validate_context(self.context)
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual("DECLARED_NOT_READ", result["source_identity_status"])
        self.assertFalse(result["join_executed"])
        self.assertEqual("NOT_EVALUATED", result["ml_readiness"])

    def test_ce02_unknown_pit_never_becomes_false(self):
        for value in (None, "UNKNOWN", False, "false", "FALSE"):
            context = copy.deepcopy(self.context); context["pit"] = value
            self.assert_blocked(context)

    def test_ce02_not_applicable_requires_reason(self):
        context = fixture("ce_l2_static.json")["context"]
        self.assertEqual("PASS", cross.validate_context(context)["status"])
        context.pop("not_applicable_reason")
        self.assert_blocked(context)

    def test_ce05_temporal_boundary_is_explicit_and_bound_to_digest(self):
        first = cross.validate_context(self.context)
        context = copy.deepcopy(self.context); context["temporal"]["boundary"] = "LT"
        second = cross.validate_context(context)
        self.assertEqual("PASS", second["status"])
        self.assertNotEqual(first["context_sha256"], second["context_sha256"])
        context["temporal"]["boundary"] = "nearest"
        self.assert_blocked(context, "EXPLICIT_BOUNDARY_REQUIRED")

    def test_ce05_timezone_and_tie_policy_fail_closed(self):
        for key, value in (("timezone", "America/Sao_Paulo"), ("tie_break", "FIRST")):
            context = copy.deepcopy(self.context); context["temporal"][key] = value
            self.assert_blocked(context)

    def test_ce06_variable_lag_not_approximated(self):
        self.context["temporal"]["lag_kind"] = "VARIABLE"
        self.assert_blocked(self.context, "VARIABLE_LATENCY_UNSUPPORTED")

    def test_ce07_bitemporal_not_claimed(self):
        for value in (True, 0, None, "false"):
            context = copy.deepcopy(self.context); context["temporal"]["bitemporal"] = value
            self.assert_blocked(context, "BITEMPORAL_UNSUPPORTED")

    def test_ce08_context_replay_changes_identity(self):
        first = cross.validate_context(self.context)["context_sha256"]
        self.context["sources"][0]["content_sha256"] = "0"*64
        second = cross.validate_context(self.context)["context_sha256"]
        self.assertNotEqual(first, second)

    def test_ce10_static_context_has_no_temporal_join(self):
        context = fixture("ce_l2_static.json")["context"]
        result = cross.validate_context(context)
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual("NOT_APPLICABLE", result["temporal_context"]["pit"])
        self.assertIsNone(result["temporal_context"]["temporal"])
        self.assertFalse(result["join_executed"])

    def test_declared_cardinality_is_not_cardinality_proof(self):
        self.context["cardinality"] = "1:1"
        result = cross.validate_context(self.context)
        self.assertEqual("PASS", result["status"])
        self.assertFalse(result["coverage_measured"])
        self.context["cardinality"] = "N:N"
        self.assert_blocked(self.context, "CARDINALITY_UNSUPPORTED")

    def test_source_ids_columns_and_key_list_are_checked(self):
        for change in (
            lambda x: x["sources"][1].update(id=x["sources"][0]["id"]),
            lambda x: x["sources"][0].update(columns=["other"]),
            lambda x: x.update(anchor="absent"),
            lambda x: x.update(entity_keys=["entity_id", "entity_id"]),
            lambda x: x["sources"][1].update(content_sha256="bad"),
            lambda x: x["sources"][1].update(columns=["entity_id"]),
        ):
            context = copy.deepcopy(self.context); change(context)
            self.assert_blocked(context)

    def test_effect_not_permitted_at_l2(self):
        self.context["requested_effect"] = "WRITE_TABLE"
        self.assert_blocked(self.context, "L2_EFFECT_NOT_ALLOWED")

    def test_no_unknown_context_keys_or_real_data(self):
        self.assert_blocked({**self.context, "secret_option": "enabled"})
        self.assert_blocked({**self.context, "synthetic": False})

    def test_temporal_clock_and_lag_types_checked(self):
        for value in (True, -1, 0.5, "1", None):
            context = copy.deepcopy(self.context); context["temporal"]["lag_days"] = value
            self.assert_blocked(context)
        self.context["temporal"]["availability_column"] = "reference_at"
        self.assert_blocked(self.context, "CLOCKS_MUST_BE_DISTINCT")


class SerializationAndOracleTests(unittest.TestCase):
    def test_duplicate_json_keys_and_nonfinite_numbers_block(self):
        for raw in ('{"pit":"UNKNOWN","pit":"NOT_APPLICABLE"}', '{"x":NaN}', '{"x":Infinity}'):
            with self.assertRaises(ContextError):
                loads_strict(raw)

    def test_context_inconsistent_anchor_grain_blocks(self):
        context = fixture("ce_l2_temporal.json")["context"]
        context["sources"][0]["grain"] = "OTHER_GRAIN"
        self.assertEqual("BLOCKED", cross.validate_context(context)["status"])

    def test_json_identity_rejects_nonfinite_and_nonserializable(self):
        for value in (float("nan"), float("inf"), object()):
            with self.assertRaises((TypeError, ValueError)):
                digest({"value": value})

    def test_cp1252_safe_json_roundtrip(self):
        payload = {"note": "contexto → execução", "status": "PASS"}
        rendered = json.dumps(payload, ensure_ascii=True, allow_nan=False)
        self.assertEqual(payload, json.loads(rendered.encode("cp1252").decode("cp1252")))

    def test_oracle_zero_absence_bool_and_nonfinite_are_distinct(self):
        expected = fixture("vf_cumulative.json")["expected_table"]
        self.assertTrue(verifier._equal_table(expected, expected))
        for value in (0, False, float("nan")):
            tampered = copy.deepcopy(expected); tampered[2]["taxa_acumulada"] = value
            self.assertFalse(verifier._equal_table(tampered, expected))
        bad = copy.deepcopy(expected); bad[0]["n_contratos_safra"] = True
        self.assertFalse(verifier._equal_table(bad, expected))

    def test_oracle_tolerance_and_extra_columns(self):
        expected = fixture("vf_cumulative.json")["expected_table"]
        bad = copy.deepcopy(expected); bad[0]["extra"] = 1
        self.assertFalse(verifier._equal_table(bad, expected))
        bad = copy.deepcopy(expected); bad[1]["taxa"] += 1e-5
        self.assertFalse(verifier._equal_table(bad, expected))

    def test_vintage_output_normalization_preserves_missing(self):
        import pandas as pd
        expected = fixture("vf_cumulative.json")["expected_table"]
        frame = pd.DataFrame(expected)
        normalized = runner._normalize_table(frame)
        self.assertEqual(expected, normalized)
        self.assertIsNone(normalized[2]["taxa_acumulada"])

    def test_vintage_output_rejects_extra_columns(self):
        import pandas as pd
        frame = pd.DataFrame(fixture("vf_cumulative.json")["expected_table"])
        frame["unapproved"] = 0
        with self.assertRaisesRegex(RuntimeError, "SCHEMA_MISMATCH"):
            runner._normalize_table(frame)


class ReleaseBoundaryTests(unittest.TestCase):
    def make_release(self, tmp):
        root = Path(tmp) / ".assistant"
        skill = root / "skills/test-skill"
        skill.mkdir(parents=True)
        source = skill / "execution_contract.json"
        source.write_text("{}\n", encoding="utf-8")
        rel = "skills/test-skill/execution_contract.json"
        manifest = {"manifest_version":"0.1", "skill":"test-skill", "algorithm":"git_blob_sha1",
                    "artifacts":[{"path":rel, "git_blob_sha1":blob(source)}]}
        (skill / "release_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return skill, source, rel, manifest

    def test_current_release_and_changed_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, source, rel, _ = self.make_release(tmp)
            self.assertIn(rel, release_integrity(skill, {rel})["artifacts"])
            source.write_text('{"modified":true}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "INTEGRITY_MISMATCH"):
                release_integrity(skill, {rel})

    def test_manifest_cannot_omit_required_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, _, rel, _ = self.make_release(tmp)
            with self.assertRaisesRegex(ValueError, "FILESET_MISMATCH"):
                release_integrity(skill, {rel, "missing.py"})

    def test_manifest_duplicate_paths_or_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill, _, rel, manifest = self.make_release(tmp)
            for bad in (rel, "../escape.py", "C:/outside.py", "a/../file.py"):
                variant = copy.deepcopy(manifest)
                variant["artifacts"].append({"path":bad, "git_blob_sha1":"a"*40})
                (skill / "release_manifest.json").write_text(json.dumps(variant), encoding="utf-8")
                with self.assertRaises(ValueError):
                    release_integrity(skill, {rel})


class SEFIntegrationTests(unittest.TestCase):
    """Not replaced by mocks; requires the complete actual checkout."""
    def test_real_sef_preflight_cross_static_and_temporal(self):
        for name in ("ce_l2_static.json", "ce_l2_temporal.json"):
            context = fixture(name)["context"]
            actual = cross.preflight(context)
            self.assertEqual("PASS", actual["status"], actual)
            self.assertTrue(cross.verify_preflight(actual, expected_context=context)["valid"])

    def test_actual_public_vintage_helper_receipt_and_trusted_oracle(self):
        for name in ("vf_cumulative.json", "vf_events.json"):
            data = fixture(name); run_id = "integration-" + data["fixture_id"]
            actual = runner.run(data["request"], run_id=run_id)
            self.assertEqual("PASS", actual["status"], actual)
            verification = verifier.verify(actual, expected_request=data["request"], expected_run_id=run_id,
                                           expected_table=data["expected_table"])
            self.assertTrue(verification["valid"], verification)
            wrong_run = verifier.verify(actual, expected_request=data["request"], expected_run_id="other-run",
                                        expected_table=data["expected_table"])
            self.assertFalse(wrong_run["valid"])
            replay_request = copy.deepcopy(data["request"]); replay_request["population_id"] = "another-population"
            self.assertFalse(verifier.verify(actual, expected_request=replay_request, expected_run_id=run_id,
                                            expected_table=data["expected_table"])["valid"])
            tampered = copy.deepcopy(actual); tampered["result"]["table"][0]["taxa"] = 0.9
            self.assertFalse(verifier.verify(tampered, expected_request=data["request"], expected_run_id=run_id,
                                            expected_table=data["expected_table"])["valid"])


if __name__ == "__main__":
    unittest.main()
