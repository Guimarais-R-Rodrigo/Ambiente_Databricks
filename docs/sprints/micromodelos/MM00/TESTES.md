# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git

**Esperado:** branch MM00 parte da `main` vigente.

**Observado na abertura:** `micromodelos/mm00-baseline` e `main` apontavam para `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Status:** PASS na abertura. Revalidar antes do fechamento.

## T02 — Estado visual

**Esperado:** plano não depender de fotografia desatualizada.

**Observado:** V00–V07 estão integradas; V08 ainda não iniciada no baseline. A V07 preserva cálculo/semântica e acrescenta rotas visuais opt-in.

**Status:** PASS para a decisão de desacoplar o visual até MM11.

## T03 — Colisão nominal

**Método:** busca por `micromodel` na `main`.

**Observado:** nenhum resultado específico encontrado.

**Status:** PASS. Isso não prova inexistência fora do repositório.

## T04 — Taxonomia do Hub

**Esperado:** micromodelo não vira sétimo tipo.

**Evidência:** `hub_padroes/skill/template.md` e `hub-ml-criar-objeto` tratam a lista de seis tipos como fechada.

**Status:** PASS.

## T05 — Reuso de componentes

**Esperado:** plano deve mapear skills/helpers existentes antes de propor novos objetos.

**Evidência:** `MATRIZ_REUSO.md` classifica Concierge, EDA, cross-EDA, feature engineering, validação, auditoria, `schema_to_yaml`, helpers Spark e `mlflow_run`.

**Status:** PASS documental.

## T06 — Sanitização

**Esperado:** nenhum identificador/path real do ambiente externo deve ser necessário ao framework versionado.

**Evidência:** plano e MM00 usam placeholders; nenhuma fixture real foi adicionada.

**Status:** PASS documental. Revalidar no diff final.

## T07 — Migração tardia

**Esperado:** nenhuma skill/briefing de migração deve ser criado antes do piloto greenfield e freeze V1.

**Evidência:** Plano Mestre posiciona migração em MM12.

**Status:** PASS documental.

## T08 — Tracking separado da especificação

**Esperado:** YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking.

**Evidência:** Plano Mestre e ADR correspondente.

**Status:** PASS arquitetural; implementação só em sprint futura.

## T09 — Não alteração funcional

**Esperado:** MM00 não modifica `ambiente_fonte/.assistant/` nem helpers/skills.

**Como validar no fechamento:** comparar arquivos alterados da PR. Qualquer mudança no produto funcional reprova MM00 salvo correção explícita de escopo aprovada.

**Status:** PENDENTE até diff final.

## T10 — Validação automática

Após a criação da PR, registrar os checks disparados no head da branch. CI verde prova apenas os contratos cobertos pelos workflows; não substitui auditoria independente.

**Status:** PENDENTE.

## T11 — Auditoria independente A1

Usar o padrão de `hub_padroes/auditoria/template.md` em sessão independente, bloqueando histórico/raciocínio da sprint e pedindo ao auditor para reconstruir as fronteiras a partir dos arquivos finais.

**Status:** PENDENTE. MM00 não fecha sem execução ou registro explícito de bloqueio aceito.

## Critério final

PASS global exige T01–T11 resolvidos, nenhuma mudança funcional escondida e checkpoint atualizado com evidências do head final.
