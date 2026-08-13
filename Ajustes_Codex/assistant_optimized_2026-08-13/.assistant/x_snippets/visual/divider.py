
"""Separadores visuais reutilizáveis para notebooks."""


def divider_light() -> str:
    return '<hr style="border:none; border-top:1px solid #D9DEE3; margin:10px 0;"/>'


def divider_medium() -> str:
    return '<hr style="border:none; border-top:1.5px solid #BFC7D1; margin:14px 0;"/>'


def divider_heavy() -> str:
    return '<hr style="border:none; border-top:2px solid #005CA9; margin:18px 0;"/>'


def divider_section() -> str:
    return '<div style="margin:20px 0;"><hr style="border:none; border-top:2px solid #005CA9; margin:0;"/><hr style="border:none; border-top:1px solid #D9DEE3; margin:4px 0 0 0;"/></div>'
