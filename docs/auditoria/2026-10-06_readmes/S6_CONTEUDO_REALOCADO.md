# Conteúdo histórico realocado — snippets de Machine Learning

Data: 2026-10-06. Baseline: `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`.

Este arquivo preserva integralmente trechos retirados dos guias operacionais, inclusive ressalvas, fontes e estados de testes datados. São evidências históricas de manutenção; não instruções atuais nem resultados de execução desta revisão. O texto operacional foi reconciliado com o código, sem modificar algoritmos ou células executáveis.

## 1. R0139 — `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/README.md`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
> **Atualização V07 — estado atual.** Cada curva legada possui agora uma rota
> opt-in `*_resolvido`: ROC, Precision–Recall, Lift e KS. A aparência usa o token
> dedicado `palette.curves_legacy`, preservando a decisão do contrato V01 de
> manter a família histórica de seis cores separada da paleta categórica geral.
> AUC, AP, lift, KS, eixos e séries continuam calculados pela mesma lógica. A
> figura Plotly resolvida pode ser serializada localmente para HTML; PNG Plotly,
> PDF e PPTX não são formatos homologados pela V07.
````

## 2. R0139 — `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/README.md`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
A paleta local tem seis cores, enquanto a paleta compartilhada do Hub tem dez. Isso é dívida conhecida e pode mudar aparência se for unificada.
````

## 3. R0139 — `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da R09. Referências primárias: documentação do scikit-learn para ROC, Precision-Recall, AUC/AP e documentação do Plotly para `graph_objects`.

As curvas descrevem comportamento na amostra fornecida; não estabelecem causalidade, calibração ou aprovação de produção.
````

## 4. R0141 — `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base da R08. Para a semântica de Tree SHAP e a dependência do espaço de saída do modelo, consulte a documentação oficial do SHAP: <https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html>.

A revisão R08 não presume causalidade, publicação Databricks, homologação regulatória nem auditoria independente.
````

## 5. R0146 — `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base R09. Referências primárias: documentação de métricas do scikit-learn (`sklearn.metrics`) e SciPy (`scipy.stats.ks_2samp`).

Os valores retornados são evidência estatística; sua adequação depende do desenho de avaliação e da decisão de negócio.
````

## 6. R0154 — `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base da R08. Documentação oficial do SHAP: [`TreeExplainer`](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html) e [API](https://shap.readthedocs.io/en/latest/api.html).

A documentação oficial ressalta que a soma SHAP depende do output explicado e que o tratamento de dependência entre features é parte da configuração. A revisão R08 não presume causalidade, publicação Databricks ou auditoria independente.
````

## 7. R0347 — `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/exemplo_curves_plotly.py`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Dívida registrada: a paleta daqui tem seis cores
# MAGIC
# MAGIC Este módulo **redeclara** `PALETA_CATEGORICA` em vez de importá-la de
# MAGIC `hub_snippets.constants.colors`, e o valor **diverge**:
# MAGIC
# MAGIC | Onde | Cores |
# MAGIC |---|---:|
# MAGIC | `constants.colors` | 10 |
# MAGIC | `ml.curves_plotly` (aqui) | **6** |
# MAGIC | `ml.umap_viz`, `ml.vintage_analysis` | 10, idênticas à original |
# MAGIC
# MAGIC Duas das três cópias são iguais à original, o que torna esta terceira
# MAGIC invisível numa inspeção rápida. Como o `__init__.py` reexporta tudo, há
# MAGIC hoje dois caminhos de import para o mesmo nome com valores diferentes.
# MAGIC
# MAGIC **Na prática:** um gráfico com mais de seis séries feito por este módulo
# MAGIC repete cor a partir da sétima; o mesmo gráfico feito com a paleta de
# MAGIC `constants` não repete. Se você precisa das dez, importe explicitamente
# MAGIC de `constants.colors` e passe em `colorway`.
# MAGIC
# MAGIC A unificação não foi feita aqui de propósito: trocar a redeclaração por
# MAGIC import mudaria a aparência de todos os gráficos existentes, e a conversão
# MAGIC não muda comportamento. É decisão de produto, e precisa de alguém olhando
# MAGIC os gráficos para dizer se seis ou dez é o certo.
````

## 8. R0349 — `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO no laboratório
# MAGIC
# MAGIC O que rodaria : generate_technical_summary(shap_importance, native_importance=nativa)
# MAGIC Por que não   : ImportError: Missing optional dependency 'tabulate'.
# MAGIC Onde verificar: hub_snippets/requirements-optional.txt
# MAGIC Primeiro bloqueio: instalar `tabulate` na sessão (%pip install tabulate).
# MAGIC Segundo bloqueio: a comparação nativa atual também espera uma coluna `rank`
# MAGIC em **ambos** os DataFrames; esta fixture não a fornece. Instalar `tabulate`
# MAGIC sozinho, portanto, não faz a célula concluir.
# MAGIC ```
# MAGIC
# MAGIC A dependência é **escondida**: não há `import tabulate` no topo do módulo.
# MAGIC Ela entra por `DataFrame.to_markdown()`, que o pandas delega ao `tabulate`
# MAGIC só na hora da chamada. Por isso `explainability_report` está na lista de
# MAGIC "núcleo, sem dependência opcional": a classificação foi feita por import de
# MAGIC topo, e esse critério não enxerga o caso. A célula 1 roda porque
# MAGIC `generate_executive_report` monta o texto à mão; só o resumo técnico
# MAGIC tabula.
````

## 9. R0135 — `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook histórico afirma que a ordem escolhida é a “melhor descrição” e associa uma ordem observada diretamente ao processo gerador. A R06 qualifica essa leitura: é a especificação selecionada pelo procedimento, no espaço e critério usados, para aquela amostra.
````

## 10. R0135 — `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R06.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. Fontes primárias consultadas em 12/09/2026: documentação `AutoARIMA`/`auto_arima` do pmdarima 2.0.x e exemplo oficial de `auto_arima`. A documentação da biblioteca informa que `d` pode ser selecionado por teste de raiz unitária, que a busca stepwise procura uma especificação segundo o critério configurado e que `random_state`/`n_fits` pertencem à busca aleatória, não ao caminho stepwise usado aqui.

O notebook fixa `pmdarima==2.0.4`; em 12/09/2026 o PyPI aponta `pmdarima 2.1.1` como release mais recente. A evidência de runtime desta R06 será registrada no relatório da sprint. Este README não presume publicação no Databricks, homologação em workspace nem auditoria independente.
````

## 11. R0143 — `ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
A figura Plotly criada por este helper **não adiciona marcadores de censura**. O notebook histórico diz que “as marcas de censura aparecem”, mas a implementação apenas adiciona a curva e a faixa de confiança. A informação de censura entra no estimador; isso não significa que esteja marcada visualmente.

Também não há tabela de indivíduos em risco, entrada tardia (`entry`) nem suporte exposto a pesos. O teste de dois grupos não adiciona um campo booleano de significância ao retorno, embora imprima uma interpretação em stdout.
````

## 12. R0143 — `ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R07.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. Fontes primárias consultadas em 12/09/2026: documentação do `KaplanMeierFitter` e de `lifelines.statistics.logrank_test`/`multivariate_logrank_test`. A documentação do lifelines explicita que a implementação do log-rank trata censura à direita e alerta para curvas cruzadas; os marcadores de censura são opção de plotagem da API do lifelines, mas não são adicionados pela figura Plotly deste helper.

Este README não presume publicação no Databricks, homologação de modelo nem auditoria independente.
````

## 13. R0145 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
A função ordena os dados internamente, então o notebook histórico que manda “ordenar antes” não descreve mais uma pré-condição técnica. A pré-condição real é fornecer uma data normalizável e um grão coerente.

O print atual fala em “warm-up das features geradas”. Blocos históricos de output do notebook que mencionem “NaN de lags” são evidência de execução anterior e não a mensagem textual atual.
````

## 14. R0145 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R06.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. A semântica de `shift`, `rolling`, `to_datetime`, `Period` e ordenação foi confrontada com a documentação oficial do pandas vigente em 12/09/2026.

Este README documenta o comportamento atual do Hub. Não presume treinamento LightGBM, publicação no Databricks, homologação em workspace nem auditoria independente.
````

## 15. R0151 — `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook histórico contém interpretações fortes sobre número mínimo de ciclos e componentes. A R06 trata essas frases como heurísticas, não como cortes universais garantidos pela API.
````

## 16. R0151 — `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R06.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. Fontes primárias consultadas em 12/09/2026: documentação oficial do Prophet sobre início rápido, diagnósticos, dados não diários, sazonalidades/feriados/regressores e intervalos de incerteza.

Em 12/09/2026 o PyPI lista Prophet `1.4.0`; o repositório oficial informa modo de manutenção a partir dessa versão. O notebook da R06 não fixa versão. Este README não presume publicação no Databricks, homologação em workspace nem auditoria independente.
````

## 17. R0155 — `ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook histórico resume o comportamento como “tudo até uma data treina, tudo depois testa”. O contrato real tem três partições, dois possíveis gaps e cortes derivados de proporções de períodos.
````

## 18. R0155 — `ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R06.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. A conversão `DatetimeIndex`/`Period` e os aliases de frequência foram confrontados com a documentação oficial do pandas vigente em 12/09/2026.

Este README documenta separação temporal no driver. Não presume ausência completa de leakage, publicação no Databricks, homologação em workspace nem auditoria independente.
````

## 19. R0156 — `ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R07.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. Fontes primárias consultadas em 12/09/2026: documentação `lifelines.CoxPHFitter` e `lifelines.statistics.proportional_hazard_test`, incluindo a forma `h(t|x)=h0(t)exp((x-x̄)'β)`, penalização e o teste com transformação temporal.

Este README não presume causalidade, homologação de modelo, publicação no Databricks nem auditoria independente.
````

## 20. R0162 — `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/README.md`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
> **Atualização V07 — estado atual.** `build_vintage_table` e `compare_safras`
> continuam sem lógica de tema. Para as figuras, V07 adiciona
> `plot_vintage_curves_resolvido` (usa `palette.categorical`) e
> `plot_vintage_heatmap_resolvido` (usa `palette.sequential`). As duas rotas
> reutilizam os mesmos pontos/matriz das funções legadas: MOB, maturidade,
> denominadores, taxas, cobertura e células `NaN` não são alterados pela
> aparência.
````

## 21. R0162 — `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R07.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. O conceito de vintage/MOB é aplicado conforme a implementação local; este README não apresenta limites de maturidade ou critérios de safra como norma externa universal.

Este README não presume projeção validada, homologação de risco, publicação no Databricks nem auditoria independente.
````

## 22. R0163 — `ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook descreve “retreinar a cada janela”; mais precisamente, o helper **chama** `model_fn` a cada janela. Retreinamento só ocorre se a implementação do callback o fizer.
````

## 23. R0163 — `ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R06.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. A semântica de períodos e conversão temporal foi confrontada com a documentação oficial do pandas vigente em 12/09/2026.

Este README documenta um orquestrador de avaliação, não um treinador. Não presume ausência de leakage no callback, publicação no Databricks, homologação em workspace nem auditoria independente.
````

## 24. R0343 — `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/exemplo_arima_wrapper.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 25. R0353 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R06.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## 3. Sem a entidade declarada — bloco histórico e política atual
# MAGIC
# MAGIC O código abaixo foi escrito antes da política atual de duplicatas. Hoje, com várias
# MAGIC entidades na mesma data e `on_duplicate_dates='raise'` (default), a chamada sem
# MAGIC `entity_cols` é recusada antes de produzir o resultado histórico. Para estudar
# MAGIC conscientemente a sequência única com empates, seria necessário optar por
# MAGIC `on_duplicate_dates='keep'`; o código executável e o output antigo são preservados
# MAGIC aqui como evidência, não como receita vigente.
````

## 26. R0353 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ### Contrato atualizado em 09/09/2026
# MAGIC O helper normaliza datas antes de ordenar e preserva colunas do chamador, inclusive nomes internos __hub_ordem e __hub_data. Datas ambíguas exigem date_format; lag_n significa observações anteriores, não períodos de calendário.
````

## 27. R0359 — `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/exemplo_prophet_wrapper.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 28. R0364 — `ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/exemplo_survival_cox.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 29. R0370 — `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/exemplo_vintage_analysis.py`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ### Nota de cor — resolvida em 18/08/2026
# MAGIC
# MAGIC Este módulo **redeclarava** `PALETA_CATEGORICA`, `AZUL_CAIXA` e
# MAGIC `PALETA_SEQUENCIAL` com literais idênticos aos de
# MAGIC `hub_snippets.constants.colors`. Hoje ele os **deriva** de lá, e a paleta
# MAGIC tem uma fonte só. Os nomes continuam na API pública do módulo, então nada
# MAGIC que importava daqui quebrou.
````

## 30. R0144 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O [notebook](exemplo_lgbm_ranker.py) instala LightGBM e reinicia o Python. Ele afirma na abertura histórica que avalia “NDCG e MAP”; nesta R05 a prosa será corrigida para refletir NDCG apenas, preservando código e saídas.
````

## 31. R0144 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. A [documentação de parâmetros do LightGBM](https://lightgbm.readthedocs.io/en/latest/Parameters.html) descreve `lambdarank`, labels de relevância, `label_gain` e parâmetros de ranking. A [documentação de early stopping](https://lightgbm.readthedocs.io/en/v4.6.0/pythonapi/lightgbm.early_stopping.html) explica o papel da validação e de `best_iteration`.

A execução de runtime desta R05 será registrada no relatório da sprint. Sem publicação Databricks, homologação de workspace ou revisão independente presumida.
````

## 32. R0149 — `ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. A [documentação do `TPESampler`](https://optuna.readthedocs.io/en/latest/reference/samplers/generated/optuna.samplers.TPESampler.html) descreve o algoritmo TPE e seus modelos `l(x)`/`g(x)`. A [API `LGBMClassifier`](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html) documenta `subsample_freq=0` como default sem subsampling periódico.

A evidência de runtime desta R05 será registrada no relatório da sprint. Sem publicação Databricks, homologação de workspace ou revisão independente presumida.
````

## 33. R0157 — `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O [notebook](exemplo_tabnet_wrapper.py) instala `pytorch-tabnet` e reinicia o Python. Nesta R05, a prosa é ajustada para não apresentar máscaras como explicação causal ou afirmar que TabNet é universalmente “último recurso”.
````

## 34. R0157 — `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. O [repositório oficial `pytorch-tabnet`](https://github.com/dreamquark-ai/tabnet) documenta parâmetros, tarefas e instalação. A implementação oficial de [`_compute_feature_importances`](https://github.com/dreamquark-ai/tabnet/blob/develop/pytorch_tabnet/abstract_model.py) mostra a agregação/normalização da explicação global usada em `feature_importances_`.

A evidência de runtime desta R05 será registrada no relatório. Sem publicação Databricks, homologação de workspace ou auditoria independente presumida.
````

## 35. R0158 — `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook histórico explicava a codificação categórica como se cada linha usasse literalmente as “linhas anteriores” em ordem temporal e fazia analogia com point-in-time join. Essa leitura é imprecisa. CatBoost usa técnicas ordenadas/permutadas para reduzir o viés e o vazamento de target das estatísticas categóricas; isso **não** certifica disponibilidade temporal das features e não substitui `pit_join`.
````

## 36. R0158 — `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. Fontes primárias consultadas em 12/09/2026: [features categóricas no CatBoost](https://catboost.ai/docs/en/features/categorical-features), [parâmetro `has_time` e ordem/permutação](https://catboost.ai/docs/en/references/training-parameters/common) e [FAQ com referências ao ordered boosting/ordered categorical statistics](https://catboost.ai/docs/en/concepts/faq).

A evidência de runtime desta R05 será registrada no relatório da sprint. Este README não afirma homologação Databricks, publicação em workspace nem revisão independente.
````

## 37. R0159 — `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook histórico exibe um bloco abreviado dos defaults e uma interpretação de `subsample=0.8` como aleatoriedade de linhas. A fonte de verdade atual é `DEFAULT_PARAMS_*` na implementação; como `subsample_freq` não é definido, não trate aquela frase histórica como descrição do comportamento atual.
````

## 38. R0159 — `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O contrato específico foi conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. Fontes primárias consultadas em 12/09/2026: [API `LGBMClassifier`](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html), incluindo `subsample_freq=0`, e [callback de early stopping](https://lightgbm.readthedocs.io/en/v4.6.0/pythonapi/lightgbm.early_stopping.html). O comportamento local dos defaults vem do código do Hub, não dessas páginas.

A evidência de runtime desta R05 será registrada no relatório da sprint; este README não presume publicação no Databricks, homologação em qualquer workspace nem revisão independente.
````

## 39. R0160 — `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Resultados próximos de LightGBM e XGBoost não provam que “o número veio do dado”: ambos podem compartilhar o mesmo vazamento ou viés. Tampouco uma diferença pequena pode ser declarada ruído sem analisar variabilidade e relevância. Os números históricos do notebook foram preservados, mas suas conclusões precisam desses limites.
````

## 40. R0160 — `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato conferido na implementação, fachada e notebook da base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. Fontes primárias externas, consultadas em 12/09/2026: [árvores impulsionadas](https://xgboost.readthedocs.io/en/stable/tutorials/model.html), [interface de estimadores](https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html), [previsão e parada](https://xgboost.readthedocs.io/en/stable/prediction.html), [vazamento de dados](https://scikit-learn.org/stable/common_pitfalls.html) e [autologging Databricks](https://docs.databricks.com/aws/en/mlflow/databricks-autologging). Cada uma sustenta o assunto ao qual foi associada no texto; não certifica este wrapper inteiro.

Revisão R02: leitura técnica e didática pelo próprio autor. Os testes locais sintéticos da sprint usam XGBoost 3.1.3 e logging desligado; não são as saídas históricas do notebook. Teste no Databricks, teste de tracking remoto e auditoria independente não fazem parte dessa evidência. Aceite humano do piloto permanece separado. Na revisão de fechamento de 12/09/2026, os três modos foram novamente exercitados localmente. Foram também reproduzidas a passagem de três classes pela checagem inicial de `binary` e a recusa de classes `1, 2, 3` pelo estimador multiclasse, com XGBoost 3.1.3 real e logging desligado. Essas verificações caracterizam o contrato e suas lacunas, não homologam produção.
````

## 41. R0352 — `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/exemplo_lgbm_ranker.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 42. R0365 — `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/exemplo_tabnet_wrapper.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 43. R0366 — `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/exemplo_train_catboost.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 44. R0366 — `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/exemplo_train_catboost.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC 2. O CatBoost escreve `catboost_info/` no diretório de trabalho por
# MAGIC    padrão. No Databricks isso é a **pasta do notebook**, e a primeira
# MAGIC    execução deste exemplo deixou dez arquivos de log publicados dentro de
# MAGIC    `.assistant/hub_snippets/ml/train_catboost/`. Foi o `--verify` da
# MAGIC    publicação que apanhou.
# MAGIC
# MAGIC    A correção ficou **no módulo**, não aqui: `train_catboost.py` agora
# MAGIC    define `allow_writing_files=False` por padrão. A primeira versão desta
# MAGIC    correção estava nesta célula, e isso deixava a mina armada para
# MAGIC    qualquer outro chamador — inclusive as skills, que recomendam o módulo
# MAGIC    por caminho de import. Quem quiser os logs sobrescreve com
# MAGIC    `params_override={"allow_writing_files": True}`.
````

## 45. R0367 — `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/exemplo_train_lgbm.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 46. R0367 — `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/exemplo_train_lgbm.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC **Como ler.** O bloco histórico acima é um extrato: a constante atual também contém `objective`, `metric`, `random_state` e `verbose`, que a célula Python imprime. Use `DEFAULT_PARAMS_BINARY` e `model.get_params()` como inventário técnico; não conte o bloco colado como lista completa. Alguns valores coincidem com defaults da biblioteca e outros são escolhas locais.
````

## 47. R0368 — `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
````

## 48. R0136 — `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base da R08. Como referência de runtime, a documentação oficial do PyTorch descreve `BatchNorm1d` e suas estatísticas por mini-batch: <https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html>.

A revisão R08 distingue leitura estática, teste local e teste de runtime. Ela não presume publicação no Databricks, homologação do detector nem auditoria independente.
````

## 49. R0137 — `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook R08 usa exatamente esse cenário sintético.
````

## 50. R0137 — `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base da R08. As métricas aqui são cálculos locais definidos no código; não há uma norma estatística externa que transforme o campo chamado `z_score` em teste de hipótese.

A revisão R08 não presume publicação Databricks, homologação de segmentação nem auditoria independente.
````

## 51. R0138 — `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base da R08. A API oficial do scikit-learn documenta `silhouette_score`, `calinski_harabasz_score` e `davies_bouldin_score`: <https://scikit-learn.org/stable/api/sklearn.metrics.html>.

A revisão R08 não presume publicação Databricks, homologação de segmentação nem auditoria independente.
````

## 52. R0142 — `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Comportamento conferido na implementação da base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. Para conceito e score, foram consultados em 12/09/2026 o [guia de outliers](https://scikit-learn.org/stable/modules/outlier_detection.html) e a [API IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html); para efeitos da sessão, a [documentação de autologging](https://docs.databricks.com/aws/en/mlflow/databricks-autologging).

A redação inicial e a revisão de fechamento R02 são autorrevisões, não auditorias independentes. Em 12/09/2026, a [execução suplementar da R02](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982) aprovou testes de treino, perfil e empates com scikit-learn e MLflow reais, sem habilitar o logging do helper. Esse resultado é evidência histórica identificada: o ambiente local do fechamento continua sem MLflow e não repete esses testes usando um módulo falso. Não houve teste de tracking remoto ou homologação Databricks. Saídas históricas do notebook não são novas execuções desta documentação.
````

## 53. R0148 — `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O [notebook](exemplo_mlp_embeddings.py) instala PyTorch e reinicia a sessão. A prosa histórica será ajustada nesta R05 para não dizer que one-hot “não expressa” relações ou que árvores necessariamente deixam de aprendê-las; o ponto correto é que embeddings oferecem uma representação densa compartilhável que deve ser comparada empiricamente.
````

## 54. R0148 — `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R05.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. A documentação oficial de [`torch.nn.Embedding`](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding) descreve a camada como tabela de lookup de tamanho e dimensão fixos, indexada por inteiros.

A evidência de runtime desta R05 será registrada no relatório. Este README não afirma publicação no Databricks, superioridade sobre árvores nem auditoria independente.
````

## 55. R0161 — `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/README.md`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
> **Atualização V07 — estado atual.** `plot_umap_clusters` permanece a rota
> legada. `plot_umap_clusters_resolvido(..., theme)` valida o tema antes do
> cálculo, chama o mesmo `compute_umap` e troca somente paleta/layout. Coordenadas,
> labels, opacidade e tamanho solicitado não são recalculados por uma segunda
> lógica. `umap-learn` continua importado de forma lazy; selecionar um tema não
> instala dependências nem prova estabilidade dos clusters.
````

## 56. R0161 — `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O módulo usa um `TEMA_BASE` e constantes visuais legadas diretamente; `plot_umap_clusters` **não recebe `ResolvedTheme` nem usa a rota V04 `_resolvido`**. Isso é estado atual documentado, não uma migração silenciosa do sistema de temas.
````

## 57. R0161 — `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base da R08. A documentação oficial do UMAP descreve o efeito de `n_neighbors`, `min_dist` e `n_components`: <https://umap-learn.readthedocs.io/en/latest/parameters.html> e <https://umap-learn.readthedocs.io/en/latest/api.html>.

A revisão R08 não presume publicação Databricks, homologação visual/analítica nem auditoria independente.
````

## 58. R0344 — `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 59. R0345 — `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC O bloco histórico abaixo é **abreviado**: a célula imprime todas as combinações cluster × feature, mas aqui foram preservadas apenas seis linhas como amostra visual:
````

## 60. R0346 — `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC A tabela histórica abaixo corresponde a `resultado_k["scores"]`, com `best_k` mostrado separadamente. A chamada `select_k` devolve um **dict**, portanto o `print(resultado_k)` literal da célula tem outra representação textual:
````

## 61. R0350 — `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
````

## 62. R0350 — `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC positivos com evidência adicional. As saídas antigas não foram reexecutadas
# MAGIC para preencher esta revisão documental.
````

## 63. R0356 — `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/exemplo_mlp_embeddings.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.
````

## 64. R0140 — `ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da R09. Referência primária para KS: documentação SciPy de `ks_2samp`. PSI/CSI são implementações locais cuja discretização, smoothing e thresholds devem ser tratados como parte do contrato do Hub, não como defaults universais.
````

## 65. R0147 — `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Um baseline de propensão é registrado com versão do dataset, split temporal, limitações, hiperparâmetros, métricas e exemplo de entrada. No E0, uma regra sintética que classificou quatro entidades pode registrar 1 TRUE, 1 FALSE e 2 INDETERMINADO, além de referência da execução. O teste local usa MLflow simulado: verifica chamadas e falhas, sem provar backend real ou Databricks Free.
````

## 66. R0147 — `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`

Referência histórica indicada na auditoria: `docs/sprints/micromodelos/RELATORIO_ENTREGA_LAB.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O SHA repetido ilustra a forma do campo, não é fingerprint de uma especificação real. O exemplo acima é ilustrativo; a prova com fingerprint MM02 real e backend MLflow local está em `tools/micromodelo_mm06_e0_tracking.py` e no relatório de entrega do laboratório. Em 2026-09-29, três runs sintéticas foram gravadas e relidas no Databricks Free com fingerprint e `mm06.complete=true`; a prova e suas limitações estão no `docs/sprints/micromodelos/RELATORIO_ENTREGA_LAB.md` no repositório. Essa execução se limita ao experimento pessoal e à configuração explícita usada no ensaio.
````

## 67. R0147 — `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`

Referência histórica indicada na auditoria: `docs/sprints/micromodelos/RELATORIO_ENTREGA_LAB.md`. O trecho é preservado aqui sem alterar o registro original.

````text
A [implementação](mlflow_run.py) contém ambos os contextos e a [fachada](__init__.py) reexporta `run_governado` e `run_micromodelo`. O [notebook](exemplo_mlflow_run.py) demonstra o caminho legado e documenta uma limitação observada de runtime; o teste MM06 novo usa fake MLflow e não substitui exemplo real.
````

## 68. R0147 — `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da R09. Referência primária: documentação oficial do MLflow para Tracking, `start_run`, logging e model flavors.

Revalide a versão e o comportamento no runtime Databricks de destino antes de transformar observações do notebook em regra operacional.
````

## 69. R0150 — `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/README.md`

Referência histórica indicada na auditoria: `docs/sprints/sistema_temas/V07/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
> **Atualização V07 — estado atual.** `PerformanceMonitor.plot_timeline(metric)`
> continua legado. `plot_timeline_resolvido(metric, theme)` reutiliza exatamente
> o mesmo histórico, baseline e thresholds e altera apenas aparência:
> `brand.primary` para a série, `text.secondary` para baseline,
> `semantic.warning` para warning e `semantic.negative` para critical. A rota
> temática não altera `should_retrain`, não recalibra a política e não autoriza
> retreino automático.
````

## 70. R0150 — `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da R09. Os thresholds são política local, não defaults de Databricks, MLflow ou scikit-learn. Para as figuras, consulte a documentação oficial do Plotly.
````

## 71. R0355 — `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ## 3. O registro completo — e a observação histórica deste runtime
# MAGIC
# MAGIC Esta é a seção que importa: o caminho feliz do helper, com parâmetros,
# MAGIC métricas e assinatura. A célula abaixo tenta executá-lo de verdade.
````

## 72. R0355 — `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO no laboratório
# MAGIC
# MAGIC O que rodaria : run_governado(...) com parametros, metricas e modelo
# MAGIC Por que não   : AnalysisException: [CONFIG_NOT_AVAILABLE.WITHOUT_SUGGESTION]
# MAGIC                 Configuration spark.mlflow.modelRegistryUri is not available.
# MAGIC                 `mlflow.start_run` instancia um MlflowClient, que resolve o
# MAGIC                 registry URI lendo essa config da sessão Spark. No
# MAGIC                 serverless, o Spark Connect recusa devolvê-la, e a exceção
# MAGIC                 acontece na ABERTURA do bloco — nenhum registro chega a ser
# MAGIC                 tentado.
# MAGIC Onde verificar: .claude/rules/free-vs-trabalho.md, matriz de runtime
# MAGIC O que falta   : compute clássico, ou uma versão do MLflow que não leia essa
# MAGIC                 config. Não é ajustável pelo helper.
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** É impedimento de runtime, não de escopo: a biblioteca não
# MAGIC inicializa aqui. A célula acima captura a exceção em vez de escondê-la,
# MAGIC então o notebook continua sendo executável e se auto-verifica. Em outro runtime, inclusive clássico, execute novamente: o sucesso depende do tracking/configuração vigentes.
# MAGIC
# MAGIC **E há um detalhe que vale mais que o erro em si.** Este mesmo caminho foi
# MAGIC testado no laboratório em **14/08/2026** e passou:
# MAGIC `docs/testes/spark/resultados/` registra `mlflow_run.completo` como
# MAGIC `"run completo aceito"`. Três dias depois, no mesmo tipo de compute, ele
# MAGIC não abre. O registro de 14/08 não está errado — descreve o que era verdade
# MAGIC então. O que mudou foi o runtime do Free, por baixo, sem aviso.
# MAGIC
# MAGIC A lição é sobre método: **"foi testado" tem data de validade em ambiente
# MAGIC gerenciado.** Um teste de três dias atrás não é garantia de hoje, e é por
# MAGIC isso que a verificação vale mais que o registro dela.
````

## 73. R0358 — `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/exemplo_performance_monitor.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC ### Contrato atualizado em 09/09/2026
# MAGIC Seleção de métricas: valores inválidos selecionados pela política agora geram erro. Use metricas_obrigatorias para exigir auc e ks_pct; para excluir uma métrica deliberadamente, forneça uma política sem essa chave. KS antigo em 0–100 mantém o valor ao migrar para ks_pct.
````

## 74. R0152 — `ambiente_fonte/.assistant/hub_snippets/ml/score_bands/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Para scorecard de pontos, veja [scorecard_builder](../scorecard_builder/README.md). Para métricas discriminatórias globais, `metrics_report` entra na R09. Para bins fixos de risco, uma transformação explícita com limites versionados pode ser mais adequada que quantis recalculados.
````

## 75. R0152 — `ambiente_fonte/.assistant/hub_snippets/ml/score_bands/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R07.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. Fonte primária consultada em 12/09/2026: documentação `pandas.qcut`, que define discretização por quantis e `duplicates="drop"` para bordas não únicas.

Este README não presume aprovação de política, publicação no Databricks nem auditoria independente.
````

## 76. R0153 — `ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
O notebook histórico diz que pontos tornam a decisão “auditável por quem não lê código”. A tabela ajuda na rastreabilidade, mas auditabilidade real também exige regras de binning, versão, origem dos dados, política, testes e trilha de aprovação.
````

## 77. R0153 — `ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R07.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. A transformação usa a relação log-odds da regressão logística e a convenção local de PDO/base score/base odds codificada no helper. Não existe neste README alegação de que essa parametrização seja uma exigência regulatória universal.

Este README não presume homologação do scorecard, publicação no Databricks nem auditoria independente.
````

## 78. R0164 — `ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/README.md`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/RELATORIO_R07.md`. O trecho é preservado aqui sem alterar o registro original.

````text
Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. A fórmula, smoothing e faixas de classificação descritas aqui são as que o código do Hub implementa; as faixas de IV não são apresentadas como norma externa obrigatória.

Este README não presume seleção automática de variável, aprovação regulatória, publicação no Databricks nem auditoria independente.
````

## 79. R0361 — `ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/exemplo_scorecard_builder.py`

Referência histórica indicada na auditoria: `docs/sprints/readmes_objetos/README.md`. O trecho é preservado aqui sem alterar o registro original.

````text
# MAGIC Executado no laboratório, o bloco histórico abaixo é **abreviado**: o código
# MAGIC imprime também as linhas de `tempo_woe`, mas o output colado antigo não as contém.
# MAGIC O bloco é preservado como evidência histórica, não como schema completo do retorno.
````
