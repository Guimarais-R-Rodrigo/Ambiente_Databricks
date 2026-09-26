# Categoria `ml` — Machine Learning e estatística aplicada

<!-- readme-categoria: 1.0.0 -->

É a maior categoria do Hub: modelos, séries temporais, avaliação, explicabilidade, sobrevivência, drift, score, clustering, anomalias e utilitários de MLOps.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre os guias locais já validados; a implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Entre aqui quando a pergunta for de modelagem, validação, métrica, explicabilidade, coorte, detecção de anomalia ou monitoramento de modelo.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Objetos disponíveis

| Objeto | Papel resumido | Documentação |
|---|---|---|
| [`arima_wrapper`](arima_wrapper/README.md) | auto-ARIMA como candidato de previsão, não como validação automática | [guia local](arima_wrapper/README.md) |
| [`autoencoder_anomaly`](autoencoder_anomaly/README.md) | erro de reconstrução para priorizar anomalias, não veredito automático | [guia local](autoencoder_anomaly/README.md) |
| [`cluster_profiling`](cluster_profiling/README.md) | descrever clusters por médias e desvios sem inventar personas | [guia local](cluster_profiling/README.md) |
| [`clustering_suite`](clustering_suite/README.md) | comparar agrupamentos e selecionar configuração sem tratar heurística como verdade | [guia local](clustering_suite/README.md) |
| [`curves_plotly`](curves_plotly/README.md) | ROC, Precision-Recall, lift e KS em Plotly | [guia local](curves_plotly/README.md) |
| [`drift_detection`](drift_detection/README.md) | PSI, KS e CSI com política de classificação explícita | [guia local](drift_detection/README.md) |
| [`explainability_report`](explainability_report/README.md) | transformar importâncias em texto executivo/técnico sem confundir explicação com causa | [guia local](explainability_report/README.md) |
| [`isolation_forest`](isolation_forest/README.md) | encontrar observações incomuns para investigar | [guia local](isolation_forest/README.md) |
| [`kaplan_meier`](kaplan_meier/README.md) | sobrevivência e comparação de grupos com censura explícita | [guia local](kaplan_meier/README.md) |
| [`lgbm_ranker`](lgbm_ranker/README.md) | ordenar alternativas dentro de grupos com LambdaRank e NDCG | [guia local](lgbm_ranker/README.md) |
| [`lgbm_temporal`](lgbm_temporal/README.md) | engenharia de features temporais por observação e entidade | [guia local](lgbm_temporal/README.md) |
| [`metrics_report`](metrics_report/README.md) | métricas padronizadas para classificação binária e regressão | [guia local](metrics_report/README.md) |
| [`mlflow_run`](mlflow_run/README.md) | contexto governado para registro mínimo obrigatório no MLflow | [guia local](mlflow_run/README.md) |
| [`mlp_embeddings`](mlp_embeddings/README.md) | MLP binária com representações aprendidas para categorias indexadas | [guia local](mlp_embeddings/README.md) |
| [`optuna_lgbm`](optuna_lgbm/README.md) | pesquisar hiperparâmetros do LightGBM sem confundir busca com teste final | [guia local](optuna_lgbm/README.md) |
| [`performance_monitor`](performance_monitor/README.md) | métricas periódicas contra política explícita | [guia local](performance_monitor/README.md) |
| [`prophet_wrapper`](prophet_wrapper/README.md) | forecast com tendência, sazonalidade e calendário sob validação temporal | [guia local](prophet_wrapper/README.md) |
| [`score_bands`](score_bands/README.md) | bandas quantílicas para diagnóstico de score, não política de aprovação pronta | [guia local](score_bands/README.md) |
| [`scorecard_builder`](scorecard_builder/README.md) | converter log-odds em pontos sem confundir escala com probabilidade | [guia local](scorecard_builder/README.md) |
| [`shap_explainer`](shap_explainer/README.md) | calcular atribuições SHAP com saída/classe explícita e limites de custo | [guia local](shap_explainer/README.md) |
| [`split_temporal`](split_temporal/README.md) | treino, validação e teste por períodos observados, com gaps explícitos | [guia local](split_temporal/README.md) |
| [`survival_cox`](survival_cox/README.md) | associações de risco relativo sob o pressuposto de riscos proporcionais | [guia local](survival_cox/README.md) |
| [`tabnet_wrapper`](tabnet_wrapper/README.md) | TabNet tabular com classificação/regressão e importância global do modelo | [guia local](tabnet_wrapper/README.md) |
| [`train_catboost`](train_catboost/README.md) | baseline de boosting com tratamento explícito de variáveis categóricas | [guia local](train_catboost/README.md) |
| [`train_lgbm`](train_lgbm/README.md) | baseline LightGBM para comparar modelos tabulares com um contrato explícito | [guia local](train_lgbm/README.md) |
| [`train_xgboost`](train_xgboost/README.md) | aprender a prever com árvores, sem confundir treino com validação | [guia local](train_xgboost/README.md) |
| [`umap_viz`](umap_viz/README.md) | projeção UMAP para exploração visual de clusters, não prova de separação | [guia local](umap_viz/README.md) |
| [`vintage_analysis`](vintage_analysis/README.md) | maturação por safra sem preencher o que ainda não foi observado | [guia local](vintage_analysis/README.md) |
| [`walk_forward`](walk_forward/README.md) | múltiplos cortes temporais com janela de treino expansiva | [guia local](walk_forward/README.md) |
| [`woe_iv_calculator`](woe_iv_calculator/README.md) | WOE/IV distribuído como diagnóstico, não selo automático de qualidade | [guia local](woe_iv_calculator/README.md) |

## Cuidados da categoria

Objetos diferentes respondem perguntas diferentes. Métrica, explicação, drift, causalidade e aprovação de produção não são equivalentes.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 30 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/ml/`.
