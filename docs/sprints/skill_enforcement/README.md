# Skill Enforcement Framework — índice vivo

Este diretório concentra o planejamento e as evidências do Skill Enforcement Framework (SEF).

## Política atual do produto

A [policy](../../../ambiente_databricks/.assistant/hub_padroes/skill_enforcement/policy.json) é a autoridade de níveis. Criar Objeto está L3/audit, `stage_specific`, após SER01; a menção L2 abaixo pertence à SE07. A [continuidade SER/B1](../skill_enforcement_rollout/README.md) separa capacidade técnica, comportamento e promoção. DoD incompleto e residual SE07 não foram apagados.

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
11. [SE05/README.md](SE05/README.md) — Postflight fail-closed L4, concluída e integrada pela PR #78 no merge `748b455d9b1a0d2f2e8878e65f27b2aabc675a0d`.
12. [SE05/DESENHO_TECNICO.md](SE05/DESENHO_TECNICO.md) — executor L4, evidence gaps, PostflightV1 e finalizer.
13. [SE05/TESTES.md](SE05/TESTES.md) — micro-evals, integração e critérios de aceite.
14. [SE06/README.md](SE06/README.md) — benchmark/adversarial ampliado, histórico encerrado na branch `sef/SE06-evals`.
15. [SE06/PROTOCOLO.md](SE06/PROTOCOLO.md) — coleta comportamental congelada e separação dos canais de evidência.
16. [SE06/METRICAS.md](SE06/METRICAS.md) — métricas, calibração e DoD computável.
17. [SE06/RUNBOOK_FREE.md](SE06/RUNBOOK_FREE.md) — execução dos 25 chats no laboratório Free.
18. [SE06/GUIA_USUARIO.md](SE06/GUIA_USUARIO.md) — operação para usuário não técnico.
19. [SE06/DECISAO_G2.md](SE06/DECISAO_G2.md) — fechamento deliberado em 24/25, `DOD=INCOMPLETE` preservado e exceção prospectiva de transição para SE07.
20. [SE07/README.md](SE07/README.md) — generalização por risco, registry 14/14 e política de migração por nível.
21. [SE08/README.md](SE08/README.md) — encerrada, certificada e integrada; operação permanente preservada e promoção ao trabalho bloqueada.
22. [SE08/RUNBOOK_LOCAL.md](SE08/RUNBOOK_LOCAL.md) — materialização do derivado e certificação local da candidata.

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

## Estado no fechamento SE08

- SE00: concluída e integrada;
- SE01: concluída e integrada;
- SE02: concluída e integrada pela PR #74;
- SE03: concluída e integrada pela PR #76;
- SE04: concluída e integrada pela PR #77;
- SE05: concluída e integrada pela PR #78; RC local/Free homologada, 12/12 workflows da PR e 18/18 workflows pós-merge em `success`;
- SE06: coleta comportamental encerrada por Gate G2 em 24/25; `S06-A1-R4=NOT_RUN`, structural suite `PASS`, thresholds primários observados satisfeitos e `DOD=INCOMPLETE` preservado;
- SE07: encerrada por decisão humana com residual conhecido; DoD de policy registry 14/14 satisfeito, `SE07_FULLY_CERTIFIED=false` pela falha aceita do oráculo sintético de resíduo; `hub-ml-criar-objeto` permanece L2 global e o piloto L3 não implica promoção global;
- SE08: encerrada, certificada e integrada; Windows/FULL, Actions e Databricks Free em PASS no alcance definido, `GENIE_BEHAVIORAL_SCREENING=NOT_APPLICABLE`, `SE08_FULLY_CERTIFIED=true`; promoção ao trabalho permanece bloqueada pelas dívidas herdadas.

A frente não deve declarar `FULLY_CERTIFIED` quando qualquer gate obrigatório estiver `NOT_RUN`, `BLOCKED` ou `DEFERRED_CREDIT`.

O Gate G2 preserva essa regra: a exceção SE06 → SE07 é de sequência, não de certificação.
