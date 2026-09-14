# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

**Abertura:** `micromodelos/mm00-baseline` nasceu da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Concorrência observada:** durante a MM00, a V08 foi integrada pelo commit `622d2c962a80998cf990b57036f7ae503bfc0458` e depois fechada documentalmente em `55f7006c47d90ae7f760992d252b658f53a59636`.

**Reconciliação final observada:** a branch MM00 incorporou a `main` fechada da V08 no merge `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`, preservando a árvore funcional da V08 e reaplicando somente artefatos MM00/documentos compartilhados necessários.

**Status:** PASS. Reconsultar `main` imediatamente antes do aceite/merge.

## T02 — Estado visual

**Esperado:** o plano não pode depender de fotografia desatualizada de outra frente.

**Observado na base reconciliada:** V00–V08 estão aceitas/integradas no Git. A V08 alinha skills, padrões, entrada `.assistant`, template EDA e Manual ao Sistema de Temas sem alterar runtime Python.

**Conclusão:** o framework de micromodelos deve respeitar essa integração transversal desde a criação de suas futuras skills, enquanto a composição visual específica continua adiada para MM11.

**Status:** PASS. A A1 confirmou a fronteira visual proposta.

## T03 — Colisão nominal

**Método:** busca por `micromodel` na `main` de abertura.

**Observado:** nenhum resultado específico encontrado.

**Status:** PASS delimitado ao repositório. Não prova inexistência no ambiente de trabalho.

## T04 — Taxonomia do Hub

**Esperado:** micromodelo não vira sétimo tipo.

**Evidência:** `hub_padroes/skill/template.md` e `hub-ml-criar-objeto` tratam a lista de seis tipos como fechada.

**Status:** PASS. A A1 confirmou a interpretação.

## T05 — Reuso de componentes

**Esperado:** mapear cobertura atual antes de criar novos objetos.

**Evidência:** `MATRIZ_REUSO.md` classifica Concierge, EDA, cross-EDA, feature engineering, validação, auditoria, `schema_to_yaml`, helpers Spark e `mlflow_run`.

**Status:** PASS. A A1 confirmou a existência e a fronteira dos componentes classificados como REUSAR/ADAPTAR.

## T06 — Sanitização

**Esperado:** nenhum identificador/path real do ambiente externo no framework versionado.

**Primeira rodada:** o CI detectou um handle corporativo histórico no ADR-0017.

**Correção:** o handle foi removido e substituído por contrato genérico de handoff. Rodadas posteriores do CI passaram a etapa de validação sem novo achado de sanitização.

**A1:** PASS sem identificador externo encontrado no diff auditado.

**Status:** PASS.

## T07 — Migração tardia

**Esperado:** skill/briefing de migração não existem antes do piloto greenfield e freeze V1.

**Evidência:** Plano Mestre posiciona migração em MM12; ADR-0018 permanece proposto.

**A1:** confirmou que nenhuma dependência da fundação exige a skill de migração antecipadamente.

**Status:** PASS.

## T08 — Tracking separado da especificação

**Esperado:** YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking.

**Evidência:** Plano Mestre e ADR-0016 proposto.

**A1:** confirmou que o helper atual de MLflow não satisfaz ainda o perfil rule-based e que a adaptação foi corretamente adiada, sem promessa falsa de capacidade existente.

**Status:** PASS arquitetural; implementação somente em sprint futura.

## T09 — Não alteração funcional pela MM00

**Esperado:** a iniciativa MM00 não cria/modifica funcionalidade do produto.

**Observado após a A1:** a PR #43 contém 23 arquivos alterados. Eles são `CLAUDE.md`, `README.md`, pacote A1 incluindo `03_resultado_a1.md`, ADR-0014 a ADR-0020, índices e documentação da iniciativa MM00.

O `README.md` raiz foi alterado exclusivamente para reconciliar as métricas que o próprio validador mediu após a inclusão documental.

Nenhum arquivo alterado pertence a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`.

**A1:** PASS para ausência de mudança funcional.

**Status:** PASS nominal. Reconfirmar a lista final antes do aceite.

## T10 — Validação automática

### Snapshots pré-A1

O histórico preserva failures documentais e sucessos subsequentes. No head auditado `f5577f5933d2ab19b5adfb9c7eea1c8fb3c80843`, CI geral, V00, V01 e V02 estavam em `success`.

### Rodada pós-A1

A inclusão de `03_resultado_a1.md` elevou a identidade medida de 1368 para **1369 arquivos**, mantendo **1859 links**. O CI geral `34878871911` reprovou exclusivamente porque o README raiz ainda congelava 1368; temas, biblioteca, ferramentas, transição, READMEs e Concierge passaram. V00, V01 e V02 também permaneceram verdes nessa rodada.

O README raiz foi então reconciliado para 1369/1859 sem relaxar validador.

**Status:** PENDENTE apenas da bateria final sobre o head de fechamento documental. Failure intermediário permanece registrado como failure.

## T11 — Auditoria independente A1

Pacote:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/03_resultado_a1.md`.

**Resultado:** `APTA_COM_CORRECOES`.

Achados:

- Q-01 — falta de entrada própria MM00 no `CHANGELOG.md`: **PROCEDE e continua bloqueador**;
- M-01 — cronologia do baseline não reconciliada uniformemente: **PROCEDE e foi corrigido no README vivo da MM00**;
- `DIVERGE`: nenhum achado atribuível à MM00.

A A1 também confirmou como adequadamente diferidas para MM01/MM02 as decisões de encoding do YAML, máquina de estados detalhada e materialidade fina do fingerprint.

**Status:** EXECUTADA; correções parcialmente concluídas, com Q-01 ainda aberto.

## T12 — Contexto canônico

**Esperado:** `CLAUDE.md` reflete a `main` vigente e não transforma ADR proposto em decisão ativa.

**Observado:** `CLAUDE.md` registra V00–V08 como integradas e MM00/ADR-0014 a ADR-0020 como propostas. O índice de ADRs mantém os mesmos status.

**Status:** PASS documental. Reconsultar `main` antes do aceite porque outra frente pode avançar em paralelo.

## T13 — Regra de changelog

`CLAUDE.md` exige entrada em `CHANGELOG.md` para toda sessão que altera algo.

A A1 classificou a ausência da entrada MM00 como **QUEBRA Q-01**. Uma tentativa de atualização por substituição integral acrescentou o bloco desejado, porém também reformatou duas linhas históricas e corrigiu inadvertidamente um typo antigo. O patch detectou as três mudanças laterais; a tentativa foi recusada e o blob histórico original foi restaurado integralmente por SHA.

Assim, nenhuma entrada histórica permanece modificada, mas a entrada MM00 ainda não existe.

**Status:** BLOQUEIO CONHECIDO. Não converter em PASS sem uma atualização estritamente aditiva ou exceção humana explícita e registrada.

## Critério final

PASS global exige T01–T13 resolvidos, diff da MM00 delimitado contra a `main` vigente, CI verde no head final e aceite humano explícito.

Neste momento, o único bloqueio de conteúdo conhecido é T13/Q-01. A bateria automática final ainda precisa confirmar o head de fechamento documental antes do checkpoint humano.