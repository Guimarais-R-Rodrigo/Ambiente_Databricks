# Adapter — Codex e agentes compatíveis com AGENTS.md

Use `CLAUDE.md` (raiz) como entrada canônica deste projeto e `.claude/CLAUDE.md`
como índice operacional. Este arquivo existe apenas como ponte para o padrão aberto.

Regras específicas para este agente:

- Preserve mudanças de outros agentes e do usuário; em conflito, pergunte.
- Registre suas alterações no `CHANGELOG.md` com atribuição `(Codex)`.
- Não edite `Novo_Ambiente_Simulado/` à mão — é derivado (use `tools/render_simulado.py`).
- Não versione nem exponha conteúdo de `Ambiente_Antigo/` (quarentena, ver ADR-0003).
- Valide `ambiente_fonte/` com `python tools/validate_assistant.py` antes de concluir.
