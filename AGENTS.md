# Adapter — Codex e agentes compatíveis com AGENTS.md

Use `CLAUDE.md` (raiz) como entrada canônica deste projeto e `.claude/CLAUDE.md`
como índice operacional. Este arquivo existe apenas como ponte para o padrão aberto.

Regras específicas para este agente:

- Preserve mudanças de outros agentes e do usuário; em conflito, pergunte.
- Registre suas alterações no `CHANGELOG.md` com atribuição `(Codex)`.
- Não edite `Novo_Ambiente_Simulado/` à mão — é derivado (use `tools/render_simulado.py`).
- Não versione nem exponha conteúdo de `Ambiente_Antigo/` (quarentena, ver ADR-0003).
- Valide `ambiente_fonte/` com `python tools/validate_assistant.py` antes de concluir.


## Codex Autonomous Controller Mode

Quando o usuário ativar explicitamente uma frente em **Codex Autonomous Controller Mode**:

1. leia `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`;
2. valide o envelope ativo em `docs/operations/autonomy/`;
3. leia o state source apontado pelo envelope;
4. use os papéis project-scoped de `.codex/agents/`;
5. mantenha exatamente um writer;
6. continue autonomamente entre Human Gates enquanto a classe de autoridade e os budgets permitirem.

Não trate aprovação desta arquitetura como ativação A2. Promoção de policy, Ready, merge, workspace/dados corporativos e `UNKNOWN` irresolvido permanecem Human Gates.

Execute `python -B tools/validate_codex_autonomy.py --json` antes de uma sessão autônoma material.
