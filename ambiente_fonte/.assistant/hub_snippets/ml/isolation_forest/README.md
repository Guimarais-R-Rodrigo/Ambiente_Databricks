# `isolation_forest` — encontrar observações incomuns para investigar

<!-- readme-objeto: 0.1.0-candidata -->

Isolation Forest ajuda a ordenar observações pelo quanto são fáceis de separar das demais. No Hub, cada observação recebe uma pontuação (score), que permite ordená-las (ranking); um corte gera a marca de anomalia. Um perfil descritivo complementa essa informação para apoiar investigação, sem transformar “incomum” em “fraude”.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Detecção não supervisionada de observações atípicas por árvores de isolamento. |
| Para que serve? | Priorizar casos para revisão quando não há um rótulo confiável do evento. |
| Use quando... | As características numéricas e a população de referência fizerem sentido juntas. |
| Evite quando... | Precisar concluir fraude, causa ou probabilidade de evento apenas pelo score. |
| Precisa de... | DataFrame pandas, colunas selecionadas e um corte de investigação justificado. |
| Entrega... | Scores, rótulos, modelo, transformador e estatísticas; perfil separado. |

Leia a [implementação](isolation_forest.py) ou a [demonstração](exemplo_isolation_forest.py). O módulo exige MLflow já na importação, mesmo quando o exemplo usa `log_mlflow=False`. Consulte dependências e efeitos nas seções 7 e 9.

## 1. O que é?

Uma observação atípica é diferente das demais segundo as características e a população escolhidas. Uma movimentação alta, por exemplo, pode ser rara numa carteira e comum em outra. A raridade precisa ser interpretada no contexto.

Isolation Forest constrói árvores com divisões aleatórias. Observações isoladas em poucos passos recebem maior indicação de anomalia; a comparação entre várias árvores reduz a dependência de um único caminho aleatório. O [guia de detecção de outliers](https://scikit-learn.org/stable/modules/outlier_detection.html) apresenta esse mecanismo. “Não supervisionado” significa que o ajuste não precisa de uma coluna dizendo quais casos são fraudes ou erros.

As funções auxiliares do Hub são `train_isolation_forest` e `profile_anomalies`. A primeira ajusta e pontua a própria base recebida; a segunda descreve casos já marcados. Ela não é uma rotina pronta de monitoramento contínuo.

## 2. Que problema este recurso resolve?

A pergunta é: “Entre estas observações, quais merecem revisão por destoarem do conjunto?”. O resultado pode orientar uma fila de investigação de qualidade ou de comportamento incomum. A fila é uma proposta analítica; a confirmação do problema exige evidência adicional e critério de negócio.

## 3. Quando faz sentido usar?

Pode ajudar numa exploração inicial sem rótulos confiáveis, quando há suspeita de registros incomuns e uma população de comparação razoavelmente homogênea. Também pode complementar uma revisão de qualidade: um valor pode ser válido isoladamente e estranho em combinação com outros.

É necessário escolher características que representem o comportamento relevante. Misturar segmentos muito diferentes pode fazer o algoritmo priorizar a diferença entre segmentos em vez de anomalias dentro deles. Compare essa decisão com a possibilidade de analisar populações separadas.

## 4. Quando não usar?

Não use o rótulo `-1` como confirmação de fraude ou motivo automático para bloquear um cliente. Um cliente legítimo de alto volume pode ser raro e receber score extremo; esse é um contraexemplo de código funcionando e decisão errada.

Se há rótulos confiáveis e o objetivo é prever um evento específico, avalie uma abordagem supervisionada. Se o problema é uma regra conhecida, como idade impossível ou duplicidade de identificador, uma verificação explícita pode responder de forma mais direta. Não substitua uma regra clara por raridade estatística sem motivo.

## 5. Como funciona, intuitivamente?

A função seleciona `feature_cols`, converte seus valores para uma matriz local e, por padrão, ajusta `StandardScaler`, que centraliza e redimensiona as colunas. Em seguida, ajusta o estimador, obtém `decision_function` e `predict` sobre a mesma base e calcula os resumos.

`contamination` ajuda a definir o **corte** dos rótulos; não informa quais linhas são raras nem revela a prevalência real do evento. A ordenação depende dos dados e das árvores. Na [API do scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html), a função de decisão é o score bruto menos um deslocamento; valores negativos são marcados como outliers. Empates e discretização podem impedir que a fração final seja exatamente a solicitada.

## 6. Exemplo de situação

Considere clientes fictícios de um mesmo perfil e período, descritos por frequência de uso e medidas agregadas de movimentação. A equipe consegue revisar um grupo pequeno por rodada e deseja começar por observações muito diferentes das usuais.

O método produz uma ordenação; o corte determina quais observações recebem a marca inicial. A capacidade de revisão pode orientar um corte investigativo declarado, mas não deve ser apresentada como estimativa comprovada de fraude. Uma amostra dos casos marcados e dos não marcados ajuda a avaliar a utilidade da fila. Este cenário é ilustrativo, sem métricas de eficácia executadas.

## 7. O que você precisa antes de usar?

Forneça um `pandas.DataFrame` não vazio e uma lista de colunas numéricas apropriadas. Verifique nulos, infinitos, codificação, grão e período antes da chamada; o wrapper não implementa uma política completa de limpeza. Como usa os valores da matriz, preserve a ordem das colunas ao reutilizar o modelo.

A anotação da assinatura não é uma validação dos dados. Além de pandas, NumPy e scikit-learn, o arquivo contém `import mlflow` no topo, sem proteção opcional. Por isso `log_mlflow=False` não torna o pacote dispensável para importar este objeto.

Neste wrapper, use `contamination` numérico no intervalo `(0, 0.5]`, compatível com a API subjacente. Embora o scikit-learn ofereça `"auto"`, o código desta pasta multiplica o argumento e calcula percentis como número; não oferece suporte correto à opção textual. `max_samples="auto"` é outro parâmetro e não tem essa restrição.

## 8. O que este recurso entrega?

`train_isolation_forest` retorna um dicionário:

| Chave | Significado |
|---|---|
| `scores` | Função de decisão: menor, especialmente negativo, indica maior anomalia relativa. |
| `labels` | `-1` para caso marcado e `1` para não marcado segundo o corte. |
| `model` | Estimador ajustado, reutilizável com a mesma preparação. |
| `scaler` | Transformador ajustado ou `None`, conforme a configuração. |
| `stats` | Contagens, percentual e resumos dos scores da base ajustada. |

`pct_anomalies` está na escala 0–100; `contamination` usa fração. `stats["score_threshold"]` é um percentil calculado sobre `scores`, não o limiar operacional oficial de `predict`, que usa zero na função de decisão. Não construa uma nova regra presumindo equivalência exata entre os dois.

`profile_anomalies` devolve até `top_n` linhas com `index`, `anomaly_score`, `most_anomalous_feature` e `max_z_score`. O último descreve o maior desvio absoluto padronizado: a distância de uma característica à média da base, medida em desvios-padrão. Um valor 3 indica uma distância de três desvios-padrão na característica selecionada; não significa probabilidade de fraude nem explica qual divisão da árvore isolou o caso. É uma comparação descritiva, não uma explicação causal ou atribuição do modelo. Sem casos marcados, a implementação pode retornar um DataFrame vazio sem essas colunas.

## 9. Como usar este recurso no Hub?

Com a raiz `.assistant` visível ao Python, use os exports da [fachada](__init__.py): `train_isolation_forest` e `profile_anomalies`. O [notebook](exemplo_isolation_forest.py) demonstra o treino e a sensibilidade ao corte com dados sintéticos; ele importa a função de perfil, mas não a chama. Não confunda importação com demonstração de todas as funções.

O helper treina e pontua localmente; não distribui o ajuste no Spark. Nas chamadas do notebook, o registro explícito é desligado. Na função, o padrão é `log_mlflow=True`, que registra parâmetros e métricas e pode afetar um run existente ou a configuração de tracking. O wrapper não gerencia explicitamente esse ciclo nem salva o modelo por `log_model`.

Não há escrita de tabela no exemplo. Ainda assim, conferir recursos e logging é necessário: desligar o registro do helper não desliga autologging externo, conforme a [documentação Databricks](https://docs.databricks.com/aws/en/mlflow/databricks-autologging). Para novas observações, reaplique o `scaler` retornado, quando houver, e use o modelo; não ajuste novamente o transformador apenas na base nova.

## 10. Decisões e configurações que mais importam

`contamination=0.01` define uma referência de corte de 1%, não uma descoberta. Faça análise de sensibilidade e justifique o uso investigativo. `n_estimators=200`, `max_samples="auto"` e a semente 42 controlam a construção do conjunto; `n_jobs=-1` permite ao estimador usar todos os núcleos disponíveis nessa execução.

`scaler="standard"` ativa a padronização. Qualquer outro texto cai no ramo sem padronização; um erro de digitação não é rejeitado. Use conscientemente `"standard"` ou `"none"`. Não ensine padronização como requisito universal de Isolation Forest: a justificativa depende da representação e do fluxo, não de uma obrigação geral de métodos baseados em árvores.

No perfil, `top_n=50` limita os casos retornados. As mesmas linhas, na mesma ordem, precisam corresponder aos arrays `scores` e `labels`; alinhar apenas pelo tamanho não comprova que sejam as observações corretas.

## 11. Limitações, riscos e armadilhas

Uma anomalia pode ser erro, mudança legítima ou caso raro relevante. O algoritmo não distingue essas causas. Scores não são probabilidades e a quantidade marcada não estima automaticamente prevalência real. Rótulos derivados do método também não se tornam verdade de referência por serem usados em outro treinamento.

O perfil usa médias e desvios globais da própria base, que podem ser influenciados pelos extremos. Sua “característica mais anômala” não identifica necessariamente o motivo de o estimador ter isolado a linha. O wrapper não mede a proporção de alertas confirmados (precisão), a proporção dos eventos reais encontrados (recall), estabilidade temporal ou valor econômico da investigação.

A matriz e suas transformações precisam caber na memória local. Valores constantes, populações heterogêneas e mudança de distribuição exigem checagens específicas. Um teste sintético com casos muito separados é uma demonstração, não estimativa da eficácia em dados reais.

## 12. Quais são as alternativas?

Regras de qualidade são preferíveis quando o erro é conhecido. Um modelo supervisionado, como [XGBoost](../train_xgboost/README.md), atende a uma pergunta diferente quando há resposta rotulada. O [autoencoder do Hub](../autoencoder_anomaly/autoencoder_anomaly.py) é outra hipótese de modelagem de anomalias e exige conhecer suas próprias premissas e dependências.

Para comparar distribuições de períodos, [drift_detection](../drift_detection/drift_detection.py) é mais próximo da pergunta do que marcar observações individuais. Não confunda essas duas escalas de análise.

## 13. Como saber se o resultado faz sentido?

Confira que `labels == -1` corresponde a `scores < 0` no estimador usado, que contagens reconciliam com o tamanho da base e que não houve reordenação entre treino e perfil. Inspecione casos conhecidos e uma amostra de ambos os lados do corte.

Varie o corte de maneira declarada e observe quem entra na fila. Se quase todos os casos escolhidos pertencem ao mesmo segmento legítimo, investigue a população de referência. Com rótulos externos confiáveis, avalie qualidade da investigação fora da base usada para ajustar; sem eles, registre que utilidade e prevalência continuam incertas.

## 14. Arquivos relacionados e próximos passos

A [implementação](isolation_forest.py) contém treino, cálculo das pontuações e perfil; a [fachada](__init__.py) lista as funções e constantes públicas; o [notebook](exemplo_isolation_forest.py) explora o corte. O [guia da coleção](../../README.md) explica importação e categorias; o [Manual](../../../MANUAL_TECNICO.md#catalogo-helpers) mantém o catálogo integrado. Antes de usar, defina o que será investigado e como os casos serão confirmados.

## 15. Referências

Comportamento conferido na implementação da base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. Para conceito e score, foram consultados em 12/09/2026 o [guia de outliers](https://scikit-learn.org/stable/modules/outlier_detection.html) e a [API IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html); para efeitos da sessão, a [documentação de autologging](https://docs.databricks.com/aws/en/mlflow/databricks-autologging).

A redação inicial e a revisão de fechamento R02 são autorrevisões, não auditorias independentes. Em 12/09/2026, a [execução suplementar da R02](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982) aprovou testes de treino, perfil e empates com scikit-learn e MLflow reais, sem habilitar o logging do helper. Esse resultado é evidência histórica identificada: o ambiente local do fechamento continua sem MLflow e não repete esses testes usando um módulo falso. Não houve teste de tracking remoto ou homologação Databricks. Saídas históricas do notebook não são novas execuções desta documentação.
