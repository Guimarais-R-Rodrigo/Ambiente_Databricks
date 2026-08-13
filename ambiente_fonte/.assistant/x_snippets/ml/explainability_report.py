"""
Gerador de relatório de explicabilidade dual-layer (E1 executivo + E2 técnico).

Uso:
    from x_snippets.ml.explainability_report import generate_executive_report, generate_technical_summary

Autor: Rodrigo via assistente
Versão: 1.0
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional


def generate_executive_report(
    shap_importance: pd.DataFrame,
    feature_business_names: Dict[str, str],
    target_description: str,
    model_metric: float,
    metric_name: str = "AUC",
    shap_values: Optional[np.ndarray] = None,
    X: Optional[np.ndarray] = None,
    feature_names: Optional[List[str]] = None,
) -> str:
    """Gera relatório executivo (E1) em Markdown.

    Args:
        shap_importance: DataFrame de get_feature_importance_shap().
        feature_business_names: Dict {feature_técnica: nome_negócio}.
        target_description: Descrição do target em linguagem de negócio.
        model_metric: Valor da métrica principal.
        metric_name: Nome da métrica.
        shap_values: SHAP values (para direção do efeito).
        X: Features originais.
        feature_names: Nomes técnicos das features.

    Returns:
        String Markdown com relatório executivo.
    """
    required = {"feature", "pct_importance"}
    missing = required - set(shap_importance.columns)
    if missing:
        raise ValueError(f"shap_importance is missing columns: {sorted(missing)}")
    if shap_importance.empty:
        raise ValueError("shap_importance cannot be empty")
    top5 = shap_importance.head(5)

    # Determinar direção do efeito
    directions = []
    if shap_values is not None and X is not None and feature_names is not None:
        for feat in top5["feature"]:
            if feat not in feature_names:
                directions.append("—")
                continue
            feat_idx = feature_names.index(feat)
            # Correlação entre valor da feature e SHAP value
            corr = np.corrcoef(X[:, feat_idx], shap_values[:, feat_idx])[0, 1]
            if not np.isfinite(corr):
                directions.append("—")
            else:
                directions.append("↑ associação positiva" if corr > 0 else "↓ associação negativa")
    else:
        directions = ["—"] * len(top5)

    # Traduzir nomes
    report = f"""## Explicabilidade — Visão Executiva

**Modelo**: {metric_name} = {model_metric:.3f} | **Target**: {target_description}

### Principais fatores que influenciam {target_description}

| # | Fator | Impacto relativo | Direção |
|---|---|---|---|
"""
    for i, (_, row) in enumerate(top5.iterrows()):
        feat_name = feature_business_names.get(row["feature"], row["feature"])
        impact = "🔴 Alto" if row["pct_importance"] > 15 else ("🟡 Médio" if row["pct_importance"] > 8 else "🟢 Moderado")
        report += f"| {i+1} | {feat_name} | {impact} ({row['pct_importance']:.1f}%) | {directions[i]} |\n"

    report += f"""
### Interpretação

Os fatores acima concentram **{top5['pct_importance'].sum():.0f}%** da importância global média medida por |SHAP|.
O fator mais importante é **{feature_business_names.get(top5.iloc[0]['feature'], top5.iloc[0]['feature'])}**,
com {top5.iloc[0]['pct_importance']:.0f}% da importância global normalizada. Isso não representa percentual do poder preditivo nem causalidade.

### Confiança
- Métrica informada: {metric_name} = {model_metric:.3f}. Interprete-a segundo a definição da métrica, a amostra de avaliação e os intervalos de confiança; ela não é automaticamente “percentual de casos corretos”.
"""

    return report


def generate_technical_summary(
    shap_importance: pd.DataFrame,
    native_importance: Optional[pd.DataFrame] = None,
) -> str:
    """Gera resumo técnico (E2) com comparação SHAP vs native.

    Args:
        shap_importance: DataFrame de get_feature_importance_shap().
        native_importance: DataFrame com feature importance nativa (opcional).

    Returns:
        String Markdown com resumo técnico.
    """
    report = """## Explicabilidade — Resumo Técnico

### SHAP Feature Importance (Mean |SHAP|)

"""
    report += shap_importance.to_markdown(index=False) + "\n\n"

    if native_importance is not None:
        from scipy.stats import spearmanr
        # Merge e calcular correlação
        merged = shap_importance.merge(native_importance, on="feature", suffixes=("_shap", "_native"))
        if len(merged) >= 3:
            rho, pval = spearmanr(merged["rank_shap"], merged["rank_native"])
            report += f"### Consistência SHAP vs Native\n"
            report += f"- Spearman ρ = {rho:.3f} (p = {pval:.4f})\n"
            status = "✅ Consistente" if rho > 0.7 else ("⚠️ Divergente" if rho > 0.5 else "❌ Inconsistente")
            report += f"- Status: {status}\n"

    return report
