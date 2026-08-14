# Changelog

Toda mudança relevante deste projeto é registrada aqui, em entradas curtas, sem
expor identificadores corporativos, PII ou segredos. Formato: seções por data,
subseções Adicionado/Atualizado/Corrigido/Removido, cada item com a IA autora
entre parênteses. Template: `.claude/templates/changelog-entry.md`.

## 2026-08-14

### Adicionado (pacote de helpers — sprints 2 e 3 de 3)

1. (Claude) Seção `## Usar helpers da biblioteca` em 11 `SKILL.md`, cada uma com
   a tabela demanda → módulo do próprio fluxo, link para o catálogo e as
   ressalvas técnicas do domínio (leakage em splits, incidência acumulada em
   safra, thresholds calibrados em drift, escape de HTML em documentação).
2. (Claude) `rodrigo-auditoria-skills` passa a verificar aderência à biblioteca:
   novo passo na auditoria de implementação (conferir seção de helpers contra o
   catálogo), novo passo na auditoria de output (reimplementação silenciosa de
   lógica disponível vira achado) e nova dimensão de avaliação.
3. (Claude) `templates/rubrica_universal.md`: dimensão D10 reescrita com âncoras
   objetivas de aderência à biblioteca.

### Corrigido

1. (Claude) A âncora 9-10 da dimensão D10 da rubrica premiava o uso de "hooks",
   capacidade inexistente na plataforma (`.claude/rules/genie-code-oficial.md`).
   Removida junto com a reescrita da dimensão.

### Notas (pacote de helpers)

- Nenhuma `description` foi alterada nos três sprints: a seleção automática lê
  apenas o frontmatter, e as seções entram no corpo. Verificado por diff — a
  certificação de roteamento 36/36 permanece válida sem reteste.

### Adicionado (pacote de helpers — sprint 1 de 3)

1. (Claude) ADR-0004: helpers passam a ser declarados explicitamente nas skills,
   em vez de descobertos em tempo de chat. Levantamento que motivou a decisão:
   **nenhum dos 12 `SKILL.md` citava um helper** — as 3 referências do pacote
   estavam em templates auxiliares.
2. (Claude) `ambiente_fonte/.assistant/x_docs/catalogo_helpers.md`: catálogo
   demanda → módulo cobrindo os 54 helpers (47 `x_snippets` + 7 `x_scripts`),
   com API pública, marcação de dependência opcional (exigida no import vs. na
   chamada) e as restrições de runtime confirmadas no smoke test.
3. (Claude) Referências cruzadas ao catálogo em `.assistant/README.md`,
   `x_snippets/README.md` e `x_scripts/README.md`. Réplica do Free republicada.

### Adicionado

1. (Claude) `docs/testes/forward/resultados/2026-08-14_rodada1.md`: resultado da
   rodada 1 dos forward tests executada pelo Rodrigo no Genie Code do Free —
   **33 PASS, 2 FAIL, 1 pendente** de 36. Coleta automatizada via arquivos de
   evidência em `x_lab/forward_tests/` lidos por CLI.

2. (Claude) `docs/testes/forward/resultados/2026-08-14_rodada2.md`: rodada 2
   (5 testes com prompts autocontidos, IDs `-r2`) — **5 PASS, 0 FAIL**.
   **Gate de roteamento FECHADO: 36/36 PASS** (positivos 12/12, negativos
   12/12, menções 12/12), sem nenhuma alteração de `description`.

### Notas

- Rodada 2 confirmou a hipótese da rodada 1: `10P` passou com a **mesma**
  `description` e apenas o artefato embutido no prompt — a falha era do
  instrumento de teste. Nenhuma `description` foi alterada em nenhuma rodada.
- Item de vigilância registrado: `comentar-notebook` respondeu ao vocabulário
  "células %md" mas não a "markdown de documentação" no `11N-r2`; sem ação por
  ora, pois no uso real o notebook aberto no editor é sinal mais forte.
- As `description` do pacote auditado pelo Codex se mostraram bem calibradas:
  **12/12 casos negativos corretos**, sem nenhuma das colisões previstas
  (drift, materialização, deterioração, auditoria×execução); em 11 deles o
  Genie ainda escolheu a skill ideal do desvio. Nenhuma description foi
  alterada.
- As 2 falhas (`10P`, `11P`, ambas com resultado "nenhuma") concentraram-se nas
  skills que dependem de artefato no chat: os prompts citavam "este notebook"/
  "este stack trace" sem que existissem — defeito do instrumento, não do
  ambiente. Prompts v2 autocontidos aplicados no roteiro para a rodada 2
  (`07M`, `10P`, `10N`, `11P`, `11N`).
- Confirmado que skills nativas do Databricks (`data-sampling`) coexistem com as
  `rodrigo-*` no mesmo chat, sem conflito de seleção.

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
