# Checkpoint V08 — integração transversal com skills, padrões e Manual

## Estado

**CANDIDATA EM FECHAMENTO; SEM ACEITE, SEM MERGE E SEM PUBLICAÇÃO DATABRICKS.**

A V08 foi criada em 14/09/2026 a partir da `main` estabilizada em `1b6632194f4b25afc09960c27b069c16df365ee6`, na branch `codex/temas-v08-integracao-transversal-20260914`.

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

A matriz [`MATRIZ_INTEGRACAO.json`](MATRIZ_INTEGRACAO.json) classifica explicitamente as superfícies da sprint. A candidata atual atualiza:

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

## Invariantes de escopo

O workflow V08 contém uma guarda que compara a branch com o SHA-base e falha se houver alteração Python em `ambiente_fonte/.assistant/hub_snippets/**` ou `hub_scripts/**`.

Até este checkpoint, o diff V08 não altera runtime Python. Fonte e `Novo_Ambiente_Simulado` são exigidos byte a byte nas superfícies alteradas, e as três cópias do Manual também precisam ser idênticas.

## Evidências e failures preservados

- `34866320427` — **FAILURE** antes da escrita: regex da migração não aceitava o Sistema de Temas como última seção `##` do Manual; nenhuma integração foi commitada por esse run.
- `34866493021` — **FAILURE** transitório: a migração foi aplicada, mas a suíte detectou nomenclatura visual local residual no template EDA e o próprio workflow temporário ainda estava write-enabled.
- `34866578667` — **FAILURE** permanente read-only: restava apenas a nomenclatura local residual no template EDA.
- `34866767026` — **FAILURE documental**: V08, cumulativas e V00 passaram; o validador encontrou apenas saída colada do README raiz desatualizada.
- `34866944219` — **FAILURE intermediário**: durante a revisão editorial do template EDA, fonte e simulado ficaram temporariamente diferentes entre dois commits sequenciais; a guarda de espelho reprovou corretamente.
- `34867002420` — **FAILURE documental no head sincronizado**: **22/22 V08**, **405/405 regressões V01–V08** e **12/12 V00** passaram. O único bloqueio foi a saída colada do README raiz: 92 helpers reais versus 88, 217/1382 links Markdown versus 217/1383 e 1349 arquivos de identidade versus 1345. O valor de links fora da raiz permaneceu 1850.

Nenhum failure é convertido retroativamente em sucesso.

## Pendências para formar a candidata final

1. reconciliar os índices vivos com **V08 candidata**, sem dizer que foi aceita;
2. registrar a V08 no changelog como candidata;
3. medir novamente as métricas do README raiz depois de todos os documentos de fechamento estarem estáveis;
4. reconciliar exclusivamente os valores medidos, sem relaxar o validador;
5. executar no SHA final: V08, regressões V01–V08, V00, validador, guarda de runtime e escopo;
6. revisar diff e confirmar ausência de script/workflow transitório;
7. confirmar que a `main` não avançou ou reconciliar se necessário;
8. abrir PR em **draft** e auditar os checks no mesmo SHA;
9. parar para aceite explícito de Rodrigo antes de qualquer merge V08.

## Limites

PASS da V08 não prova seleção determinística de skill pela Genie Code, publicação/instalação no workspace, browser Databricks, acessibilidade, ACL, UAT humano nem theming de SHAP/Matplotlib ou Kaplan–Meier.

Nenhuma publicação Databricks foi realizada pela V08.
