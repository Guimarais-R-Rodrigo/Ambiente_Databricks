
"""Separadores visuais reutilizáveis para notebooks."""

from hub_snippets.constants.colors import AZUL_CAIXA


def divider_light() -> str:
    return '<hr style="border:none; border-top:1px solid #D9DEE3; margin:10px 0;"/>'


def divider_medium() -> str:
    return '<hr style="border:none; border-top:1.5px solid #BFC7D1; margin:14px 0;"/>'


def divider_heavy() -> str:
    return f'<hr style="border:none; border-top:2px solid {AZUL_CAIXA}; margin:18px 0;"/>'


def divider_section() -> str:
    return (f'<div style="margin:20px 0;"><hr style="border:none; border-top:2px solid {AZUL_CAIXA}; margin:0;"/>'
            '<hr style="border:none; border-top:1px solid #D9DEE3; margin:4px 0 0 0;"/></div>')
