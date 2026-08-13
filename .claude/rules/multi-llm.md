# Regra — Trabalho multi-IA

Padrão herdado do ecossistema Verg (Verg_Alchemy_Hub): o papel importa mais que a
ferramenta.

## Hierarquia de contexto

- `CLAUDE.md` (raiz) é canônico. `AGENTS.md` (Codex/padrão aberto) e `GEMINI.md`
  são adaptadores finos que apontam para ele. Nunca crie sistema concorrente.
- Papéis usuais: Claude = implementação e governança local; Codex = auditoria de
  implementação/segunda opinião técnica; Gemini = pesquisa ampla e síntese.

## Obrigações de toda sessão que altera algo

1. Entrada no `CHANGELOG.md` (template `.claude/templates/changelog-entry.md`),
   com IA autora entre parênteses.
2. Preservar mudanças de outras IAs; conflito real → sinalizar, não sobrescrever.
3. Mudança estrutural (arquitetura, regra, decisão) → ADR e/ou handoff
   (`docs/handoffs/`, template `.claude/templates/handoff.md`).

## Auditorias formais

- Seguir o playbook do Hub (`../Verg_Alchemy_Hub/docs/playbooks/auditoria-multillm.md`):
  níveis `A0_light` (1 LLM) a `A3_incident` (3+), papéis independentes em níveis altos.
- Pasta padrão: `docs/auditoria/<YYYY-MM-DD>_<tema>/` com `01_contexto.md`,
  rodadas por IA e `99_consenso.md` (template `.claude/templates/auditoria.md`).
- Gatilhos mínimos de auditoria `A1+`: antes de compartilhar com a squad, antes de
  replicar mudança grande no trabalho, e quando duas IAs divergirem sobre a
  plataforma (aí a fonte oficial decide — `rules/genie-code-oficial.md`).
