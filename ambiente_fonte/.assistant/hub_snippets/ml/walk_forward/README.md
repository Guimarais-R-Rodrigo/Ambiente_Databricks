# `walk_forward` — múltiplos cortes temporais com janela de treino expansiva

<!-- readme-objeto: 1.0.0 -->

Walk-forward validation repete a avaliação ao longo do tempo: em cada fold, o histórico disponível cresce e um bloco posterior é entregue a um callback de modelagem. Este helper organiza os períodos e metadados de cada fold. Ele **não treina modelo por conta própria**; `model_fn` é responsável por ajustar no treino e avaliar somente no teste recebido.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um orquestrador pandas de folds temporais em janela expansiva. |
| Para que serve? | Medir desempenho em vários cortes históricos sucessivos. |
| Use quando... | Um único split não basta e existe um callback de treino/avaliação sem leakage. |
| Evite quando... | Há poucos períodos, o callback usa informação do teste no fit ou o dado não cabe no driver. |
| Precisa de... | pandas, NumPy, data/target e uma função `model_fn(train_df, test_df)`. |
| Entrega... | Lista de dicionários de métricas + metadados por fold. |

Consulte a [implementação](walk_forward.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_walk_forward.py). A função trabalha sobre períodos observados e não completa buracos de calendário.

## 1. O que é?

Uma única validação temporal pode coincidir com um mês fácil ou difícil. Walk-forward repete a pergunta em vários pontos do histórico. No desenho implementado aqui, o conjunto de treino começa com `min_train_periods` e cresce a cada fold; o bloco de avaliação vem depois de um `gap` opcional.

A função `walk_forward_cv` cria os DataFrames de treino/teste, chama `model_fn` e agrega o dicionário devolvido pelo callback com metadados da janela.

## 2. Que problema este recurso resolve?

Ele padroniza a mecânica de múltiplos cortes temporais, tornando visível quantos folds realmente foram avaliados, onde termina o treino, onde começa o teste e quantas linhas existem em cada lado.

O recurso ajuda a estudar estabilidade temporal. Não garante que o modelo será retreinado corretamente: essa responsabilidade permanece dentro de `model_fn`.

## 3. Quando faz sentido usar?

Use quando o uso real prevê atualizações/retrenos periódicos ou quando você quer saber se uma métrica é estável em diferentes regimes históricos. Também faz sentido quando o target tem latência e um `gap` precisa separar o fim do treino do início da avaliação.

A janela é expansiva, não deslizante: folds posteriores usam todo o histórico desde o primeiro período observado até o fim do treino daquele fold.

## 4. Quando não usar?

Não use com callback que pré-ajustou preprocessing ou modelo fora de `model_fn` usando a base inteira. O helper não consegue detectar esse leakage.

Não use como substituto de monitoramento de produção. O walk-forward é retrospectivo. Também não é adequado quando se deseja janela móvel de tamanho fixo, porque a implementação atual sempre expande o treino.

## 5. Como funciona, intuitivamente?

A função converte a data e cria períodos com `dt.to_period(period_unit)`. Extrai os períodos únicos observados em ordem. Para cada posição `end`, treino recebe todos os períodos anteriores; `gap` posições observadas são puladas; teste recebe `test_periods` posições.

`step` controla quantas posições o fim do treino avança entre folds. Se treino ou teste ficarem vazios, aquele fold é ignorado. O callback precisa retornar `dict`; outro tipo gera `TypeError`.

Depois, o helper acrescenta `fold`, `train_end`, `test_start`, `n_train` e `n_test` e imprime média ± desvio-padrão para métricas numéricas encontradas a partir das chaves do primeiro resultado.

## 6. Exemplo de situação

Com 24 meses observados, `min_train_periods=6`, `test_periods=1`, `step=1` e `gap=0`, o primeiro fold treina nos seis primeiros meses e testa no sétimo; o segundo incorpora esse sétimo mês ao treino e testa no oitavo.

Com `gap=3`, três **períodos observados** ficam entre treino e teste. Se a base pula um mês de calendário, a distância real entre datas pode ser maior que três meses. Por isso `gap` deve ser interpretado na sequência de períodos presentes, não como cronômetro absoluto.

## 7. O que você precisa antes de usar?

`date_col` e `target_col` devem existir. `min_train_periods`, `test_periods` e `step` precisam ser positivos; `gap` não pode ser negativo. Datas precisam ser convertíveis pelo pandas.

`model_fn` recebe dois DataFrames completos. O test DataFrame inclui a coluna target porque o callback precisa calculá-la para a avaliação; a disciplina de não usar esse target no fit é responsabilidade do callback.

A função não exige explicitamente um número mínimo de folds. Se não houver períodos suficientes para entrar no loop, pode retornar uma **lista vazia** sem erro. Confira `len(results)` antes de interpretar qualquer média.

## 8. O que este recurso entrega?

Retorna `List[Dict[str, Any]]`. Cada dicionário contém as métricas devolvidas pelo callback e os metadados:

- `fold`;
- `train_end`;
- `test_start`;
- `n_train`;
- `n_test`.

Se `model_fn` devolver chaves com esses mesmos nomes, os valores serão sobrescritos pelos metadados do helper. O retorno não é DataFrame; o consumidor pode convertê-lo depois.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.walk_forward import walk_forward_cv


def model_fn(train_df, test_df):
    model = ajustar_somente_no_treino(train_df)
    pred = model.predict(test_df[features])
    return {"rmse": calcular_rmse(test_df[target], pred)}

results = walk_forward_cv(
    df,
    date_col="dt_ref",
    target_col="target",
    model_fn=model_fn,
    min_train_periods=12,
    test_periods=1,
    gap=1,
    period_unit="M",
)
```

O [notebook de exemplo](exemplo_walk_forward.py) usa um callback de baseline que recalcula a média do target a cada fold.

## 10. Decisões e configurações que mais importam

`min_train_periods` define quanto histórico mínimo cada primeiro modelo recebe. `test_periods` define o tamanho temporal do bloco avaliado. `step` define a frequência de novos folds.

`gap` precisa representar a indisponibilidade real do target ou de features, mas conta posições de períodos **observados**. O helper não conhece a latência de negócio e não verifica se o número passado está correto.

`period_unit` transforma timestamps em períodos. A série continua sendo baseada nos períodos presentes; não há reindexação automática de buracos.

## 11. Limitações, riscos e armadilhas

O helper não consegue provar que preprocessing, feature engineering, seleção de hiperparâmetros ou modelo foram ajustados apenas no treino. Essa disciplina pertence ao callback.

Ele pode retornar zero folds silenciosamente. A média impressa usa `np.std` com `ddof=0`, isto é, desvio-padrão populacional dos valores observados, e não um intervalo de confiança.

A rotina escolhe as chaves de resumo a partir do primeiro fold. Métrica numérica que só apareça em folds posteriores não entra no print agregado. Chaves de metadados devolvidas pelo callback são substituídas.

O notebook descreve “retreinar a cada janela”; mais precisamente, o helper **chama** `model_fn` a cada janela. Retreinamento só ocorre se a implementação do callback o fizer.

## 12. Quais são as alternativas?

[split_temporal](../split_temporal/README.md) é mais simples quando um único corte treino/validação/teste é suficiente. Para validação específica de bibliotecas de forecasting, ferramentas nativas podem oferecer horizontes e diagnósticos adicionais.

Uma janela deslizante fixa requer outro algoritmo: o helper atual usa expanding window.

## 13. Como saber se o resultado faz sentido?

Confira a quantidade de folds esperada a partir dos períodos observados e parâmetros. Para alguns folds, reconstrua manualmente as datas de treino e teste e confirme o gap. Garanta que `max(train_date) < min(test_date)`.

Audite o callback: scaler, encoder, seleção de features e tuning precisam ser ajustados dentro do fold, sem informação futura. Compare distribuição de métricas entre folds, não apenas a média.

## 14. Arquivos relacionados e próximos passos

A [implementação](walk_forward.py) cria folds e chama o callback; a [fachada](__init__.py) exporta `walk_forward_cv`; o [notebook](exemplo_walk_forward.py) demonstra um baseline sintético.

Para um corte único consulte [split_temporal](../split_temporal/README.md). Para geração de lags/rollings, [lgbm_temporal](../lgbm_temporal/README.md). Modelos como [arima_wrapper](../arima_wrapper/README.md) e [prophet_wrapper](../prophet_wrapper/README.md) podem ser avaliados dentro de um protocolo temporal compatível, com adaptação do callback.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. A semântica de períodos e conversão temporal foi confrontada com a documentação oficial do pandas vigente em 12/09/2026.

Este README documenta um orquestrador de avaliação, não um treinador. Não presume ausência de leakage no callback, publicação no Databricks, homologação em workspace nem auditoria independente.
