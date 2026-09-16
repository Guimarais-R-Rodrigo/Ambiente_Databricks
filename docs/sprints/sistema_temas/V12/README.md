# V12 — homologação de jornadas com pessoas e ambiente

## Estado de fechamento

A V12 está em **candidata de fechamento pré-aceite**. Todos os casos V12 possuem agora estado explícito, sem transformar CI em evidência humana, sem transformar bloqueio de autorização em PASS e sem reabrir a arquitetura V11.

Estado canônico das jornadas:

| Caso | Classe | Estado | Evidência/limite |
|---|---|---|---|
| `DOC-02` | `human_uat` | **PASS** | participante real autorizado identificou a próxima ação sem ajuda em 25 s |
| `DOC-03` | `human_uat` | **PASS** | participante distinguiu prévia, salvar, submeter, aprovar, publicar e recuperar sessão sem ajuda |
| `A11-01` | `human_uat` | **FAIL** | contraste objetivo reprovou pares efetivamente renderizados; issue #57 |
| `SEC-01` | `databricks_environment` | **PASS** | identidade e permissão efetivas observadas, sem papel autodeclarado e sem PII versionada |
| `UAT-01` | `human_uat` | **PASS** | rota textual herdada da V01 concluída em 360 s, sem ajuda e sem alteração compartilhada acidental |
| `V12-LAB-01` | `databricks_environment` | **BLOQUEADO_AUTORIZACAO** | não há autorização específica para mutação do Visual Lab real; ambiente/pré-requisito real também não foi estabelecido |
| `V12-APP-01` | `databricks_environment` | **BLOQUEADO_AUTORIZACAO** | deploy do Databricks App não foi autorizado |
| `V12-AIBI-01` | `databricks_environment` | **PASS** | dashboard draft real, dados sintéticos, import sem Publish, Light/Dark e rollback integral |
| `V12-AIBI-02` | `databricks_environment` | **BLOQUEADO_AUTORIZACAO** | workspace theme/admin/snapshot/reaplicação não foram autorizados; Publish continua gate separado |

`FAIL`, `BLOQUEADO_AUTORIZACAO` e `PASS` não são sinônimos. O encerramento da V12 exige estado honesto para todos os casos executáveis; não exige forçar cada superfície ambiental a PASS.

## O que a V12 é

A V12 é a camada de **protocolo, evidência e homologação formativa** do Sistema de Temas. Ela prova ou registra explicitamente aquilo que CI/local sozinho não consegue provar: uso humano, comportamento real no Databricks, identidade/permissão efetiva, render, rollback e bloqueios operacionais.

Ela não cria outro engine de temas, não implementa `context="aibi"`, não transforma revisão do autor em auditoria independente, não autoriza produção e não inicia V13/V14.

## Contrato V11 preservado

A V12 mantém integralmente as decisões da V11:

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- 48 tokens continuam classificados em 3 `translated`, 23 `approximated` e 22 `unsupported`;
- somente `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette` e `card.radius_px -> widget.corner_radius` são bindings diretos;
- arquivo nativo só é manipulado a partir de export real fixado por SHA-256 e JSON Pointers revisados existentes;
- `dashboard_sintetico.json` continua não importável;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme são escopos distintos;
- `Import theme` e `Publish` continuam gates separados.

O achado `A11-01` não altera esse contrato. As cores que reprovaram pertencem a `cellFormat` explícito do dashboard, não aos três bindings diretos do Hub. A issue #57 registra a decisão futura necessária; a V12 não amplia silenciosamente a V11 para fazê-la passar.

## Evidência Git/local

A V12 foi reconciliada aditivamente com a `main` atual `28669f99db27cf23df73549297bbf57eda033f58`, que integrou a frente de Skill Enforcement. O merge de reconciliação `fd8f5dfdd6354e10964feaa51d10ede746c8c970` ficou `behind_by=0`, `mergeable=true` e teve **7/7 workflows de pull request em success**.

No workflow V12 `35026047355` desse baseline reconciliado:

- V12 específica: 47/47 PASS;
- evidência/hardening: 10/10 PASS;
- regressões V01–V12: 514/514 PASS;
- V00: 12/12 PASS;
- validador: 0 falhas / 0 avisos;
- métricas medidas: 1424 arquivos / 1887 links;
- higiene: 17 caminhos integrais + 3 documentos compartilhados pelo diff;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`;
- workflow read-only com `Contents: read`, `Metadata: read` e `persist-credentials:false`.

O workflow V00 mantém uma etapa condicional de branch isolada em `SKIP`; esse `SKIP` não é promovido a PASS. O warning de Node 20 é da plataforma GitHub Actions, não do validador do projeto.

Este documento integra um novo teste permanente para as evidências humanas reais e para o `FAIL` de `A11-01`. Portanto o **head de fechamento precisa ter sua própria execução de CI** antes de ser apresentado para aceite; o baseline `fd8f5df...` não certifica automaticamente o commit documental/teste seguinte.

## Homologação AI/BI e segurança

`V12-AIBI-01` possui uma tentativa #1 preservada como **FAIL** porque usou dado público de amostra em vez de dado sintético. A tentativa #2 é **PASS real**: duas queries temporárias em SQL `VALUES`, nenhum objeto persistente criado, tema importado somente em dashboard draft, Light/Dark observado, `published=false`, semântica preservada e rollback integral.

`SEC-01` é **PASS real de ambiente**. A identidade autenticada foi observada separadamente e a permissão efetiva foi demonstrada pelas ações realmente concluídas na sessão sintética válida. Nome, e-mail, workspace ID e bytes de identidade não são versionados. Papel autodeclarado não conta como autorização.

As autorizações AI/BI e A11 já consumidas não se tornam autorizações permanentes. Workspace theme, ACL, deploy de App e Publish permanecem fora do escopo autorizado.

## Homologação humana

A sessão de documentação/UAT usou participante real autorizado sanitizado como `P-UAT-01`, sem identidade pessoal no Git. Foram entregues somente o README e o guia de primeiro uso do `theme_lab`, sem explicação verbal inicial.

- `DOC-02`: 25 segundos, nenhuma ajuda, próxima ação identificada corretamente;
- `DOC-03`: alcance e persistência explicados corretamente, nenhuma ajuda;
- `UAT-01`: 360 segundos, jornada textual completa e correta, nenhuma ajuda, sem confundir salvar com publicar ou alterar o padrão da equipe.

O `PASS` de `UAT-01` é **explicitamente a rota textual herdada da V01**. Ele não prova browser/runtime do Visual Lab; essa prova pertence a `V12-LAB-01`, que permanece bloqueado por autorização.

`A11-01` foi executado separadamente com participante autorizado `P-MAINT-01`. O participante não percebeu irregularidade em Light/Dark, teclado, foco, zoom 200%, dependência exclusiva de cor ou rótulos, mas o oráculo objetivo falhou:

- vermelho `#9C2638` sobre widget Light `#E8F4FD`: 6.837793163467097:1 — PASS;
- vermelho `#9C2638` sobre widget Dark `#11171C`: 2.3624715346329377:1 — FAIL;
- amarelo `#FFD465` sobre widget Light `#E8F4FD`: 1.264684095079348:1 — FAIL;
- amarelo `#FFD465` sobre widget Dark `#11171C`: 12.773222792356847:1 — PASS.

Nenhum desses textos foi classificado como texto grande. Logo `A11-01 = FAIL` e `oracle_met=false`; percepção subjetiva não sobrescreve a medição.

## Critério para aceite desta candidata

Antes de integrar a PR #54:

1. o head de fechamento deve ter seus próprios workflows verdes;
2. a PR deve continuar `behind_by=0` e mergeável contra a `main` vigente;
3. o usuário precisa aceitar explicitamente a V12 **sabendo** que `A11-01` permanece FAIL rastreado na issue #57 e que três jornadas ambientais estão bloqueadas por autorização;
4. nenhum bloqueio será convertido em PASS para facilitar merge;
5. depois do merge, os workflows da `main` precisam ser auditados;
6. documentação viva que dependa do estado pós-merge pode ser reconciliada em PR documental separada.

Até esse aceite, a PR permanece draft. V13 continua bloqueada.
