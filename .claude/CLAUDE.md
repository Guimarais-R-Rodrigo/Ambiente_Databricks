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
├── skills/            # playbooks executáveis deste repositório (5 ativas)
│   ├── validar-assistant/   # roda tools/validate_assistant.py e interpreta
│   ├── render-simulado/     # roda tools/render_simulado.py
│   ├── publicar-free/       # roda tools/publicar_free.py (plano/execute/verify)
│   ├── forward-test-skills/ # roteiro de teste de roteamento das skills
│   └── replicar-trabalho/   # pré-requisitos e guardrails da cópia manual
└── templates/         # changelog, ADR, handoff, auditoria
```

O inventário com status de cada uma está em `skills/README.md`, que é o dono
dessa lista. Planejada e **ainda inexistente**: `revisar-docs-oficiais` (revisão
periódica da documentação oficial). Não invente que ela já existe.

## Convenções desta pasta

- Regras são curtas e imperativas; contexto é factual e estável.
- Uma regra que só vale para uma IA específica vai no adapter (`AGENTS.md`,
  `GEMINI.md`), não aqui.
- Ao criar/alterar regra ou skill, registre no `CHANGELOG.md`.
