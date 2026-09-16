# Checkpoint V12 — candidata de fechamento pré-aceite

Data: 15/09/2026.

Branch: `codex/temas-v12-homologacao-jornadas-20260914`.

## Base e reconciliação

A base vigente é a `main` `28669f99db27cf23df73549297bbf57eda033f58`, que incorporou a frente de Skill Enforcement. A V12 foi reconciliada por merge aditivo `fd8f5dfdd6354e10964feaa51d10ede746c8c970`, com os dois históricos preservados, sem rebase, reset ou force-push.

Após a reconciliação:

- `behind_by=0`;
- merge-base = `28669f99db27cf23df73549297bbf57eda033f58`;
- PR #54 = aberta, draft e mergeável;
- PR #51/MM01 permanece paralela e não é incorporada à V12;
- `CHANGELOG.md` continua fora da candidata para evitar conflito documental com MM01.

## Baseline reconciliado certificado

O head `fd8f5dfdd6354e10964feaa51d10ede746c8c970` obteve 7/7 workflows de pull request em `success`:

- V00 `35026047301`;
- V02 `35026047191`;
- V01 `35026047195`;
- CI geral `35026047390`;
- V12 `35026047355`;
- V10 `35026047337`;
- V11 `35026047348`.

Auditoria interna do V12 `35026047355`:

- 47/47 V12 PASS;
- 10/10 evidência/hardening PASS;
- 514/514 regressões V01–V12 PASS;
- 12/12 V00 PASS;
- validador `APROVADO: 0 falha(s), 0 aviso(s)`;
- 1424 arquivos / 1887 links;
- worktree extras = 0;
- higiene = 17 caminhos integrais + 3 documentos compartilhados;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`;
- token do workflow somente `Contents: read` e `Metadata: read`;
- checkout com `persist-credentials:false`.

O `SKIP` condicional do workflow V00 continua sendo `SKIP`, não PASS. O warning de Node 20 pertence ao GitHub Actions e não ao validador do projeto.

## Estado final das jornadas antes do aceite

| Caso | Estado | Decisão |
|---|---|---|
| `DOC-02` | **PASS** | participante real autorizado; próxima ação sem ajuda em 25 s |
| `DOC-03` | **PASS** | conceitos de alcance/persistência distinguidos sem ajuda |
| `A11-01` | **FAIL** | contraste insuficiente de `cellFormat` explícito do dashboard em Light/Dark; issue #57 |
| `SEC-01` | **PASS** | identidade + permissão efetiva observadas em ambiente; sem PII versionada |
| `UAT-01` | **PASS** | rota textual V01 concluída em 360 s, sem ajuda e sem mudança compartilhada acidental |
| `V12-LAB-01` | **BLOQUEADO_AUTORIZACAO** | não existe autorização específica para a mutação real; ambiente/pré-requisito também não foi estabelecido |
| `V12-APP-01` | **BLOQUEADO_AUTORIZACAO** | deploy de App não autorizado |
| `V12-AIBI-01` | **PASS** | dashboard draft real, dados sintéticos, import sem Publish e rollback integral |
| `V12-AIBI-02` | **BLOQUEADO_AUTORIZACAO** | workspace theme/admin/snapshot/reaplicação não autorizados; Publish é gate separado |

Todos os casos executáveis têm estado explícito. Nenhum bloqueio foi promovido a PASS e nenhum FAIL foi apagado.

## `A11-01` — achado real preservado

A revisão humana de Light/Dark, foco, teclado, zoom 200%, rótulos e dependência exclusiva de cor não relatou dificuldade perceptiva. O critério objetivo, porém, reprovou dois pares realmente renderizados:

- `#9C2638` sobre `#11171C` = `2.3624715346329377:1` em Dark;
- `#FFD465` sobre `#E8F4FD` = `1.264684095079348:1` em Light.

O limiar aplicável é 4,5:1; não houve classificação de texto grande. Portanto `oracle_met=false` e o caso permanece FAIL. A issue #57 registra o achado.

As cores pertencem à formatação condicional explícita do dashboard (`cellFormat`), não à matriz de tokens do Hub. A V11 continua limitada aos três bindings diretos canônicos e não foi ampliada para “fazer passar” a homologação.

## Evidência humana consolidada

Participante sanitizado: `P-UAT-01`, papel `nontechnical_user`, autorizado.

Documentação entregue sem ajuda inicial:

- `ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/README.md`;
- `ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md`.

Versão observada: `89486948045e7222232f8d3aa4c602151f46c6c1`.

Resultados:

- DOC-02: 25 s, `help_events=[]`;
- DOC-03: sem confusão, `help_events=[]`;
- UAT-01: 360 s, `help_events=[]`, jornada textual completa, sem alteração compartilhada acidental.

A rota textual de UAT é a prevista historicamente pela V01 e não substitui `V12-LAB-01`.

## Autorizações consumidas e fronteiras

Foram consumidas apenas as autorizações específicas já registradas para `V12-AIBI-01` e `A11-01`. Nenhuma delas autoriza de forma permanente ou implícita:

- workspace theme;
- ACL/grupos;
- deploy de Databricks App;
- `Publish`;
- qualquer mutação de `V12-LAB-01`, `V12-APP-01` ou `V12-AIBI-02`.

## História de failures preservada

Continuam históricos e não reclassificados:

- failures originais de métricas stale, fetch redundante e auto-match da higiene;
- tentativa AI/BI #1 = FAIL por dado não sintético;
- incidente do commit `468eb637...` com README placeholder, reparado aditivamente por `4823f3ab...`;
- `10785088...` = FAILURE legítimo de integração parcial do hardening, reparado por `26f84d...`;
- `A11-01` = FAIL real de contraste, issue #57.

## Próximo gate

Este checkpoint pertence ao **commit de fechamento pré-aceite**, que precisa ter CI próprio. Não reutilizar o verde de `fd8f5df...` para certificar alterações posteriores.

Se o head de fechamento ficar verde, a PR #54 deverá permanecer draft até o usuário decidir explicitamente se aceita integrar a V12 com:

- `A11-01` conhecido como FAIL rastreado;
- três jornadas ambientais explicitamente bloqueadas por autorização;
- demais casos humanos/ambientais encerrados conforme seus oráculos.

Somente após aceite explícito: marcar a PR pronta, integrar sem force e auditar os workflows pós-merge. V13 permanece bloqueada até esse ciclo terminar.
