# SE04 — plano de testes

## Princípio

`task_correctness` e `receipt_validity/canonical_compliance` são dimensões independentes. Output matematicamente correto não recebe homologação canônica por equivalência de conteúdo.

## Suíte local SE04

A suíte dedicada deve cobrir pelo menos R01–R19 do threat model, incluindo:

- schema/versionamento;
- serialização canônica determinística;
- emissão somente em trace PASS;
- binding de trace/input/output/release;
- tamper de receipt;
- tamper de trace;
- output sobrescrito;
- stale/replay com `expected_run_id`;
- wrong skill;
- wrong release/runner/contract;
- provenance conflict;
- primitive failure;
- fallback;
- manual/direct helper sem receipt;
- campos faltantes/tipos errados;
- versão desconhecida;
- ausência de payload de negócio no receipt.

## Regressões

A certificação SE04 deve continuar executando:

- contrato v0.1;
- SE01;
- SE02;
- SE03;
- SE04;
- validação estrutural;
- renderer canônico;
- render-diff incluindo untracked;
- snapshot README.

Os guards históricos de SE02/SE03 que antes exigiam `receipt.py` ausente devem evoluir na SE04: passam a permitir o artefato da sprint corrente, mas continuam proibindo `postflight.py` e qualquer artefato funcional de SE05.

## Estados do verifier

```text
VALID
ABSENT
MALFORMED
INVALID
INCOMPATIBLE
STALE_REPLAYED
UNSUPPORTED_VERSION
```

Nenhum estado diferente de `VALID` implica canonical compliance.

## Databricks Free

Probe SE04 deverá usar somente dados sintéticos e demonstrar:

1. receipt emitido e `VALID`;
2. output adulterado;
3. receipt adulterado;
4. stale receipt;
5. output manual sem receipt;
6. chamada direta à primitive sem receipt;
7. release integrity quebrada;
8. provenance conflict;
9. primitive failure sem fallback;
10. `published_package_mutated=false`;
11. `persistent_writes_performed=false`.

Screening conversacional do Genie Code não é gate estrutural da SE04. Se repetido, permanece em `GENIE_BEHAVIORAL_SCREENING`, sem reclassificar E02 histórico.

## Release candidate

A candidata só pode abrir PR depois de:

- `LOCAL_CERTIFICATION=PASS` no HEAD exato;
- `DATABRICKS_FREE=PASS` no alcance determinístico SE04;
- derivado sem drift;
- documentação completa;
- worktree limpa;
- nenhum postflight SE05 presente.
