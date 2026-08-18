# Catálogo de helpers — demanda → módulo

> **Documento do Hub, não auto-descoberto pelo Genie Code.**
> Adicione-o ao chat com `@` ou **Add context** quando quiser explorar a
> biblioteca inteira. Cada `SKILL.md` já declara os helpers do seu próprio
> fluxo; este catálogo é a visão completa e a fonte de manutenção.

A biblioteca reúne módulos curados em `hub_snippets/` e `hub_scripts/`, com lógica
analítica auditada e verificada no runtime Databricks. A regra que
justifica o catálogo é simples: **quando existe helper para a demanda, use o
helper; não reimplemente a lógica**. Código estatístico reescrito a cada
conversa é a origem mais comum de erro silencioso — o ambiente anterior a este
continha um PSI calculado por média e desvio, incorreto por construção.

## Como carregar

```python
import sys
sys.path.insert(0, "/Workspace/Users/<username>/.assistant")

from hub_snippets.spark.psi_calculator import calcular_psi
from hub_scripts.quick_profile import quick_profile
```

O caminho a inserir é a pasta `.assistant`, não `hub_snippets`. Importar afeta
apenas o runtime Python; não injeta o conteúdo do módulo no contexto do chat.

## Legenda de disponibilidade

| Marca | Significado |
|---|---|
| — | Sem dependência além de PySpark/pandas/Plotly; funciona no Free e no trabalho |
| **imp** | Dependência opcional exigida **no import**: o módulo nem carrega sem a lib |
| **exec** | Dependência opcional exigida **na chamada**: o import passa e o erro só aparece no uso |

Dependências opcionais estão inventariadas em `hub_snippets/requirements-optional.txt`,
com o conjunto de versões que funcionou em runtime. Instale apenas o subconjunto
necessário e **fixe a versão**; instalar sem fixar derruba o kernel em serverless,
por alteração de pacotes core.

Situação de verificação dos módulos com dependência opcional: todos foram
exercitados no runtime, exceto `prophet_wrapper`, que falha por não inicializar
o backend do Prophet nesse ambiente. Detalhes em `docs/testes/spark/` no
repositório.

## Exploração, qualidade e perfil de dados

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Resumo de nulos por coluna com semáforo | `hub_snippets.spark.null_summary` | `null_summary` | — |
| Perfil de tabela com amostragem declarada | `hub_scripts.quick_profile` | `quick_profile` | — |
| Unicidade de chave, nulos e freshness | `hub_scripts.data_quality_check` | `data_quality_check` | — |
| Exportar schema documentado em YAML/JSON | `hub_scripts.schema_to_yaml` | `schema_to_dict`, `schema_to_yaml` | — |
| Conferir convenção de nomes (política do projeto) | `hub_scripts.naming_checker` | `naming_checker` | — |
| Medir cobertura de documentação de notebook | `hub_scripts.doc_coverage` | `doc_coverage` | — |
| **Diagnóstico de join antes de executá-lo** | `hub_snippets.spark.join_diagnostics` | `diagnosticar_join` | — |
| Amostra reprodutível, com estratificação opcional | `hub_snippets.spark.smart_sample` | `smart_sample` | — |
| Exibir DataFrame grande sem varredura completa | `hub_snippets.spark.safe_display` | `safe_display` | — |
| Heatmap de correlação | `hub_snippets.display.correlation_matrix` | `plot_correlation` | — |
| Grid de distribuições numéricas | `hub_snippets.display.distribution_grid` | `plot_distributions` | — |
| Tabela pandas estilizada em HTML | `hub_snippets.display.dataframe_styled` | `display_styled` | **exec** |

`quick_profile` separa explicitamente o que é calculado na tabela inteira
(contagem, nulos) do que vem da amostra (cardinalidade, top valores, faixas).
Preserve essa distinção ao reportar resultados.

## Feature engineering

| Demanda | Módulo | API |
|---|---|---|
| **Junção point-in-time (as-of) com atraso de publicação** | `hub_snippets.spark.pit_join` | `pit_join` |
| Features de calendário (com feriados do projeto) | `hub_snippets.spark.date_features` | `extrair_features_data` |
| Lags e janelas móveis por entidade | `hub_snippets.ml.lgbm_temporal` | `create_temporal_features` |
| WOE e Information Value | `hub_snippets.ml.woe_iv_calculator` | `calculate_woe_iv`, `classify_iv` |
| Recência, frequência e valor até data de corte | `hub_scripts.rfv_calculator` | `rfv_calculator` |

`extrair_features_data` cobre apenas feriados nacionais de data fixa; feriados
móveis, estaduais, municipais e bancários entram por `holiday_dates`.
`rfv_calculator` já exclui eventos posteriores à data de referência — não
adicione filtro redundante nem remova o existente.

## Split, validação temporal e métricas

| Demanda | Módulo | API |
|---|---|---|
| Split temporal por período de calendário | `hub_snippets.ml.split_temporal` | `temporal_split` |
| Validação walk-forward com janela expansiva | `hub_snippets.ml.walk_forward` | `walk_forward_cv` |
| Métricas de classificação binária (AUC, KS, Gini, lift) | `hub_snippets.ml.metrics_report` | `calculate_binary_metrics` |
| Métricas de regressão | `hub_snippets.ml.metrics_report` | `calculate_regression_metrics` |
| Curvas ROC, PR, lift e KS | `hub_snippets.ml.curves_plotly` | `plot_roc_curve`, `plot_pr_curve`, `plot_lift_curve`, `plot_ks_curve` |

`temporal_split` e `walk_forward_cv` operam em unidades de calendário, não em
posição de linha — é o que sustenta a exigência anti-leakage. Reimplementar
split por `orderBy` e fatia de linhas reintroduz o vazamento que esses módulos
existem para evitar.

## Treino de modelos

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Baseline LightGBM com MLflow | `hub_snippets.ml.train_lgbm` | `train_lightgbm_baseline` | **imp** |
| Baseline XGBoost com MLflow | `hub_snippets.ml.train_xgboost` | `train_xgboost_baseline` | **imp** |
| Baseline CatBoost com MLflow | `hub_snippets.ml.train_catboost` | `train_catboost_baseline` | **imp** |
| Busca de hiperparâmetros | `hub_snippets.ml.optuna_lgbm` | `optimize_lgbm` | **imp** |
| Ranking (LambdaRank, NDCG) | `hub_snippets.ml.lgbm_ranker` | `train_lgbm_ranker`, `evaluate_ranking` | **imp** |
| **Registro MLflow com os campos exigidos pela política** | `hub_snippets.ml.mlflow_run` | `run_governado` | **exec** |
| MLP com embeddings categóricas | `hub_snippets.ml.mlp_embeddings` | `train_embedding_mlp` | **imp** |
| TabNet | `hub_snippets.ml.tabnet_wrapper` | `train_tabnet` | **exec** |

O registro em MLflow é opcional nos wrappers e só ocorre quando solicitado.
Atenção verificada em runtime: os wrappers registram no run **ativo**, então
chamar dois deles na mesma sessão colide na chave `algorithm`, que o MLflow
trata como imutável. Use `run_governado` para isolar cada execução.

`run_governado` recusa fechar um run sem parâmetros, métricas e assinatura, e
recusa abrir sem limitações declaradas — a política de registro das instruções
passa a ser aplicada em vez de lembrada.

## Scorecard e bandas de score

| Demanda | Módulo | API |
|---|---|---|
| Converter modelo logístico em pontos | `hub_snippets.ml.scorecard_builder` | `build_scorecard` |
| Bandas de score auditáveis | `hub_snippets.ml.score_bands` | `generate_score_bands` |

`generate_score_bands` exige direção do score declarada. Definir qual extremo
representa maior risco é decisão de negócio, não default do helper.

## Explicabilidade

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Cálculo SHAP e plots global/local | `hub_snippets.ml.shap_explainer` | `compute_shap`, `get_feature_importance_shap`, `plot_shap_global`, `plot_shap_local` | **exec** |
| Relatório dual-layer (executivo + técnico) | `hub_snippets.ml.explainability_report` | `generate_executive_report`, `generate_technical_summary` | **exec** |

Importância SHAP não é causalidade nem percentual de poder preditivo; os módulos
formulam os textos de acordo e essa formulação deve ser preservada.

## Monitoramento e drift

| Demanda | Módulo | API |
|---|---|---|
| PSI/CSI nativo em PySpark | `hub_snippets.spark.psi_calculator` | `calcular_psi`, `calcular_csi`, `interpretar_psi` |
| Diagnóstico driver-side (PSI, KS, CSI, varredura) | `hub_snippets.ml.drift_detection` | `calculate_psi`, `calculate_ks`, `calculate_csi`, `detect_drift_all_features` |
| Comparar duas coortes de uma tabela | `hub_scripts.drift_detector` | `drift_detector` |
| Acompanhar métricas contra política calibrada | `hub_snippets.ml.performance_monitor` | `PerformanceMonitor` |

Prefira a versão PySpark em escala; a driver-side serve a amostras já reduzidas.
Thresholds de PSI e regras de alerta são **política calibrada por modelo e
feature**, nunca padrão universal: `interpretar_psi` só classifica quando recebe
os limites do consumidor. `PerformanceMonitor` não autoriza retreino — a decisão
exige investigação, champion-challenger e aprovação.

## Safras, sobrevivência e séries temporais

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Tabela de safra, curvas de maturação e heatmap | `hub_snippets.ml.vintage_analysis` | `build_vintage_table`, `plot_vintage_curves`, `plot_vintage_heatmap`, `compare_safras` | — |
| Kaplan-Meier e log-rank | `hub_snippets.ml.kaplan_meier` | `plot_kaplan_meier`, `log_rank_test` | **exec** |
| Cox com teste de proporcionalidade | `hub_snippets.ml.survival_cox` | `train_cox_ph`, `validate_proportionality` | **exec** |
| Prophet com feriados BR | `hub_snippets.ml.prophet_wrapper` | `train_prophet` | **exec** |
| ARIMA com diagnóstico | `hub_snippets.ml.arima_wrapper` | `train_arima` | **exec** |

`build_vintage_table` calcula incidência acumulada no nível contrato × MOB.
Somar taxas por safra produz número diferente e incorreto.

## Clustering e detecção de anomalia

| Demanda | Módulo | API | Dep. |
|---|---|---|---|
| Seleção de k e pipeline de clustering | `hub_snippets.ml.clustering_suite` | `select_k`, `run_clustering_pipeline` | — |
| Profiling e diferenciadores de cluster | `hub_snippets.ml.cluster_profiling` | `profile_clusters`, `top_differentiators` | — |
| Projeção 2D para visualizar clusters | `hub_snippets.ml.umap_viz` | `compute_umap`, `plot_umap_clusters` | **exec** |
| Isolation Forest com profiling | `hub_snippets.ml.isolation_forest` | `train_isolation_forest`, `profile_anomalies` | — |
| Autoencoder para anomalia | `hub_snippets.ml.autoencoder_anomaly` | `train_autoencoder_anomaly` | **imp** |

## Apresentação e formatação

| Demanda | Módulo | API |
|---|---|---|
| Números no padrão brasileiro | `hub_snippets.constants.format_br` | `fmt_int`, `fmt_pct`, `fmt_brl`, `fmt_dec`, `fmt_delta`, `fmt_n` |
| Tema Plotly institucional | `hub_snippets.visual.theme_plotly` | `get_tema_eda`, `aplicar_tema`, `registrar_template_plotly` |
| KPI cards | `hub_snippets.visual.kpi_card` | `kpi_card_html`, `kpi_card_markdown` |
| Badges de status e score | `hub_snippets.visual.badge` | `badge_status`, `badge_score`, `badge_inline` |
| Headers de seção | `hub_snippets.visual.section_header` | `section_header_html` |
| Separadores | `hub_snippets.visual.divider` | `divider_light`, `divider_medium`, `divider_heavy`, `divider_section` |
| Índice de notebook de EDA | `hub_snippets.visual.index_generator` | `gerar_indice_eda` |
| Paletas, emojis e estilos CSS | `hub_snippets.constants.colors`, `.emojis`, `.styles` | constantes |

Formatação brasileira vale para a narrativa; os dados preservam o tipo numérico
original. Entradas dos helpers de HTML são escapadas — não monte HTML por
concatenação manual para contornar o escape.

## Testes e fixtures

| Demanda | Módulo | API |
|---|---|---|
| Base tabular sintética (chave, categórica, nulos, alvo) | `hub_snippets.testing.fixtures` | `base_tabular` |
| Painel de série temporal por entidade | `hub_snippets.testing.fixtures` | `serie_temporal` |
| Par fatos/features com vazamento marcado | `hub_snippets.testing.fixtures` | `fatos_e_features` |
| Painel contrato × MOB para curvas de safra | `hub_snippets.testing.fixtures` | `safras` |

Toda função é determinística: mesma `seed`, mesmo resultado. Nenhuma grava
tabela — o retorno é DataFrame em memória, e materializar continua sendo decisão
visível de quem consome. `fatos_e_features` marca com `eh_futura` as linhas
publicadas depois da decisão, para que um teste de junção temporal possa provar
que elas foram descartadas.

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
(ver ADR-0004). A skill `hub-ml-auditoria-skills` verifica aderência de outputs
ao que está declarado aqui.
