"""Tema Plotly institucional e adaptador explícito do Sistema de Temas.

As três funções legadas permanecem compatíveis. A V03 acrescenta uma rota opt-in
que consome ``ResolvedTheme`` da V02 sem alterar sessão, figura ou configuração
legada durante o simples import.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional

import plotly.io as pio
import plotly.graph_objects as go

from hub_snippets.constants.colors import (
    AZUL_CAIXA,
    CINZA_ESCURO,
    PALETA_CATEGORICA,
    TEXTO_SECUNDARIO,
)
from hub_snippets.visual.tema import ResolvedTheme, ThemeError, export_theme


_FONT_STACKS = {
    "system_sans": "Segoe UI, Roboto, sans-serif",
    "system_arial": "Arial, sans-serif",
}
_TEMPLATE_NAME_RE = re.compile(r"^hub-[a-z0-9]+(?:-[a-z0-9]+)*$")


def get_tema_eda() -> Dict[str, Any]:
    """Return the legacy default Plotly theme configuration for the ecosystem."""
    return {
        "template": "plotly_white",
        "font": {"family": "Segoe UI, Roboto, sans-serif", "size": 12, "color": CINZA_ESCURO},
        "title": {"font": {"size": 16, "color": AZUL_CAIXA}, "x": 0.01, "xanchor": "left"},
        "colorway": PALETA_CATEGORICA,
        "height": 450,
        "width": 900,
        "margin": {"l": 60, "r": 30, "t": 70, "b": 60},
        "legend": {"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
    }


def aplicar_tema(fig: go.Figure, subtitulo: Optional[str] = None, fonte: Optional[str] = None, n: Optional[int] = None) -> go.Figure:
    """Apply the legacy institutional theme and optional footer annotations."""
    fig.update_layout(**get_tema_eda())
    footer_parts = []
    if n is not None:
        footer_parts.append(f"N = {n:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if fonte:
        footer_parts.append(f"Fonte: {fonte}")
    if subtitulo:
        footer_parts.append(subtitulo)

    if footer_parts:
        fig.add_annotation(
            text=" | ".join(footer_parts),
            xref="paper",
            yref="paper",
            x=0,
            y=-0.18,
            showarrow=False,
            font={"size": 10, "color": TEXTO_SECUNDARIO},
            xanchor="left",
        )
    return fig


def registrar_template_plotly() -> None:
    """Register the legacy 'caixa' Plotly template globally in the current session."""
    pio.templates["caixa"] = go.layout.Template(layout=get_tema_eda())
    pio.templates.default = "caixa"


def _dados_tema_plotly(theme: ResolvedTheme) -> tuple[dict[str, Any], Any]:
    """Revalida um resultado V02 e limita a V03 ao contexto notebook/light."""
    if type(theme) is not ResolvedTheme:
        raise ThemeError(
            "RESULT_TYPE",
            "Forneça um tema resolvido pelo núcleo V02.",
            action="Use resolve_theme ou load_theme; não passe dicionário diretamente ao adaptador Plotly.",
        )
    # export_theme revalida schema, recursos e fingerprint; não grava arquivo.
    # A representação devolvida é a única fonte confiável para o adaptador:
    # não lemos _values/tokens diretamente de um dataclass potencialmente substituído.
    data = json.loads(export_theme(theme))
    if data["context"] != "notebook":
        raise ThemeError(
            "CONTEXT_MISMATCH",
            "O adaptador Plotly exige contexto notebook.",
            field="$.context",
            action="Escolha uma configuração completa de notebook; não force fallback.",
        )
    if data["mode"] != "light":
        raise ThemeError(
            "PLOTLY_MODE_UNSUPPORTED",
            "A V03 aplica somente o modo light ao Plotly.",
            field="$.mode",
            action="Mantenha o modo light nesta etapa; dark/high_contrast exigem tokens de superfície próprios antes de uso.",
        )
    return data, data["tokens"]


def get_tema_plotly(theme: ResolvedTheme) -> Dict[str, Any]:
    """Converte tokens notebook validados em layout Plotly, sem efeito de sessão.

    A função não lê tema global, não usa fixture implicitamente e não aprova a
    configuração. O alinhamento do título, legenda e template-base continuam
    políticas do adaptador porque o contrato 0.1.0 não os expõe como tokens.
    """
    _data, tokens = _dados_tema_plotly(theme)
    family = _FONT_STACKS[tokens["font.family"]]
    return {
        "template": "plotly_white",
        "font": {
            "family": family,
            "size": tokens["chart.font_px"],
            "color": tokens["text.plot"],
        },
        "title": {
            "font": {"size": tokens["chart.title_px"], "color": tokens["brand.primary"]},
            "x": 0.01,
            "xanchor": "left",
        },
        "colorway": list(tokens["palette.categorical"]),
        "height": tokens["chart.height_px"],
        "width": tokens["chart.width_px"],
        "margin": {
            "l": tokens["chart.margin_left_px"],
            "r": tokens["chart.margin_right_px"],
            "t": tokens["chart.margin_top_px"],
            "b": tokens["chart.margin_bottom_px"],
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.25,
            "xanchor": "center",
            "x": 0.5,
        },
    }


def aplicar_tema_resolvido(
    fig: go.Figure,
    theme: ResolvedTheme,
    subtitulo: Optional[str] = None,
    fonte: Optional[str] = None,
    n: Optional[int] = None,
) -> go.Figure:
    """Aplica explicitamente um tema V02 notebook à figura recebida.

    Modifica e devolve a mesma figura, como a API legada. Não altera
    ``pio.templates.default`` e não modifica dados, eixos ou cores já definidas
    nos traces; propriedades específicas podem ser ajustadas depois da chamada.
    """
    _data, tokens = _dados_tema_plotly(theme)
    config = get_tema_plotly(theme)
    fig.update_layout(**config)
    footer_parts = []
    if n is not None:
        footer_parts.append(f"N = {n:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if fonte:
        footer_parts.append(f"Fonte: {fonte}")
    if subtitulo:
        footer_parts.append(subtitulo)
    if footer_parts:
        fig.add_annotation(
            text=" | ".join(footer_parts),
            xref="paper",
            yref="paper",
            x=0,
            y=-0.18,
            showarrow=False,
            font={
                "size": tokens["chart.footer_px"],
                "color": tokens["text.secondary"],
            },
            xanchor="left",
        )
    return fig


def registrar_template_plotly_resolvido(
    theme: ResolvedTheme,
    *,
    nome: str,
    ativar: bool = False,
    substituir: bool = False,
) -> None:
    """Registra um template configurado com efeito de sessão explicitamente controlado.

    ``nome`` deve usar o namespace ``hub-*``. O nome legado ``caixa`` e templates
    nativos ficam fora desta API. Registrar não ativa por padrão; ``ativar=True``
    é a ação explícita que muda ``pio.templates.default``. Substituir um nome que
    já participa do default ativo também exige ``ativar=True`` para não produzir
    mudança global implícita pela troca do objeto registrado.
    """
    config = get_tema_plotly(theme)
    if type(nome) is not str or len(nome) > 64 or _TEMPLATE_NAME_RE.fullmatch(nome) is None:
        raise ThemeError(
            "PLOTLY_TEMPLATE_NAME",
            "Use um nome de template no formato hub-nome, com letras minúsculas, números e hífens.",
            field="$.template_name",
            action="Escolha um nome próprio da sessão; o template legado caixa é reservado.",
        )
    if type(ativar) is not bool or type(substituir) is not bool:
        raise ThemeError(
            "PLOTLY_TEMPLATE_OPTION",
            "As opções ativar e substituir precisam ser booleanas.",
            field="$.template_options",
        )
    default_atual = pio.templates.default
    templates_ativos = (
        {parte.strip() for parte in default_atual.split("+") if parte.strip()}
        if isinstance(default_atual, str)
        else set()
    )
    if nome in pio.templates and not substituir:
        raise ThemeError(
            "PLOTLY_TEMPLATE_EXISTS",
            "Já existe um template com esse nome na sessão.",
            field="$.template_name",
            action="Escolha outro nome ou use substituir=True conscientemente.",
        )
    if nome in pio.templates and substituir and not ativar and nome in templates_ativos:
        raise ThemeError(
            "PLOTLY_TEMPLATE_ACTIVE",
            "O template solicitado já participa do padrão ativo da sessão.",
            field="$.template_name",
            action="Para substituí-lo, use ativar=True explicitamente ou escolha outro nome.",
        )
    pio.templates[nome] = go.layout.Template(layout=config)
    if ativar:
        pio.templates.default = nome
