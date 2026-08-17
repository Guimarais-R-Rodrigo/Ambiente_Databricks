# Prompt: pipeline de dados com Lakeflow

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe fontes, schema, pipeline e
> repositório com **Add context**/`@`. Skill: `@hub-ml-pipeline-builder`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Prompt pronto para colar

```text
Use @hub-ml-pipeline-builder para desenhar um pipeline Databricks atual, testável e
operável. Não crie, implante nem execute recursos até eu autorizar explicitamente.

BRIEFING
- Objetivo e consumidores: {{OBJETIVO_CONSUMIDORES}}
- Fontes/formato/modo de chegada: {{FONTES}}
- Destinos e granularidade: {{DESTINOS}}
- Batch/streaming/CDC: {{MODO}}
- Chaves e ordenação/sequência: {{CHAVES_SEQUENCIA}}
- Schema e evolução esperada: {{SCHEMA_EVOLUCAO}}
- Regras de qualidade: {{REGRAS_QUALIDADE}}
- SLA/SLO, volume e frequência: {{SLO_VOLUME_FREQUENCIA}}
- Ambientes/catálogos: {{DEV_STAGE_PROD}}
- Segurança/PII/permissões: {{RESTRICOES}}
- Modo de entrega: {{ARQUITETURA_CODIGO_OU_DEPLOY_AUTORIZADO}}

FLUXO
1. Confirme fontes, contratos, owners, checkpoint/estado e semântica de reprocessamento.
2. Proponha arquitetura proporcional ao caso. Use Lakeflow Spark Declarative
   Pipelines quando adequado e explique a escolha; não force streaming sem necessidade.
3. Defina idempotência, deduplicação, late data, evolução de schema, quarantine,
   qualidade e recuperação. Expectations devem ter ação explícita e justificativa.
4. Proponha Declarative Automation Bundles para versionar recursos e targets de
   ambiente quando houver ciclo de deploy. Valide antes de implantar.
5. Recomende serverless para novos pipelines quando suportado pelo caso, declarando
   requisitos/limitações; não invente disponibilidade regional ou permissões.
6. Inclua observabilidade pelo event log, métricas, alertas e runbook.
7. Não grave no destino, não faça deploy, não altere grants e não inicie pipeline
   sem mostrar diff/plano, ambiente alvo e impacto e obter autorização.

CONTRATO DE SAÍDA
- Arquitetura e fluxo bronze/silver/gold somente onde agregar valor.
- Contratos de input/output, chaves, watermark/CDC e qualidade.
- Árvore do projeto e recursos do bundle, se aplicável.
- Código/configuração propostos e testes.
- Plano de deploy dev→stage→prod, rollback, observabilidade e custo.

VALIDAÇÃO FINAL
- Teste duplicatas, atraso, reprocessamento, schema novo e falha parcial.
- Confirme que writes são idempotentes e destinos/ambientes são parametrizados.
- Separe recurso documentado da Databricks de convenção personalizada do projeto.
```

## Exemplo mínimo

Fonte = arquivos JSON incrementais; destino = tabela silver por evento; modo =
streaming; chave = id_evento; sequência = ts_atualizacao; entrega = arquitetura + código.

## Follow-ups úteis

- “Gere o bundle com targets dev/stage/prod, sem deploy.”
- “Adicione expectations e testes para duplicata, nulo e late data.”
- “Revise o event log e proponha alertas operacionais.”

## Referências oficiais Azure Databricks

- [Lakeflow Spark Declarative Pipelines — melhores práticas](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices)
- [Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
