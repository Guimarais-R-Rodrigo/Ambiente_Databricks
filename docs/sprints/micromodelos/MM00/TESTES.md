# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

**Abertura:** `micromodelos/mm00-baseline` nasceu da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Concorrência observada:** durante a MM00, a V08 foi integrada pelo commit `622d2c962a80998cf990b57036f7ae503bfc0458` e depois fechada documentalmente em `55f7006c47d90ae7f760992d252b658f53a59636`.

**Reconciliação final observada:** a branch MM00 incorporou a `main` fechada da V08 no merge `edfcf58e4700ccf5d58d2befddccbd9fe50ac124`, preservando a árvore funcional da V08 e reaplicando somente artefatos MM00/documentos compartilhados necessários.

**Reconsulta:** antes desta atualização de gate, a `main` permanecia em `55f7006c47d90ae7f760992d252b658f53a59636`.

**Status:** PASS. Reconsultar imediatamente antes do aceite/merge.

## T02 — Estado visual

**Esperado:** o plano não pode depender de fotografia desatualizada de outra frente.

**Observado:** V00–V08 estão aceitas/integradas no Git; V09 não havia sido iniciada na `main` reconsultada. A V08 alinha skills, padrões, entrada `.assistant`, template EDA e Manual ao Sistema de Temas sem alterar runtime Python.

**Conclusão:** o framework de micromodelos deve respeitar essa integração transversal desde a criação de suas futuras skills, enquanto a composição visual específica continua adiada para MM11.

**Status:** PASS arquitetural; a auditoria A1 deve revisar a interpretação.

## T03 — Colisão nominal

**Método:** busca por `micromodel` na `main` de abertura.

**Observado:** nenhum resultado específico encontrado.

**Status:** PASS delimitado ao repositório. Não prova inexistência no ambiente de trabalho.

## T04 — Taxonomia do Hub

**Esperado:** micromodelo não vira sétimo tipo.

**Evidência:** `hub_padroes/skill/template.md` e `hub-ml-criar-objeto` tratam a lista de seis tipos como fechada.

**Status:** PASS.

## T05 — Reuso de componentes

**Esperado:** mapear cobertura atual antes de criar novos objetos.

**Evidência:** `MATRIZ_REUSO.md` classifica Concierge, EDA, cross-EDA, feature engineering, validação, auditoria, `schema_to_yaml`, helpers Spark e `mlflow_run`.

**Status:** PASS documental; auditor A1 deve confirmar os contratos citados contra a árvore vigente.

## T06 — Sanitização

**Esperado:** nenhum identificador/path real do ambiente externo no framework versionado.

**Primeira rodada:** o CI detectou um handle corporativo histórico no ADR-0017.

**Correção:** o handle foi removido e substituído por contrato genérico de handoff. Rodadas posteriores do CI passaram a etapa de validação sem novo achado de sanitização.

**Status:** PASS automatizado, sujeito à revisão semântica A1.

## T07 — Migração tardia

**Esperado:** skill/briefing de migração não existem antes do piloto greenfield e freeze V1.

**Evidência:** Plano Mestre posiciona migração em MM12; ADR-0018 permanece proposto.

**Status:** PASS documental.

## T08 — Tracking separado da especificação

**Esperado:** YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking.

**Evidência:** Plano Mestre e ADR-0016 proposto.

**Status:** PASS arquitetural; implementação só em sprint futura.

## T09 — Não alteração funcional pela MM00

**Esperado:** a iniciativa MM00 não cria/modifica funcionalidade do produto.

**Observado contra a `main` fechada da V08:** a PR #43 contém 21 arquivos alterados e nenhum deles pertence a `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou `.github/workflows/`.

Os 21 arquivos são contexto canônico, ADRs, índices e documentação/auditoria da MM00.

**Status:** PASS nominal. A auditoria A1 deve verificar que nenhum conteúdo documental cria efeito funcional indireto incompatível com o escopo.

## T10 — Validação automática

### Rodada que encontrou as divergências finais

No head anterior, o CI geral `34875814570` reprovou somente porque o bloco congelado do README raiz ainda registrava 1350 arquivos/1850 links, enquanto o validador mediu 1368 arquivos/1859 links. Temas, biblioteca, ferramentas, transição, READMEs e todos os checks do Concierge passaram nessa mesma execução.

### Rodada corrigida

No head `f5e57db5c7fd1fdd21385eaa3f5f6aa07fcaa0a5`:

- CI geral `34876036424`: `success`;
- V00 `34876036437`: `success`;
- V01 `34876036418`: `success`;
- V02 `34876036413`: `success`.

O README foi corrigido apenas para os valores medidos `1368` e `1859`; nenhum validador foi relaxado.

**Status:** PASS no snapshot `f5e57db5...`. As atualizações finais destes documentos de gate devem receber nova rodada de CI; o aceite permanece proibido enquanto o head corrente não estiver verde.

## T11 — Auditoria independente A1

Pacote reproduzível:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`.

A sessão implementadora não se autoqualifica como auditor independente.

**Status:** PREPARADA, NÃO EXECUTADA.

## T12 — Contexto canônico

**Esperado:** `CLAUDE.md` reflete a `main` vigente e não transforma ADR proposto em decisão ativa.

**Observado:** `CLAUDE.md` registra V00–V08 como integradas, V09 não iniciada, MM00 como proposta e ADR-0014 a ADR-0020 como propostos. O índice de ADRs mantém os mesmos status.

**Status:** PASS documental, sujeito à A1.

## T13 — Regra de changelog

`CLAUDE.md` exige entrada em `CHANGELOG.md` para toda sessão que altera algo.

A reconciliação com a `main` preservou integralmente o `CHANGELOG.md` oficial da V08. A entrada própria da MM00 ainda não foi adicionada. A interface disponível nesta sessão oferece substituição integral para esse arquivo histórico extenso, sem operação de patch/append segura; reescrever o histórico apenas para marcar o gate seria um risco maior.

**Status:** BLOQUEIO CONHECIDO. Requer atualização aditiva segura antes do aceite, ou exceção humana explícita e registrada.

## Critério final

PASS global exige T01–T13 resolvidos, diff da MM00 delimitado contra a `main` vigente, CI verde no head corrente, auditoria independente registrada e checkpoint reconciliado.

Neste momento, os bloqueios deliberados são T11 (A1 independente) e T13 (changelog próprio da MM00), além da revalidação automática do head após esta atualização documental.
