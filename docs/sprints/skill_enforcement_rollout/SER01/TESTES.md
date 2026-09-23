# Skill Enforcement Rollout — SER

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é sustentar o nível adequado por superfície, não transformar todas as skills em L4. A policy do produto continua sendo a fonte operacional dos níveis.

## Estado integrado e frente corrente

A SER00 foi aceita e integrada pela PR #101 em `dedde0741ed4c387c3a500adfbf7de2c6166aba5`, após a certificação da candidata e as manutenções A07 #102/#105. A MM01 já compõe essa base. Os documentos históricos da candidata SER00 são preservados; seus estados de pending não desfazem o merge aceito.

A SER01 foi iniciada em 2026-09-23. A1 e A2 já foram certificadas no host Windows/NTFS no alcance documentado. A frente corrente é A3: certifier prospectivo SER com identidade própria e gate de record+Receipt, ainda sem alterar `current_level=L2`, `target_level=L3` ou `rollout_mode=audit`.

```text
SER00 = INTEGRATED
SER01 = IN_PROGRESS_A3_PREPARED_NOT_CERTIFIED
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

## A4 — evidência externa (2026-09-23)

`tools/skill_enforcement/ser01_free_probe.py` é notebook de probe externo e não faz parte do pacote `.assistant`. Ele testa release/contrato, verifier de Receipt no runtime Free, tamper/replay, claims fracos, policy ainda L2 e ausência de mutação do pacote publicado. Sua fixture positiva é explicitamente `INTEGRITY_ONLY_NOT_EXECUTION_PROOF`; ela não substitui a execução repo-side já provada na A3.

`A4_RUNBOOK_FREE.md` exige dry-run/publicação/verify rápido/completo/conteúdo e execução única do probe. `A4_GENIE_CASES.md` fixa cinco chats novos para rota indisponível, bypass, Receipt inválido, autoridade limitada e negativo de roteamento. Preservar respostas literais e separar task correctness, agent adherence e canonical compliance.

A4 não requer mudança em `ambiente_fonte`; qualquer delta em produto desde `fcec3e34...` bloqueia a execução e volta ao ChatGPT.
