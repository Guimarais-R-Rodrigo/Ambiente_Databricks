"""Renderização HTML estilizada de DataFrames pandas.

A função legada preserva a aparência existente. A V04 acrescenta uma rota
opt-in que recebe ``ResolvedTheme`` para cabeçalho e destaque negativo, sem
alterar dados, formatos ou estado global do pandas.
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from hub_snippets.constants.styles import (
    TABLE_FONT_FAMILY,
    TABLE_HEADER_BACKGROUND,
    TABLE_HEADER_TEXT,
    TABLE_NEGATIVE,
    get_styles_resolvidos,
)
from hub_snippets.visual.tema import ResolvedTheme


def _display_styled(df_pandas, highlight_cols: Optional[Iterable[str]], format_dict: Optional[Dict[str, str]], *, header_background: str, header_text: str, font_family: str, negative: str) -> str:
    styled = df_pandas.style.set_table_styles([
        {"selector": "th", "props": [("background-color", header_background), ("color", header_text), ("font-family", font_family)]}
    ])
    if highlight_cols:
        for col in highlight_cols:
            if col in df_pandas.columns:
                # `Styler.applymap` foi removido no pandas 3.0 em favor de
                # `Styler.map`; o fallback mantém runtimes anteriores.
                aplicar = getattr(styled, "map", None) or styled.applymap
                styled = aplicar(
                    lambda v: f"color:{negative}; font-weight:bold;"
                    if isinstance(v, (int, float)) and v < 0 else "",
                    subset=[col],
                )
    if format_dict:
        styled = styled.format(format_dict)
    return styled.to_html()


def display_styled(df_pandas, highlight_cols: Optional[Iterable[str]] = None, format_dict: Optional[Dict[str, str]] = None) -> str:
    """Return styled HTML for a pandas DataFrame."""
    return _display_styled(
        df_pandas,
        highlight_cols,
        format_dict,
        header_background=TABLE_HEADER_BACKGROUND,
        header_text=TABLE_HEADER_TEXT,
        font_family=TABLE_FONT_FAMILY,
        negative=TABLE_NEGATIVE,
    )


def display_styled_resolvido(df_pandas, theme: ResolvedTheme, highlight_cols: Optional[Iterable[str]] = None, format_dict: Optional[Dict[str, str]] = None) -> str:
    """Renderiza a tabela com tokens notebook do tema explicitamente recebido."""
    styles = get_styles_resolvidos(theme)
    return _display_styled(
        df_pandas,
        highlight_cols,
        format_dict,
        header_background=styles["table.header_background"],
        header_text=styles["table.header_text"],
        font_family=styles["table.font_family"],
        negative=styles["table.negative"],
    )
