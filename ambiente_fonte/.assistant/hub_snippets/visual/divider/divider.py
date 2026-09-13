"""Separadores visuais reutilizáveis para notebooks.

As funções legadas preservam o HTML existente. A V04 acrescenta variantes
opt-in que consomem ``ResolvedTheme`` sem manter estado compartilhado.
"""

from __future__ import annotations

from hub_snippets.constants.styles import (
    STYLE_DIVIDER_HEAVY,
    STYLE_DIVIDER_LIGHT,
    STYLE_DIVIDER_MEDIUM,
    STYLE_DIVIDER_SECTION_PRIMARY,
    STYLE_DIVIDER_SECTION_SECONDARY,
    get_styles_resolvidos,
)
from hub_snippets.visual.tema import ResolvedTheme


def divider_light() -> str:
    return f'<hr style="{STYLE_DIVIDER_LIGHT}"/>'


def divider_medium() -> str:
    return f'<hr style="{STYLE_DIVIDER_MEDIUM}"/>'


def divider_heavy() -> str:
    return f'<hr style="{STYLE_DIVIDER_HEAVY}"/>'


def divider_section() -> str:
    return (f'<div style="margin:20px 0;"><hr style="{STYLE_DIVIDER_SECTION_PRIMARY}"/>'
            f'<hr style="{STYLE_DIVIDER_SECTION_SECONDARY}"/></div>')


def divider_light_resolvido(theme: ResolvedTheme) -> str:
    styles = get_styles_resolvidos(theme)
    return f'<hr style="{styles["divider.light"]}"/>'


def divider_medium_resolvido(theme: ResolvedTheme) -> str:
    styles = get_styles_resolvidos(theme)
    return f'<hr style="{styles["divider.medium"]}"/>'


def divider_heavy_resolvido(theme: ResolvedTheme) -> str:
    styles = get_styles_resolvidos(theme)
    return f'<hr style="{styles["divider.heavy"]}"/>'


def divider_section_resolvido(theme: ResolvedTheme) -> str:
    styles = get_styles_resolvidos(theme)
    return (f'<div style="margin:20px 0;"><hr style="{styles["divider.section_primary"]}"/>'
            f'<hr style="{styles["divider.section_secondary"]}"/></div>')
