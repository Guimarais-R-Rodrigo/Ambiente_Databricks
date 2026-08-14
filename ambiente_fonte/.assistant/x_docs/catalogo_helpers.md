# Catálogo de helpers — demanda → módulo

> **Documento customizado (`x_docs`), não auto-descoberto pela Genie Code.**
> Adicione-o ao chat com `@` ou **Add context** quando quiser explorar a
> biblioteca inteira. Cada `SKILL.md` já declara os helpers do seu próprio
> fluxo; este catálogo é a visão completa e a fonte de manutenção.

A biblioteca reúne 54 módulos curados — 47 em `x_snippets/`, 7 em `x_scripts/` —
com lógica analítica auditada e verificada no runtime Databricks. A regra que
justifica o catálogo é simples: **quando existe helper para a demanda, use o
helper; não reimplemente a lógica**. Código estatístico reescrito a cada
conversa é a origem mais comum de erro silencioso — o ambiente anterior a este
continha um PSI calculado por média e desvio, incorreto por construção.

## Como carregar

```python
import sys
sys.path.insert(0, "/Workspace/Users/<username>/.assistant")

from x_snippets.spark.psi_calculator import calcular_psi
from x_scripts.quick_profile import quick_profile
```

O caminho a inserir é a pasta `.assistant`, não `x_snippets`. Importar afeta
apenas o runtime Python; não injeta o conteúdo do módulo no contexto do chat.

## Legenda de disponibilidade

| Marca | Significado |
|---|---|
| — | Sem dependência além de PySpark/pandas/Plotly; funciona no Free e no trabalho |
| **imp** | Dependência opcional exigida **no import**: o módulo nem carrega sem a lib |
| **exec** | Dependência opcional exigida **na chamada**: o import passa e o erro só aparece no uso |

Dependências opcionais estão inventariadas em `x_snippets/requirements-optional.txt`.
Instale apenas o subconjunto necessário e **fixe a versão no projeto consumidor**;
o inventário não é arquivo de instalação. Nenhum dos módulos marcados foi
exercitado no runtime até aqui — essa verificação é gate por workflow.

## Exploração, qualidade e perfil de dados

| Demanda | Módulo | API |
|---|---|---|
| Resumo de nulos por coluna com semáforo | `x_snippets.spark.null_summary` | `null_summary` |
| Perfil de tabela com amostragem declarada | `x_scripts.quick_profile` | `quick_profile` |
| Unicidade de chave, nulos e freshness | `x_scripts.data_quality_check` | `data_quality_check` |
| Exportar schema documentado em YAML/JSON | `x_scripts.schema_to_yaml` | `schema_to_dict`, `schema_to_yaml` |
| Conferir convenção de nomes (política do projeto) | `x_scripts.naming_checker` | `naming_checker` |
| Medir cobertura de documentação de notebook | `x_scripts.doc_coverage` | `doc_coverage` |
| Amostra reprodutível, com estratificação opcional | `x_snippets.spark.smart_sample` | `smart_sample` |
| Exibir DataFrame grande sem varredura completa | `x_snippets.spark.safe_display` | `safe_display` |
| Heatmap de correlação | `x_snippets.display.correlation_matrix` | `plot_correlation` |
| Grid de distribuições numéricas | `x_snippets.display.distribution_grid` | `plot_distributions` |
| Tabela pandas estilizada em HTML | `x_snippets.display.dataframe_styled` | `display_styled` |

`quick_profile` separa explicitamente o que é calculado na tabela inteira
(contagem, nulos) do que vem da amostra (cardinalidade, top valores, faixas).
Preserve essa distinção ao reportar resultados.

## Feature engineering

| Demanda | Módulo | API |
|---|---|---|
| Features de calendário (com feriados do projeto) | `x_snippets.spark.date_features` | `extrair_features_data` |
| Lags e janelas móveis por entidade | `x_snippets.ml.lgbm_temporal` | `create_temporal_features` |
| WOE e Information Value | `x_snippets.ml.woe_iv_calculator` | `calculate_woe_iv`, `classify_iv` |
| Recência, frequência e valor até data de corte | `x_scripts.rfv_calculator` | `rfv_calculator` |

`extrair_features_data` cobre apenas feriados nacionais de data fixa; feriados
móveis, estaduais, municipais e bancários entram por `holiday_dates`.
`rfv_calculator` já exclui eventos posteriores à data de referência — não
adicione filtro redundante nem remova o existente.

## Split, validação temporal e métricas

| Demanda | Módulo | API |
|---|---|---|
| Split temporal por período de calendário | `x_snippets.ml.split_temporal` | `temporal_split` |
| Validação walk-forward com janela expansiva | `x_snippets.ml.walk_forward` | `walk_forward_cv` |
| Métricas de classificação binária (AUC, KS, Gini, lift) | `x_snippets.ml.metrics_report` | `calculate_binary_metrics` |
| Métricas de regressão | `x_snippets.ml.metrics_report` | `calculate_regression_metrics` |
| Curvas ROC, PR, lift e KS | `x_snippets.ml.curves_plotly` | `plot_roc_curve`, `plot_pr_curve`, `plot_lift_curve`, `plot_ks_curve` |

`temporal_split` e `walk_forward_cv` operam em unidades de calendário, não em
posição de linha — é o que sustenta a exigência anti-leakage. Reimplementar
split por `orderBy` e fatia de linhas reintroduz o vazamento que esses módulos
existem para evitar.

## Treino de modelos

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Baseline LightGBM com MLflow | `x_snippets.ml.train_lgbm` | `train_lightgbm_baseline` | **imp** |
| Baseline XGBoost com MLflow | `x_snippets.ml.train_xgboost` | `train_xgboost_baseline` | **imp** |
| Baseline CatBoost com MLflow | `x_snippets.ml.train_catboost` | `train_catboost_baseline` | **imp** |
| Busca de hiperparâmetros | `x_snippets.ml.optuna_lgbm` | `optimize_lgbm` | **imp** |
| Ranking (LambdaRank, NDCG) | `x_snippets.ml.lgbm_ranker` | `train_lgbm_ranker`, `evaluate_ranking` | **imp** |
| MLP com embeddings categóricas | `x_snippets.ml.mlp_embeddings` | `train_embedding_mlp` | **imp** |
| TabNet | `x_snippets.ml.tabnet_wrapper` | `train_tabnet` | **exec** |

O registro em MLflow é opcional e só ocorre quando solicitado explicitamente.

## Scorecard e bandas de score

| Demanda | Módulo | API |
|---|---|---|
| Converter modelo logístico em pontos | `x_snippets.ml.scorecard_builder` | `build_scorecard` |
| Bandas de score auditáveis | `x_snippets.ml.score_bands` | `generate_score_bands` |

`generate_score_bands` exige direção do score declarada. Definir qual extremo
representa maior risco é decisão de negócio, não default do helper.

## Explicabilidade

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Cálculo SHAP e plots global/local | `x_snippets.ml.shap_explainer` | `compute_shap`, `get_feature_importance_shap`, `plot_shap_global`, `plot_shap_local` | **exec** |
| Relatório dual-layer (executivo + técnico) | `x_snippets.ml.explainability_report` | `generate_executive_report`, `generate_technical_summary` | — |

Importância SHAP não é causalidade nem percentual de poder preditivo; os módulos
formulam os textos de acordo e essa formulação deve ser preservada.

## Monitoramento e drift

| Demanda | Módulo | API |
|---|---|---|
| PSI/CSI nativo em PySpark | `x_snippets.spark.psi_calculator` | `calcular_psi`, `calcular_csi`, `interpretar_psi` |
| Diagnóstico driver-side (PSI, KS, CSI, varredura) | `x_snippets.ml.drift_detection` | `calculate_psi`, `calculate_ks`, `calculate_csi`, `detect_drift_all_features` |
| Comparar duas coortes de uma tabela | `x_scripts.drift_detector` | `drift_detector` |
| Acompanhar métricas contra política calibrada | `x_snippets.ml.performance_monitor` | `PerformanceMonitor` |

Prefira a versão PySpark em escala; a driver-side serve a amostras já reduzidas.
Thresholds de PSI e regras de alerta são **política calibrada por modelo e
feature**, nunca padrão universal: `interpretar_psi` só classifica quando recebe
os limites do consumidor. `PerformanceMonitor` não autoriza retreino — a decisão
exige investigação, champion-challenger e aprovação.

## Safras, sobrevivência e séries temporais

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Tabela de safra, curvas de maturação e heatmap | `x_snippets.ml.vintage_analysis` | `build_vintage_table`, `plot_vintage_curves`, `plot_vintage_heatmap`, `compare_safras` | — |
| Kaplan-Meier e log-rank | `x_snippets.ml.kaplan_meier` | `plot_kaplan_meier`, `log_rank_test` | **exec** |
| Cox com teste de proporcionalidade | `x_snippets.ml.survival_cox` | `train_cox_ph`, `validate_proportionality` | **exec** |
| Prophet com feriados BR | `x_snippets.ml.prophet_wrapper` | `train_prophet` | **exec** |
| ARIMA com diagnóstico | `x_snippets.ml.arima_wrapper` | `train_arima` | **exec** |

`build_vintage_table` calcula incidência acumulada no nível contrato × MOB.
Somar taxas por safra produz número diferente e incorreto.

## Clustering e detecção de anomalia

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Seleção de k e pipeline de clustering | `x_snippets.ml.clustering_suite` | `select_k`, `run_clustering_pipeline` | — |
| Profiling e diferenciadores de cluster | `x_snippets.ml.cluster_profiling` | `profile_clusters`, `top_differentiators` | — |
| Projeção 2D para visualizar clusters | `x_snippets.ml.umap_viz` | `compute_umap`, `plot_umap_clusters` | **exec** |
| Isolation Forest com profiling | `x_snippets.ml.isolation_forest` | `train_isolation_forest`, `profile_anomalies` | — |
| Autoencoder para anomalia | `x_snippets.ml.autoencoder_anomaly` | `train_autoencoder_anomaly` | **imp** |

## Apresentação e formatação

| Demanda | Módulo | API |
|---|---|---|
| Números no padrão brasileiro | `x_snippets.constants.format_br` | `fmt_int`, `fmt_pct`, `fmt_brl`, `fmt_dec`, `fmt_delta`, `fmt_n` |
| Tema Plotly institucional | `x_snippets.visual.theme_plotly` | `get_tema_eda`, `aplicar_tema`, `registrar_template_plotly` |
| KPI cards | `x_snippets.visual.kpi_card` | `kpi_card_html`, `kpi_card_markdown` |
| Badges de status e score | `x_snippets.visual.badge` | `badge_status`, `badge_score`, `badge_inline` |
| Headers de seção | `x_snippets.visual.section_header` | `section_header_html` |
| Separadores | `x_snippets.visual.divider` | `divider_light`, `divider_medium`, `divider_heavy`, `divider_section` |
| Índice de notebook de EDA | `x_snippets.visual.index_generator` | `gerar_indice_eda` |
| Paletas, emojis e estilos CSS | `x_snippets.constants.colors`, `.emojis`, `.styles` | constantes |

Formatação brasileira vale para a narrativa; os dados preservam o tipo numérico
original. Entradas dos helpers de HTML são escapadas — não monte HTML por
concatenação manual para contornar o escape.

## Restrições verificadas no runtime

Verificação executada em Spark 4.1 serverless (2026-08-13, 64 checks):

- `cache()` e `persist()` **não são suportados** em compute serverless.
  `safe_display` opera sem cache; `quick_profile` e `drift_detector` degradam
  silenciosamente para execução sem cache e mantêm o cache em compute clássico.
  Chamadas novas a `cache()` em código gerado quebram no Free.
- Módulos não recebem a variável global `spark` de notebook: resolvem a sessão
  por `SparkSession.getActiveSession()`. Código novo que dependa do global falha
  quando movido para dentro de módulo.
- O runtime pode ser anterior ao Python 3.12: barra invertida dentro da
  expressão de f-string (PEP 701) não compila.

## Manutenção

Alteração na biblioteca exige, na mesma sessão: atualizar este catálogo,
atualizar a seção de helpers das skills afetadas, rodar
`tools/validate_assistant.py`, regerar o simulado e registrar no `CHANGELOG.md`
(ver ADR-0004). A skill `rodrigo-auditoria-skills` verifica aderência de outputs
ao que está declarado aqui.
