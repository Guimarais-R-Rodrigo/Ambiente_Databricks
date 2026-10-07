# MT atlas 03

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0101"></a>
<a id="doc-0101"></a>
### D0101 — Quando o contexto MLflow considera uma run completa?

O README de `mlflow_run` descreve `run_governado(nome, dataset, split, limitacoes, experimento, exigir_completo)` como context manager. Antes de abrir a run, valida metadados e, se informado, seleciona experimento. Dentro do `with`, o coletor oferece `parametros`, `metricas`, `modelo`, `artefato` e `pendencias`. O público é o autor de notebook que quer deixar intenção, divisão dos dados e limitações registradas junto da execução.

Um uso local registra configuração de treino, métricas de validação e modelo scikit-learn com exemplo de entrada para assinatura. Ao sair normalmente com `exigir_completo=True`, o helper cobra parâmetros, métricas e exemplo de entrada, sem reverificar a assinatura persistida; `modelo` usa especificamente `mlflow.sklearn.log_model`, portanto não é exportador genérico de LightGBM ou PyTorch. Se ocorrer exceção dentro do `with`, a verificação pós-`yield` é pulada, embora tags e registros anteriores possam já ter chegado ao backend.

A API aditiva `run_micromodelo` registra E0 rule-based sintético com fingerprint, contrato, parâmetros permitidos e agregados reconciliados; exige fechamento completo, sem modelo sklearn ou resultados individuais. `synthetic:` declara origem, não a verifica.

Na manutenção, esclarecer destino, autorização, artefatos e efeito de falha. Fechar com erro não equivale a desfazer uma run. A observação histórica sobre serverless Free é contexto do exemplo, não garantia atual de plataforma.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/mlflow_run/README.md). SHA-256 da fonte histórica da redação: `9c34f1124b91c7d48548dbe92b1be4dac05aed6bd6c16bff629b9fec6fc3a44f`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0100](MT-atlas-02.md#doc-0100) · [Próximo: D0102](#doc-0102) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0102"></a>
<a id="doc-0102"></a>
### D0102 — Quais categorias entram no MLP com embeddings?

O guia `mlp_embeddings` combina classe `EmbeddingMLP` e treinador `train_embedding_mlp`. A classe admite `task='regression'`, mas o treinador disponível ajusta somente classificação binária e devolve modelo, AUC e Gini de validação, além de épocas percorridas. O leitor deve fornecer matriz numérica finita e uma lista de arrays categóricos, um por coluna, com códigos inteiros no intervalo `[0, cardinalidade)`.

Se canal possui três categorias, codificá-las como 0, 1 e 2 e declarar cardinalidade 3 é válido; código 3 ou um texto bruto não é. O treino precisa das duas classes. A validação aceita formalmente rótulos 0/1, porém AUC fica indefinida se ela contiver só uma classe; conforme a versão de scikit-learn, o cálculo pode lançar erro ou devolver NaN com aviso. Confira essa divisão antes da chamada. A parada antecipada guarda o melhor AUC de validação, enquanto `epochs_trained` informa quantas épocas rodaram, não necessariamente a época restaurada.

Na manutenção, preservar encoder, tratamento de categoria desconhecida, escala dos números e versão do modelo, pois o helper não exporta esse pré-processamento nem calibração. PyTorch é exigido; o import de MLflow é protegido e a dependência se torna obrigatória quando o logging está ligado. Na classe direta, lista curta de dimensões de embedding pode causar inconsistência por `zip`.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/mlp_embeddings/README.md). SHA-256 da fonte histórica da redação: `3f3e4e38070501e0c2bb6112da756223ae9600dcc5476447a42ae66d441ed2c9`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0101](#doc-0101) · [Próximo: D0103](#doc-0103) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0103"></a>
<a id="doc-0103"></a>
### D0103 — O que a busca Optuna devolve?

O README de `optuna_lgbm` documenta `optimize_lgbm(X_train, y_train, X_val, y_val, task='binary', n_trials=50, metric='auc', timeout=None)`. Seu retorno é o dicionário de melhores parâmetros sugeridos e um objeto `Study`, não um modelo treinado para produção. O guia atende ao autor que já separou treino e validação e precisa entender qual objetivo foi efetivamente buscado.

Com classificação binária e quinze tentativas, o exemplo usa TPE com semente 42, até 500 árvores e parada antecipada em cinquenta rodadas por trial. O objetivo maximizado é AUC; para regressão é menos RMSE e para multiclasse, menos log-loss. O argumento `metric` só alimenta a métrica interna do ramo binário e não troca essa função objetivo, apesar da formulação ampla da docstring. A mesma validação participa de todas as tentativas; ela não é teste final independente.

Na manutenção, guardar espaço de busca, seed, dados, versão e avaliação posterior. `best_params` contém apenas parâmetros variáveis, faltando constantes do ajuste; sozinho não reproduz o modelo. `subsample` pode ficar inativo com `subsample_freq=0` padrão do LightGBM.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/optuna_lgbm/README.md). SHA-256 da fonte histórica da redação: `80aabd567f17e3c89283404f3594930f5a2310df4d02e7e76f3e1f8d3b9dc598`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0102](#doc-0102) · [Próximo: D0104](#doc-0104) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0104"></a>
<a id="doc-0104"></a>
### D0104 — Que decisão cabe ao monitor de performance?

O README de `performance_monitor` orienta quem acompanha métricas periódicas de um modelo já avaliado. `PerformanceMonitor` recebe baseline, política de warning/critical, direção e tipo de delta; `add_period` guarda entradas em memória, sem ordenar, deduplicar ou detectar lacunas de calendário. A classe devolve status, relatório Markdown e orientação de investigação por `should_retrain()`. As timelines legada e `_resolvido(metric, theme)` retornam figura Plotly sobre o mesmo histórico, mudando apenas a aparência.

Com AUC de referência 0,78, política de queda absoluta de 0,03 para aviso e 0,05 para crítico, uma observação 0,73 alcança o limite crítico. O código compara com o baseline, não com o mês anterior. `selecionar_metricas_do_relatorio` traduz `auc_roc` para `auc` e permite exigir métricas; `ks_pct` permanece em pontos percentuais de 0 a 100. Target ainda imaturo ou escala diferente invalida a comparação.

Na manutenção, calibrar limites pelo modelo e risco, registrar período, população e persistir evidências externamente. A decisão crítica traz `automatic_retrain_authorized=False`; sem períodos, `NO_EVIDENCE` vem sem esse campo. Nenhum retorno agenda ou autoriza treino, e Plotly é exigido já no import, transitivamente por `theme_plotly`.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/performance_monitor/README.md). SHA-256 da fonte histórica da redação: `805266e31d89d092f6901c051912d8c78292a286faf88c8a7f6a5ee9b49a8cc3`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0103](#doc-0103) · [Próximo: D0105](#doc-0105) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0105"></a>
<a id="doc-0105"></a>
### D0105 — Que previsão o wrapper Prophet entrega?

O guia `prophet_wrapper` apresenta `train_prophet(df, ds_col, y_col, periods, freq, yearly, weekly, country_holidays, changepoint_prior, log_mlflow)`. É um candidato univariado para séries datadas: o helper seleciona apenas data e alvo, ajusta Prophet, projeta histórico mais horizonte futuro e devolve modelo, DataFrame de previsão e três métricas de ajuste. O leitor deve definir a frequência antes de interpretar sazonalidade ou calendário.

Em uma série mensal de 36 linhas, `periods=6` e `freq="MS"` produzem previsão que contém também as datas históricas; o resultado não é só seis linhas. `mape_insample`, `rmse_insample` e `mae_insample` comparam `yhat` ao próprio treino, não estimam erro futuro. MAPE divide diretamente pelo alvo e pode ficar inválido com zero. Feriados só atuam quando sua data coincide com observação: agregação no início do mês não recebe automaticamente o efeito de todos os feriados do mês.

Na manutenção, preservar grão, calendário, versões e backtest separado. Regressoras adicionais são descartadas; `SEED=42` exportada não controla o ajuste nem intervalos. MLflow é importado no topo mesmo com logging desligado. O notebook instala Prophet sem pin e reinicia Python.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/prophet_wrapper/README.md). SHA-256 da fonte histórica da redação: `0378491f1b9cdcb33a1888aae3c4537174a8d846040ea6f551d802190805652d`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0104](#doc-0104) · [Próximo: D0106](#doc-0106) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0106"></a>
<a id="doc-0106"></a>
### D0106 — O que uma banda de score representa?

O README de `score_bands` serve ao analista que quer inspecionar como um score ordena eventos numa população. A função forma grupos por quantis e resume volume, mínimo/máximo, taxa do evento e cobertura acumulada na direção declarada. O documento existe para impedir que uma coluna histórica chamada `aprovacao_acum` seja confundida com aprovações de uma política real: ela mede a fração da base percorrida das melhores para as piores bandas, não decisões tomadas.

Para usar o helper, scores e target binário precisam estar alinhados; o valor 1 é tratado como evento adverso, e `higher_score_is_better` deve refletir o significado do score. O retorno é DataFrame pandas; muitos empates podem reduzir a quantidade de bandas porque limites quantílicos duplicados são descartados. Na manutenção, conferir essa regra, colunas de saída e direção de ordenação com a implementação. A cada população, os quantis são recalculados: duas tabelas de bandas não compartilham necessariamente os mesmos cortes. A leitura pode orientar investigação de monotonicidade ou discussão de cutoff, mas não escolhe uma política, calibra probabilidade ou autoriza aplicação regulada.

<!-- editorial:exclude:start -->
Fonte: [README de score_bands](../../hub_snippets/ml/score_bands/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0105](#doc-0105) · [Próximo: D0107](#doc-0107) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0107"></a>
<a id="doc-0107"></a>
### D0107 — Como coeficientes viram pontos de scorecard?

O README de `scorecard_builder` atende a quem já treinou um modelo logístico sobre variáveis WOE e precisa revisar uma tabela de pontos por faixa. Ele explica a ponte entre log-odds, uma escala base, odds de referência e PDO — pontos para dobrar as odds favoráveis na convenção escolhida. A função `build_scorecard` distribui intercepto e contribuições dos coeficientes entre features e faixas; não treina modelo nem descobre os bins.

O leitor precisa alinhar a ordem de `coefs` e `feature_names`, fornecer tabelas pandas por feature com `faixa` e `woe`, declarar se o evento modelado é adverso e conferir a escala. A saída Spark do helper de WOE não encaixa diretamente: exige coleta pequena e renomeação controlada. O retorno é DataFrame de coeficiente, WOE e pontos arredondados; a soma arredondada pode divergir um pouco da transformação contínua. Na manutenção, conferir fórmula, direção `event_is_bad`, validações e nomes de campos com o código. A tabela não atribui faixa a novos clientes, não calcula score individual, não escolhe cutoff nem certifica uso em ambiente regulado.

<!-- editorial:exclude:start -->
Fonte: [README de scorecard_builder](../../hub_snippets/ml/scorecard_builder/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0106](#doc-0106) · [Próximo: D0108](#doc-0108) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0108"></a>
<a id="doc-0108"></a>
### D0108 — Como ler uma atribuição SHAP deste wrapper?

O README de `shap_explainer` serve a quem já possui modelo validado, dados alinhados e output a explicar. `compute_shap` escolhe árvore, linear ou Kernel e devolve matriz de contribuições por linha/feature e base escalar. Em saída com múltiplas classes, `output_index` seleciona explicitamente uma; a escala depende do output do explainer e não é sempre probabilidade. `get_feature_importance_shap` ordena média absoluta e calcula percentuais antes de limitar `top_n`.

Quando o classificador de árvores devolve várias saídas e a ordem das classes foi confirmada, `compute_shap(modelo, X_eval, nomes, model_type="tree", output_index=1)` explica a saída de índice 1 em todas as linhas. Se o retorno SHAP já for matriz 2D, `output_index=1` não seleciona classe; confirme o output e sua escala separadamente. `max_samples` não limita árvores. No Kernel, a função pode amostrar até `max_samples` linhas e usar até cem delas como background, mas não devolve os índices sorteados. Assim, o chamador precisa controlar a amostra e seus IDs antes da chamada para ligar explicações a pessoas sem erro.

No ramo linear, `background` admite matriz finita, 2D e de mesma largura; `None` usa `X`. Árvore e Kernel rejeitam essa opção. Os plotters global/local fecham Matplotlib e não retornam `Figure`; o local indexa `X[idx]`, por isso matriz NumPy é rota mais segura. SHAP não comprova causalidade, e o pin do notebook é histórico.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/shap_explainer/README.md). SHA-256 da fonte histórica da redação: `68d80d7ba97fb25301629d36bd8bf787c652f34cd1fca6bbba80ba56272330ce`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0107](#doc-0107) · [Próximo: D0109](#doc-0109) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0109"></a>
<a id="doc-0109"></a>
### D0109 — Como separar períodos sem embaralhar o futuro?

O README de `split_temporal` orienta quem precisa criar treino, validação e teste em ordem cronológica. Sua função `temporal_split` recebe DataFrame pandas, converte datas em períodos completos observados, reserva blocos para treino/validação e deixa gaps opcionais antes dos blocos seguintes. O documento existe porque uma divisão aleatória pode permitir que o passado avaliado apareça depois do futuro usado no treino, enquanto percentuais por período são frequentemente confundidos com percentuais de linhas.

O leitor deve definir a unidade de calendário e confirmar períodos suficientes; `gap_periods=1` pula uma posição observada, não necessariamente um mês de relógio se há lacunas. Com `group_col`, entidades não nulas vistas no treino saem da validação e entidades anteriores saem do teste, desenho útil para generalização a entidades novas, mas inadequado a todo painel. Datas nulas podem ficar fora de todas as partes. Renomeie previamente `__period`, pois essa coluna é sobrescrita e removida. Na manutenção, conferir validações, regra de gaps e retorno dos três DataFrames com o código. A função não ajusta preprocessing, não fornece múltiplos cortes e não corrige uma feature calculada com informação futura antes da separação.

<!-- editorial:exclude:start -->
Fonte: [README de split_temporal](../../hub_snippets/ml/split_temporal/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0108](#doc-0108) · [Próximo: D0110](#doc-0110) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0110"></a>
<a id="doc-0110"></a>
### D0110 — O que um hazard ratio permite concluir?

O README de `survival_cox` serve a quem investiga tempo até evento com censura e covariáveis. O modelo de Cox relaciona essas variáveis ao hazard, a taxa instantânea condicional do evento, sob a hipótese de riscos proporcionais. O guia explica `train_cox_ph`, que ajusta `CoxPHFitter` e devolve modelo com métricas, e `validate_proportionality`, que examina o pressuposto. Ele existe para evitar traduzir um hazard ratio em mudança direta da probabilidade final ou em efeito causal.

O leitor precisa preparar duração positiva, evento binário, features e linhas utilizáveis em pandas; `lifelines` é dependência; o logging explícito do helper é opcional, mas autologging da sessão exige conferência separada. A função remove linhas com nulos nas colunas usadas, então compare `n_observations` com a entrada. C-index e AIC parcial retornados pertencem ao ajuste na própria amostra, não a uma validação externa. Na manutenção, sincronizar parâmetros, forma do retorno e regra de complete case com o código. Se covariáveis variam no tempo sem representação adequada, há censura informativa ou proporcionalidade inadequada, a conclusão deve ser revista; o helper não resolve esses problemas automaticamente.

<!-- editorial:exclude:start -->
Fonte: [README de survival_cox](../../hub_snippets/ml/survival_cox/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0109](#doc-0109) · [Próximo: D0111](#doc-0111) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0111"></a>
<a id="doc-0111"></a>
### D0111 — Quando comparar TabNet com o baseline?

O README de `tabnet_wrapper` documenta `train_tabnet` para classificação binária ou regressão sobre matrizes preparadas. O retorno contém estimador treinado, métricas de validação e `feature_importances_` global da biblioteca. O consumidor o usa depois de estabelecer uma referência simples sob a mesma partição, para perguntar se o custo da rede neural acrescenta valor mensurável.

Num problema binário com oito colunas, o exemplo informa treino/validação, ajusta TabNet por até quinze épocas e lê `auc_val`, `gini_val` e importância por coluna. `cat_idxs` e `cat_dims` precisam corresponder a índices e cardinalidades; o wrapper confere comprimentos e faixas declaradas, mas não cada código categórico da matriz. Treino exige duas classes; a checagem local da validação aceita rótulos 0/1 sem exigir ambas. Classe única pode causar erro ou AUC indefinida; confirme ambas antes do fit. Os parâmetros do regressor não são todos os mesmos fixados no classificador.

Na manutenção, registrar codificação, versões, seed, custo e comparação sob dados iguais. A importância vem de máscaras agregadas do estimador, não de SHAP ou efeito causal individual. PyTorch e `pytorch-tabnet` são necessários; MLflow tem import protegido, mas logging ligado exige a dependência após treino.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/tabnet_wrapper/README.md). SHA-256 da fonte histórica da redação: `005400ccb1cc39cc38f0fe28f169e4cd8dc306ad31260b2d0f8294ff39ce7810`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0110](#doc-0110) · [Próximo: D0112](#doc-0112) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0112"></a>
<a id="doc-0112"></a>
### D0112 — Que cuidado torna o baseline CatBoost categórico?

O guia `train_catboost` apresenta `train_catboost_baseline` para classificação binária, multiclasse ou regressão. Recebe matrizes e rótulos de treino/validação, `cat_features` declarado pelo consumidor, parâmetros opcionais e opção de logging; retorna modelo e métricas da tarefa. É uma referência de boosting quando categorias nominais merecem tratamento explícito, não detector automático de tipo ou disponibilidade temporal.

O notebook constrói matriz NumPy `dtype=object`, preserva um código de agência como inteiro na coluna 2 e passa `cat_features=[2]`. Um `column_stack` que promova toda a matriz a float pode fazer CatBoost recusar essa declaração. O helper fixa `allow_writing_files=False` por padrão para evitar `catboost_info/`, mas `params_override` pode reabilitar escrita. Overrides de `loss_function` e, na classificação, `eval_metric` são substituídos pela escolha posterior de `task`.

Na manutenção, conferir tipos, índices, ordem das colunas e validação temporal. O mecanismo categórico ordenado da biblioteca reduz certo vazamento de target, sem certificar point-in-time das features. A validação participa do early stopping. MLflow tem import protegido; se logging estiver ligado e a biblioteca faltar, o erro vem após o treinamento.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/train_catboost/README.md). SHA-256 da fonte histórica da redação: `fe119dc6211b18692561f3df57295aa1ecffc4fbba700c2120d0d9427449d567`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0111](#doc-0111) · [Próximo: D0113](#doc-0113) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0113"></a>
<a id="doc-0113"></a>
### D0113 — Que comparação o baseline LightGBM permite?

O README de `train_lgbm` documenta `train_lightgbm_baseline` para dados tabulares já separados. A função escolhe defaults por tarefa, aceita `params_override`, usa validação para parada antecipada e devolve modelo com métricas. Em binário, há AUC de treino e validação, Gini e diferença de AUC; em regressão, RMSE e gap relativo; em multiclasse, log loss, accuracy e gap de log loss.

Com oito colunas e rótulos binários preparados, o notebook chama `task="binary", log_mlflow=False` e compara a validação com uma referência sob a mesma população. O valor histórico do exemplo não promete desempenho novo. `subsample=0.8` aparece nos defaults, mas sem `subsample_freq` não ativa sozinho amostragem periódica de linhas; `colsample_bytree=0.8` controla colunas. Um override de `objective`, `metric` ou `num_class` pode desalinhar treino e cálculo ainda guiado por `task`.

Na manutenção, preservar ordem das features, partição, versão e parâmetros efetivos. A validação escolhe a iteração, portanto não é teste final. MLflow tem import protegido; com logging ligado, sua ausência só é verificada depois do treino. O wrapper roda localmente, sem Spark distribuído ou registro explícito do modelo.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/train_lgbm/README.md). SHA-256 da fonte histórica da redação: `6cf941340ac7a33ca20d6d5bdfeba9b3c5f154f265b9d09187408555767fcb81`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0112](#doc-0112) · [Próximo: D0114](#doc-0114) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0114"></a>
<a id="doc-0114"></a>
### D0114 — O que o baseline XGBoost prova?

O guia `train_xgboost` introduz uma referência supervisionada para classificação binária, multiclasse ou regressão, após preparar matrizes e rótulos alinhados. `train_xgboost_baseline` monta parâmetros por `task`, usa validação no `fit` e devolve modelo mais AUC/Gini, log loss/accuracy ou RMSE, conforme a tarefa. A pergunta é se o estimador prevê em dados separados sob o mesmo protocolo; isso não demonstra causa nem aprova produção.

O notebook usa a mesma fixture sintética de LightGBM e desliga logging explícito. Uma diferença pequena entre seus números históricos descreve aquelas execuções, sem eleger biblioteca para outra base. No binário, o código só exige ao menos duas classes em treino e validação: três classes podem passar por essa checagem e falhar mais tarde. No multiclasse, a versão testada requer rótulos inteiros consecutivos desde zero. `early_stopping_rounds=0` não elimina um valor já fornecido em `params_override`.

Na manutenção, conferir domínio dos rótulos, classe positiva, features disponíveis na decisão e teste independente; a validação orienta o treino. MLflow tem import protegido, mas logging ligado é checado depois do treino. `log_mlflow=False` não desliga autologging já configurado na sessão.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/train_xgboost/README.md). SHA-256 da fonte histórica da redação: `97cd6a2a3a64bbe95f8f831b10f2ec6c640b868b27de822b6d3de38a00c4e4e8`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0113](#doc-0113) · [Próximo: D0115](#doc-0115) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0115"></a>
<a id="doc-0115"></a>
### D0115 — O que uma projeção UMAP mostra?

O README de `umap_viz` orienta a exploração visual de labels já existentes. `compute_umap(X, n_components=2, n_neighbors=15, min_dist=0.1)` devolve coordenadas; `plot_umap_clusters(X_scaled, labels, ...)` recalcula a projeção com esses defaults e retorna figura Plotly. A rota `plot_umap_clusters_resolvido(..., theme)` valida o tema antes do cálculo, reaproveita a mesma projeção e muda apenas paleta/layout.

Com três grupos sintéticos plantados em dez atributos padronizados, cores podem revelar mistura ou ilhas que merecem investigação. O gráfico não preserva escala nem distância original; seus eixos não têm unidade de negócio. O argumento `n` só muda o rodapé, sem amostrar dados ou conferir seu valor. `cluster_names` mapeia strings `"0"`, `"1"` pela posição da lista; labels arbitrários ou ruído `-1` podem ficar sem nome. A contagem do rodapé exclui `-1`.

Na manutenção, comparar parâmetros e validar clusters no espaço original. O wrapper fixa `random_state=42`; variar sementes exige a API UMAP direta. O plotter não expõe parâmetros UMAP, então comparação de configurações exige `compute_umap` e figura própria. A seção 11 distingue a função legada, sem `theme`, da rota temática; ambas usam a mesma lógica de projeção. `umap-learn` é importado ao calcular.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/umap_viz/README.md). SHA-256 da fonte histórica da redação: `e40f65a63ad2f4cd42b57573ccc8390421960850e2590d279652b45a7ad7838a`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0114](#doc-0114) · [Próximo: D0116](#doc-0116) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0116"></a>
<a id="doc-0116"></a>
### D0116 — Por que uma célula de safra pode não ter taxa?

O README de `vintage_analysis` atende quem compara contratos ou clientes segundo o período de origem e sua idade. Ele explica MOB, meses desde a originação, e a matriz safra × MOB para que safras recentes não pareçam melhores apenas por terem menos tempo de observação. O documento existe para fixar o significado de denominador, cobertura e evento acumulado antes de construir curvas ou heatmaps.

`build_vintage_table` recebe pandas, reduz duplicidades por contrato/MOB segundo máximo do evento e calcula a taxa somente quando todos os contratos da coorte válida têm observação naquela célula. Em células parcialmente observadas, `taxa_acumulada` fica ausente e `cobertura_observada` informa a lacuna; não preencher com zero. Um MOB totalmente ausente pode nem gerar linha. MOB negativo ou nulo sai antes de formar o denominador, que deve ser reconciliado com a população de origem. O leitor pode usar `compare_safras` em checkpoints iguais e funções de figura para comunicar o resultado. Na manutenção, conferir essa regra, os campos de saída e as variantes de tema `_resolvido` com a implementação. Tema muda aparência; não altera maturidade, taxa nem evidencia causa de deterioração.

<!-- editorial:exclude:start -->
Fonte: [README de vintage_analysis](../../hub_snippets/ml/vintage_analysis/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0115](#doc-0115) · [Próximo: D0117](#doc-0117) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0117"></a>
<a id="doc-0117"></a>
### D0117 — Como repetir uma avaliação ao longo do tempo?

O README de `walk_forward` serve a quem não quer confiar em um único mês de validação. A função organiza vários cortes sucessivos: em cada fold, o histórico disponível para treino cresce, um gap opcional é respeitado e um bloco posterior é entregue a `model_fn` para avaliação. O documento existe para tornar essas fronteiras observáveis, já que estabilidade temporal não pode ser inferida de um split isolado.

A entrada é pandas e o callback recebe DataFrames de treino e teste, devolvendo um dicionário de métricas. O helper acrescenta número do fold, fim do treino, início do teste e quantidades de linhas. Ele não ajusta o modelo: o callback precisa treinar e aprender transformações apenas com o treino recebido. `gap` e `step` percorrem períodos **observados**, não necessariamente meses consecutivos de relógio; com histórico insuficiente, a lista de resultados pode ser vazia. Na manutenção, conferir parâmetros, metadados acrescentados, impressão de médias e colisões de chaves do callback com o código. O leitor deve olhar `len(results)` e cada janela antes de discutir performance; a função não prova ausência de vazamento nem monitora produção.

<!-- editorial:exclude:start -->
Fonte: [README de walk_forward](../../hub_snippets/ml/walk_forward/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0116](#doc-0116) · [Próximo: D0118](#doc-0118) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0118"></a>
<a id="doc-0118"></a>
### D0118 — O que WOE e IV dizem sobre uma variável?

O README de `woe_iv_calculator` orienta a leitura de uma feature já categorizada diante de alvo binário. WOE compara a participação de “bons” e “maus” em cada faixa; IV soma a separação dessas distribuições. O documento existe porque um IV alto pode atrair seleção automática de feature sem que a data de disponibilidade, a construção das faixas e a estabilidade tenham sido conferidas.

`calculate_woe_iv` opera em DataFrame Spark, exige target 0/1 com ambas as classes e smoothing positivo. Devolve uma tabela Spark por faixa e um `float` de IV total; a coluna de faixa mantém o nome da feature original. Isso importa ao integrar com `scorecard_builder`, que espera pandas e uma coluna chamada `faixa`: a ponte deve ser pequena e explícita. O guia também mostra `classify_iv`, uma régua histórica local, não obrigação regulatória. Na manutenção, conferir fórmula, campos, alisamento e ações Spark com a implementação. O helper não cria binning, não impede vazamento de alvo e não demonstra que a variável melhorará um modelo fora do tempo.

<!-- editorial:exclude:start -->
Fonte: [README de woe_iv_calculator](../../hub_snippets/ml/woe_iv_calculator/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0117](#doc-0117) · [Próximo: D0119](#doc-0119) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0119"></a>
<a id="doc-0119"></a>
### D0119 — Onde escolher um helper Spark?

Este README é o índice da categoria `hub_snippets/spark`. Ele existe para quem sabe que precisa continuar em DataFrame distribuído, mas ainda não escolheu entre calendário, diagnóstico de join, nulos, junção point-in-time, PSI, prévia ou amostragem. Sua função é encaminhar ao guia local de cada um dos sete objetos, preservando a diferença entre o mapa da coleção e o contrato da função.

O leitor deve localizar a demanda na tabela e abrir o README de objeto antes de importar. As entradas e saídas variam: algumas funções devolvem DataFrame, outras dicionário ou número, e `safe_display` produz efeito de exibição. Os custos também variam; uma API curta pode disparar shuffle, quantis, joins e coletas agregadas. O índice aponta as rotas relacionadas do catálogo geral e da entrada `.assistant`, mas não substitui assinatura, exemplo ou avaliação de volume. Na manutenção, conferir se a lista ainda tem todos os objetos diretamente presentes, se os links relativos chegam aos guias e se a descrição não promete suporte de runtime não testado. Resultado sintético local não homologa compute do destino.

<!-- editorial:exclude:start -->
Fonte: [índice Spark](../../hub_snippets/spark/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0118](#doc-0118) · [Próximo: D0120](#doc-0120) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0120"></a>
<a id="doc-0120"></a>
### D0120 — Qual calendário foi transformado em feature?

O README de `date_features` serve a quem quer derivar atributos de uma data sem cada notebook inventar convenções próprias. A função produz nove colunas Spark, como dia da semana ISO, fim de semana, mês, trimestre, ano e indicadores de feriado. O documento existe porque um indicador de calendário pode estar matematicamente correto e ainda se referir à data errada, como processamento em vez de decisão do cliente.

O leitor informa DataFrame, coluna de data, prefixo opcional e datas de feriado do projeto. A lista embutida cobre nove feriados nacionais brasileiros de data fixa; não constitui calendário móvel, local ou bancário. `to_date` descarta horário e pode reagir a texto inválido conforme configuração do Spark; `withColumn` substitui colunas existentes se os nomes colidirem. O retorno mantém as linhas e acrescenta até nove campos, substituindo colisões, sem medir utilidade preditiva. Na manutenção, conferir alias, nomes, lista fixa e regras dos dois indicadores de feriado com o código; documentar a fonte de `holiday_dates`. Feriado fixo e calendário fornecido respondem perguntas distintas, e nenhum deles garante ausência de vazamento temporal.

<!-- editorial:exclude:start -->
Fonte: [README de date_features](../../hub_snippets/spark/date_features/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0119](#doc-0119) · [Próximo: D0121](#doc-0121) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0121"></a>
<a id="doc-0121"></a>
### D0121 — O que aconteceria com as linhas após um join?

O README de `join_diagnostics` orienta a checagem anterior a uma junção de DataFrames Spark. Ele existe porque um join pode multiplicar fatos, perder linhas ou manter linhas sem atributos sem levantar erro. `diagnosticar_join` informa cobertura, chaves nulas, órfãs, multiplicidade da direita e expansão prevista para left e inner join, permitindo que o analista confronte o efeito com o grão desejado.

A cobertura usa linhas com chave válida à esquerda como denominador; chaves nulas são contadas separadamente. Multiplicidade da direita considera apenas chaves que também aparecem à esquerda. Para saber quantas linhas originais o inner perderia, some chaves nulas e linhas válidas sem match: o total final do inner pode mascarar perdas se outras chaves duplicarem. O retorno é dicionário com contagens e pequenas amostras de chaves; não executa a junção de negócio nem escolhe o tipo correto. Na manutenção, conferir fórmulas, nomes de campos e semântica das amostras com o código. Agregações e joins diagnósticos têm custo; expansão acima de 1 é sinal para verificar a unidade, não defeito universal.

<!-- editorial:exclude:start -->
Fonte: [README de join_diagnostics](../../hub_snippets/spark/join_diagnostics/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0120](#doc-0120) · [Próximo: D0122](#doc-0122) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0122"></a>
<a id="doc-0122"></a>
### D0122 — Que ausência o semáforo está mostrando?

O README de `null_summary` atende quem já tem um DataFrame Spark e quer localizar valores `NULL` por coluna. Ele existe porque um semáforo parece um julgamento de qualidade, mas o código apenas compara percentuais de nulidade com dois limiares informados pelo consumidor. A tabela resultante mostra nome da coluna, contagem, percentual e status verde, amarelo ou vermelho, ordenada do maior percentual para o menor.

A função faz `count()` da população recebida e coleta uma linha agregada de somas de `isNull()`. Por isso o recorte do DataFrame define o denominador, e a chamada pode ter custo mesmo sem escrita. O limiar é inclusivo para amarelo/vermelho; alterar a política muda a cor sem mudar os dados. Strings vazias, códigos sentinela e `NaN` não são automaticamente `NULL`. Na manutenção, conferir cálculo, campos, emojis e falta de validação dos limiares com a implementação. Em DataFrame vazio, agregados nulos podem causar falha ao converter `None` em inteiro; o leitor deve verificar a população antes. O retorno não explica por que o valor falta nem substitui uma checagem de chave ou domínio.

<!-- editorial:exclude:start -->
Fonte: [README de null_summary](../../hub_snippets/spark/null_summary/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0121](#doc-0121) · [Próximo: D0123](#doc-0123) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0123"></a>
<a id="doc-0123"></a>
### D0123 — A feature já existia no instante da decisão?

O README de `pit_join` orienta quem precisa anexar histórico de features a linhas de decisão sem consultar o futuro. Cada versão tem uma data de referência e uma data em que se torna utilizável; a função calcula esta última somando um atraso de publicação explícito e escolhe a versão elegível mais recente por entidade e decisão. O documento existe porque um join pela chave ou pelo valor atual pode produzir uma base historicamente impossível.

`pit_join` recebe DataFrames Spark, chave, tempos, atraso obrigatório e janela máxima opcional; devolve fatos preservados com colunas selecionadas e um diagnóstico. Esse dicionário separa linhas sem chave/data, entidades sem histórico, histórico indisponível na data e linhas com feature. A janela limita idade desde a referência, enquanto o fuso da sessão afeta conversões de data. Empate no instante elegível escolhido bloqueia pela política padrão; versões antigas empatadas não implicam o mesmo bloqueio. Na manutenção, conferir condições, nomes, sufixo e quatro categorias com o código. A função executa joins e contagens potencialmente caros; atraso fixo não reconstrói fonte com publicação variável ou revisões históricas perdidas.

<!-- editorial:exclude:start -->
Fonte: [README de pit_join](../../hub_snippets/spark/pit_join/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0122](#doc-0122) · [Próximo: D0124](#doc-0124) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0124"></a>
<a id="doc-0124"></a>
### D0124 — O índice de estabilidade mede que mudança?

O README de `psi_calculator` atende quem monitora distribuição com duas populações Spark. PSI compara proporções em faixas numéricas definidas pela referência; `calcular_csi` percorre features, aplicando essa rotina às numéricas e comparação categórica às demais. O documento existe para deixar explícitos a régua fixa, o tratamento de ausentes e a diferença entre medir mudança e concluir degradação de um modelo.

O leitor informa DataFrames comparáveis, colunas e configuração de bins. Para categorias, o código usa grupos de valores e uma guarda `max_categorias` antes da coleta agregada; essa guarda não limita bytes totais nem evita o custo do `groupBy`. `calcular_psi` devolve `float`; `calcular_csi`, dicionário ordenado por índice; `interpretar_psi`, texto que só classifica com dois limiares. O retorno numérico não traz os cortes e contribuições por faixa, então mantenha contexto e referência ao interpretar. Na manutenção, conferir assinaturas, classificação, missing e o tipo determinado pela referência com a implementação. PSI alto pode resultar de mudança de unidade ou de população; não identifica causa, performance, necessidade automática de retreino ou valor de negócio.

<!-- editorial:exclude:start -->
Fonte: [README de psi_calculator](../../hub_snippets/spark/psi_calculator/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0123](#doc-0123) · [Próximo: D0125](#doc-0125) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0125"></a>
<a id="doc-0125"></a>
### D0125 — Uma prévia limitada representa a população?

O README de `safe_display` serve a quem quer ver poucas linhas de um DataFrame Spark sem entregar uma prévia ilimitada ao renderer. A função cria um prefixo de `limit+1`, conta esse prefixo para detectar truncamento e envia até `limit` linhas à função de exibição. O documento existe para distinguir o número que apareceu na tela da quantidade real de linhas e da distribuição da base.

O leitor deve passar `display_fn=display` no notebook importador, pois o módulo não herda automaticamente o `display` do escopo interativo. O retorno é `None`; a ação está na renderização e, se `msg=True`, na mensagem com `+` quando há mais linhas. `msg=False` não elimina a contagem limitada. A função não escolhe linhas aleatórias, não filtra um caso e não reduz o custo de agregação ou join já embutido no DataFrame. Na manutenção, conferir teto, busca do renderer, assinatura e texto do aviso com o código. Para estimar média ou prevalência, usar amostra ou agregação apropriada, declarando população e método; primeiras linhas não são evidência representativa.

<!-- editorial:exclude:start -->
Fonte: [README de safe_display](../../hub_snippets/spark/safe_display/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0124](#doc-0124) · [Próximo: D0126](#doc-0126) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0126"></a>
<a id="doc-0126"></a>
### D0126 — Quando preservar cada estrato na amostra?

O README de `smart_sample` orienta quem reduz um DataFrame Spark para inspeção ou prototipação. A função oferece modo simples com semente e teto `n`, ou modo estratificado que reserva ao menos uma linha por categoria quando o número de estratos cabe no orçamento. O documento existe porque “amostra pequena” não garante que uma categoria rara apareça, e preservá-la deliberadamente muda as proporções vistas pelo leitor.

Se a base tem no máximo `n` linhas, o retorno é o próprio DataFrame. No modo simples, `sample` sem reposição seguido de `limit(n)` pode entregar menos que `n`; com `n < total <= 1,2 × n`, a fração é 1 e o limite pode selecionar um prefixo, sem sorteio efetivo. No estratificado, a alocação de vagas restantes usa maiores restos; mais estratos que vagas gera erro. A função conta linhas e estratos, mas não coleta valores de categoria ao driver, e devolve DataFrame sem pesos de amostragem. Na manutenção, conferir metas por estrato, condição de erro e semântica da seed com a implementação. Não use uma amostra que força categorias raras para estimar prevalência global sem ponderação adequada; também não trate a mesma seed como garantia de linhas idênticas após mudar dados ou partições.

<!-- editorial:exclude:start -->
Fonte: [README de smart_sample](../../hub_snippets/spark/smart_sample/README.md). Detalhe: [MT07](MT-parte-ii.md#mt07).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0125](#doc-0125) · [Próximo: D0127](#doc-0127) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0127"></a>
<a id="doc-0127"></a>
### D0127 — Onde encontrar dados controlados para aprender e testar?

O índice da categoria `testing` orienta a escolha de dados sintéticos antes de abrir uma tabela real. Ele aponta para o objeto `fixtures` e seu guia local; não implementa geradores nem executa testes. A separação importa porque encontrar uma entrada no catálogo não informa, por si só, quais bibliotecas, dimensões ou cuidados uma chamada exige. Primeiro escolha o cenário; depois confira o README do objeto e seu exemplo.

Para experimentar um diagnóstico de duplicatas, por exemplo, siga a rota de `base_tabular` e procure uma configuração com identificadores repetidos. Para uma junção temporal, a rota pertinente é `fatos_e_features`, que prepara versões anteriores e futuras. O índice também situa séries por entidade e painéis de safras, permitindo escolher pelo problema em vez de apenas pelo nome da função.

A geração começa com listas locais em Python, mesmo quando o retorno é um DataFrame Spark. Use dimensões pequenas; probabilidades de sorteio não asseguram quotas exatas. Os testes do mantenedor estão em `tools/tests/runtime/`, fora do produto distribuído. Ao manter o índice, confira a tabela de objetos e seus destinos. Uma fixture ou teste sintético não representa a distribuição de uma carteira e não homologa permissões, volume ou runtime do destino.

<!-- editorial:exclude:start -->
Fonte: [índice de testing](../../hub_snippets/testing/README.md). Detalhe: [MT27](MT-parte-vii.md#mt27). Uso: [MU19](MU-parte-vi.md#mu19).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0126](#doc-0126) · [Próximo: D0128](#doc-0128) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0128"></a>
<a id="doc-0128"></a>
### D0128 — Como preparar uma entrada que revele o comportamento esperado?

O README de `fixtures` explica quatro famílias de dados fictícios e os limites de cada cenário. `base_tabular` prepara registros com chaves, categorias, nulos e alvo; `serie_temporal` produz entidade por mês; `fatos_e_features` devolve um par de DataFrames; `safras` organiza contratos por idade em meses. O guia conecta essa escolha à API pública, à implementação e ao notebook de demonstração, sem transformar dados de teste em estimativa de negócio.

Uma chamada `base_tabular(n=20, n_entidades=5, seed=42)` constrói vinte linhas com cinco identificadores, permitindo verificar duplicidade deliberada. Já uma probabilidade de nulos não fixa sua quantidade: para exigir exatamente um nulo, prepare linhas explícitas. No par temporal, `eh_futura` funciona como gabarito do cenário com um cliente por decisão; não é um preditor nem resolve toda forma de vazamento.

Os geradores montam listas locais, requerem PySpark e procuram uma sessão Spark ativa, tentando criar uma se necessário. Devolvem dados em memória, sem gravar tabelas. Registre parâmetros e versões, mantenha dimensões pequenas e ordene antes de comparar resultados. Ao alterar o recurso, reconcilie assinaturas, validações e exemplos; `n_entidades=0`, por exemplo, usa o padrão em vez de ser recusado. A leitura ou execução sintética não certifica o runtime do destino.

<!-- editorial:exclude:start -->
Fontes: [guia de fixtures](../../hub_snippets/testing/fixtures/README.md), [implementação](../../hub_snippets/testing/fixtures/fixtures.py), [API pública](../../hub_snippets/testing/fixtures/__init__.py) e [exemplo](../../hub_snippets/testing/fixtures/exemplo_fixtures.py). Detalhe: [MT27](MT-parte-vii.md#mt27).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0127](#doc-0127) · [Próximo: D0129](#doc-0129) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0129"></a>
<a id="doc-0129"></a>
### D0129 — Como navegar pelos componentes visuais do Hub?

O README de `visual` é o índice de oito objetos: `badge`, `divider`, `index_generator`, `kpi_card`, `section_header`, `tema`, `theme_lab` e `theme_plotly`. Ele organiza componentes de comunicação e rotas de tema, ajudando quem escreve notebooks ou READMEs a escolher o objeto cuja função coincide com a necessidade. Um badge apresenta estado, um índice mostra roteiro, um cartão exibe valor já calculado e `tema` resolve tokens; nenhuma dessas peças calcula a qualidade do dado por existir na página.

Um uso válido para abrir uma etapa EDA vai ao README de `section_header`, verifica a chamada e a saída HTML e só então insere o componente no notebook. Para aplicar cores Plotly, o leitor deve abrir `theme_plotly` e decidir entre aplicar a uma figura e registrar template de sessão. `theme_lab` aparece no índice com guia de primeiro uso; permite experimentar e comparar propostas, com salvamento opcional em pasta autorizada. Validar em `tema`, aplicar no consumidor e salvar são ações distintas.

Na manutenção, conferir caminhos dos oito objetos listados, assinaturas, imports e exemplos reais antes de mudar o índice. O README é mapa de categoria, não o contrato de quinze seções de cada objeto. A visualização precisa conservar rótulos e critérios textuais, e um tema validado estruturalmente não homologa acessibilidade ou resultado analítico em todas as telas.

<!-- editorial:exclude:start -->
Fonte: [README de visual](../../hub_snippets/visual/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0128](#doc-0128) · [Próximo: D0130](#doc-0130) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0130"></a>
<a id="doc-0130"></a>
### D0130 — Quando um badge é um sinal fiel?

O README de `badge` descreve `badge_status`, `badge_score` e `badge_inline`, além das variantes V04 que recebem tema resolvido. São geradores de HTML para comunicar um estado definido pelo chamador; não verificam a origem do estado. `badge_score` compara uma razão com cortes de 0,5 e 0,8 para escolher a faixa visual. O consumidor deve saber se numerador, máximo e rótulo representam a mesma unidade e período.

Um uso válido calcula a taxa antes, passa valor e máximo coerentes e mostra também o critério textual ao lado do badge. Há uma sutileza: a faixa é escolhida pelo valor não arredondado, enquanto a exibição pode arredondar. Um placar de 79,6 em 100 pode parecer 80 na tela e ainda cair na faixa abaixo de 0,8. O README registra que `tipo` desconhecido recai em `info` e `max=0` não é rejeitado; o chamador precisa validar ambos se forem críticos.

Na manutenção, testar fronteiras de 0,5 e 0,8, zero, entradas inesperadas e o contraste final. O par `warn` documentado tem contraste insuficiente para texto normal. A variante temática altera CSS localmente e não corrige a classificação nem aplica política global. Rótulo, legenda e medida original devem acompanhar o sinal em decisões importantes.

<!-- editorial:exclude:start -->
Fonte: [README de badge](../../hub_snippets/visual/badge/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0129](#doc-0129) · [Próximo: D0131](#doc-0131) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0131"></a>
<a id="doc-0131"></a>
### D0131 — Que limite tem um separador visual?

`divider` agrupa oito funções: quatro variantes legadas e quatro temáticas que devolvem trechos HTML de separação, com três variações baseadas em `<hr>` e uma composição de linha dupla. O README oferece exemplos e explica opções de espaçamento e aparência para leitores de notebook. Essas funções organizam a leitura entre blocos, mas não criam uma seção semântica, título, checkpoint de execução ou mudança de fluxo do código.

Um uso válido é gerar uma linha entre explicação metodológica e resultados e passá-la ao mecanismo de exibição HTML do ambiente. A função retorna uma string; ela não chama `displayHTML` por conta própria. Para uma página acessível, um cabeçalho textual continua necessário quando a passagem marca uma nova seção. Cada uma das quatro variantes legadas — `light`, `medium`, `heavy` e `section` — tem contraparte `_resolvido(theme)`; o tema age somente quando o consumidor chama essa rota explicitamente.

Na manutenção, verificar margens e contraste no renderizador onde a string aparece, inclusive em telas estreitas. Ajustar `divider` não deve mascarar ordem errada de células ou ausência de legenda. As quatro contrapartes temáticas precisam ser conferidas junto das quatro legadas para evitar divergência de espaçamento ou CSS. O README é referência de apresentação local; a confirmação de que a etapa foi executada pertence ao notebook e às evidências de seu fluxo.

<!-- editorial:exclude:start -->
Fonte: [README de divider](../../hub_snippets/visual/divider/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0130](#doc-0130) · [Próximo: D0132](#doc-0132) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0132"></a>
<a id="doc-0132"></a>
### D0132 — O índice EDA reflete a execução do notebook?

O README de `index_generator` documenta `gerar_indice_eda`, que transforma entradas de `SECOES_EDA` em um roteiro Markdown ou HTML. Se o chamador não fornece etapas, a função inclui 0 a 8. Se fornece lista, preserva sua ordem e até repetições. A função serve ao autor que deseja mostrar ao leitor a sequência planejada de uma análise sem copiar manualmente títulos e emojis de cada etapa.

Um uso válido escolhe explicitamente as etapas presentes no notebook e revisa o texto exibido depois de mover ou remover células. O índice não inspeciona o notebook para descobrir o que existe: pode listar uma etapa ainda não escrita ou omitir uma já executada. Também não produz, por si, links clicáveis para células nem estado de conclusão. O consumidor precisa manter título, posição e evidência da execução em outro lugar.

Na manutenção, conferir a correspondência entre o mapa `SECOES_EDA`, a lista passada e os cabeçalhos reais. Alterar um rótulo compartilhado pode modificar índices em vários notebooks; uma lista local pode continuar semanticamente desatualizada mesmo que o HTML renderize bem. Emoji é sinal de navegação, não resultado analítico. Testar formato de saída e etapas inválidas no destino antes de publicar o roteiro.

<!-- editorial:exclude:start -->
Fonte: [README de index_generator](../../hub_snippets/visual/index_generator/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0131](#doc-0131) · [Próximo: D0133](#doc-0133) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0133"></a>
<a id="doc-0133"></a>
### D0133 — O que um cartão de KPI entrega?

`kpi_card` transforma um dicionário de indicadores já preparados em apresentação compacta. `kpi_card_html` produz cartões HTML com rótulo e valor escapados; `kpi_card_markdown` produz uma linha textual e escapa apenas o separador `|`. A variante V04 `kpi_card_html_resolvido` recebe tema para o CSS do HTML; o Markdown não muda com tema. O consumidor é o autor de um relatório que precisa colocar poucos números e ressalvas perto do início, sem esconder a análise que lhes dá sentido.

Um exemplo válido passa `{"Linhas": "1.000", "Cobertura": "92,8%", "Ressalva": "amostra parcial"}` depois de calcular cobertura, definir denominador e formatar a taxa. O helper preserva ordem de inserção, mas não agrega dados, arredonda, acrescenta unidade ou escolhe status. Com dicionário vazio, HTML retorna string vazia e Markdown retorna uma linha mínima, sem diagnóstico. `None` também vira texto.

Na manutenção, comparar cada valor com a origem, período e população. Rótulos devem ser únicos após conversão a string: chaves `1` e `"1"` podem colidir na preparação Markdown. Texto externo requer revisão do renderizador, pois escape parcial não é sanitização geral. Uma mudança visual não torna o indicador confiável ou aprovado.

<!-- editorial:exclude:start -->
Fonte: [README de kpi_card](../../hub_snippets/visual/kpi_card/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0132](#doc-0132) · [Próximo: D0134](#doc-0134) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0134"></a>
<a id="doc-0134"></a>
### D0134 — Como um cabeçalho declara a etapa certa?

O README de `section_header` documenta `section_header_html`, que gera título `h3` e descrição HTML para orientar a leitura de um notebook. A função pode consultar `SECOES_EDA` pela etapa ou usar emoji, título e descrição explícitos; textos não vazios fornecidos pelo chamador prevalecem sobre o mapa. A rota V04 `_resolvido` aplica tokens de um tema de notebook recebido explicitamente. Nenhuma das duas rotas descobre o conteúdo das células ou comprova que a etapa foi executada.

Um uso válido passa `etapa=3` e uma descrição concreta da verificação de faltantes feita com dados sintéticos. Para uma seção fora do roteiro, fornece título e descrição próprios em vez de escolher número apenas pelo ícone. Os campos passam por `html.escape`; marcação inserida no título aparece como texto. Etapa inválida ou campos vazios podem cair em “Seção” e “Descrição não informada.” sem erro, por isso o chamador precisa conferir o resultado.

Na manutenção, comparar índice, cabeçalho e conteúdo real após reorganizar o notebook. Testar etapa conhecida, personalização e caracteres `<` e `>`, além da legibilidade no destino. `displayHTML` é responsabilidade do consumidor; obter a string não garante navegação acessível, contraste ou uma análise concluída.

<!-- editorial:exclude:start -->
Fonte: [README de section_header](../../hub_snippets/visual/section_header/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0133](#doc-0133) · [Próximo: D0135](#doc-0135) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0135"></a>
<a id="doc-0135"></a>
### D0135 — Que garantia oferece o núcleo de temas?

`visual.tema` carrega, valida e resolve uma configuração completa antes de outro componente consumi-la. Seu `ResolvedTheme` conserva tokens e origens somente para leitura, avisos e hashes de conteúdo, bytes e dependências. O schema define campos, contexto e opções aceitas; falta ou incompatibilidade explícita falha, sem herança ou default oculto. O núcleo não desenha figura, altera padrão global, aprova identidade ou publica arquivos.

Um exemplo válido carrega `load_reference_theme("notebook")`, confere `brand.primary` e exporta a proposta em memória para revisão. A referência é fixture sintética, não tema operacional aprovado. `load_theme` exige raiz e caminho relativo explícitos; `expected_sha256` prende os bytes recebidos. `fingerprint` relaciona conteúdo, schema, manifesto e protocolo, mas não autentica quem criou a proposta. `to_dict()` fornece cópia editável sem mudar o tema resolvido.

Na manutenção, conferir versão de schema, contexto, avisos e hash ao exportar e reimportar; remover um campo obrigatório deve produzir recusa, não reparo silencioso. Consumidores Plotly e HTML optam pela integração em suas APIs próprias. O README encaminha aplicação de figuras a `theme_plotly` e experimentação a `theme_lab`; Apps e AI/BI têm componentes próprios, sem inferir homologação no Databricks ou autorização de destino.

<!-- editorial:exclude:start -->
Fonte: [README de visual.tema](../../hub_snippets/visual/tema/README.md). Detalhe: [MT23](MT-parte-vi.md#mt23).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0134](#doc-0134) · [Próximo: D0136](#doc-0136) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0136"></a>
<a id="doc-0136"></a>
### D0136 — Como começar uma proposta no Visual Lab?

O guia de primeiro uso conduz uma pessoa iniciante pelo `theme_lab`: abrir o launcher, escolher base, ajustar cor, aplicar, comparar e, se necessário, salvar uma sessão local. O mantenedor prepara o pacote, as dependências e uma pasta regular com acesso controlado; o operador não precisa de Git ou CLI. As referências empacotadas aparecem como demonstração. A galeria compara base e proposta com os mesmos dados sintéticos em seis representações, sem alterar métricas.

Um uso válido abre `build_theme_lab_launcher(save_root=PASTA_DE_RASCUNHOS)`, seleciona um ponto de partida e aplica uma cor HEX válida. Campos pendentes não são a proposta salva: a atualização valida todos os controles juntos e preserva o último rascunho válido diante de erro. JSON avulso guarda só a configuração; sessão rastreável guarda base, proposta, histórico e `session.json`, escrito por último com hashes. Na reabertura, a proposta não vira nova base.

Na manutenção, testar escolha, desfazer, salvar e reabrir no runtime autorizado. Falha de gravação não emite recibo e pode exigir inspeção de resíduo; não consertar hash manualmente. A galeria completa usa `light`; frontend, ACL, acessibilidade e uso autônomo exigem evidência própria no destino. A listagem valida o manifesto da sessão; somente reabrir confere todos os payloads e hashes, sem publicação ou homologação implícita.

<!-- editorial:exclude:start -->
Fonte: [Guia de primeiro uso do theme_lab](../../hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0135](#doc-0135) · [Próximo: D0137](#doc-0137) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0137"></a>
<a id="doc-0137"></a>
### D0137 — O que o Visual Lab preserva entre sessões?

O README técnico de `theme_lab` descreve `ThemeLabDraft`, controles com limites derivados do schema, prévia, comparação, presets, persistência e reabertura. O laboratório recebe um `ResolvedTheme` de contexto notebook, isola base e proposta e revalida a configuração inteira ao aplicar alterações. `get_control_specs()` informa rótulos e limites; controles sem consumidor na galeria ficam desabilitados. A prévia usa os mesmos dados sintéticos nos dois lados para tornar visível a mudança de aparência.

Um exemplo válido parte de preset conhecido, muda cor e tamanho, aplica, compara e salva uma sessão em pasta preparada. `save_theme_lab_session()` registra `base.json`, `proposal.json`, histórico e, por último, `session.json` com hashes e revisão. `reopen_theme_lab_session()` confere bytes e restaura a base original, não a substitui pela proposta. Um JSON avulso salva somente a proposta e não permite retomar toda a autoria. Preset ausente e modo incompatível falham sem troca silenciosa.

Na manutenção, testar adulteração, pasta incompleta, `undo()` depois da reabertura e falhas de I/O. Recibo local não equivale a aprovação, ACL ou assinatura. Testes Python cobrem contrato no kernel, mas não navegador, teclado, contraste ou usuário iniciante. A listagem valida somente o manifesto; integridade dos payloads é conferida ao reabrir. Existência do código não certifica o destino nem autoriza publicação.

<!-- editorial:exclude:start -->
Fonte: [README de theme_lab](../../hub_snippets/visual/theme_lab/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0136](#doc-0136) · [Próximo: D0138](#doc-0138) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0138"></a>
<a id="doc-0138"></a>
### D0138 — Aplicar tema à figura muda a sessão?

`theme_plotly` separa operações legadas e consumo explícito de `ResolvedTheme`. `get_tema_eda` devolve layout; `aplicar_tema` altera e devolve a mesma figura; `registrar_template_plotly` registra `caixa` e muda o default Plotly da sessão. A V03 acrescenta tradução, aplicação e registro resolvidos, com namespace `hub-*` e ativação do default apenas quando pedida. A V07 expõe `get_tokens_plotly(theme)` para consumidores como matriz e distribuições, sem registro global.

Um uso válido cria uma figura sintética, aplica tema uma vez com `fonte` e `n` corretos e ajusta largura específica depois. O helper não conta observações: se `n=3` representa três pontos mensais, o rodapé deve dizer isso. Reaplicar com rodapé acrescenta anotação, podendo duplicá-la. Registrar template afeta figuras posteriores da sessão; aplicar à figura isolada não muda o default. A paleta não recolore traces com cores fixas nem escalas explícitas de heatmap.

Na manutenção, conferir dados dos traces antes/depois, número de anotações, default anterior e renderização final. O adaptador V03 de Plotly aceita `light` e recusa modos sem superfície suficiente; um tema validado não garante renderização em qualquer modo. O README distingue consumidores legados e resolvidos e lista sete APIs; `get_tema_eda` compartilha a paleta legada, enquanto consultas resolvidas devolvem cópias.

<!-- editorial:exclude:start -->
Fonte: [README de theme_plotly](../../hub_snippets/visual/theme_plotly/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0137](#doc-0137) · [Próximo: D0139](#doc-0139) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0139"></a>
<a id="doc-0139"></a>
### D0139 — Catálogo de Agent Skills

O índice apresenta as 15 Agent Skills do Hub a quem precisa escolher método e entender seus recursos. Agent Skill é o mecanismo nativo de instruções da Genie Code; nomes `hub-ml-*`, procedimentos, templates e helpers são conteúdo deste projeto. Cada pasta tem `SKILL.md` com nome, descrição, escopo e passos; não é módulo Python para importar. O catálogo também distingue skills de snippets e scripts, que contêm código reutilizável.

Há duas rotas de seleção: relevância do pedido frente à descrição e menção explícita com `@nome-da-skill`. Por exemplo, pedir features com entidade e data de referência pode sugerir a skill correspondente; a menção explicita a escolha, mas é preciso conferir o que foi efetivamente carregado. Recursos adicionais são lidos conforme referência e necessidade, não necessariamente a pasta inteira. Um briefing manual em `hub_prompts` exige anexo ou envio; não vira skill por estar no catálogo.

O catálogo inclui Micromodelos e encaminha aos runners sintéticos documentados. Na manutenção, confira catálogo e rotas antes de repetir contagens. O índice explica guardrails, templates e aprovações, mas a escala de enforcement vigente pertence a `policy.json`: nível alvo não prova execução atual. Ler o catálogo não concede acesso ao workspace, não chama helpers nem confirma resultado analítico.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../skills/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0138](#doc-0138) · [Próximo: D0140](#doc-0140) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0140"></a>
<a id="doc-0140"></a>
### D0140 — Skill de análise de safra

A skill `hub-ml-analise-safra` orienta quem compara coortes definidas pela entrada, como contratos originados em meses diferentes. Antes de calcular, fixa entidade, origem, observação, data de corte, evento, numerador e denominador. MOB significa mês desde a origem; sua convenção para mês parcial precisa ser declarada. O fluxo exige matriz safra por MOB, células imaturas ausentes, volumes e taxas com denominador, comparações na mesma idade e separação de mix, calendário e deterioração.

Por exemplo, não se pode somar percentuais acumulados com `cumsum` nem comparar a safra recente no MOB 3 com uma antiga no MOB 12. O texto recomenda `hub_snippets.ml.vintage_analysis` e um template de relatório, mas esses recursos só ajudam se forem aplicáveis e usados. Diferença descritiva entre safras não demonstra causa. Uma referência normativa exige fonte e revisão jurídica, não basta citar técnica ou sigla.

A policy atual mantém esta skill em L0, orientação textual, com alvo L3, execução canônica comprovável; a rota implementada não promove o nível. O perfil `MONTHLY_BINARY_PILOT_V1` exige roster completo, dados sintéticos e verificação com tabela-oráculo externa; cobertura incompleta não admite taxa provisória. O arquivo não calcula curva nem comprova uso no Databricks por sua leitura.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-analise-safra/SKILL.md](../../skills/hub-ml-analise-safra/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0139](#doc-0139) · [Próximo: D0141](#doc-0141) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0141"></a>
<a id="doc-0141"></a>
### D0141 — README da execução sintética de safra

Este README documenta a pasta `scripts` da skill de safra para mantenedores que avaliam um piloto, sem declarar a skill produtiva em nível novo. Ele nomeia `preflight.py`, `run.py` e `verify.py`: checagem de entradas, cálculo canônico e verificação de um Receipt, comprovante estruturado da execução. O escopo implementado é mensal e binário, com entradas fechadas no `input.schema.json`.

A receita prepara contratos mensais sintéticos, roster completo e resultado esperado independente. O runner retorna estruturas em memória; sua interface de linha de comando imprime JSON, formato estruturado de dados. Já `verify.py` expõe uma função Python, sem comando equivalente: abrir o arquivo não chama a verificação. Denominador fixo e cobertura precisam ser preservados; uma observação ausente não se torna zero. Os modos `EVENT` e `CUMULATIVE` exigem tratamentos diferentes para evitar acumular novamente um estoque já acumulado.

A policy permanece L0, orientação textual. A rota implementada e seus comprovantes não promovem esse nível. Trimestre, junções Spark e conclusão L4 ficam fora do perfil. Ao manter a receita, confira contrato, manifesto e oráculo juntos. Hashes não autenticam pessoa, e um resultado sintético não homologa uma análise real nem autoriza publicação.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-analise-safra/scripts/README.md](../../skills/hub-ml-analise-safra/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0140](#doc-0140) · [Próximo: D0142](#doc-0142) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0142"></a>
<a id="doc-0142"></a>
### D0142 — Template de relatório de safras

O template `relatorio_safra.md` oferece estrutura editável para quem precisa comunicar uma análise por coortes depois do cálculo. Ele reserva resumo executivo, curvas de maturação, mapa de calor, tabela comparativa, alertas e recomendações. MOB é mês desde a origem da safra; as colunas MOB-6 e MOB-12 só são comparáveis quando ambas as coortes maturaram até essas idades.

Imagine contratos originados em janeiro e março. Antes de preencher “pior safra”, o analista precisa definir evento, exposição, numerador e denominador, reconciliar quantos contratos são observáveis em cada MOB e marcar a célula de março ainda imatura como ausente. O campo `Ever-bad` deve receber a definição real do evento cumulativo, não uma taxa calculada por somar percentuais. No perfil de roster fixo, cobertura incompleta mantém taxa ausente; não substitua o denominador pelos observados. Sem corte, a maturidade formal permanece pendente.

O template não traz dados medidos, algoritmo ou critério universal de alerta. Os blocos de safra, calendário e maturação registram padrões observados e hipóteses; não identificam causalidade por comparação descritiva. O nível atual da skill na policy é L0, orientação textual; preencher este relatório não o eleva.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-analise-safra/templates/relatorio_safra.md](../../skills/hub-ml-analise-safra/templates/relatorio_safra.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0141](#doc-0141) · [Próximo: D0143](#doc-0143) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0143"></a>
<a id="doc-0143"></a>
### D0143 — Skill de auditoria de skills e outputs

A skill de auditoria serve a revisores de implementação de outra skill ou do output que ela produziu. O modo IMPLEMENTAÇÃO examina pacote, contrato, recursos e testes; OUTPUT requer skill produtora, pedido original e artefato entregue. O preflight, verificação anterior à análise, bloqueia julgamento substantivo se a entrada necessária falta. Depois, o runner registra evidência e Receipt, comprovante estruturado da execução da auditoria.

A escada de evidência distingue recurso citado, localizado, lido, importado, chamado e concluído. Por exemplo, um notebook com `postflight=PASS` salvo mostra estado persistido; só execução do verificador canônico aplicável permite `PASS_REVERIFIED`. Sem adapter de verificação, declare `NOT_REVERIFIED`, ainda que o relatório esteja completo. O Receipt da auditoria não autentica a execução da skill produtora e não substitui seus próprios controles.

A policy vigente define L3, execução canônica com Receipt, em rollout `audit`. Esse modo não bloqueia homologação por si; preflight e runner ainda podem barrar a auditoria quando requisitos falham. A skill pede achados com arquivo, evidência, impacto, correção e aceite; severidade crítica não deve ser compensada por média. Ler o `SKILL.md` não executa auditoria nem valida um artefato específico.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-auditoria-skills/SKILL.md](../../skills/hub-ml-auditoria-skills/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0142](#doc-0142) · [Próximo: D0144](#doc-0144) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0144"></a>
<a id="doc-0144"></a>
### D0144 — Checkpoints por skill para auditoria

Este arquivo é um conjunto de pistas locais para quem audita uma das skills do Hub. Começa por descobribilidade do `SKILL.md`, frontmatter, links, scripts, exemplos, segurança e handoff; depois lista riscos particulares de EDA, safra, baseline, pipeline e outras skills. EDA significa análise exploratória de dados. As pistas ajudam a formular testes, mas não são padrão oficial Databricks nem substituem o contrato atual da produtora.

Para uma análise de safra, por exemplo, o checklist lembra conferir MOB, mês desde a origem, data de corte, denominador, células imaturas e comparação na mesma idade. A presença das palavras “MOB” e “denominador” num relatório não demonstra que os cálculos respeitaram essas regras: o auditor precisa ler dados, código e evidência disponíveis. Para explicabilidade, o arquivo lembra que SHAP, atribuição de contribuição do modelo, não fornece percentual causal da decisão.

A própria introdução manda confrontar `SKILL.md` vigente e artefato real. Checkpoint pode ser inaplicável a determinada tarefa; a ausência de item irrelevante não vira falha automática. O template não executa testes nem emite veredito, e a policy da skill auditora permanece L3, runner canônico com Receipt (comprovante de execução), em rollout `audit`, medição sem veto automático por esse modo, independentemente deste texto.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-auditoria-skills/templates/checkpoints_por_skill.md](../../skills/hub-ml-auditoria-skills/templates/checkpoints_por_skill.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0143](#doc-0143) · [Próximo: D0145](#doc-0145) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0145"></a>
<a id="doc-0145"></a>
### D0145 — Template de relatório de auditoria

O template de laudo ajuda o auditor de outputs a registrar o que examinou: notebook, skill produtora, data, células, linhas, evidência, notas e ações. A matriz do Skill Enforcement Framework (SEF), estrutura de verificação do Hub, pede para cada recurso estados separados — citado, localizado, lido, importado, chamado e concluído — com fonte e aplicabilidade. Também distingue nível atual da policy de nível alvo, que é plano, e estado persistido de reverificação independente.

Num output que contém `postflight=PASS`, o auditor pode registrar o valor observado, mas não preencher “reverificado” sem chamar o verificador canônico pertinente. O quadro de dez dimensões recebe evidências objetivas, julgamento justificado, score de zero a dez, semáforo, eventual veto e prescrições priorizadas. Um radar visual é opcional; não transforma nota em prova técnica. Placeholders recebem fatos verificados ou estado não avaliado. Pesos exigem aprovação no caso; vetos e verificadores prevalecem sobre médias.

Este template não executa preflight, runner ou verificador, nem prova que o notebook foi rodado. A skill auditora tem L3, runner canônico com Receipt (comprovante de execução), em rollout `audit`, medição sem veto automático por esse modo, na policy atual; o laudo preenchido ainda precisa separar conformidade mecânica, julgamento e limitações. O contrato do produtor continua sendo a referência do comportamento esperado.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-auditoria-skills/templates/relatorio_auditoria.md](../../skills/hub-ml-auditoria-skills/templates/relatorio_auditoria.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0144](#doc-0144) · [Próximo: D0146](#doc-0146) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0146"></a>
<a id="doc-0146"></a>
### D0146 — Rubrica universal de auditoria

A rubrica orienta o auditor a justificar notas de zero a dez em dez dimensões, da completude à aderência ao ecossistema. Cada faixa tem âncora descritiva; a nota deve citar célula, contagem, trecho ou teste observado. O arquivo distingue avaliação qualitativa de evidência: falta de prova é NÃO AVALIADO; dimensão inaplicável exige redistribuir peso explicitamente. Um score agregado não neutraliza falha crítica nem substitui o contrato da skill produtora.

Para um notebook de baseline, o auditor pode verificar split, métrica e registro de experimento antes de julgar rigor e rastreabilidade. A dimensão D5 exige os bindings e artefatos do perfil escolhido, com request, Receipt, links e versões conforme aplicável; ausência de logging opcional não reduz nota. A seção visual exige apresentação pertinente e legível, sem biblioteca ou decoração obrigatória. Fórmulas de score, critérios e evidência precisam ser aplicados ao artefato real, sem preencher a nota por aparência.

O template é recurso customizado do Hub. Não roda notebook, não executa verificador e não emite aprovação por si. A skill auditora usa policy L3, runner canônico com Receipt (comprovante de execução), em rollout `audit`, medição sem veto automático por esse modo, mas a presença desta rubrica não reverifica Receipt de nenhuma skill produtora.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-auditoria-skills/templates/rubrica_universal.md](../../skills/hub-ml-auditoria-skills/templates/rubrica_universal.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0145](#doc-0145) · [Próximo: D0147](#doc-0147) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0147"></a>
<a id="doc-0147"></a>
### D0147 — Skill de baseline de modelos

A skill de baseline ensina a estabelecer uma régua reproduzível antes de otimizar modelo. O consumidor define decisão, custo dos erros, unidade, target, horizonte, instante de predição, população, split e métrica; sem target ou contrato temporal, não treina suite supervisionada como pronta. As suites cobrem classificação/regressão, série temporal, clustering, ranking, survival e anomalia, com referência trivial apropriada para cada uma.

Num problema de cancelamento, o split fora do tempo deve manter clientes relacionados no grupo correto e o teste final intocado durante seleção. Preprocessamento e calibradores são ajustados no treino. A comparação usa mesma população e métrica, reporta incerteza quando material e separa tracking de promoção. MLflow é a ferramenta indicada para parâmetros, versões, métricas e artefatos, quando o ambiente permitir; nenhum alias de produção nasce automaticamente de um run.

A policy atual mantém esta skill em L0, orientação textual, embora o alvo seja L4, conclusão condicionada a validação final. O perfil `BINARY_TEMPORAL_LOCAL_V1` calcula uma classificação mensal sintética; tracking pessoal exige autorização e registro de efeito separados. Suites mais amplas continuam orientação metodológica, sem Receipt por aproximação. Antes de executar, conferir bibliotecas, compute e permissões; uma métrica bonita sem split válido não sustenta a decisão.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/SKILL.md](../../skills/hub-ml-baseline-ml/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0146](#doc-0146) · [Próximo: D0148](#doc-0148) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0148"></a>
<a id="doc-0148"></a>
### D0148 — Template de perfil de anomalias

O template de anomalias serve para documentar uma detecção depois que método, população e scores existirem. Campos de algoritmo, volume, limiar, distribuição dos scores, amostras, padrões, métricas condicionais a labels, evolução temporal e ações tornam a decisão revisável. LOF significa fator local de outlier; é apenas uma das opções listadas. Um score extremo assinala observação atípica segundo o método, não fraude ou erro comprovado.

Imagine priorizar 50 alertas para revisão humana. O limiar precisa relacionar capacidade operacional, prevalência conhecida e custo de falso positivo; o percentil 95 mostrado é estatística descritiva, não limiar aprovado. Precision@50 mede a fração de casos relevantes entre os 50 primeiros, mas só pode ser preenchida se houver rótulos confiáveis. IDs de exemplos e características individuais pedem cuidado com informações pessoais identificáveis; uma tabela de placeholders não autoriza expô-las.

O bloco executivo contém frases com números entre colchetes, não achados observados. Compare mês, base e amostragem antes de afirmar tendência, e registre a validação manual real se ocorreu. A skill de baseline permanece L0, orientação textual, na policy; preencher este modelo de relatório não gera Receipt, comprovante de execução, nem homologa resultados.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/anomaly_profiling.md](../../skills/hub-ml-baseline-ml/templates/anomaly_profiling.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0147](#doc-0147) · [Próximo: D0149](#doc-0149) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0149"></a>
<a id="doc-0149"></a>
### D0149 — Template de perfil de clusters

Este template apoia quem precisa descrever segmentos obtidos por clustering, método de agrupar observações por semelhança sem target supervisionado. Reserva tamanho por grupo, participação na base, silhouette, algoritmo, características, estabilidade e ação sugerida. Silhouette é medida de separação e coesão relativa; um valor preenchido deve vir de cálculo sobre o recorte e método usados, não de um nome sugestivo para o cluster.

Num perfil de clientes, uma média de renda do grupo versus média global pode mostrar diferença descritiva. Antes de nomear “alto valor”, confira denominador, dispersão, variáveis sensíveis e estabilidade por período ou reamostragem. A reamostragem exige fração, repetições, semente e limiar justificados no estudo. Alinhe rótulos dos clusters antes de comparar concordância: seus números podem permutar. Também lista estatística F e importância relativa, que precisam de método e interpretação coerentes.

O nome de cluster não explica causa, não demonstra que uma ação de negócio funcionará e não comprova validade fora da amostra. Os campos `[N]`, `[X]` e texto executivo são placeholders. A skill de baseline está em L0, orientação textual, na policy; preencher o relatório não executa nem valida a segmentação.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/cluster_profiling.md](../../skills/hub-ml-baseline-ml/templates/cluster_profiling.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0148](#doc-0148) · [Próximo: D0150](#doc-0150) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0150"></a>
<a id="doc-0150"></a>
### D0150 — Template para comparar aprendizado profundo e LightGBM

O template compara DL, aprendizado profundo, com LightGBM, biblioteca de árvores de gradiente, em dados tabulares. Seu consumidor deve registrar baseline reproduzível, métrica, tempo de treino e inferência, custo operacional, interpretabilidade e manutenção antes de recomendar arquitetura. Métricas como `AUC`, área sob curva de discriminação, e `KS`, distância máxima entre distribuições de score, só entram quando pertinentes e medidas; o quadro atual pede métrica primária, baseline e incerteza.

Imagine um modelo neural ligeiramente acima de LightGBM no mesmo teste. A decisão exige comparar os dois no mesmo split e objetivo, declarar incerteza e custo de servir e manter. O texto pede critério de ganho definido pelo caso, sem cardinalidade mínima ou ganho fixo universal. Tracking no MLflow depende de rota e autorização; registro de modelo e promoção exigem decisão separada.

O template contém placeholders de comparação e recomendação que devem receber os resultados do caso; sem benchmark comparável, o ganho é NÃO DEMONSTRADO. Ele não treina modelos, não valida GPU, processador gráfico, disponível nem autoriza deploy. A policy da skill de baseline continua L0, orientação textual, independentemente de uma justificativa preenchida.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/dl_vs_lgbm_justificativa.md](../../skills/hub-ml-baseline-ml/templates/dl_vs_lgbm_justificativa.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0149](#doc-0149) · [Próximo: D0151](MT-atlas-04.md#doc-0151) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
