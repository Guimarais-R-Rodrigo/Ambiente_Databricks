# Regra — Trabalho multi-IA

Padrão herdado do ecossistema Verg (Verg_Alchemy_Hub): o papel importa mais que a
ferramenta.

## Hierarquia de contexto

- `CLAUDE.md` (raiz) é canônico. `AGENTS.md` (Codex/padrão aberto) e `GEMINI.md`
  são adaptadores finos que apontam para ele. Nunca crie sistema concorrente.
- Papéis são definidos pela sessão e pelo envelope, não pela marca do modelo. Claude,
  Codex ou outra IA podem implementar/auditar quando o contrato da frente permitir.
  O Codex possui três modos explícitos: reviewer, executor e
  `autonomous-controller`; o último segue o ADR-0024 e nunca amplia autoridade por
  inferência. Gemini continua útil para pesquisa ampla/síntese quando essa for a
  tarefa delegada.

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


## Codex Autonomous Controller

O modo autônomo é opt-in e governado pelo ADR-0024, por
`docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md` e por um envelope machine-readable.

Aprovar o modo não equivale a autorizar efeitos A2. A0/A1/A2/A3 são classes de
autoridade separadas. Subagentes não criam netos e só um agente pode escrever na
árvore por vez.


### Precedência e papéis

O ADR-0025 separa executor de autoria A1 de executor determinístico de campanha.
Restrições de campanha não bloqueiam repair repo-side dentro do envelope A1.
State source vivo prevalece sobre snapshots/runbooks históricos. Governança do
próprio controller exige `CONTROLLER_MAINTENANCE`.
