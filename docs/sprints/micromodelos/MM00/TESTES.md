# MM00 — Testes e evidências

## Objetivo

MM00 é uma sprint documental/arquitetural. Os testes verificam baseline, ausência de deriva funcional, coerência cruzada e capacidade de avançar com segurança; não homologam Databricks nem executam micromodelos.

## T01 — Baseline Git

**Esperado:** branch MM00 parte da `main` vigente.

**Observado na abertura:** `micromodelos/mm00-baseline` e `main` apontavam para `1b6632194f4b25afc09960c27b069c16df365ee6`.

**Revalidação durante a execução:** a `main` continuava no mesmo SHA após a criação da PR e do pacote de auditoria.

**Status:** PASS até o head atual. Revalidar uma última vez antes do aceite/merge.

## T02 — Estado visual

**Esperado:** plano não depender de fotografia desatualizada.

**Observado:** V00–V07 estão integradas; V08 ainda não iniciada no baseline. A V07 preserva cálculo/semântica e acrescenta rotas visuais opt-in.

**Ação executada:** `CLAUDE.md` foi reconciliado para remover o estado obsoleto de V05 candidata e apontar o estado vigente V07/V08, sem alteração da implementação visual.

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

**Status:** PASS documental no diff examinado até o head atual. A auditoria independente deve tentar quebrar esta afirmação.

## T07 — Migração tardia

**Esperado:** nenhuma skill/briefing de migração deve ser criado antes do piloto greenfield e freeze V1.

**Evidência:** Plano Mestre posiciona migração em MM12; ADR-0018 mantém o gate como decisão proposta.

**Status:** PASS documental.

## T08 — Tracking separado da especificação

**Esperado:** YAML define política/identidade; MLflow guarda histórico de runs; dados individuais permanecem fora do tracking.

**Evidência:** Plano Mestre e ADR-0016 proposto.

**Status:** PASS arquitetural; implementação só em sprint futura.

## T09 — Não alteração funcional

**Esperado:** MM00 não modifica `ambiente_fonte/.assistant/`, helpers/skills, `tools/` ou workflows.

**Executado:** comparação da candidata contra a base e listagem nominal da PR #43.

**Observado:** o primeiro commit modificou apenas `docs/`; a reconciliação posterior alterou apenas `CLAUDE.md`; o pacote de auditoria adicionou somente `docs/auditoria/`. Nenhum arquivo do produto funcional, ferramenta ou workflow foi alterado.

**Status:** PASS no head atual. Revalidar após qualquer commit adicional.

## T10 — Validação automática

A PR #43 disparou os workflows permanentes. No primeiro head, V00, V01 e V02 concluíram com `success` enquanto o CI geral ainda executava. O head posterior reexecutou os checks por causa da reconciliação documental e do pacote de auditoria.

**Status:** EM EXECUÇÃO no head atual. Registrar conclusões finais antes do checkpoint de aceite. CI verde cobre apenas contratos automatizados; não substitui auditoria independente.

## T11 — Auditoria independente A1

O pacote reproduzível foi criado em:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`.

O prompt contém doze testes obrigatórios e bloqueia histórico/justificativas antes da formação dos achados.

**Status:** PREPARADA, NÃO EXECUTADA. A sessão implementadora não se autoqualifica como auditor independente. MM00 não fecha sem o parecer ou sem decisão explícita de exceção ao gate.

## T12 — Contexto canônico

**Esperado:** o arquivo canônico não induz novas sessões a trabalhar com estado visual obsoleto e não transforma ADR proposto em ativo.

**Executado:** atualização de `CLAUDE.md` na branch.

**Observado:** V00–V07 aparecem como integradas, V08 como não iniciada; ADRs 0014–0020 estão rotulados como propostos; MM01 permanece bloqueada; números pós-R13 de cobertura são tratados como históricos, não como medida corrente.

**Status:** PASS documental no head atual.

## T13 — Regra de changelog

`CLAUDE.md` exige entrada em `CHANGELOG.md` para toda sessão que altera algo.

**Status:** PENDENTE no head atual. A candidata não deve ser aceita enquanto a entrada aditiva da MM00 não estiver registrada sem reescrever o histórico existente.

## Critério final

PASS global exige T01–T13 resolvidos, nenhuma mudança funcional escondida, auditoria independente registrada e checkpoint atualizado com evidências do head final.
