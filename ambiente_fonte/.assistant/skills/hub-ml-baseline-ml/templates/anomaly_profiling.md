# Template: Profiling de Anomalias

> **[N]** analisados | **[X]** anomalias ([Y]%) | **[threshold]** threshold | **[algoritmo]** método


## Uso
Documentar anomalias detectadas: scores, características e acionabilidade.

## Resumo da detecção

| Aspecto | Valor |
|---|---|
| Algoritmo | [Isolation Forest / Autoencoder / LOF] |
| N total analisado | [X] |
| Anomalias detectadas | [X] ([Y]%) |
| Threshold usado | [score / percentil] |
| Justificativa do threshold | [capacidade operacional / contaminação conhecida] |

## Distribuição de scores

```
Score distribution:
  Min:  [X.XX]
  P25:  [X.XX]
  P50:  [X.XX]
  P75:  [X.XX]
  P95:  [X.XX]  ← threshold candidato
  P99:  [X.XX]  ← threshold conservador
  Max:  [X.XX]

Threshold definido: [X.XX] (percentil [X]%)
```

## Top anomalias (amostra)

| Rank | ID | Score | Feature mais anômala | Desvio | Descrição |
|---|---|---|---|---|---|
| 1 | [id] | [X.XX] | [feature] | [X]σ | [breve descrição] |
| 2 | [id] | [X.XX] | [feature] | [X]σ | [breve descrição] |
| ... | ... | ... | ... | ... | ... |

## Padrões de anomalia

| Padrão | N | % anomalias | Características | Severidade |
|---|---|---|---|---|
| Tipo A: [nome] | [X] | [X]% | [descrição] | [Alta/Média/Baixa] |
| Tipo B: [nome] | [X] | [X]% | [descrição] | [Alta/Média/Baixa] |
| Isolados | [X] | [X]% | Sem padrão claro | Investigar |

## Features mais relevantes para anomalias

| Feature | Importância | Direção | Interpretação |
|---|---|---|---|
| [feature_1] | [X.XX] | Valores altos | [explicação] |
| [feature_2] | [X.XX] | Valores baixos | [explicação] |
| ... | ... | ... | ... |

## Métricas de qualidade (se houver labels)

| Métrica | Valor | Aceitável? |
|---|---|---|
| Precision@50 | [X]% | [✅ >60% / ❌] |
| Precision@100 | [X]% | [comparar à capacidade de revisão] |
| Recall | [X]% | [comparar ao custo de falso negativo] |
| AUC-PR | [X.XX] | [comparar à prevalência e benchmark] |
| False Positive Rate | [X]% | [comparar ao limite operacional] |

## Evolução temporal

| Período | N anomalias | % base | Tendência |
|---|---|---|---|
| [mês-1] | [X] | [X]% | — |
| [mês-2] | [X] | [X]% | [↑/↓/→] |
| [mês-3] | [X] | [X]% | [↑/↓/→] |

## Ações recomendadas

| Prioridade | Ação | Impacto | Responsável |
|---|---|---|---|
| 1 | [ação] | [alto/médio] | [área] |
| 2 | [ação] | [alto/médio] | [área] |
| 3 | [ação] | [médio/baixo] | [área] |

## Interpretação executiva

"Detectamos [N] anomalias ([X]% da base) usando [algoritmo].
As anomalias se concentram em [padrão principal], com [X]% relacionadas a
[tipo A]. Validação manual das top-50 indica precisão de [X]%.
Recomendamos [ação principal] para [impacto estimado]."
