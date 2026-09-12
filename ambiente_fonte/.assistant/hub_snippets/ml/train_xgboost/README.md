# `train_xgboost` — aprender a prever com árvores, sem confundir treino com validação

<!-- readme-objeto: 0.1.0-candidata -->

XGBoost combina árvores de decisão para aprender relações entre características e uma resposta conhecida. Este recurso do Hub organiza um primeiro treinamento, sua avaliação em validação e, quando solicitado, o registro de parâmetros e métricas no MLflow, sistema de acompanhamento de experimentos.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper: uma função que prepara e chama a biblioteca XGBoost. |
| Para que serve? | Construir uma referência preditiva para classificação ou regressão. |
| Use quando... | Houver dados tabulares preparados, resposta conhecida e uma partição de validação pertinente. |
| Evite quando... | Precisar descobrir causas ou entregar um pipeline completo de produção. |
| Precisa de... | Matrizes de treino/validação, respostas alinhadas e bibliotecas compatíveis. |
| Entrega... | Modelo ajustado e dicionário de métricas; logging opcional, habilitado por padrão. |

A [implementação](train_xgboost.py) e a [fachada pública](__init__.py) definem a API. Antes de abrir o [notebook](exemplo_train_xgboost.py), observe que ele instala uma biblioteca e reinicia o Python. Suas chamadas desligam o logging explícito do helper; confira também o autologging da sessão, conforme a seção 9.

## 1. O que é?

Uma árvore de decisão divide os exemplos por perguntas sobre suas características: valores acima de um corte seguem um caminho, os demais seguem outro. Em vez de depender de uma árvore isolada, o *gradient boosting* acrescenta árvores sucessivamente, buscando melhorar a previsão do conjunto segundo uma função de perda, que mede o erro. O XGBoost implementa esse processo com controles de complexidade e eficiência. Essa é a ideia apresentada no [tutorial de árvores impulsionadas](https://xgboost.readthedocs.io/en/stable/tutorials/model.html).

No Hub, `train_xgboost_baseline` não é a biblioteca inteira. É um recorte que recebe dados já preparados, escolhe uma tarefa, treina e calcula algumas métricas. *Baseline* significa referência inicial para comparação, não modelo aprovado ou necessariamente a solução mais simples possível.

## 2. Que problema este recurso resolve?

A pergunta típica é: “As características que conhecemos antes da decisão ajudam a prever a resposta em dados separados do treino?”. O resultado ajuda a decidir se vale aprofundar a modelagem e comparar outras configurações. Ele não escolhe campanhas, concede crédito, define um corte operacional nem mede o efeito de uma intervenção.

## 3. Quando faz sentido usar?

É uma opção de investigação para classificação binária, como resposta ou não resposta a uma campanha; classificação multiclasse, quando a resposta é uma entre várias classes; e regressão, quando se prevê uma quantidade numérica. O código oferece esses três modos por `task`.

Faz sentido comparar o resultado com uma referência mais simples e com outros modelos sob os mesmos dados, horizonte e critérios. Relações não lineares e combinações entre variáveis podem ser relevantes; isso é uma razão para testar árvores, não uma garantia de que ganharão. Dados tabulares significam aqui uma linha por unidade observada e colunas com características disponíveis no momento da previsão.

## 4. Quando não usar?

Não use uma boa métrica para responder “a campanha causou esta compra”. O helper aprende associação preditiva e não identifica efeito causal. Também não é um leitor direto de imagens, áudios ou documentos brutos: essas entradas exigem representação apropriada e um desenho que este wrapper não fornece.

Um contraexemplo é treinar propensão com uma coluna preenchida somente depois da compra. O código pode executar e produzir uma avaliação atraente, mas a variável não existiria na decisão real. Corrija disponibilidade temporal e preparação antes do treino; trocar o algoritmo não resolve esse vazamento.

## 5. Como funciona, intuitivamente?

A função começa conferindo a tarefa, a paciência de parada e algumas condições dos rótulos. Copia `DEFAULT_PARAMS`, adapta objetivo e métrica à tarefa e aplica `params_override`. Depois cria um `XGBClassifier` ou `XGBRegressor` e chama `fit` com os dados de validação.

A *parada antecipada* acompanha uma métrica de validação e interrompe o crescimento após um número de rodadas sem melhora. Por isso, a validação participa da escolha do modelo: não é um teste final intocado. A [interface scikit-learn do XGBoost](https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html) explica esse mecanismo. A função calcula as métricas previstas para `task`, registra-as se habilitado e retorna o modelo.

## 6. Exemplo de situação

Imagine uma campanha fictícia já encerrada. Cada linha representa um contato, com atributos disponíveis antes do envio e uma resposta 0/1 observada após um horizonte definido. Uma primeira parte histórica serve para aprender e outra para escolher configurações; um período posterior fica reservado para teste final.

O helper poderia treinar a classificação binária e devolver AUC e Gini de validação. A interpretação seria “quanto o modelo ordena respondedores acima de não respondedores nessa população”, não “quanto a campanha aumentará vendas”. Este cenário não é uma execução nem uma promessa de métrica. Havendo contatos repetidos por cliente, reveja também a dependência entre linhas e a estratégia de separação.

## 7. O que você precisa antes de usar?

`X_train` e `X_val` são matrizes de características, com mesmas colunas, ordem e significado. `y_train` e `y_val` contêm as respostas na mesma ordem das respectivas linhas. A assinatura usa arrays NumPy; categorias e outros formatos aceitos pela biblioteca dependem de preparação e versão. O wrapper não cria um pipeline de transformação nem garante suporte a qualquer DataFrame recebido.

Para classificação binária, use a convenção 0/1 e confirme a classe positiva. O helper exige duas classes em treino e validação. No modo multiclasse, exige ao menos duas classes no treino e não aceita classes de validação ausentes no treino; a codificação ainda precisa satisfazer o estimador subjacente. Conjuntos vazios são recusados.

São necessários NumPy, scikit-learn e XGBoost. MLflow pode faltar somente quando `log_mlflow=False`: com logging habilitado, a checagem de sua ausência ocorre **depois do treinamento**. Confirme isso antes de gastar compute. Ajuste transformações apenas no treino e aplique a mesma preparação nos demais conjuntos; a [documentação de prevenção de vazamento](https://scikit-learn.org/stable/common_pitfalls.html) detalha esse cuidado.

## 8. O que este recurso entrega?

O retorno é a tupla `(model, metrics)`, não um relatório nem um pipeline implantado.

| Tarefa | Chaves em `metrics` | Leitura |
|---|---|---|
| `binary` | `auc_val`, `gini_val` | Ordenação na validação; Gini calculado como `2 × AUC − 1`. |
| `multiclass` | `log_loss_val`, `accuracy_val` | Perda das probabilidades e proporção de classes acertadas. |
| `regression` | `rmse_val` | Raiz do erro quadrático médio, na unidade da resposta. |

As métricas saem numéricas, sem formatação percentual. O código binário usa `predict_proba(X_val)[:, 1]`; não confunda esse score com probabilidade calibrada por um procedimento adicional. A função não calcula incerteza das métricas, importância de variáveis, ganho financeiro ou métricas de teste independente. Consulte a [implementação](train_xgboost.py) para o cálculo exato de cada retorno.

## 9. Como usar este recurso no Hub?

Depois de tornar a raiz `.assistant` confirmada visível ao Python, importe `train_xgboost_baseline` de `hub_snippets.ml.train_xgboost`. A preparação do caminho está no [guia da coleção](../../README.md); o [notebook](exemplo_train_xgboost.py) contém um cenário sintético completo. Não use `%run` para carregar o módulo.

O notebook executa `%pip install xgboost` e `%restart_python`: isso altera o ambiente da sessão e apaga seu estado Python. Leia a preparação antes de executar. Nas chamadas demonstradas, `log_mlflow=False` desliga apenas `mlflow.log_params` e `mlflow.log_metrics` realizados pelo wrapper. Não desliga autologging que já esteja ativo.

Com logging habilitado, confira destino do experimento, permissão e ciclo de vida do run, que não são geridos explicitamente pela função. Ela não registra o modelo por chamada explícita a `log_model`; o comportamento de autologging é separado. A [documentação Databricks](https://docs.databricks.com/aws/en/mlflow/databricks-autologging) distingue autologging e registro manual; uma falha histórica no laboratório não prova que todo MLflow seja incompatível com serverless.

## 10. Decisões e configurações que mais importam

`task="binary"` é o padrão. Escolha `multiclass` ou `regression` pela natureza da resposta, não apenas substituindo `objective` em `params_override`. Overrides incompatíveis podem fazer o treino e a avaliação responderem a contratos diferentes.

Os defaults incluem `learning_rate=0.05`, `max_depth=6` e `n_estimators=500`. A taxa de aprendizado controla a intensidade dos acréscimos; profundidade e número de rodadas afetam complexidade e custo. `min_child_weight=5` é um controle ligado à soma de pesos de segunda ordem da perda, não uma promessa de “cinco clientes por folha”. Subamostragem e penalidades também estão em `DEFAULT_PARAMS`.

`early_stopping_rounds=50` define a paciência. Zero impede que o argumento da função acrescente esse parâmetro; um override que já o contenha não é removido. A semente padrão é 42, mas não certifica igualdade bit a bit entre versões, máquinas ou configurações. Defaults são ponto de partida, não valores ótimos universais.

## 11. Limitações, riscos e armadilhas

O treino usa a interface Python do estimador, não uma implementação distribuída Spark. Planeje memória e volume das matrizes locais; o wrapper não coleta nem amostra uma tabela Spark para você. GPU, treino distribuído, ranking e tuning não são fluxos implementados por esta função.

Mesmo numa partição adequada, reutilizar repetidamente a validação para escolher modelos pode tornar seu resultado otimista. A [documentação de previsão](https://xgboost.readthedocs.io/en/stable/prediction.html) também distingue o uso de `best_iteration` entre interfaces; não transporte conclusões da API nativa para a interface usada aqui sem conferir.

Resultados próximos de LightGBM e XGBoost não provam que “o número veio do dado”: ambos podem compartilhar o mesmo vazamento ou viés. Tampouco uma diferença pequena pode ser declarada ruído sem analisar variabilidade e relevância. Os números históricos do notebook foram preservados, mas suas conclusões precisam desses limites.

## 12. Quais são as alternativas?

Uma referência de maioria, média ou um modelo linear adequado pode esclarecer quanto o método acrescenta. Os helpers de [LightGBM](../train_lgbm/train_lgbm.py) e [CatBoost](../train_catboost/train_catboost.py) permitem investigar outras implementações, após conferir seus próprios contratos. A escolha depende de dados, métricas, preparação, interpretabilidade e custo, não de um vencedor universal.

Para separar dados no tempo, examine [split_temporal](../split_temporal/split_temporal.py). Ele complementa o treinamento; não é outro algoritmo preditivo.

## 13. Como saber se o resultado faz sentido?

Confira alinhamento entre linhas e respostas, classe positiva e disponibilidade das variáveis. Compare a mesma população com uma referência simples, registre a partição e reserve o teste final. No binário, recompute AUC com as probabilidades e confira a identidade do Gini; na regressão, confira a unidade do RMSE.

Inspecione a quantidade de rodadas e os parâmetros realmente usados. Uma execução concluída confirma apenas que o caminho testado funcionou. Diferenças entre modelos devem ser estudadas com validação adequada ao problema e custo de decisão, sem escolher automaticamente pela terceira casa decimal.

## 14. Arquivos relacionados e próximos passos

A [implementação](train_xgboost.py) contém o treino e as métricas; a [fachada](__init__.py), os nomes exportados; o [notebook](exemplo_train_xgboost.py), a demonstração e suas saídas históricas. O [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantém a visão integrada. Comece pela preparação dos dados e só então execute o exemplo pertinente.

## 15. Referências

Contrato conferido na implementação, fachada e notebook da base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. Fontes primárias externas, consultadas em 12/09/2026: [árvores impulsionadas](https://xgboost.readthedocs.io/en/stable/tutorials/model.html), [interface de estimadores](https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html), [previsão e parada](https://xgboost.readthedocs.io/en/stable/prediction.html), [vazamento de dados](https://scikit-learn.org/stable/common_pitfalls.html) e [autologging Databricks](https://docs.databricks.com/aws/en/mlflow/databricks-autologging). Cada uma sustenta o assunto ao qual foi associada no texto; não certifica este wrapper inteiro.

Revisão R02: leitura técnica e didática pelo próprio autor. Os testes locais sintéticos da sprint usam XGBoost 3.1.3 e logging desligado; não são as saídas históricas do notebook. Teste no Databricks, teste de tracking remoto e auditoria independente não fazem parte dessa evidência. Aceite humano do piloto permanece separado.
