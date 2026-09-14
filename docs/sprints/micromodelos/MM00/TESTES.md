# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

**Abertura:** `micromodelos/mm00-baseline` nasceu da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Concorrência V08:** durante a MM00, V08 foi integrada por `622d2c962a80998cf990b57036f7ae503bfc0458` e fechada documentalmente em `55f7006c47d90ae7f760992d252b658f53a59636`. A MM00 foi reconciliada com essa base em `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`.

**Concorrência V09:** depois da A1, V09 foi integrada pelo PR #45 em `0f7234c4734f1974ebb1a20123f3c26626c67ef3`; a correção de preparação Node do workflow operacional levou a `main` a `4ae714a35a0aafd930a8cd796d962b0a79449b88`. A MM00 incorporou essa base por merge de dois pais em `922ae38491cb7a502b834b092ea637620b54300a`.

**Reconsulta após a bateria técnica:** `main` permaneceu em `4ae714a35a0aafd930a8cd796d962b0a79449b88`.

**Status:** PASS estrutural. Reconsultar novamente imediatamente antes do aceite/merge.

## T02 — Estado visual

**Esperado:** o plano não pode depender de fotografia desatualizada de outra frente.

**Observado:** V00–V09 estão integradas no Git. V08 cobre integração transversal; V09 leva o contrato temático ao kit offline de transição sem converter transporte em publicação/ativação.

**Status:** PASS. A A1 confirmou a fronteira visual proposta e a reconciliação V09 não a altera.

## T03 — Colisão nominal

**Método:** busca por `micromodel` na `main` de abertura.

**Observado:** nenhum resultado específico encontrado.

**Status:** PASS delimitado ao repositório. Não prova inexistência no ambiente de trabalho.

## T04 — Taxonomia do Hub

**Esperado:** micromodelo não vira sétimo tipo.

**Status:** PASS. O template de skill e `hub-ml-criar-objeto` sustentam a lista fechada de seis tipos; a A1 confirmou a interpretação.

## T05 — Reuso de componentes

**Evidência:** `MATRIZ_REUSO.md` classifica Concierge, EDA, cross-EDA, feature engineering, validação, auditoria, `schema_to_yaml`, helpers Spark e `mlflow_run`.

**Status:** PASS. A A1 confirmou existência e fronteiras dos componentes classificados como REUSAR/ADAPTAR.

## T06 — Sanitização

O primeiro CI detectou um handle corporativo histórico no ADR-0017; ele foi removido e substituído por contrato genérico. A A1 não encontrou identificador externo no diff auditado.

**Status:** PASS.

## T07 — Migração tardia

Plano Mestre posiciona migração em MM12; ADR-0018 permanece proposto. A A1 confirmou que nenhuma dependência da fundação exige a skill de migração antecipadamente.

**Status:** PASS.

## T08 — Tracking separado da especificação

YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking. A A1 confirmou que o helper atual ainda não satisfaz o perfil rule-based e que a adaptação foi corretamente adiada.

**Status:** PASS arquitetural; implementação somente em sprint futura.

## T09 — Não alteração funcional pela MM00

Após a reconciliação V09 e a atualização do README raiz, a PR #43 contém 23 arquivos alterados, todos de contexto, ADRs e documentação/auditoria MM00. Nenhum arquivo alterado pertence a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`.

**Status:** PASS nominal. Reconfirmar imediatamente antes do aceite.

## T10 — Validação automática

### Snapshot auditado

No head `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`, CI geral, V00, V01 e V02 estavam em `success` antes da A1.

### Pós-A1 / base V08

A inclusão do resultado A1 elevou a identidade medida de 1368 para 1369 arquivos, mantendo 1859 links. O CI `34878871911` reprovou exclusivamente a contagem congelada 1368; as demais etapas e V00/V01/V02 passaram.

### Pós-reconciliação V09

No head `922ae38491cb7a502b834b092ea637620b54300a`, V00/V01/V02 passaram e o CI geral `34881774760` reprovou apenas porque o README da `main` V09 isolada registrava 1355/1850 enquanto a composição V09+MM00 mediu **1374 arquivos / 1859 links**. Temas, biblioteca, ferramentas, transição, READMEs e Concierge passaram nessa mesma execução.

### Bateria técnica final antes deste registro

No head `5552c074fe7c0ef0512f41c7a003013f5a212f55`, após sincronizar README, contexto canônico e documentos MM00:

- CI geral `34882393722`: `success`;
- V00 `34882393690`: `success`;
- V01 `34882393695`: `success`;
- V02 `34882393657`: `success`.

O bloco verificável permaneceu em **1374 arquivos / 1859 links** e nenhum validador foi relaxado.

**Status:** PASS no head imediatamente anterior. Como este arquivo foi atualizado para registrar a evidência, a árvore corrente deve repetir os mesmos gates antes da decisão humana; nenhuma nova alteração documental será feita depois dessa repetição salvo correção de falha real ou decisão do gate Q-01.

## T11 — Auditoria independente A1

Pacote:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/03_resultado_a1.md`.

**Resultado:** `APTA_COM_CORRECOES`.

- Q-01 — falta de entrada própria MM00 no `CHANGELOG.md`: **PROCEDE e continua bloqueador**;
- M-01 — cronologia não reconciliada uniformemente: **PROCEDE e foi corrigido**;
- `DIVERGE`: nenhum achado atribuível à MM00.

A A1 confirmou como adequadamente diferidas para MM01/MM02 as decisões de encoding do YAML, máquina de estados detalhada e materialidade fina do fingerprint.

**Status:** EXECUTADA; M-01 fechado, Q-01 aberto.

## T12 — Contexto canônico

`CLAUDE.md` registra V00–V09 integradas, distingue transporte de ativação/publicação, registra a A1 da MM00 e mantém ADR-0014 a ADR-0020 como propostos.

**Status:** PASS documental, sujeito à última repetição de CI e reconsulta da `main`.

## T13 — Regra de changelog

A A1 classificou a ausência da entrada MM00 como **QUEBRA Q-01**. Uma tentativa de atualização integral acrescentou o bloco desejado, mas também modificou três linhas históricas. O patch detectou as mudanças laterais; a tentativa foi rejeitada e o blob histórico original `2095dbcf1dd6b99e7ff008a9180361702222092b` foi restaurado por SHA.

A reconciliação V09 preservou o mesmo blob oficial. Nenhuma linha histórica permanece modificada, porém a entrada MM00 continua ausente.

**Status:** BLOQUEIO CONHECIDO. Não converter em PASS sem atualização estritamente aditiva comprovada ou exceção humana explícita e registrada.

## Critério final

PASS global exige T01–T13 resolvidos, diff delimitado contra a `main` vigente, CI verde na árvore de decisão e aceite humano explícito.

No fechamento técnico, o único bloqueio de conteúdo conhecido é T13/Q-01. A última repetição automática desta atualização de evidência deve ficar verde antes do gate humano.