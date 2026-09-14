# Checkpoint V08 — integração transversal com skills, padrões e Manual

## Estado

**CANDIDATA FINAL VALIDADA; PR #42 EM DRAFT; SEM ACEITE, SEM MERGE E SEM PUBLICAÇÃO DATABRICKS.**

A V08 foi criada em 14/09/2026 a partir da `main` estabilizada em `1b6632194f4b25afc09960c27b069c16df365ee6`, na branch `codex/temas-v08-integracao-transversal-20260914`.

Ela não acrescenta runtime ao Sistema de Temas. O objetivo é fazer as superfícies transversais do Hub apontarem para as capacidades e limites já integrados nas V02–V07, sem criar uma segunda fonte de paleta, token ou aprovação.

A PR #42 permanece em draft. Este checkpoint não autoriza merge: a integração depende de aceite explícito de Rodrigo depois dos checks finais no SHA exato da candidata.

## Fonte de verdade preservada

- schema e limites: `hub_padroes/identidade_visual/theme.schema.json`;
- tokens: `hub_padroes/identidade_visual/TOKENS.md`;
- resolução: `hub_snippets.visual.tema` / `ResolvedTheme`;
- Plotly: `hub_snippets.visual.theme_plotly`;
- uso específico: API/README local do consumidor;
- navegação transversal: padrões, skills e Manual Técnico.

Skills orientam e roteiam; não substituem o contrato visual.

## Superfícies integradas na candidata

A matriz `MATRIZ_INTEGRACAO.json` classifica explicitamente as superfícies da sprint. A candidata atualiza:

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

Essa compactação também tornou a manutenção das métricas do validador menos frágil. O estado final conferido no run verde registra:

- helpers citados: **92 caminhos**;
- Markdown/links: **217 arquivos / 1382 links relativos**;
- identidade do repositório: **1350 arquivos**;
- links fora da raiz: **1850**.

## Invariantes de escopo

O workflow V08 contém uma guarda que compara a branch com o SHA-base e falha se houver alteração Python em `ambiente_fonte/.assistant/hub_snippets/**` ou `hub_scripts/**`.

No head validado, a guarda declarou explicitamente `V08_RUNTIME_EDIT=0`. Fonte e `Novo_Ambiente_Simulado` são exigidos byte a byte nas superfícies alteradas, e as três cópias do Manual também precisam ser idênticas.

## Evidências e failures preservados

- `34866320427` — **FAILURE** antes da escrita: regex da migração não aceitava o Sistema de Temas como última seção `##` do Manual; nenhuma integração foi commitada por esse run.
- `34866493021` — **FAILURE** transitório: migração aplicada, mas a suíte detectou nomenclatura visual local residual e o workflow temporário ainda estava write-enabled.
- `34866578667` — **FAILURE** permanente read-only: restava apenas nomenclatura local residual no template EDA.
- `34866767026` — **FAILURE documental**: V08, cumulativas e V00 passaram; saída colada do README estava desatualizada.
- `34866944219` — **FAILURE intermediário**: fonte e simulado ficaram temporariamente diferentes entre dois commits sequenciais; a guarda de espelho reprovou corretamente.
- `34867002420` — **FAILURE documental** no head sincronizado: **22/22 V08**, **405/405 regressões** e **12/12 V00** passaram; somente métricas do README divergiam.
- `34867738695` — **FAILURE de configuração** de um mecanismo transitório; nenhum job de produto foi executado.
- `34867935251` e `34869358530` — **FAILURES documentais** que consolidaram as métricas finais anteriores à compactação do README.
- checks da PR no head anterior `cf5f4523...`: CI geral, V04, V05, V06 e V08 falharam apenas em validação documental; V00–V03 ficaram verdes.
- `34871141693` — **FAILURE documental de uma linha** depois da compactação: todos os testes passaram e somente `repo (links)` estava colado como 1851 quando o real era 1850.
- `34871401757` — **SUCCESS permanente read-only** no head `e80c3abc974022cc3daec8533af4cf47ed09d801`: V08, regressões V01–V08, V00, validador, guarda de runtime e escopo passaram; validador terminou com **0 falhas / 0 avisos**.

Nenhum failure é convertido retroativamente em sucesso.

## Estado para aceite

A implementação e a documentação da V08 estão tecnicamente fechadas. Após esta atualização de checkpoint/testes, um novo SHA será gerado apenas por documentação; esse SHA precisa repetir os mesmos gates e os checks da PR #42 antes do pedido de aceite.

A candidata final deve manter:

1. V08 **22/22**;
2. regressões V01–V08 **405/405**;
3. V00 **12/12**;
4. validador **0 falhas / 0 avisos**;
5. `V08_RUNTIME_EDIT=0`;
6. workflow permanente read-only;
7. branch sem drift em relação à `main`;
8. PR #42 em draft até aceite explícito.

## Limites

PASS da V08 não prova seleção determinística de skill pela Genie Code, publicação/instalação no workspace, browser Databricks, acessibilidade, ACL, UAT humano nem theming de SHAP/Matplotlib ou Kaplan–Meier.

Nenhuma publicação Databricks foi realizada pela V08. A V09 não foi iniciada.
