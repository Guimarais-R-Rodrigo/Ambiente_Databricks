"""V03 — adaptador Plotly opt-in sobre o núcleo V02; sem Databricks/rede."""
from __future__ import annotations

import inspect
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ambiente_databricks/.assistant"))

import plotly.graph_objects as go
import plotly.io as pio

from hub_snippets.constants.colors import AZUL_CAIXA, PALETA_CATEGORICA
from hub_snippets.visual.tema import ThemeError, load_reference_theme, resolve_theme
from hub_snippets.visual.theme_plotly import (
    aplicar_tema,
    aplicar_tema_resolvido,
    get_tema_eda,
    get_tema_plotly,
    registrar_template_plotly,
    registrar_template_plotly_resolvido,
)


def proposta(**tokens):
    data = load_reference_theme("notebook").to_dict()
    data["theme_id"] = "hub-v03-proposta"
    data["display_name"] = "V03 proposta sintética"
    data["description"] = "Configuração sintética para testes do adaptador Plotly V03."
    data["tokens"].update(tokens)
    return resolve_theme(data, expected_context="notebook")


class TemasV03Tests(unittest.TestCase):
    def test_legado_assinatura_aplicar_preservada(self):
        self.assertEqual(list(inspect.signature(aplicar_tema).parameters), ["fig", "subtitulo", "fonte", "n"])

    def test_legado_assinaturas_restantes_preservadas(self):
        self.assertEqual(list(inspect.signature(get_tema_eda).parameters), [])
        self.assertEqual(list(inspect.signature(registrar_template_plotly).parameters), [])

    def test_fixture_legada_mapeia_exatamente_para_layout_legado(self):
        self.assertEqual(get_tema_plotly(load_reference_theme("notebook")), get_tema_eda())

    def test_get_config_nao_altera_default_da_sessao(self):
        before = pio.templates.default
        get_tema_plotly(load_reference_theme("notebook"))
        self.assertEqual(pio.templates.default, before)

    def test_config_retorna_copia_da_paleta(self):
        theme = load_reference_theme("notebook")
        config = get_tema_plotly(theme)
        config["colorway"][0] = "#FFFFFF"
        self.assertEqual(theme.tokens["palette.categorical"][0], "#005CA9")

    def test_tokens_configurados_chegam_ao_layout(self):
        theme = proposta(**{
            "brand.primary": "#112233",
            "text.plot": "#223344",
            "text.secondary": "#334455",
            "font.family": "system_arial",
            "chart.font_px": 14,
            "chart.title_px": 21,
            "chart.footer_px": 11,
            "chart.height_px": 510,
            "chart.width_px": 1020,
            "chart.margin_left_px": 71,
            "chart.margin_right_px": 41,
            "chart.margin_top_px": 81,
            "chart.margin_bottom_px": 61,
            "palette.categorical": ["#112233", "#445566", "#778899"],
        })
        config = get_tema_plotly(theme)
        self.assertEqual(config["font"], {"family": "Arial, sans-serif", "size": 14, "color": "#223344"})
        self.assertEqual(config["title"]["font"], {"size": 21, "color": "#112233"})
        self.assertEqual(config["colorway"], ["#112233", "#445566", "#778899"])
        self.assertEqual((config["height"], config["width"]), (510, 1020))
        self.assertEqual(config["margin"], {"l": 71, "r": 41, "t": 81, "b": 61})

    def test_aplicar_resolvido_retorna_mesmo_objeto(self):
        fig = go.Figure(go.Bar(x=["A"], y=[1]))
        self.assertIs(aplicar_tema_resolvido(fig, load_reference_theme("notebook")), fig)

    def test_aplicar_resolvido_preserva_dados_e_eixos(self):
        fig = go.Figure(go.Bar(x=["A", "B"], y=[10, 20], marker_color="#ABCDEF"))
        fig.update_xaxes(title="Categoria")
        fig.update_yaxes(title="Valor", range=[0, 25])
        before = json.loads(fig.to_json())
        aplicar_tema_resolvido(fig, proposta(**{"brand.primary": "#112233"}))
        after = json.loads(fig.to_json())
        self.assertEqual(before["data"], after["data"])
        self.assertEqual(before["layout"]["xaxis"], after["layout"]["xaxis"])
        self.assertEqual(before["layout"]["yaxis"], after["layout"]["yaxis"])
        self.assertEqual(after["data"][0]["marker"]["color"], "#ABCDEF")

    def test_aplicar_resolvido_nao_altera_default_da_sessao(self):
        before = pio.templates.default
        aplicar_tema_resolvido(go.Figure(), load_reference_theme("notebook"))
        self.assertEqual(pio.templates.default, before)

    def test_rodape_usa_tokens_configurados(self):
        theme = proposta(**{"text.secondary": "#334455", "chart.footer_px": 13})
        fig = go.Figure()
        aplicar_tema_resolvido(fig, theme, "Sintético", "fixture_local", 12000)
        ann = fig.layout.annotations[-1]
        self.assertEqual(ann.text, "N = 12.000 | Fonte: fixture_local | Sintético")
        self.assertEqual(ann.font.color, "#334455")
        self.assertEqual(ann.font.size, 13)

    def test_contexto_readme_e_rejeitado(self):
        with self.assertRaises(ThemeError) as ctx:
            get_tema_plotly(load_reference_theme("readme"))
        self.assertEqual(ctx.exception.code, "CONTEXT_MISMATCH")

    def test_dark_e_rejeitado_fail_closed(self):
        data = load_reference_theme("notebook").to_dict()
        data["mode"] = "dark"
        with self.assertRaises(ThemeError) as ctx:
            get_tema_plotly(resolve_theme(data))
        self.assertEqual(ctx.exception.code, "PLOTLY_MODE_UNSUPPORTED")

    def test_high_contrast_e_rejeitado_fail_closed(self):
        data = load_reference_theme("notebook").to_dict()
        data["mode"] = "high_contrast"
        with self.assertRaises(ThemeError) as ctx:
            get_tema_plotly(resolve_theme(data))
        self.assertEqual(ctx.exception.code, "PLOTLY_MODE_UNSUPPORTED")

    def test_dicionario_nao_e_aceito_no_adaptador(self):
        with self.assertRaises(ThemeError) as ctx:
            get_tema_plotly(load_reference_theme("notebook").to_dict())
        self.assertEqual(ctx.exception.code, "RESULT_TYPE")

    def test_fingerprint_adulterado_e_recusado(self):
        theme = load_reference_theme("notebook")
        adulterado = replace(theme, fingerprint="0" * 64)
        with self.assertRaises(ThemeError) as ctx:
            get_tema_plotly(adulterado)
        self.assertEqual(ctx.exception.code, "RESULT_INTEGRITY")

    def test_values_adulterados_nao_contaminam_layout_ou_rodape(self):
        theme = load_reference_theme("notebook")
        values = theme.to_dict()
        values["tokens"]["chart.width_px"] = 1
        values["tokens"]["chart.footer_px"] = 99
        values["tokens"]["text.secondary"] = "#FFFFFF"
        adulterado = replace(theme, _values=values)

        config = get_tema_plotly(adulterado)
        self.assertEqual(config, get_tema_eda())

        fig = go.Figure()
        aplicar_tema_resolvido(fig, adulterado, fonte="fixture_local", n=1)
        ann = fig.layout.annotations[-1]
        self.assertEqual(ann.font.size, theme.tokens["chart.footer_px"])
        self.assertEqual(ann.font.color, theme.tokens["text.secondary"])

    def test_registro_configurado_nao_ativa_por_padrao(self):
        name = "hub-v03-teste-nao-ativa"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            if existed:
                del pio.templates[name]
            self.assertIsNone(registrar_template_plotly_resolvido(load_reference_theme("notebook"), nome=name))
            self.assertIn(name, pio.templates)
            self.assertEqual(pio.templates.default, before_default)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_registro_configurado_ativa_somente_explicitamente(self):
        name = "hub-v03-teste-ativa"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            if existed:
                del pio.templates[name]
            registrar_template_plotly_resolvido(load_reference_theme("notebook"), nome=name, ativar=True)
            self.assertEqual(pio.templates.default, name)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_nome_de_template_precisa_namespace_hub(self):
        with self.assertRaises(ThemeError) as ctx:
            registrar_template_plotly_resolvido(load_reference_theme("notebook"), nome="caixa")
        self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_NAME")

    def test_colisao_nao_substitui_sem_opt_in(self):
        name = "hub-v03-colisao"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            with self.assertRaises(ThemeError) as ctx:
                registrar_template_plotly_resolvido(load_reference_theme("notebook"), nome=name)
            self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_EXISTS")
            self.assertEqual(pio.templates[name].layout.width, 321)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_substituicao_exige_flag_explicita(self):
        name = "hub-v03-substituir"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            registrar_template_plotly_resolvido(
                proposta(**{"chart.width_px": 1111}), nome=name, substituir=True
            )
            self.assertEqual(pio.templates[name].layout.width, 1111)
            self.assertEqual(pio.templates.default, before_default)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_substituicao_template_ativo_simples_exige_ativacao(self):
        name = "hub-v03-ativo-simples"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            pio.templates.default = name
            with self.assertRaises(ThemeError) as ctx:
                registrar_template_plotly_resolvido(
                    proposta(**{"chart.width_px": 1111}), nome=name, substituir=True
                )
            self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_ACTIVE")
            self.assertEqual(pio.templates[name].layout.width, 321)
            self.assertEqual(pio.templates.default, name)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_substituicao_template_ativo_composto_exige_ativacao(self):
        name = "hub-v03-ativo-composto"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            pio.templates.default = f"plotly+{name}"
            with self.assertRaises(ThemeError) as ctx:
                registrar_template_plotly_resolvido(
                    proposta(**{"chart.width_px": 1111}), nome=name, substituir=True
                )
            self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_ACTIVE")
            self.assertEqual(pio.templates[name].layout.width, 321)
            self.assertIn(name, pio.templates.default.split("+"))
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_substituicao_template_ativo_com_ativacao_explicita(self):
        name = "hub-v03-ativo-explicito"
        before_default = pio.templates.default
        existed = name in pio.templates
        old = pio.templates[name] if existed else None
        try:
            pio.templates[name] = go.layout.Template(layout={"width": 321})
            pio.templates.default = name
            registrar_template_plotly_resolvido(
                proposta(**{"chart.width_px": 1111}),
                nome=name,
                substituir=True,
                ativar=True,
            )
            self.assertEqual(pio.templates[name].layout.width, 1111)
            self.assertEqual(pio.templates.default, name)
        finally:
            pio.templates.default = before_default
            if name in pio.templates:
                del pio.templates[name]
            if existed:
                pio.templates[name] = old

    def test_opcoes_precisam_booleanas(self):
        with self.assertRaises(ThemeError) as ctx:
            registrar_template_plotly_resolvido(
                load_reference_theme("notebook"), nome="hub-v03-opcao", ativar=1
            )
        self.assertEqual(ctx.exception.code, "PLOTLY_TEMPLATE_OPTION")

    def test_registro_legado_caixa_continua_funcionando(self):
        before_default = pio.templates.default
        existed = "caixa" in pio.templates
        old = pio.templates["caixa"] if existed else None
        try:
            self.assertIsNone(registrar_template_plotly())
            self.assertEqual(pio.templates.default, "caixa")
            self.assertEqual(list(pio.templates["caixa"].layout.colorway), list(PALETA_CATEGORICA))
            self.assertEqual(pio.templates["caixa"].layout.title.font.color, AZUL_CAIXA)
        finally:
            pio.templates.default = before_default
            if existed:
                pio.templates["caixa"] = old
            elif "caixa" in pio.templates:
                del pio.templates["caixa"]


if __name__ == "__main__":
    unittest.main(verbosity=2)
