"""V12 — homologação de jornadas: evidência separada, fail-closed e sem Databricks remoto."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "temas_v12_homologacao.py"
SPEC = importlib.util.spec_from_file_location("temas_v12_homologacao", MODULE_PATH)
assert SPEC and SPEC.loader
v12 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v12)

MATRIX_PATH = ROOT / "docs" / "sprints" / "sistema_temas" / "V12" / "matriz_homologacao.json"
V11_TEST = ROOT / "tools" / "tests" / "test_temas_v11.py"
AIBI_FIXTURE = ROOT / "ambiente_fonte" / ".assistant" / "hub_padroes" / "identidade_visual" / "aibi" / "dashboard_sintetico.json"
WORKFLOW = ROOT / ".github" / "workflows" / "temas-v12-ci.yml"
SHA = "a" * 64
COMMIT = "b" * 40


def artifact():
    return [{"kind": "sanitized_log", "sha256": "c" * 64, "path": "evidence://sanitized"}]


def env_base(case_id: str, facts: dict):
    facts = dict(facts)
    facts.setdefault("oracle_met", True)
    return {
        "schema_version": 1,
        "sprint": "V12",
        "record_id": f"V12-{case_id.replace('-', '_')}",
        "case_id": case_id,
        "evidence_class": "databricks_environment",
        "status": "PASS",
        "source_commit": COMMIT,
        "observed_at": "2026-09-14T20:30:00-03:00",
        "environment": {
            "environment_class": "databricks_nonprod_authorized",
            "environment_authorized": True,
            "authorization_ref": "AUTH-V12-TEST",
        },
        "human": {},
        "facts": facts,
        "artifacts": artifact(),
        "notes": "fixture sintética de teste do validador",
    }


def human_base(case_id: str, facts: dict, role="nontechnical_user"):
    facts = dict(facts)
    facts.setdefault("oracle_met", True)
    return {
        "schema_version": 1,
        "sprint": "V12",
        "record_id": f"V12-{case_id.replace('-', '_')}",
        "case_id": case_id,
        "evidence_class": "human_uat",
        "status": "PASS",
        "source_commit": COMMIT,
        "observed_at": "2026-09-14T20:30:00-03:00",
        "environment": {},
        "human": {
            "participant_alias": "P-01",
            "participant_authorized": True,
            "participant_role": role,
        },
        "facts": facts,
        "artifacts": artifact(),
        "notes": "fixture sintética de teste do validador",
    }


class MatrixContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = v12.load_matrix(MATRIX_PATH)
        cls.cases = {item["id"]: item for item in cls.matrix["cases"]}

    def test_canonical_human_cases_from_v01_are_preserved(self):
        self.assertTrue({"DOC-02", "DOC-03", "A11-01", "SEC-01", "UAT-01"} <= set(self.cases))

    def test_evidence_classes_are_not_synonyms(self):
        policy = self.matrix["claim_policy"]
        self.assertTrue(policy["git_local_does_not_prove_databricks"])
        self.assertTrue(policy["databricks_does_not_prove_human_uat"])
        self.assertTrue(policy["automated_test_does_not_prove_human_uat"])
        self.assertTrue(policy["production_ready_is_not_v12_synonym"])

    def test_v12_keeps_v11_native_fixture_non_importable(self):
        fixture = json.loads(AIBI_FIXTURE.read_text(encoding="utf-8"))
        self.assertFalse(fixture["databricks_importable"])
        self.assertEqual(fixture["data_classification"], "synthetic_only")

    def test_v11_direct_mapping_contract_is_unchanged(self):
        text = V11_TEST.read_text(encoding="utf-8")
        self.assertIn('"widget.background"', text)
        self.assertIn('"widget.corner_radius"', text)
        self.assertIn('"visualization.categorical_palette"', text)
        self.assertIn('{"translated": 3, "approximated": 23, "unsupported": 22}', text)


class EvidenceFailClosedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = v12.load_matrix(MATRIX_PATH)

    def assertCode(self, expected, record):
        with self.assertRaises(v12.V12EvidenceError) as cm:
            v12.validate_evidence(record, self.matrix)
        self.assertEqual(cm.exception.code, expected)

    def test_pending_record_does_not_fake_pass(self):
        record = human_base("UAT-01", {
            "participant_authorized": False,
            "observed_seconds": None,
            "help_events": [],
            "journey_completed": False,
            "shared_change_absent": False,
        })
        record["status"] = "BLOQUEADO_AUTORIZACAO"
        record["facts"]["oracle_met"] = False
        record["artifacts"] = []
        v12.validate_evidence(record, self.matrix)

    def test_pass_without_evidence_is_rejected(self):
        record = human_base("UAT-01", {
            "participant_authorized": True,
            "observed_seconds": 31,
            "help_events": [],
            "journey_completed": True,
            "shared_change_absent": True,
        })
        record["artifacts"] = []
        self.assertCode("V12_PASS_WITHOUT_EVIDENCE", record)

    def test_human_pass_requires_authorized_real_participant(self):
        record = human_base("UAT-01", {
            "participant_authorized": False,
            "observed_seconds": 31,
            "help_events": [],
            "journey_completed": True,
            "shared_change_absent": True,
        })
        record["human"]["participant_authorized"] = False
        self.assertCode("V12_PARTICIPANT_AUTH", record)

    def test_human_pass_requires_observed_duration_when_case_requires_it(self):
        record = human_base("DOC-02", {
            "participant_authorized": True,
            "observed_seconds": None,
            "help_events": [],
            "document_version": "V12-candidate",
            "next_action_identified_without_help": True,
        })
        self.assertCode("V12_DURATION", record)

    def test_mutation_requires_explicit_authorization_reference_and_rollback(self):
        record = env_base("V12-LAB-01", {
            "environment_authorized": True,
            "authorization_ref": "",
            "synthetic_data_only": True,
            "rollback_plan_verified": True,
            "browser_observed": True,
            "persistence_observed": True,
        })
        record["environment"]["authorization_ref"] = ""
        self.assertCode("V12_AUTH_REQUIRED", record)

    def test_real_environment_pass_rejects_non_synthetic_data(self):
        record = env_base("V12-LAB-01", {
            "environment_authorized": True,
            "authorization_ref": "AUTH-V12-TEST",
            "synthetic_data_only": False,
            "rollback_plan_verified": True,
            "browser_observed": True,
            "persistence_observed": True,
        })
        self.assertCode("V12_FACT_VALUE", record)

    def _aibi_record(self):
        return env_base("V12-AIBI-01", {
            "environment_authorized": True,
            "authorization_ref": "AUTH-V12-TEST",
            "synthetic_data_only": True,
            "rollback_plan_verified": True,
            "dashboard_draft": True,
            "export_sha256": SHA,
            "reviewed_export_sha256": SHA,
            "used_export_sha256": SHA,
            "semantic_before_sha256": "d" * 64,
            "semantic_after_sha256": "d" * 64,
            "synthetic_fixture_used_as_databricks_input": False,
            "approximated_automated": False,
            "unsupported_automated": False,
            "published": False,
            "light_dark_observed": True,
        })

    def test_aibi_rejects_stale_export_hash(self):
        record = self._aibi_record()
        record["facts"]["used_export_sha256"] = "e" * 64
        self.assertCode("V12_EXPORT_STALE", record)

    def test_aibi_rejects_semantic_drift(self):
        record = self._aibi_record()
        record["facts"]["semantic_after_sha256"] = "e" * 64
        self.assertCode("V12_SEMANTIC_DRIFT", record)

    def test_aibi_rejects_synthetic_fixture_as_databricks_input(self):
        record = self._aibi_record()
        record["facts"]["synthetic_fixture_used_as_databricks_input"] = True
        self.assertCode("V12_FACT_VALUE", record)

    def test_aibi_rejects_approximated_automation(self):
        record = self._aibi_record()
        record["facts"]["approximated_automated"] = True
        self.assertCode("V12_FACT_VALUE", record)

    def test_aibi_rejects_unsupported_automation(self):
        record = self._aibi_record()
        record["facts"]["unsupported_automated"] = True
        self.assertCode("V12_FACT_VALUE", record)

    def test_aibi_dashboard_journey_rejects_accidental_publication(self):
        record = self._aibi_record()
        record["facts"]["published"] = True
        self.assertCode("V12_FACT_VALUE", record)

    def test_workspace_theme_rejects_live_link_claim(self):
        record = env_base("V12-AIBI-02", {
            "environment_authorized": True,
            "authorization_ref": "AUTH-V12-TEST",
            "synthetic_data_only": True,
            "rollback_plan_verified": True,
            "identity_checked": True,
            "permission_checked": True,
            "workspace_admin_observed": True,
            "new_dashboard_inheritance_observed": True,
            "snapshot_observed": True,
            "reapply_observed": True,
            "auto_propagation_claimed": True,
            "published": False,
        })
        self.assertCode("V12_FACT_VALUE", record)

    def test_workspace_theme_publication_requires_own_authorization(self):
        record = env_base("V12-AIBI-02", {
            "environment_authorized": True,
            "authorization_ref": "AUTH-V12-TEST",
            "synthetic_data_only": True,
            "rollback_plan_verified": True,
            "identity_checked": True,
            "permission_checked": True,
            "workspace_admin_observed": True,
            "new_dashboard_inheritance_observed": True,
            "snapshot_observed": True,
            "reapply_observed": True,
            "auto_propagation_claimed": False,
            "published": True,
        })
        self.assertCode("V12_PUBLICATION_AUTH", record)

    def test_app_pass_requires_real_identity_isolation_and_absent_publication_actions(self):
        record = env_base("V12-APP-01", {
            "environment_authorized": True,
            "authorization_ref": "AUTH-V12-TEST",
            "synthetic_data_only": True,
            "rollback_plan_verified": True,
            "identity_checked": True,
            "permission_checked": True,
            "browser_observed": True,
            "isolation_observed": False,
            "publication_actions_absent": True,
        })
        self.assertCode("V12_FACT_VALUE", record)

    def test_a11_pass_requires_measured_contrast_not_rounded_up(self):
        record = human_base("A11-01", {
            "participant_authorized": True,
            "render_observed": True,
            "contrast_measurements": [{"label": "texto", "ratio": 4.49, "required_ratio": 4.5}],
            "keyboard_review": True,
            "zoom_review": True,
        })
        self.assertCode("V12_CONTRAST", record)

    def test_pass_requires_oracle_explicitly_met(self):
        record = human_base("UAT-01", {
            "participant_authorized": True,
            "observed_seconds": 44,
            "help_events": [],
            "journey_completed": True,
            "shared_change_absent": True,
            "oracle_met": False,
        })
        self.assertCode("V12_FACT_VALUE", record)

    def test_valid_aibi_draft_evidence_passes(self):
        v12.validate_evidence(self._aibi_record(), self.matrix)

    def test_valid_uat_evidence_passes_without_claiming_environment(self):
        record = human_base("UAT-01", {
            "participant_authorized": True,
            "observed_seconds": 44,
            "help_events": [],
            "journey_completed": True,
            "shared_change_absent": True,
        })
        v12.validate_evidence(record, self.matrix)


class PackagingAndWorkflowTests(unittest.TestCase):
    def test_v12_workflow_is_read_only_and_has_no_databricks_credentials(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        forbidden = (
            "DATABRICKS_" + "TOKEN",
            "DATABRICKS_CLIENT_" + "SECRET",
            "databricks auth",
            "databricks workspace",
            "WorkspaceClient",
            "/api/2.0/",
        )
        self.assertIn("permissions:\n  contents: read", text)
        self.assertIn("persist-credentials: false", text)
        for needle in forbidden:
            self.assertNotIn(needle, text)

    def test_v12_tool_has_no_network_or_databricks_client(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        for needle in ("databricks.sdk", "requests.", "urllib.request", "subprocess.", "/api/2.0/"):
            self.assertNotIn(needle, text)

    def test_matrix_hash_is_stable_for_traceability(self):
        first = MATRIX_PATH.read_bytes()
        second = MATRIX_PATH.read_bytes()
        self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest())


if __name__ == "__main__":
    unittest.main(verbosity=2)
