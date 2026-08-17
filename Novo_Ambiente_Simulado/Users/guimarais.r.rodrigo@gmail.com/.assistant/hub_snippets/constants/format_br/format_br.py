"""
Formatação numérica padrão brasileiro para outputs de notebooks.

Uso:
    from hub_snippets.constants.format_br import fmt_int, fmt_pct, fmt_brl, fmt_dec, fmt_delta

    fmt_int(3375674)       # "3.375.674"
    fmt_pct(0.928)         # "92,8%"
    fmt_pct(0.1229, 2)     # "12,29%"
    fmt_brl(12345.67)      # "R$ 12.345,67"
    fmt_dec(0.8234, 4)     # "0,8234"
    fmt_delta(-0.032)      # "-3,2 pp"
    fmt_delta(0.005, "bps") # "+5 bps"

Autor: Rodrigo via assistente
Versão: 1.0
"""

from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal, Union

Number = Union[int, float]


def fmt_int(n: Number) -> str:
    """Formata inteiro no padrão BR (3.375.674).

    Args:
        n: Número inteiro (ou float que será truncado).

    Returns:
        String formatada com ponto como separador de milhares.
    """
    return f"{int(n):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(v: float, casas: int = 1, input_scale: Literal["ratio", "percent"] = "ratio") -> str:
    """Formata percentual no padrão BR (92,8%).

    Args:
        v: Razão (0.928) por padrão ou percentual (92.8) quando
            ``input_scale="percent"``.
        casas: Casas decimais.

    Returns:
        String formatada (ex: "92,8%").
    """
    if input_scale not in {"ratio", "percent"}:
        raise ValueError("input_scale must be 'ratio' or 'percent'")
    pct = v * 100 if input_scale == "ratio" else v
    formatted = f"{pct:.{casas}f}".replace(".", ",")
    return f"{formatted}%"


def fmt_brl(v: float) -> str:
    """Formata valor monetário BR (R$ 12.345,67).

    Args:
        v: Valor numérico.

    Returns:
        String formatada com R$, ponto de milhar e vírgula decimal.
    """
    rounded = Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sign = "-" if rounded < 0 else ""
    absolute = abs(rounded)
    integer_part = int(absolute)
    decimal_part = int((absolute - integer_part) * 100)
    formatted_integer = f"{integer_part:,}".replace(",", ".")
    return f"{sign}R$ {formatted_integer},{decimal_part:02d}"


def fmt_dec(v: float, casas: int = 4) -> str:
    """Formata decimal no padrão BR (0,8234).

    Args:
        v: Valor decimal.
        casas: Casas decimais.

    Returns:
        String com vírgula como separador decimal.
    """
    return f"{v:.{casas}f}".replace(".", ",")


def fmt_delta(v: float, unidade: str = "pp") -> str:
    """Formata diferença/delta com sinal e unidade.

    Args:
        v: Valor do delta (ex: -0.032 para -3.2pp).
        unidade: "pp" (pontos percentuais) ou "bps" (basis points).

    Returns:
        String formatada (ex: "-3,2 pp" ou "+5 bps").
    """
    if unidade == "bps":
        valor = v * 10000  # 0.0005 -> 5 bps
        sinal = "+" if valor > 0 else ""
        return f"{sinal}{valor:.0f} bps".replace(".", ",")
    else:  # pp
        valor = v * 100  # 0.032 -> 3.2 pp
        sinal = "+" if valor > 0 else ""
        formatted = f"{sinal}{valor:.1f}".replace(".", ",")
        return f"{formatted} pp"


def fmt_n(n: Number, sufixo: bool = True) -> str:
    """Formata número com sufixo inteligente (3,4M, 125k, 42).

    Args:
        n: Número a formatar.
        sufixo: Se True, usa k/M/B para números grandes.

    Returns:
        String compacta.
    """
    n = float(n)
    if not sufixo or abs(n) < 1000:
        return fmt_int(n) if n == int(n) else fmt_dec(n, 1)
    elif abs(n) < 1_000_000:
        return f"{n/1000:.1f}k".replace(".", ",")
    elif abs(n) < 1_000_000_000:
        return f"{n/1_000_000:.1f}M".replace(".", ",")
    else:
        return f"{n/1_000_000_000:.1f}B".replace(".", ",")
