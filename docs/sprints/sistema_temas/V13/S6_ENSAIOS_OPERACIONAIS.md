# V13 — S6: ensaios operacionais por superfície

Status: **candidata S6 em execução**.

Baseline de abertura: merge certificado da S5 na `main`,
`11e4e17f02d4ba7846f5b80bd88c0180124b5772`, após **15/15 workflows de `push` com `success`**.

Este documento é o runbook dos ensaios S6. Ele não concede autorização para operação Databricks real, não publica tema, não altera dashboard/workspace/App remoto e não inicia a S7.

## 1. Objetivo canônico

A S6 prova, nas superfícies em que isso é possível sem ambiente remoto, o ciclo:

`PREPARE → PREFLIGHT → PACKAGE → STAGE → VERIFY → ROLLBACK`

A ordem preferencial do Plano Mestre permanece:

1. notebook/Plotly/HTML local;
2. Visual Lab local/simulado;
3. bundle V09;
4. App V10 em build/dry-run local;
5. AI/BI V11 com fixtures e export real apenas quando já disponível/autorizado;
6. ambiente Databricks real somente com autorização específica.

Nesta candidata, os cinco primeiros itens são exercitados em alcance local/simulado. O sexto permanece bloqueado porque o aceite para iniciar S6 **não** é autorização de mutação Databricks.

## 2. Para quem é

Use este runbook para provar que as rotas operacionais existentes podem ser combinadas sem depender de conhecimento tácito e sem transformar CI em homologação de ambiente.

Para um operador novo:

- `PASS` local significa somente que o ensaio local/simulado terminou conforme seu contrato;
- `BLOCKED` significa que falta um gate real e a operação não deve prosseguir;
- `NOT_APPLICABLE` não é PASS;
- uma superfície que exige Databricks real não pode ser promovida por inferência a partir de Git/CI;
- `Publish` continua uma decisão separada.

## 3. Owners reutilizados

A S6 não cria segunda implementação das superfícies.

| Superfície S6 | Owner reutilizado | Ensaio desta candidata |
|---|---|---|
| `notebook_visual_core` | V02 + V03 + V04 | render opt-in em memória, invariantes de dados/eixos/default e descarte do stage |
| `visual_lab` | V05 | preset sintético, proposta, save/reopen em diretório temporário e restore da base |
| `transition_bundle` | V09 + S2 + S3 | build canônico local, preflight, staging temporário e rollback dry-run |
| `databricks_app` | V10 + S2 + S3 | build canônico local do bundle, preflight, staging temporário e rollback dry-run |
| `aibi_dashboard` | V11 + S2 | projeção e binding somente em fixture local; sem import remoto |
| `workspace_theme` | V11 + S2 | provar que a ação remota continua `BLOCKED` |

A matriz S1 continua sendo o inventário canônico de superfícies/ações. Este documento registra execução S6; não substitui `MATRIZ_OPERACIONAL.json`.

## 4. Ferramenta e evidência

Ferramenta de ensaio:

`tools/temas_v13_ensaios.py`

Suíte permanente:

`tools/tests/test_temas_v13_s6.py`

O relatório S6:

- engine `V13-S6`;
- escopo `LOCAL_OR_SIMULATED_ONLY`;
- seis superfícies na ordem canônica;
- seis fases explícitas por superfície;
- `PASS`, `BLOCKED`, `FAIL` e `NOT_APPLICABLE` mantidos distintos;
- referências de evidência somente por caminhos relativos do repositório;
- `network_access=false`;
- `remote_mutation_performed=false`;
- `publication_performed=false`;
- `s7_started=false`.

A saída não inclui caminhos temporários do runner, credenciais, e-mail, PII ou conteúdo arbitrário dos identificadores de autorização.

## 5. Ensaio notebook/Plotly/HTML local

### PREPARE

Carrega o tema notebook de referência pelo owner V02.

### PREFLIGHT

Executa S2 para `notebook_visual_core / render_with_resolved_theme`, fixando os bytes do tema por SHA-256 e `context=notebook`.

### PACKAGE

Exporta o `ResolvedTheme` canônico em memória. Isso não cria segundo schema ou manifesto.

### STAGE

Aplica a rota V03 `_resolvido` a uma **cópia** da figura sintética e renderiza um KPI V04 com o mesmo tema.

### VERIFY

Confere:

- `data` Plotly inalterado;
- eixos/ranges inalterados;
- cor explicitamente fornecida à série preservada;
- default global `pio.templates.default` inalterado;
- valor do KPI preservado.

### ROLLBACK

Descartar a cópia staged deve deixar o objeto original byte/semântica-equivalente ao estado anterior.

Nenhum arquivo persistente é necessário nessa superfície.

## 6. Ensaio Visual Lab local/simulado

O ensaio usa somente preset sintético empacotado V05.

Ciclo:

1. S2 verifica `visual_lab / preview_proposal` como operação local/read-only;
2. o operador sintético cria um draft a partir de `legado_notebook`;
3. altera `brand.primary` por API V05;
4. salva a sessão em diretório temporário local;
5. reabre a sessão e confere o fingerprint da proposta;
6. executa `restore()` e confere o fingerprint da base;
7. o diretório temporário é descartado.

Isso prova save/reopen/restore local. Não prova frontend Databricks, persistência em workspace, permissões, browser ou UAT real.

`V12-LAB-01 = BLOQUEADO_AUTORIZACAO` permanece inalterado.

## 7. Ensaio bundle V09

A S6 chama o builder canônico existente:

`tools/bundle_implantacao.py`

O ZIP é criado somente sob `.artifacts/` e dentro de diretório temporário ignorado pelo Git.

Depois:

1. S2 valida presença, `theme_contract`, hashes, autorização local explícita e rollback preparado;
2. S3 exige árvore limpa e artefato ligado ao mesmo preflight;
3. o artefato é staged em diretório temporário;
4. o stage é revalidado pelo owner V09;
5. o rollback dry-run prova descarte/restauração esperada;
6. o temporário é removido.

Transporte continua não sendo instalação, ativação ou publicação.

## 8. Ensaio App V10 em build/dry-run local

A S6 reutiliza `tools/temas_v10_app.py` para gerar o bundle local derivado.

Depois executa:

- S2 `databricks_app / build_app_bundle`;
- S3 `release` local;
- staging temporário;
- verificação do bundle pelo owner V10;
- rollback dry-run local.

O ensaio **não executa `deploy_app`**.

Portanto continuam não comprovados:

- identidade encaminhada real;
- permissões do App;
- UC Volume real;
- abertura em browser;
- isolamento entre identidades reais;
- deploy/upgrade/rollback Databricks.

`V12-APP-01 = BLOQUEADO_AUTORIZACAO` permanece inalterado.

## 9. Ensaio AI/BI V11 com fixture local

A rota local usa:

- tema notebook validado pelo V02;
- `project_theme()` do V11;
- somente os três bindings diretos já autorizados;
- um template local deliberadamente mínimo com esses caminhos e um campo futuro que deve permanecer intacto;
- o fixture `dashboard_sintetico.json` somente para fingerprint semântico, **nunca como import nativo**.

O ensaio prova localmente que:

- a projeção é determinística;
- os três bindings diretos são aplicáveis a caminhos já existentes;
- campo desconhecido não é apagado;
- adicionar identidade de projeção ao fixture não altera o fingerprint de queries/filtros;
- descartar a cópia bound deixa os bytes originais intactos.

Isso não reexecuta `V12-AIBI-01` no Databricks. O PASS histórico de `V12-AIBI-01` continua restrito ao escopo real já observado na V12.

`A11-01 = FAIL` permanece verdadeiro e a issue #57 deve continuar aberta até correção + nova evidência aplicável. A S6 não converte o preflight S5 em correção do dashboard.

## 10. Workspace theme e ambiente Databricks real

A S6 executa somente o preflight local S2 para `workspace_theme / apply_workspace_theme` e exige que ele permaneça `BLOCKED`.

As fases `PACKAGE`, `STAGE`, `VERIFY` e `ROLLBACK` remotas ficam `NOT_APPLICABLE` porque nenhuma mutação ocorreu.

Ações que permanecem fora desta autorização:

- alterar workspace theme;
- importar tema em dashboard real;
- publicar dashboard;
- criar/atualizar Databricks App;
- alterar ACL/grupos;
- persistir sessão em workspace;
- criar/alterar UC Volume;
- qualquer outra mutação Databricks.

## 11. Casos V12 que continuam bloqueados

Sem nova autorização específica de ambiente, a saída S6 deve preservar exatamente:

| Caso | Superfície | Estado S6 |
|---|---|---|
| `V12-LAB-01` | Visual Lab real | `BLOQUEADO_AUTORIZACAO` |
| `V12-APP-01` | deploy real do App | `BLOQUEADO_AUTORIZACAO` |
| `V12-AIBI-02` | workspace theme administrativo | `BLOQUEADO_AUTORIZACAO` |

Esses casos não são contados como PASS, SKIP ou “cobertos pela CI”.

## 12. Invariantes e negativos

A suíte S6 bloqueia a candidata se:

- qualquer uma das cinco rotas locais/simuladas não completar seu ciclo aplicável;
- dados/eixos/defaults mudarem no notebook;
- save/reopen/restore V05 divergir;
- V09/V10 não comprovarem stage + rollback dry-run;
- AI/BI alterar semântica do fixture ou ampliar bindings;
- workspace theme deixar de ficar bloqueado;
- um dos três casos ambientais aparecer como PASS;
- rede, cliente Databricks, mutação remota ou publicação aparecerem no núcleo S6;
- evidência vazar caminho temporário, segredo, PII ou e-mail;
- S7 for antecipada.

## 13. Fronteiras vivas esperadas

O workflow V13 deve terminar a candidata com:

- `V13_S6_NETWORK=0`;
- `V13_S6_REMOTE_MUTATION=0`;
- `V13_S6_IMPLICIT_PUBLICATION=0`;
- `V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5`;
- `V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3`;
- `V13_S7_NOT_STARTED=1`.

A antiga asserção `V13_S6_NOT_STARTED=1` passa a ser somente comentário histórico da S5.

## 14. O que a S6 não altera

A candidata:

- não altera `ambiente_databricks/`;
- não edita `Novo_Ambiente_Simulado/`;
- não altera schema/tokens/bindings/papéis;
- não altera S1/S2/S3/S4/S5 históricos;
- não fecha issue #57;
- não altera os estados V12;
- não cria novo empacotador V09/V10;
- não inicia V14;
- não inicia S7.

## 15. Critério de aceite da S6

Para a S6 chegar ao ponto de aceite, será necessário:

1. executar a suíte própria S6 no runner;
2. executar S1–S5 novamente;
3. executar regressões V01–V13 e V00;
4. validar documentação e métricas reais;
5. preservar qualquer first failure;
6. registrar checkpoint S6;
7. recertificar o HEAD final exato;
8. reconfirmar `main`, merge-base, ahead/behind, diff, mergeabilidade, issue #57 e PRs paralelas;
9. parar para aceite explícito.

**S7 não foi iniciada.**
