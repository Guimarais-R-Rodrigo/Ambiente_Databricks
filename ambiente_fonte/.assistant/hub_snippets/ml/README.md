# Categoria `ml` — Machine Learning e estatística aplicada

<!-- readme-categoria: 1.0.0 -->

É a maior categoria do Hub: modelos, séries temporais, avaliação, explicabilidade, sobrevivência, drift, score, clustering, anomalias e utilitários de MLOps.

Este é um **índice de categoria**, não um README de objeto. Ele organiza a navegação entre guias locais revisados; essa revisão documental não comprova execução no seu runtime. A implementação continua definida pelos módulos Python e cada objeto mantém seu próprio exemplo.

## Quando começar por esta categoria?

Entre aqui quando a pergunta for de modelagem, validação, métrica, explicabilidade, coorte, detecção de anomalia ou monitoramento de modelo.

## Como escolher um objeto

1. Localize a necessidade na tabela abaixo.
2. Abra o **guia local** do objeto antes de importar ou executar.
3. Confira entradas, saídas, dependências, efeitos persistentes e limitações no README do objeto.
4. Só depois adapte o notebook de exemplo ao dado real.

## Percursos por tarefa

- Preparar e avaliar no tempo: [split_temporal](split_temporal/README.md), [lgbm_temporal](lgbm_temporal/README.md) e [walk_forward](walk_forward/README.md)
- Treinar e buscar configurações: baselines [LightGBM](train_lgbm/README.md), [XGBoost](train_xgboost/README.md), [CatBoost](train_catboost/README.md), [ranking](lgbm_ranker/README.md), [TabNet](tabnet_wrapper/README.md), [MLP](mlp_embeddings/README.md), [Optuna](optuna_lgbm/README.md), [ARIMA](arima_wrapper/README.md) e [Prophet](prophet_wrapper/README.md)
- Medir, explicar e comunicar: [metrics_report](metrics_report/README.md), [curves_plotly](curves_plotly/README.md), [SHAP](shap_explainer/README.md), [relatório de explicabilidade](explainability_report/README.md), [WOE/IV](woe_iv_calculator/README.md), [scorecard](scorecard_builder/README.md) e [bandas](score_bands/README.md)
- Agrupar, detectar e analisar maturidade: [clustering_suite](clustering_suite/README.md), [perfil de grupos](cluster_profiling/README.md), [Isolation Forest](isolation_forest/README.md), [autoencoder](autoencoder_anomaly/README.md), [UMAP](umap_viz/README.md), [Kaplan–Meier](kaplan_meier/README.md), [Cox](survival_cox/README.md) e [safras](vintage_analysis/README.md)
- Monitorar e registrar: [drift_detection](drift_detection/README.md), [performance_monitor](performance_monitor/README.md) e [mlflow_run](mlflow_run/README.md)

Uma trilha mínima de classificação temporal é `split_temporal` → `train_lgbm` → `metrics_report` → `shap_explainer` → `performance_monitor`. Primeiro reserve treino, validação e teste: early stopping/tuning podem usar a validação, mas o teste final deve permanecer separado dessas escolhas. Calcule SHAP com output e linhas alinhados; só monitore métricas com target realizado e períodos comparáveis. XGBoost/CatBoost são alternativas de baseline; walk-forward pode substituir a avaliação de corte único. Nenhuma seta executa a próxima etapa nem concede aprovação.

## Objetos disponíveis

| Objeto | Papel resumido | Execução | Dependência especial | Efeito do helper |
|---|---|---|---|---|
| [`arima_wrapper`](arima_wrapper/README.md) | auto-ARIMA como candidato de previsão, não como validação automática | Driver | pmdarima na chamada; MLflow no import | Tracking por padrão |
| [`autoencoder_anomaly`](autoencoder_anomaly/README.md) | erro de reconstrução para priorizar anomalias, não veredito automático | Driver CPU/CUDA | PyTorch | Tracking por padrão |
| [`cluster_profiling`](cluster_profiling/README.md) | descrever clusters por médias e desvios sem inventar personas | Driver | pandas/NumPy | Memória e stdout |
| [`clustering_suite`](clustering_suite/README.md) | comparar agrupamentos e selecionar configuração sem tratar heurística como verdade | Driver | scikit-learn; MLflow no import | Tracking por padrão |
| [`curves_plotly`](curves_plotly/README.md) | ROC, Precision-Recall, lift e KS em Plotly | Driver | Plotly/scikit-learn | Figura em memória |
| [`drift_detection`](drift_detection/README.md) | PSI, KS e CSI com política de classificação explícita | Driver | SciPy | Memória |
| [`explainability_report`](explainability_report/README.md) | transformar importâncias em texto executivo/técnico sem confundir explicação com causa | Driver | tabulate no resumo técnico; SciPy na comparação | Texto em memória |
| [`isolation_forest`](isolation_forest/README.md) | encontrar observações incomuns para investigar | Driver | scikit-learn; MLflow no import | Tracking por padrão |
| [`kaplan_meier`](kaplan_meier/README.md) | sobrevivência e comparação de grupos com censura explícita | Driver | Plotly no import; lifelines na chamada | Figura/dados em memória |
| [`lgbm_ranker`](lgbm_ranker/README.md) | ordenar alternativas dentro de grupos com LambdaRank e NDCG | Driver | LightGBM e MLflow no import | Tracking por padrão |
| [`lgbm_temporal`](lgbm_temporal/README.md) | engenharia de features temporais por observação e entidade | Driver | pandas/NumPy | Memória |
| [`metrics_report`](metrics_report/README.md) | métricas padronizadas para classificação binária e regressão | Driver | scikit-learn/SciPy | Memória |
| [`mlflow_run`](mlflow_run/README.md) | contexto governado para registro mínimo obrigatório no MLflow | Driver + backend | MLflow; flavor sklearn na rota de modelo | Registro persistente |
| [`mlp_embeddings`](mlp_embeddings/README.md) | MLP binária com representações aprendidas para categorias indexadas | Driver CPU/CUDA | PyTorch/scikit-learn | Tracking por padrão |
| [`optuna_lgbm`](optuna_lgbm/README.md) | pesquisar hiperparâmetros do LightGBM sem confundir busca com teste final | Driver | Optuna/LightGBM | Memória; muda logger Optuna |
| [`performance_monitor`](performance_monitor/README.md) | métricas periódicas contra política explícita | Driver | Plotly no import | Memória |
| [`prophet_wrapper`](prophet_wrapper/README.md) | forecast com tendência, sazonalidade e calendário sob validação temporal | Driver | Prophet na chamada; MLflow no import | Tracking por padrão |
| [`score_bands`](score_bands/README.md) | bandas quantílicas para diagnóstico de score, não política de aprovação pronta | Driver | pandas/NumPy | Memória |
| [`scorecard_builder`](scorecard_builder/README.md) | converter log-odds em pontos sem confundir escala com probabilidade | Driver | pandas/NumPy | Memória |
| [`shap_explainer`](shap_explainer/README.md) | calcular atribuições SHAP com saída/classe explícita e limites de custo | Driver | SHAP; Matplotlib nos plots | Arquivo se save_path for usado |
| [`split_temporal`](split_temporal/README.md) | treino, validação e teste por períodos observados, com gaps explícitos | Driver | pandas | Memória |
| [`survival_cox`](survival_cox/README.md) | associações de risco relativo sob o pressuposto de riscos proporcionais | Driver | lifelines | Tracking por padrão |
| [`tabnet_wrapper`](tabnet_wrapper/README.md) | TabNet tabular com classificação/regressão e importância global do modelo | Driver CPU/GPU | pytorch-tabnet/PyTorch | Tracking por padrão |
| [`train_catboost`](train_catboost/README.md) | baseline de boosting com tratamento explícito de variáveis categóricas | Driver | CatBoost/scikit-learn | Tracking; arquivo por override |
| [`train_lgbm`](train_lgbm/README.md) | baseline LightGBM para comparar modelos tabulares com um contrato explícito | Driver | LightGBM/scikit-learn | Tracking por padrão |
| [`train_xgboost`](train_xgboost/README.md) | aprender a prever com árvores, sem confundir treino com validação | Driver | XGBoost/scikit-learn | Tracking por padrão |
| [`umap_viz`](umap_viz/README.md) | projeção UMAP para exploração visual de clusters, não prova de separação | Driver | Plotly no import; UMAP na chamada | Figura em memória |
| [`vintage_analysis`](vintage_analysis/README.md) | maturação por safra sem preencher o que ainda não foi observado | Driver | Plotly no import | Memória |
| [`walk_forward`](walk_forward/README.md) | múltiplos cortes temporais com janela de treino expansiva | Driver | pandas/NumPy; depende do callback | Efeitos do callback |
| [`woe_iv_calculator`](woe_iv_calculator/README.md) | WOE/IV distribuído como diagnóstico, não selo automático de qualidade | Spark | PySpark/sessão autorizada | Leitura, agregação e coleta escalar |

“Tracking por padrão” indica `log_mlflow=True`; `False` desliga apenas o registro explícito do helper, não autologging da sessão. Alguns módulos exigem MLflow já no import. Dependências especiais não substituem os requisitos completos de cada guia. Os notebooks podem instalar pacotes/reiniciar Python e ter efeitos diferentes dos helpers; confira antes de executar.

## Cuidados da categoria

Objetos diferentes respondem perguntas diferentes. Métrica, explicação, drift, causalidade e aprovação de produção não são equivalentes.

Um resultado local ou sintético não equivale a homologação no Databricks Runtime do destino. Permissões, volume, versão e regras de negócio continuam externos ao índice.

## Rotas relacionadas

- [Catálogo geral de snippets](../README.md)
- [Entrada do ecossistema `.assistant`](../../README.md)
- [Manual Técnico — inventário de helpers](../../MANUAL_TECNICO.md#catalogo-helpers)

**Cobertura deste índice:** 30 objeto(s) com README local encontrado(s) diretamente em `hub_snippets/ml/`.
