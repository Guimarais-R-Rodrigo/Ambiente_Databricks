# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

- Abertura: `main=1b6632194f4b25afc09960c27b069c16df365ee6`, com V00–V07 integradas.
- V08: integração `622d2c962a80998cf990b57036f7ae503bfc0458`, fechamento `55f7006c47d90ae7f760992d252b658f53a59636`, reconciliação MM00 `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`.
- V09: integração PR #45 `0f7234c4734f1974ebb1a20123f3c26626c67ef3`, correção PR #46 `4ae714a35a0aafd930a8cd796d962b0a79449b88`, reconciliação MM00 `922ae38491cb7a502b834b092ea637620b54300a`.
- Fechamento documental V09: PR #47 / `main=d6655411ca4ac1834b0983f6ce6bdadc30b831bb`.
- Reconciliação MM00 sobre a base V09 fechada: `26cf7c8edd631f97b5c0541daff2e73dc2286a71`.

**Status:** PASS estrutural. Reconsultar `main` imediatamente antes do aceite/merge.

## T02 — Estado visual

V00–V09 estão aceitas/integradas no Git. V08 cobre integração transversal; V09 leva o contrato temático ao kit offline de transição sem converter transporte em publicação ou ativação.

**Status:** PASS. A A1 confirmou a fronteira visual proposta; as reconciliações V09 não alteram a arquitetura de micromodelos.

## T03 — Colisão nominal

Busca por `micromodel` na `main` de abertura não encontrou artefato específico.

**Status:** PASS delimitado ao repositório; não prova inexistência no ambiente de trabalho.

## T04 — Taxonomia do Hub

O template de skill e `hub-ml-criar-objeto` sustentam a lista fechada de seis tipos; a A1 confirmou que micromodelo permanece artefato de domínio e não sétimo tipo.

**Status:** PASS.

## T05 — Reuso de componentes

`MATRIZ_REUSO.md` cobre Concierge, EDA, cross-EDA, feature engineering, validação, auditoria, `schema_to_yaml`, helpers Spark e `mlflow_run`. A A1 confirmou existência e fronteiras dos itens REUSAR/ADAPTAR.

**Status:** PASS.

## T06 — Sanitização

O primeiro CI detectou um handle corporativo histórico no ADR-0017; ele foi removido e substituído por contrato genérico. A A1 não encontrou identificador externo no diff auditado.

**Status:** PASS.

## T07 — Migração tardia

Plano Mestre posiciona migração em MM12; ADR-0018 permanece proposto. A A1 confirmou que a fundação não depende da skill de migração antecipadamente.

**Status:** PASS.

## T08 — Tracking separado da especificação

YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking. A A1 confirmou que o helper atual ainda não satisfaz o perfil rule-based e que a adaptação futura foi corretamente delimitada.

**Status:** PASS arquitetural.

## T09 — Não alteração funcional pela MM00

Contra `main=d6655411...`, a PR permanece restrita a contexto, ADRs e documentação/auditoria MM00. O patch do README raiz altera somente as métricas medidas; o patch de `docs/sprints/README.md` acrescenta somente a seção MM00. Nenhum arquivo MM00 próprio pertence a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`.

**Status:** PASS nominal; reconfirmar a lista final antes do aceite.

## T10 — Validação automática

### Snapshot auditado

No head `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`, CI geral, V00, V01 e V02 estavam em `success` antes da A1.

### Pós-A1 / base V08

A inclusão do resultado A1 elevou a identidade medida de 1368 para 1369 arquivos, mantendo 1859 links. O CI `34878871911` reprovou exclusivamente a contagem congelada 1368; as demais etapas e V00/V01/V02 passaram.

### Pós-integração V09

No head `922ae38491cb7a502b834b092ea637620b54300a`, V00/V01/V02 passaram e o CI `34881774760` reprovou somente porque o README da `main` V09 isolada registrava 1355/1850 enquanto a composição mediu **1374/1859**.

### Candidata reconciliada antes do fechamento documental V09

No head `ffc7981a9d8bcebb406f918aaff2b7d414effb6f`:

- CI geral `34882724684`: `success`;
- V00 `34882724514`: `success`;
- V01 `34882724892`: `success`;
- V02 `34882724729`: `success`.

### Candidata reconciliada com o fechamento V09

No head `26cf7c8edd631f97b5c0541daff2e73dc2286a71`:

- CI geral `34883378412`: `success`;
- V00 `34883378511`: `success`;
- V01 `34883378518`: `success`;
- V02 `34883378432`: `success`.

A composição preservou **1374 arquivos / 1859 links**. O patch do README raiz foi verificado e contém somente a atualização de 1355/1850 para 1374/1859; o índice de sprints contém somente a seção MM00 além da `main`.

**Status:** PASS nos heads técnicos registrados. Como este arquivo e o checkpoint foram atualizados para registrar o último fechamento, a árvore resultante deve repetir os mesmos gates uma vez antes do gate humano; nenhuma nova alteração documental será feita depois dessa repetição salvo falha real ou decisão sobre Q-01.

## T11 — Auditoria independente A1

Arquivos: `01_contexto.md`, `02_prompt_auditoria.md` e `03_resultado_a1.md` em `docs/auditoria/2026-09-14_micromodelos-mm00/`.

**Resultado:** `APTA_COM_CORRECOES`.

- Q-01 — falta de entrada própria MM00 no `CHANGELOG.md`: **PROCEDE e continua bloqueador**;
- M-01 — cronologia não reconciliada uniformemente: **PROCEDE e está corrigido**;
- `DIVERGE`: nenhum achado atribuível à MM00.

A A1 confirmou como escopo legítimo de MM01/MM02 as decisões de encoding do YAML, máquina de estados detalhada e materialidade fina do fingerprint.

**Status:** EXECUTADA.

## T12 — Contexto canônico

`CLAUDE.md` registra V00–V09 integradas, distingue transporte de ativação/publicação, registra a A1 da MM00 e mantém ADR-0014 a ADR-0020 como propostos.

**Status:** PASS documental, sujeito à repetição final e reconsulta da `main`.

## T13 — Regra de changelog

A A1 classificou a ausência da entrada MM00 como **QUEBRA Q-01**. Uma tentativa de atualização integral acrescentou o bloco desejado, mas também modificou três linhas históricas. O patch detectou as mudanças; a tentativa foi rejeitada e o blob histórico original `2095dbcf1dd6b99e7ff008a9180361702222092b` foi restaurado por SHA. As reconciliações V09 preservaram esse mesmo blob.

**Status:** BLOQUEIO CONHECIDO. A entrada MM00 continua ausente. Não converter em PASS sem atualização estritamente aditiva comprovada ou exceção humana explícita e registrada.

## Critério final

PASS global exige T01–T13 resolvidos, diff delimitado contra a `main` vigente, CI verde na árvore de decisão e aceite humano explícito.

No fechamento técnico, o único bloqueio de conteúdo conhecido é T13/Q-01. A última repetição automática desta atualização de evidência deve ficar verde antes do gate humano.