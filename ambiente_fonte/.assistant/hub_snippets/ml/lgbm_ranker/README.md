# `lgbm_ranker` — ordenar alternativas dentro de grupos com LambdaRank e NDCG

<!-- readme-objeto: 1.0.0 -->

Problemas de ranking não perguntam apenas “qual linha é positiva?”. Eles perguntam “qual item deve aparecer antes dos outros **dentro deste grupo**?”. Este helper treina um LightGBM com objetivo `lambdarank` e calcula NDCG@k por grupo para avaliar a ordem prevista.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper da API nativa `lightgbm.train` para ranking LambdaRank. |
| Para que serve? | Aprender a ordenar itens dentro de consultas, clientes ou outros grupos declarados. |
| Use quando... | O objetivo for ranking relativo e cada linha pertencer a um grupo com mais de uma alternativa. |
| Evite quando... | Precisar de probabilidade calibrada, classificação linha a linha ou não possuir grupos confiáveis. |
| Precisa de... | NumPy, LightGBM e **MLflow disponível já no import** deste módulo. |
| Entrega... | `lightgbm.Booster` e dicionário de NDCG@k; `evaluate_ranking` pode recalcular outros k. |

Consulte a [implementação](lgbm_ranker.py), a [fachada](__init__.py) e o [notebook](exemplo_lgbm_ranker.py). O exemplo instala `lightgbm`, reinicia o Python e usa `log_mlflow=False`; isso não elimina a dependência de import do módulo `mlflow`, que é importado sem guarda na implementação.

## 1. O que é?

Ranking supervisionado aprende uma ordem a partir de sinais de relevância. Um grupo pode ser uma consulta com documentos candidatos, um cliente com ofertas candidatas ou uma solicitação com alternativas. O rótulo diz quão relevante cada item foi considerado **dentro daquele contexto**.

O objetivo `lambdarank` do LightGBM modifica o aprendizado para favorecer métricas de ranking. No Hub, `train_lgbm_ranker` recebe as matrizes, labels e tamanhos dos grupos já preparados, treina e chama `evaluate_ranking`.

## 2. Que problema este recurso resolve?

A pergunta concreta é: “Dentro de cada grupo, o modelo coloca os itens de maior relevância nas primeiras posições?”. Um classificador pode ter boa discriminação global e ainda ordenar mal as alternativas do mesmo cliente; ranking torna o grupo parte explícita do problema.

O helper responde com NDCG, não com taxa de acerto, probabilidade de conversão ou valor econômico. Essas são perguntas diferentes.

## 3. Quando faz sentido usar?

Use quando existem grupos reais e a decisão é relativa: qual oferta mostrar primeiro, qual documento priorizar ou qual item recomendar. Os labels podem representar relevância graduada não negativa, como 0, 1, 2 e 3.

A avaliação faz mais sentido quando a separação entre treino e validação respeita a unidade relevante. Se linhas do mesmo contexto vazarem entre splits, a métrica pode responder a um problema mais fácil que o uso real.

## 4. Quando não usar?

Não use com grupo de uma única alternativa se a pergunta for exclusivamente ordenar: não há comparação interna a aprender. O código aceita tamanho 1 porque só exige grupo positivo; a inadequação é conceitual, não um erro de validação.

Não use `model.predict(X)` como probabilidade. O score do ranker serve para ordenar; não há calibração implementada. Se a decisão exige probabilidade absoluta ou corte regulatório, escolha/avalie um contrato próprio para isso.

## 5. Como funciona, intuitivamente?

`groups_train` e `groups_val` são vetores de tamanhos: por exemplo `[3, 2]` significa que as três primeiras linhas formam um grupo e as duas seguintes outro. `_validate_groups` exige inteiros positivos cuja soma seja exatamente o número de labels.

A função cria `lightgbm.Dataset` com `group=...`, treina com `objective="lambdarank"`, `metric="ndcg"` e avaliação padrão em `[5, 10, 20]`, usando early stopping. Depois o modelo prevê scores. Dentro de cada grupo, `evaluate_ranking` ordena esses scores do maior para o menor e calcula NDCG@k.

NDCG compara o ganho da ordem prevista com o ganho da ordem ideal, descontando posições mais baixas. O helper usa ganho `2^relevância - 1` no avaliador próprio, coerente com o padrão usual de ganhos graduados.

## 6. Exemplo de situação

Imagine uma campanha com dez ofertas elegíveis para cada cliente. Cada oferta histórica recebeu relevância 0 a 3 após um critério previamente definido. Você quer aprender qual oferta deve ficar no topo para novos clientes com o mesmo tipo de conjunto candidato.

O treino recebe todas as linhas em sequência e um vetor `groups` indicando quantas ofertas pertencem a cada cliente. O retorno pode trazer NDCG@5 e NDCG@10. Um NDCG alto diz que a ordem acumulou ganho próximo da ideal naquele k; não significa “percentual de clientes em que o topo foi exatamente correto”.

## 7. O que você precisa antes de usar?

`X` e `y` precisam ter o mesmo número não nulo de linhas. `groups` precisa ser vetor inteiro, não vazio, com valores positivos somando exatamente `len(y)`. O helper também recusa labels negativos.

A ordem física das linhas é essencial: os primeiros `groups[0]` registros pertencem ao primeiro grupo, os seguintes ao segundo e assim por diante. A função não recebe um ID de grupo e não reordena os dados para você.

Os labels usados pelo LightGBM para `lambdarank` precisam ser compatíveis com a configuração de ganhos da biblioteca. Este wrapper não valida integralidade ou limite máximo do label antes do `lightgbm.train`; confira o domínio.

Há uma dependência particular: `lgbm_ranker.py` faz `import mlflow` sem `try/except`. Portanto **importar o pacote exige MLflow instalado**, mesmo quando `log_mlflow=False`. LightGBM e NumPy também são obrigatórios.

## 8. O que este recurso entrega?

`train_lgbm_ranker` retorna `(model, metrics)`, onde `model` é um `lightgbm.Booster` e `metrics` contém `ndcg_at_5`, `ndcg_at_10` e `ndcg_at_20` por padrão.

`evaluate_ranking(model, X, y, groups, ks=...)` permite escolher outros cortes positivos. Cada NDCG é calculado por grupo e depois é feita a média simples entre grupos. Isso significa que, nessa avaliação local, um grupo pequeno e um grupo grande têm o mesmo peso na média final.

A docstring atual de `evaluate_ranking` diz “NDCG@k e MAP@k”, mas **MAP não é implementado nem retornado**. O contrato real desta versão é NDCG apenas.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.lgbm_ranker import train_lgbm_ranker, evaluate_ranking

model, metrics = train_lgbm_ranker(
    X_train, y_train, groups_train,
    X_val, y_val, groups_val,
    log_mlflow=False,
)

ndcg_top3 = evaluate_ranking(model, X_val, y_val, groups_val, ks=[3])
```

O [notebook](exemplo_lgbm_ranker.py) instala LightGBM e reinicia o Python. Ele afirma na abertura histórica que avalia “NDCG e MAP”; nesta R05 a prosa será corrigida para refletir NDCG apenas, preservando código e saídas.

Com logging habilitado, a função chama `mlflow.log_params` e `mlflow.log_metrics` no contexto de run disponível; não administra o ciclo de vida do run nem registra o modelo.

## 10. Decisões e configurações que mais importam

Os defaults locais usam `objective=lambdarank`, `metric=ndcg`, `ndcg_eval_at=[5,10,20]`, learning rate 0,05, `num_leaves=63`, `min_data_in_leaf=50`, frações de features/linhas de 0,8 e `bagging_freq=5`. Aqui o bagging de linhas está efetivamente habilitado porque `bagging_freq` é positivo.

`params` substitui o dicionário inteiro quando fornecido; não é merge com os defaults. Se você passa `params={"objective": ...}`, precisa fornecer também tudo o que quer preservar. O avaliador local continuará calculando NDCG independentemente da métrica configurada no LightGBM.

`num_boost_round` limita rodadas e `early_stopping_rounds` controla a paciência. O código sempre cria callback de early stopping; valores inadequados são repassados à biblioteca.

## 11. Limitações, riscos e armadilhas

O helper não valida IDs de grupo, apenas tamanhos. Duas matrizes podem ter os mesmos tamanhos e linhas agrupadas incorretamente sem qualquer erro. Guarde e confira a chave que originou cada bloco.

A média de NDCG trata grupos com o mesmo peso, e labels sem ganho ideal positivo produzem NDCG 0 no avaliador local. Escolha `k` conforme a decisão; comparar NDCG@1 de um modelo com NDCG@10 de outro não é comparação equivalente.

O módulo importa MLflow obrigatoriamente e a docstring menciona MAP sem implementá-lo. Esses são fatos desta versão; a documentação não os transforma em capacidades inexistentes.

## 12. Quais são as alternativas?

Se a pergunta é classificação/probabilidade, use um baseline supervisionado como [train_lgbm](../train_lgbm/README.md) ou outro classificador apropriado. Se o ranking é trivial ou há poucos candidatos, uma regra de negócio transparente pode ser referência importante.

Outros objetivos de ranking do LightGBM existem, mas este wrapper não os configura como caminho validado. Alterar `params` muda o treino e exige reavaliar o contrato.

## 13. Como saber se o resultado faz sentido?

Primeiro reconstrua alguns grupos usando a chave original e confira que os blocos físicos das matrizes correspondem aos tamanhos de `groups`. Para um grupo pequeno, ordene manualmente os scores e compare o NDCG com `_ndcg_at_k` ou uma implementação independente.

Cheque também uma métrica operacional diretamente ligada à decisão — por exemplo, hit-rate@1 se a pergunta realmente é “o melhor item ficou no topo?”. NDCG e hit-rate respondem perguntas diferentes.

## 14. Arquivos relacionados e próximos passos

A [implementação](lgbm_ranker.py) contém treino, validação de grupos e NDCG; a [fachada](__init__.py) exporta `SEED`, `train_lgbm_ranker` e `evaluate_ranking`; o [notebook](exemplo_lgbm_ranker.py) demonstra grupos sintéticos. O [guia da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantêm as rotas integradas.

Depois do baseline, escolha métricas alinhadas ao produto e avalie separação por grupo/tempo antes de tuning.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. A [documentação de parâmetros do LightGBM](https://lightgbm.readthedocs.io/en/latest/Parameters.html) descreve `lambdarank`, labels de relevância, `label_gain` e parâmetros de ranking. A [documentação de early stopping](https://lightgbm.readthedocs.io/en/v4.6.0/pythonapi/lightgbm.early_stopping.html) explica o papel da validação e de `best_iteration`.

A execução de runtime desta R05 será registrada no relatório da sprint. Sem publicação Databricks, homologação de workspace ou revisão independente presumida.