
"""Renderização HTML estilizada de DataFrames pandas."""

from __future__ import annotations

from typing import Dict, Iterable, Optional


def display_styled(df_pandas, highlight_cols: Optional[Iterable[str]] = None, format_dict: Optional[Dict[str, str]] = None) -> str:
    """Return styled HTML for a pandas DataFrame.

    Notes:
        The caller may use `displayHTML(display_styled(...))`.
    """
    styled = df_pandas.style.set_table_styles([
        {"selector": "th", "props": [("background-color", "#005CA9"), ("color", "white"), ("font-family", "Segoe UI")]} 
    ])
    if highlight_cols:
        for col in highlight_cols:
            if col in df_pandas.columns:
                styled = styled.applymap(lambda v: "color:#C4262E; font-weight:bold;" if isinstance(v, (int, float)) and v < 0 else "", subset=[col])
    if format_dict:
        styled = styled.format(format_dict)
    return styled.to_html()
