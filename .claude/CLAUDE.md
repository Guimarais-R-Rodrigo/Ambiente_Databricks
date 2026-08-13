# Índice operacional — .claude/

Leia este arquivo primeiro; depois carregue apenas o que a tarefa pedir.

## O que ler para cada tipo de tarefa

| Tarefa | Leia |
|---|---|
| Editar skills/instruções do produto | `rules/fonte-de-verdade.md`, `rules/genie-code-oficial.md`, depois `ambiente_fonte/` |
| Validar/publicar/replicar | `skills/validar-assistant/`, `skills/render-simulado/`, `rules/free-vs-trabalho.md` |
| Documentar (READMEs, relatórios) | `rules/docs-e-readmes.md` |
| Coordenar com outra IA / fechar sessão | `rules/multi-llm.md`, `templates/changelog-entry.md`, `templates/handoff.md` |
| Decisão arquitetural | `docs/decisions/` (ADRs) + `templates/adr.md` |
| Entender o usuário e os ambientes | `context/perfil-usuario.md`, `context/ambiente-trabalho.md`, `context/ambiente-free.md` |

## Estrutura

```text
.claude/
├── CLAUDE.md          # este índice
├── rules/             # regras duráveis (5 arquivos, uma responsabilidade cada)
├── context/           # fatos permanentes sobre usuário e ambientes
├── skills/            # playbooks executáveis deste repositório
│   ├── validar-assistant/   # roda tools/validate_assistant.py e interpreta
│   └── render-simulado/     # roda tools/render_simulado.py
└── templates/         # changelog, ADR, handoff, auditoria
```

Skills planejadas para as próximas fases (ver README raiz): `publicar-free`
(engine do Hub), `forward-test-skills`, `replicar-trabalho`,
`revisar-docs-oficiais`. Não invente que já existem.

## Convenções desta pasta

- Regras são curtas e imperativas; contexto é factual e estável.
- Uma regra que só vale para uma IA específica vai no adapter (`AGENTS.md`,
  `GEMINI.md`), não aqui.
- Ao criar/alterar regra ou skill, registre no `CHANGELOG.md`.
