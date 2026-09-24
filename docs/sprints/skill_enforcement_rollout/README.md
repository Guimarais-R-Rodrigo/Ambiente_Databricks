# Skill Enforcement Rollout — SER

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é sustentar o nível adequado por superfície, não transformar todas as skills em L4. A policy do produto continua sendo a fonte operacional dos níveis.

## Estado integrado e frente corrente

A SER00 foi aceita e integrada pela PR #101. A SER01 promoveu `hub-ml-criar-objeto` de L2 para L3, foi certificada por `SER-PROMOTION-CERT-2` e integrada pela PR #108; a `main` de entrada do B0 é `d2988e97e7b6c5fe1fd561852e947a155c2d731b`.

Em 2026-09-24 foi aceita a mudança operacional para execução paralela governada, formalizada pelo ADR-0023. Isso **não** renumera SER02–SER16, não altera targets e não autoriza promoções em lote. A ordem histórica permanece rastreável; o DAG passa a controlar execução e qualificação de componentes independentes antes da integração serial.

A frente corrente é o **B0 — mecanismo comum da execução paralela**. A candidata implementa contratos fechados, scheduler, launcher read-only, verificador, bundle RAW/SHARE, inventário de cobertura por método, dois pilotos sintéticos, qualificação de host e metatestes. Nenhuma campanha real de SER02–SER14 foi iniciada.

```text
SER00 = INTEGRATED
SER01 = INTEGRATED / CLOSED
B0 = AUDIT_CORRECTIVE_V3_FULL_CHECKOUT_PENDING
B0_TEST_METHODS_STATIC = 76
B0_AUTHORING_PREFLIGHT = NOT_RUN_ON_FINAL_SHA
B0_FULL_METATESTS_ON_CHECKOUT = NOT_RUN
B0_COVERAGE_V3_ON_CHECKOUT = NOT_RUN
B0_POLICY_CHANGE = NONE
SER02_TO_SER14 = NOT_STARTED_UNDER_PARALLEL_FRAMEWORK
SER15 = NOT_STARTED
SER16 = NOT_STARTED
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
PROMOCAO_TRABALHO = BLOQUEADA
```

## Navegação

- [Plano Mestre](PLANO_MESTRE.md)
- [Execução paralela governada](PARALELO/README.md)
- [B0: mecanismo comum](PARALELO/B0/README.md)
- [SER00: baseline e decisões](SER00/README.md)
- [SER01: histórico da primeira promoção](SER01/README.md)

ChatGPT conduz autoria e revisão repo-side. O executor local executa somente campanhas congeladas e comandos allowlisted; não redesenha solução, testes, critérios ou policy. Diagnóstico, certificação, prova externa, promoção e merge são estados distintos.
