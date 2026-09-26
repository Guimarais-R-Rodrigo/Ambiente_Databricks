---
name: hub-ml-pipeline-builder
description: Desenha e implementa pipelines de dados e ML no Databricks com arquitetura bronze/silver/gold quando adequada, Lakeflow Spark Declarative Pipelines, Lakeflow Jobs, Delta Lake, Unity Catalog, serverless e Declarative Automation Bundles. Usar quando pedirem pipeline, ingestão incremental, medallion, expectations, orquestração, job, bundle, CI/CD, deploy dev/staging/prod, feature/scoring pipeline ou migração de DLT/Asset Bundles.
---

# Construir pipelines Databricks

## Quando esta skill se aplica

- Pedem **pipeline, ingestão incremental, medallion, expectations, orquestração,
  job, bundle, CI/CD ou deploy** dev/staging/prod.
- O produto é **infraestrutura que roda sozinha**, não uma análise que alguém lê.

**Não cobre:** construir as features que o pipeline materializa
(`hub-ml-feature-engineering`) nem decidir o que monitorar depois que ele está de
pé (`hub-ml-monitoramento-modelo`).


## Escolher a arquitetura

Confirmar cloud, região, workspace, Unity Catalog, origem, SLA, volume, latência, frequência, política de reprocessamento e ambientes. Usar medallion apenas quando suas fronteiras melhorarem qualidade, reuso ou governança; não criar camadas vazias.

Preferir:

- **Lakeflow Spark Declarative Pipelines** para fluxos declarativos, incrementais, streaming tables/materialized views e expectations;
- **Lakeflow Jobs** para orquestrar notebooks, scripts, SQL, pipelines e tarefas ML;
- **Declarative Automation Bundles** para versionar, validar e implantar recursos por ambiente;
- **serverless** quando suportado e compatível com requisitos, conforme recomendação oficial atual;
- **Unity Catalog** para nomes, permissões, linhagem e artefatos governados.

Mencionar Delta Live Tables ou Databricks Asset Bundles somente como nomenclaturas anteriores durante migração.

## Definir contratos por camada

- **Bronze:** preservar dados brutos, metadados de ingestão e capacidade de replay.
- **Silver:** normalizar schema, deduplicar com regra determinística, aplicar qualidade e conformar entidades.
- **Gold:** publicar dados de consumo com granularidade e contrato explícitos.
- **Features/scoring:** garantir point-in-time, versão do modelo, rastreabilidade e idempotência.

Para cada dataset, documentar owner, schema, chave, event time, frequência, SLA, regras de qualidade e consumidores.

## Implementar incrementalmente

1. Escolher batch/streaming pela semântica, não pela preferência.
2. Usar Auto Loader ou mecanismo oficial compatível para ingestão incremental de arquivos quando aplicável.
3. Definir checkpoint e schema location em storage governado; não em caminhos efêmeros.
4. Tratar deduplicação com chave e tempo, incluindo chegada tardia.
5. Usar MERGE somente com condição e chave determinísticas.
6. Preservar histórico quando o caso exige; não sobrescrever silenciosamente.
7. Implementar backfill e replay parametrizados e testáveis.

## Aplicar qualidade

Em Lakeflow Spark Declarative Pipelines, usar expectations com ação coerente: observar, descartar ou falhar. Não inventar uma API. Confirmar os decorators e imports atuais na documentação do cloud/runtime antes de escrever código.

Classificar regras por severidade e registrar volume afetado. Não descartar registro crítico sem tabela/quarentena ou evidência suficiente para investigação.

## Automatizar ambientes

No bundle:

- declarar recursos, variáveis e targets `dev`, `staging` e `prod`;
- separar identidade, catálogo/schema e compute por target;
- usar secrets/scopes ou credenciais oficiais, nunca valores no YAML;
- executar `databricks bundle validate`, `deploy` e testes de smoke antes de `run` em produção;
- manter lockfile/dependências e permissões explícitas;
- promover o mesmo código e variar configuração.

## Observar e operar

Monitorar event log/pipeline events, duração, freshness, backlog, falhas, volume e expectativas. Definir retry, timeout, alertas, owner, runbook e critério de rollback. Para scoring, registrar modelo, versão/alias, snapshot de features e população.

## Entregar

Produzir:

- diagrama/DAG e contratos;
- layout do repositório e bundle;
- código implementável por recurso;
- regras de qualidade;
- estratégia de backfill e recuperação;
- matriz de ambientes/permissões;
- testes e checklist de implantação;
- runbook operacional.

Usar [templates/pipeline_spec.md](templates/pipeline_spec.md) como spec editável. Adaptar recursos às capacidades oficiais disponíveis e registrar qualquer componente customizado.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Unicidade de chave, nulos e freshness | `hub_scripts.data_quality_check` |
| Schema documentado como contrato de camada | `hub_scripts.schema_to_yaml` |
| Conferir convenção de nomes do projeto | `hub_scripts.naming_checker` |
| Inspecionar amostra sem varredura completa | `hub_snippets.spark.safe_display` |

Esses helpers servem a diagnóstico e prototipação. Em pipeline, a regra de qualidade deve ser declarada como expectation do Lakeflow e monitorada pelo event log, não executada como script avulso. `naming_checker` aplica política do projeto, não requisito da Databricks.

## Evitar erros comuns

- Não usar `F.col(data).max()`; usar agregação `F.max(F.col(data))` quando necessário.
- Não coletar dados de pipeline no driver.
- Não confundir idempotência com overwrite completo.
- Não colocar caminhos pessoais, tokens ou e-mails no código.
- Não chamar pasta customizada de recurso nativo do Genie Code.
