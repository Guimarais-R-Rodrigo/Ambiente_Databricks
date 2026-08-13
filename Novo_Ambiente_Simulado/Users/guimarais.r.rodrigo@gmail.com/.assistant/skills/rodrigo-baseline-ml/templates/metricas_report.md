# Template: Relatório de Métricas

> **[Métrica principal]** valor | **[N train]** treino | **[N test]** teste | **[Gap]** train-test


## Uso
Tabela padronizada de métricas por tipo de problema. Inclui camada executiva e técnica.

## Classificação Binária

### Camada executiva
| O que mede | Resultado | Qualidade | Em linguagem simples |
|---|---|---|---|
| Ordenação de risco | AUC = [X] | [✅/🟡/🔴] | "Em pares positivo-negativo, ordena o positivo acima do negativo em aproximadamente [X]%" |
| Separação bons/maus | KS = [X] | [✅/🟡/🔴] | "Separa os grupos em [X] pontos" |
| Ganho no top-10% | Lift = [X]x | [✅/🟡/🔴] | "Top 10% concentra [X]x mais eventos" |
| Calibração | Brier = [X] | [✅/🟡/🔴] | "Probabilidades [confiáveis/razoáveis/ruins]" |

### Camada técnica
| Métrica | Treino | Val | Teste | IC 95% | Faixa ref. | Gap T-Te |
|---|---|---|---|---|---|---|
| AUC-ROC | [X] | [X] | [X] | [[lo]-[hi]] | [benchmark aprovado] | [X]% |
| AUC-PR | [X] | [X] | [X] | [[lo]-[hi]] | > prevalência | [X]% |
| KS | [X] | [X] | [X] | — | [benchmark aprovado] | [X]% |
| Gini | [X] | [X] | [X] | — | [benchmark aprovado] | [X]% |
| Lift@10% | — | — | [X] | — | [benchmark aprovado] | — |
| Brier Score | [X] | [X] | [X] | — | [benchmark/calibração] | — |
| F1 (threshold=[decisão]) | [X] | [X] | [X] | — | [benchmark aprovado] | — |

### Camada comparativa
| Métrica | Baseline trivial | Modelo | Δ absoluto | Δ relativo | Significativo? |
|---|---|---|---|---|---|
| AUC | [X] | [X] | +[X] | +[X]% | [✅/❌] |
| KS | [X] | [X] | +[X] | — | [✅/❌] |

## Regressão

### Camada executiva
| O que mede | Resultado | Qualidade | Em linguagem simples |
|---|---|---|---|
| Erro típico | RMSE = [X] | [✅/🟡/🔴] | "Erra em média R$ [X] para cima ou baixo" |
| Erro percentual | MAPE = [X]% | [✅/🟡/🔴] | "Erra [X]% em média" |
| Variância explicada | R² = [X] | [✅/🟡/🔴] | "Explica [X]% da variação" |

## Critérios de aceite

Preencher com benchmark histórico, baseline trivial, custo dos erros e política aprovada. Não usar faixas universais para classificar AUC, KS, Gini, Lift, MAPE ou R².
