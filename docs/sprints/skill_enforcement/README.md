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
8. [SE04/README.md](SE04/README.md) — `ExecutionReceiptV1`, concluída e integrada pela PR #77 no merge `d74b2fcbf9accdf3878aa3aef9c0ec629a811028`.
9. [SE04/DESENHO_TECNICO.md](SE04/DESENHO_TECNICO.md) — schema, bindings e verifier do Receipt.
10. [SE04/THREAT_MODEL.md](SE04/THREAT_MODEL.md) — modelo de ameaça R01+.
11. [SE05/README.md](SE05/README.md) — Postflight fail-closed L4, sprint corrente na branch `sef/SE05-postflight-fail-closed`.
12. [SE05/DESENHO_TECNICO.md](SE05/DESENHO_TECNICO.md) — executor L4, evidence gaps, PostflightV1 e finalizer.
13. [SE05/TESTES.md](SE05/TESTES.md) — micro-evals, integração e critérios de aceite.
14. [SE05/RUNBOOK_FREE.md](SE05/RUNBOOK_FREE.md) — homologação determinística L4 no Databricks Free.
15. [SE05/GUIA_USUARIO.md](SE05/GUIA_USUARIO.md) — operação para usuário não técnico.

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

Na SE05, `run.py` permanece o core L3 histórico; `run_enforced.py` adiciona a coleta de evidência L4 e `postflight.py` é o único finalizador que pode autorizar `completion=COMPLETED` quando o Postflight estiver em `PASS`.

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
- SE04: concluída e integrada pela PR #77;
- SE05: em desenvolvimento branch-first; engine de Postflight, executor L4, finalizer, testes e probe Free presentes; gates completos local/Free ainda pendentes;
- SE06–SE08: não iniciadas.

A frente não deve declarar `FULLY_CERTIFIED` quando qualquer gate obrigatório estiver `NOT_RUN`, `BLOCKED` ou `DEFERRED_CREDIT`.
