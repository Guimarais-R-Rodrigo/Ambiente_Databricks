# Template: Estrutura do Notebook Baseline

## Uso
Estrutura sugerida para notebooks gerados com `@rodrigo-baseline-ml`.

## Estrutura

```markdown
# Baseline — [Contexto]

> **Suite**: [B1/B2/B3/B4/B5/B6/B7]
> **Modo**: [tabular/scorecard/temporal/dl/cluster/ranking/survival/anomaly]
> **Dataset**: [catalog.schema.tabela]
> **Target**: [coluna] (ou "nenhum" para B4/B7)
> **Split**: [temporal/estratificado/group/walk-forward]
> **Data**: [YYYY-MM-DD]
> **Autor**: [usuário]

---

## 1. Setup e Configuração
[Imports, seed=42, MLflow experiment, logging]

## 2. Carga e Validação
[Load dataset, validar schema, importar Context Card se disponível]

## 3. Preparação
[Split, encoding, nulos, scaling se necessário]
[Declarar: N_treino, N_val, N_teste, N_features]

## 4. Baseline Trivial
[Treinar baseline, métricas, registrar MLflow run tipo=trivial]

## 5. Modelo Principal
[Treinar modelo, otimização (se Optuna), early stopping]

## 6. Avaliação Comparativa

### 6.1 Tabela de métricas (dual-layer)

#### Para executivos:
| Indicador | Resultado | Interpretação |
|---|---|---|
| [métrica] | [valor] | [frase em linguagem natural] |

#### Para técnicos:
| Métrica | Treino | Validação | Teste | IC 95% | vs Trivial |
|---|---|---|---|---|---|
| [métrica] | [val] | [val] | [val] | [lower-upper] | +Δ |

### 6.2 Curvas diagnósticas
[ROC, PR, Lift, Calibration — com anotações]

## 7. Feature Importance
[Top-20: gain + permutation + SHAP summary]
[Narrativa: "As top-3 features explicam X% das decisões"]

## 8. Diagnóstico de Overfitting
[Gap treino-teste + semáforo + recomendação]

## 9. Relatório Executivo Final
[3 frases + semáforo + próximos passos]

## 10. Context Card (handoff)
[JSON de handoff para `@rodrigo-explainability`]
```
