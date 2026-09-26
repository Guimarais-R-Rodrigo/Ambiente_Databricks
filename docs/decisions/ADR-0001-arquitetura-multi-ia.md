# ADR-0001 — Arquitetura multi-IA com repositório canônico e camadas derivadas

Data: 2026-08-13
Status: Aceito
Autor: Claude (aprovado por Rodrigo)

## Contexto

O ecossistema `.assistant` do Genie Code do trabalho foi auditado e corrigido pelo
Codex (entrega congelada em `Ajustes_Codex/`). O projeto precisa: (1) evoluir esse
pacote com múltiplas IAs sem conflito; (2) testar no Databricks Free antes de
replicar no trabalho (onde não há CLI); (3) escalar de pessoal para squad/missão.
O usuário já pratica um padrão multi-IA maduro no ecossistema Verg
(`CLAUDE.md` canônico + adaptadores + `.claude/` + ADRs + changelog).

## Decisão

Adotar o padrão Verg neste repositório:

- `CLAUDE.md` canônico na raiz; `AGENTS.md` e `GEMINI.md` como adaptadores finos.
- `.claude/` como centro de IA: `rules/`, `context/`, `skills/`, `templates/`.
- `CHANGELOG.md` obrigatório com atribuição da IA autora; handoffs em
  `docs/handoffs/`; auditorias multi-LLM em `docs/auditoria/`.
- Separação de camadas: `ambiente_fonte/` (editável) → `Novo_Ambiente_Simulado/`
  (derivado por script, espelho da árvore do workspace) → workspaces Databricks
  (cópias operacionais). `Ajustes_Codex/` e `Ambiente_Antigo/` congelados.

## Alternativas consideradas

- Editar o pacote do Codex in-place — rejeitada: perde rastreabilidade do que
  mudou em relação à entrega auditada.
- Simulado como pasta editável — rejeitada: duas fontes de verdade geram drift;
  derivar por script garante que a cópia para o trabalho é mecânica.

## Consequências

- Toda mudança tem trilha: fonte → validação → render → changelog → publicação.
- Custo assumido: manter changelog e regenerar o simulado a cada mudança.

## Referências

- `README.md` (mapa e ciclo de vida), `.claude/rules/fonte-de-verdade.md`,
  padrão de origem em `../Verg_Projects/Verg_Alchemy_Hub/`.
