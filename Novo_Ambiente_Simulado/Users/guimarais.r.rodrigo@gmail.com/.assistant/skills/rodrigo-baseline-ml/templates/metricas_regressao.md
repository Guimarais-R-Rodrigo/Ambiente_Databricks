# Template: Faixas de Métricas — Regressão

> **[RMSE]** RMSE | **[MAE]** MAE | **[R²]** R² | **[MAPE]** MAPE


## Uso
Referência de faixas de qualidade para métricas de regressão.

## Faixas por métrica

### RMSE (Root Mean Square Error)
- Interpretar em unidade do target (R$, unidades, %)
- Comparar SEMPRE com a média do target
- RMSE / mean(y) = coeficiente de variação do erro

### MAE (Mean Absolute Error)
- Mais robusto a outliers que RMSE
- Se MAE << RMSE → há outliers influenciando

### MAPE (Mean Absolute Percentage Error)
| Faixa | Qualidade |
|---|---|
| < 5% | 🌟 Excelente |
| 5 - 10% | ✅ Bom |
| 10 - 20% | 🟡 Aceitável |
| 20 - 50% | 🔴 Fraco |
| > 50% | ❌ Inútil |

### R² (Coeficiente de Determinação)
| Faixa | Qualidade | Contexto |
|---|---|---|
| < 0.3 | 🔴 | Modelo explica pouca variação |
| 0.3 - 0.5 | 🟡 | Aceitável para fenômenos complexos |
| 0.5 - 0.7 | ✅ | Bom para a maioria dos casos |
| 0.7 - 0.9 | 🌟 | Excelente |
| > 0.9 | ⚠️ | Verificar leakage ou overfitting |

## Armadilhas comuns

| Armadilha | Problema | Solução |
|---|---|---|
| MAPE com y ≈ 0 | Divisão por zero / valores infinitos | Usar SMAPE ou MAE |
| R² negativo | Modelo pior que a média | Bug ou features ruins |
| RMSE alto mas R² bom | Escala do target é grande | Normalizar para interpretar |

---

#### 💼 Interpretação executiva

> "O modelo erra em média R$ [MAE] por predição (MAE), com erro
> percentual médio de [MAPE]%. O R² de [X] indica que [X]% da
> variabilidade é explicada pelo modelo."
