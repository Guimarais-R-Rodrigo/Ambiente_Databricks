from __future__ import annotations

import ast
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import temas_v13_ensaios as s6  # noqa: E402


class V13S6OperationalRehearsalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = s6.run_rehearsals()
        cls.by_surface = {item["surface_id"]: item for item in cls.report["surfaces"]}

    def test_report_identity_and_scope_are_closed(self):
        self.assertEqual(self.report["report_version"], 1)
        self.assertEqual(self.report["engine"], "V13-S6")
        self.assertEqual(self.report["scope"], "LOCAL_OR_SIMULATED_ONLY")

    def test_surface_order_matches_plan(self):
        self.assertEqual(
            tuple(item["surface_id"] for item in self.report["surfaces"]),
            s6.SURFACE_ORDER,
        )

    def test_every_surface_exposes_full_cycle_in_order(self):
        for item in self.report["surfaces"]:
            self.assertEqual(tuple(phase["phase"] for phase in item["phases"]), s6.PHASES)

    def test_five_local_or_simulated_rehearsals_pass(self):
        for surface_id in (
            "notebook_visual_core",
            "visual_lab",
            "transition_bundle",
            "databricks_app",
            "aibi_dashboard",
        ):
            self.assertEqual(self.by_surface[surface_id]["overall_status"], "PASS", surface_id)

    def test_workspace_theme_remains_blocked(self):
        item = self.by_surface["workspace_theme"]
        self.assertEqual(item["overall_status"], "BLOCKED")
        self.assertEqual(item["phases"][1]["status"], "BLOCKED")
        self.assertEqual(item["phases"][1]["code"], "AUTHORIZATION_BLOCKED")
        self.assertTrue(all(phase["status"] == "NOT_APPLICABLE" for phase in item["phases"][2:]))

    def test_notebook_semantics_and_rollback_pass(self):
        item = self.by_surface["notebook_visual_core"]
        self.assertEqual(item["phases"][4]["code"], "SEMANTICS_PRESERVED")
        self.assertEqual(item["phases"][5]["code"], "DISCARD_STAGE_VERIFIED")
        self.assertFalse(item["local_mutation_performed"])

    def test_visual_lab_session_roundtrip_and_restore_pass(self):
        item = self.by_surface["visual_lab"]
        self.assertEqual(item["phases"][3]["code"], "LOCAL_SESSION_STAGED")
        self.assertEqual(item["phases"][4]["code"], "SESSION_ROUNDTRIP_VERIFIED")
        self.assertEqual(item["phases"][5]["code"], "RESTORE_BASE_VERIFIED")
        self.assertTrue(item["local_mutation_performed"])

    def test_v09_stage_and_rollback_are_local_and_verified(self):
        item = self.by_surface["transition_bundle"]
        self.assertEqual(item["phases"][2]["code"], "V09_BUNDLE_PACKAGED")
        self.assertEqual(item["phases"][3]["code"], "LOCAL_STAGE_VERIFIED")
        self.assertEqual(item["phases"][5]["code"], "ROLLBACK_DRY_RUN_VERIFIED")
        self.assertTrue(item["local_mutation_performed"])

    def test_v10_stage_and_rollback_are_local_and_verified(self):
        item = self.by_surface["databricks_app"]
        self.assertEqual(item["phases"][2]["code"], "V10_APP_BUNDLE_PACKAGED")
        self.assertEqual(item["phases"][3]["code"], "LOCAL_STAGE_VERIFIED")
        self.assertEqual(item["phases"][5]["code"], "ROLLBACK_DRY_RUN_VERIFIED")
        self.assertTrue(item["local_mutation_performed"])

    def test_aibi_fixture_uses_local_binding_and_preserves_semantics(self):
        item = self.by_surface["aibi_dashboard"]
        self.assertEqual(item["phases"][3]["code"], "LOCAL_FIXTURE_BOUND")
        self.assertEqual(item["phases"][4]["code"], "SEMANTICS_PRESERVED")
        self.assertEqual(item["phases"][5]["code"], "DISCARD_BOUND_COPY_VERIFIED")
        self.assertFalse(item["local_mutation_performed"])

    def test_real_environment_cases_remain_exactly_three_and_blocked(self):
        expected = {
            ("V12-LAB-01", "visual_lab"),
            ("V12-APP-01", "databricks_app"),
            ("V12-AIBI-02", "workspace_theme"),
        }
        actual = {
            (item["case_id"], item["surface_id"])
            for item in self.report["real_environment_cases"]
        }
        self.assertEqual(actual, expected)
        self.assertTrue(
            all(item["status"] == "BLOQUEADO_AUTORIZACAO" for item in self.report["real_environment_cases"])
        )

    def test_s6_does_not_reclassify_a11_or_issue_57(self):
        self.assertEqual(self.report["a11_status"], "FAIL")
        self.assertEqual(self.report["issue_57_state_expected"], "open")

    def test_s7_is_not_started(self):
        self.assertIs(self.report["s7_started"], False)

    def test_global_boundary_has_no_network_remote_mutation_or_publication(self):
        self.assertIs(self.report["network_access"], False)
        self.assertIs(self.report["remote_mutation_performed"], False)
        self.assertIs(self.report["publication_performed"], False)

    def test_every_surface_preserves_remote_boundary(self):
        for item in self.report["surfaces"]:
            self.assertIs(item["network_access"], False, item["surface_id"])
            self.assertIs(item["remote_mutation_performed"], False, item["surface_id"])
            self.assertIs(item["publication_performed"], False, item["surface_id"])
            self.assertIs(item["evidence_sanitized"], True, item["surface_id"])

    def test_evidence_refs_are_repository_relative_and_sanitized(self):
        for item in self.report["surfaces"]:
            self.assertTrue(item["evidence_refs"])
            for ref in item["evidence_refs"]:
                self.assertFalse(ref.startswith(("/", "\\")))
                self.assertNotIn("..", Path(ref).parts)
                self.assertTrue((ROOT / ref).exists(), ref)

    def test_report_does_not_expose_temp_paths_credentials_or_email(self):
        payload = json.dumps(self.report, ensure_ascii=False)
        for forbidden in ("sk-proj-", "DATABRICKS_TOKEN", "\\Temp\\", "/tmp/", "@gmail.com"):
            self.assertNotIn(forbidden, payload)
        self.assertIsNone(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", payload))

    def test_all_phase_statuses_use_closed_vocabulary(self):
        allowed = {"PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"}
        for item in self.report["surfaces"]:
            for phase in item["phases"]:
                self.assertIn(phase["status"], allowed)

    def test_no_surface_infers_remote_pass_from_local_pass(self):
        remote_cases = {item["surface_id"] for item in self.report["real_environment_cases"]}
        self.assertEqual(remote_cases, {"visual_lab", "databricks_app", "workspace_theme"})
        self.assertTrue(all(item["status"] != "PASS" for item in self.report["real_environment_cases"]))

    def test_tool_has_no_network_or_databricks_client_import(self):
        source_path = ROOT / "tools/temas_v13_ensaios.py"
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        forbidden_roots = {"requests", "socket", "urllib", "httpx", "databricks"}
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported.isdisjoint(forbidden_roots), imported & forbidden_roots)

    def test_subprocess_is_restricted_to_canonical_local_builder(self):
        source = (ROOT / "tools/temas_v13_ensaios.py").read_text(encoding="utf-8")
        self.assertIn("tools/bundle_implantacao.py", source)
        for forbidden in ("databricks apps", "databricks workspace", "databricks auth", "curl ", "requests."):
            self.assertNotIn(forbidden, source)

    def test_s6_document_covers_plan_order_and_remote_boundary(self):
        text = (ROOT / "docs/sprints/sistema_temas/V13/S6_ENSAIOS_OPERACIONAIS.md").read_text(encoding="utf-8")
        for marker in (
            "notebook/Plotly/HTML local",
            "Visual Lab local/simulado",
            "bundle V09",
            "App V10",
            "AI/BI V11",
            "ambiente Databricks real",
            "BLOQUEADO_AUTORIZACAO",
            "V13_S7_NOT_STARTED=1",
        ):
            self.assertIn(marker, text)

    def test_s6_document_keeps_historical_v12_states_distinct(self):
        text = (ROOT / "docs/sprints/sistema_temas/V13/S6_ENSAIOS_OPERACIONAIS.md").read_text(encoding="utf-8")
        self.assertIn("V12-AIBI-01", text)
        self.assertIn("A11-01 = FAIL", text)
        self.assertIn("issue #57", text)
        for case_id in ("V12-LAB-01", "V12-APP-01", "V12-AIBI-02"):
            self.assertIn(case_id, text)

    def test_v13_live_readme_preserves_s6_history_when_s7_starts(self):
        text = (ROOT / "docs/sprints/sistema_temas/V13/README.md").read_text(encoding="utf-8")
        self.assertIn("S6 — PR #65", text)
        self.assertIn("6dfb8707835921f2f48020f383cf571902080109", text)
        self.assertIn("S7 — handoff operacional e fechamento", text)
        self.assertIn("HUMAN-01 = BLOCKED", text)
        self.assertIn("V14 não foi iniciada", text)

    def test_workflow_runs_s6_read_only(self):
        text = (ROOT / ".github/workflows/temas-v13-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("V13 S6 — ensaios operacionais locais/simulados", text)
        self.assertIn("python -B tools/tests/test_temas_v13_s6.py -v", text)
        for forbidden in ("DATABRICKS_TOKEN", "DATABRICKS_HOST", "secrets."):
            self.assertNotIn(forbidden, text)

    def test_workflow_s6_frontier_is_explicit(self):
        text = (ROOT / ".github/workflows/temas-v13-ci.yml").read_text(encoding="utf-8")
        for marker in (
            "V13_S6_NETWORK=0",
            "V13_S6_REMOTE_MUTATION=0",
            "V13_S6_IMPLICIT_PUBLICATION=0",
            "V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5",
            "V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3",
        ):
            self.assertIn(marker, text)
        self.assertNotIn('echo "V13_S6_NOT_STARTED=1"', text)
        self.assertIn("Historical S5 checkpoint assertion: V13_S6_NOT_STARTED=1", text)
        self.assertNotIn('echo "V13_S7_NOT_STARTED=1"', text)
        self.assertIn("Historical S6 checkpoint assertion: V13_S7_NOT_STARTED=1", text)

    def test_no_product_or_simulated_tree_is_an_s6_artifact(self):
        doc = (ROOT / "docs/sprints/sistema_temas/V13/S6_ENSAIOS_OPERACIONAIS.md").read_text(encoding="utf-8")
        self.assertIn("não altera `ambiente_fonte/`", doc)
        self.assertIn("não edita `Novo_Ambiente_Simulado/`", doc)

    def test_rehearsal_report_is_json_serializable_without_custom_encoder(self):
        encoded = json.dumps(self.report, ensure_ascii=False, sort_keys=True)
        self.assertEqual(json.loads(encoded)["engine"], "V13-S6")


if __name__ == "__main__":
    unittest.main()
