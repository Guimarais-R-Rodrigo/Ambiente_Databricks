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

### Adicionado (testes Spark serverless — gate aprovado)

1. (Claude) `tools/spark_smoke_test.py` (notebook) + suíte `docs/testes/spark/`:
   71 checks executados em job serverless one-time no Free (Spark 4.1.0) —
   resultado final **64 PASS / 0 FAIL / 7 opcionais ausentes**.
2. (Claude) O gate revelou e levou à correção de 3 defeitos reais no
   `ambiente_fonte/` invisíveis à validação estática: `spark` como global
   inexistente em 6 módulos; `cache()`/`unpersist()` incompatíveis com
   serverless em `safe_display`, `quick_profile` e `drift_detector`;
   f-string com backslash (PEP 701, Python ≥ 3.12) em `kpi_card.py`.
   Réplica do workspace Free republicada após as correções.

### Adicionado (forward tests)

1. (Claude) Skill `.claude/skills/forward-test-skills/` e suíte em
   `docs/testes/forward/`: roteiro com 36 testes (12 skills × positivo,
   negativo e `@menção`), template de resultados e índice de rodadas. Casos
   negativos desenhados sobre as zonas de colisão entre descriptions
   (drift, WoE/IV, explicar×documentar, materialização, deterioração).

### Atualizado

1. (Claude) Workspace Databricks Free zerado e republicado como réplica deste
   projeto, a pedido do Rodrigo: backup do conteúdo anterior (camada global
   `global-*` do Hub + instruções, 10 arquivos) feito antes da remoção;
   `Novo_Ambiente_Simulado/Users/<username>/` importado via
   `databricks workspace import-dir`. Verificado: 12 skills `rodrigo-*`,
   extensões `x_`, instruções e `.py` como `FILE` (não notebook).
2. (Claude) `.claude/context/ambiente-free.md` atualizado com o novo estado do
   workspace (camada global do Hub removida; republicável pelo Hub).

### Notas

- Análise independente confirmou os achados da auditoria do Codex contra o
  export original (6 skills sem frontmatter, skills de até 2.141 linhas,
  instruções com nome sem ponto, aliases `/eda` e "hooks" não suportados,
  MCP JSON vazio, identificador corporativo em 7+ arquivos).
- Repositório GitHub privado confirmado; `Ambiente_Antigo/` mantido fora do
  git por conter identificador corporativo (ver ADR-0003).
