# Prompt: pipeline de dados com Lakeflow

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe fontes, schema, pipeline e
> repositório com **Add context**/`@`. Skill: `@hub-ml-pipeline-builder`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-pipeline-builder/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers) é o catálogo integrado.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{OBJETIVO_CONSUMIDORES}}` | Descreva produto, decisão e consumidores. | Define contrato e criticidade. | silver de eventos para risco |
| `{{FONTES}}` | Liste origem, formato, cadência e chegada. | Determina ingestão e idempotência. | JSON em volume; microbatch |
| `{{DESTINOS}}` | Informe tabela, grão e particionamento. | Evita escrita no destino errado. | `main.silver.eventos`; um evento |
| `{{MODO}}` | Escolha batch, streaming ou CDC com razão. | Muda estado, custo e recuperação. | CDC com CDF |
| `{{CHAVES_SEQUENCIA}}` | Defina chave, ordenação e desempate. | Evita duplicata e atualização fora de ordem. | `id_evento`; `ts_update`, versão |
| `{{SCHEMA_EVOLUCAO}}` | Declare schema, compatibilidade e ação. | Evita aceitar mudança silenciosa. | nova coluna nullable; tipo bloqueia |
| `{{REGRAS_QUALIDADE}}` | Liste regra, severidade e ação. | Expectations sem ação não governam. | chave nula: quarantine |
| `{{SLO_VOLUME_FREQUENCIA}}` | Informe latência, volume e cadência. | Dimensiona desenho e alertas. | p95 < 15 min; 20M/dia |
| `{{DEV_STAGE_PROD}}` | Mapeie catálogos e permissões por ambiente. | Evita deploy cruzado. | dev=`dev`, prod=`main` |
| `{{RESTRICOES}}` | Declare PII, grants e limites operacionais. | Previne exposição e privilégio excessivo. | mascarar CPF; sem alterar grants |
| `{{ARQUITETURA_CODIGO_OU_DEPLOY_AUTORIZADO}}` | Escolha arquitetura, código ou deploy autorizado. | Separa proposta de mudança externa. | bundle sem deploy |

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

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Gere o bundle com targets dev/stage/prod, sem deploy.”
- “Adicione expectations e testes para duplicata, nulo e late data.”
- “Revise o event log e proponha alertas operacionais.”

## Referências oficiais Azure Databricks

- [Lakeflow Spark Declarative Pipelines — melhores práticas](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices)
- [Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
