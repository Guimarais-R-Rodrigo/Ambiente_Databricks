# Skill Enforcement Rollout — SER

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é sustentar o nível adequado por superfície, não transformar todas as skills em L4. A policy do produto continua sendo a fonte operacional dos níveis.

## Estado integrado e frente corrente

A SER00 foi aceita e integrada pela PR #101. A SER01 foi certificada, promovida para L3 e integrada pela PR #108; a `main` de entrada do B0 é `d2988e97e7b6c5fe1fd561852e947a155c2d731b`. Os estados intermediários e FAILs históricos da SER01 permanecem evidência datada e não são reclassificados.

Em 2026-09-24 o usuário aprovou substituir a espera estritamente sequencial por execução paralela governada. O ADR-0023 preserva os gates do ADR-0022, mas permite autoria e execução independentes conforme DAG explícito. A frente corrente é **B0 — infraestrutura comum de campanha paralela**. B0 não promove skills e não inicia SER02–SER14.

```text
SER00 = INTEGRATED
SER01 = INTEGRATED_L3
B0 = AUTHORING_CANDIDATE
SER02_TO_SER14 = NOT_STARTED
SER15 = NOT_STARTED
SER16 = NOT_STARTED
GITHUB_ACTIONS = DEFERRED_NO_CREDITS
PROMOCAO_TRABALHO = BLOQUEADA
```

## Navegação

- [Plano Mestre](PLANO_MESTRE.md)
- [SER00: baseline e decisões](SER00/README.md)
- [SER01: histórico da promoção integrada](SER01/README.md)
- [Checkpoint SER01](SER01/CHECKPOINT.md)
- [SER paralelo: plano detalhado e B0](PARALELO/README.md)

ChatGPT conduz a autoria repo-side e a revisão. No regime paralelo, agentes locais executam e auditam tarefas fechadas pelo manifesto; não redesenham implementação, testes ou critérios. Aceite da arquitetura, certificação, promoção de policy, publicação e merge continuam decisões distintas.
