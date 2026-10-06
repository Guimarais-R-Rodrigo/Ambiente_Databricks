# `split_temporal` — treino, validação e teste por períodos observados, com gaps explícitos

<!-- readme-objeto: 1.0.0 -->

`temporal_split` separa um DataFrame pandas em treino, validação e teste sem embaralhar o tempo. O corte é feito por **períodos de calendário observados** — por exemplo meses presentes na base — e pode deixar períodos de gap entre as partições. Isso preserva ordem temporal, mas exige entender que proporções são aplicadas sobre períodos, não sobre linhas.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um splitter pandas por períodos completos observados. |
| Para que serve? | Criar treino/validação/teste temporais com gaps opcionais. |
| Use quando... | A avaliação precisa respeitar tempo e a unidade temporal está definida. |
| Evite quando... | As linhas são intercambiáveis, datas são problemáticas ou você precisa de vários cortes históricos. |
| Precisa de... | pandas, uma coluna de data e períodos suficientes. |
| Entrega... | Três DataFrames pandas ordenados: treino, validação e teste. |

Consulte a [implementação](split_temporal.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_split_temporal.py). O helper trabalha no driver; não recebe DataFrame Spark.

## 1. O que é?

Quando a previsão será usada no futuro, embaralhar linhas entre treino e teste pode colocar períodos posteriores no treino e anteriores no teste. `temporal_split` evita esse desenho ao converter datas em períodos (`Period`) e reservar blocos cronológicos inteiros.

A função recebe proporções de períodos para treino e validação; o teste recebe o que sobra depois de considerar dois gaps. Opcionalmente, `group_col` remove da validação e do teste entidades já vistas em partições anteriores.

## 2. Que problema este recurso resolve?

Ele padroniza um único corte temporal com três partições e intervalos de segurança. O recurso é especialmente útil quando o target demora a se materializar e é preciso deixar distância entre o fim do treino e a avaliação.

Também ajuda a evitar que um mês seja parcialmente treino e parcialmente teste quando há muitas linhas por período: a unidade de corte é o período completo observado.

## 3. Quando faz sentido usar?

Use quando existe uma coluna temporal confiável, o objetivo é avaliar períodos posteriores e um único recorte treino/validação/teste é suficiente para o estágio atual. Escolha `period_unit` de acordo com a unidade que deve ficar indivisível — por exemplo `"M"` para mês.

`group_col` faz sentido apenas quando o objetivo é medir generalização para **entidades novas**. Em previsão de painel em que a mesma entidade deve ter história no treino e ser prevista no futuro, omita esse argumento.

## 4. Quando não usar?

Não use `group_col` por reflexo em painel temporal recorrente. Ele torna as partições entity-disjoint e pode remover todas as entidades da validação/teste se elas já apareceram antes.

Não use um único split como evidência de estabilidade ao longo do tempo. Para múltiplos cortes, [walk_forward](../walk_forward/README.md) é mais adequado.

## 5. Como funciona, intuitivamente?

A função converte `date_col` com `pd.to_datetime`, cria `__period = date.dt.to_period(period_unit)` e extrai os períodos únicos **que existem nos dados**. Em seguida calcula quantos períodos vão para treino e validação, pula `gap_periods` entre treino/validação e outro gap entre validação/teste, e devolve o restante como teste.

Isso significa que `gap_periods=1` pula **um período observado**, não necessariamente exatamente um mês de relógio. Se junho estiver ausente, pular uma posição na sequência pode atravessar uma distância calendárica maior.

Com `group_col`, a validação perde entidades já presentes no treino; depois o teste perde entidades presentes no treino ou na validação retida.

## 6. Exemplo de situação

Uma base mensal tem 24 meses observados e 30 clientes por mês. Com `train_pct=0.70`, `val_pct=0.15`, `gap_periods=1` e `period_unit="M"`, a função reserva blocos completos e deixa um período observado em cada fronteira.

A quantidade de **linhas** em cada partição depende da volumetria dos meses. As porcentagens foram aplicadas à quantidade de períodos únicos, então 70% dos períodos não implica necessariamente 70% das linhas se os meses têm volumes diferentes.

## 7. O que você precisa antes de usar?

`__period` é um nome reservado: a implementação sobrescreve uma coluna de entrada com esse nome e depois a remove das saídas. Recuse ou renomeie essa coluna antes de chamar. Para exclusividade por entidade, exija `group_col` não nulo ou defina uma política explícita: nulos não entram nos conjuntos de exclusão e não têm exclusividade garantida.

`date_col` deve existir e ser convertível por pandas. `train_pct` e `val_pct` precisam ser positivos e somar menos que 1. `gap_periods` não pode ser negativo.

A base precisa ter ao menos `3 + 2*gap_periods` períodos observados. Ainda assim, combinações de percentuais e gaps podem deixar o teste vazio; o helper detecta esse caso.

Datas nulas não são explicitamente rejeitadas: `NaT` fica fora da lista de períodos e essas linhas não entram em nenhuma das três partições. Se isso não for desejado, trate datas ausentes antes da chamada e reconcilie a contagem de linhas de entrada com a soma das saídas.

## 8. O que este recurso entrega?

Retorna `(train, val, test)`, cada elemento um novo `pandas.DataFrame`. A coluna temporária `__period` é removida e cada partição é ordenada por `date_col` com índice reiniciado.

O helper não devolve as datas-limite ou períodos descartados em estrutura separada. Se a auditoria precisar dessas fronteiras, derive-as das saídas e da base original.

## 9. Como usar este recurso no Hub?

Fixture mensal, uma linha por mês, sem filtro de entidade:

```python
import pandas as pd
from hub_snippets.ml.split_temporal import temporal_split

df = pd.DataFrame({"dt_ref": pd.date_range("2024-01-01", periods=24, freq="MS")})
assert "__period" not in df.columns
train, val, test = temporal_split(df, "dt_ref")
assert [len(train), len(val), len(test)] == [16, 3, 3]
assert train["dt_ref"].max() == pd.Timestamp("2025-04-01")
assert val["dt_ref"].min() == pd.Timestamp("2025-06-01")
assert test["dt_ref"].min() == pd.Timestamp("2025-10-01")
```

Janeiro/2024–abril/2025 treinam; maio/2025 é gap; junho–agosto validam; setembro é gap; outubro–dezembro testam. São 16 + 3 + 3 períodos e dois gaps. Com 30 linhas em cada mês seriam 480/90/90 linhas e 60 excluídas pelos gaps, antes de eventuais filtros de entidade/datas. Para `group_col`, confira `df[group_col].notna().all()` antes do split quando exclusividade for requisito.

```python
from hub_snippets.ml.split_temporal import temporal_split

train, val, test = temporal_split(
    df,
    date_col="dt_ref",
    train_pct=0.70,
    val_pct=0.15,
    gap_periods=1,
    period_unit="M",
)
```

Para generalização a entidades nunca vistas, passe `group_col="cliente_id"` conscientemente e confira a perda de linhas/entidades.

## 10. Decisões e configurações que mais importam

`period_unit` define a granularidade do corte. `"M"` cria períodos mensais, mas somente para os meses efetivamente presentes. O helper não completa buracos de calendário.

`train_pct` e `val_pct` são convertidos para contagens com `int(...)` e piso, preservando pelo menos um período em cada bloco. O teste recebe os períodos restantes, então a fração final pode diferir das proporções nominais.

`gap_periods` deve refletir uma justificativa temporal real, como maturação do target. Não há lógica automática para descobrir a latência correta.

## 11. Limitações, riscos e armadilhas

O split protege a ordem da avaliação, mas não corrige features construídas com futuro. Uma base pode continuar vazando por joins, agregações ou targets mal definidos.

A função opera em pandas/driver. Datas nulas podem desaparecer das três saídas sem erro. O gap é por períodos observados, não por duração contínua garantida. Os percentuais são sobre períodos, não linhas.

`group_col` implementa um contrato conservador de entidades disjuntas e pode esvaziar validação/teste. Ele não é equivalente a “evitar leakage” em qualquer painel; depende da pergunta de generalização.

O retorno contém três partições, com até dois gaps. Os cortes são calculados sobre períodos observados, não por uma data-limite fornecida pelo chamador.

## 12. Quais são as alternativas?

[walk_forward](../walk_forward/README.md) avalia vários cortes em janela expansiva. Para validação aleatória de dados realmente intercambiáveis, split aleatório estratificado pode ser mais apropriado.

Para impedir informação futura na construção de atributos históricos em Spark, consulte [pit_join](../../spark/pit_join/README.md). Ele resolve outro eixo do problema.

## 13. Como saber se o resultado faz sentido?

Liste os períodos únicos de cada partição e verifique `max(train) < min(val) < min(test)`, considerando os gaps esperados. Reconcilie a quantidade de linhas da entrada com treino + validação + teste + períodos descartados + linhas sem data.

Se `group_col` foi usado, confira interseções de entidades: treino∩val, treino∩teste e val∩teste devem estar vazias no resultado do contrato atual.

## 14. Arquivos relacionados e próximos passos

A [implementação](split_temporal.py) contém o corte; a [fachada](__init__.py) exporta `temporal_split`; o [notebook](exemplo_split_temporal.py) demonstra gaps e conversão controlada de Spark para pandas.

Depois de um split único, use [walk_forward](../walk_forward/README.md) se precisar medir estabilidade em várias janelas. Para features temporais, consulte [lgbm_temporal](../lgbm_temporal/README.md).

## 15. Referências

Consulte a conversão datetime/Period do pandas para as frequências aceitas. Este helper separa dados no driver e preserva a ordem dos períodos; a preparação das features ainda precisa impedir informação futura.
