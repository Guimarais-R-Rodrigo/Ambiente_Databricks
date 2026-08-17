---
name: hub-ml-baseline-ml
description: Treina e compara baselines reproduzíveis de machine learning no Databricks para classificação, regressão, séries temporais, ranking, survival, clustering e detecção de anomalias, com splits anti-leakage, MLflow, métricas condicionais e handoff para explicabilidade/monitoramento. Usar quando pedirem baseline, primeiro modelo, benchmark, scorecard, LightGBM/XGBoost/CatBoost, forecasting, clustering, ranking, survival, anomaly detection, deep learning tabular ou comparação de modelos.
---

# Construir baseline de ML

## Firmar o contrato

Antes do treino, registrar:

- decisão suportada e custo dos erros;
- unidade de predição, target e horizonte;
- instante de decisão e data de corte;
- população, exclusões e peso amostral;
- chave de entidade e coluna temporal;
- estratégia de split;
- métrica primária, guardrails e baseline trivial;
- ambiente, dependências e restrições de compute.

Sem target ou contrato temporal, não executar suite supervisionada como se estivesse pronta.

## Selecionar a suite

Escolher explicitamente, sem auto-detecção silenciosa:

| Suite | Caso | Baseline mínimo |
|---|---|---|
| B1 tabular | classificação/regressão | trivial + modelo linear/árvore simples |
| B1 scorecard | probabilidade binária com transparência | regressão logística; WoE opcional |
| B2 temporal | previsão por tempo | naïve/seasonal naïve + modelo candidato |
| B3 deep learning | sinal tabular complexo e escala justificável | comparar com B1 nas mesmas divisões |
| B4 clustering | segmentação sem label | solução simples + estabilidade/perfil |
| B5 ranking | itens agrupados por query/cliente | regra simples + ranker com grupos válidos |
| B6 survival | tempo até evento com censura | Kaplan-Meier + Cox/modelo candidato |
| B7 anomalia | eventos raros sem labels confiáveis | regra robusta + Isolation Forest/candidato |

Se várias suites forem plausíveis, explicar a escolha e manter a comparação justa.

## Dividir sem leakage

1. Escolher split aleatório estratificado somente quando tempo e entidade não vazarem.
2. Preferir out-of-time quando o uso futuro depender de estabilidade temporal.
3. Agrupar entidades quando registros do mesmo cliente/contrato não puderem cruzar splits.
4. Aplicar gap por tempo real, não por número de linhas.
5. Ajustar preprocessamento, seleção, binning e calibradores apenas no treino.
6. Particionar lags/janelas por entidade e limitar à informação anterior à previsão.
7. Manter teste intocado até a seleção final.

## Controlar escala

Executar preparação e agregação no Spark. Converter para pandas/NumPy somente após estimar memória e limitar/amostrar explicitamente com seed. Não usar `toPandas()` direto por uma contagem arbitrária de milhões de linhas.

Registrar biblioteca e versão. Instalar dependências com mecanismo compatível com o compute; em serverless, confirmar as práticas atuais de dependências na documentação oficial.

## Treinar e comparar

1. Implementar baseline trivial coerente com o problema.
2. Criar pipeline de preprocessamento reproduzível.
3. Treinar um modelo simples antes de tuning.
4. Usar validação compatível com tempo, grupo e censura.
5. Ajustar hiperparâmetros somente na validação/CV; passar `early_stopping` somente quando a biblioteca realmente o suporta.
6. Avaliar treino, validação e teste com mesma população e definição.
7. Quantificar incerteza ou variabilidade quando material.
8. Escolher pelo objetivo, guardrails, estabilidade, custo e interpretabilidade; não por uma métrica isolada.

## Usar métricas apropriadas

### Classificação

Reportar prevalência, AUC-ROC, AUC-PR, log loss/Brier quando houver probabilidade, calibração e métricas no threshold escolhido. AUC é a probabilidade de ordenar corretamente um par positivo-negativo, não percentual de casos acertados. Em uma única classe, não calcular métricas que exigem ambas.

### Regressão

Reportar MAE/RMSE e métrica alinhada ao negócio, distribuição dos resíduos e desempenho por faixa/segmento. Proteger divisões por zero em MAPE; preferir WAPE/MASE/sMAPE quando adequados.

### Séries temporais

Usar backtesting/walk-forward, baseline naïve e métricas fora da amostra. Não aprovar modelo com ajuste apenas in-sample. Validar frequência, gaps, sazonalidade e entidades.

### Ranking

Validar grupos contíguos/tamanhos e medir NDCG/MAP/Recall@k conforme relevância. Não reportar MAP se o código não o calculou.

### Clustering/anomalia

Combinar métricas internas com estabilidade, perfil e utilidade. Não inventar AUC sem labels. Tratar cluster de ruído (`-1`) separadamente.

### Survival

Validar duração positiva, evento binário, censura e pressuposto de riscos proporcionais quando usar Cox. Reportar C-index e, se possível, métricas dependentes do tempo com validação.

## Registrar no MLflow

Usar MLflow para registrar:

- parâmetros e versões de código/dependência;
- métricas e gráficos relevantes;
- dataset/snapshot e schema sem vazar PII;
- assinatura e exemplo de entrada seguro;
- artefato do pipeline completo;
- tags de suite, target, split, janela e owner;
- modelo em Models in Unity Catalog quando houver governança e promoção.

Confirmar as assinaturas da API MLflow atual antes de gerar código. Não registrar segredo nem amostra sensível. Separar tracking de promoção; não atribuir alias de produção automaticamente sem autorização.

## Usar templates sob demanda

- Seleção/split: [templates/suite_selection_guide.md](templates/suite_selection_guide.md), [templates/split_strategy.md](templates/split_strategy.md), [templates/walk_forward_guide.md](templates/walk_forward_guide.md)
- Métricas: [templates/metricas_classificacao.md](templates/metricas_classificacao.md), [templates/metricas_regressao.md](templates/metricas_regressao.md), [templates/metricas_series_temporais.md](templates/metricas_series_temporais.md), [templates/metricas_ranking.md](templates/metricas_ranking.md), [templates/survival_interpretation.md](templates/survival_interpretation.md)
- Suites: [templates/cluster_profiling.md](templates/cluster_profiling.md), [templates/anomaly_profiling.md](templates/anomaly_profiling.md), [templates/scorecard_report.md](templates/scorecard_report.md), [templates/score_bands_table.md](templates/score_bands_table.md)
- Operação/saída: [templates/mlflow_checklist.md](templates/mlflow_checklist.md), [templates/notebook_output_baseline.md](templates/notebook_output_baseline.md), [templates/relatorio_executivo_baseline.md](templates/relatorio_executivo_baseline.md)
- Deep learning: [templates/dl_vs_lgbm_justificativa.md](templates/dl_vs_lgbm_justificativa.md)

Tratar thresholds contidos nos templates como placeholders customizados, nunca como regra universal.

## Usar helpers da biblioteca

Importar de `hub_snippets` em vez de reimplementar a lógica. Catálogo completo: [CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md).

| Demanda | Módulo |
|---|---|
| Split temporal e validação walk-forward | `hub_snippets.ml.split_temporal`, `hub_snippets.ml.walk_forward` |
| Métricas de classificação e regressão | `hub_snippets.ml.metrics_report` |
| Curvas ROC, PR, lift e KS | `hub_snippets.ml.curves_plotly` |
| Treino com MLflow opcional | `hub_snippets.ml.train_lgbm`, `.train_xgboost`, `.train_catboost`, `.optuna_lgbm` |
| Registro com dataset, split, assinatura e limitações | `hub_snippets.ml.mlflow_run` (`run_governado`) |
| Scorecard e bandas de score | `hub_snippets.ml.scorecard_builder`, `hub_snippets.ml.score_bands` |
| Suites não tabulares | `hub_snippets.ml.lgbm_ranker`, `.clustering_suite`, `.isolation_forest`, `.survival_cox`, `.prophet_wrapper` |

`temporal_split` e `walk_forward_cv` operam em unidades de calendário; substituí-los por fatia de linhas reintroduz o leakage que eles evitam. Os wrappers de treino dependem de bibliotecas opcionais — confirmar instalação e versão fixada antes de prometer execução.

## Entregar

Fornecer notebook/código reproduzível, contrato, comparação com trivial, tabela de métricas, diagnóstico de leakage/overfit, registro MLflow, limitações e recomendação. Encaminhar `hub-ml-explainability` após escolher o candidato e `hub-ml-monitoramento-modelo` antes de produção.
