"""
Conversão de modelo logístico em scorecard de pontos.

Uso:
    from hub_snippets.ml.scorecard_builder import build_scorecard
    scorecard = build_scorecard(coefs, intercept, woe_tables, pdo=20, base_score=600, base_odds=50)

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import pandas as pd
from typing import Dict, List


def build_scorecard(
    coefs: np.ndarray,
    intercept: float,
    feature_names: List[str],
    woe_tables: Dict[str, pd.DataFrame],
    pdo: int = 20,
    base_score: int = 600,
    base_odds: int = 50,
    event_is_bad: bool = True,
) -> pd.DataFrame:
    """Converte coeficientes de logistic regression em pontos de scorecard.

    Args:
        coefs: Coeficientes do modelo (array).
        intercept: Intercepto do modelo.
        feature_names: Nomes das features (ordem dos coefs).
        woe_tables: Dict feature_name → DataFrame **pandas** com colunas
            [faixa, woe]. **A saída de `woe_iv_calculator.calculate_woe_iv` não
            serve direto**: ela é Spark, e a coluna de faixa se chama como a
            feature. A ponte é de duas linhas e está no smoke test::

                ponte = (tabela.toPandas()
                         .rename(columns={feature: "faixa"})[["faixa", "woe"]])

            Os dois módulos passavam sozinhos e a junção nunca tinha sido
            exercitada; quem a descobriu foi a bateria funcional de 19/08/2026.
        pdo: Points to Double Odds.
        base_score: Score base (no ponto de base_odds).
        base_odds: Odds de referência (bom:mau) no base_score.

    Returns:
        DataFrame com scorecard: feature | faixa | woe | pontos.
    """
    coefs = np.asarray(coefs, dtype=float).reshape(-1)
    if len(feature_names) == 0 or len(coefs) != len(feature_names):
        raise ValueError("coefs and feature_names must have the same non-zero length")
    if not np.isfinite(coefs).all() or not np.isfinite(float(intercept)):
        raise ValueError("coefs and intercept must contain only finite values")
    if pdo <= 0 or base_odds <= 0:
        raise ValueError("pdo and base_odds must be positive")
    missing = set(feature_names) - set(woe_tables)
    if missing:
        raise ValueError(f"woe_tables missing features: {sorted(missing)}")

    # The model logit predicts P(event). When event is bad, higher log-odds must
    # reduce the score; when event is good, they increase it.
    direction = -1.0 if event_is_bad else 1.0
    factor = pdo / np.log(2)
    offset = base_score - factor * np.log(base_odds)

    # Pontos do intercepto (distribuídos igualmente)
    n_features = len(feature_names)
    intercept_points = (offset + direction * factor * intercept) / n_features

    # Construir scorecard
    rows = []
    for i, feat in enumerate(feature_names):
        coef = coefs[i]
        woe_table = woe_tables[feat]
        required = {"faixa", "woe"}
        if not required.issubset(woe_table.columns):
            raise ValueError(f"woe table for {feat!r} must contain {sorted(required)}")
        woe_values = pd.to_numeric(woe_table["woe"], errors="coerce")
        if not np.isfinite(woe_values.to_numpy(dtype=float)).all():
            raise ValueError(f"woe table for {feat!r} must contain finite numeric woe values")

        for (_, row), woe in zip(woe_table.iterrows(), woe_values):
            points = intercept_points + direction * factor * coef * woe
            rows.append({
                "feature": feat,
                "faixa": row["faixa"],
                "woe": round(woe, 4),
                "coef": round(coef, 4),
                "pontos": round(points, 0),
                "event_is_bad": event_is_bad,
            })

    scorecard_df = pd.DataFrame(rows)
    return scorecard_df
