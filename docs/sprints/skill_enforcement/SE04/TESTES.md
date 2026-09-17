# SE04 — testes e micro-evals

## Princípio

`task_correctness` e `canonical_compliance` permanecem dimensões independentes. Resultado manual correto não recebe Receipt retroativo.

## Suítes dedicadas

### `test_skill_enforcement_se04.py`

Cobre o contrato do Receipt isoladamente, incluindo:

- R01 válido;
- R02 manual sem Receipt;
- R03 direct helper sem Receipt;
- R05 Receipt adulterado;
- R06 output adulterado;
- R07 stale run;
- R08 wrong skill;
- R09 wrong release;
- R10 provenance conflict;
- R11 release integrity corrente falha;
- R12 primitive/fallback inválidos;
- R13 Receipt copiado para outro payload;
- R14 Receipt parcial/malformed;
- R15 versão desconhecida;
- R16 trace adulterado;
- R17 release anterior;
- R18 determinismo independente da ordem JSON;
- R19 agent-declared não substitui runtime-derived;
- ausência de payload de negócio no Receipt;
- ausência de evidência fabricada para import/template consumption.

### `test_skill_enforcement_se04_runner.py`

Cobre integração com o produto real:

- manifest protege o receipt engine e fingerprints batem;
- runner canônico emite Receipt V1;
- wrapper contra release corrente retorna `VALID`;
- tamper de Receipt → `INVALID`;
- tamper de output → `INCOMPATIBLE`;
- Receipt anterior contra run atual → `STALE_REPLAYED`;
- provenance conflict → `BLOCKED`, sem Receipt;
- primitive failure → `FAIL`, chamada mas não concluída, sem Receipt e sem fallback;
- output manual → `ABSENT`;
- `postflight.py` permanece ausente.

## Regressões SE01–SE03

O perfil oficial `se04` do certifier executa:

1. contrato v0.1;
2. SE01;
3. SE02;
4. SE03;
5. Receipt SE04;
6. runner SE04;
7. validação estrutural;
8. renderer;
9. render-diff incluindo arquivos untracked;
10. snapshot README.

Os antigos guards temporais de SE02/SE03 foram evoluídos apenas para reconhecer que SE04 agora existe. Eles continuam proibindo artefatos funcionais da SE05 e não reclassificam E01–E12 históricos.

## Evidência já observada fora do certifier oficial

Em harness isolado foram observados:

- 20/20 testes do contrato do Receipt: PASS;
- integração sintética runner → Receipt `1.0` → verifier `VALID`: PASS;
- alteração posterior do output → `INCOMPATIBLE`: PASS.

Essa evidência é útil para desenvolvimento, mas **não equivale a `LOCAL_CERTIFICATION=PASS`**, porque não executou a árvore completa, renderer, drift e snapshot.

## Databricks Free

`tools/skill_enforcement/se04_free_probe.py` cobre, com view temporária sintética:

- Receipt emitido e `VALID`;
- Receipt adulterado;
- output adulterado;
- stale Receipt;
- output manual sem Receipt;
- chamada direta a `quick_profile` sem Receipt;
- release integrity quebrada somente em fixture temporária;
- provenance conflict;
- primitive failure sem fallback;
- `published_package_mutated=false`;
- `persistent_writes_performed=false`.

Até existir execução real e JSON bruto preservado, `DATABRICKS_FREE` permanece `NOT_RUN`.

## Genie Code

A SE04 não repete comportamento estocástico como gate estrutural. O histórico da SE03 permanece:

```text
GENIE_BEHAVIORAL_SCREENING = MIXED
E02 = FAIL_OBSERVED
E12 = PASS_OBSERVED
```

## Release candidate

PR somente depois de observar no mesmo HEAD candidato:

- `LOCAL_CERTIFICATION=PASS`;
- `DERIVED_STALE=false`;
- regressões SE01–SE03 PASS;
- suítes SE04 PASS;
- `DATABRICKS_FREE=PASS` no alcance determinístico;
- documentação reconciliada;
- worktree limpa;
- nenhum artefato de SE05.
