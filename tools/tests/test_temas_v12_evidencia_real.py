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
