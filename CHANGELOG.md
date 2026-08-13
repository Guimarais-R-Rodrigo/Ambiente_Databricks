# Changelog

Toda mudança relevante deste projeto é registrada aqui, em entradas curtas, sem
expor identificadores corporativos, PII ou segredos. Formato: seções por data,
subseções Adicionado/Atualizado/Corrigido/Removido, cada item com a IA autora
entre parênteses. Template: `.claude/templates/changelog-entry.md`.

## 2026-08-13

### Adicionado

1. (Claude) Bootstrap do repositório: `CLAUDE.md` canônico, adaptadores
   `AGENTS.md`/`GEMINI.md`, `README.md`, este changelog e `.gitignore` com
   quarentena de `Ambiente_Antigo/`.
2. (Claude) Centro de IA `.claude/`: índice operacional, 5 regras
   (fonte de verdade, nomenclatura oficial Genie Code, Free vs. trabalho,
   multi-LLM, padrão de documentação), 3 arquivos de contexto, skills
   `validar-assistant` e `render-simulado`, e 4 templates.
3. (Claude) `ambiente_fonte/` criado como cópia editável do pacote
   `Ajustes_Codex/assistant_optimized_2026-08-13/` (12 skills, instruções,
   extensões `x_`). O pacote original permanece congelado como referência.
4. (Claude) `tools/validate_assistant.py`: recria localmente a bateria de
   validação da auditoria do Codex (frontmatter, links, tamanhos, AST Python,
   cercas Markdown, mojibake, identificadores pessoais).
5. (Claude) `tools/render_simulado.py`: gera `Novo_Ambiente_Simulado/` como
   espelho da árvore do workspace a partir de `ambiente_fonte/`.
6. (Claude) ADRs 0001 (arquitetura multi-IA), 0002 (reuso do engine
   `databricks-genie` do Verg_Alchemy_Hub) e 0003 (quarentena do
   `Ambiente_Antigo/`).

### Notas

- Análise independente confirmou os achados da auditoria do Codex contra o
  export original (6 skills sem frontmatter, skills de até 2.141 linhas,
  instruções com nome sem ponto, aliases `/eda` e "hooks" não suportados,
  MCP JSON vazio, identificador corporativo em 7+ arquivos).
- Repositório GitHub privado confirmado; `Ambiente_Antigo/` mantido fora do
  git por conter identificador corporativo (ver ADR-0003).
