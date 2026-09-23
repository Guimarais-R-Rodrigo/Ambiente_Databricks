# Skill Enforcement Rollout — SER

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é sustentar o nível adequado por superfície, não transformar todas as skills em L4. A policy do produto continua sendo a fonte operacional dos níveis.

## Estado integrado e frente corrente

A SER00 foi aceita e integrada pela PR #101 em `dedde0741ed4c387c3a500adfbf7de2c6166aba5`, após a certificação da candidata e as manutenções A07 #102/#105. A MM01 já compõe essa base. Os documentos históricos da candidata SER00 são preservados; seus estados de pending não desfazem o merge aceito.

A SER01 foi iniciada em 2026-09-23. O recorte A1 prepara a validação repo-side de pacotes em overlay e aguarda laboratório delegado. Não alterou `current_level=L2` de criar-objeto, `target_level=L3` ou `rollout_mode=audit`.

```text
SER00 = INTEGRATED
SER01 = IN_PROGRESS_A1_PREPARED_NOT_CERTIFIED
POLICY_PROMOTION = NOT_AUTHORIZED
SER02 = NOT_STARTED
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
PROMOCAO_TRABALHO = BLOQUEADA
```

## Navegação

- [Plano Mestre](PLANO_MESTRE.md)
- [SER00: baseline e decisões](SER00/README.md)
- [SER01: componente candidato e próximo gate](SER01/README.md)
- [Checkpoint SER01](SER01/CHECKPOINT.md)

ChatGPT conduz a implementação e a revisão. O agente Cloud executa somente a missão técnica delegada, sem redesenhar a solução. Aceite da arquitetura, certificação, promoção de policy, publicação e merge são decisões distintas.
