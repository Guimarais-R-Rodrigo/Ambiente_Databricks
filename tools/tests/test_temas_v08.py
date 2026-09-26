"""V08 — integração transversal de temas com skills, padrões e Manual."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "ambiente_fonte/.assistant"
MIRROR = ROOT / "Novo_Ambiente_Simulado/Users/usuario-free/.assistant"
REGISTRY = ROOT / "docs/sprints/sistema_temas/V08/MATRIZ_INTEGRACAO.json"
ROOT_MANUAL = ROOT / "MANUAL_TECNICO.md"
HEX = re.compile(r"#[0-9A-Fa-f]{6}")

UPDATED_RELATIVE = [
    "README.md",
    "skills/README.md",
    "skills/hub-ml-concierge/SKILL.md",
    "skills/hub-ml-criar-objeto/SKILL.md",
    "skills/hub-ml-eda-profissional/SKILL.md",
    "skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md",
    "skills/hub-ml-baseline-ml/SKILL.md",
    "skills/hub-ml-analise-safra/SKILL.md",
    "skills/hub-ml-monitoramento-modelo/SKILL.md",
    "skills/hub-ml-explainability/SKILL.md",
    "hub_padroes/README.md",
    "hub_padroes/identidade_visual/README.md",
    "hub_padroes/identidade_visual/GUIA_OPERACIONAL.md",
    "MANUAL_TECNICO.md",
]


def text(relative: str) -> str:
    return (SOURCE / relative).read_text(encoding="utf-8")


class MatrixTests(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.rows = {row["id"]: row for row in self.matrix["surfaces"]}

    def test_matrix_has_expected_transversal_surfaces(self):
        expected = {
            "assistant.entrypoint", "skills.catalog", "skill.concierge",
            "skill.criar_objeto", "skill.eda", "skill.eda.visual_template",
            "skill.baseline", "skill.safra", "skill.monitoramento",
            "skill.explainability", "skill.comentar_notebook", "patterns.index",
            "patterns.identity", "patterns.identity.first_use", "manual.canonical",
            "manual.root_copy", "manual.simulated_copy", "runtime.visual_objects",
        }
        self.assertEqual(set(self.rows), expected)

    def test_each_row_has_reason_and_effect(self):
        for row in self.rows.values():
            self.assertTrue(row["reason"], row["id"])
            self.assertTrue(row["expected_effect"], row["id"])

    def test_no_edit_decision_for_commenting_skill_is_preserved(self):
        row = self.rows["skill.comentar_notebook"]
        self.assertEqual(row["classification"], "already_aligned_no_edit")


class MirrorTests(unittest.TestCase):
    def test_updated_assistant_surfaces_match_simulated_bytes(self):
        for relative in UPDATED_RELATIVE:
            source = SOURCE / relative
            mirror = MIRROR / relative
            self.assertTrue(source.is_file(), relative)
            self.assertTrue(mirror.is_file(), relative)
            self.assertEqual(source.read_bytes(), mirror.read_bytes(), relative)

    def test_all_manual_copies_are_identical(self):
        canonical = (SOURCE / "MANUAL_TECNICO.md").read_bytes()
        self.assertEqual(ROOT_MANUAL.read_bytes(), canonical)
        self.assertEqual((MIRROR / "MANUAL_TECNICO.md").read_bytes(), canonical)


class CurrentStateTests(unittest.TestCase):
    def test_assistant_entrypoint_no_longer_calls_v05_candidate(self):
        content = text("README.md")
        self.assertNotIn("Visual Lab do Sistema de Temas — V05 candidata", content)
        self.assertNotIn("A V05 ainda não possui aceite nem merge", content)
        self.assertIn("V07", content)

    def test_identity_pattern_is_current_through_v07(self):
        content = text("hub_padroes/identidade_visual/README.md")
        self.assertNotIn("CONSUMO OPT-IN ATÉ V04", content)
        self.assertIn("V07", content)
        self.assertIn("ResolvedTheme", content)

    def test_first_use_does_not_stop_at_v04(self):
        content = text("hub_padroes/identidade_visual/GUIA_OPERACIONAL.md")
        self.assertNotIn("operações permanecem fora de V00–V04", content)
        self.assertIn("Visual Lab", content)
        self.assertIn("V07", content)
        self.assertIn("_resolvido", content)

    def test_manual_live_heading_and_state_are_current(self):
        content = text("MANUAL_TECNICO.md")
        self.assertNotIn("## Sistema de Temas — V04 integrada no Git; V05 candidata em fechamento", content)
        self.assertIn("## Sistema de Temas — V00–V07 integradas no Git", content)
        self.assertIn("V08", content)


class EdaVisualTemplateTests(unittest.TestCase):
    def setUp(self):
        self.content = text("skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md")

    def test_template_is_not_a_second_theme_source(self):
        self.assertIn("ResolvedTheme", self.content)
        self.assertIn("load_reference_theme", self.content)
        self.assertIn("aplicar_tema_resolvido", self.content)
        self.assertNotIn("PALETA_EDA", self.content)
        self.assertNotIn("TEMA_EDA", self.content)
        self.assertNotIn("centraliza todas as decisões estéticas", self.content)

    def test_template_has_no_hex_palette_policy(self):
        self.assertIsNone(HEX.search(self.content))

    def test_template_does_not_recommend_legacy_global_registration(self):
        self.assertNotIn("`registrar_template_plotly()`", self.content)
        self.assertIn("não registre template global", self.content.lower())


class SkillRoutingTests(unittest.TestCase):
    def test_concierge_has_visual_route_and_no_publication_claim(self):
        content = text("skills/hub-ml-concierge/SKILL.md")
        self.assertIn("identidade_visual", content)
        self.assertIn("Visual Lab", content)
        self.assertIn("SHAP", content)
        self.assertIn("Kaplan", content)
        self.assertIn("não", content.lower())

    def test_create_object_uses_resolved_theme_as_configurable_source(self):
        content = text("skills/hub-ml-criar-objeto/SKILL.md")
        self.assertIn("ResolvedTheme", content)
        self.assertIn("hub_padroes/identidade_visual", content)
        self.assertNotIn("| Paleta e cores semânticas | `hub_snippets.constants.colors` |", content)
        self.assertIn("constants.colors", content)
        self.assertIn("legado", content.lower())

    def test_eda_skill_routes_to_resolved_consumers(self):
        content = text("skills/hub-ml-eda-profissional/SKILL.md")
        self.assertIn("plot_correlation_resolvido", content)
        self.assertIn("plot_distributions_resolvido", content)
        self.assertIn("ResolvedTheme", content)

    def test_baseline_keeps_metrics_separate_from_visual_theme(self):
        content = text("skills/hub-ml-baseline-ml/SKILL.md")
        self.assertIn("plot_roc_curve_resolvido", content)
        self.assertIn("métricas", content.lower())
        self.assertIn("aparência", content.lower())

    def test_vintage_routes_to_resolved_plots_without_changing_rates(self):
        content = text("skills/hub-ml-analise-safra/SKILL.md")
        self.assertIn("plot_vintage_curves_resolvido", content)
        self.assertIn("plot_vintage_heatmap_resolvido", content)
        self.assertIn("denominador", content.lower())

    def test_monitoring_theme_does_not_change_policy(self):
        content = text("skills/hub-ml-monitoramento-modelo/SKILL.md")
        self.assertIn("plot_timeline_resolvido", content)
        self.assertIn("threshold", content.lower())
        self.assertIn("aparência", content.lower())

    def test_explainability_marks_shap_exception_and_resolved_curves(self):
        content = text("skills/hub-ml-explainability/SKILL.md")
        self.assertIn("plot_roc_curve_resolvido", content)
        self.assertIn("SHAP/Matplotlib", content)
        self.assertIn("não", content.lower())


class PatternsAndWorkflowTests(unittest.TestCase):
    def test_patterns_index_reaches_v07(self):
        content = text("hub_padroes/README.md")
        self.assertIn("V07", content)
        self.assertIn("Visual Lab", content)
        self.assertIn("ResolvedTheme", content)

    def test_skills_catalog_names_canonical_visual_owner(self):
        content = text("skills/README.md")
        self.assertIn("hub_padroes/identidade_visual", content)
        self.assertIn("ResolvedTheme", content)
        self.assertIn("estilo_visual_eda.md", content)

    def test_v08_workflow_is_read_only(self):
        content = (ROOT / ".github/workflows/temas-v08-ci.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", content)
        self.assertIn("persist-credentials: false", content)
        self.assertNotIn("contents: write", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
