# Template: Interpretação de Análise de Sobrevivência

> **[N]** observações | **[Eventos]** ([X]%) | **[C-index]** concordância | **[Mediana]** sobrevivência


## Uso
Documentar resultados de survival analysis: curvas, hazard ratios e implicações.

## Visão geral do dataset

| Aspecto | Valor |
|---|---|
| N total | [X] |
| Eventos observados | [X] ([Y]%) |
| Censurados | [X] ([Y]%) |
| Tempo mediano de sobrevivência | [X] meses |
| Período de observação | [X] a [Y] meses |

## Kaplan-Meier (resultados globais)

| Tempo (meses) | S(t) — Sobrevivência | IC 95% inferior | IC 95% superior |
|---|---|---|---|
| 3 | [X]% | [X]% | [X]% |
| 6 | [X]% | [X]% | [X]% |
| 12 | [X]% | [X]% | [X]% |
| 24 | [X]% | [X]% | [X]% |

**Interpretação**: "Após [X] meses, [Y]% dos [entidades] ainda não experimentaram [evento]."

## Kaplan-Meier por segmento

| Segmento | Mediana sobrevivência | S(12) | Log-rank p-value |
|---|---|---|---|
| [Grupo A] | [X] meses | [X]% | ref |
| [Grupo B] | [X] meses | [X]% | [p] |
| [Grupo C] | [X] meses | [X]% | [p] |

## Cox PH — Hazard Ratios

| Feature | HR | IC 95% | p-value | Interpretação |
|---|---|---|---|---|
| [feature_1] | [X.XX] | [X.XX - X.XX] | [p] | [associação com hazard, condicionada ao modelo] |
| [feature_2] | [X.XX] | [X.XX - X.XX] | [p] | [associação com hazard, condicionada ao modelo] |
| ... | ... | ... | ... | ... |

**Leitura dos HRs**:
- HR > 1: associação com hazard maior, condicionada às covariáveis e à comparação declarada.
- HR < 1: associação com hazard menor, nas mesmas condições.
- HR = 1: estimativa pontual sem diferença no hazard; considerar IC e pressupostos.

HR não é razão de probabilidades acumuladas nem prova de proteção/efeito causal.
Declarar escala da feature, grupo de referência, censura e pressuposto de riscos proporcionais.

**Exemplo de redação, somente com resultado observado**: "No modelo ajustado, [feature]=1 está associado a hazard [X] vezes o de [feature]=0 (HR=[X], IC=[intervalo]); essa associação não demonstra efeito de intervenção."

## Validação do modelo

| Aspecto | Resultado | Aceitável? |
|---|---|---|
| C-index | [X.XX] | [benchmark, incerteza e critério do estudo] |
| Schoenfeld (proporcionalidade) | p global = [X.XX] | [alfa definido, diagnóstico gráfico e limitações; não prova isolada] |
| IBS (Integrated Brier Score) | [X.XX] | [horizonte, censura, baseline e critério do estudo] |
| Calibração visual | [OK / Desvio em t>X] | [✅/❌] |

## Risk groups

| Risk group | N | % evento | Mediana sobrevivência | Ação |
|---|---|---|---|---|
| [grupo/corte definido no estudo] | [N] | [X]% | [X] meses ou não atingida | [recomendação sujeita a política e aprovação próprias] |

## Interpretação executiva

"O modelo de sobrevivência indica que [target] tem mediana de [X] meses.
Os principais fatores de risco são [feature_1] (HR=[X]) e [feature_2] (HR=[X]).
Risco acumulado em [período], se estimado separadamente, é [valor/IC]. Qualquer intervenção é hipótese a avaliar e depende de autoridade própria; HR não permite preencher essa probabilidade."
