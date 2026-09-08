# Template: Faixas de Métricas — Séries Temporais

> **[MAPE]** MAPE | **[MASE]** MASE | **[RMSE]** RMSE | **[Coverage]** cobertura IC


## Uso
Referência de faixas de qualidade para métricas de previsão temporal.

## Faixas por métrica

### MAPE (Mean Absolute Percentage Error)
| Faixa | Qualidade | Ação |
|---|---|---|
| < 5% | 🌟 Excelente | Modelo pronto para produção |
| 5 - 10% | ✅ Bom | Adequado para decisão |
| 10 - 20% | 🟡 Aceitável | Uso direcional (não para SLA rígido) |
| 20 - 50% | 🔴 Fraco | Revisar features / modelo |
| > 50% | ❌ Inútil | Descartar |

**Armadilhas**:
- MAPE é indefinido quando y=0 → usar SMAPE ou MAE nesses casos
- MAPE é assimétrico (penaliza mais subestimação) → considerar SMAPE
- MAPE em séries com valores pequenos pode ser artificialmente alto

### SMAPE (Symmetric MAPE)
- Mesmas faixas que MAPE
- Vantagem: simétrico e limitado (0 a 200%)
- Desvantagem: pode esconder erros grandes em séries com valores altos

### MASE (Mean Absolute Scaled Error)
| Faixa | Qualidade | Interpretação |
|---|---|---|
| < 0.5 | 🌟 Excelente | 2x melhor que naive sazonal |
| 0.5 - 0.8 | ✅ Bom | Claramente superior ao naive |
| 0.8 - 1.0 | 🟡 Marginal | Apenas levemente melhor |
| ≥ 1.0 | 🔴 FALHA | Modelo NÃO supera naive → descartar |

**Regra**: MASE é a métrica mais importante em séries temporais.
Se MASE ≥ 1.0, o modelo é INÚTIL (usar naive é melhor).

### Coverage (% dentro do intervalo de confiança)
| IC nominal | Coverage esperada | Aceitável | Problema |
|---|---|---|---|
| 80% | ~80% | 75-85% | < 70% = IC estreito demais |
| 95% | ~95% | 90-97% | < 85% = modelo subestima incerteza |

**Armadilha**: Coverage alta + IC muito largo = modelo sem valor
(prever "entre 0 e infinito" tem 100% de coverage mas é inútil).

## Tabela comparativa (template)

| Modelo | MAPE | SMAPE | MASE | RMSE | Coverage 95% | Decisão |
|---|---|---|---|---|---|---|
| Naive sazonal | [X]% | [X]% | 1.00 (ref) | [X] | — | Baseline |
| Prophet | [X]% | [X]% | [X] | [X] | [X]% | [✅/❌] |
| ARIMA | [X]% | [X]% | [X] | [X] | [X]% | [✅/❌] |
| LightGBM temporal | [X]% | [X]% | [X] | [X] | — | [✅/❌] |

## Interpretação executiva (template)

"O modelo [algoritmo] prevê [target] com erro médio de [MAPE]%,
o que é [X]x melhor que simplesmente repetir o valor do ano passado (MASE=[X]).
Para os próximos [N] meses, esperamos que o valor real esteja dentro da
faixa prevista em [Coverage]% dos casos."
