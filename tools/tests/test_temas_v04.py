"""V04 — componentes HTML e tabela pandas opt-in sobre ResolvedTheme.

Sem Databricks, rede ou dados reais. A referência legada precisa continuar
compatível; a rota nova só aceita resultado íntegro do núcleo V02.
"""
from __future__ import annotations

import inspect
import re
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "ambiente_fonte/.assistant"
sys.path.insert(0, str(PRODUCT))

import pandas as pd

from hub_snippets.constants.styles import (
    FONT_FAMILY,
    STYLE_BADGE_FAIL,
    STYLE_BADGE_INFO,
    STYLE_BADGE_OK,
    STYLE_BADGE_WARN,
    STYLE_DIVIDER_HEAVY,
    STYLE_DIVIDER_LIGHT,
    STYLE_DIVIDER_MEDIUM,
    STYLE_DIVIDER_SECTION_PRIMARY,
    STYLE_DIVIDER_SECTION_SECONDARY,
    STYLE_INDEX_CONTAINER,
    STYLE_INDEX_DESCRIPTION,
    STYLE_INDEX_HEADING,
    STYLE_INDEX_ITEM,
    STYLE_KPI_CARD,
    STYLE_SECTION_DESCRIPTION,
    STYLE_SECTION_HEADER,
    STYLE_SECTION_TITLE,
    get_styles_resolvidos,
)
from hub_snippets.display.dataframe_styled import display_styled, display_styled_resolvido
from hub_snippets.visual.badge import (
    badge_inline,
    badge_inline_resolvido,
    badge_score,
    badge_score_resolvido,
    badge_status,
    badge_status_resolvido,
)
from hub_snippets.visual.divider import (
    divider_heavy,
    divider_heavy_resolvido,
    divider_light,
    divider_light_resolvido,
    divider_medium,
    divider_medium_resolvido,
    divider_section,
    divider_section_resolvido,
)
from hub_snippets.visual.index_generator import gerar_indice_eda, gerar_indice_eda_resolvido
from hub_snippets.visual.kpi_card import kpi_card_html, kpi_card_html_resolvido, kpi_card_markdown
from hub_snippets.visual.section_header import section_header_html, section_header_html_resolvido
from hub_snippets.visual.tema import ThemeError, load_reference_theme, resolve_theme


def proposta(*, mode: str = "light", **tokens):
    data = load_reference_theme("notebook").to_dict()
    data["theme_id"] = "hub-v04-proposta"
    data["display_name"] = "V04 proposta sintética"
    data["description"] = "Configuração sintética para testes de HTML e tabela da V04."
    data["mode"] = mode
    data["tokens"].update(tokens)
    return resolve_theme(data, expected_context="notebook")


def normalizar_styler(html: str) -> str:
    """Remove somente o UUID aleatório do pandas Styler para comparar estrutura."""
    return re.sub(r"T_[0-9a-f]+", "T_UUID", html)


class AssinaturasLegadasTests(unittest.TestCase):
    def test_badges_preservados(self):
        self.assertEqual(list(inspect.signature(badge_status).parameters), ["texto", "tipo"])
        self.assertEqual(list(inspect.signature(badge_score).parameters), ["valor", "max"])
        self.assertEqual(list(inspect.signature(badge_inline).parameters), ["texto"])

    def test_divisores_preservados(self):
        for fn in (divider_light, divider_medium, divider_heavy, divider_section):
            self.assertEqual(list(inspect.signature(fn).parameters), [])

    def test_kpi_preservado(self):
        self.assertEqual(list(inspect.signature(kpi_card_html).parameters), ["metricas"])
        self.assertEqual(list(inspect.signature(kpi_card_markdown).parameters), ["metricas"])

    def test_section_header_preservado(self):
        self.assertEqual(
            list(inspect.signature(section_header_html).parameters),
            ["etapa", "emoji", "titulo", "descricao"],
        )

    def test_indice_preservado(self):
        self.assertEqual(list(inspect.signature(gerar_indice_eda).parameters), ["etapas_ativas", "markdown"])

    def test_dataframe_preservado(self):
        self.assertEqual(
            list(inspect.signature(display_styled).parameters),
            ["df_pandas", "highlight_cols", "format_dict"],
        )


class EquivalenciaLegadaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.theme = load_reference_theme("notebook")

    def test_styles_reference_reproduz_constantes_legadas(self):
        styles = get_styles_resolvidos(self.theme)
        self.assertEqual(styles["font.family"], FONT_FAMILY)
        self.assertEqual(styles["section.container"], STYLE_SECTION_HEADER)
        self.assertEqual(styles["section.title"], STYLE_SECTION_TITLE)
        self.assertEqual(styles["section.description"], STYLE_SECTION_DESCRIPTION)
        self.assertEqual(styles["card.kpi"], STYLE_KPI_CARD)
        self.assertEqual(styles["divider.light"], STYLE_DIVIDER_LIGHT)
        self.assertEqual(styles["divider.medium"], STYLE_DIVIDER_MEDIUM)
        self.assertEqual(styles["divider.heavy"], STYLE_DIVIDER_HEAVY)
        self.assertEqual(styles["divider.section_primary"], STYLE_DIVIDER_SECTION_PRIMARY)
        self.assertEqual(styles["divider.section_secondary"], STYLE_DIVIDER_SECTION_SECONDARY)
        self.assertEqual(styles["badge.ok"], STYLE_BADGE_OK)
        self.assertEqual(styles["badge.warn"], STYLE_BADGE_WARN)
        self.assertEqual(styles["badge.fail"], STYLE_BADGE_FAIL)
        self.assertEqual(styles["badge.info"], STYLE_BADGE_INFO)
        self.assertEqual(styles["index.container"], STYLE_INDEX_CONTAINER)
        self.assertEqual(styles["index.heading"], STYLE_INDEX_HEADING)
        self.assertEqual(styles["index.item"], STYLE_INDEX_ITEM)
        self.assertEqual(styles["index.description"], STYLE_INDEX_DESCRIPTION)

    def test_badges_reference_iguais(self):
        for tipo in ("ok", "warn", "fail", "info", "desconhecido"):
            with self.subTest(tipo=tipo):
                self.assertEqual(
                    badge_status("A&B <ok>", tipo),
                    badge_status_resolvido("A&B <ok>", self.theme, tipo),
                )
        for valor in (20, 50, 80, 99.6):
            self.assertEqual(badge_score(valor), badge_score_resolvido(valor, self.theme))
        self.assertEqual(badge_inline("Nota"), badge_inline_resolvido("Nota", self.theme))

    def test_divisores_reference_iguais(self):
        pares = (
            (divider_light, divider_light_resolvido),
            (divider_medium, divider_medium_resolvido),
            (divider_heavy, divider_heavy_resolvido),
            (divider_section, divider_section_resolvido),
        )
        for legacy, resolved in pares:
            self.assertEqual(legacy(), resolved(self.theme))

    def test_kpi_reference_igual(self):
        metricas = {"Clientes <ativos>": "10 & 2", "AUC": 0.81}
        self.assertEqual(kpi_card_html(metricas), kpi_card_html_resolvido(metricas, self.theme))

    def test_section_header_reference_igual(self):
        kwargs = {"etapa": 1, "titulo": "Título <x>", "descricao": "A&B"}
        self.assertEqual(section_header_html(**kwargs), section_header_html_resolvido(self.theme, **kwargs))

    def test_indice_reference_igual(self):
        self.assertEqual(gerar_indice_eda([0, 2]), gerar_indice_eda_resolvido(self.theme, [0, 2]))
        self.assertEqual(
            gerar_indice_eda([0, 2], markdown=True),
            gerar_indice_eda_resolvido(self.theme, [0, 2], markdown=True),
        )

    def test_dataframe_reference_semantico_equivalente(self):
        df = pd.DataFrame({"a": [1, -2], "b": [3.1415, 4.2]})
        legacy = normalizar_styler(display_styled(df, ["a"], {"b": "{:.1f}"}))
        resolved = normalizar_styler(display_styled_resolvido(df, self.theme, ["a"], {"b": "{:.1f}"}))
        # `white` no legado e `#FFFFFF` no contrato são a mesma cor; normalize só esse alias.
        legacy = legacy.replace("color: white;", "color: #FFFFFF;")
        self.assertEqual(legacy, resolved)


class PropagacaoTokensTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.theme = proposta(**{
            "brand.primary": "#112233",
            "text.primary": "#223344",
            "text.secondary": "#334455",
            "surface.section": "#E1E2E3",
            "surface.card": "#D1D2D3",
            "table.header_text": "#FAFAFA",
            "divider.light": "#A1A2A3",
            "divider.medium": "#B1B2B3",
            "status.ok_bg": "#C1F1C1",
            "status.ok_text": "#145214",
            "status.warn_bg": "#FFF0C1",
            "status.warn_text": "#805000",
            "status.fail_bg": "#FAD1D1",
            "status.fail_text": "#801111",
            "semantic.negative": "#991122",
            "font.family": "system_arial",
            "section.title_px": 24,
            "section.description_px": 15,
            "section.radius_px": 9,
            "section.padding_y_px": 14,
            "section.padding_x_px": 19,
            "section.border_px": 6,
            "card.font_px": 15,
            "card.radius_px": 13,
            "card.padding_y_px": 6,
            "card.padding_x_px": 12,
            "badge.font_px": 14,
            "badge.radius_px": 11,
            "badge.padding_y_px": 4,
            "badge.padding_x_px": 10,
        })

    def test_section_tokens(self):
        html = section_header_html_resolvido(self.theme, titulo="Teste", descricao="Descrição")
        for trecho in ("background:#E1E2E3", "border-left:6px solid #112233", "padding:14px 19px", "border-radius:9px", "font-family:Arial, sans-serif", "font-size:24px", "color:#334455", "font-size:15px"):
            self.assertIn(trecho, html)

    def test_card_tokens_e_escape(self):
        html = kpi_card_html_resolvido({"A<B": "1&2"}, self.theme)
        for trecho in ("background:#D1D2D3", "padding:6px 12px", "border-radius:13px", "font-size:15px", "color:#223344", "font-family:Arial, sans-serif"):
            self.assertIn(trecho, html)
        self.assertIn("A&lt;B", html)
        self.assertIn("1&amp;2", html)
        self.assertNotIn("A<B", html)

    def test_badge_tokens_e_fallback(self):
        esperado = {
            "ok": ("#C1F1C1", "#145214"),
            "warn": ("#FFF0C1", "#805000"),
            "fail": ("#FAD1D1", "#801111"),
            "info": ("#D1D2D3", "#112233"),
            "qualquer": ("#D1D2D3", "#112233"),
        }
        for tipo, (bg, fg) in esperado.items():
            html = badge_status_resolvido("<x>", self.theme, tipo)
            self.assertIn(f"background:{bg}", html)
            self.assertIn(f"color:{fg}", html)
            self.assertIn("padding:4px 10px", html)
            self.assertIn("border-radius:11px", html)
            self.assertIn("font-size:14px", html)
            self.assertIn("&lt;x&gt;", html)

    def test_score_muda_somente_aparencia(self):
        self.assertIn("Score: 80/100", badge_score_resolvido(80, self.theme))
        self.assertIn("background:#C1F1C1", badge_score_resolvido(80, self.theme))
        self.assertIn("background:#FFF0C1", badge_score_resolvido(50, self.theme))
        self.assertIn("background:#FAD1D1", badge_score_resolvido(49, self.theme))

    def test_divider_tokens(self):
        self.assertIn("#A1A2A3", divider_light_resolvido(self.theme))
        self.assertIn("#B1B2B3", divider_medium_resolvido(self.theme))
        self.assertIn("#112233", divider_heavy_resolvido(self.theme))
        section = divider_section_resolvido(self.theme)
        self.assertIn("2px solid #112233", section)
        self.assertIn("1px solid #A1A2A3", section)

    def test_indice_tokens(self):
        html = gerar_indice_eda_resolvido(self.theme, [0])
        self.assertIn("font-family:Arial, sans-serif", html)
        self.assertIn("color:#112233", html)
        self.assertIn("background:#E1E2E3", html)
        self.assertIn("color:#334455", html)

    def test_dataframe_tokens_e_dados_preservados(self):
        df = pd.DataFrame({"x": [1, -2], "y": [3, 4]})
        before = df.copy(deep=True)
        html = display_styled_resolvido(df, self.theme, ["x"])
        pd.testing.assert_frame_equal(df, before)
        self.assertIn("background-color: #112233", html)
        self.assertIn("color: #FAFAFA", html)
        self.assertIn("color: #991122", html)

    def test_markdown_nao_recebe_css(self):
        texto = gerar_indice_eda_resolvido(self.theme, [0], markdown=True)
        self.assertEqual(texto, gerar_indice_eda([0], markdown=True))
        self.assertNotIn("#112233", texto)


class IntegridadeTests(unittest.TestCase):
    def reject(self, code, callback, *args, **kwargs):
        with self.assertRaises(ThemeError) as exc:
            callback(*args, **kwargs)
        self.assertEqual(exc.exception.code, code)

    def test_dicionario_cru_rejeitado(self):
        self.reject("RESULT_TYPE", get_styles_resolvidos, load_reference_theme("notebook").to_dict())

    def test_contexto_readme_rejeitado(self):
        self.reject("CONTEXT_MISMATCH", get_styles_resolvidos, load_reference_theme("readme"))

    def test_fingerprint_adulterado_rejeitado(self):
        theme = replace(load_reference_theme("notebook"), fingerprint="0" * 64)
        self.reject("RESULT_INTEGRITY", get_styles_resolvidos, theme)

    def test_values_adulterados_nao_contaminam_estilos(self):
        theme = load_reference_theme("notebook")
        values = theme.to_dict()
        values["tokens"]["brand.primary"] = "#FFFFFF"
        values["tokens"]["badge.font_px"] = 24
        adulterado = replace(theme, _values=values)
        styles = get_styles_resolvidos(adulterado)
        self.assertEqual(styles["section.title"], STYLE_SECTION_TITLE)
        self.assertEqual(styles["badge.ok"], STYLE_BADGE_OK)

    def test_dicionario_de_estilos_e_copia(self):
        theme = load_reference_theme("notebook")
        styles = get_styles_resolvidos(theme)
        styles["section.title"] = "color:#FFFFFF"
        self.assertEqual(get_styles_resolvidos(theme)["section.title"], STYLE_SECTION_TITLE)

    def test_dark_e_high_contrast_sao_aceitos_no_html(self):
        for mode in ("dark", "high_contrast"):
            with self.subTest(mode=mode):
                theme = proposta(mode=mode, **{"brand.primary": "#112233"})
                self.assertIn("#112233", section_header_html_resolvido(theme, titulo=mode))

    def test_modo_nao_certifica_acessibilidade_nem_altera_logica(self):
        theme = proposta(mode="high_contrast")
        self.assertIn("Score: 50/100", badge_score_resolvido(50, theme))
        self.assertIn("background:#FFF8E1", badge_score_resolvido(50, theme))

    def test_markdown_ainda_revalida_o_tema(self):
        theme = replace(load_reference_theme("notebook"), fingerprint="0" * 64)
        self.reject("RESULT_INTEGRITY", gerar_indice_eda_resolvido, theme, [0], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
