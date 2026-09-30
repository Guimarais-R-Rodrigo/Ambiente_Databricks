---
name: hub-ml-baseline-ml
description: Treina e compara baselines reproduzíveis de machine learning no Databricks para classificação, regressão, séries temporais, ranking, survival, clustering e detecção de anomalias, com splits anti-leakage, MLflow, métricas condicionais e handoff para explicabilidade/monitoramento. Usar quando pedirem baseline, primeiro modelo, benchmark, scorecard, LightGBM/XGBoost/CatBoost, forecasting, clustering, ranking, survival, anomaly detection, deep learning tabular ou comparação de modelos.
---

# Construir baseline de ML

## Rota executável sintética SER09 (candidata)

Para pedido explícito do perfil `BINARY_TEMPORAL_LOCAL_V1`, use
`input.schema.json` e `scripts/preflight.py::preflight` antes de
`scripts/run.py::run`. Verifique o Receipt e os bindings de partição/fit com
`scripts/verify.py::verify` usando request e run_id mantidos pelo invocador.
Esta rota cobre somente classificação binária mensal sintética, split
50/25/25, gap zero, feature numérica única, scaler e regressão logística
ajustados no treino e métricas em memória. O perfil é candidato não promovido:
sem MLflow, escrita, seleção de modelo, deploy ou promoção. Pedidos fora
deste perfil seguem o fluxo de planejamento abaixo e não recebem Receipt
executável por aproximação.
Um pedido para **planejar** não autoriza criar observações, treinar ou medir
como se os dados tivessem sido fornecidos. Se um exemplo sintético executável
for solicitado separadamente, identifique as linhas geradas e limite AUC/Brier
àquela simulação; verificação do split e do Receipt não certifica ausência
de leakage operacional, calibração futura ou prontidão do modelo. Amostrar
uma feature condicionalmente ao rótulo em um gerador sintético não é, por
si só, prova de leakage; avalie disponibilidade e proveniência no uso real.

## Tracking sintético pessoal SER10 (candidato)

Para registrar **o mesmo Pipeline treinado** no perfil SER09, use
`scripts/run_tracking.py::run_tracking` apenas com autorização externa
`SER10-AUTH-1` vinculada ao digest exato do request, run_id e experimento
pessoal novo. O invocador configura `tracking_uri` e `registry_uri` do MLflow
como `databricks` (sem registrar modelo no Registry) e passa uma sessão Spark autenticada para derivar `current_user()`. O adapter chama
`scripts/verify_tracking.py::verify_live` internamente enquanto o recurso
está ativo e **antes** do cleanup. Depois confira
`scripts/verify_tracking.py::verify_finalized` com request, autorização,
identidade e cliente mantidos externamente.

O adapter cria experimento e run, chama `run_governado`, lê parâmetros,
métricas, tags, assinatura e predições do modelo serializado. Só após
verificação live independente, faz soft delete do run e confere seu estado
com o experimento ativo; por fim, deleta e confere o experimento por ID.
PASS exige toda essa sequência observada. O Receipt
SER09 continua prova da **computação sem escrita**; o efeito MLflow fica em
registro separado, sem alegar autorização autenticada pelo Receipt.
Esta rota não registra Model Registry, deploy, job ou score produtivo.

## Quando esta skill se aplica

- Pedem **baseline, primeiro modelo, benchmark ou comparação de modelos** — em
  classificação, regressão, série temporal, ranking, survival, clustering ou
  detecção de anomalia.
- Existe alvo definido e base pronta o bastante para treinar algo que sirva de
  régua.

**Não cobre:** construir as features (`hub-ml-feature-engineering`), explicar o
modelo depois de treinado (`hub-ml-explainability`), nem acompanhá-lo em produção
(`hub-ml-monitoramento-modelo`).

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

Importar de `hub_snippets` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Split temporal e validação walk-forward | `hub_snippets.ml.split_temporal`, `hub_snippets.ml.walk_forward` |
| Métricas de classificação e regressão | `hub_snippets.ml.metrics_report` |
| Curvas ROC, PR, lift e KS | `hub_snippets.ml.curves_plotly` |
| Treino com MLflow opcional | `hub_snippets.ml.train_lgbm`, `hub_snippets.ml.train_xgboost`, `hub_snippets.ml.train_catboost`, `hub_snippets.ml.optuna_lgbm` |
| Registro com dataset, split, assinatura e limitações | `hub_snippets.ml.mlflow_run` (`run_governado`) |
| Scorecard e bandas de score | `hub_snippets.ml.scorecard_builder`, `hub_snippets.ml.score_bands` |
| Suites não tabulares | `hub_snippets.ml.lgbm_ranker`, `hub_snippets.ml.clustering_suite`, `hub_snippets.ml.isolation_forest`, `hub_snippets.ml.survival_cox`, `hub_snippets.ml.prophet_wrapper` |

Se um `ResolvedTheme` notebook tiver sido selecionado para a entrega, as curvas podem usar `plot_roc_curve_resolvido`, `plot_pr_curve_resolvido`, `plot_lift_curve_resolvido` e `plot_ks_curve_resolvido`. Isso é somente aparência: métricas, probabilidades, thresholds e a seleção do modelo continuam definidos pelo fluxo analítico, não pelo tema.

`temporal_split` e `walk_forward_cv` operam em unidades de calendário; substituí-los por fatia de linhas reintroduz o leakage que eles evitam. Os wrappers de treino dependem de bibliotecas opcionais — confirmar instalação e versão fixada antes de prometer execução.

## Entregar

Fornecer notebook/código reproduzível, contrato, comparação com trivial, tabela de métricas, diagnóstico de leakage/overfit, registro MLflow, limitações e recomendação. Encaminhar `hub-ml-explainability` após escolher o candidato e `hub-ml-monitoramento-modelo` antes de produção.
## O que nunca fazer

- **Dividir por posição de linha** quando o dado é temporal. Split aleatório em
  série temporal vaza o futuro e produz métrica que não se repete em produção.
- **Comparar modelos com métricas diferentes**, ou com a mesma métrica sobre
  amostras diferentes.
- **Tratar o baseline como entrega final.** Ele é régua: existe para dizer se o
  modelo seguinte vale o custo.
- **Instalar biblioteca opcional sem fixar versão** onde o inventário manda fixar
  — `shap`, `umap-learn` e `pmdarima` exigem pin, e as três juntas quebram o
  `import numpy`.
- **Abrir run de MLflow no serverless** sem conferir runtime, backend e
  autorização. O bloqueio observado no Free em 17/08/2026 é histórico;
  confirme a configuração do perfil executável antes de prometer tracking.
