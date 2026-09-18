# SE06 — checkpoint

## Base

```text
branch     = sef/SE06-evals
base_main  = 748b455d9b1a0d2f2e8878e65f27b2aabc675a0d
SE05       = CLOSED_AND_INTEGRATED
PR         = NOT_OPENED
```

## Escopo

SE06 mede o enforcement integrado. Não altera comportamento de `.assistant`.

## Implementado até aqui

```text
canonical_matrix_spec       = IMPLEMENTED
behavioral_runs_planned     = 25
deterministic_variants      = 12
scorer                      = IMPLEMENTED
structural_adversarial_test = IMPLEMENTED
certifier_profile_se06      = IMPLEMENTED
protocol_docs               = IMPLEMENTED
```

## Gates

```text
LOCAL_CERTIFICATION        = NOT_RUN
DATABRICKS_FREE_VERIFY     = NOT_RUN
GENIE_BEHAVIORAL_BENCHMARK= NOT_RUN
SE06_DOD                   = NOT_RUN
GITHUB_ACTIONS             = NOT_RUN
FULLY_CERTIFIED            = false
PR                         = NOT_OPENED
```

## Economia de CI

US$ 3 foram adicionados ao orçamento da frente.

Política:

- Actions zero durante desenvolvimento/coleta;
- PR somente após DOD e gates locais estabilizados;
- uma rodada de PR;
- zero rerun automático;
- merge só após aceite humano;
- pós-merge apenas a rodada automática de `push main`.

Referência observada na SE05:

- PR: ~25 min Linux;
- pós-merge: ~39 min Linux;
- consumo aproximado combinado: ~US$ 0,384 na referência de US$ 0,006/min.

## Próximos passos

1. executar gate local inicial SE06;
2. corrigir apenas defeitos do instrumento/scorer;
3. materializar snapshot se necessário;
4. `FULL_SE06_LOCAL=PASS`;
5. verify por conteúdo no Free;
6. gerar bundle externo;
7. executar 25 chats;
8. score final;
9. consolidar resultados;
10. RC/PR/Actions.

## Proibido antes da coleta

- alterar runtime SE05 para melhorar o benchmark;
- abrir PR;
- rodar Actions manualmente;
- publicar correção de comportamento no meio dos runs sem invalidar a rodada;
- iniciar generalização SE07.
