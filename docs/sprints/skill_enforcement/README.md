# Skill Enforcement Framework — índice vivo

Este diretório concentra o planejamento e as evidências do Skill Enforcement Framework (SEF).

## Documentos canônicos

1. [PLANO_MESTRE.md](PLANO_MESTRE.md) — arquitetura e sequência original SE00–SE08.
2. [REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md](REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md) — revisão operacional vigente, com laboratório sintético, prioridade structural-first e regime local-first.
3. `SE00/` — baseline e instrumentos históricos.
4. `SE01/` — contrato verificável e capability experiment, concluída/integrada.
5. `SE02/` — preflight L2, concluída e integrada pela PR #74 no merge `0f1a8b18e8e7380aad75be096b0ce167e14f9662`.
6. `SE03/` — entrypoint estrutural L3 e governança de canonical compliance, integrada pela PR #76 no merge `216df1544c2b21a8ff94bb5ce51fd84b8a444057`.
7. [SE03/TESTES.md](SE03/TESTES.md) — histórico E01–E12, incluindo `GENIE_BEHAVIORAL_SCREENING=MIXED`.
8. [SE04/README.md](SE04/README.md) — `ExecutionReceiptV1`, iniciativa corrente na branch `sef/SE04-execution-receipt`.
9. [SE04/DESENHO_TECNICO.md](SE04/DESENHO_TECNICO.md) — schema, bindings e verifier.
10. [SE04/THREAT_MODEL.md](SE04/THREAT_MODEL.md) — modelo de ameaça R01+.
11. [SE04/TESTES.md](SE04/TESTES.md) — regressões e micro-evals.
12. [SE04/RUNBOOK_FREE.md](SE04/RUNBOOK_FREE.md) — homologação determinística no Databricks Free.

## Regra de leitura

O Plano Mestre original não é apagado para acomodar aprendizados posteriores. A revisão de 2026-09-17 é aditiva e governa os pontos operacionais alterados explicitamente, em especial:

- prioridade structural-first;
- distinção entre task correctness, agent adherence e canonical compliance;
- provenance runtime quando observável;
- certificação local-first;
- mesmo certifier Python para local/CI;
- GitHub Actions reservado para release candidate/Ready-for-review e pós-merge;
- branch sem PR durante desenvolvimento;
- estados separados para local, Databricks Free, comportamento conversacional e Actions.

A emenda pós-SE03 preserva `E02=FAIL_OBSERVED` e desloca a garantia forte de homologação para duas camadas distintas:

```text
SE04 = Receipt formal verificável
SE05 = postflight fail-closed da conclusão homologada
```

## Fluxo operacional

```text
branch sem PR
  → implementação
  → gate local
  → Databricks Free
  → release candidate
  → abrir PR
  → observar GitHub Actions uma vez
  → aceite humano
  → merge
  → certificação pós-merge
```

Uma PR Draft não deve ser usada como mecanismo de economia de CI, porque workflows transversais podem continuar reagindo a `pull_request/synchronize`.

## Estado atual

- SE00: concluída e integrada;
- SE01: concluída e integrada;
- SE02: concluída e integrada pela PR #74;
- SE03: concluída e integrada pela PR #76;
- SE04: em desenvolvimento branch-first; implementação funcional presente, gates oficial local/Free ainda não observados;
- SE05–SE08: não iniciadas.

A frente não deve declarar `FULLY_CERTIFIED` quando qualquer gate obrigatório estiver `NOT_RUN`, `BLOCKED` ou `DEFERRED_CREDIT`.
