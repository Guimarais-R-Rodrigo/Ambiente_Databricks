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

**Observado na `main`:** V00–V07 estão integradas. Durante a execução da MM00 foi identificada a PR draft #42 para V08 em trabalho paralelo; portanto a afirmação anterior “V08 não iniciada” foi retirada dos documentos MM00. A MM00 só afirma que V08 ainda não está integrada na `main` e não presume o resultado da frente paralela.

**Ação executada:** `CLAUDE.md` havia sido reconciliado com V07; uma nova correção ainda precisa substituir a frase “V08 ainda não foi iniciada” por formulação compatível com a PR paralela.

**Status:** CORREÇÃO EM CURSO. A decisão arquitetural de desacoplar o visual até MM11 permanece válida.

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

**Primeiro CI:** o validador detectou um handle corporativo histórico dentro do ADR-0017. O trecho foi removido e substituído por descrição genérica do handoff institucional.

**Status:** CORRIGIDO; novo CI precisa confirmar.

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

**Observado:** os commits da MM00 alteram documentação, ADRs, `CLAUDE.md` e o pacote de auditoria. Nenhum arquivo do produto funcional, ferramenta ou workflow foi alterado.

**Status:** PASS no head atual. Revalidar após qualquer commit adicional.

## T10 — Validação automática

No head `5adcac3291ace7a9bcad5ef6201b75e4093d6cd4`:

- V00: `34871696028` — `success`;
- V01: `34871695981` — `success`;
- V02: `34871696024` — `success`;
- CI geral: `34871695827` — `failure` na etapa `validacao`.

O CI geral encontrou cinco falhas documentais: três no bloco de saída congelada do `README.md` raiz, porque a MM00 alterou a contagem do repositório; uma decorrente do próprio estado reprovado do bloco; e uma sanitização no ADR-0017. Os valores medidos naquele head foram `1363` arquivos e `1858` links fora da raiz. O ADR foi corrigido. O README raiz ainda precisa ser reconciliado sem relaxar o validador.

**Status:** FAIL CONHECIDO, CORREÇÃO EM CURSO. Não aceitar MM00 com esse CI vermelho.

## T11 — Auditoria independente A1

O pacote reproduzível foi criado em:

- `docs/auditoria/2026-09-14_micromodelos-mm00/01_contexto.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/02_prompt_auditoria.md`.

O prompt contém doze testes obrigatórios e bloqueia histórico/justificativas antes da formação dos achados.

**Status:** PREPARADA, NÃO EXECUTADA. A sessão implementadora não se autoqualifica como auditor independente. MM00 não fecha sem o parecer ou sem decisão explícita de exceção ao gate.

## T12 — Contexto canônico

**Esperado:** o arquivo canônico não induz novas sessões a trabalhar com estado visual obsoleto e não transforma ADR proposto em ativo.

**Executado:** atualização de `CLAUDE.md` na branch para retirar V05 candidata e registrar a iniciativa MM00 como proposta.

**Achado posterior:** a existência da PR draft V08 tornou a frase “V08 ainda não foi iniciada” imprecisa. A correção deve registrar apenas que V08 ainda não está integrada na `main` e que existe trabalho paralelo, sem presumir seu aceite.

**Status:** CORREÇÃO EM CURSO.

## T13 — Regra de changelog

`CLAUDE.md` exige entrada em `CHANGELOG.md` para toda sessão que altera algo.

**Status:** PENDENTE no head atual. A candidata não deve ser aceita enquanto a entrada aditiva da MM00 não estiver registrada sem reescrever o histórico existente.

## Critério final

PASS global exige T01–T13 resolvidos, nenhuma mudança funcional escondida, auditoria independente registrada e checkpoint atualizado com evidências do head final.
