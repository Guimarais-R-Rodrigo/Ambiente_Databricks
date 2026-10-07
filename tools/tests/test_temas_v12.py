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
V01_MATRIX = ROOT / "docs" / "sprints" / "sistema_temas" / "V01" / "matriz_testes.json"
V11_TEST = ROOT / "tools" / "tests" / "test_temas_v11.py"
AIBI_FIXTURE = ROOT / "ambiente_databricks" / ".assistant" / "hub_padroes" / "identidade_visual" / "aibi" / "dashboard_sintetico.json"
WORKFLOW = ROOT / ".github" / "workflows" / "temas-v12-ci.yml"
SHA = "a" * 64
COMMIT = "b" * 40
# SHA-256 congelado da matriz V12. A versão anterior deste valor não existia:
# o teste lia o mesmo arquivo duas vezes e comparava consigo mesmo, o que não
# pode falhar e não protege rastreabilidade nenhuma. Congelado, alterar a
# matriz sem atualizar este valor na mesma mudança reprova o gate.
MATRIX_SHA256 = "493e45a23de2858de50524fe60bb907fd8e2b7cbaf0211ba3d95aa626944dfd3"


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


def sec01_base(**alteracoes):
    """Registro SEC-01 sintético: ambiente observacional, sem mutação."""
    facts = {
        "environment_authorized": True,
        "identity_checked": True,
        "permission_checked": True,
        "synthetic_data_only": True,
        "oracle_met": True,
        "self_declared_role_used": False,
        "identity_bytes_versioned": False,
    }
    facts.update(alteracoes)
    registro = env_base("SEC-01", facts)
    registro["environment"]["authorization_ref"] = ""
    return registro


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

    def test_sec01_specialization_is_ratified_in_v12_without_touching_v01(self):
        ratificacao = self.cases["SEC-01"]["v01_specialization"]
        self.assertIs(ratificacao["alters_v01"], False)
        self.assertIs(ratificacao["v01_human_required"], True)
        self.assertEqual(ratificacao["v12_evidence_class"], "databricks_environment")
        self.assertEqual(self.cases["SEC-01"]["evidence_class"], ratificacao["v12_evidence_class"])
        self.assertEqual(ratificacao["v01_case_source"], "docs/sprints/sistema_temas/V01/matriz_testes.json")
        self.assertTrue(ratificacao["rationale"].strip())
        # A V01 continua intacta: a especialização é declarada e justificada na
        # V12, nunca aplicada por edição retroativa do registro canônico.
        v01 = json.loads(V01_MATRIX.read_text(encoding="utf-8"))
        sec01_v01 = next(c for c in v01["cases"] if c["id"] == "SEC-01")
        self.assertIs(sec01_v01["human_required"], True)
        self.assertEqual(sec01_v01["human_status"], "PENDENTE")

    def test_specialization_does_not_leak_to_the_other_human_cases(self):
        for caso in ("DOC-02", "DOC-03", "A11-01", "UAT-01"):
            self.assertEqual(self.cases[caso]["evidence_class"], "human_uat")
            self.assertNotIn("v01_specialization", self.cases[caso])

    def test_sec01_hygiene_facts_are_canonical(self):
        exigidos = self.cases["SEC-01"]["required_facts"]
        self.assertIn("self_declared_role_used", exigidos)
        self.assertIn("identity_bytes_versioned", exigidos)

    def test_aibi01_requires_rollback_hashes_on_pass(self):
        self.assertEqual(
            self.cases["V12-AIBI-01"]["required_facts_on_pass"],
            ["rollback_original_semantic_sha256", "rollback_final_semantic_sha256"],
        )

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
            "rollback_original_semantic_sha256": "f" * 64,
            "rollback_final_semantic_sha256": "f" * 64,
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

    def test_aibi_rejects_divergent_rollback(self):
        record = self._aibi_record()
        record["facts"]["rollback_final_semantic_sha256"] = "e" * 64
        self.assertCode("V12_ROLLBACK_DRIFT", record)

    def test_aibi_rejects_pass_without_rollback_hashes(self):
        record = self._aibi_record()
        del record["facts"]["rollback_final_semantic_sha256"]
        self.assertCode("V12_FACT_MISSING", record)

    def test_aibi_rejects_malformed_rollback_hash(self):
        record = self._aibi_record()
        record["facts"]["rollback_original_semantic_sha256"] = "nao-e-sha256"
        self.assertCode("V12_HASH", record)

    def test_sec01_rejects_permission_sustained_by_self_declared_role(self):
        self.assertCode("V12_FACT_VALUE", sec01_base(self_declared_role_used=True))

    def test_sec01_rejects_versioned_identity_bytes(self):
        self.assertCode("V12_FACT_VALUE", sec01_base(identity_bytes_versioned=True))

    def test_sec01_rejects_record_missing_the_hygiene_facts(self):
        record = sec01_base()
        del record["facts"]["self_declared_role_used"]
        self.assertCode("V12_FACT_MISSING", record)

    def test_preserved_fail_record_survives_the_new_pass_only_facts(self):
        # Um FAIL real preservado não tem hash de rollback, e exigir isso de
        # todo registro obrigaria a fabricar evidência ou a reclassificar o
        # FAIL. Por isso os hashes são exigidos só do PASS.
        record = self._aibi_record()
        record["status"] = "FAIL"
        record["facts"]["oracle_met"] = False
        record["facts"]["synthetic_data_only"] = False
        del record["facts"]["rollback_original_semantic_sha256"]
        del record["facts"]["rollback_final_semantic_sha256"]
        record["artifacts"] = []
        v12.validate_evidence(record, self.matrix)

    def test_valid_sec01_environment_evidence_passes(self):
        v12.validate_evidence(sec01_base(), self.matrix)

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
        self.assertNotIn("git fetch --no-tags origin main", text)
        for needle in forbidden:
            self.assertNotIn(needle, text)

    def test_v12_tool_has_no_network_or_databricks_client(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        for needle in ("databricks.sdk", "requests.", "urllib.request", "subprocess.", "/api/2.0/"):
            self.assertNotIn(needle, text)

    def test_matrix_hash_is_frozen_for_traceability(self):
        medido = hashlib.sha256(MATRIX_PATH.read_bytes()).hexdigest()
        self.assertEqual(
            medido,
            MATRIX_SHA256,
            "A matriz V12 mudou sem atualizar MATRIX_SHA256 na mesma mudança. "
            "Confira o diff da matriz e, se a mudança for intencional, congele o novo valor.",
        )


class HigieneDeConteudoTests(unittest.TestCase):
    """A higiene precisa cobrir o que a candidata escreve — inclusive na
    documentação raiz permitida — e precisa provar que detectaria."""

    def test_forbidden_credential_added_to_permitted_root_doc_is_detected(self):
        credencial = "DATABRICKS_" + "TOKEN"
        adicionada = "Exporte " + credencial + "=abc antes de publicar."
        achados = v12.scan_hygiene("README.md (linhas adicionadas)", adicionada)
        self.assertEqual(len(achados), 1)
        self.assertEqual(achados[0][0], "V12_HYGIENE_CREDENTIAL")
        self.assertEqual(achados[0][1], "README.md (linhas adicionadas)")

    def test_workspace_identifier_and_paths_added_to_root_doc_are_detected(self):
        casos = (
            ("/Workspace/" + "Users/fulano/hub", "V12_HYGIENE_WORKSPACE_PATH"),
            ("/Vol" + "umes/catalogo/schema/volume", "V12_HYGIENE_VOLUME_PATH"),
            ("https://adb-" + "1234567890123456.7.exemplo/", "V12_HYGIENE_WORKSPACE_ID"),
            ("DATABRICKS_CLIENT_" + "SECRET" + "=xyz", "V12_HYGIENE_CREDENTIAL"),
        )
        for trecho, esperado in casos:
            with self.subTest(esperado=esperado):
                achados = v12.scan_hygiene("CHANGELOG.md (linhas adicionadas)", trecho)
                self.assertTrue(achados)
                self.assertEqual(achados[0][0], esperado)

    def test_hygiene_finding_never_echoes_the_matched_secret(self):
        credencial = "DATABRICKS_CLIENT_" + "SECRET"
        achados = v12.scan_hygiene("README.md", "valor " + credencial + "=xyz")
        self.assertEqual(len(achados), 1)
        for campo in achados[0]:
            self.assertNotIn(credencial, str(campo))

    def test_clean_root_doc_content_produces_no_finding(self):
        limpo = "A V12 usa somente dados sinteticos e nao versiona identidade."
        self.assertEqual(v12.scan_hygiene("README.md (linhas adicionadas)", limpo), [])

    def test_hygiene_does_not_match_the_files_that_implement_it(self):
        implementacao = (
            MODULE_PATH,
            Path(__file__).resolve(),
            WORKFLOW,
            ROOT / "tools" / "tests" / "test_temas_v12_evidencia_real.py",
        )
        for caminho in implementacao:
            with self.subTest(arquivo=caminho.name):
                texto = caminho.read_text(encoding="utf-8")
                self.assertEqual(v12.scan_hygiene(caminho.name, texto), [])

    def test_only_added_lines_are_extracted_from_a_diff(self):
        diff = (
            "diff --git a/README.md b/README.md\n"
            "--- a/README.md\n"
            "+++ b/README.md\n"
            "@@ -1,0 +2,2 @@\n"
            "+linha nova A\n"
            "+linha nova B\n"
            "diff --git a/CHANGELOG.md b/CHANGELOG.md\n"
            "--- a/CHANGELOG.md\n"
            "+++ b/CHANGELOG.md\n"
            "@@ -1,0 +2,1 @@\n"
            "+entrada nova\n"
        )
        self.assertEqual(
            v12.linhas_adicionadas(diff),
            {"README.md": "linha nova A\nlinha nova B", "CHANGELOG.md": "entrada nova"},
        )

    def test_added_line_that_looks_like_a_diff_header_is_not_dropped(self):
        # Conteúdo que começa com "++ " vira "+++ " no diff. Se o parser tratar
        # prefixo como cabeçalho, essa linha some da varredura e um segredo
        # escrito nela passa despercebido.
        credencial = "DATABRICKS_" + "TOKEN"
        diff = (
            "diff --git a/README.md b/README.md\n"
            "--- a/README.md\n"
            "+++ b/README.md\n"
            "@@ -1,0 +2,1 @@\n"
            "+++ " + credencial + "=abc\n"
        )
        adicionadas = v12.linhas_adicionadas(diff)
        self.assertEqual(adicionadas, {"README.md": "++ " + credencial + "=abc"})
        achados = v12.scan_hygiene("README.md", adicionadas["README.md"])
        self.assertEqual(len(achados), 1)
        self.assertEqual(achados[0][0], "V12_HYGIENE_CREDENTIAL")

    def test_historic_debt_outside_the_diff_is_not_swept(self):
        # Linha removida e linha de contexto não entram: a higiene julga o que
        # esta candidata escreveu, não o que já estava na main.
        credencial = "DATABRICKS_" + "TOKEN"
        diff = (
            "--- a/README.md\n"
            "+++ b/README.md\n"
            "@@ -1,2 +1,1 @@\n"
            "-" + credencial + "=antigo\n"
            " contexto com " + credencial + "\n"
            "+linha limpa\n"
        )
        adicionadas = v12.linhas_adicionadas(diff)
        self.assertEqual(adicionadas, {"README.md": "linha limpa"})
        self.assertEqual(v12.scan_hygiene("README.md", adicionadas["README.md"]), [])

    def test_workflow_delegates_hygiene_and_declares_every_permitted_path(self):
        texto = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("from temas_v12_homologacao import linhas_adicionadas, scan_hygiene", texto)
        permitidos = (
            "tools/temas_v12_homologacao.py",
            "tools/tests/test_temas_v12.py",
            "tools/tests/test_temas_v12_evidencia_real.py",
            ".github/workflows/temas-v12-ci.yml",
            "docs/sprints/sistema_temas/V12/",
            "docs/sprints/sistema_temas/README.md",
            "docs/sprints/README.md",
            "README.md",
            "CHANGELOG.md",
        )
        for caminho in permitidos:
            with self.subTest(caminho=caminho):
                self.assertIn(caminho, texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
