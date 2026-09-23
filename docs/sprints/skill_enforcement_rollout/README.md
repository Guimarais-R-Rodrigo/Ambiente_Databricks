# Skill Enforcement Rollout — SER

Regime: `LOCAL_FIRST`. Baseline auditada: `11851e137dd7793b351ac08fc211c0be90005dee`. Main reconciliada após as manutenções A07 e a integração MM01: `73d7659dcf11509a7fba392221c4810d10401c35`. Data de reconciliação: 2026-09-23.

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é implementar o nível adequado por superfície, não obter L4 em todas as skills.

```text
SER00 = SER00_NOT_READY_FINAL_LOCAL_CERTIFICATION
PLAN_FREEZE = ACCEPTED
A07_MAINTENANCE = INTEGRATED
SER01 = NOT_STARTED
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
PROMOCAO_TRABALHO = BLOQUEADA
```

O inventário confirma 14 skills, cinco no target e nove abaixo. Current e target não foram alterados. As decisões A01–A03 foram aceitas em 2026-09-22. As manutenções #102 e #105 foram certificadas localmente e integradas; a #105 acrescentou `FILE_SHARE_DELETE` aos streams temporários Win32, com teste causal, stress 30/30, CI 10/10 e FULL 21/21. A MM01 também foi integrada em `73d7659d...` após reconciliação com #105. A SER00 agora depende somente da certificação local SHA-bound de sua candidata documental reconciliada antes de revisão/merge.

## Navegação

- [Plano Mestre](PLANO_MESTRE.md)
- [SER00 e seus entregáveis](SER00/README.md)
- [Decisões arquiteturais aceitas e limites](SER00/DESENHO_TECNICO.md)
- [Checkpoint](SER00/CHECKPOINT.md)

A PR permanece draft. O aceite de A01–A03 e os merges das manutenções #102/#105 não autorizam merge da SER00, promoção de policy, publicação Free ou início da SER01. Não houve autorização corporativa. A decisão arquitetural transversal está no ADR-0022; o próximo gate é uma única certificação local final no SHA documental reconciliado.
