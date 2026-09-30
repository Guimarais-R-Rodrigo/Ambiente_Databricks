# Skill Enforcement Rollout — SER

A SER sucede operacionalmente o SEF, sem reabrir SE01–SE08. O objetivo é sustentar o nível adequado por superfície, não transformar todas as skills em L4. A policy do produto continua sendo a fonte operacional dos níveis.

## Estado integrado e frente corrente

SER00 e SER01 estão integradas. O B0 — mecanismo comum da execução paralela —
foi aceito e integrado pela PR #113 no merge
`4ba7f551767d847381df1556ed937116258fa77d`.

A frente corrente é a **B1 — skills executáveis**, agora em uma
[candidata isolada do controller](PR_B1_SKILLS_SEM_CONTROLLER_2026-09-30.md).
Ela reúne Safra, Explainability, Validação Estatística, Cross-EDA, Feature
Engineering, Baseline, Monitoramento e Pipeline Builder, com regressões
proporcionais e MM04 estática. O PR #115 e o #117 empilhado permanecem como
histórico em rascunho. O G6 R7 de #115 segue incompleto; as provas Free e Genie
da versão atual são avaliadas separadamente e nenhuma das skills recebeu
homologação integral nesta campanha.

```text
SER00 = INTEGRATED
SER01 = INTEGRATED / CLOSED
B0 = INTEGRATED / PR #113 / 4ba7f551...
B1_SKILLS = DRAFT / ACEITE_PARCIAL
B1_G6_R7_HISTORICO = INCOMPLETO
B1_FREE_ATUAL = PROBES_SINTETICOS_VERIFICADOS
B1_GENIE_ATUAL = PARCIAL
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
CI_NOVA_CANDIDATA = NOT_RUN
```

## Navegação

- [Plano Mestre](PLANO_MESTRE.md)
- [Execução paralela governada](PARALELO/README.md)
- [B0: mecanismo comum](PARALELO/B0/README.md)
- [SER00: baseline e decisões](SER00/README.md)
- [SER01: histórico da primeira promoção](SER01/README.md)
- [B1: pacote de skills sem controller](PR_B1_SKILLS_SEM_CONTROLLER_2026-09-30.md)

Diagnóstico, certificação, prova externa, promoção e merge permanecem estados
distintos. O conteúdo desta candidata não altera o controller nem substitui
os registros históricos de G6.
