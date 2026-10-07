# Template: Relatório de Scorecard

> **[KS]** KS | **[Gini]** Gini | **[IV por variável]** diagnóstico univariado | **[N vars]** variáveis selecionadas


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
| [variável] | [IV calculado no treino] | [interpretação contextual] | [decisão por ganho incremental, estabilidade, redundância e disponibilidade; evidência] |

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
[Recomendação técnica + evidência + limitações + próximos passos]
[Decisão humana: responsável, data, escopo e aprovação registrada ou NÃO INFORMADO]
[A recomendação não aprova o modelo nem clientes e não autoriza registro/deploy]
```

---

#### 💼 Interpretação executiva

> "O scorecard utiliza [N] variáveis selecionadas por [evidência incremental].
> IV é diagnóstico univariado: somá-lo entre features não mede informação
> conjunta independente. KS = [X] foi comparado com [benchmark/critério],
> com [incerteza]. As faixas têm taxas observadas [valores/período]."
