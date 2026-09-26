# Achados R05 — modelos tabulares

**Data:** 2026-09-12
**Base:** `d9da056c95bf5c4209b2f208de1c9a987580efe7`
**Escopo:** leitura estática dos seis objetos R05 e confronto com documentação primária; testes de runtime são registrados separadamente.

## Achados por objeto

### `lgbm_ranker`

1. A docstring de `evaluate_ranking` anuncia “NDCG@k e MAP@k”, mas a implementação calcula e retorna somente `ndcg_at_<k>`. O README assume NDCG como contrato real; o notebook deve deixar de prometer MAP. Não há alteração funcional nesta sprint.
2. `lgbm_ranker.py` importa `mlflow` sem guarda. Portanto importar o módulo exige MLflow instalado mesmo quando `log_mlflow=False`. Os outros treinadores R05 tratam a importação de MLflow como opcional.
3. `groups` contém tamanhos consecutivos, não IDs. A soma é validada, mas a função não consegue detectar linhas fisicamente atribuídas ao grupo errado.

### `mlp_embeddings`

4. A classe `EmbeddingMLP` oferece `task="binary"` e `task="regression"`, mas `train_embedding_mlp` é exclusivamente binário: instancia o default binário, exige labels 0/1, usa `BCELoss` e seleciona checkpoint por AUC.
5. Consumidores diretos da classe podem passar `emb_dims` com comprimento diferente de `cat_dims`; o construtor usa `zip` e não recusa a divergência. O treinador pronto não expõe esse argumento e usa o caminho default.
6. O notebook dizia que one-hot “não expressa” a relação entre níveis e que árvore necessariamente não aprende proximidade. A formulação é forte demais. Embeddings oferecem uma representação densa compartilhável; a superioridade precisa ser medida contra baselines.

### `optuna_lgbm`

7. A função objetivo real é fixa por tarefa: AUC no binário, `-RMSE` na regressão e `-log_loss` no multiclasse. `metric` só entra como métrica interna do LightGBM no caminho binário; não redefine o valor maximizado pelo Optuna de forma geral.
8. `study.best_params`/`best_params` contém apenas os oito hiperparâmetros sugeridos. Não inclui `objective`, métrica interna, `random_state`, `n_estimators` ou `num_class`; não é uma configuração completa para reconstrução do trial.
9. O espaço sugere `subsample`, mas não define `subsample_freq`. A API LightGBM documenta frequência zero como subsampling desabilitado. Esse eixo pode ser inerte na busca atual.
10. O notebook continha limiar informal de “~30 trials” e comparação hiperbólica entre ganho de feature e tuning. A R05 substitui essas frases por critérios condicionais, sem inventar limiar universal.

### `tabnet_wrapper`

11. `feature_importances_` da implementação `pytorch-tabnet` é importância global derivada da explicação/máscaras sobre o treino e normalizada. Não é SHAP, causalidade nem garantia de estabilidade. A frase histórica de que “nada recebe zero” não é propriedade garantida.
12. O wrapper não valida coerência/positividade de `n_d`, `n_a`, `n_steps` nem expõe `virtual_batch_size`. A biblioteca subjacente decide parte relevante do comportamento e pode variar por versão.

### `train_catboost`

13. A explicação histórica de categorical statistics como “linhas anteriores” foi confundida com ordem temporal. CatBoost usa mecanismos ordenados/permutados para reduzir target leakage; isso não substitui disponibilidade point-in-time das features.
14. `params_override` é aplicado antes de o código fixar `loss_function` e `eval_metric` por `task`; overrides dessas chaves podem ser sobrescritos. `allow_writing_files`, ao contrário, pode ser reabilitado por override e voltar a criar artefatos locais.
15. O wrapper não valida shapes/tipos/cat_features integralmente antes de chamar CatBoost. O exemplo documenta o risco de um ndarray misto virar float e deixar de representar categoria como esperado.

### `train_lgbm`

16. Os defaults definem `subsample=0.8`, mas não `subsample_freq`; com o default LightGBM `subsample_freq=0`, bagging periódico de linhas não está habilitado. A prosa histórica dizia o contrário.
17. O bloco de output histórico dos parâmetros no notebook é abreviado e não contém todas as chaves atualmente iteradas por `DEFAULT_PARAMS_BINARY`. A saída preservada não deve ser usada como inventário completo; a constante e `model.get_params()` são as fontes técnicas.
18. `overfit_gap` é uma convenção local sem limiar de “pequeno/grande”. A R05 remove leitura universal de 0,046 como automaticamente pequeno.
19. `params_override` pode sobrescrever objetivo, métrica e `num_class` sem alterar a lógica de métricas escolhida por `task`, produzindo contratos incoerentes se usado sem conferência.

## Achados transversais

20. Os notebooks instalam dependências sem pin (`%pip install ...`) e reiniciam o Python. Isso é útil como laboratório, mas não é especificação reproduzível de ambiente. O runner da R05 deve registrar versões efetivamente testadas.
21. Resultados numéricos colados nos notebooks são evidência histórica de um cenário sintético, não benchmark entre objetos: datasets, sementes, configurações e objetivos diferem.
22. `log_mlflow=False` desliga as chamadas explícitas de logging dos wrappers, não prova ausência de todo autologging/configuração externa do ambiente.
23. Nenhum dos seis helpers implementa preparação completa, política de produção, teste final, calibração, fairness, aprovação humana ou publicação de modelo. README local não converte baseline em artefato homologado.

## Decisão da sprint

Os achados acima são tratados por documentação, testes de caracterização e correções de prosa. **Nenhuma implementação ou fachada dos seis objetos será modificada na R05.** Problemas que mereçam evolução funcional futura permanecem explicitamente separados da migração documental.
