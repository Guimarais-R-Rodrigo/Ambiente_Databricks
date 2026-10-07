# Leitura dos arquivos de modelagem

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt09-code-map"></a>
<a id="mt09-code-map"></a>
### Leitura dos arquivos de modelagem

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Na modelagem, a ficha exige atenção à orientação da métrica, ao tipo de estimador retornado e ao registro de artefatos. Ajustar, prever, explicar e registrar são etapas com contratos diferentes.

Reconciliado com a fonte de 07/10/2026: 46 arquivos, 33 com bytes preservados e 13 com alterações em comentários de notebook. As fichas conservam o mérito das leituras anteriores; os comentários alterados foram confrontados com a implementação. Os hashes abaixo identificam os arquivos atuais. Isso não representa reexecução dos exemplos nem homologação de runtime.

<a id="mt09-code-map-file-001"></a>
#### 1. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/__init__.py` · SHA-256 `041655c508ce21d4699325c4de5efbea685dffef0efed4b52f2109288661f459` |
| Papel e motivo técnico | Marcar namespace ml sem registrar/exportar modelos. |
| Nomes disponibilizados | nenhum |
| Entradas | import de pacote |
| Saídas | namespace Python |
| Efeitos | nenhum efeito operacional observado |
| Dependências e momento de uso | nenhuma |
| Como interpretar este arquivo | Este `__init__.py` contém somente docstring e não reexporta modelos no namespace ml. Importar o pacote não registra, ajusta, valida nem exporta modelo; as operações estão nos módulos de família e dependem de chamada explícita. |

<a id="mt09-code-map-file-002"></a>
#### 2. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/arima_wrapper/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/__init__.py` · SHA-256 `2da192b59cf2d505a7a94b6a02bc0f06c012978f4c9790133dadfb88477ed853` |
| Papel e motivo técnico | Série univariada regularmente espaçada; distinguir horizonte em passos de meses e métricas ajustadas de backtest. |
| Nomes disponibilizados | SEED, train_arima |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; train_arima(series,m=12,forecast_periods=6,seasonal=True,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | numpy/pandas/mlflow importados no topo; pmdarima importado na chamada. |
| Como interpretar este arquivo | A fachada reexporta SEED, train_arima; importar o pacote carrega as dependências de topo (numpy/pandas/mlflow importados no topo; pmdarima importado na chamada.), mas não chama a operação. O horizonte é contado em passos da frequência da série, não necessariamente em meses. RMSE e MAPE são calculados sobre o ajuste; não equivalem a backtest. O intervalo de confiança calculado não integra o retorno; zeros no denominador do MAPE exigem atenção. |

<a id="mt09-code-map-file-003"></a>
#### 3. `arima_wrapper.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/arima_wrapper/arima_wrapper.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/arima_wrapper.py` · SHA-256 `6f5914712ad2552f891d7ed5f3d63f948bf736b4e281028837b901b2efd9d1ca` |
| Papel e motivo técnico | Série univariada regularmente espaçada; distinguir horizonte em passos de meses e métricas ajustadas de backtest. |
| Nomes disponibilizados | SEED; train_arima(series,m=12,forecast_periods=6,seasonal=True,log_mlflow=True) |
| Entradas | Série univariada numérica em ordem cronológica: assinatura `np.ndarray`, com `Series` pandas compatível; m, horizonte e flags sazonal/log. |
| Saídas | (modelo pmdarima, forecast ndarray, metrics AIC/BIC/ordens/RMSE/MAPE in-sample); intervalo de confiança calculado e descartado. |
| Efeitos | `pmdarima.auto_arima` ajusta modelo; MLflow registra parâmetros/métricas somente se `log_mlflow=True`. O helper não imprime resumo, não chama `model.summary()` e não grava arquivo explícito. |
| Dependências e momento de uso | numpy/pandas/mlflow importados no topo; pmdarima importado na chamada. |
| Como interpretar este arquivo | O horizonte conta passos da frequência, não necessariamente meses. RMSE e MAPE são do ajuste, não backtest. Para MAPE, `series != 0` exclui zeros do denominador; sem observações válidas o valor fica indefinido. Aceita série numérica ordenada como `np.ndarray` da assinatura ou `Series` pandas compatível. Retorna modelo, previsão e métricas; calcula intervalo de confiança mas o descarta. O helper não imprime resumo nem chama `model.summary()`; eventual impressão pertence ao chamador. MLflow só registra explicitamente quando `log_mlflow=True`. |

<a id="mt09-code-map-file-004"></a>
#### 4. `exemplo_arima_wrapper.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/arima_wrapper/exemplo_arima_wrapper.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/exemplo_arima_wrapper.py` · SHA-256 `ef3df0ef27a97e6033e3589e3700e982c07d013374cfae5fef3dae7fb6e1bdad` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Série univariada regularmente espaçada; distinguir horizonte em passos de meses e métricas ajustadas de backtest. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; train_arima(series,m=12,forecast_periods=6,seasonal=True,log_mlflow=True) |
| Entradas | fixture sintética local em `np.ndarray` numérico univariado, ordenado cronologicamente; `Series` pandas compatível também pode ser entrada do helper; periodicidade m, horizonte e flags. |
| Saídas | Notebook instala pmdarima==2.0.4 e numpy==1.23.5, reinicia Python, cria série sintética, usa log_mlflow=False; números são laboratório histórico. |
| Efeitos | células `%pip`/`%restart_python`, consulta `spark.sql("SELECT current_user()").first()` antes de `sys.path`, ajuste local ARIMA e `print` de modelo/previsão/métricas no notebook. `log_mlflow=False` desliga registro explícito do helper; ele não imprime resumo nem grava arquivo. |
| Dependências e momento de uso | numpy/pandas/mlflow importados no topo; pmdarima importado na chamada. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | O notebook passa um `np.ndarray` numérico ordenado ao helper; `Series` pandas compatível também é aceita. Horizonte em passos não equivale sempre a meses; RMSE e MAPE são in-sample. MAPE exclui `series == 0` e, se nenhuma observação resta, fica indefinido. O helper retorna modelo, previsão e métricas sem imprimir resumo; os `print` de ordem, previsão e métricas são células do exemplo. Os números colados são históricos; `log_mlflow=False` só desliga o registro explícito do helper, sem controlar autologging externo. |

<a id="mt09-code-map-file-005"></a>
#### 5. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/autoencoder_anomaly/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/__init__.py` · SHA-256 `bfe6424835f0bee7bd490c8f4273dc1ffd2f05ece0f1ff87520e62b6fcc133eb` |
| Papel e motivo técnico | Erro de reconstrução alto sugere anomalia; limiar é percentil do treino normal, não probabilidade. |
| Nomes disponibilizados | SEED, Autoencoder, train_autoencoder_anomaly |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; Autoencoder; train_autoencoder_anomaly(X_train_normal,X_test,encoding_dim=16,epochs=100,batch_size=256,lr=.001,patience=10,threshold_percentile=95,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | torch e numpy no topo; mlflow import protegido e exigido para logging. |
| Como interpretar este arquivo | A fachada reexporta SEED, Autoencoder, train_autoencoder_anomaly; importar o pacote carrega as dependências de topo (torch e numpy no topo; mlflow import protegido e exigido para logging.), mas não chama a operação. O limiar é percentil dos erros de reconstrução do treino normal, não probabilidade de fraude. O retorno contém erros alinhados ao teste, sem rótulos; escalar fora e dentro do helper muda a interpretação dos valores. |

<a id="mt09-code-map-file-006"></a>
#### 6. `autoencoder_anomaly.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/autoencoder_anomaly/autoencoder_anomaly.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/autoencoder_anomaly.py` · SHA-256 `d4a7ea89c695782faf13c123930244a4583ddba01e298c7e2d19c9895b342e6f` |
| Papel e motivo técnico | Erro de reconstrução alto sugere anomalia; limiar é percentil do treino normal, não probabilidade. |
| Nomes disponibilizados | SEED; Autoencoder; train_autoencoder_anomaly(X_train_normal,X_test,encoding_dim=16,epochs=100,batch_size=256,lr=.001,patience=10,threshold_percentile=95,log_mlflow=True) |
| Entradas | ndarrays 2D finitos, mesmas colunas, treino >=2 e teste não vazio; batch>1, percentil em (0,100). |
| Saídas | (modelo torch, threshold dos erros de treino, test_errors alinhados à ordem do teste); sem labels. |
| Efeitos | Treina rede, imprime contagem acima do limiar; MLflow somente se True. |
| Dependências e momento de uso | torch e numpy no topo; mlflow import protegido e exigido para logging. |
| Como interpretar este arquivo | O limiar é percentil dos erros de reconstrução do treino normal, não probabilidade de fraude. O retorno contém erros alinhados ao teste, sem rótulos; escalar fora e dentro do helper muda a interpretação dos valores. Entrada: ndarrays 2D finitos, mesmas colunas, treino >=2 e teste não vazio; batch>1, percentil em (0,100). Saída: (modelo torch, threshold dos erros de treino, test_errors alinhados à ordem do teste); sem labels. Efeitos da chamada: Treina rede, imprime contagem acima do limiar; MLflow somente se True. Dependências: torch e numpy no topo; mlflow import protegido e exigido para logging. |

<a id="mt09-code-map-file-007"></a>
#### 7. `exemplo_autoencoder_anomaly.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py` · SHA-256 `2f1d1418c515331840cf26215badd517a85de8452daa7734df1e962aa1a0bafb` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Erro de reconstrução alto sugere anomalia; limiar é percentil do treino normal, não probabilidade. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; Autoencoder; train_autoencoder_anomaly(X_train_normal,X_test,encoding_dim=16,epochs=100,batch_size=256,lr=.001,patience=10,threshold_percentile=95,log_mlflow=True) |
| Entradas | fixture sintética local; ndarrays 2D finitos, mesmas colunas, treino >=2 e teste não vazio; batch>1, percentil em (0,100). |
| Saídas | Notebook instala torch, reinicia, simula normais/anômalos, escala externamente, chama log_mlflow=False; helper também escala internamente; contagens históricas. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; Treina rede, imprime contagem acima do limiar; MLflow somente se True. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | torch e numpy no topo; mlflow import protegido e exigido para logging. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | O limiar é percentil dos erros de reconstrução do treino normal, não probabilidade de fraude. O retorno contém erros alinhados ao teste, sem rótulos; escalar fora e dentro do helper muda a interpretação dos valores. O exemplo usa esta fixture e sequência: Notebook instala torch, reinicia, simula normais/anômalos, escala externamente, chama log_mlflow=False; helper também escala internamente; contagens históricas. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-008"></a>
#### 8. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/cluster_profiling/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/__init__.py` · SHA-256 `2d9e3bf8dd37f40c960c6716ecd0009c20254a2158b98d622c00c952279bb48e` |
| Papel e motivo técnico | Descrever grupos já atribuídos sem converter diferença descritiva em persona ou significância. |
| Nomes disponibilizados | profile_clusters, top_differentiators |
| Entradas | import do namespace da família; assinaturas da implementação: profile_clusters(df,feature_cols,cluster_col="cluster_id"); top_differentiators(profiles_df,cluster_id,top_n=5) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | pandas/numpy no topo. |
| Como interpretar este arquivo | A fachada reexporta profile_clusters, top_differentiators; importar o pacote carrega as dependências de topo (pandas/numpy no topo.), mas não chama a operação. O perfil descreve clusters já atribuídos; uma diferença ou ranking não demonstra persona nem significância. Quando a média global é zero, o índice relativo não tem base interpretável, embora o z-score ainda possa ordenar variáveis. |

<a id="mt09-code-map-file-009"></a>
#### 9. `cluster_profiling.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/cluster_profiling/cluster_profiling.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/cluster_profiling.py` · SHA-256 `88680467a361f4ad9590ab1a391f25e343db9467928de23cc69f82780e7b477e` |
| Papel e motivo técnico | Descrever grupos já atribuídos sem converter diferença descritiva em persona ou significância. |
| Nomes disponibilizados | profile_clusters(df,feature_cols,cluster_col="cluster_id"); top_differentiators(profiles_df,cluster_id,top_n=5) |
| Entradas | DataFrame pandas com rótulo de cluster e features numéricas; perfil prévio para diferenciadores. |
| Saídas | Tabela longa por cluster/feature com média, índice relativo e z_score; tabela top_n por abs(z_score). |
| Efeitos | profile_clusters imprime distribuição; não escreve nem treina. |
| Dependências e momento de uso | pandas/numpy no topo. |
| Como interpretar este arquivo | O perfil descreve clusters já atribuídos; uma diferença ou ranking não demonstra persona nem significância. Quando a média global é zero, o índice relativo não tem base interpretável, embora o z-score ainda possa ordenar variáveis. Entrada: DataFrame pandas com rótulo de cluster e features numéricas; perfil prévio para diferenciadores. Saída: Tabela longa por cluster/feature com média, índice relativo e z_score; tabela top_n por abs(z_score). Efeitos da chamada: profile_clusters imprime distribuição; não escreve nem treina. Dependências: pandas/numpy no topo. |

<a id="mt09-code-map-file-010"></a>
#### 10. `exemplo_cluster_profiling.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py` · SHA-256 `bba166db5c5b0e1d1045466560630c33fd700a56699301a6049a93fd30818449` |
| Reconciliação dos comentários atuais | Delta MAGIC explica que as seis linhas são amostra abreviada; o retorno contém todas as combinações cluster × feature. |
| Papel e motivo técnico | Descrever grupos já atribuídos sem converter diferença descritiva em persona ou significância. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de profile_clusters(df,feature_cols,cluster_col="cluster_id"); top_differentiators(profiles_df,cluster_id,top_n=5) |
| Entradas | fixture sintética local; DataFrame pandas com rótulo de cluster e features numéricas; perfil prévio para diferenciadores. |
| Saídas | Notebook driver-side cria três grupos sintéticos, dois quase iguais, imprime perfis/ranking; nenhuma escrita. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; profile_clusters imprime distribuição; não escreve nem treina. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | pandas/numpy no topo. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | O perfil descreve clusters já atribuídos; uma diferença ou ranking não demonstra persona nem significância. Quando a média global é zero, o índice relativo não tem base interpretável, embora o z-score ainda possa ordenar variáveis. O exemplo usa esta fixture e sequência: Notebook driver-side cria três grupos sintéticos, dois quase iguais, imprime perfis/ranking; nenhuma escrita. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-011"></a>
#### 11. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/clustering_suite/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/__init__.py` · SHA-256 `d97843f4c57663a0477f52a8d6809fb384432bdae30e121160210fb61f3dfc07` |
| Papel e motivo técnico | Separar heurística de k, escala e rótulos; DBSCAN não usa k. |
| Nomes disponibilizados | SEED, select_k, run_clustering_pipeline |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; select_k(X_scaled,k_range=range(2,11),method="both"); run_clustering_pipeline(df,feature_cols,k=None,k_range=range(2,11),algorithm="kmeans",scaler="standard",log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório na importação. |
| Como interpretar este arquivo | A fachada reexporta SEED, select_k, run_clustering_pipeline; importar o pacote carrega as dependências de topo (numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório na importação.), mas não chama a operação. A seleção de k é heurística sobre dados escalados; no método elbow com pelo menos três pontos, a implementação usa segunda diferença da inércia. DBSCAN não usa k, exclui ruído das métricas e pode ficar sem silhueta. |

<a id="mt09-code-map-file-012"></a>
#### 12. `clustering_suite.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/clustering_suite/clustering_suite.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/clustering_suite.py` · SHA-256 `937f8875982a634298f1f0209b1924bd406ca149e05aa2e55ec8e8ab010ed058` |
| Papel e motivo técnico | Separar heurística de k, escala e rótulos; DBSCAN não usa k. |
| Nomes disponibilizados | SEED; select_k(X_scaled,k_range=range(2,11),method="both"); run_clustering_pipeline(df,feature_cols,k=None,k_range=range(2,11),algorithm="kmeans",scaler="standard",log_mlflow=True) |
| Entradas | select_k recebe ndarray já escalado e k válidos 2..n-1; pipeline recebe pandas finito com >=3 linhas/colunas existentes. |
| Saídas | select_k -> {scores DataFrame,best_k}; pipeline -> {labels,metrics,model,scaler,X_scaled}. |
| Efeitos | fit local e prints; mlflow.log_params/log_metrics quando True. |
| Dependências e momento de uso | numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório na importação. |
| Como interpretar este arquivo | A seleção de k é heurística sobre dados escalados; no método elbow com pelo menos três pontos, a implementação usa segunda diferença da inércia. DBSCAN não usa k, exclui ruído das métricas e pode ficar sem silhueta. Entrada: select_k recebe ndarray já escalado e k válidos 2..n-1; pipeline recebe pandas finito com >=3 linhas/colunas existentes. Saída: select_k -> {scores DataFrame,best_k}; pipeline -> {labels,metrics,model,scaler,X_scaled}. Efeitos da chamada: fit local e prints; mlflow.log_params/log_metrics quando True. Dependências: numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório na importação. |

<a id="mt09-code-map-file-013"></a>
#### 13. `exemplo_clustering_suite.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py` · SHA-256 `337d1657f269ffc2e381ca76b2ba7e3f82d4bfc09bbc25c4155cae3a8786342a` |
| Reconciliação dos comentários atuais | Delta MAGIC distingue dict retornado de scores.to_string(index=False) e best_k; tabela colada não é o repr literal do dict. |
| Papel e motivo técnico | Separar heurística de k, escala e rótulos; DBSCAN não usa k. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; select_k(X_scaled,k_range=range(2,11),method="both"); run_clustering_pipeline(df,feature_cols,k=None,k_range=range(2,11),algorithm="kmeans",scaler="standard",log_mlflow=True) |
| Entradas | fixture sintética local; select_k recebe ndarray já escalado e k válidos 2..n-1; pipeline recebe pandas finito com >=3 linhas/colunas existentes. |
| Saídas | Notebook cria três nuvens, chama select_k diretamente sobre pontos sem escalonamento (mesma escala sintética) e pipeline com k=3/log_mlflow=False; nenhuma escrita. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; fit local e prints; mlflow.log_params/log_metrics quando True. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório na importação. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | A seleção de k é heurística sobre dados escalados; no método elbow com pelo menos três pontos, a implementação usa segunda diferença da inércia. DBSCAN não usa k, exclui ruído das métricas e pode ficar sem silhueta. O exemplo usa esta fixture e sequência: Notebook cria três nuvens, chama select_k diretamente sobre pontos sem escalonamento (mesma escala sintética) e pipeline com k=3/log_mlflow=False; nenhuma escrita. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-014"></a>
#### 14. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/isolation_forest/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/__init__.py` · SHA-256 `203bb7b2664aa2635048e64d76a6bd53269f5a812b61a950bf4be4a10ffa9521` |
| Papel e motivo técnico | Priorizar casos com menor decision_function; contamination calibra corte, não prevalência. |
| Nomes disponibilizados | SEED, train_isolation_forest, profile_anomalies |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; train_isolation_forest(df,feature_cols,contamination=.01,n_estimators=200,max_samples="auto",scaler="standard",log_mlflow=True); profile_anomalies(df,feature_cols,scores,labels,top_n=50) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório mesmo se False. |
| Como interpretar este arquivo | A fachada reexporta SEED, train_isolation_forest, profile_anomalies; importar o pacote carrega as dependências de topo (numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório mesmo se False.), mas não chama a operação. Na decision_function, valores menores e mais negativos indicam maior anomalia. contamination calibra o corte do estimador, não mede a prevalência verdadeira; o limiar estatístico mostrado é aproximação, não regra exata. |

<a id="mt09-code-map-file-015"></a>
#### 15. `exemplo_isolation_forest.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py` · SHA-256 `0aaa05227e708f10aa5fdbb541c770a6b40b1173ff199cb7ef234a208e436c99` |
| Reconciliação dos comentários atuais | Deltas MAGIC explicitam fixture sem eficácia de produção, ausência de garantia numérica e necessidade de avaliar também casos não marcados. |
| Papel e motivo técnico | Demonstrar treino Isolation Forest e efeito de três valores de contamination no corte; o perfil de anomalias é API relacionada, não exercitada pelo notebook. |
| Nomes disponibilizados | notebook Databricks; importa train_isolation_forest(df,feature_cols,contamination=.01,n_estimators=200,max_samples="auto",scaler="standard",log_mlflow=True) e profile_anomalies(df,feature_cols,scores,labels,top_n=50); chama somente train_isolation_forest. |
| Entradas | fixture sintética local; DataFrame e colunas numéricas usados no treino; scores/labels para profile_anomalies seriam entradas de outra chamada, ausente aqui. |
| Saídas | Notebook simula 30 anômalos em 3000 e chama treino para três contaminações com log_mlflow=False; não chama profile_anomalies. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; fit local para três cortes; registro MLflow explícito desligado por log_mlflow=False; não há cópia de DataFrame pelo perfil não chamado nem arquivo produzido. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório mesmo com log_mlflow=False. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | Na decision_function, valores menores e mais negativos indicam maior anomalia. contamination calibra o corte do estimador, não mede a prevalência verdadeira; o limiar estatístico mostrado é aproximação, não regra exata. O notebook importa profile_anomalies, mas exercita somente train_isolation_forest com log_mlflow=False para três contaminações; autologging externo não é controlado pela flag. Os números impressos são históricos, sem execução atual. |

<a id="mt09-code-map-file-016"></a>
#### 16. `isolation_forest.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/isolation_forest/isolation_forest.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/isolation_forest.py` · SHA-256 `4cebf50694b3fda8e9ebd02f3d7bc71a39caf7fa7efa76a94fe72adfd7fec380` |
| Papel e motivo técnico | Priorizar casos com menor decision_function; contamination calibra corte, não prevalência. |
| Nomes disponibilizados | SEED; train_isolation_forest(df,feature_cols,contamination=.01,n_estimators=200,max_samples="auto",scaler="standard",log_mlflow=True); profile_anomalies(df,feature_cols,scores,labels,top_n=50) |
| Entradas | DataFrame/colunas; scores e labels alinhados para perfil. |
| Saídas | Treino -> {scores,labels(-1/1),model,stats,scaler}; perfil -> DataFrame índice, score, maior desvio z absoluto. |
| Efeitos | fit local, prints, MLflow se True; perfil copia DataFrame; sem arquivo. |
| Dependências e momento de uso | numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório mesmo se False. |
| Como interpretar este arquivo | Na decision_function, valores menores e mais negativos indicam maior anomalia. contamination calibra o corte do estimador, não mede a prevalência verdadeira; o limiar estatístico mostrado é aproximação, não regra exata. Entrada: DataFrame/colunas; scores e labels alinhados para perfil. Saída: Treino -> {scores,labels(-1/1),model,stats,scaler}; perfil -> DataFrame índice, score, maior desvio z absoluto. Efeitos da chamada: fit local, prints, MLflow se True; perfil copia DataFrame; sem arquivo. Dependências: numpy/pandas/sklearn/mlflow importados no topo; MLflow obrigatório mesmo se False. |

<a id="mt09-code-map-file-017"></a>
#### 17. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/lgbm_ranker/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/__init__.py` · SHA-256 `720d1b2863bb0da7a11e318b88933533a7865dd0f6f4f9d8ee3f967b6a5ffa7c` |
| Papel e motivo técnico | Grupos são tamanhos de blocos consecutivos e ranking é intragrupo, não probabilidade. |
| Nomes disponibilizados | SEED, train_lgbm_ranker, evaluate_ranking |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; train_lgbm_ranker(...groups_train,...groups_val,params=None,num_boost_round=500,early_stopping_rounds=50,log_mlflow=True); evaluate_ranking(model,X,y,groups,ks=None) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | numpy/lightgbm/mlflow importados no topo. |
| Como interpretar este arquivo | A fachada reexporta SEED, train_lgbm_ranker, evaluate_ranking; importar o pacote carrega as dependências de topo (numpy/lightgbm/mlflow importados no topo.), mas não chama a operação. Os grupos são tamanhos de blocos consecutivos cujas somas devem cobrir as linhas; a ordenação interessa dentro de cada grupo e o score não é probabilidade. A docstring menciona MAP, mas o cálculo e o retorno de avaliação usam NDCG. |

<a id="mt09-code-map-file-018"></a>
#### 18. `exemplo_lgbm_ranker.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/lgbm_ranker/exemplo_lgbm_ranker.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/exemplo_lgbm_ranker.py` · SHA-256 `48736168f6353c8531d6b045b5bf528795e7143154387eee7e8d58c13a314646` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Grupos são tamanhos de blocos consecutivos e ranking é intragrupo, não probabilidade. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; train_lgbm_ranker(...groups_train,...groups_val,params=None,num_boost_round=500,early_stopping_rounds=50,log_mlflow=True); evaluate_ranking(model,X,y,groups,ks=None) |
| Entradas | fixture sintética local; X/y alinhados; vetor inteiro de grupos positivos somando linhas; relevância não negativa; ks positivos. |
| Saídas | Notebook instala LightGBM, gera 400 grupos de 10, separa por grupo, treina com log_mlflow=False e avalia k=1,3,5; histórico NDCG não é hit-rate. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; fit LightGBM e prints; MLflow se True. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | numpy/lightgbm/mlflow importados no topo. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | Os grupos são tamanhos de blocos consecutivos cujas somas devem cobrir as linhas; a ordenação interessa dentro de cada grupo e o score não é probabilidade. A docstring menciona MAP, mas o cálculo e o retorno de avaliação usam NDCG. O exemplo usa esta fixture e sequência: Notebook instala LightGBM, gera 400 grupos de 10, separa por grupo, treina com log_mlflow=False e avalia k=1,3,5; histórico NDCG não é hit-rate. A chamada usa log_mlflow=False: desliga o registro explícito do helper, mas não controla autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-019"></a>
#### 19. `lgbm_ranker.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/lgbm_ranker/lgbm_ranker.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/lgbm_ranker.py` · SHA-256 `029c2922f6acd754405ac207a9a9d735dc26cd732dbf35b54be716566d13b5cd` |
| Papel e motivo técnico | Grupos são tamanhos de blocos consecutivos e ranking é intragrupo, não probabilidade. |
| Nomes disponibilizados | SEED; train_lgbm_ranker(...groups_train,...groups_val,params=None,num_boost_round=500,early_stopping_rounds=50,log_mlflow=True); evaluate_ranking(model,X,y,groups,ks=None) |
| Entradas | X/y alinhados; vetor inteiro de grupos positivos somando linhas; relevância não negativa; ks positivos. |
| Saídas | (Booster, métricas ndcg_at_k); evaluate_ranking devolve só NDCG, apesar da docstring mencionar MAP. |
| Efeitos | fit LightGBM e prints; MLflow se True. |
| Dependências e momento de uso | numpy/lightgbm/mlflow importados no topo. |
| Como interpretar este arquivo | Os grupos são tamanhos de blocos consecutivos cujas somas devem cobrir as linhas; a ordenação interessa dentro de cada grupo e o score não é probabilidade. A docstring menciona MAP, mas o cálculo e o retorno de avaliação usam NDCG. Entrada: X/y alinhados; vetor inteiro de grupos positivos somando linhas; relevância não negativa; ks positivos. Saída: (Booster, métricas ndcg_at_k); evaluate_ranking devolve só NDCG, apesar da docstring mencionar MAP. Efeitos da chamada: fit LightGBM e prints; MLflow se True. Dependências: numpy/lightgbm/mlflow importados no topo. |

<a id="mt09-code-map-file-020"></a>
#### 20. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/lgbm_temporal/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/__init__.py` · SHA-256 `69105e70a8e8267751f4a5193abdd040c1386dda1799e5550e7006c90d4b3000` |
| Papel e motivo técnico | Gerar lag/rolling por entidade em ordem cronológica real; não treina LightGBM. |
| Nomes disponibilizados | SEED, create_temporal_features |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; create_temporal_features(df,target_col,date_col,lags=None,rolling_windows=None,calendar_features=True,entity_cols=None,*,date_format=None,on_duplicate_dates="raise") |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | pandas/numpy/re importados no topo. |
| Como interpretar este arquivo | A fachada reexporta SEED, create_temporal_features; importar o pacote carrega as dependências de topo (pandas/numpy/re importados no topo.), mas não chama a operação. Lag e rolling dependem da ordem cronológica dentro de cada entidade e não treinam LightGBM. O bloco histórico sem entidade não satisfaz o default atual quando há datas duplicadas; nulos anteriores fora das features também importam. |

<a id="mt09-code-map-file-021"></a>
#### 21. `exemplo_lgbm_temporal.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py` · SHA-256 `8912cf78c1c76be1210d5b5490c0488ebce083cf4f588a8c0089e10c0de84423` |
| Reconciliação dos comentários atuais | Deltas MAGIC tornam explícito o contraexemplo sem entity_cols: ValueError pelo default de duplicatas; 33 linhas antigas não são saída atual. lag_n conta observações, e colisões de features são verificadas. |
| Papel e motivo técnico | Gerar lag/rolling por entidade em ordem cronológica real; não treina LightGBM. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; create_temporal_features(df,target_col,date_col,lags=None,rolling_windows=None,calendar_features=True,entity_cols=None,*,date_format=None,on_duplicate_dates="raise") |
| Entradas | fixture sintética local; pandas com target/data e entidade opcional; texto auto só ano-mês-dia; data ambígua exige formato; duplicatas no grão recusadas por default. |
| Saídas | Notebook painel 3 entidades; bloco com entidade é coerente; contraexemplo sem entity_cols deve levantar ValueError por datas duplicadas; a saída de 33 linhas pertence à implementação anterior. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; print contagem removida; sem escrita/modelo. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | pandas/numpy/re importados no topo. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | Lag e rolling dependem da ordem cronológica dentro de cada entidade e não treinam LightGBM. O bloco histórico sem entidade não satisfaz o default atual quando há datas duplicadas; nulos anteriores fora das features também importam. O exemplo usa esta fixture e sequência: Notebook painel 3 entidades; bloco com entidade é coerente; contraexemplo sem entity_cols deve levantar ValueError por datas duplicadas; a saída de 33 linhas pertence à implementação anterior. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-022"></a>
#### 22. `lgbm_temporal.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/lgbm_temporal/lgbm_temporal.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/lgbm_temporal.py` · SHA-256 `45db43d8c29058f6a6e1d8c35e722613b4f8714fdd46a4914482ab9d88f3f627` |
| Papel e motivo técnico | Gerar lag/rolling por entidade em ordem cronológica real; não treina LightGBM. |
| Nomes disponibilizados | SEED; create_temporal_features(df,target_col,date_col,lags=None,rolling_windows=None,calendar_features=True,entity_cols=None,*,date_format=None,on_duplicate_dates="raise") |
| Entradas | pandas com target/data e entidade opcional; texto auto só ano-mês-dia; data ambígua exige formato; duplicatas no grão recusadas por default. |
| Saídas | DataFrame cópia ordenado, data original preservada, lag/rolling deslocados, calendário/trend; `dropna(subset=generated_required)` remove qualquer linha com nulo em feature gerada, inclusive por target ausente no meio, e preserva nulos em colunas alheias. |
| Efeitos | print contagem removida; sem escrita/modelo. |
| Dependências e momento de uso | pandas/numpy/re importados no topo. |
| Como interpretar este arquivo | Lag e rolling dependem da ordem cronológica dentro de cada entidade e não treinam LightGBM. O bloco histórico sem entidade não satisfaz o default atual quando há datas duplicadas. O `dropna(subset=generated_required)` não remove só warm-up: qualquer nulo nas features lag/rolling geradas elimina a linha, inclusive se o target ausente estava no meio; nulos em colunas que não pertencem ao subconjunto são preservados. Entrada: pandas com target/data e entidade opcional; datas ambíguas exigem formato. Saída: DataFrame cópia com features e linhas filtradas; o helper imprime contagem removida, sem escrita ou treino. |

<a id="mt09-code-map-file-023"></a>
#### 23. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/mlp_embeddings/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/__init__.py` · SHA-256 `7cc020279dba75c7d01cf8abef491c89c9234b5208a13629d7dcd89ad2421faf` |
| Papel e motivo técnico | Classificação binária com categorias indexadas e baseline comparável; classe possui branch regressão mas treinador não. |
| Nomes disponibilizados | SEED, EmbeddingMLP, train_embedding_mlp |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; EmbeddingMLP; train_embedding_mlp(X_num_train,X_cat_train,y_train,X_num_val,X_cat_val,y_val,cat_dims,epochs=50,batch_size=512,lr=.001,patience=10,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | torch/numpy/sklearn no topo; mlflow import protegido. |
| Como interpretar este arquivo | A fachada reexporta SEED, EmbeddingMLP, train_embedding_mlp; importar o pacote carrega as dependências de topo (torch/numpy/sklearn no topo; mlflow import protegido.), mas não chama a operação. A categoria precisa de índice dentro do vocabulário informado; valor novo fora dele é recusado. O treinador cobre classificação binária, embora a classe de rede tenha ramo de regressão; AUC de validação com classe única pode ficar indefinida ou NaN. |

<a id="mt09-code-map-file-024"></a>
#### 24. `exemplo_mlp_embeddings.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/mlp_embeddings/exemplo_mlp_embeddings.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/exemplo_mlp_embeddings.py` · SHA-256 `1361c0a58ba512f8b58e4892cb0710cc94fa8426806d607645b46639ce1d18ea` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Classificação binária com categorias indexadas e baseline comparável; classe possui branch regressão mas treinador não. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; EmbeddingMLP; train_embedding_mlp(X_num_train,X_cat_train,y_train,X_num_val,X_cat_val,y_val,cat_dims,epochs=50,batch_size=512,lr=.001,patience=10,log_mlflow=True) |
| Entradas | fixture sintética local; arrays numéricos 2D finitos; listas categóricas alinhadas dentro de [0,cardinalidade); treino duas classes. |
| Saídas | Notebook instala torch, sintetiza 2 numéricas e 2 categorias, log_mlflow=False; AUC histórico de uma partição. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; treina em CPU/CUDA, define seeds, early stopping, print se parar; MLflow se True. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | torch/numpy/sklearn no topo; mlflow import protegido. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | A categoria precisa de índice dentro do vocabulário informado; valor novo fora dele é recusado. O treinador cobre classificação binária, embora a classe de rede tenha ramo de regressão; AUC de validação com classe única pode ficar indefinida ou NaN. O exemplo usa esta fixture e sequência: Notebook instala torch, sintetiza 2 numéricas e 2 categorias, log_mlflow=False; AUC histórico de uma partição. A chamada usa log_mlflow=False: desliga o registro explícito do helper, mas não controla autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-025"></a>
#### 25. `mlp_embeddings.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/mlp_embeddings/mlp_embeddings.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/mlp_embeddings.py` · SHA-256 `de12962cbe1b1e4d3848aaad367d8a30c94fbd0406ecd650a969b01475194708` |
| Papel e motivo técnico | Classificação binária com categorias indexadas e baseline comparável; classe possui branch regressão mas treinador não. |
| Nomes disponibilizados | SEED; EmbeddingMLP; train_embedding_mlp(X_num_train,X_cat_train,y_train,X_num_val,X_cat_val,y_val,cat_dims,epochs=50,batch_size=512,lr=.001,patience=10,log_mlflow=True) |
| Entradas | arrays numéricos 2D finitos; listas categóricas alinhadas dentro de [0,cardinalidade); treino duas classes. |
| Saídas | (modelo Torch, {auc_val,gini_val,epochs_trained}); forward produz tensor [batch,1]. |
| Efeitos | treina em CPU/CUDA, define seeds, early stopping, print se parar; MLflow se True. |
| Dependências e momento de uso | torch/numpy/sklearn no topo; mlflow import protegido. |
| Como interpretar este arquivo | A categoria precisa de índice dentro do vocabulário informado; valor novo fora dele é recusado. O treinador cobre classificação binária, embora a classe de rede tenha ramo de regressão; AUC de validação com classe única pode ficar indefinida ou NaN. Entrada: arrays numéricos 2D finitos; listas categóricas alinhadas dentro de [0,cardinalidade); treino duas classes. Saída: (modelo Torch, {auc_val,gini_val,epochs_trained}); forward produz tensor [batch,1]. Efeitos da chamada: treina em CPU/CUDA, define seeds, early stopping, print se parar; MLflow se True. Dependências: torch/numpy/sklearn no topo; mlflow import protegido. |

<a id="mt09-code-map-file-026"></a>
#### 26. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/optuna_lgbm/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/__init__.py` · SHA-256 `9164e00bc97d2ae7b80d14ee646eea96437838ea50db1e8d8bf16e28f80843d3` |
| Papel e motivo técnico | Tuning escolhe parâmetros de um estudo, não produz modelo final; validação reutilizada otimiza ruído. |
| Nomes disponibilizados | SEED, optimize_lgbm |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; optimize_lgbm(X_train,y_train,X_val,y_val,task="binary",n_trials=50,metric="auc",timeout=None) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | optuna/lightgbm/numpy/sklearn no topo. |
| Como interpretar este arquivo | A fachada reexporta SEED, optimize_lgbm; importar o pacote carrega as dependências de topo (optuna/lightgbm/numpy/sklearn no topo.), mas não chama a operação. O estudo escolhe hiperparâmetros, não entrega modelo final. Reusar validação em trials pode otimizar ruído; `metric` altera a métrica interna do LightGBM somente em `task="binary"`; multiclass fixa `multi_logloss` e regressão fixa `rmse`, ignorando esse argumento. O objetivo do Optuna continua AUC, `-log_loss` ou `-RMSE` conforme a tarefa. AUC binária com validação de classe única é indefinida. |

<a id="mt09-code-map-file-027"></a>
#### 27. `exemplo_optuna_lgbm.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/optuna_lgbm/exemplo_optuna_lgbm.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/exemplo_optuna_lgbm.py` · SHA-256 `df699526eb28c9999290822939f1b4984e6fce1604fb705caa1f797e17ec3d99` |
| Papel e motivo técnico | Tuning escolhe parâmetros de um estudo, não produz modelo final; validação reutilizada otimiza ruído. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; optimize_lgbm(X_train,y_train,X_val,y_val,task="binary",n_trials=50,metric="auc",timeout=None) |
| Entradas | fixture sintética local; arrays treino/val; classes de val representadas em treino; n_trials positivo. |
| Saídas | Notebook instala LightGBM/Optuna, 15 trials sintéticos, imprime parâmetros e best_value históricos; sem escrita explícita. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; cria estudo Optuna e treina um LGBM por trial; altera verbosidade Optuna global; sem MLflow/arquivo explícito. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | optuna/lightgbm/numpy/sklearn no topo. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | O estudo escolhe hiperparâmetros, não entrega modelo final. Reusar validação em trials pode otimizar ruído; `metric` altera a métrica interna do LightGBM somente em `task="binary"`; multiclass fixa `multi_logloss` e regressão fixa `rmse`, ignorando esse argumento. O objetivo do Optuna continua AUC, `-log_loss` ou `-RMSE` conforme a tarefa. AUC binária com validação de classe única é indefinida. O exemplo usa esta fixture e sequência: Notebook instala LightGBM/Optuna, 15 trials sintéticos, imprime parâmetros e best_value históricos; sem escrita explícita. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-028"></a>
#### 28. `optuna_lgbm.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/optuna_lgbm/optuna_lgbm.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/optuna_lgbm.py` · SHA-256 `c773d2c0aea663863f0ae403a05259d97574328cea9faa062a69ecdd7325e629` |
| Papel e motivo técnico | Tuning escolhe parâmetros de um estudo, não produz modelo final; validação reutilizada otimiza ruído. |
| Nomes disponibilizados | SEED; optimize_lgbm(X_train,y_train,X_val,y_val,task="binary",n_trials=50,metric="auc",timeout=None) |
| Entradas | arrays treino/val; classes de val representadas em treino; n_trials positivo. |
| Saídas | (study.best_params, study); objetivo binário AUC, multiclasse -log_loss, regressão -RMSE. |
| Efeitos | cria estudo Optuna e treina um LGBM por trial; altera verbosidade Optuna global; sem MLflow/arquivo explícito. |
| Dependências e momento de uso | optuna/lightgbm/numpy/sklearn no topo. |
| Como interpretar este arquivo | O estudo escolhe hiperparâmetros, não entrega modelo final. Reusar validação em trials pode otimizar ruído; `metric` altera a métrica interna do LightGBM somente em `task="binary"`; multiclass fixa `multi_logloss` e regressão fixa `rmse`, ignorando esse argumento. O objetivo do Optuna continua AUC, `-log_loss` ou `-RMSE` conforme a tarefa. AUC binária com validação de classe única é indefinida. Entrada: arrays treino/val; classes de val representadas em treino; n_trials positivo. Saída: (study.best_params, study); objetivo binário AUC, multiclasse -log_loss, regressão -RMSE. Efeitos da chamada: cria estudo Optuna e treina um LGBM por trial; altera verbosidade Optuna global; sem MLflow/arquivo explícito. Dependências: optuna/lightgbm/numpy/sklearn no topo. |

<a id="mt09-code-map-file-029"></a>
#### 29. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/prophet_wrapper/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/__init__.py` · SHA-256 `8b66b00568ea81cdb1e8c759ea9d445deed61287d4ae6658c935a6fc3d6be0d9` |
| Papel e motivo técnico | Forecast por frequência declarada e métricas in-sample; feriado diário pode não afetar linha mensal. |
| Nomes disponibilizados | SEED, train_prophet |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; train_prophet(df,ds_col="ds",y_col="y",periods=12,freq="MS",yearly=True,weekly=False,country_holidays="BR",changepoint_prior=.05,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | pandas/numpy/mlflow no topo, prophet importado dentro da função. |
| Como interpretar este arquivo | A fachada reexporta SEED, train_prophet; importar o pacote carrega as dependências de topo (pandas/numpy/mlflow no topo, prophet importado dentro da função.), mas não chama a operação. A frequência declarada determina os passos da previsão, e as métricas devolvidas são de ajuste. Um feriado diário pode não coincidir com observações mensais; MAPE divide pelo valor real sem máscara para zero e intervalos do exemplo variam sem semente fixa. |

<a id="mt09-code-map-file-030"></a>
#### 30. `exemplo_prophet_wrapper.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/prophet_wrapper/exemplo_prophet_wrapper.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/exemplo_prophet_wrapper.py` · SHA-256 `ca784e2072a89a501c37bfc6089b0531260742f191962c969120d5c1c9bc4014` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Forecast por frequência declarada e métricas in-sample; feriado diário pode não afetar linha mensal. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; train_prophet(df,ds_col="ds",y_col="y",periods=12,freq="MS",yearly=True,weekly=False,country_holidays="BR",changepoint_prior=.05,log_mlflow=True) |
| Entradas | fixture sintética local; DataFrame com data/valor; datas convertidas por pandas; periods/freq e configuração sazonal. |
| Saídas | Notebook instala Prophet, série mensal sintética 36 meses +6; intervalos de incerteza variam porque não fixa semente; log_mlflow=False. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; ajusta e prevê; MLflow se True; sem arquivo explícito. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | pandas/numpy/mlflow no topo, prophet importado dentro da função. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | A frequência declarada determina os passos da previsão, e as métricas devolvidas são de ajuste. Um feriado diário pode não coincidir com observações mensais; MAPE divide pelo valor real sem máscara para zero e intervalos do exemplo variam sem semente fixa. O exemplo usa esta fixture e sequência: Notebook instala Prophet, série mensal sintética 36 meses +6; intervalos de incerteza variam porque não fixa semente; log_mlflow=False. A chamada usa log_mlflow=False: desliga o registro explícito do helper, mas não controla autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-031"></a>
#### 31. `prophet_wrapper.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/prophet_wrapper/prophet_wrapper.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/prophet_wrapper.py` · SHA-256 `9b46169cf489095a59f052e932515d84d893189b84a6ae01e67235e1c9518a77` |
| Papel e motivo técnico | Forecast por frequência declarada e métricas in-sample; feriado diário pode não afetar linha mensal. |
| Nomes disponibilizados | SEED; train_prophet(df,ds_col="ds",y_col="y",periods=12,freq="MS",yearly=True,weekly=False,country_holidays="BR",changepoint_prior=.05,log_mlflow=True) |
| Entradas | DataFrame com data/valor; datas convertidas por pandas; periods/freq e configuração sazonal. |
| Saídas | (modelo Prophet, forecast DataFrame com histórico+futuro, métricas MAPE/RMSE/MAE in-sample). |
| Efeitos | ajusta e prevê; MLflow se True; sem arquivo explícito. |
| Dependências e momento de uso | pandas/numpy/mlflow no topo, prophet importado dentro da função. |
| Como interpretar este arquivo | A frequência declarada determina os passos da previsão, e as métricas devolvidas são de ajuste. Um feriado diário pode não coincidir com observações mensais; MAPE divide pelo valor real sem máscara para zero e intervalos do exemplo variam sem semente fixa. Entrada: DataFrame com data/valor; datas convertidas por pandas; periods/freq e configuração sazonal. Saída: (modelo Prophet, forecast DataFrame com histórico+futuro, métricas MAPE/RMSE/MAE in-sample). Efeitos da chamada: ajusta e prevê; MLflow se True; sem arquivo explícito. Dependências: pandas/numpy/mlflow no topo, prophet importado dentro da função. |

<a id="mt09-code-map-file-032"></a>
#### 32. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/tabnet_wrapper/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/__init__.py` · SHA-256 `b03213d3a8c6b01c5ffd618781bcf77d576e5529c9e0272bf9bc8c982abb06ba` |
| Papel e motivo técnico | Modelo supervisionado; importância global interna não é SHAP/local/causal. |
| Nomes disponibilizados | SEED, train_tabnet |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; train_tabnet(X_train,y_train,X_val,y_val,task="binary",cat_idxs=None,cat_dims=None,n_d=32,n_a=32,n_steps=5,max_epochs=100,patience=15,batch_size=1024,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | numpy topo; torch/pytorch_tabnet/sklearn importados na função; mlflow import protegido. |
| Como interpretar este arquivo | A fachada reexporta SEED, train_tabnet; importar o pacote carrega as dependências de topo (numpy topo; torch/pytorch_tabnet/sklearn importados na função; mlflow import protegido.), mas não chama a operação. A importância devolvida é global e interna ao modelo, não explicação SHAP local nem efeito causal. AUC de validação com uma classe pode ficar indefinida; dependências do TabNet são carregadas durante a chamada. |

<a id="mt09-code-map-file-033"></a>
#### 33. `exemplo_tabnet_wrapper.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/tabnet_wrapper/exemplo_tabnet_wrapper.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/exemplo_tabnet_wrapper.py` · SHA-256 `04356473a4a6561cab36c7ce4bbb25e3ee2505bf41b10748e14eab6bb80657e1` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Modelo supervisionado; importância global interna não é SHAP/local/causal. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; train_tabnet(X_train,y_train,X_val,y_val,task="binary",cat_idxs=None,cat_dims=None,n_d=32,n_a=32,n_steps=5,max_epochs=100,patience=15,batch_size=1024,log_mlflow=True) |
| Entradas | fixture sintética local; X 2D e y alinhados; categorias por índice/cardinalidade; binário treino 0/1 com duas classes. |
| Saídas | Notebook instala pytorch-tabnet, base sintética de interação, log_mlflow=False, ordena importâncias históricas; sem SHAP. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; treino torch/TabNet, seeds, MLflow se True; sem plot/arquivo. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | numpy topo; torch/pytorch_tabnet/sklearn importados na função; mlflow import protegido. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | A importância devolvida é global e interna ao modelo, não explicação SHAP local nem efeito causal. AUC de validação com uma classe pode ficar indefinida; dependências do TabNet são carregadas durante a chamada. O exemplo usa esta fixture e sequência: Notebook instala pytorch-tabnet, base sintética de interação, log_mlflow=False, ordena importâncias históricas; sem SHAP. A chamada usa log_mlflow=False: desliga o registro explícito do helper, mas não controla autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-034"></a>
#### 34. `tabnet_wrapper.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/tabnet_wrapper/tabnet_wrapper.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/tabnet_wrapper.py` · SHA-256 `90a8344eddc6c679685c58f5d0299b9af27fa1aad54bd2f5c902af32ae286624` |
| Papel e motivo técnico | Modelo supervisionado; importância global interna não é SHAP/local/causal. |
| Nomes disponibilizados | SEED; train_tabnet(X_train,y_train,X_val,y_val,task="binary",cat_idxs=None,cat_dims=None,n_d=32,n_a=32,n_steps=5,max_epochs=100,patience=15,batch_size=1024,log_mlflow=True) |
| Entradas | X 2D e y alinhados; categorias por índice/cardinalidade; binário treino 0/1 com duas classes. |
| Saídas | (modelo TabNet, métricas auc_val/gini_val ou rmse_val, feature_importances_ ndarray). |
| Efeitos | treino torch/TabNet, seeds, MLflow se True; sem plot/arquivo. |
| Dependências e momento de uso | numpy topo; torch/pytorch_tabnet/sklearn importados na função; mlflow import protegido. |
| Como interpretar este arquivo | A importância devolvida é global e interna ao modelo, não explicação SHAP local nem efeito causal. AUC de validação com uma classe pode ficar indefinida; dependências do TabNet são carregadas durante a chamada. Entrada: X 2D e y alinhados; categorias por índice/cardinalidade; binário treino 0/1 com duas classes. Saída: (modelo TabNet, métricas auc_val/gini_val ou rmse_val, feature_importances_ ndarray). Efeitos da chamada: treino torch/TabNet, seeds, MLflow se True; sem plot/arquivo. Dependências: numpy topo; torch/pytorch_tabnet/sklearn importados na função; mlflow import protegido. |

<a id="mt09-code-map-file-035"></a>
#### 35. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_catboost/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/__init__.py` · SHA-256 `6204991a4c352547336cde5b0246c33089b4cd806f8f492b354dfd8e507396a5` |
| Papel e motivo técnico | Baseline para categóricas com tipos preservados e validação separada. |
| Nomes disponibilizados | SEED, train_catboost_baseline |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; train_catboost_baseline(X_train,y_train,X_val,y_val,task="binary",cat_features=None,params_override=None,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | catboost/numpy/sklearn topo; mlflow import protegido. |
| Como interpretar este arquivo | A fachada reexporta SEED, train_catboost_baseline; importar o pacote carrega as dependências de topo (catboost/numpy/sklearn topo; mlflow import protegido.), mas não chama a operação. Tipos categóricos devem ser preservados entre treino e validação. allow_writing_files=False reduz escrita por padrão, mas override de parâmetro pode reativá-la; AUC de validação de classe única pode ser indefinida. |

<a id="mt09-code-map-file-036"></a>
#### 36. `exemplo_train_catboost.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_catboost/exemplo_train_catboost.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/exemplo_train_catboost.py` · SHA-256 `efa1945508d856111c7b155303d392d42364edb22605ef9b251f2576be98f7b3` |
| Reconciliação dos comentários atuais | Deltas MAGIC recusam garantia de ausência de leakage por codificação ordenada, condicionam tracking e substituem narrativa do incidente por contrato allow_writing_files=False com override consciente. |
| Papel e motivo técnico | Baseline para categóricas com tipos preservados e validação separada. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; train_catboost_baseline(X_train,y_train,X_val,y_val,task="binary",cat_features=None,params_override=None,log_mlflow=True) |
| Entradas | fixture sintética local; arrays treino/val, task binária/multiclasse/regressão, índices categóricos. |
| Saídas | Notebook instala catboost, ndarray object preserva categoria inteira, log_mlflow=False; saída histórica; explica o default que evita arquivos catboost_info e o efeito do override. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; fit; allow_writing_files=False por default evita catboost_info; override pode reativar escrita; MLflow se True. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | catboost/numpy/sklearn topo; mlflow import protegido. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | Tipos categóricos devem ser preservados entre treino e validação. allow_writing_files=False reduz escrita por padrão, mas override de parâmetro pode reativá-la; AUC de validação de classe única pode ser indefinida. O exemplo usa esta fixture e sequência: Notebook instala catboost, ndarray object preserva categoria inteira, log_mlflow=False; saída histórica; explica o default que evita arquivos catboost_info e o efeito do override. A chamada usa log_mlflow=False: desliga o registro explícito do helper, mas não controla autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-037"></a>
#### 37. `train_catboost.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_catboost/train_catboost.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/train_catboost.py` · SHA-256 `e11f97f03c44b7393f6759bfaed3d0144727b732e90612dc3e988df8a2359ebf` |
| Papel e motivo técnico | Baseline para categóricas com tipos preservados e validação separada. |
| Nomes disponibilizados | SEED; train_catboost_baseline(X_train,y_train,X_val,y_val,task="binary",cat_features=None,params_override=None,log_mlflow=True) |
| Entradas | arrays treino/val, task binária/multiclasse/regressão, índices categóricos. |
| Saídas | (modelo CatBoost, métricas AUC/Gini, log_loss/accuracy ou RMSE). |
| Efeitos | fit; allow_writing_files=False por default evita catboost_info; override pode reativar escrita; MLflow se True. |
| Dependências e momento de uso | catboost/numpy/sklearn topo; mlflow import protegido. |
| Como interpretar este arquivo | Tipos categóricos devem ser preservados entre treino e validação. allow_writing_files=False reduz escrita por padrão, mas override de parâmetro pode reativá-la; AUC de validação de classe única pode ser indefinida. Entrada: arrays treino/val, task binária/multiclasse/regressão, índices categóricos. Saída: (modelo CatBoost, métricas AUC/Gini, log_loss/accuracy ou RMSE). Efeitos da chamada: fit; allow_writing_files=False por default evita catboost_info; override pode reativar escrita; MLflow se True. Dependências: catboost/numpy/sklearn topo; mlflow import protegido. |

<a id="mt09-code-map-file-038"></a>
#### 38. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_lgbm/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/__init__.py` · SHA-256 `3aa32e321053c9ae9a27fae1dd6b6d8c25fe3eab758aaa197f3de138f0b424b1` |
| Papel e motivo técnico | Baseline tabular, sobreajuste e validação, com defaults por tarefa. |
| Nomes disponibilizados | SEED, DEFAULT_PARAMS_BINARY, DEFAULT_PARAMS_REGRESSION, DEFAULT_PARAMS_MULTICLASS, train_lightgbm_baseline |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; DEFAULT_PARAMS_BINARY/REGRESSION/MULTICLASS; train_lightgbm_baseline(X_train,y_train,X_val,y_val,task="binary",params_override=None,early_stopping_rounds=50,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | lightgbm/numpy/sklearn topo; mlflow import protegido. |
| Como interpretar este arquivo | A fachada reexporta SEED, DEFAULT_PARAMS_BINARY, DEFAULT_PARAMS_REGRESSION, DEFAULT_PARAMS_MULTICLASS, train_lightgbm_baseline; importar o pacote carrega as dependências de topo (lightgbm/numpy/sklearn topo; mlflow import protegido.), mas não chama a operação. O baseline depende da tarefa e da partição de validação. subsample=0.8 sem subsample_freq não ativa bagging de linhas; AUC de validação com uma classe pode ficar indefinida ou NaN. |

<a id="mt09-code-map-file-039"></a>
#### 39. `exemplo_train_lgbm.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_lgbm/exemplo_train_lgbm.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/exemplo_train_lgbm.py` · SHA-256 `02fc5e8f181a40928c6a6d3989c75cce6758dd2f021d837a8b2579e5aa74d6d2` |
| Reconciliação dos comentários atuais | Deltas MAGIC condicionam tracking e distinguem extrato histórico da configuração completa DEFAULT_PARAMS_BINARY/model.get_params; subsample sozinho não ativa bagging. |
| Papel e motivo técnico | Baseline tabular, sobreajuste e validação, com defaults por tarefa. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; DEFAULT_PARAMS_BINARY/REGRESSION/MULTICLASS; train_lightgbm_baseline(X_train,y_train,X_val,y_val,task="binary",params_override=None,early_stopping_rounds=50,log_mlflow=True) |
| Entradas | fixture sintética local; X/y treino e val não vazios; classificação treino >=2 classes e labels de val contidos no treino. |
| Saídas | Notebook instala LightGBM, base sintética binária, log_mlflow=False; imprime default completo no código, bloco histórico é extrato. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; fit/early stop; MLflow se True; sem arquivo. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | lightgbm/numpy/sklearn topo; mlflow import protegido. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | O baseline depende da tarefa e da partição de validação. subsample=0.8 sem subsample_freq não ativa bagging de linhas; AUC de validação com uma classe pode ficar indefinida ou NaN. O exemplo usa esta fixture e sequência: Notebook instala LightGBM, base sintética binária, log_mlflow=False; imprime default completo no código, bloco histórico é extrato. A chamada usa log_mlflow=False: desliga o registro explícito do helper, mas não controla autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-040"></a>
#### 40. `train_lgbm.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_lgbm/train_lgbm.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/train_lgbm.py` · SHA-256 `3f1b80ce1dc4bf39351fe3156c71aa72dacff9293a57c3c103b4b6e125a9bc77` |
| Papel e motivo técnico | Baseline tabular, sobreajuste e validação, com defaults por tarefa. |
| Nomes disponibilizados | SEED; DEFAULT_PARAMS_BINARY/REGRESSION/MULTICLASS; train_lightgbm_baseline(X_train,y_train,X_val,y_val,task="binary",params_override=None,early_stopping_rounds=50,log_mlflow=True) |
| Entradas | X/y treino e val não vazios; classificação treino >=2 classes e labels de val contidos no treino. |
| Saídas | (modelo LightGBM sklearn, métricas binárias AUC treino/val,Gini,gap; regressão RMSE; multi logloss/accuracy). |
| Efeitos | fit/early stop; MLflow se True; sem arquivo. |
| Dependências e momento de uso | lightgbm/numpy/sklearn topo; mlflow import protegido. |
| Como interpretar este arquivo | O baseline depende da tarefa e da partição de validação. subsample=0.8 sem subsample_freq não ativa bagging de linhas; AUC de validação com uma classe pode ficar indefinida ou NaN. Entrada: X/y treino e val não vazios; classificação treino >=2 classes e labels de val contidos no treino. Saída: (modelo LightGBM sklearn, métricas binárias AUC treino/val,Gini,gap; regressão RMSE; multi logloss/accuracy). Efeitos da chamada: fit/early stop; MLflow se True; sem arquivo. Dependências: lightgbm/numpy/sklearn topo; mlflow import protegido. |

<a id="mt09-code-map-file-041"></a>
#### 41. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_xgboost/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/__init__.py` · SHA-256 `f819ac6b004d1b5bbe21736693a406640f57f1721df9cfe957c228bd0b11b0b4` |
| Papel e motivo técnico | Comparar baseline na mesma partição, sem inferir vencedor geral de milésimos. |
| Nomes disponibilizados | SEED, DEFAULT_PARAMS, train_xgboost_baseline |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; DEFAULT_PARAMS; train_xgboost_baseline(X_train,y_train,X_val,y_val,task="binary",params_override=None,early_stopping_rounds=50,log_mlflow=True) |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | xgboost/numpy/sklearn topo; mlflow import protegido. |
| Como interpretar este arquivo | A fachada reexporta SEED, DEFAULT_PARAMS, train_xgboost_baseline; importar o pacote carrega as dependências de topo (xgboost/numpy/sklearn topo; mlflow import protegido.), mas não chama a operação. Compare com outro baseline somente na mesma partição e escala de métrica. log_mlflow=False desliga o logging explícito desta função; autologging externo depende do ambiente. Diferença pequena impressa no notebook é observação histórica, não vitória geral. |

<a id="mt09-code-map-file-042"></a>
#### 42. `exemplo_train_xgboost.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py` · SHA-256 `336e5a53e5bfef6eff172475230a9cd3217f05da2af61f372b8e6da6e144ec57` |
| Reconciliação dos comentários atuais | Delta MAGIC pede registrar versões e comparar contrato, sem esperar métricas idênticas; resultado continua referência histórica. |
| Papel e motivo técnico | Comparar baseline na mesma partição, sem inferir vencedor geral de milésimos. |
| Nomes disponibilizados | notebook Databricks; demonstra chamadas de SEED; DEFAULT_PARAMS; train_xgboost_baseline(X_train,y_train,X_val,y_val,task="binary",params_override=None,early_stopping_rounds=50,log_mlflow=True) |
| Entradas | fixture sintética local; X/y treino/val; binária exige duas classes em ambos; multi valida classes no treino. |
| Saídas | Notebook instala xgboost, mesma fixture de train_lgbm, log_mlflow=False; saídas históricas; texto adverte autologging externo. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; distinguir show/notebook de helper; fit/early stopping; MLflow se True, autologging externo fora do controle. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | xgboost/numpy/sklearn topo; mlflow import protegido. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | Compare com outro baseline somente na mesma partição e escala de métrica. log_mlflow=False desliga o logging explícito desta função; autologging externo depende do ambiente. Diferença pequena impressa no notebook é observação histórica, não vitória geral. O exemplo usa esta fixture e sequência: Notebook instala xgboost, mesma fixture de train_lgbm, log_mlflow=False; saídas históricas; texto adverte autologging externo. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |

<a id="mt09-code-map-file-043"></a>
#### 43. `train_xgboost.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/train_xgboost/train_xgboost.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/train_xgboost.py` · SHA-256 `601f5e275c55326a2413769288681c1fefbf36e27f694b6ab5e5112cbcd79373` |
| Papel e motivo técnico | Comparar baseline na mesma partição, sem inferir vencedor geral de milésimos. |
| Nomes disponibilizados | SEED; DEFAULT_PARAMS; train_xgboost_baseline(X_train,y_train,X_val,y_val,task="binary",params_override=None,early_stopping_rounds=50,log_mlflow=True) |
| Entradas | X/y treino/val; binária exige duas classes em ambos; multi valida classes no treino. |
| Saídas | (modelo XGB sklearn, métricas AUC/Gini, log_loss/accuracy ou RMSE). |
| Efeitos | fit/early stopping; MLflow se True, autologging externo fora do controle. |
| Dependências e momento de uso | xgboost/numpy/sklearn topo; mlflow import protegido. |
| Como interpretar este arquivo | Compare com outro baseline somente na mesma partição e escala de métrica. log_mlflow=False desliga o logging explícito desta função; autologging externo depende do ambiente. Diferença pequena impressa no notebook é observação histórica, não vitória geral. Entrada: X/y treino/val; binária exige duas classes em ambos; multi valida classes no treino. Saída: (modelo XGB sklearn, métricas AUC/Gini, log_loss/accuracy ou RMSE). Efeitos da chamada: fit/early stopping; MLflow se True, autologging externo fora do controle. Dependências: xgboost/numpy/sklearn topo; mlflow import protegido. |

<a id="mt09-code-map-file-044"></a>
#### 44. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/umap_viz/__init__.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/__init__.py` · SHA-256 `2348a18323c0b1cfbe068f4d4e381c6620ffdafbccda4291067ddf9135242e54` |
| Papel e motivo técnico | Projeção exploratória não prova separação, eixo não tem unidade; tema V07 não muda embedding. |
| Nomes disponibilizados | SEED, PALETA_CATEGORICA, AZUL_CAIXA, TEMA_BASE, compute_umap, plot_umap_clusters, plot_umap_clusters_resolvido |
| Entradas | import do namespace da família; assinaturas da implementação: SEED; PALETA_CATEGORICA; AZUL_CAIXA; TEMA_BASE; compute_umap; plot_umap_clusters; plot_umap_clusters_resolvido |
| Saídas | objetos públicos reexportados, sem cálculo próprio |
| Efeitos | importa a implementação e suas dependências top-level; não chama treino nem grava artefatos |
| Dependências e momento de uso | NumPy/Plotly e tokens de tema no topo; `umap-learn` importado ao projetar; pandas importado dentro de `plot_umap_clusters` (também chamado pela variante resolvida). `compute_umap` isolado não usa pandas. |
| Como interpretar este arquivo | A fachada reexporta SEED, PALETA_CATEGORICA, AZUL_CAIXA, TEMA_BASE, compute_umap, plot_umap_clusters, plot_umap_clusters_resolvido; importar o pacote carrega as dependências de topo (numpy/plotly/hub colors+tema topo; umap-learn importado na chamada.), mas não chama a operação. A projeção UMAP é exploratória: eixos não têm unidade original e separação visual não valida clusters. A função de plot refaz a projeção; a rota legada e a variante V07 com ResolvedTheme diferem em entrada visual, não no significado do embedding. O plot importa pandas internamente; `compute_umap` isolado não depende desse import. |

<a id="mt09-code-map-file-045"></a>
#### 45. `exemplo_umap_viz.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/umap_viz/exemplo_umap_viz.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/exemplo_umap_viz.py` · SHA-256 `976e4b14b868c9ff83aab8dd87c8e49618f9760ddd3ba77a015192ce405f66f5` |
| Papel e motivo técnico | Demonstrar projeção exploratória e plot legado: a separação visual não valida clusters e eixos UMAP não têm unidade original. A variante V07 com tema é API relacionada, não demonstrada. |
| Nomes disponibilizados | notebook Databricks; importa e chama compute_umap e plot_umap_clusters; não importa nem chama plot_umap_clusters_resolvido. |
| Entradas | fixture sintética local; X numérico escalado e labels alinhados para compute_umap e plot_umap_clusters; nenhum ResolvedTheme é fornecido. |
| Saídas | Notebook instala umap-learn==0.5.5, escala 3 grupos sintéticos, chama projeção e plot legado; figura.show apenas no notebook; não cobre rota resolvida. |
| Efeitos | células %pip/%restart_python quando presentes, sys.path e prints; compute_umap ajusta projeção e plot_umap_clusters refaz UMAP e cria figura Plotly; figura.show pertence ao notebook, sem save/show no helper. A variante resolvida não é chamada. Antes de ajustar `sys.path`, o notebook consulta `spark.sql("SELECT current_user()").first()` para montar o caminho; essa consulta não lê tabela de negócio nem treina de modo distribuído. |
| Dependências e momento de uso | NumPy/Plotly e tokens de tema no topo; `umap-learn` importado ao projetar; pandas importado dentro de `plot_umap_clusters` (também chamado pela variante resolvida). `compute_umap` isolado não usa pandas. A preparação do import requer sessão Spark para `current_user()` antes de `sys.path`; não é evidência de execução do modelo. |
| Como interpretar este arquivo | A projeção UMAP é exploratória: eixos não têm unidade original e separação visual não valida clusters. O notebook instala umap-learn==0.5.5, escala três grupos sintéticos, chama compute_umap e depois plot_umap_clusters, que refaz a projeção; figura.show ocorre apenas na célula do notebook. plot_umap_clusters_resolvido é uma API V07 existente na implementação, mas não participa deste ensaio histórico. |

<a id="mt09-code-map-file-046"></a>
#### 46. `umap_viz.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/umap_viz/umap_viz.py) · [MT09: explicação do mecanismo](MT-parte-ii.md#mt09-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/umap_viz.py` · SHA-256 `5b24447bc4b13a1f8033a485f9a3fee2a22cca4f528b5401ca02af1b8d907b69` |
| Papel e motivo técnico | Projeção exploratória não prova separação, eixo não tem unidade; tema V07 não muda embedding. |
| Nomes disponibilizados | SEED; PALETA_CATEGORICA; AZUL_CAIXA; TEMA_BASE; compute_umap; plot_umap_clusters; plot_umap_clusters_resolvido |
| Entradas | X numérico escalado, labels alinhados; tema ResolvedTheme obrigatório na rota resolvida. |
| Saídas | compute_umap -> ndarray; plots -> go.Figure; plot legado recomputa embedding. |
| Efeitos | fit UMAP, cria figura Plotly; sem save/show no helper; resolved aplica tokens de tema após plot legado. |
| Dependências e momento de uso | NumPy/Plotly e tokens de tema no topo; `umap-learn` importado ao projetar; pandas importado dentro de `plot_umap_clusters` (também chamado pela variante resolvida). `compute_umap` isolado não usa pandas. |
| Como interpretar este arquivo | A projeção UMAP é exploratória: eixos não têm unidade original e separação visual não valida clusters. A função de plot refaz a projeção; a rota legada e a variante V07 com ResolvedTheme diferem em entrada visual, não no significado do embedding. Entrada: X numérico escalado, labels alinhados; tema ResolvedTheme obrigatório na rota resolvida. Saída: compute_umap -> ndarray; plots -> go.Figure; plot legado recomputa embedding. Efeitos da chamada: fit UMAP, cria figura Plotly; sem save/show no helper; resolved aplica tokens de tema após plot legado. Dependências: numpy/plotly/hub colors+tema topo; umap-learn importado na chamada. O plot importa pandas internamente; `compute_umap` isolado não depende desse import. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
