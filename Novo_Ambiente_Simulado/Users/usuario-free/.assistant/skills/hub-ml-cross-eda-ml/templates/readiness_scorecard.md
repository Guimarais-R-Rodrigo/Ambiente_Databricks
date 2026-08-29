# Template: Scorecard de ML Readiness

> Recurso customizado. Pontuar somente com evidência e critérios aprovados. A média não substitui vetos de leakage, chave, representatividade ou governança.

## Scorecard

| Dimensão | Peso definido | Score (0–4) | Evidência | Bloqueador | Ação/owner/aceite |
|---|---:|---:|---|---|---|
| Unidade, entidade e chave | [X] | [X] | [unicidade, multiplicidade, overlap] | [sim/não] | [ação] |
| Alinhamento point-in-time | [X] | [X] | [event time, atraso, horizonte] | [sim/não] | [ação] |
| Cobertura e representatividade | [X] | [X] | [coverage por período/segmento] | [sim/não] | [ação] |
| Qualidade combinada | [X] | [X] | [nulos, domínios, conflitos, drift] | [sim/não] | [ação] |
| Sinal incremental | [X] | [X] | [comparação OOT com/sem fonte] | [sim/não] | [ação] |
| Target e avaliação | [X] | [X] | [definição, maturação, volume] | [sim/não] | [ação] |
| Governança e operação | [X] | [X] | [owner, permissões, SLA, linhagem] | [sim/não] | [ação] |

## Âncoras de pontuação

| Score | Definição |
|---:|---|
| 4 | Evidência completa, critério atendido e risco residual baixo/controlado |
| 3 | Adequado com limitação documentada e monitorável |
| 2 | Lacuna material mitigável, com owner e aceite definidos |
| 1 | Lacuna material sem mitigação comprovada |
| 0 | Contrato ausente, evidência inválida ou risco impeditivo |

## Vetos

Marcar `NO-GO` independentemente da média quando houver:

- unidade de predição ou chave indefinida;
- feature/registro conhecido somente depois da decisão;
- target ambíguo ou sem maturação suficiente;
- população sem representatividade para o uso;
- acesso/uso de dados não autorizado;
- join que altera a granularidade sem regra semântica.

## Decisão

| Resultado | Condição |
|---|---|
| GO | sem veto; dimensões atendem aos critérios aprovados |
| CONDICIONAL | sem veto imediato; lacunas têm owner, prazo e aceite antes do treino/promoção |
| NO-GO | ao menos um veto ou risco sem mitigação defensável |

## Resumo

> Decisão: **[GO/CONDICIONAL/NO-GO]**. Principais evidências: [itens]. Bloqueadores: [itens]. Próxima ação: [ação, owner, prazo, critério de aceite].
