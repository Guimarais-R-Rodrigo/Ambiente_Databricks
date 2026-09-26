# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

- Abertura: `main=1b6632194f4b25afc09960c27b069c16df365ee6`, com V00–V07 integradas.
- V08: integração `622d2c962a80998cf990b57036f7ae503bfc0458` e fechamento `55f7006c47d90ae7f760992d252b658f53a59636`.
- A1: head auditado `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`.
- V09: PRs #45/#46 e fechamento documental PR #47 em `d6655411ca4ac1834b0983f6ce6bdadc30b831bb`.
- Head final da candidata: `e3809b15b61f2bc1eeec06c9de6f38a329868e98`.
- Merge MM00: PR #43 / `36e89515a46df24f41deea4791b109f5a1f938f2`.

**Status:** PASS final.

## T02 — Estado visual

V00–V09 estavam integradas no Git no fechamento da MM00. A A1 confirmou a fronteira visual proposta: micromodelos consomem o Sistema de Temas e não criam tema paralelo.

**Status:** PASS. MM00 não alterou implementação visual.

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

O primeiro CI detectou conteúdo incompatível com a política de sanitização no ADR-0017; ele foi removido e substituído por contrato genérico. Uma rodada posterior detectou falso positivo documental em SHA abreviado; a correção preservou a política e passou a usar o SHA completo.

**Status:** PASS sem relaxamento de regra.

## T07 — Migração tardia

Plano Mestre posiciona migração em MM12. O ADR-0018 foi aceito sem ressalvas em D2 e mantém a migração posterior ao piloto greenfield e freeze V1.

**Status:** PASS.

## T08 — Tracking separado da especificação

YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking. O ADR-0016 foi aceito em D2. A A1 confirmou que o helper atual ainda não satisfaz o perfil rule-based e que a adaptação futura foi corretamente delimitada.

**Status:** PASS arquitetural.

## T09 — Não alteração funcional pela MM00

A PR #43 foi integrada contendo somente contexto, ADRs e documentação/auditoria MM00; nenhuma alteração funcional própria pertenceu a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou workflows.

**Status:** PASS.

## T10 — Validação automática

No head final `e3809b15b61f2bc1eeec06c9de6f38a329868e98`:

- CI geral `34893158270`: `success`;
- V00 `34893158453`: `success`;
- V01 `34893158339`: `success`;
- V02 `34893158265`: `success`.

A indisponibilidade temporária anterior de runners do GitHub Actions ficou registrada e não foi confundida com regressão da candidata.

**Status:** PASS técnico final da candidata aceita.

## T11 — Auditoria independente A1

Arquivos: `01_contexto.md`, `02_prompt_auditoria.md` e `03_resultado_a1.md` em `docs/auditoria/2026-09-14_micromodelos-mm00/`.

**Resultado histórico:** `APTA_COM_CORRECOES`.

- Q-01 — falta de entrada própria MM00 no `CHANGELOG.md`: **PROCEDE**;
- M-01 — cronologia não reconciliada uniformemente: **PROCEDE e foi corrigido**;
- `DIVERGE`: nenhum achado atribuível à MM00.

A A1 confirmou como escopo legítimo de MM01/MM02 as decisões de encoding do YAML, máquina de estados detalhada e materialidade fina do fingerprint.

**Status:** EXECUTADA. O resultado histórico não é reescrito pelos fechamentos posteriores.

## T12 — Contexto canônico e D2

ADR-0014 a ADR-0020 foram aceitos sem ressalvas e integrados com a MM00. O contexto canônico é reconciliado no fechamento pós-merge para registrar MM00 integrada e MM01 ainda não iniciada.

**Status:** PASS documental após esta manutenção.

## T13 — Regra de changelog / Q-01

A primeira tentativa de inserção integral do bloco MM00 foi rejeitada porque alterava linhas históricas. O histórico foi restaurado antes do merge.

Após a integração da PR #43, uma automação transitória restrita à branch `micromodelos/mm00-fechamento-pos-merge`:

1. leu `CHANGELOG.md` como bytes;
2. encontrou o primeiro cabeçalho histórico após o preâmbulo;
3. inseriu o bloco MM00 sem decodificar/reformatar o conteúdo anterior;
4. verificou prefixo e sufixo byte a byte;
5. removeu o próprio workflow no mesmo commit.

A comparação entre `36e89515a46df24f41deea4791b109f5a1f938f2` e o commit resultante do passo Q-01 mostrou somente `CHANGELOG.md`, com **22 adições, 0 deleções**.

**Status:** PASS. Q-01 está fechado; D1-B foi consumida e não cria exceção permanente à regra de changelog.

## T14 — Ratificação arquitetural D2

Foi concedido aceite explícito sem ressalvas a ADR-0014 a ADR-0020. Os sete ADRs preservaram o corpo decisório, receberam ratificação datada e foram integrados pela PR #43.

**Status:** PASS humano e integrado.

## T15 — Aceite final e merge

A MM00 recebeu aceite final explícito e autorização de integração. A PR #43 foi retirada de draft e integrada com `expected_head_sha=e3809b15b61f2bc1eeec06c9de6f38a329868e98`, resultando no merge `36e89515a46df24f41deea4791b109f5a1f938f2`.

**Status:** PASS.

## Critério final

T01–T15 estão fechados. MM00 cumpriu seu objetivo e está integrada. Esta manutenção pós-merge fecha o último débito documental Q-01 e atualiza o estado vivo.

**MM01 é a próxima sprint prevista, mas não foi iniciada por esta manutenção.**
