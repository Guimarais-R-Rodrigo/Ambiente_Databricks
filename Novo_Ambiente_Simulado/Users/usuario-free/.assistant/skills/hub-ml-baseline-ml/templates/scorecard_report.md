# Template: Relatório de Scorecard

> **[KS]** KS | **[Gini]** Gini | **[IV total]** IV | **[N vars]** variáveis selecionadas


## Uso
Estrutura do relatório de desenvolvimento de scorecard de crédito.

## Formato

```markdown
# Desenvolvimento de Scorecard — [Produto]

## 1. Objetivo
Desenvolver scorecard de [produto] para [decisão] com horizonte de [N] dias.

## 2. Amostra de desenvolvimento
| Item | Valor |
|---|---|
| Período | [dt_inicio] a [dt_fim] |
| Volume (total) | [N] contratos |
| Volume (bons) | [N] ([X]%) |
| Volume (maus) | [N] ([X]%) |
| Definição de mau | [critério: atraso > 90d, default, etc.] |

## 3. Seleção de variáveis

### Por Information Value
| Variável | IV | Classificação | Decisão |
|---|---|---|---|
| [var1] | [X] | Forte | Incluir |
| [var2] | [X] | Média | Incluir |
| [var3] | [X] | Fraca | Excluir |

### Variáveis selecionadas
[N] variáveis selecionadas por valor incremental, estabilidade e interpretação (de [M] candidatas)

## 4. Binning e WOE
[Tabela de bins por variável: faixa | N | %bom | %mau | WOE]

## 5. Modelo logístico
| Variável | Coeficiente | Exp(coef) | p-value | VIF |
|---|---|---|---|---|
| [var1] | [X] | [X] | [X] | [X] |

## 6. Scorecard (pontos)
| Variável | Faixa | Pontos |
|---|---|---|
| [var1] | [faixa_A] | [X] |
| [var1] | [faixa_B] | [X] |

Parametrização: PDO=[X], Base Score=[X], Base Odds=[X]:1

## 7. Performance
[Tabela de métricas: AUC, KS, Gini — dev vs val vs teste]

## 8. Score Bands
[Tabela: faixa | min | max | N | % base | % mau | taxa default | aprovação acum.]

## 9. Estabilidade (PSI)
PSI (dev vs val): [X] — [interpretação]

## 10. Conclusão e recomendação
[Modelo aprovado/reprovado + próximos passos]
```

---

#### 💼 Interpretação executiva

> "O scorecard utiliza [N] variáveis com IV total de [X]. O KS de [X]
> indica [boa/excelente] capacidade de separação. As faixas de score
> distribuem a base em [K] grupos com taxas de evento entre [min]% e [max]%."
