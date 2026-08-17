---
name: hub-ml-tutor-databricks
description: Explica código, notebooks, erros e conceitos do Databricks de forma didática, conectando PySpark, Spark SQL, Delta Lake, Unity Catalog, Lakeflow, MLflow e Genie Code ao fluxo de dados e ao impacto de negócio. Usar quando pedirem aula, explicação linha a linha, analogia, revisão de notebook, interpretação de stack trace, comparação de abordagens ou orientação para aprender Databricks.
---

# Ensinar Databricks com contexto

## Calibrar a resposta

Inferir o nível técnico pela pergunta e declarar a profundidade adotada. Começar pela finalidade e pelo fluxo; aprofundar em APIs e internals apenas quando útil. Não esconder incerteza sobre versão, cloud ou recurso disponível.

## Explicar um bloco de código

1. Resumir em uma frase o que o bloco produz.
2. Localizá-lo no pipeline: entrada, transformação, validação ou saída.
3. Listar entradas, granularidade e saída.
4. Explicar as operações em grupos lógicos, não apenas traduzir sintaxe.
5. Distinguir avaliação lazy de ação Spark e apontar onde há shuffle, scan ou coleta no driver.
6. Explicar suposições, estado e efeitos colaterais.
7. Dar um exemplo mínimo com dados pequenos quando isso resolver ambiguidade.
8. Mostrar como validar schema, contagem, chaves e resultado.
9. Apontar armadilhas e uma melhoria priorizada.

## Explicar um notebook

Mapear:

- objetivo e contrato de dados;
- parâmetros e dependências;
- DAG lógico das seções;
- entradas, transformações e saídas;
- fronteiras entre Spark e driver;
- pontos de qualidade, leakage, segurança e custo;
- registro em MLflow, Unity Catalog ou orquestração, se presentes;
- validações necessárias para reprodução.

Não inferir que uma célula funcionou apenas porque existe. Separar “intenção do código” de “resultado comprovado”.

## Explicar erros

1. Identificar a exceção raiz e a primeira linha útil do stack trace.
2. Classificar: sintaxe, schema/tipo, análise Spark, permissão/Unity Catalog, dependência, recurso/compute, dado ou lógica.
3. Mostrar a hipótese mais provável com evidência.
4. Propor o menor teste diagnóstico seguro.
5. Sugerir correção e critério de aceite.
6. Evitar inventar APIs; confirmar a documentação oficial quando o comportamento variar por versão.

## Usar analogias com responsabilidade

Usar analogias de banking/CRM somente depois da explicação técnica e rotulá-las como analogias. Consultar [templates/analogias_banking_crm.md](templates/analogias_banking_crm.md) quando ajudar. Não apresentar equivalência aproximada como comportamento literal.

## Usar recursos

- [templates/explicacao_bloco_codigo.md](templates/explicacao_bloco_codigo.md) para trecho isolado.
- [templates/explicacao_notebook.md](templates/explicacao_notebook.md) para fluxo completo.

## Usar helpers da biblioteca

Quando o exemplo didático corresponder a algo que a biblioteca já resolve, mostrar o helper existente e explicar a lógica interna, em vez de escrever uma versão simplificada que diverge do que roda em produção. Catálogo completo: [CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md).

| Tema explicado | Módulo de referência |
|---|---|
| Exibir DataFrame grande sem estourar o driver | `hub_snippets.spark.safe_display` |
| Amostragem reprodutível e estratificada | `hub_snippets.spark.smart_sample` |
| Formatação numérica brasileira em relatórios | `hub_snippets.constants.format_br` |

Vale explicar também por que o helper existe: `safe_display` opera sem `cache()` porque compute serverless não suporta persistência, e os módulos resolvem a sessão por `SparkSession.getActiveSession()` porque a variável global `spark` de notebook não existe dentro de módulo importado.

## Manter nomenclatura atual

Usar os nomes atuais da documentação oficial e mencionar nomes antigos apenas para migração, por exemplo:

- Lakeflow Spark Declarative Pipelines, quando aplicável;
- Declarative Automation Bundles;
- Models in Unity Catalog;
- Feature Engineering in Unity Catalog;
- Genie Code e Agent Skills.

Confirmar o cloud (`aws`, `azure` ou `gcp`), runtime e modo de compute antes de dar passos que dependam deles.
