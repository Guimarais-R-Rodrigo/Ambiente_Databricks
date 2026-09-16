"""V13-S5 — compatibilidade e acessibilidade operacional, fail-closed."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "temas_v13_compatibilidade.py"
SPEC = importlib.util.spec_from_file_location("temas_v13_compatibilidade", MODULE_PATH)
assert SPEC and SPEC.loader
s5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s5)

DOC = ROOT / "docs" / "sprints" / "sistema_temas" / "V13" / "S5_COMPATIBILIDADE_ACESSIBILIDADE.md"
V13_README = ROOT / "docs" / "sprints" / "sistema_temas" / "V13" / "README.md"
V12_TESTES = ROOT / "docs" / "sprints" / "sistema_temas" / "V12" / "TESTES.md"
S1_MATRIX = ROOT / "docs" / "sprints" / "sistema_temas" / "V13" / "MATRIZ_OPERACIONAL.json"
WORKFLOW = ROOT / ".github" / "workflows" / "temas-v13-ci.yml"

SHA = "1c136fa9218c49754caa849883a13cefb51a913ad5df7d47e773a5ea65085802"


def pair(pair_id: str = "pair", foreground: str = "#000000", background: str = "#FFFFFF",
         mode: str = "LIGHT", text_class: str = "NORMAL", observed: bool = True) -> dict:
    return {
        "pair_id": pair_id,
        "foreground": foreground,
        "background": background,
        "mode": mode,
        "text_class": text_class,
        "observed": observed,
    }


def request(pairs: list[dict] | None = None) -> dict:
    return {
        "schema_version": 1,
        "engine": "V13-S5",
        "surface_id": "aibi_dashboard",
        "evidence_basis": "REVIEWED_REAL_EXPORT",
        "export_sha256": SHA,
        "synthetic_fixture_used": False,
        "pairs": [pair()] if pairs is None else pairs,
    }


def error_code(payload) -> str:
    with unittest.TestCase().assertRaises(s5.CompatibilityRequestError) as cm:
        s5.evaluate(payload)
    return cm.exception.code


class V13S5CompatibilityTests(unittest.TestCase):
    def test_black_white_ratio_is_exactly_twenty_one(self):
        self.assertEqual(s5.contrast_ratio("#000000", "#FFFFFF"), 21.0)

    def test_historical_a11_pairs_reproduce_documented_ratios_and_fail(self):
        historical = [
            pair("conditional_red_light_widget", "#9C2638", "#E8F4FD", "LIGHT"),
            pair("conditional_red_dark_widget", "#9C2638", "#11171C", "DARK"),
            pair("conditional_yellow_light_widget", "#FFD465", "#E8F4FD", "LIGHT"),
            pair("conditional_yellow_dark_widget", "#FFD465", "#11171C", "DARK"),
        ]
        report = s5.evaluate(request(historical))
        ratios = {item["pair_id"]: item["ratio"] for item in report["pairs"]}
        self.assertAlmostEqual(ratios["conditional_red_light_widget"], 6.837793163467097, places=14)
        self.assertAlmostEqual(ratios["conditional_red_dark_widget"], 2.3624715346329377, places=14)
        self.assertAlmostEqual(ratios["conditional_yellow_light_widget"], 1.264684095079348, places=14)
        self.assertAlmostEqual(ratios["conditional_yellow_dark_widget"], 12.773222792356847, places=14)
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertEqual([item["status"] for item in report["pairs"]], ["PASS", "FAIL", "FAIL", "PASS"])

    def test_historical_colors_are_anchored_in_v12_evidence_document(self):
        text = V12_TESTES.read_text(encoding="utf-8")
        for value in ("#9C2638", "#FFD465", "#E8F4FD", "#11171C",
                      "6.837793163467097", "2.3624715346329377",
                      "1.264684095079348", "12.773222792356847"):
            self.assertIn(value, text)

    def test_decision_uses_raw_ratio_without_rounding_to_pass(self):
        report = s5.evaluate(request([pair("near", "#777777", "#FFFFFF")]))
        item = report["pairs"][0]
        self.assertLess(item["ratio"], 4.5)
        self.assertEqual(item["status"], "FAIL")

    def test_large_text_uses_three_to_one_only_when_declared(self):
        normal = s5.evaluate(request([pair("n", "#777777", "#FFFFFF", text_class="NORMAL")]))
        large = s5.evaluate(request([pair("l", "#777777", "#FFFFFF", text_class="LARGE")]))
        self.assertEqual(normal["pairs"][0]["status"], "FAIL")
        self.assertEqual(large["pairs"][0]["status"], "PASS")
        self.assertEqual(normal["pairs"][0]["required_ratio"], 4.5)
        self.assertEqual(large["pairs"][0]["required_ratio"], 3.0)

    def test_unobserved_pair_is_not_inferred_and_has_no_ratio(self):
        report = s5.evaluate(request([pair("not_seen", "#000000", "#FFFFFF", observed=False)]))
        item = report["pairs"][0]
        self.assertEqual(item["status"], "NOT_APPLICABLE")
        self.assertEqual(item["code"], "STATE_NOT_EXERCISED")
        self.assertIsNone(item["ratio"])
        self.assertEqual(report["overall_status"], "NOT_APPLICABLE")

    def test_high_contrast_unexercised_is_explicit(self):
        report = s5.evaluate(request([pair("light", "#000000", "#FFFFFF", mode="LIGHT")]))
        self.assertEqual(report["mode_coverage"]["HIGH_CONTRAST"], "NOT_EXERCISED")
        self.assertEqual(report["mode_coverage"]["DARK"], "NOT_EXERCISED")

    def test_observed_high_contrast_is_measured_not_assumed(self):
        report = s5.evaluate(request([pair("hc", "#000000", "#FFFFFF", mode="HIGH_CONTRAST")]))
        self.assertEqual(report["mode_coverage"]["HIGH_CONTRAST"], "EXERCISED")
        self.assertEqual(report["pairs"][0]["status"], "PASS")

    def test_fail_dominates_passing_pairs(self):
        report = s5.evaluate(request([
            pair("pass", "#000000", "#FFFFFF"),
            pair("fail", "#777777", "#FFFFFF"),
        ]))
        self.assertEqual(report["overall_status"], "FAIL")
        self.assertEqual(report["decision_code"], "CONTRAST_FAIL")

    def test_all_observed_pairs_passing_yields_local_pass_only(self):
        report = s5.evaluate(request([pair("pass", "#000000", "#FFFFFF")]))
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["scope"], "LOCAL_CONTRAST_PREFLIGHT_ONLY")
        self.assertFalse(report["evidence_authenticated"])

    def test_output_never_claims_network_or_remote_mutation(self):
        report = s5.evaluate(request())
        self.assertFalse(report["network_access"])
        self.assertFalse(report["remote_mutation_performed"])
        self.assertFalse(report["v11_binding_contract_changed"])

    def test_wrong_request_type_fails(self):
        self.assertEqual(error_code([]), "REQUEST_TYPE")

    def test_extra_or_missing_field_fails(self):
        payload = request()
        payload["extra"] = True
        self.assertEqual(error_code(payload), "REQUEST_FIELDS")

    def test_wrong_engine_or_version_fails(self):
        payload = request()
        payload["engine"] = "V13-S4"
        self.assertEqual(error_code(payload), "REQUEST_VERSION")

    def test_other_surface_is_not_silently_generalized(self):
        payload = request()
        payload["surface_id"] = "workspace_theme"
        self.assertEqual(error_code(payload), "SURFACE_UNSUPPORTED")

    def test_non_real_evidence_basis_fails(self):
        payload = request()
        payload["evidence_basis"] = "SYNTHETIC"
        self.assertEqual(error_code(payload), "EVIDENCE_BASIS_INVALID")

    def test_bad_export_hash_fails(self):
        payload = request()
        payload["export_sha256"] = "abc"
        self.assertEqual(error_code(payload), "EXPORT_HASH_INVALID")

    def test_synthetic_fixture_is_forbidden_as_real_export(self):
        payload = request()
        payload["synthetic_fixture_used"] = True
        self.assertEqual(error_code(payload), "SYNTHETIC_FIXTURE_FORBIDDEN")

    def test_pairs_must_be_nonempty_list(self):
        self.assertEqual(error_code(request([])), "PAIRS_INVALID")

    def test_pair_shape_is_closed(self):
        payload = request()
        payload["pairs"][0]["extra"] = "x"
        self.assertEqual(error_code(payload), "PAIR_SHAPE_INVALID")

    def test_pair_id_is_sanitized_and_unique(self):
        self.assertEqual(error_code(request([pair("../secret")])), "PAIR_ID_INVALID")
        duplicate = [pair("same"), pair("same", mode="DARK")]
        self.assertEqual(error_code(request(duplicate)), "PAIR_ID_DUPLICATE")

    def test_color_must_be_six_digit_hex_without_alpha(self):
        for value in ("#FFF", "#FFFFFFFF", "red", "#GG0000"):
            payload = request([pair("bad", value, "#FFFFFF")])
            self.assertEqual(error_code(payload), "COLOR_INVALID")

    def test_mode_is_closed_enum(self):
        self.assertEqual(error_code(request([pair("bad", mode="AUTO")])), "MODE_INVALID")

    def test_text_class_is_closed_enum(self):
        self.assertEqual(error_code(request([pair("bad", text_class="HUGE")])), "TEXT_CLASS_INVALID")

    def test_observed_must_be_boolean(self):
        payload = request([pair("bad")])
        payload["pairs"][0]["observed"] = 1
        self.assertEqual(error_code(payload), "OBSERVED_INVALID")

    def test_same_request_is_deterministic(self):
        payload = request([
            pair("a", "#9C2638", "#11171C", "DARK"),
            pair("b", "#000000", "#FFFFFF", "HIGH_CONTRAST", observed=False),
        ])
        self.assertEqual(s5.evaluate(payload), s5.evaluate(json.loads(json.dumps(payload))))

    def test_tool_has_no_network_databricks_shell_or_mutation_import(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = ("import requests", "import socket", "import urllib", "import httpx",
                     "from databricks", "import databricks", "import subprocess", "import shutil")
        for token in forbidden:
            self.assertNotIn(token, source)

    def test_compatibility_matrix_documents_exact_s1_surfaces_and_owner_refs(self):
        inventory = json.loads(S1_MATRIX.read_text(encoding="utf-8"))
        doc = DOC.read_text(encoding="utf-8")
        surface_ids = [item["surface_id"] for item in inventory["surfaces"]]
        self.assertEqual(set(surface_ids), {
            "notebook_visual_core", "visual_lab", "transition_bundle",
            "databricks_app", "aibi_dashboard", "workspace_theme",
        })
        for item in inventory["surfaces"]:
            self.assertIn(f"`{item['surface_id']}`", doc)
            self.assertIn(item["primary_owner"]["contract_ref"], doc)

    def test_document_decides_preflight_but_keeps_issue_open_and_v11_frozen(self):
        doc = DOC.read_text(encoding="utf-8")
        for phrase in (
            "PREFLIGHT_FAIL_CLOSED",
            "issue #57 permanece aberta",
            "3 `translated`, 23 `approximated`, 22 `unsupported`",
            "cellFormat` não vira token",
            "S6 não foi iniciada",
        ):
            self.assertIn(phrase, doc)

    def test_document_explicitly_covers_light_dark_and_high_contrast(self):
        doc = DOC.read_text(encoding="utf-8")
        for mode in ("Light", "Dark", "High Contrast"):
            self.assertIn(mode, doc)
        self.assertIn("NOT_EXERCISED", doc)

    def test_workflow_runs_s5_read_only_and_preserves_s4_history(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("V13 S5 — compatibilidade e acessibilidade operacional", workflow)
        self.assertIn("python -B tools/tests/test_temas_v13_s5.py -v", workflow)
        self.assertIn("V13_S5_NETWORK=0", workflow)
        self.assertIn("V13_S5_REMOTE_MUTATION=0", workflow)
        self.assertIn("V13_S5_CONTRAST_PREFLIGHT_LOCAL=1", workflow)
        self.assertIn("Historical S5 checkpoint assertion: V13_S6_NOT_STARTED=1", workflow)
        self.assertNotIn('echo "V13_S6_NOT_STARTED=1"', workflow)
        self.assertIn("Historical S4 checkpoint assertion: V13_S5_NOT_STARTED=1", workflow)
        self.assertNotIn("DATABRICKS_TOKEN", workflow)
        self.assertNotIn("secrets.", workflow)

    def test_v13_live_readme_preserves_s5_history_when_s7_starts(self):
        text = V13_README.read_text(encoding="utf-8")
        self.assertIn("S5 — PR #64", text)
        self.assertIn("11e4e17f02d4ba7846f5b80bd88c0180124b5772", text)
        self.assertIn("S6 — PR #65", text)
        self.assertIn("6dfb8707835921f2f48020f383cf571902080109", text)
        self.assertIn("S7 — handoff operacional e fechamento", text)
        self.assertIn("HUMAN-01 = BLOCKED", text)
        self.assertIn("V14 não foi iniciada", text)


if __name__ == "__main__":
    unittest.main()
