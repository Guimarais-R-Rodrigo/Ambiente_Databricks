# SE04 — evidências de certificação e homologação

## Escopo

Este documento consolida as evidências observadas da SE04 até a formação da candidata de release. Ele distingue evidência de desenvolvimento, certificação local canônica e homologação determinística no Databricks Free.

Base funcional homologada:

```text
9d7d09daaf943e857b468a21f6f774560c519f7e
```

## 1. Evidências de desenvolvimento

Durante a construção da SE04 foram executados harnesses isolados dos novos componentes.

Resultados observados:

```text
Receipt unit harness      = 20/20 PASS
Runner synthetic fixture  = PASS
Receipt verification      = VALID
Tampered output           = INCOMPATIBLE
```

A suíte unitária cobriu contrato V1, tampering, bindings, stale/replay contextual, wrong skill/release, provenance, failure/fallback, malformed/unknown version, determinismo e ausência de payload de negócio.

## 2. Certificação local oficial

No HEAD `9d7d09daaf943e857b468a21f6f774560c519f7e`, o certifier canônico foi executado em checkout completo e worktree limpa.

Resultado final:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE04_LOCAL
DERIVED_STALE       = false
failures            = 0
```

O perfil executou e aprovou:

```text
contract_v0_1
se01_regression
se02_regression
se03_regression
se04_receipt_tests
se04_runner_tests
assistant_structure
render_simulado
render_diff
readme_snapshot
```

Contagens diretamente relevantes:

```text
SE01 regression = 14 tests PASS
SE02 regression = 22 tests PASS
SE03 regression = 22 tests PASS
SE04 Receipt    = 20 tests PASS
SE04 runner     = 9 tests PASS
assistant       = APROVADO: 0 falha(s), 0 aviso(s)
derived drift   = 0
README snapshot = APROVADO: 0 falha(s), 0 aviso(s)
```

O evidence bundle local foi gravado sob `~/.ambiente_databricks/sef_certifications/20260917T214515Z_9d7d09daaf94`.

## 3. Publicação e verify no Databricks Free

A publicação foi feita no workspace pessoal configurado pelo profile `FREE`, usando o mesmo HEAD funcional certificado.

Resultado observado:

```text
publicação               = PASS
verify rápido            = PASS
verify completo          = PASS
verify por conteúdo      = PASS
arquivos esperados       = 557
arquivos comparados      = 557/557
ausentes                 = 0
obsoletos                = 0
arquivo de plataforma    = .assistant/.mcp_servers.json
skills                   = 14/14
extensões hub_           = 5/5
```

O relatório por conteúdo foi preservado como `se04_free_verify_9d7d09daaf94.json` no diretório local de certificações.

## 4. Transporte do probe

O endpoint individual `workspace/import` apresentou `PROTOCOL_ERROR` em três tentativas. Esse evento foi tratado como falha de transporte, não como falha funcional.

O fallback previsto no runbook foi usado:

```text
workspace import-dir = PASS
remote object        = NOTEBOOK
remote/local compare = PASS
```

O notebook remoto `SE04_Free_Probe` foi exportado e comparado ao arquivo local antes da execução.

## 5. Resultado do SE04_FREE_PROBE_V1

Saída global observada:

```text
marker                      = SE04_FREE_PROBE_V1
status                      = PASS
published_package_mutated   = false
persistent_writes_performed = false
```

Todos os casos executados retornaram `ok=true`.

| Caso | Evidência observada |
|---|---|
| R01 | `PASS`, preflight `PASS`, `quick_profile` chamada/concluída, Receipt `1.0`, verifier `VALID`, canonical compliance `PASS` |
| R02/R04 | output manual sem Receipt classificado como `ABSENT` |
| R03 | chamada direta da primitive sem Receipt classificada como `ABSENT` |
| R05 | Receipt adulterado classificado como `INVALID` por `RECEIPT_ID_MISMATCH` |
| R06 | output adulterado classificado como `INCOMPATIBLE` por execução subjacente não canônica |
| R07 | Receipt de run anterior classificado como `STALE_REPLAYED` por `RUN_ID_STALE` |
| R10 | conflito `numeric_columns` bloqueado antes do preflight/core; provenance `runtime_derived`, `conflict=true`, sem Receipt |
| R11 | fingerprint do receipt engine adulterado em fixture temporária; `BLOCKED`, sem Receipt, `RELEASE_INTEGRITY_MISMATCH` |
| R12 | falha deliberada de `quick_profile`; `FAIL`, sem Receipt, sem completion e `fallback_used=false` |

No happy path, `numeric_columns=3` foi derivado de `spark.table(...).dtypes`, com `conflict=false`.

## 6. Classificação

Com as evidências acima:

```text
LOCAL_CERTIFICATION = PASS
DATABRICKS_FREE      = PASS
DERIVED_STALE        = false
```

`GENIE_BEHAVIORAL_SCREENING=MIXED` permanece a classificação histórica da SE03 e não foi reclassificada pela SE04.

`GITHUB_ACTIONS` ainda não foi executado para esta branch e `FULLY_CERTIFIED` permanece `false` até o gate de PR/CI previsto. A SE05 continua `NOT_STARTED`.
