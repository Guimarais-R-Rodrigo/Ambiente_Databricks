# SE04 — checkpoint técnico

## Natureza deste checkpoint

Este checkpoint registra o estado tecnicamente auditável da implementação antes dos gates finais de release candidate. Ele **não** declara a sprint certificada nem autoriza PR/merge.

`checkpoint_basis_head = f549e222d49ef54933b70fe172c6ec3ba0698ffc`

O commit que adiciona este próprio documento é posterior ao `checkpoint_basis_head`; o SHA de branch deve ser consultado diretamente no GitHub quando este arquivo for usado.

## Git

```text
branch      = sef/SE04-execution-receipt
base_main   = 216df1544c2b21a8ff94bb5ce51fd84b8a444057
merge_base  = 216df1544c2b21a8ff94bb5ce51fd84b8a444057
ahead_by    = 15 no checkpoint_basis_head
behind_by   = 0 no checkpoint_basis_head
PR          = NOT_OPENED
```

A branch nasceu diretamente da `main` real após confirmação da integração da SE03 pela PR #76.

## Estados de certificação

```text
LOCAL_CERTIFICATION        = NOT_RUN
DATABRICKS_FREE            = NOT_RUN
GENIE_BEHAVIORAL_SCREENING = MIXED   # histórico SE03; não reclassificado
GITHUB_ACTIONS             = NOT_RUN
FULLY_CERTIFIED            = false

DERIVED_STALE              = true
worktree                    = NOT_EVALUATED_NO_CHECKOUT
SE05                        = NOT_STARTED
```

`DERIVED_STALE=true` foi observado comparando o blob da fonte alterada com o derivado ainda materializado da SE03. Exemplo: o runner fonte está em `c102df83c8b58c3e9aadfb831c65a2d158f367d2`, enquanto o runner derivado permanece em `96682938898e7fbd48f32571b21046d3620a0f43`. O derivado não foi editado manualmente.

## Estado funcional da SE04

```text
Receipt schema          = IMPLEMENTED (ExecutionReceiptV1 / 1.0)
Receipt emission        = IMPLEMENTED
Receipt verification    = IMPLEMENTED
canonical serialization = IMPLEMENTED
receipt_id              = er1:sha256(body)
tamper detection        = IMPLEMENTED
output binding          = IMPLEMENTED
trace binding           = IMPLEMENTED
input binding           = IMPLEMENTED
release binding         = IMPLEMENTED
contract binding        = IMPLEMENTED
runner binding          = IMPLEMENTED
replay/stale protection = IMPLEMENTED_CONTEXTUAL
provenance enforcement  = IMPLEMENTED
fallback protection     = IMPLEMENTED
postflight SE05         = NOT_STARTED
```

A proteção replay/stale é deliberadamente contextual: exige `expected_run_id`/run atual conhecido. A SE04 não alega anti-replay universal sem estado/nonce confiável externo.

## Evidências observadas de desenvolvimento

Harness isolado do contrato do Receipt:

```text
20/20 tests = PASS_OBSERVED
```

Fixture sintética isolada de integração:

```text
runner status                 = PASS_OBSERVED
receipt_version               = 1.0
receipt verification          = VALID_OBSERVED
tampered output verification  = INCOMPATIBLE_OBSERVED
```

Essas evidências não substituem o certifier oficial porque o ambiente disponível nesta execução não possui checkout completo da árvore.

## Regressões oficiais

```text
SE01 regression = NOT_RUN no certifier final
SE02 regression = NOT_RUN no certifier final
SE03 regression = NOT_RUN no certifier final
SE04 tests      = PARTIAL_PASS_OBSERVED em harness isolado
```

Os guards temporais das regressões SE02/SE03 foram atualizados para reconhecer a existência legítima de `receipt.py` na SE04, mantendo `postflight.py` proibido. E01–E12 não foram reclassificados.

## Threat model

Classificação esperada codificada/testada:

| Caso | Classificação |
|---|---|
| R01 canonical receipt | `VALID` |
| R02 manual output | `ABSENT` |
| R03 direct helper | `ABSENT` |
| R04 receipt ausente | `ABSENT` |
| R05 receipt adulterado | `INVALID` |
| R06 output adulterado | `INCOMPATIBLE` |
| R07 receipt stale | `STALE_REPLAYED` |
| R08 wrong skill | `INCOMPATIBLE` |
| R09 wrong release/runner/contract | `INCOMPATIBLE` |
| R10 provenance conflict | emissão recusada / execução bloqueada |
| R11 release integrity quebrada | emissão recusada / execução bloqueada |
| R12 primitive failure/fallback | sem Receipt válido |
| R13 receipt copiado/output recriado | `INCOMPATIBLE` ou `STALE_REPLAYED` conforme contexto |
| R14 schema parcial | `MALFORMED` |
| R15 versão desconhecida | `UNSUPPORTED_VERSION` |
| R16 trace adulterado | `INCOMPATIBLE` |
| R17 receipt de release anterior | `INCOMPATIBLE` |
| R18 ordem JSON distinta | digest canônico estável |
| R19 agent-declared contra runtime-derived | emissão recusada |

## Commits até o checkpoint_basis_head

1. `30f85d02dfdaf68e4da00472ffd9b41a2cf82163` — bootstrap arquitetural;
2. `db414783cdbb375c2fd6c07c51b7d98725d9be6d` — engine Receipt V1;
3. `1a84c217d30362a1617b393736ecd8500e249607` — threat-model tests;
4. `255c735a33d0667cc8136144d2e110e835b10912` — emissão pelo runner;
5. `6c87a3251d7854e78cc9020e4beca93844a3428b` — receipt engine no manifest;
6. `281ad9399f7665ef75b890372def0c6a1258e47f` — integração runner/Receipt;
7. `399d03617f4b15a4082e2b89697a8fe942cdd882` — guard temporal SE02;
8. `a38ae38e7f65645123515ab5fe40ea3fb545aec1` — guard temporal SE03;
9. `1a9bfc3ca103a85c362b9d9b137046790f3dccb1` — perfil `se04` do certifier;
10. `cb857fd7bc3e81f9262f27368b23bedd79a2c779` — documentação operacional da skill;
11. `165fcf92366f4b4764d1ca6cb8f7ed338bdd7138` — fingerprint da skill;
12. `a3bf039305bbb1287a2993b6619a3d05f23d77c1` — probe Databricks Free;
13. `ce825227f09c0b6cdbbf790d172862e1e2a30351` — documentação SE04 consolidada;
14. `eb54fe6b6da337de474529e20c5a359541f035bd` — README do runtime `skill_execution`;
15. `f549e222d49ef54933b70fe172c6ec3ba0698ffc` — README das ferramentas/certifier.

## Arquivos do produto alterados

```text
ambiente_fonte/.assistant/hub_scripts/skill_execution/README.md
ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt.py
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/release_manifest.json
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/run.py
```

Testes/tooling/documentação correspondentes também foram adicionados/atualizados sob `tools/` e `docs/sprints/skill_enforcement/SE04/`.

## Bloqueios para release candidate

### B04-01 — derivado ainda stale

O renderer canônico requer checkout completo do repositório. O ambiente de execução desta conversa não fornece esse checkout; editar `Novo_Ambiente_Simulado/` por API equivaleria a materialização manual e violaria a governança.

Ação necessária no gate seguinte:

```powershell
python tools/render_simulado.py --write
```

Inspecionar exatamente o drift, versionar somente o derivado gerado e recertificar até `DERIVED_STALE=false`.

### B04-02 — certifier oficial ainda não executado

Sem checkout completo não foi possível executar:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se04
```

Portanto `LOCAL_CERTIFICATION` permanece `NOT_RUN`.

### B04-03 — Databricks Free não acessível nesta execução

O ambiente atual não possui Databricks CLI/configuração/autenticação. O probe e o runbook foram preparados, mas não executados. Portanto `DATABRICKS_FREE=NOT_RUN`.

## Decisão de governança neste checkpoint

A branch **não é release candidate**. Nenhuma PR foi aberta. GitHub Actions não foi consumido. Nenhum merge foi realizado. A SE05 continua `NOT_STARTED`.

O próximo avanço permitido é exclusivamente completar os gates faltantes da própria SE04: renderer → certifier oficial → Databricks Free → recertificação. Só depois disso a candidata pode abrir PR e observar Actions uma única vez.
