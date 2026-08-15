# Changelog

Toda mudança relevante deste projeto é registrada aqui, em entradas curtas, sem
expor identificadores corporativos, PII ou segredos. Formato: seções por data,
subseções Adicionado/Atualizado/Corrigido/Removido, cada item com a IA autora
entre parênteses. Template: `.claude/templates/changelog-entry.md`.

## 2026-08-14 — biblioteca, sprints 0 a 3

### Adicionado

1. (Claude) `x_snippets/spark/pit_join.py`: junção point-in-time com atraso de
   publicação declarado. Devolve o DataFrame e o diagnóstico do que foi
   descartado por indisponibilidade temporal. Preenche exigência textual da
   skill de feature engineering que não tinha implementação.
2. (Claude) `x_snippets/spark/join_diagnostics.py`: cobertura, não-match,
   multiplicidade e fator de expansão medidos **antes** do join, com chaves
   nulas contabilizadas à parte.
3. (Claude) `x_snippets/testing/fixtures.py`: geradores determinísticos
   (tabular, série temporal, fatos/features com vazamento marcado, safras).

### Corrigido

1. (Claude) **Defeito real em `x_snippets/ml/lgbm_ranker.py`**, encontrado ao
   exercitar o módulo pela primeira vez no runtime. Em `evaluate_ranking`, o
   reordenamento `group_labels[ranked_idx]` faz busca **por rótulo** quando `y`
   é uma Series do pandas: funcionava no primeiro grupo, onde rótulo coincide
   com posição, e quebrava do segundo em diante com `KeyError`. Passou a
   converter para array antes de fatiar.
2. (Claude) Defeito na fixture `fatos_e_features`, revelado pelo próprio teste
   anti-vazamento: com clientes repetidos entre decisões, uma feature "futura"
   para uma decisão era legitimamente passada para outra do mesmo cliente, e a
   marca `eh_futura` deixava de valer. Cada decisão passou a ter cliente
   próprio, e o teste ganhou a invariante universal
   (`feature_ts + atraso <= decisão`), que não depende do rótulo.

### Notas

- Verificação no runtime: **11 aprovações, nenhuma falha**, incluindo o teste
  que prova que nenhuma feature publicada após a decisão sobrevive ao
  `pit_join`, e a expansão de join medida contra multiplicidade conhecida
  (1:1 → 1,0; 1:N controlado → 2,0).
- Rodada 7 documentou uma restrição de ambiente não conhecida: instalar as
  bibliotecas de ML sem fixar versão derruba o kernel serverless por alteração
  de pacotes core (`pandas`, `numpy`). Detalhe em `docs/testes/spark/README.md`.
- Sprint 0 permanece **aberto**: apenas 3 dos 14 módulos com dependência
  opcional foram verificados (`train_lgbm`, `survival_cox`, `kaplan_meier`).
  Os demais exigem novo ambiente com versões compatíveis fixadas.

## 2026-08-14 — documentação, sprint 6 de 6

### Atualizado

1. (Claude) `docs/decisions/README.md`: apresenta o que é um ADR e por que a
   imutabilidade importa, usando o par 0002/0005 deste próprio projeto como
   demonstração — a sequência preserva inclusive o erro corrigido.
2. (Claude) `docs/handoffs/README.md`: exemplo curto de handoff. O formato só
   fica claro vendo um pronto; a descrição sozinha não ensinava.
3. (Claude) `docs/auditoria/README.md`: explica por que auditar com mais de um
   modelo — cada um erra de forma diferente, e a divergência entre eles marca
   onde o material é ambíguo. Tabela dos quatro níveis com o gatilho de cada um.
4. (Claude) `docs/testes/forward/README.md`: define roteamento antes de mostrar
   resultado, para quem cai direto na página.
5. (Claude) `docs/testes/spark/README.md`: como ler uma falha, com os três
   padrões observados na prática e a advertência de que passar na máquina local
   não prova nada sobre o runtime.

### Encerramento do plano de documentação

Seis sprints concluídos. Balanço em relação ao diagnóstico: os 14 READMEs
receberam tratamento, mais um glossário novo; as três lacunas sistêmicas
apontadas — ausência de glossário, exemplos sem retorno e falta de percurso
inicial — foram fechadas. Nenhuma `description` de skill foi tocada em nenhum
sprint, e a certificação de roteamento 36/36 permanece válida.

## 2026-08-14 — documentação, sprint 5 de 6

### Adicionado

1. (Claude) `ambiente_fonte/README.md`: diagrama do trajeto fonte → simulado →
   workspaces e a resposta direta a "por que duas pastas com o mesmo conteúdo" —
   a fonte é neutra, o simulado acrescenta a camada `Users/<username>/` que muda
   conforme o destino. Inclui o percurso completo de uma alteração.
2. (Claude) `x_projects/README.md`: diagrama da descoberta hierárquica do
   `AGENTS.md`, com as três consequências práticas — busca de baixo para cima,
   diretórios sem o arquivo são apenas atravessados, e os arquivos encontrados
   somam contexto em vez de se substituírem.
3. (Claude) `x_scripts/README.md`: saída real de `data_quality_check` executada
   em serverless sobre tabela sintética. O exemplo escolhido reprova por prazo de
   atualização com todos os demais checks aprovados, o que evidencia que
   `status: "fail"` reflete a política de limite configurada, não qualidade do
   dado.
4. (Claude) `x_snippets/README.md`: tabela de falhas de import com causa e
   correção, montada a partir de erros reais do runtime, não de suposição.

### Atualizado

1. (Claude) O catálogo por pacote de `x_snippets` passa a apontar para o
   catálogo por demanda, encerrando a duplicação que levaria as duas listas a
   divergir na primeira alteração.

## 2026-08-14 — documentação, sprint 4 de 6

### Atualizado

1. (Claude) `x_config/README.md`: passa a explicar o que é MCP e por que outras
   ferramentas usam arquivo JSON, antes de dizer que aqui isso não vale. Um
   arquivo de configuração que não configura nada, sem mensagem de erro que
   explique, justifica o aviso. Inclui os passos da configuração real e a
   proibição de segredos em pasta versionada.
2. (Claude) `.claude/skills/README.md`: explicita a distinção entre as duas
   famílias de skill do projeto — as daqui constroem o ecossistema, as
   `rodrigo-*` são o ecossistema. Acrescenta como uma skill é acionada e como
   criar outra.
3. (Claude) `x_prompts/README.md`: percurso completo de um formulário, do modelo
   ao preenchido, com a explicação de por que `NÃO INFORMADO` difere de campo
   vazio e de como reconhecer resposta que ignorou o contrato.

### Pendente

- O passo 4 do percurso de `x_prompts` descreve o contrato esperado em vez de
  mostrar retorno real: falta uma execução no Genie Code. Marcado no próprio
  arquivo; resposta plausível não foi inventada para preencher a lacuna.

## 2026-08-14 — documentação, sprint 3 de 6

### Adicionado

1. (Claude) Guia do ecossistema: tabela com o pedido que aciona cada uma das 12
   skills sem precisar de `@`. As frases não foram inventadas — são as que
   passaram nos forward tests. Acompanham as duas lições que os testes deram:
   skill que trabalha sobre artefato não dispara sem o artefato no chat, e
   vocabulário genérico vai para a skill errada.
2. (Claude) Verificação de acesso à biblioteca com saída real, já que o import
   não imprime nada e silêncio pode ser confundido com falha.

### Atualizado

1. (Claude) Tabela de solução de problemas ampliada de 7 para 12 sintomas,
   incorporando o que apareceu durante os gates: `.py` importado como notebook,
   `cache()` recusado em serverless, arquivo obsoleto sobrevivendo à publicação,
   metadata em cache após editar skill, e nenhuma skill carregada por falta do
   artefato citado.

### Corrigido

1. (Claude) `tools/render_simulado.py` copiava a árvore inteira, inclusive
   artefatos de execução local. Rodar um helper dentro de `ambiente_fonte/` — o
   que aconteceu ao capturar as saídas deste sprint — criava `__pycache__`, que
   era renderizado e **publicado no workspace**. O `verify` não acusava, porque
   compara fonte com remoto e o lixo estava nos dois. O render passa a ignorar
   `__pycache__`, `.pyc`, `.pyo` e caches de ferramenta; fonte, simulado e
   workspace foram limpos.

## 2026-08-14 — documentação, sprint 2 de 6

### Adicionado

1. (Claude) `README.md`: percurso de primeira hora em cinco passos, do zero até
   uma alteração publicada e conferida no workspace.
2. (Claude) Seção de comandos com **saída real capturada de execução** — padrão
   que os sprints seguintes replicam. Retorno redigido à mão foi descartado como
   prática: envelhece sem avisar.
3. (Claude) FAQ com oito perguntas, entre elas as três que o diagnóstico
   apontou como não respondidas em lugar nenhum: por que duas pastas com o mesmo
   conteúdo, o que acontece ao editar direto no workspace, e por que a skill
   alterada continua se comportando como antes.

### Corrigido

1. (Claude) O diagrama de ciclo de vida ainda citava publicação pelo engine do
   Hub, decisão supersedida pelo ADR-0005. Passou a refletir os comandos reais,
   incluindo a conferência, que antes não aparecia no fluxo.

## 2026-08-14 — documentação, sprint 1 de 6

### Adicionado

1. (Claude) `x_docs/glossario.md`: 49 verbetes separados por procedência —
   plataforma Databricks, vocabulário de modelagem e convenção deste projeto —
   mais uma seção final sobre capacidades que não existem e induzem a erro
   (slash commands próprios, hooks, memória automática, MCP por arquivo).
   A separação por origem é o ponto: procurar um termo de convenção na
   documentação oficial não devolve nada, e isso não era explicado em lugar
   nenhum.
2. (Claude) Ponteiro para o glossário no `README.md` da raiz e no guia do
   ecossistema. Nenhum outro texto foi alterado neste sprint.

## 2026-08-14

### Adicionado (publicação no Free com verificação)

1. (Claude) `tools/publicar_free.py` e skill `.claude/skills/publicar-free/`:
   plano em dry-run, publicação com gate `--execute` e `verify` read-only que
   confere ausentes, obsoletos, `.py` como `FILE`, 12 skills e 6 diretórios de
   extensão. Ciclo completo executado: 164/164 arquivos, zero pendências.
2. (Claude) ADR-0005, supersedindo o ADR-0002: o engine do Hub não pode ser
   consumido nesta camada. Evidência medida no workspace — `.py` publicado por
   ele vira `NOTEBOOK` (quebraria todos os imports de `x_snippets`), enquanto
   `--format AUTO` produz `FILE`; e o cabeçalho que ele antepõe invalidaria o
   frontmatter YAML das skills. O padrão de três fases foi mantido.

### Corrigido (publicação no Free)

1. (Claude) O `verify` detectou, na primeira execução,
   `.assistant/.mcp_servers.json` remanescente no workspace — arquivo legado
   inerte que a auditoria do Codex removera do pacote e que sobrevivera porque
   `import-dir --overwrite` sobrescreve mas nunca apaga. Removido, e a detecção
   de obsoletos incorporada à ferramenta.

2. (Claude) `tools/publicar_free.py` concatenava stdout e stderr antes de fazer
   parse de JSON. A CLI emite um aviso intermitente em stderr que corrompia a
   saída e derrubava o `verify` com `JSONDecodeError`. Os fluxos passaram a ser
   tratados separadamente, com parse tolerante; verificado em execuções
   repetidas.

### Observação encaminhável (outro repositório)

- O `_fmt_args` do engine do Hub publica `.py` como notebook; o próprio
  `write_evidence.py` da camada global está nessa condição. Correção cabe ao
  dono daquele repositório, com testes próprios.

### Adicionado (fase 4 — replicação no trabalho)

1. (Claude) `docs/playbooks/replicacao-trabalho.md`: runbook completo para o
   workspace corporativo sem CLI — backup obrigatório antes de qualquer
   remoção, três rotas de transporte com o que confirmar em cada uma, limpeza
   do ambiente antigo, verificação de estrutura, testes de aceitação, rollback
   e caminho de escala para squad.
2. (Claude) Skill operacional `.claude/skills/replicar-trabalho/` com os
   pré-requisitos verificáveis e os guardrails da operação.
3. (Claude) `.claude/rules/free-vs-trabalho.md`: nova matriz de diferenças de
   runtime já observadas (cache/persist, config de cluster, bibliotecas ML,
   variável global `spark`).

### Corrigido (fase 4)

1. (Claude) `tools/spark_smoke_test.py` tinha o caminho da biblioteca fixo no
   usuário do laboratório, o que o tornava inútil no trabalho. Passa a resolver
   pelo usuário logado, com widget `assistant_root` para sobrepor. Regressão
   executada no Free: 64 aprovações, nenhuma falha.
2. (Claude) Vetor de vazamento fechado: identificador corporativo em **nome de
   pasta** escapava à validação, que só lia conteúdo. Renderizar o simulado com
   o username do trabalho criaria `Users/<identificador>/` e um `git add`
   publicaria o identificador. Agora `tools/render_simulado.py` recusa username
   com aparência corporativa e `tools/validate_assistant.py` verifica caminhos
   além do conteúdo.

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
