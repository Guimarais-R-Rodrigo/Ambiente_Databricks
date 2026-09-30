from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import micromodelo_mm01_contract as mm01
import micromodelo_mm02_fingerprint as mm02
import micromodelo_mm06_artifacts as mm06


SCHEMA = REPO / "docs/sprints/micromodelos/MM01/micromodelo.schema.json"
TEMPLATE = REPO / "docs/sprints/micromodelos/MM01/micromodelo.template.yaml"
VALID = REPO / "tools/tests/fixtures/micromodelos_mm01/valido_validado.json"


class MM06ArtifactsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = mm01.load_schema(SCHEMA)
        cls.idea = mm01.load_document(TEMPLATE)
        cls.validated = json.loads(VALID.read_text(encoding="utf-8"))

    def test_idea_generates_all_study_sections_without_claiming_results(self) -> None:
        artifacts = mm06.render_artifacts(self.idea, self.schema)
        notebook = artifacts.notebook_source
        self.assertTrue(notebook.startswith("# Databricks notebook source\n"))
        compile(notebook, "generated_micromodel_study.py", "exec")
        self.assertIn("ARTIFACT_KIND = 'STUDY_SCAFFOLD'", notebook)
        self.assertIn("Scaffold de domínio NOT_RUN", artifacts.readme_markdown)
        for number in range(18):
            self.assertIn(f"# MAGIC ## {number}.", notebook)
        self.assertIn("GENERATION_EXECUTION_STATUS = 'NOT_RUN'", notebook)
        self.assertIn("nenhuma contagem, percentual ou estatística foi medida", notebook)
        self.assertIn("PENDENTE: nenhuma fonte selecionada", notebook)
        self.assertNotIn("mlflow.start_run", notebook)
        self.assertNotIn("spark.sql", notebook)

    def test_fingerprint_matches_mm02_and_is_stable(self) -> None:
        artifacts = mm06.render_artifacts(self.validated, self.schema)
        expected = mm02.calculate_spec_fingerprint(self.validated, self.schema)
        self.assertEqual(expected.sha256, artifacts.spec_fingerprint)
        self.assertEqual(expected.algorithm, artifacts.fingerprint_algorithm)
        self.assertIn(expected.sha256, artifacts.notebook_source)
        self.assertIn(expected.sha256, artifacts.readme_markdown)
        self.assertEqual(artifacts, mm06.render_artifacts(self.validated, self.schema))

    def test_material_change_changes_both_artifacts(self) -> None:
        changed = copy.deepcopy(self.idea)
        changed["entidade"]["populacao_elegivel"] = "Somente clientes sintéticos com evento no período."
        first = mm06.render_artifacts(self.idea, self.schema)
        second = mm06.render_artifacts(changed, self.schema)
        self.assertNotEqual(first.spec_fingerprint, second.spec_fingerprint)
        self.assertNotEqual(first.notebook_source, second.notebook_source)
        self.assertNotEqual(first.readme_markdown, second.readme_markdown)

    def test_invalid_spec_is_refused_before_artifact_creation(self) -> None:
        invalid = copy.deepcopy(self.idea)
        invalid["classificacao"]["ausencia_evidencia"]["resultado_sem_evidencia"] = "FALSE"
        with self.assertRaises(mm02.InvalidSpecificationError):
            mm06.render_artifacts(invalid, self.schema)

    def test_spec_text_cannot_create_notebook_cell_or_active_html(self) -> None:
        injection = copy.deepcopy(self.idea)
        injection["negocio"]["objetivo"] = (
            "Objetivo sintético\n# COMMAND ----------\nimport os\n<script>alert(1)</script>"
        )
        artifacts = mm06.render_artifacts(injection, self.schema)
        self.assertEqual(18, artifacts.notebook_source.splitlines().count("# COMMAND ----------"))
        self.assertNotIn("\nimport os\n", artifacts.notebook_source)
        self.assertNotIn("<script>", artifacts.notebook_source)
        self.assertNotIn("<script>", artifacts.readme_markdown)

    def test_run_policy_separates_approval_and_individual_results(self) -> None:
        artifacts = mm06.render_artifacts(self.validated, self.schema)
        for run_type in mm06.RUN_TYPES:
            self.assertIn(run_type, artifacts.notebook_source)
            self.assertIn(run_type, artifacts.readme_markdown)
        self.assertIn("aprovação humana permanece separada", artifacts.notebook_source)
        self.assertIn("nunca resultados individuais em artifacts MLflow", artifacts.notebook_source)
        self.assertIn("run_micromodelo", artifacts.notebook_source)
        self.assertIn("não publica nem concede acesso", artifacts.readme_markdown)

    def test_blocked_condition_and_reason_are_visible_in_both_artifacts(self) -> None:
        blocked = copy.deepcopy(self.idea)
        blocked["identidade"]["estado"].update(
            {"condicao": "BLOQUEADO", "motivo_condicao": "Cobertura sintética insuficiente"}
        )
        self.assertEqual([], mm01.validate_spec(blocked, self.schema))
        artifacts = mm06.render_artifacts(blocked, self.schema)
        for content in (artifacts.notebook_source, artifacts.readme_markdown):
            self.assertIn("BLOQUEADO", content)
            self.assertIn("Cobertura sintética insuficiente", content)

    def test_existing_rules_criteria_and_measured_result_are_attributed(self) -> None:
        artifacts = mm06.render_artifacts(self.validated, self.schema)
        for content in (artifacts.notebook_source, artifacts.readme_markdown):
            self.assertIn("limiar_true", content)
            self.assertIn("GTE 70", content)
            self.assertIn("recorrencia", content)
            self.assertIn("peso 0.6", content)
            self.assertIn("casos positivos, negativos, indeterminados", content)
            self.assertIn("todos os casos sintéticos previstos foram reproduzidos", content)
            self.assertIn("run-validacao-001", content)
            self.assertIn("Este gerador não autentica a decisão", content)


if __name__ == "__main__":
    unittest.main()
