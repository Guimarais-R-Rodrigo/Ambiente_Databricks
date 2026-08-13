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
| [feature_1] | [X.XX] | [X.XX - X.XX] | [p] | [protege/risco] |
| [feature_2] | [X.XX] | [X.XX - X.XX] | [p] | [protege/risco] |
| ... | ... | ... | ... | ... |

**Leitura dos HRs**:
- HR > 1: feature **aumenta** o risco (acelera o evento)
- HR < 1: feature **protege** (retarda o evento)
- HR = 1: sem efeito

**Exemplo**: "Clientes com [feature] = 1 têm risco [X]x maior de [evento]
comparado com [feature] = 0 (HR = [X.XX], p = [X.XXX])."

## Validação do modelo

| Aspecto | Resultado | Aceitável? |
|---|---|---|
| C-index | [X.XX] | [✅ >0.7 / ❌ <0.7] |
| Schoenfeld (proporcionalidade) | p global = [X.XX] | [✅ >0.05 / ❌ <0.05] |
| IBS (Integrated Brier Score) | [X.XX] | [✅ <0.25 / ❌ >0.25] |
| Calibração visual | [OK / Desvio em t>X] | [✅/❌] |

## Risk groups

| Risk group | N | % evento | Mediana sobrevivência | Ação |
|---|---|---|---|---|
| Alto risco (score > p75) | [N] | [X]% | [X] meses | Intervenção imediata |
| Médio risco | [N] | [X]% | [X] meses | Monitoramento |
| Baixo risco (score < p25) | [N] | [X]% | [X] meses | Manter |

## Interpretação executiva

"O modelo de sobrevivência indica que [target] tem mediana de [X] meses.
Os principais fatores de risco são [feature_1] (HR=[X]) e [feature_2] (HR=[X]).
Clientes no grupo de alto risco têm [X]x mais chance de [evento] em [período],
sugerindo [ação] prioritária para esse segmento ([N] clientes, [Y]% da base)."
