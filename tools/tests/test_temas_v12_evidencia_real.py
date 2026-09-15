"""V12 — regressão das evidências reais e guardas endurecidas, sem converter CI em ambiente."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "temas_v12_homologacao.py"
SPEC = importlib.util.spec_from_file_location("temas_v12_homologacao_evidence", MODULE_PATH)
assert SPEC and SPEC.loader
v12 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v12)

V12_ROOT = ROOT / "docs" / "sprints" / "sistema_temas" / "V12"
MATRIX = V12_ROOT / "matriz_homologacao.json"
V01_MATRIX = ROOT / "docs" / "sprints" / "sistema_temas" / "V01" / "matriz_testes.json"
WORKFLOW = ROOT / ".github" / "workflows" / "temas-v12-ci.yml"
EVIDENCE = V12_ROOT / "evidencias" / "V12-AIBI-01"
ATTEMPT_1 = EVIDENCE / "V12-AIBI-01_attempt-01.json"
ATTEMPT_2 = EVIDENCE / "V12-AIBI-01_attempt-02.json"
SEC_01 = V12_ROOT / "evidencias" / "SEC-01" / "SEC-01_attempt-01.json"
SYNTHETIC_SQL = (
    EVIDENCE / "synthetic_trips.sql",
    EVIDENCE / "synthetic_route_revenue.sql",
)
MATRIX_SHA256 = "493e45a23de2858de50524fe60bb907fd8e2b7cbaf0211ba3d95aa626944dfd3"
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")

_HUMAN_SOURCE_COMMIT = "89486948045e7222232f8d3aa4c602151f46c6c1"
_HUMAN_DOCUMENT_VERSION = f"theme_lab-docs@{_HUMAN_SOURCE_COMMIT}"
_HUMAN_ARTIFACT = {
    "kind": "human_session_observation",
    "sha256": "9277a8d9a12675dc4dcab8ca920531d10f65e230205df55059539bac91ac530e",
    "path": "evidence://v12-human/session-01",
}

DOC_02_RECORD = {
    "schema_version": 1,
    "sprint": "V12",
    "record_id": "V12-DOC_02-ATTEMPT_01",
    "case_id": "DOC-02",
    "evidence_class": "human_uat",
    "status": "PASS",
    "source_commit": _HUMAN_SOURCE_COMMIT,
    "observed_at": "2026-09-15T18:25:07-03:00",
    "environment": {},
    "human": {
        "participant_alias": "P-UAT-01",
        "participant_authorized": True,
        "participant_role": "nontechnical_user",
    },
    "facts": {
        "participant_authorized": True,
        "observed_seconds": 25,
        "help_events": [],
        "document_version": _HUMAN_DOCUMENT_VERSION,
        "oracle_met": True,
        "next_action_identified_without_help": True,
    },
    "artifacts": [_HUMAN_ARTIFACT],
    "notes": "Sessão formativa real; somente README e guia de primeiro uso foram entregues, sem ajuda verbal inicial. Identidade pessoal não é versionada.",
}

DOC_03_RECORD = {
    "schema_version": 1,
    "sprint": "V12",
    "record_id": "V12-DOC_03-ATTEMPT_01",
    "case_id": "DOC-03",
    "evidence_class": "human_uat",
    "status": "PASS",
    "source_commit": _HUMAN_SOURCE_COMMIT,
    "observed_at": "2026-09-15T18:25:07-03:00",
    "environment": {},
    "human": {
        "participant_alias": "P-UAT-01",
        "participant_authorized": True,
        "participant_role": "nontechnical_user",
    },
    "facts": {
        "participant_authorized": True,
        "help_events": [],
        "document_version": _HUMAN_DOCUMENT_VERSION,
        "oracle_met": True,
        "scope_persistence_explained_correctly": True,
    },
    "artifacts": [_HUMAN_ARTIFACT],
    "notes": "O participante distinguiu prévia, salvar, submeter, aprovar, publicar e recuperar sessão sem ajuda ou confusão observada.",
}

UAT_01_RECORD = {
    "schema_version": 1,
    "sprint": "V12",
    "record_id": "V12-UAT_01-ATTEMPT_01",
    "case_id": "UAT-01",
    "evidence_class": "human_uat",
    "status": "PASS",
    "source_commit": _HUMAN_SOURCE_COMMIT,
    "observed_at": "2026-09-15T18:25:07-03:00",
    "environment": {},
    "human": {
        "participant_alias": "P-UAT-01",
        "participant_authorized": True,
        "participant_role": "nontechnical_user",
    },
    "facts": {
        "participant_authorized": True,
        "observed_seconds": 360,
        "help_events": [],
        "journey_completed": True,
        "shared_change_absent": True,
        "oracle_met": True,
        "journey_mode": "textual_v01",
    },
    "artifacts": [_HUMAN_ARTIFACT],
    "notes": "PASS da rota textual herdada da V01: escolher, ajustar, aplicar/comparar, desfazer e salvar foram explicados sem ajuda; não prova browser/runtime do Visual Lab.",
}

A11_01_RECORD = {
    "schema_version": 1,
    "sprint": "V12",
    "record_id": "V12-A11_01-ATTEMPT_01",
    "case_id": "A11-01",
    "evidence_class": "human_uat",
    "status": "FAIL",
    "source_commit": _HUMAN_SOURCE_COMMIT,
    "observed_at": "2026-09-15T18:15:53-03:00",
    "environment": {},
    "human": {
        "participant_alias": "P-MAINT-01",
        "participant_authorized": True,
        "participant_role": "maintainer",
    },
    "facts": {
        "participant_authorized": True,
        "render_observed": True,
        "contrast_measurements": [
            {"label": "conditional_red_light_widget", "ratio": 6.837793163467097, "required_ratio": 4.5},
            {"label": "conditional_red_dark_widget", "ratio": 2.3624715346329377, "required_ratio": 4.5},
            {"label": "conditional_yellow_light_widget", "ratio": 1.264684095079348, "required_ratio": 4.5},
            {"label": "conditional_yellow_dark_widget", "ratio": 12.773222792356847, "required_ratio": 4.5},
        ],
        "keyboard_review": True,
        "zoom_review": True,
        "oracle_met": False,
        "authorization_ref": "AUTH-V12-A11-01-20260915-PR54",
        "rollback_verified": True,
        "perceptual_irregularities_reported": False,
        "issue_ref": 57,
    },
    "artifacts": [
        {"kind": "post_import_theme", "sha256": "1c136fa9218c49754caa849883a13cefb51a913ad5df7d47e773a5ea65085802", "path": "evidence://v12-a11-01/post-import-theme"},
        {"kind": "light_mode_screenshot", "sha256": "108cd1e5f2f9863aa9f190bcef2eca24a451a73e961d22e2104c2f7c016590e8", "path": "evidence://v12-a11-01/light-100"},
        {"kind": "dark_mode_screenshot", "sha256": "717bb77127af33581303b7a1eeca715115087f9b9236084138dfd5975af2929a", "path": "evidence://v12-a11-01/dark-100"},
        {"kind": "final_restored_theme", "sha256": "71c8038d5b68b35ff888ea6bb7406dcfc74d5d1798b0af71626e592a2a50091b", "path": "evidence://v12-a11-01/final-theme"},
        {"kind": "final_restored_dashboard", "sha256": "0ba3a8399728de7776c0c80ce505123e2553c44d864d47bd49283d8b0c000308", "path": "evidence://v12-a11-01/final-dashboard"},
    ],
    "notes": "FAIL real preservado. O participante não percebeu irregularidade, mas pares de formatação condicional explícita do dashboard falharam objetivamente em Light/Dark. Issue #57. V11 não foi ampliada para cellFormat.",
}


def _code(record: dict) -> str:
    with unittest.TestCase().assertRaises(v12.V12EvidenceError) as cm:
        v12.validate_evidence(record, v12.load_matrix())
    return cm.exception.code


class RealAibiEvidenceTests(unittest.TestCase):
    def test_real_records_remain_fail_closed_and_synthetic_pass_validates(self):
        matrix = v12.load_matrix()
        first = json.loads(ATTEMPT_1.read_text(encoding="utf-8"))
        second = json.loads(ATTEMPT_2.read_text(encoding="utf-8"))

        self.assertEqual(first["status"], "FAIL")
        self.assertFalse(first["facts"]["synthetic_data_only"])
        v12.validate_evidence(first, matrix)

        self.assertEqual(second["status"], "PASS")
        self.assertTrue(second["facts"]["synthetic_data_only"])
        self.assertFalse(second["facts"]["published"])
        v12.validate_evidence(second, matrix)

        for path in SYNTHETIC_SQL:
            sql = path.read_text(encoding="utf-8")
            upper = sql.upper()
            self.assertIn("FROM VALUES", upper)
            self.assertNotIn("SAMPLES.NYCTAXI", upper)
            for forbidden in ("CREATE TABLE", "CREATE SCHEMA", "CREATE VOLUME", "INSERT INTO", "MERGE INTO"):
                self.assertNotIn(forbidden, upper)

    def test_sec_01_identity_and_effective_permission_are_sanitized_and_valid(self):
        matrix = v12.load_matrix()
        raw = SEC_01.read_text(encoding="utf-8")
        record = json.loads(raw)

        self.assertEqual(record["status"], "PASS")
        self.assertEqual(record["case_id"], "SEC-01")
        self.assertTrue(record["facts"]["identity_checked"])
        self.assertTrue(record["facts"]["permission_checked"])
        self.assertTrue(record["facts"]["synthetic_data_only"])
        self.assertFalse(record["facts"]["self_declared_role_used"])
        self.assertFalse(record["facts"]["identity_bytes_versioned"])
        self.assertEqual(record["human"], {})
        self.assertIsNone(_EMAIL_RE.search(raw))
        self.assertNotIn("workspace_id", raw.lower())
        self.assertNotIn("opensharing", raw.lower())
        v12.validate_evidence(record, matrix)

    def test_real_human_records_preserve_passes_and_a11_fail(self):
        matrix = v12.load_matrix()
        for record in (DOC_02_RECORD, DOC_03_RECORD, UAT_01_RECORD, A11_01_RECORD):
            v12.validate_evidence(record, matrix)
            raw = json.dumps(record, ensure_ascii=False, sort_keys=True)
            self.assertIsNone(_EMAIL_RE.search(raw))
            self.assertNotIn("workspace_id", raw.lower())
            self.assertNotIn("opensharing", raw.lower())

        self.assertEqual(DOC_02_RECORD["status"], "PASS")
        self.assertEqual(DOC_02_RECORD["facts"]["observed_seconds"], 25)
        self.assertEqual(DOC_02_RECORD["facts"]["help_events"], [])
        self.assertTrue(DOC_02_RECORD["facts"]["next_action_identified_without_help"])

        self.assertEqual(DOC_03_RECORD["status"], "PASS")
        self.assertTrue(DOC_03_RECORD["facts"]["scope_persistence_explained_correctly"])
        self.assertEqual(DOC_03_RECORD["facts"]["help_events"], [])

        self.assertEqual(UAT_01_RECORD["status"], "PASS")
        self.assertEqual(UAT_01_RECORD["facts"]["observed_seconds"], 360)
        self.assertEqual(UAT_01_RECORD["facts"]["help_events"], [])
        self.assertEqual(UAT_01_RECORD["facts"]["journey_mode"], "textual_v01")
        self.assertTrue(UAT_01_RECORD["facts"]["shared_change_absent"])

        self.assertEqual(A11_01_RECORD["status"], "FAIL")
        self.assertFalse(A11_01_RECORD["facts"]["oracle_met"])
        failing = [m for m in A11_01_RECORD["facts"]["contrast_measurements"] if m["ratio"] < m["required_ratio"]]
        self.assertEqual({m["label"] for m in failing}, {"conditional_red_dark_widget", "conditional_yellow_light_widget"})
        self.assertEqual(A11_01_RECORD["facts"]["issue_ref"], 57)


class HardeningContractTests(unittest.TestCase):
    def setUp(self):
        self.matrix = v12.load_matrix()
        self.cases = {item["id"]: item for item in self.matrix["cases"]}

    def test_sec01_specialization_is_explicit_and_v01_remains_historical(self):
        case = self.cases["SEC-01"]
        spec = case["v01_specialization"]
        self.assertEqual(case["evidence_class"], "databricks_environment")
        self.assertEqual(case["evidence_class"], spec["v12_evidence_class"])
        self.assertIs(spec["v01_human_required"], True)
        self.assertIs(spec["alters_v01"], False)
        self.assertTrue(spec["rationale"].strip())

        v01 = json.loads(V01_MATRIX.read_text(encoding="utf-8"))
        old = next(item for item in v01["cases"] if item["id"] == "SEC-01")
        self.assertIs(old["human_required"], True)
        self.assertEqual(old["human_status"], "PENDENTE")
        for case_id in ("DOC-02", "DOC-03", "A11-01", "UAT-01"):
            self.assertEqual(self.cases[case_id]["evidence_class"], "human_uat")
            self.assertNotIn("v01_specialization", self.cases[case_id])

    def test_sec01_sanitization_facts_are_canonical_and_enforced(self):
        required = self.cases["SEC-01"]["required_facts"]
        self.assertIn("self_declared_role_used", required)
        self.assertIn("identity_bytes_versioned", required)
        base = json.loads(SEC_01.read_text(encoding="utf-8"))

        role = copy.deepcopy(base)
        role["facts"]["self_declared_role_used"] = True
        self.assertEqual(_code(role), "V12_FACT_VALUE")

        identity = copy.deepcopy(base)
        identity["facts"]["identity_bytes_versioned"] = True
        self.assertEqual(_code(identity), "V12_FACT_VALUE")

        missing = copy.deepcopy(base)
        del missing["facts"]["self_declared_role_used"]
        self.assertEqual(_code(missing), "V12_FACT_MISSING")

    def test_aibi_pass_requires_integral_rollback_but_preserved_fail_does_not(self):
        self.assertEqual(
            self.cases["V12-AIBI-01"]["required_facts_on_pass"],
            ["rollback_original_semantic_sha256", "rollback_final_semantic_sha256"],
        )
        good = json.loads(ATTEMPT_2.read_text(encoding="utf-8"))
        v12.validate_evidence(good, self.matrix)

        drift = copy.deepcopy(good)
        drift["facts"]["rollback_final_semantic_sha256"] = "e" * 64
        self.assertEqual(_code(drift), "V12_ROLLBACK_DRIFT")

        missing = copy.deepcopy(good)
        del missing["facts"]["rollback_final_semantic_sha256"]
        self.assertEqual(_code(missing), "V12_FACT_MISSING")

        malformed = copy.deepcopy(good)
        malformed["facts"]["rollback_original_semantic_sha256"] = "nao-e-sha256"
        self.assertEqual(_code(malformed), "V12_HASH")

        preserved_fail = json.loads(ATTEMPT_1.read_text(encoding="utf-8"))
        self.assertNotIn("rollback_original_semantic_sha256", preserved_fail["facts"])
        v12.validate_evidence(preserved_fail, self.matrix)

    def test_matrix_hash_is_actually_frozen(self):
        self.assertEqual(hashlib.sha256(MATRIX.read_bytes()).hexdigest(), MATRIX_SHA256)


class HygieneGateTests(unittest.TestCase):
    def test_scanner_detects_forbidden_values_without_echoing_secret(self):
        cases = (
            ("DATABRICKS_" + "TOKEN=abc", "V12_HYGIENE_CREDENTIAL"),
            ("DATABRICKS_CLIENT_" + "SECRET=xyz", "V12_HYGIENE_CREDENTIAL"),
            ("https://adb-" + "1234567890123456.7.example/", "V12_HYGIENE_WORKSPACE_ID"),
            ("/Workspace/" + "Users/fulano/hub", "V12_HYGIENE_WORKSPACE_PATH"),
            ("/Vol" + "umes/catalogo/schema/volume", "V12_HYGIENE_VOLUME_PATH"),
        )
        for text, expected in cases:
            with self.subTest(expected=expected):
                findings = v12.scan_hygiene("README.md (linhas adicionadas)", text)
                self.assertTrue(findings)
                self.assertEqual(findings[0][0], expected)
                self.assertNotIn(text, " ".join(map(str, findings[0])))

    def test_added_line_that_looks_like_diff_header_is_not_dropped(self):
        credential = "DATABRICKS_" + "TOKEN"
        diff = (
            "diff --git a/README.md b/README.md\n"
            "--- a/README.md\n"
            "+++ b/README.md\n"
            "@@ -1,0 +2,1 @@\n"
            "+++ " + credential + "=abc\n"
        )
        added = v12.linhas_adicionadas(diff)
        self.assertEqual(added, {"README.md": "++ " + credential + "=abc"})
        self.assertEqual(v12.scan_hygiene("README.md", added["README.md"])[0][0], "V12_HYGIENE_CREDENTIAL")

    def test_removed_and_context_lines_are_not_treated_as_candidate_additions(self):
        credential = "DATABRICKS_" + "TOKEN"
        diff = (
            "--- a/README.md\n"
            "+++ b/README.md\n"
            "@@ -1,2 +1,1 @@\n"
            "-" + credential + "=antigo\n"
            " contexto com " + credential + "\n"
            "+linha limpa\n"
        )
        self.assertEqual(v12.linhas_adicionadas(diff), {"README.md": "linha limpa"})

    def test_workflow_delegates_hygiene_and_remains_read_only(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("from temas_v12_homologacao import linhas_adicionadas, scan_hygiene", text)
        self.assertIn("permissions:\n  contents: read", text)
        self.assertIn("persist-credentials: false", text)
        for path in (
            "README.md", "CHANGELOG.md", "docs/sprints/README.md",
            "docs/sprints/sistema_temas/README.md", "docs/sprints/sistema_temas/V12/",
            "tools/temas_v12_homologacao.py", "tools/tests/test_temas_v12_evidencia_real.py",
        ):
            self.assertIn(path, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
