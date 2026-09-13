# Relatório R06 — READMEs de séries e validação temporal

**Data:** 2026-09-12
**Base de partida:** `cae94988cda66a8c61ecebbe6ceed487120a76f2`
**Branch de autoria:** `codex/readmes-r06`
**Contrato:** README de objeto `1.0.0`
**Autoria/revisão:** ChatGPT, autorrevisão A0_light; sem auditor independente.

## 1. Objetivo

Documentar os cinco objetos marcados como R06/lote A no controle de migração, sem alterar implementação ou fachada:

1. `arima_wrapper`
2. `lgbm_temporal`
3. `prophet_wrapper`
4. `split_temporal`
5. `walk_forward`

A sprint trata três camadas que precisam permanecer distintas: geração de features temporais, desenho de validação temporal e ajuste de candidatos de forecasting. A cobertura aritmética esperada, sujeita ao validador da árvore final, é **43/75 operacionais, 3/3 exemplares e 32 pendências**.

## 2. Método de revisão

Cada objeto foi lido em implementação, fachada e notebook. Quando o comportamento dependia de biblioteca externa ou semântica temporal, a leitura foi confrontada com documentação primária de pmdarima, Prophet e pandas.

A regra é a mesma da R05: achado funcional não autoriza correção funcional dentro da migração documental. Divergências são registradas em `ACHADOS_R06.md`; o README explica o contrato real e o notebook pode receber somente correção editorial.

## 3. READMEs novos

| Objeto | Foco do guia |
|---|---|
| `arima_wrapper` | busca auto-ARIMA, critérios/ordens, métricas in-sample, MLflow obrigatório no import e intervalo calculado mas não retornado. |
| `lgbm_temporal` | geração pandas de lags/rollings/calendário, entidade, datas, duplicatas e fato de que o objeto não treina LightGBM. |
| `prophet_wrapper` | tendência/sazonalidade/feriados, forecast histórico+futuro, métricas in-sample, zero no MAPE e limites em séries agregadas. |
| `split_temporal` | partições por períodos observados, proporções por período, gaps e semântica de `group_col`. |
| `walk_forward` | expanding window, contrato do callback, quantidade de folds, gaps e metadados. |

## 4. Documentação alterada além dos cinco READMEs

A lista nominal completa está em `MATRIZ_ALTERACOES_R06.md`. Esta seção é deliberadamente explícita porque documentação operacional fora do README do objeto também faz parte do produto da sprint.

### Notebooks de exemplo

Os cinco `exemplo_*.py` recebem somente Markdown/backlinks e correções de interpretação. Devem permanecer idênticos em AST Python, magics executáveis, linhas não-Markdown e blocos históricos de output.

### Documentação de navegação e operação

A candidata final deve atualizar também:

- `ambiente_fonte/.assistant/hub_snippets/README.md`, incluindo correção do papel de `lgbm_temporal` no catálogo;
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md` e `MANUAL_TECNICO.md`;
- `README.md` da raiz;
- `CLAUDE.md`;
- `PLANO_HUB.md`;
- `docs/sprints/README.md`;
- `docs/sprints/readmes_objetos/README.md`;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`;
- `CHANGELOG.md`.

### Evidência e governança da sprint

Também são novos/alterados:

- `ACHADOS_R06.md`;
- `MATRIZ_ALTERACOES_R06.md`;
- `RELATORIO_R06.md`;
- `RUBRICA_R06.json`;
- `evidencias_r06/verificar_r06.py`;
- `evidencias_r06/verificar_preservacao.py`.

As cópias em `Novo_Ambiente_Simulado` devem ser regeneradas exclusivamente pelo renderer.

## 5. Achados que mudam a interpretação

Os detalhes estão em `ACHADOS_R06.md`. Os pontos de maior impacto editorial são:

- `arima_wrapper` devolve métricas in-sample, descarta o intervalo de previsão e usa parâmetros de busca aleatória em um caminho stepwise no qual eles não significam “50 random fits”;
- a ordem escolhida pelo auto-ARIMA é uma especificação selecionada pelo procedimento, não prova do processo gerador;
- `lgbm_temporal` não treina LightGBM e não exige `entity_cols`; o notebook histórico também conflita com a política atual de duplicatas no trecho “sem entidade”;
- lag e rolling são definidos por observações anteriores, não por duração de calendário;
- Prophet calcula somente métricas in-sample no wrapper; `SEED` não é usado; target zero pode invalidar MAPE;
- feriados de Prophet em dados agregados dependem de coincidência com a data representativa do período e não devem ser presumidos como efeito mensal automático;
- `split_temporal` e `walk_forward` avançam sobre períodos observados, não sobre uma grade temporal preenchida;
- `group_col` mede generalização a entidades inéditas; não é proteção universal de painel;
- `walk_forward` chama um callback, mas não consegue garantir que ele retreina/preprocessa apenas no treino;
- `walk_forward` pode retornar zero folds silenciosamente quando o histórico é insuficiente.

## 6. Estratégia de testes

O fechamento deve testar a **mesma árvore** que será materializada:

1. gate permanente vigente do repositório;
2. V00, V01, V02 e V03;
3. `verificar_preservacao.py` contra `cae94988...`;
4. `verificar_r06.py` para contratos estáticos e runtime pandas;
5. runtime real de pmdarima/Prophet em ambiente isolado quando as dependências estiverem presentes;
6. validador final com zero falhas/avisos e contagem de 43/75;
7. conferência de árvore antes/depois dos testes.

A suíte deve caracterizar limitações em vez de convertê-las em aprovação de design. Um comportamento existente pode passar como caracterização e continuar listado como dívida funcional.

## 7. Estado dos testes

Workflow de fechamento: **run 34730179976 — success até esta etapa**. Na árvore final: gate vigente aprovado; validador 0 falhas/0 avisos; V00/V01/V02/V03 aprovadas; preservação PASS; suíte R06 **19/19 aprovada sem skips** no ambiente isolado registrado em `r06-pacotes.txt`. Cobertura validada: **43/75 operacionais, 3/3 exemplares e 32 pendências**. A materialização ocorre somente após a reconferência abaixo.

## 8. Critérios de aceite técnico

- cinco READMEs passam no contrato 1.0.0;
- exatamente cinco pendências R06 saem do controle, sem adicionar dispensas;
- cobertura validada é derivada pelo validador, esperada em 43/75 operacionais + 3/3 exemplares + 32 pendentes;
- cinco implementações e cinco fachadas permanecem byte a byte iguais à base;
- notebooks preservam AST, magics executáveis, linhas não-Markdown e outputs históricos;
- READMEs anteriores permanecem intactos;
- ferramentas, workflows, Concierge e sistema de temas permanecem preservados;
- Manual canônico, cópia raiz e simulado permanecem sincronizados;
- dependências de teste externas não viram dependências permanentes do produto;
- nenhuma publicação/homologação Databricks é alegada;
- nenhuma auditoria independente é alegada.

## 9. Parada

Depois do fechamento técnico, a R06 deve ficar em PR draft aguardando **aceite editorial humano**. Não fazer merge nem iniciar R07 antes desse gate.
