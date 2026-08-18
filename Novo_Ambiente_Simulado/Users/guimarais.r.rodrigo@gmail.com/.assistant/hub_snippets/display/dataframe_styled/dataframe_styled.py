
"""Renderização HTML estilizada de DataFrames pandas."""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from hub_snippets.constants.colors import AZUL_CAIXA, VERMELHO


def display_styled(df_pandas, highlight_cols: Optional[Iterable[str]] = None, format_dict: Optional[Dict[str, str]] = None) -> str:
    """Return styled HTML for a pandas DataFrame.

    Notes:
        The caller may use `displayHTML(display_styled(...))`.
    """
    styled = df_pandas.style.set_table_styles([
        {"selector": "th", "props": [("background-color", AZUL_CAIXA), ("color", "white"), ("font-family", "Segoe UI")]} 
    ])
    if highlight_cols:
        for col in highlight_cols:
            if col in df_pandas.columns:
                # `Styler.applymap` foi removido no pandas 3.0 em favor de
                # `Styler.map`. O runtime do Free traz 1.5.3, onde só existe o
                # antigo; o workspace do trabalho tem política de runtime
                # própria. O getattr cobre os dois sem mudar o comportamento.
                aplicar = getattr(styled, "map", None) or styled.applymap
                styled = aplicar(lambda v: f"color:{VERMELHO}; font-weight:bold;" if isinstance(v, (int, float)) and v < 0 else "", subset=[col])
    if format_dict:
        styled = styled.format(format_dict)
    return styled.to_html()
