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

Uma rodada posterior detectou falso positivo documental em SHA abreviado; a correção preservou a política e passou a usar o SHA completo.

**Status:** PASS sem relaxamento de regra.

## T07 — Migração tardia

Plano Mestre posiciona migração em MM12. O ADR-0018 foi aceito sem ressalvas em D2 e mantém a migração posterior ao piloto greenfield e freeze V1.

**Status:** PASS.

## T08 — Tracking separado da especificação

YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking. O ADR-0016 foi aceito em D2. A A1 confirmou que o helper atual ainda não satisfaz o perfil rule-based e que a adaptação futura foi corretamente delimitada.

**Status:** PASS arquitetural.

## T09 — Não alteração funcional pela MM00

Contra a `main` V09 fechada, a PR permanece restrita a contexto, ADRs e documentação/auditoria MM00. O patch do README raiz altera somente métricas medidas; o índice de sprints acrescenta somente a seção MM00. Nenhum arquivo MM00 próprio pertence a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`.

**Status:** PASS nominal; reconfirmar a lista final antes do aceite.

## T10 — Validação automática

A candidata acumulou rodadas verdes após A1, reconciliações V08/V09, correções de sanitização e D1-B. Antes de D2, os quatro workflows permanentes estavam verdes no head então vigente, preservando **1374 arquivos / 1859 links** e sem relaxar validadores.

**Status:** PASS técnico pré-D2. A árvore resultante da ratificação D2 deve repetir CI geral, V00, V01 e V02 antes do aceite final da MM00. A evidência final será registrada na descrição da PR para evitar novo commit apenas por run ID.

## T11 — Auditoria independente A1

Arquivos: `01_contexto.md`, `02_prompt_auditoria.md` e `03_resultado_a1.md` em `docs/auditoria/2026-09-14_micromodelos-mm00/`.

**Resultado:** `APTA_COM_CORRECOES`.

- Q-01 — falta de entrada própria MM00 no `CHANGELOG.md`: **PROCEDE**;
- M-01 — cronologia não reconciliada uniformemente: **PROCEDE e está corrigido**;
- `DIVERGE`: nenhum achado atribuível à MM00.

A A1 confirmou como escopo legítimo de MM01/MM02 as decisões de encoding do YAML, máquina de estados detalhada e materialidade fina do fingerprint.

**Status:** EXECUTADA. O resultado histórico não é reescrito por D1-B ou D2.

## T12 — Contexto canônico e D2

`CLAUDE.md` registra V00–V09 integradas, D1-B, a A1 e o aceite sem ressalvas dos ADR-0014 a ADR-0020. O índice de ADRs e os sete ADRs foram sincronizados para `Aceito`, com integração da MM00 ainda pendente.

**Status:** PASS documental sujeito à bateria pós-D2.

## T13 — Regra de changelog

A A1 classificou a ausência da entrada MM00 como **QUEBRA Q-01**. Uma tentativa de atualização integral acrescentou o bloco desejado, mas também modificou três linhas históricas. O patch detectou as mudanças; a tentativa foi rejeitada e o blob histórico original foi restaurado por SHA.

Foi concedida a decisão humana **D1-B**: exceção explícita e exclusiva para diferir a entrada MM00 para a manutenção documental imediatamente posterior.

**Status:** DEFERIDO POR EXCEÇÃO HUMANA D1-B — **não é PASS**. Q-01 deixa de bloquear o aceite/merge da MM00, mas permanece débito documental obrigatório e deve ser fechado antes do início efetivo da MM01.

## T14 — Ratificação arquitetural D2

O usuário declarou: `D2: Aceito ADR-0014 a ADR-0020 sem ressalvas.`

Os sete ADRs preservaram o corpo decisório e receberam ratificação datada. O índice de decisões e o contexto canônico foram sincronizados. O D2 não autoriza implementação funcional, acesso a metadata real, publicação, migração ou início da MM01.

**Status:** PASS humano para as decisões arquiteturais; integração na `main` ainda depende do aceite final da MM00 e do merge.

## Critério final

T01–T12 permanecem técnicos; T13 está coberto pela exceção D1-B sem apagar o achado; T14 registra o aceite arquitetural. O fechamento da MM00 agora exige bateria pós-D2 verde, `main` estável e aceite humano explícito da MM00.

Após o merge, a manutenção documental imediatamente posterior deve registrar a entrada da MM00 no `CHANGELOG.md` antes do início efetivo da MM01.
