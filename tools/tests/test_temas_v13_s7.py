from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V13 = ROOT / "docs/sprints/sistema_temas/V13"
HANDOFF = V13 / "S7_HANDOFF_OPERACIONAL.md"
HUMAN = V13 / "S7_HOMOLOGACAO_HUMANA.md"
CHECKPOINT = V13 / "CHECKPOINT_S7.md"
README = V13 / "README.md"
WORKFLOW = ROOT / ".github/workflows/temas-v13-ci.yml"
MATRIX = V13 / "MATRIZ_OPERACIONAL.json"


class V13S7HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = HANDOFF.read_text(encoding="utf-8")
        cls.human = HUMAN.read_text(encoding="utf-8")
        cls.checkpoint = CHECKPOINT.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))

    def test_s7_artifacts_exist(self):
        self.assertTrue(HANDOFF.is_file())
        self.assertTrue(HUMAN.is_file())
        self.assertTrue(CHECKPOINT.is_file())
        self.assertTrue(MATRIX.is_file())

    def test_baseline_is_integrated_s6_merge(self):
        sha = "6dfb8707835921f2f48020f383cf571902080109"
        self.assertIn(sha, self.handoff)
        self.assertIn("15/15 workflows de `push` com `success`", self.handoff)

    def test_human_gate_has_real_versioned_pass(self):
        for text in (self.handoff, self.human, self.checkpoint, self.readme):
            self.assertIn("HUMAN-01 = PASS", text)
        self.assertIn("HUMAN_EVIDENCE_RECORDED", self.handoff)
        self.assertIn("HUMAN_EVIDENCE_RECORDED", self.human)
        self.assertIn("HUMAN-01 = BLOCKED", self.human)
        self.assertIn("HUMAN_EVIDENCE_MISSING", self.human)

    def test_human_gate_cannot_be_forged_by_ci(self):
        for text in (self.handoff, self.human):
            self.assertIn("CI", text)
        self.assertIn("Git/CI não podem fabricar nem alterar por conta própria", self.human)
        self.assertIn("não por CI autônoma", self.handoff)

    def test_start_here_routes_to_existing_owners(self):
        expected = {
            "MATRIZ_OPERACIONAL.json",
            "S2_PREFLIGHT_OPERACIONAL.md",
            "S3_RELEASE_OPERACIONAL.md",
            "S4_OBSERVABILIDADE_DIAGNOSTICO.md",
            "S5_COMPATIBILIDADE_ACESSIBILIDADE.md",
            "S6_ENSAIOS_OPERACIONAIS.md",
        }
        for name in expected:
            self.assertIn(name, self.handoff)
            self.assertTrue((V13 / name).exists(), name)

    def test_status_vocabulary_is_preserved(self):
        for status in ("PASS", "BLOCKED", "FAIL", "NOT_APPLICABLE"):
            self.assertIn(f"`{status}`", self.handoff)
        self.assertIn("FAIL > BLOCKED > PASS > NOT_APPLICABLE", self.handoff)

    def test_first_operation_uses_real_canonical_notebook_route(self):
        surfaces = {item["surface_id"]: item for item in self.matrix["surfaces"]}
        notebook = surfaces["notebook_visual_core"]
        action_ids = {item["action_id"] for item in notebook["actions"]}
        self.assertIn("render_with_resolved_theme", action_ids)
        self.assertIn('"surface_id": "notebook_visual_core"', self.handoff)
        self.assertIn('"action_id": "render_with_resolved_theme"', self.handoff)
        self.assertIn(
            "hub_padroes/identidade_visual/exemplos/legado_notebook.json",
            self.handoff,
        )

    def test_first_operation_executes_real_preflight_cli(self):
        self.assertIn(
            "python -B tools/temas_v13_preflight.py --request .artifacts/s7-notebook-preflight.json",
            self.handoff,
        )
        self.assertIn("overall_status = PASS", self.handoff)
        self.assertIn("THEME_VALID", self.handoff)

    def test_blocked_training_route_matches_matrix(self):
        surfaces = {item["surface_id"]: item for item in self.matrix["surfaces"]}
        workspace = surfaces["workspace_theme"]
        action_ids = {item["action_id"] for item in workspace["actions"]}
        self.assertIn("apply_workspace_theme", action_ids)
        self.assertIn('"surface_id": "workspace_theme"', self.handoff)
        self.assertIn('"action_id": "apply_workspace_theme"', self.handoff)
        self.assertIn("AUTHORIZATION_CANONICALLY_BLOCKED", self.handoff)
        self.assertIn("exit code 2", self.handoff)

    def test_training_never_authorizes_remote_environment(self):
        self.assertIn("**não** requer Databricks real", self.handoff)
        self.assertIn("nenhuma mutação remota", self.handoff)
        self.assertIn("não execute nenhuma operação remota", self.human.lower())

    def test_decision_matrix_covers_core_failure_routes(self):
        for marker in (
            "SHA/inventário/manifesto divergente",
            "preflight local `BLOCKED` por autorização",
            "identidade/permissão real não comprovada",
            "rollback não preparado",
            "staging local falhou",
            "contraste A11 histórico reaparece",
            "workspace theme solicitado",
        ):
            self.assertIn(marker, self.handoff)

    def test_decision_matrix_forbids_silent_bypass(self):
        for marker in (
            "não edite hash manualmente",
            "não invente `authorization_ref` como prova",
            "não use CI como prova de identidade viva",
            "não transforme `cellFormat` em token nem amplie V11",
            "não confunda Import theme com Publish",
        ):
            self.assertIn(marker, self.handoff)

    def test_rehearsal_registry_references_historical_evidence(self):
        for name in (
            "CHECKPOINT_S2.md",
            "CHECKPOINT_S3.md",
            "CHECKPOINT_S4.md",
            "CHECKPOINT_S5.md",
            "CHECKPOINT_S6.md",
        ):
            self.assertIn(name, self.handoff)
            self.assertTrue((V13 / name).exists(), name)

    def test_inherited_v12_nonpass_states_are_preserved(self):
        for marker in (
            "A11-01 = FAIL",
            "issue #57 aberta",
            "V12-LAB-01 = BLOQUEADO_AUTORIZACAO",
            "V12-APP-01 = BLOQUEADO_AUTORIZACAO",
            "V12-AIBI-02 = BLOQUEADO_AUTORIZACAO",
        ):
            self.assertIn(marker, self.handoff)

    def test_v12_pass_scope_is_not_generalized(self):
        self.assertIn("V12-AIBI-01 = PASS` somente no alcance V12", self.handoff)
        self.assertIn("SEC-01 = PASS` somente no alcance observado", self.handoff)
        self.assertIn("UAT-01 = PASS` somente textual", self.handoff)

    def test_v14_scope_is_reserved_not_implemented(self):
        self.assertIn("V14_NOT_STARTED = true", self.handoff)
        self.assertIn("production readiness final", self.handoff)
        self.assertIn("SLA/SLO sem base real", self.handoff)
        self.assertIn("decisão final de go-live", self.handoff)
        self.assertNotIn("V14_STARTED = true", self.handoff)

    def test_release_rollback_is_non_destructive(self):
        self.assertIn("Last Known Good pré-fechamento", self.handoff)
        self.assertIn("6dfb8707835921f2f48020f383cf571902080109", self.handoff)
        self.assertIn("não use force-push/reset da `main`", self.handoff)
        self.assertIn("reversão normal do merge em branch/PR própria", self.handoff)

    def test_human_protocol_requires_non_builder_and_no_verbal_instruction(self):
        self.assertIn("não ter construído o procedimento", self.human)
        self.assertIn("não receber instrução verbal do autor", self.human)
        self.assertIn("sem complemento verbal", self.human)

    def test_human_protocol_has_all_six_oracles(self):
        for marker in (
            "H1 — navegação",
            "H2 — cenário notebook",
            "H3 — cenário workspace theme",
            "H4 — diagnóstico",
            "H5 — rollback",
            "H6 — segurança/privacidade",
        ):
            self.assertIn(marker, self.human)

    def test_human_protocol_records_duration_help_and_interpretation_errors(self):
        for marker in (
            "duração observada",
            "ajuda verbal do autor",
            "ajuda documental extra",
            "erros de interpretação",
        ):
            self.assertIn(marker, self.human)

    def test_human_protocol_records_completed_evidence(self):
        for marker in (
            "`participant_id` | `Tester`",
            "duração observada | `5 minutos`",
            "ajuda verbal do autor | `0`",
            "ajuda documental extra | `0`",
            "erros de interpretação | `0`",
            "H1 navegação | `PASS`",
            "H2 notebook | `PASS`",
            "H3 workspace BLOCKED | `PASS`",
            "H4 diagnóstico | `PASS`",
            "H5 rollback | `PASS`",
            "H6 segurança/privacidade | `PASS`",
            "resultado humano | `PASS`",
        ):
            self.assertIn(marker, self.human)
        self.assertNotIn("<sanitizado>", self.human)
        self.assertNotIn("<minutos>", self.human)
        self.assertIn("Tester", self.checkpoint)
        self.assertIn("5 minutos", self.checkpoint)

    def test_human_protocol_forbids_statistical_inference_and_sla(self):
        self.assertIn("sem inferência estatística", self.human)
        self.assertIn("Não definir SLA, SLO", self.human)

    def test_no_new_s7_engine_is_created(self):
        self.assertFalse((ROOT / "tools/temas_v13_handoff.py").exists())
        self.assertFalse((ROOT / "tools/temas_v13_s7.py").exists())

    def test_live_readme_moves_to_s7_after_integrated_s6(self):
        self.assertIn("S6 — PR #65", self.readme)
        self.assertIn("6dfb8707835921f2f48020f383cf571902080109", self.readme)
        self.assertIn("S7 — handoff operacional e fechamento", self.readme)
        self.assertIn("HUMAN-01 = PASS", self.readme)
        self.assertIn("V14 não foi iniciada", self.readme)

    def test_workflow_runs_s7_contract_before_regressions(self):
        step = "V13 S7 — handoff operacional e gate humano"
        command = "python -B tools/tests/test_temas_v13_s7.py -v"
        regressions = "Regressões de temas V01–V13"
        self.assertIn(step, self.workflow)
        self.assertIn(command, self.workflow)
        self.assertLess(self.workflow.index(step), self.workflow.index(regressions))

    def test_workflow_remains_read_only_without_databricks_credentials(self):
        self.assertIn("permissions:\n  contents: read", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)
        for forbidden in ("DATABRICKS_TOKEN", "DATABRICKS_HOST", "secrets."):
            self.assertNotIn(forbidden, self.workflow)

    def test_workflow_s7_frontier_is_explicit_and_human_is_versioned_pass(self):
        for marker in (
            "V13_S7_NETWORK=0",
            "V13_S7_REMOTE_MUTATION=0",
            "V13_S7_DATABRICKS_MUTATION=0",
            "V13_S7_HUMAN_VALIDATION=PASS",
            "V13_S7_HUMAN_EVIDENCE=VERSIONED_HUMAN_SESSION",
            "V13_V14_NOT_STARTED=1",
        ):
            self.assertIn(marker, self.workflow)
        self.assertNotIn('echo "V13_S7_HUMAN_VALIDATION=BLOCKED"', self.workflow)

    def test_s6_not_started_marker_becomes_historical_only(self):
        self.assertNotIn('echo "V13_S7_NOT_STARTED=1"', self.workflow)
        self.assertIn("Historical S6 checkpoint assertion: V13_S7_NOT_STARTED=1", self.workflow)


if __name__ == "__main__":
    unittest.main()
