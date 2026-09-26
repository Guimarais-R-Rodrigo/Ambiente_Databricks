# SE04 — checkpoint técnico

## Natureza deste checkpoint

Este checkpoint registra o estado da SE04 depois da certificação local canônica e da homologação determinística no Databricks Free, mas antes da PR/CI final.

```text
certification_basis_head   = 9d7d09daaf943e857b468a21f6f774560c519f7e
documentation_basis_head   = 8f0f0b8f3c9c95a817a04db9b814b9d416f586c7
```

O primeiro SHA identifica exatamente o produto/testes certificados localmente e publicados no Databricks Free. O segundo contém somente reconciliação documental posterior dessas evidências. O commit que atualiza este próprio checkpoint é necessariamente posterior ao `documentation_basis_head`.

## Git

```text
branch      = sef/SE04-execution-receipt
base_main   = 216df1544c2b21a8ff94bb5ce51fd84b8a444057
merge_base  = 216df1544c2b21a8ff94bb5ce51fd84b8a444057
ahead_by    = 27 no documentation_basis_head
behind_by   = 0 no documentation_basis_head
PR          = NOT_OPENED
```

A branch permanece sem drift da `main` na direção de atraso (`behind_by=0`). Nenhum merge foi realizado.

## Estados de certificação

```text
LOCAL_CERTIFICATION        = PASS
LOCAL_SCOPE                = FULL_SE04_LOCAL
DATABRICKS_FREE            = PASS
GENIE_BEHAVIORAL_SCREENING = MIXED   # histórico SE03; não reclassificado
GITHUB_ACTIONS             = NOT_RUN
FULLY_CERTIFIED            = false

DERIVED_STALE              = false
worktree                    = CLEAN_OBSERVED_ON_CERTIFICATION_BASIS_HEAD
SE05                        = NOT_STARTED
```

`FULLY_CERTIFIED=false` permanece correto porque a PR ainda não foi aberta e o gate de GitHub Actions da candidata de release ainda não foi consumido.

## Certificação local oficial

No `certification_basis_head` foi executado:

```text
python -B tools/skill_enforcement/certify_local.py --profile se04 --verbose
```

Resultado final observado:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE04_LOCAL
DERIVED_STALE       = false
failures            = 0
```

Passaram no mesmo ciclo:

```text
contract_v0_1       = PASS
SE01 regression     = 14 tests PASS
SE02 regression     = 22 tests PASS
SE03 regression     = 22 tests PASS
SE04 Receipt        = 20 tests PASS
SE04 runner         = 9 tests PASS
assistant_structure = PASS
render_simulado     = PASS
render_diff         = PASS
readme_snapshot     = PASS
```

O renderer materializou `Novo_Ambiente_Simulado/` exclusivamente a partir de `ambiente_fonte/`; o gate `render_diff` observou ausência de drift rastreado ou não rastreado.

## Databricks Free

A publicação foi executada no workspace pessoal Free a partir do mesmo `certification_basis_head`.

Verificações observadas:

```text
publicação canônica      = PASS
verify rápido            = PASS (67/67 diretórios)
verify completo          = PASS
verify por conteúdo      = PASS
arquivos esperados       = 557
arquivos comparados      = 557/557
ausentes                 = 0
obsoletos                = 0
plataforma                = .assistant/.mcp_servers.json (gerenciado separadamente)
skills                    = 14/14
extensões hub_            = 5/5
```

O import individual do probe falhou por transporte com `PROTOCOL_ERROR` em três tentativas. O runbook prevê essa classe de falha; o fallback `workspace import-dir` foi executado com sucesso. Em seguida, o notebook remoto foi exportado e comparado ao arquivo local, com igualdade observada.

## SE04_FREE_PROBE_V1

Resultado global:

```text
marker                      = SE04_FREE_PROBE_V1
status                      = PASS
published_package_mutated   = false
persistent_writes_performed = false
```

Todos os nove casos executados retornaram `ok=true`.

| Caso | Resultado observado |
|---|---|
| R01 canonical receipt | `VALID`, canonical compliance `PASS` |
| R02/R04 manual sem Receipt | `ABSENT` |
| R03 direct primitive | `ABSENT` |
| R05 receipt adulterado | `INVALID` / `RECEIPT_ID_MISMATCH` |
| R06 output adulterado | `INCOMPATIBLE` / `UNDERLYING_EXECUTION_NOT_CANONICAL` |
| R07 stale/replay | `STALE_REPLAYED` / `RUN_ID_STALE` |
| R10 provenance conflict | `BLOCKED`, sem Receipt, `CONTEXT_PROVENANCE_CONFLICT` |
| R11 release integrity | `BLOCKED`, sem Receipt, `RELEASE_INTEGRITY_MISMATCH` em fixture temporária |
| R12 primitive failure | `FAIL`, sem Receipt, sem completion, `fallback_used=false` |

No caso R01, `numeric_columns=3` foi derivado do runtime Spark com `source=runtime_derived` e `conflict=false`.

## Estado funcional da SE04

```text
Receipt schema          = IMPLEMENTED (ExecutionReceiptV1 / 1.0)
Receipt emission        = IMPLEMENTED
Receipt verification    = IMPLEMENTED
canonical serialization = IMPLEMENTED
receipt_id              = er1:sha256(body)
tamper detection        = IMPLEMENTED_AND_FREE_OBSERVED
output binding          = IMPLEMENTED_AND_FREE_OBSERVED
trace binding           = IMPLEMENTED
input binding           = IMPLEMENTED
release binding         = IMPLEMENTED_AND_FREE_OBSERVED
contract binding        = IMPLEMENTED
runner binding          = IMPLEMENTED
replay/stale protection = IMPLEMENTED_CONTEXTUAL_AND_FREE_OBSERVED
provenance enforcement  = IMPLEMENTED_AND_FREE_OBSERVED
fallback protection     = IMPLEMENTED_AND_FREE_OBSERVED
postflight SE05         = NOT_STARTED
```

A proteção replay/stale continua deliberadamente contextual: exige o run atual conhecido (`expected_run_id`). A SE04 não alega anti-replay universal sem estado/nonce confiável externo.

## Threat model preservado

O contrato adversarial R01–R19 continua sendo a referência da sprint. O probe Free cobre o subconjunto executável necessário para homologação de runtime, enquanto a suíte local cobre os casos adicionais de wrong skill/release, malformed/unknown version, trace tamper, release anterior, determinismo JSON e provenance agent-declared.

A SE04 não transforma SHA-256 em autenticação criptográfica. Os hashes fornecem deterministic binding/tamper evidence dentro do trust boundary documentado.

## Produto publicado

Arquivos de produto relevantes da SE04:

```text
ambiente_fonte/.assistant/hub_scripts/skill_execution/README.md
ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt/__init__.py
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/release_manifest.json
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/run.py
```

O derivado correspondente foi materializado pelo renderer canônico e homologado sem drift.

## Estado da release candidate

Os bloqueios antigos de renderer, certifier local e Databricks Free estão encerrados.

Resta antes da PR:

1. recertificar localmente o HEAD documental final;
2. confirmar worktree limpa e `behind_by=0`;
3. congelar esse SHA como release candidate;
4. abrir a PR da SE04;
5. observar GitHub Actions uma única vez, evitando consumo iterativo desnecessário de créditos.

Depois da PR/CI, o merge continua proibido sem aceite humano explícito.

## Decisão de governança

A SE04 atingiu PASS local e PASS no Databricks Free. Ela ainda **não** é `FULLY_CERTIFIED` porque PR/CI permanecem pendentes. A SE05 continua `NOT_STARTED` e não deve ser iniciada nesta conversa antes do encerramento formal da SE04.
