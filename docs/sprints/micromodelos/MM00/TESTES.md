# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git e reconciliação

**Abertura:** `micromodelos/mm00-baseline` nasceu da `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Evento concorrente:** durante a execução, a V08 foi integrada na `main` pelo commit `622d2c962a80998cf990b57036f7ae503bfc0458`.

**Reconciliação:** a branch MM00 incorporou a nova `main` por merge de dois pais no commit `e322e73fc0dc73c3081c99662ac29cb7721add67`, preservando os arquivos funcionais da V08 e os documentos MM00.

**Status:** PASS para a reconciliação estrutural. Revalidar `main` antes do aceite/merge final.

## T02 — Estado visual

**Esperado:** o plano não pode depender de fotografia desatualizada de outra frente.

**Observado:** V00–V08 estão integradas no Git. V08 alinha skills, padrões, entrada `.assistant`, template EDA e Manual ao Sistema de Temas sem alterar runtime Python.

**Conclusão:** o framework de micromodelos deve respeitar essa integração transversal desde a criação de suas futuras skills, mas a composição visual específica continua adiada para MM11.

**Status:** PASS arquitetural após reconciliação; nova auditoria independente deve validar a interpretação.

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

**Status:** PASS documental; auditor A1 deve confirmar contratos citados contra a árvore pós-V08.

## T06 — Sanitização

**Esperado:** nenhum identificador/path real do ambiente externo no framework versionado.

**Primeira rodada:** o CI detectou um handle corporativo histórico no ADR-0017.

**Correção:** o handle foi removido e substituído por contrato genérico de handoff. O CI do head `4c162436b6947681e58ea94f342d0acf11399688` passou após a correção.

**Status:** PASS naquele head; reexecutar no head reconciliado com V08.

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

**Observado antes da reconciliação V08:** a PR MM00 alterava apenas `CLAUDE.md`, `README.md`, ADRs e documentação MM00/auditoria.

**Após a reconciliação:** a branch contém alterações funcionais da V08 porque elas já são parte da nova `main`, não porque a MM00 as criou. O diff relevante para escopo deve ser calculado contra a `main` reconciliada, não contra a base histórica V07.

**Status:** PENDENTE de nova listagem/diff contra a `main` pós-V08.

## T10 — Validação automática

### Head pré-reconciliação V08

No head `4c162436b6947681e58ea94f342d0acf11399688`:

- V00: success;
- V01: success;
- V02: success;
- CI geral `34872513600`: success.

Isso comprovou a correção dos failures anteriores de sanitização e métricas do README naquele snapshot.

### Head reconciliado V08

A incorporação da V08 muda a contagem e amplia os workflows aplicáveis. O gate precisa ser executado novamente sobre o head pós-reconciliação; resultados antigos não são transferidos por inferência.

**Status:** PENDENTE de CI final.

## T11 — Auditoria independente A1

Pacote reproduzível:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`.

A sessão implementadora não se autoqualifica como auditor independente.

**Status:** PREPARADA, NÃO EXECUTADA.

## T12 — Contexto canônico

**Esperado:** `CLAUDE.md` reflete a `main` vigente e não transforma ADR proposto em decisão ativa.

**Ação:** a candidata será reconciliada para V00–V08 integradas e MM00/ADRs 0014–0020 em estado proposto.

**Status:** PENDENTE do commit documental pós-merge e CI.

## T13 — Regra de changelog

`CLAUDE.md` exige entrada em `CHANGELOG.md` para toda sessão que altera algo.

A `main` pós-V08 já traz a entrada da V08; a entrada própria da MM00 ainda não foi adicionada. A interface disponível nesta sessão oferece substituição integral para esse arquivo histórico extenso, sem patch/append seguro; a MM00 não deve arriscar reescrever o histórico apenas para marcar o checkbox.

**Status:** BLOQUEIO CONHECIDO. Requer atualização aditiva segura antes do aceite, ou decisão humana explícita de exceção documentada.

## Critério final

PASS global exige T01–T13 resolvidos, diff da MM00 delimitado contra a `main` vigente, CI verde no head final, auditoria independente registrada e checkpoint reconciliado.
