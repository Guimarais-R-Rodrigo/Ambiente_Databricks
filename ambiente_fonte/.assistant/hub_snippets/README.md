# Hub Snippets — catálogo e navegação

> Biblioteca customizada do Hub. Não é biblioteca institucional da Databricks e não é carregada automaticamente pela Genie Code.

Cada pasta de objeto mantém fachada, implementação, notebook de exemplo e, após a migração, um README didático. O README explica conceito e limites; a implementação continua sendo a fonte da assinatura executável. Para o inventário completo, consulte também `.assistant/MANUAL_TECNICO.md#catalogo-helpers`.

## Guias por leva

### R05 — modelos tabulares
[LightGBM](ml/train_lgbm/README.md) · [CatBoost](ml/train_catboost/README.md) · [LambdaRank](ml/lgbm_ranker/README.md) · [Optuna](ml/optuna_lgbm/README.md) · [MLP embeddings](ml/mlp_embeddings/README.md) · [TabNet](ml/tabnet_wrapper/README.md)

### R06 — séries e validação temporal
[ARIMA](ml/arima_wrapper/README.md) · [Features temporais](ml/lgbm_temporal/README.md) · [Prophet](ml/prophet_wrapper/README.md) · [Split temporal](ml/split_temporal/README.md) · [Walk-forward](ml/walk_forward/README.md)

### R07 — score, safra e sobrevivência
[Kaplan–Meier](ml/kaplan_meier/README.md) · [Bandas de score](ml/score_bands/README.md) · [Scorecard](ml/scorecard_builder/README.md) · [Cox PH](ml/survival_cox/README.md) · [Vintage](ml/vintage_analysis/README.md) · [WOE/IV](ml/woe_iv_calculator/README.md)

### R08 — clusters, anomalias e explicabilidade
[Autoencoder](ml/autoencoder_anomaly/README.md) · [Profiling](ml/cluster_profiling/README.md) · [Clustering](ml/clustering_suite/README.md) · [Relatório de explicabilidade](ml/explainability_report/README.md) · [SHAP](ml/shap_explainer/README.md) · [UMAP](ml/umap_viz/README.md)

### R09 — avaliação, drift e MLOps
- [Curvas ROC/PR/lift/KS](ml/curves_plotly/README.md) — figuras driver-side; `n` é metadado visual.
- [Drift de features](ml/drift_detection/README.md) — PSI, KS, CSI e classificação somente com política explícita.
- [Relatório de métricas](ml/metrics_report/README.md) — classificação/regressão; `ks_pct` em escala 0–100.
- [Run MLflow governado](ml/mlflow_run/README.md) — registro fail-closed com efeito externo.
- [Monitor de performance](ml/performance_monitor/README.md) — histórico em memória e candidato a investigação, sem retreino automático.

## Mapa funcional resumido

- `ml`: modelagem, avaliação, explicabilidade, monitoramento e estatística aplicada.
- `spark`: operações distribuídas e qualidade/diagnóstico de dados.
- `display` e `visual`: apresentação e identidade visual.
- `constants`: constantes compartilhadas.
- `testing`: fixtures e dados sintéticos.

## Regras de interpretação

1. “Testado” significa cenário e runtime delimitados, não garantia universal.
2. Driver-side exige controle consciente do volume antes de coletar dados Spark.
3. Métrica, drift, explicabilidade e monitoramento são evidências diferentes.
4. Nenhum helper aprova automaticamente modelo, política, publicação ou retreino.
5. `Novo_Ambiente_Simulado` é derivado do `ambiente_fonte`; não o edite como fonte canônica.
