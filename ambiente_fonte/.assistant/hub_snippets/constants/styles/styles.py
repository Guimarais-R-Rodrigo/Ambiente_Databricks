"""Estilos CSS compartilhados para displayHTML e consumidores HTML do Hub.

As constantes públicas preservam a aparência legada. A V04 acrescenta
``get_styles_resolvidos``: uma materialização opt-in de CSS a partir de um
``ResolvedTheme`` notebook validado pelo núcleo V02. Não há estado global,
instalação, publicação ou CSS arbitrário vindo do tema.
"""

from __future__ import annotations

import json
from typing import Dict

from hub_snippets.constants import colors
from hub_snippets.visual.tema import ResolvedTheme, ThemeError, export_theme

FONT_FAMILY = "Segoe UI, Roboto, sans-serif"

STYLE_SECTION_HEADER = (
    f"background:{colors.BG_SECTION}; border-left:4px solid {colors.AZUL_CAIXA}; padding:12px 16px; "
    "margin:8px 0 12px 0; border-radius:4px; font-family:Segoe UI, Roboto, sans-serif;"
)
STYLE_SECTION_TITLE = f"margin:0; color:{colors.AZUL_CAIXA}; font-size:18px;"
STYLE_SECTION_DESCRIPTION = f"margin:6px 0 0 0; color:{colors.TEXTO_SECUNDARIO}; font-size:13px;"

STYLE_KPI_CARD = (
    f"display:inline-block; background:{colors.BG_HEADER}; padding:4px 10px; border-radius:12px; "
    f"font-size:12px; margin-right:8px; color:{colors.TEXTO_PRINCIPAL}; font-family:Segoe UI, Roboto, sans-serif;"
)

STYLE_DIVIDER_LIGHT = "border:none; border-top:1px solid #D9DEE3; margin:10px 0;"
STYLE_DIVIDER_MEDIUM = "border:none; border-top:1.5px solid #BFC7D1; margin:14px 0;"
STYLE_DIVIDER_HEAVY = f"border:none; border-top:2px solid {colors.AZUL_CAIXA}; margin:18px 0;"
STYLE_DIVIDER_SECTION_SECONDARY = "border:none; border-top:1px solid #D9DEE3; margin:4px 0 0 0;"

STYLE_BADGE_OK = "display:inline-block; background:#EAF7EC; color:#2E7D32; padding:2px 8px; border-radius:10px; font-size:11px;"
STYLE_BADGE_WARN = "display:inline-block; background:#FFF8E1; color:#B26A00; padding:2px 8px; border-radius:10px; font-size:11px;"
STYLE_BADGE_FAIL = "display:inline-block; background:#FDECEC; color:#B71C1C; padding:2px 8px; border-radius:10px; font-size:11px;"
STYLE_BADGE_INFO = f"display:inline-block; background:{colors.BG_HEADER}; color:{colors.AZUL_CAIXA}; padding:2px 8px; border-radius:10px; font-size:11px;"

STYLE_INDEX_CONTAINER = "font-family:Segoe UI, Roboto, sans-serif;"
STYLE_INDEX_HEADING = f"color:{colors.AZUL_CAIXA}; margin-bottom:10px;"
STYLE_INDEX_ITEM = f"margin:6px 0; padding:6px 10px; background:{colors.BG_SECTION}; border-radius:6px;"
STYLE_INDEX_DESCRIPTION = f"color:{colors.TEXTO_SECUNDARIO}; font-size:12px;"

TABLE_HEADER_BACKGROUND = colors.AZUL_CAIXA
TABLE_HEADER_TEXT = "#FFFFFF"
TABLE_FONT_FAMILY = "Segoe UI"
TABLE_NEGATIVE = colors.VERMELHO

_FONT_STACKS = {
    "system_sans": "Segoe UI, Roboto, sans-serif",
    "system_arial": "Arial, sans-serif",
}


def _dados_tema_notebook(theme: ResolvedTheme) -> tuple[dict, dict]:
    """Revalida o resultado V02 e devolve apenas configuração notebook confiável."""
    if type(theme) is not ResolvedTheme:
        raise ThemeError(
            "RESULT_TYPE",
            "Forneça um tema resolvido pelo núcleo V02.",
            action="Use resolve_theme ou load_theme; não passe dicionário diretamente aos componentes HTML.",
        )
    data = json.loads(export_theme(theme))
    if data["context"] != "notebook":
        raise ThemeError(
            "CONTEXT_MISMATCH",
            "Os componentes HTML da V04 exigem contexto notebook.",
            field="$.context",
            action="Escolha uma configuração completa de notebook; não force fallback.",
        )
    return data, data["tokens"]


def get_styles_resolvidos(theme: ResolvedTheme) -> Dict[str, str]:
    """Materializa estilos HTML a partir de tokens notebook, sem efeito global.

    O contrato continua fechado: não há campo de CSS livre. Valores de cor,
    dimensões e família tipográfica já foram validados pelo núcleo antes de
    compor estas strings. Modificar o dicionário retornado não altera o tema.
    """
    _data, tokens = _dados_tema_notebook(theme)
    family = _FONT_STACKS[tokens["font.family"]]

    return {
        "font.family": family,
        "section.container": (
            f"background:{tokens['surface.section']}; border-left:{tokens['section.border_px']}px solid {tokens['brand.primary']}; "
            f"padding:{tokens['section.padding_y_px']}px {tokens['section.padding_x_px']}px; margin:8px 0 12px 0; "
            f"border-radius:{tokens['section.radius_px']}px; font-family:{family};"
        ),
        "section.title": f"margin:0; color:{tokens['brand.primary']}; font-size:{tokens['section.title_px']}px;",
        "section.description": (
            f"margin:6px 0 0 0; color:{tokens['text.secondary']}; font-size:{tokens['section.description_px']}px;"
        ),
        "card.kpi": (
            f"display:inline-block; background:{tokens['surface.card']}; padding:{tokens['card.padding_y_px']}px {tokens['card.padding_x_px']}px; "
            f"border-radius:{tokens['card.radius_px']}px; font-size:{tokens['card.font_px']}px; margin-right:8px; "
            f"color:{tokens['text.primary']}; font-family:{family};"
        ),
        "divider.light": f"border:none; border-top:1px solid {tokens['divider.light']}; margin:10px 0;",
        "divider.medium": f"border:none; border-top:1.5px solid {tokens['divider.medium']}; margin:14px 0;",
        "divider.heavy": f"border:none; border-top:2px solid {tokens['brand.primary']}; margin:18px 0;",
        "divider.section_secondary": f"border:none; border-top:1px solid {tokens['divider.light']}; margin:4px 0 0 0;",
        "badge.ok": (
            f"display:inline-block; background:{tokens['status.ok_bg']}; color:{tokens['status.ok_text']}; "
            f"padding:{tokens['badge.padding_y_px']}px {tokens['badge.padding_x_px']}px; border-radius:{tokens['badge.radius_px']}px; "
            f"font-size:{tokens['badge.font_px']}px;"
        ),
        "badge.warn": (
            f"display:inline-block; background:{tokens['status.warn_bg']}; color:{tokens['status.warn_text']}; "
            f"padding:{tokens['badge.padding_y_px']}px {tokens['badge.padding_x_px']}px; border-radius:{tokens['badge.radius_px']}px; "
            f"font-size:{tokens['badge.font_px']}px;"
        ),
        "badge.fail": (
            f"display:inline-block; background:{tokens['status.fail_bg']}; color:{tokens['status.fail_text']}; "
            f"padding:{tokens['badge.padding_y_px']}px {tokens['badge.padding_x_px']}px; border-radius:{tokens['badge.radius_px']}px; "
            f"font-size:{tokens['badge.font_px']}px;"
        ),
        "badge.info": (
            f"display:inline-block; background:{tokens['surface.card']}; color:{tokens['brand.primary']}; "
            f"padding:{tokens['badge.padding_y_px']}px {tokens['badge.padding_x_px']}px; border-radius:{tokens['badge.radius_px']}px; "
            f"font-size:{tokens['badge.font_px']}px;"
        ),
        "index.container": f"font-family:{family};",
        "index.heading": f"color:{tokens['brand.primary']}; margin-bottom:10px;",
        "index.item": f"margin:6px 0; padding:6px 10px; background:{tokens['surface.section']}; border-radius:6px;",
        "index.description": f"color:{tokens['text.secondary']}; font-size:12px;",
        "table.header_background": tokens["brand.primary"],
        "table.header_text": tokens["table.header_text"],
        "table.negative": tokens["semantic.negative"],
        "table.font_family": TABLE_FONT_FAMILY,
    }
