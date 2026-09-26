# Skill Enforcement Rollout — SER

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é sustentar o nível adequado por superfície, não transformar todas as skills em L4. A policy do produto continua sendo a fonte operacional dos níveis.

## Estado integrado e frente corrente

SER00 e SER01 estão integradas. O B0 — mecanismo comum da execução paralela —
foi aceito e integrado pela PR #113 no merge
`4ba7f551767d847381df1556ed937116258fa77d`.

A frente real corrente é a **B1 — SER03 L3 + SER05 L2**, na PR #115
(`ser/B1-ser03-ser05-authoring`). G4 e G5 passaram. O G6 publicou o pacote R10
e passou o full-content verify, mas a tentativa dos probes terminou em estado
parcial: SER03 foi reportado criado/verificado e SER05 ausente após
`PROTOCOL_ERROR`. A recuperação residual SER05 está em autoria/qualificação;
Free probes, Genie, promoção, Ready e merge continuam pendentes conforme o state
source B1.

Em 2026-09-26 o ADR-0024 adicionou **Codex Autonomous Controller Mode** para
reduzir micro-handoffs. O envelope piloto B1 ativa A0/A1; A2 remoto continua
pendente de autorização humana específica.

```text
SER00 = INTEGRATED
SER01 = INTEGRATED / CLOSED
B0 = INTEGRATED / PR #113 / 4ba7f551...
B1 = ACTIVE / PR #115 / DRAFT
B1_G4_LOCAL = PASS
B1_G5_AUDIT = PASS
B1_G6 = FAIL_PARTIAL_RECOVERY_IN_PROGRESS
B1_AUTONOMY = ACTIVE_A0_A1
B1_A2_REMOTE = PENDING_EXPLICIT_ACTIVATION
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
```

## Navegação

- [Plano Mestre](PLANO_MESTRE.md)
- [Execução paralela governada](PARALELO/README.md)
- [B0: mecanismo comum](PARALELO/B0/README.md)
- [SER00: baseline e decisões](SER00/README.md)
- [SER01: histórico da primeira promoção](SER01/README.md)

Autoria/revisão repo-side pode ser conduzida por ChatGPT ou pelo Codex Autonomous Controller dentro do envelope ativo. O executor determinístico de campanha continua limitado a comandos congelados/allowlisted e não corrige a candidata durante uma certificação. Diagnóstico, certificação, prova externa, promoção e merge permanecem estados distintos.
