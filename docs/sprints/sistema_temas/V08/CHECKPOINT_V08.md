# Checkpoint V08 — integração transversal com skills, padrões e Manual

## Estado

**ACEITA E INTEGRADA NO GIT; SEM PUBLICAÇÃO DATABRICKS.**

A V08 foi criada em 14/09/2026 a partir da `main` estabilizada em `1b6632194f4b25afc09960c27b069c16df365ee6`, na branch `codex/temas-v08-integracao-transversal-20260914`. Rodrigo autorizou explicitamente a integração; a PR #42 foi mesclada no commit `622d2c962a80998cf990b57036f7ae503bfc0458` a partir do head final validado `9af5615d79b02cbd86f5a6d084444c83f203ae03`.

Ela não acrescenta runtime ao Sistema de Temas. O objetivo é fazer as superfícies transversais do Hub apontarem para as capacidades e limites já integrados nas V02–V07, sem criar uma segunda fonte de paleta, token ou aprovação.

## Fonte de verdade preservada

- schema e limites: `hub_padroes/identidade_visual/theme.schema.json`;
- tokens: `hub_padroes/identidade_visual/TOKENS.md`;
- resolução: `hub_snippets.visual.tema` / `ResolvedTheme`;
- Plotly: `hub_snippets.visual.theme_plotly`;
- uso específico: API/README local do consumidor;
- navegação transversal: padrões, skills e Manual Técnico.

Skills orientam e roteiam; não substituem o contrato visual.

## Superfícies integradas

A [matriz `MATRIZ_INTEGRACAO.json`](MATRIZ_INTEGRACAO.json) classifica explicitamente as superfícies da sprint. A V08 atualiza:

- entrada `.assistant/README.md`;
- catálogo de skills;
- Concierge;
- criação de objeto;
- EDA profissional e seu template visual;
- baseline ML;
- análise de safra;
- monitoramento de modelo;
- explainability;
- índice de Hub Padrões;
- padrão de identidade visual e guia operacional;
- Manual Técnico canônico e suas duas cópias derivadas.

`hub-ml-comentar-notebook` foi deliberadamente classificada como **sem edição**: seu contrato é documentar notebook sem alterar código. Injetar theming nessa skill ampliaria escopo de forma incorreta.

## Correção estrutural mais relevante

O antigo `estilo_visual_eda.md` competia com o Sistema de Temas ao declarar paleta/dicionário próprios, repetir valores visuais e recomendar registro global legado. Na V08 ele passa a ser um guia editorial de EDA:

- sem paleta ou tema paralelo;
- sem literais hexadecimais usados como política visual;
- com `ResolvedTheme`/rotas `_resolvido` como caminho configurável;
- preservando convenções úteis de gráficos, anotações, emojis, números, tabelas, KPI-line, hierarquia, índice e cabeçalhos;
- explicitando SHAP/Matplotlib e Kaplan–Meier como limites atuais.

## Separação entre aparência e análise

As skills atualizadas registram que tema não altera:

- métricas ou probabilidades de baseline;
- MOB, denominador, cobertura ou taxa em safras;
- threshold, baseline, policy ou decisão de monitoramento;
- dados, amostra, agregação ou conclusão na EDA;
- explicação SHAP/Matplotlib, que permanece fora do theming V07.

## README raiz reconciliado

O README raiz acumulava visão corrente e um histórico extenso que já existia no índice de sprints. A V08 o compactou para uma entrada operacional curta, preservando navegação para o histórico canônico e o bloco verificável do gate local.

No head final validado, o estado conferido é:

- helpers citados: **92 caminhos**;
- Markdown/links: **217 arquivos / 1382 links relativos**;
- identidade do repositório: **1350 arquivos**;
- links fora da raiz: **1849**.

## Invariantes de escopo

O workflow V08 contém uma guarda que compara a branch com o SHA-base e falha se houver alteração Python em `ambiente_fonte/.assistant/hub_snippets/**` ou `hub_scripts/**`.

No head final, a guarda declarou explicitamente `V08_RUNTIME_EDIT=0`. Fonte e `Novo_Ambiente_Simulado` são exigidos byte a byte nas superfícies alteradas, e as três cópias do Manual também precisam ser idênticas.

## Evidências e failures preservados

- `34866320427` — **FAILURE** antes da escrita: regex da migração não aceitava o Sistema de Temas como última seção `##` do Manual; nenhuma integração foi commitada por esse run.
- `34866493021` — **FAILURE** transitório: migração aplicada, mas a suíte detectou nomenclatura visual local residual e o workflow temporário ainda estava write-enabled.
- `34866578667` — **FAILURE** permanente read-only: restava apenas nomenclatura local residual no template EDA.
- `34866767026` — **FAILURE documental**: V08, cumulativas e V00 passaram; saída colada do README estava desatualizada.
- `34866944219` — **FAILURE intermediário**: fonte e simulado ficaram temporariamente diferentes entre dois commits sequenciais; a guarda de espelho reprovou corretamente.
- `34867002420` — **FAILURE documental** no head sincronizado: **22/22 V08**, **405/405 regressões** e **12/12 V00** passaram; somente métricas do README divergiam.
- `34867738695` — **FAILURE de configuração** de um mecanismo transitório; nenhum job de produto foi executado.
- `34867935251` e `34869358530` — **FAILURES documentais** que consolidaram as métricas anteriores à compactação do README.
- checks da PR no head anterior `cf5f4523...`: CI geral, V04, V05, V06 e V08 falharam apenas em validação documental; V00–V03 ficaram verdes.
- `34871141693` — **FAILURE documental de uma linha** depois da compactação: todos os testes passaram e somente `repo (links)` estava colado como 1851 quando o real era 1850.
- `34871401757` — **SUCCESS permanente read-only** no head intermediário `e80c3abc974022cc3daec8533af4cf47ed09d801`: V08, regressões V01–V08, V00, validador, guarda de runtime e escopo passaram; naquele checkout a contagem real de links era 1850.
- `34871866915` — **FAILURE documental de uma linha** após a atualização do checkpoint/testes: V08 **22/22**, regressões **405/405** e V00 **12/12** passaram; o validador mediu `repo (links)=1849` diante de 1850 colado.
- `34872178809` — **SUCCESS permanente read-only** no head final `9af5615d79b02cbd86f5a6d084444c83f203ae03`: V08 **22/22**, regressões **405/405**, V00 **12/12**, validador **0 falhas / 0 avisos**, `V08_RUNTIME_EDIT=0` e escopo verde.

Nenhum failure é convertido retroativamente em sucesso.

## Aceite, PR e merge

A PR #42 recebeu aceite explícito de Rodrigo após os checks finais no head `9af5615d79b02cbd86f5a6d084444c83f203ae03`. Antes do merge, todos os nove checks disparados pela PR concluíram com `success`:

- V00 `34872182858`;
- V01 `34872182762`;
- V02 `34872182754`;
- V03 `34872182780`;
- V04 `34872182788`;
- V05 `34872183073`;
- V06 `34872182761`;
- CI geral `34872182808`;
- V08 `34872182789`.

O merge efetivo foi `622d2c962a80998cf990b57036f7ae503bfc0458`, com árvore idêntica à do head testado.

## Pós-merge na `main`

No merge `622d2c962a80998cf990b57036f7ae503bfc0458`, os dez workflows disparados por `push` concluíram com `success`:

- V00 `34872703807`;
- V01 `34872703784`;
- V02 `34872703942`;
- V03 `34872703701`;
- V04 `34872703770`;
- V05 `34872703955`;
- V06 `34872703775`;
- V07 `34872703931`;
- V08 `34872703962`;
- CI geral `34872703809`.

Não houve failure, cancelamento ou workflow ainda em execução no fechamento da bateria pós-merge.

## Estado encerrado

A V08 está integrada no Git. Este fechamento não publica o Hub no Databricks, não altera ACL/compute, não executa Spark/SQL/MLflow remoto e não homologa browser, acessibilidade ou UAT.

A V09 não foi iniciada.
