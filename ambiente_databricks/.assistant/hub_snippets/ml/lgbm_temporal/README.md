# `lgbm_temporal` — engenharia de features temporais por observação e entidade

<!-- readme-objeto: 1.0.0 -->

Apesar do nome histórico, este objeto **não treina LightGBM**. Sua API pública atual prepara features temporais em pandas: lags, estatísticas móveis, calendário e tendência. O ponto crítico é preservar a ordem cronológica e, quando houver painel, isolar cada entidade para que o histórico de uma não entre nas features de outra.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um gerador pandas de lags, janelas móveis, calendário e tendência. |
| Para que serve? | Preparar atributos temporais antes da modelagem. |
| Use quando... | A ordem temporal, o grão e a entidade estiverem definidos e os dados couberem no driver. |
| Evite quando... | Precisar de processamento Spark, lag por intervalo de calendário sem reindexação ou treino de modelo. |
| Precisa de... | pandas, NumPy e um DataFrame com target/data; `entity_cols` quando houver painel. |
| Entrega... | Novo DataFrame ordenado, com features adicionadas e linhas com nulos nas features temporais geradas removidas. |

Consulte a [implementação](lgbm_temporal.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_lgbm_temporal.py). O nome da pasta é legado; a fonte de verdade do contrato é `create_temporal_features`.

## 1. O que é?

Séries temporais costumam ganhar poder preditivo quando o modelo recebe informação sobre passado recente: valor anterior, média dos últimos períodos, posição no calendário e tendência. Em um painel, a mesma ideia precisa ser aplicada **dentro de cada entidade**.

`create_temporal_features` automatiza essas transformações em pandas. A função normaliza a data, ordena as linhas, cria lags e rollings deslocados, deriva calendário, acrescenta uma tendência ordinal e remove linhas com nulos nas features de lag/rolling geradas, inclusive nulos propagados do target.

## 2. Que problema este recurso resolve?

Ele reduz dois erros comuns: construir lag antes de ordenar corretamente a data e misturar entidades ao criar histórico. Também torna explícito que `lag_1` significa a observação imediatamente anterior da mesma sequência — não “um mês atrás” ou “um dia atrás”.

O helper não resolve sozinho disponibilidade point-in-time de outras features, frequência irregular, imputação de dados ausentes nem modelagem. É preparação de atributos, não pipeline temporal completo.

## 3. Quando faz sentido usar?

Use quando o dataset já representa uma série ou painel cuja linha, entidade e data têm significado claro. Em painel de clientes, contratos ou produtos, passe `entity_cols` para que cada lag e rolling seja calculado apenas dentro da entidade correta.

Também faz sentido em protótipos pandas antes de treinar um modelo tabular. Se o dado original está em Spark, reduza o volume de forma controlada antes de coletar ao driver.

## 4. Quando não usar?

Não use sem `entity_cols` quando várias entidades compartilham o mesmo DataFrame e o histórico de uma não pode contaminar outra. A função **permite** omitir a entidade; ela não consegue inferir que o DataFrame é um painel.

Não use `lag_1` como sinônimo de “período anterior de calendário” em séries com buracos. Para esse contrato, reindexe para uma grade temporal completa ou construa a junção temporal explicitamente.

## 5. Como funciona, intuitivamente?

Primeiro, `_normalizar_datas` converte a coluna temporal. Datetime já tipado é aceito; texto no padrão ano-mês-dia pode ser convertido automaticamente; formatos ambíguos precisam de `date_format`. Datas nulas, numéricas ambíguas e fusos misturados são recusados.

Depois, a função ordena por `entity_cols` + data. Por padrão, mais de uma linha para a mesma entidade/data gera erro. Com `on_duplicate_dates="keep"`, os empates são mantidos em ordem estável de entrada.

Lags usam `shift(lag)`. Rollings usam primeiro `shift(1)` e só depois média, desvio-padrão amostral, mínimo e máximo — assim a linha atual não entra na própria janela. Ao final, descarta linhas com nulos em qualquer feature de lag/rolling gerada. Isso inclui o início da série e também nulos propagados de valores ausentes internos do target.

## 6. Exemplo de situação

Considere três contratos com saldos em patamares muito diferentes e 24 observações mensais cada. Você quer `lag_1` e média móvel de três observações para um LightGBM posterior.

Com `entity_cols=["contrato_id"]`, o primeiro `lag_1` válido de cada contrato vem do próprio contrato. Sem `entity_cols`, as datas repetidas entre contratos são recusadas por `on_duplicate_dates="raise"`, o default. Optar deliberadamente por `"keep"` permite uma sequência única, com risco de usar outra entidade como passado. Essa opção serve para estudar o contraexemplo, não é padrão seguro para painéis.

## 7. O que você precisa antes de usar?

`target_col`, `date_col` e todas as `entity_cols` devem existir. Chaves de entidade não podem ter nulos. `lags` precisam ser inteiros positivos sem repetição; `rolling_windows` precisam ser inteiros >= 2, também sem duplicatas.

A função recusa colisão com nomes que ela pretende criar, como `lag_1`, `rolling_mean_3`, `month` ou `trend`. Isso evita sobrescrever feature existente em silêncio.

A data precisa poder ser normalizada. Se o texto não estiver no formato ano-mês-dia, declare `date_format`. A função preserva os valores originais de `date_col` no DataFrame devolvido; usa uma chave datetime temporária somente para ordenação e calendário.

## 8. O que este recurso entrega?

Retorna um novo `pandas.DataFrame`, sem alterar o objeto de entrada. As colunas possíveis são:

- `lag_<n>` para cada lag;
- `rolling_mean_<w>`, `rolling_std_<w>`, `rolling_min_<w>`, `rolling_max_<w>`;
- `month`, `quarter`, `day_of_week`, `day_of_year`, `is_month_start`, `is_month_end` quando `calendar_features=True`;
- `trend`, que é a posição ordinal da linha dentro da entidade ou da série.

As linhas removidas são somente as que ainda têm `NaN` nas features de lag/rolling geradas. Nulos preexistentes em outras colunas não são removidos pelo helper.

## 9. Como usar este recurso no Hub?

Caso sintético curto para conferir perdas e preservar a chave do painel:

```python
import numpy as np
import pandas as pd
from hub_snippets.ml.lgbm_temporal import create_temporal_features

painel = pd.DataFrame({
    "id": ["A"] * 4 + ["B"] * 4,
    "data": list(pd.date_range("2024-01-01", periods=4, freq="MS")) * 2,
    "valor": [1.0, np.nan, 3.0, 4.0, 10.0, 20.0, 30.0, 40.0],
})
saida = create_temporal_features(painel, "valor", "data", lags=[1],
                                 rolling_windows=[], entity_cols=["id"])
assert saida.groupby("id").size().to_dict() == {"A": 2, "B": 3}
```

A primeira linha de cada entidade perde o lag. Em A, março também é removido porque fevereiro tem target nulo; fevereiro permanece com `lag_1=1.0`, embora seu próprio target seja nulo. Reconcilie perdas por entidade e posição, e trate o target antes do treino. O bloco sem entidade do notebook é um contraexemplo que pode interromper a execução com `ValueError`.

```python
from hub_snippets.ml.lgbm_temporal import create_temporal_features

features = create_temporal_features(
    df,
    target_col="saldo",
    date_col="dt_ref",
    entity_cols=["contrato_id"],
    lags=[1, 3, 6],
    rolling_windows=[3, 6],
)
```

O [notebook de exemplo](exemplo_lgbm_temporal.py) usa dados sintéticos e roda inteiramente no driver depois da preparação. Ele não instala nem treina LightGBM.

## 10. Decisões e configurações que mais importam

`entity_cols` é a decisão mais importante em painel. O parâmetro é opcional porque uma série única não precisa de entidade; isso significa que o helper **não exige nem descobre** a chave correta por conta própria.

`on_duplicate_dates="raise"` protege contra ordem arbitrária quando há duas linhas para o mesmo grão temporal. `"keep"` é uma aceitação explícita: empates preservam a ordem de entrada, então a semântica do lag passa a depender dessa ordem.

`lags` e `rolling_windows` são medidos em **número de observações**. Em calendário irregular, um lag de 3 pode cobrir três dias, três meses ou três eventos espaçados de forma desigual.

## 11. Limitações, riscos e armadilhas

O objeto opera em pandas/driver. Não há API Spark distribuída. O nome `lgbm_temporal` pode induzir a esperar treinamento de LightGBM; a implementação atual não possui nenhuma chamada LightGBM.

A função normaliza a data e ordena por entidade e tempo internamente. Forneça um grão coerente e datas normalizáveis. A remoção final elimina linhas com nulos nas features temporais geradas, inclusive nulos propagados de observações internas do target.

A função também não testa leakage de features externas, não reindexa uma grade contínua, não cria targets futuros e não garante que a linha atual tinha todas as informações disponíveis no instante real de decisão.

## 12. Quais são as alternativas?

Para separar períodos, use [split_temporal](../split_temporal/README.md). Para múltiplos backtests, use [walk_forward](../walk_forward/README.md). Para joins históricos point-in-time sobre Spark, consulte [pit_join](../../spark/pit_join/README.md).

Se o requisito é lag de calendário exato em uma série irregular, reindexação por frequência ou uma junção explícita por timestamp é mais adequada que `shift(n)`.

## 13. Como saber se o resultado faz sentido?

Inspecione as primeiras linhas válidas de cada entidade e compare manualmente `lag_1` com o target da observação anterior daquela entidade. Conte quantas linhas foram removidas por entidade e verifique se o warm-up corresponde à maior janela usada.

Crie um caso com entidades em escalas muito diferentes: um lag cruzado fica evidente. Em série irregular, compare as datas das linhas ligadas pelo lag para não confundir posição com duração de calendário.

## 14. Arquivos relacionados e próximos passos

A [implementação](lgbm_temporal.py) contém normalização de datas e geração das features; a [fachada](__init__.py) exporta `SEED` e `create_temporal_features`; o [notebook](exemplo_lgbm_temporal.py) demonstra o risco de omitir entidade.

Depois da engenharia de features, defina um protocolo temporal de treino/validação com [split_temporal](../split_temporal/README.md) ou [walk_forward](../walk_forward/README.md) antes de avaliar qualquer modelo.

## 15. Referências

Consulte shift, rolling, to_datetime e ordenação na documentação da versão pandas usada. O helper gera atributos no driver; não treina LightGBM e não garante disponibilidade point-in-time das demais features.
