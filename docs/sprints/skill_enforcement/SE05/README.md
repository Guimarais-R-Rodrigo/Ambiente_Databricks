# SE05 — Postflight fail-closed

> **Nota administrativa — 06/10/2026.** SE05 integrada pela PR #78 em `748b455d`. As pendências de abertura de PR, certificação e merge abaixo descrevem candidatas anteriores. [História SEF](../README.md) e [operação atual SER](../../skill_enforcement_rollout/README.md) distinguem o fechamento histórico da policy vigente. Esta nota não reclassifica resultados nem amplia o escopo certificado.

## Registro histórico preservado

## Estado

**IMPLEMENTAÇÃO FUNCIONAL HOMOLOGADA LOCALMENTE E NO DATABRICKS FREE; release candidate documental em preparação.**

Branch: `sef/SE05-postflight-fail-closed`  
Baseline: `main@d74b2fcbf9accdf3878aa3aef9c0ec629a811028`  
Skill piloto: `hub-ml-eda-profissional`  
Contrato: v0.1, `mode="audit"`, com `metadata.postflight.policy="fail_closed"`.

## Objetivo

A SE05 eleva o piloto para L4: uma execução só pode ser apresentada como **concluída com aderência ao contrato** depois de um Postflight `PASS`.

A regra operacional é simples:

```text
postflight != PASS
    → completion.authorized = false
    → completion.status = NOT_COMPLETED
```

O postflight não julga se a análise de negócio está “boa”. Ele julga se há evidência suficiente de que a rota canônica e os requisitos materiais aplicáveis foram satisfeitos.

## Arquitetura

A SE05 preserva o core L3 da SE04 e adiciona uma rota L4:

```text
run.py::run
  → ExecutionTraceV0
  → run_enforced.py::run_enforced
      → imports/calls/completions
      → templates_loaded + digests
      → artifacts + evidence_gaps
  → ExecutionReceiptV1
  → verify_receipt
  → postflight.py::finalize
  → PostflightV1
  → completion
```

Isso evita reescrever o core já homologado e mantém E01–E12/R01–R19 comparáveis.

## O que o Postflight valida

- Receipt `VALID` contra a release corrente;
- skill e run vinculados;
- uso da rota L4 canônica;
- recursos `required`;
- recursos `conditional` quando aplicáveis;
- justificativa de skips condicionais;
- templates aplicáveis efetivamente carregados e com digest;
- artifacts vinculados ao trace;
- handoff mínimo definido no contrato;
- consistência do claim final de completion.

Estados:

```text
PASS     = conclusão pode ser homologada
FAIL     = requisito material aplicável não foi satisfeito
BLOCKED  = evidência/configuração insuficiente ou inconsistente
REVIEW   = não é seguro homologar automaticamente; requer revisão
```

Somente `PASS` autoriza conclusão.

## Decisão importante: L3 continua existindo

`run.py` permanece como core L3 histórico e continua podendo produzir Receipt válido da execução protegida pela SE04. Isso não equivale a conclusão L4.

Para uma entrega declarada como concluída com aderência ao contrato, a skill passa a exigir:

1. `scripts/run_enforced.py`;
2. handoff estruturado;
3. `scripts/postflight.py`;
4. `completion.authorized=true` somente após Postflight `PASS`.

## Evidência já observada

No desenvolvimento inicial:

```text
postflight unit/micro-evals = 15/15 PASS
integração L4               = 7/7 PASS
contrato                    = PASS
regressões SE01–SE04        = PASS no certifier parcial
```

No HEAD funcional `0d4d6af630d2760c754313218f51cff0d6ad2375`, o certifier completo fechou `LOCAL_CERTIFICATION=PASS`, `scope=FULL_SE05_LOCAL`, `DERIVED_STALE=false` e `failures=0`. O renderer materializou 561 arquivos e o snapshot README passou.

## Databricks Free

O gate Free foi executado e aprovado no HEAD funcional `0d4d6af630d2760c754313218f51cff0d6ad2375`. Publicação, verify rápido, verify completo e verify por conteúdo passaram; 560/560 arquivos controlados foram comparados sem ausentes ou obsoletos. O probe `tools/skill_enforcement/se05_free_probe.py` usa apenas view sintética temporária e cobre:

- happy path L4 autorizado;
- core L3 isolado sem autorização L4;
- input obrigatório ausente;
- handoff incompleto;
- adulteração do claim de completion;
- nenhuma escrita persistente;
- nenhuma mutação do pacote publicado.

Resultado global: `SE05_FREE_PROBE_V1 = PASS`, `published_package_mutated=false` e `persistent_writes_performed=false`.

Consulte [RUNBOOK_FREE.md](RUNBOOK_FREE.md) e [EVIDENCIAS.md](EVIDENCIAS.md).

## Fora do escopo

- generalizar L4 para as 14 skills;
- mudar o contrato inteiro para `mode="enforce"`;
- declarar qualidade analítica/estatística com base apenas no postflight;
- HMAC/PKI/attestation externa;
- promover ao workspace corporativo;
- benchmark conversacional amplo da SE06.

## Documentos

- [DESENHO_TECNICO.md](DESENHO_TECNICO.md)
- [TESTES.md](TESTES.md)
- [RUNBOOK_FREE.md](RUNBOOK_FREE.md)
- [GUIA_USUARIO.md](GUIA_USUARIO.md)
- [EVIDENCIAS.md](EVIDENCIAS.md)
- [CHECKPOINT.md](CHECKPOINT.md)
