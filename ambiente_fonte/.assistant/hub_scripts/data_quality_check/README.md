# `data_quality_check` — diagnosticar qualidade sem transformar heurística em lei

<!-- readme-objeto: 1.0.0 -->

Qualidade de dados não é uma nota única. Uma tabela pode ter chave consistente e, ao mesmo tempo, estar desatualizada; pode ter poucos nulos, mas duplicar entidades. `data_quality_check` reúne três verificações simples — chave candidata, nulos e atualidade — para tornar esses sinais explícitos antes de uma análise.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um script PySpark de diagnóstico de uma tabela ou view acessível pela sessão Spark. |
| Para que serve? | Tornar explícitos duplicidade/nulidade da chave, nulos por coluna e atualidade opcional. |
| Use quando... | Precisar de um check ad hoc, com política de limiares conhecida e custo de leitura aceitável. |
| Evite quando... | Precisar de uma garantia operacional de pipeline, validação semântica ou certificação ampla de qualidade. |
| Precisa de... | Nome do recurso, ao menos uma coluna de chave candidata e, opcionalmente, coluna de data e limiares. |
| Entrega... | Dicionário com `status`, `score`, política aplicada, checks e alertas. |

Consulte a [implementação](data_quality_check.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_data_quality_check.py). O exemplo cria/substitui views temporárias de sessão; a função consultada não grava na tabela de origem.

## 1. O que é?

Um *data quality check* é uma verificação objetiva sobre uma propriedade observável dos dados. Aqui, a implementação verifica três famílias: unicidade/nulidade de uma chave candidata; taxa de `NULL` em todas as colunas; e, se houver `date_column`, idade do maior valor de data.

A palavra “qualidade” é mais ampla que isso. O script não conhece significado de negócio, população correta, faixas permitidas, consistência entre campos, viés de seleção ou regras regulatórias. Portanto, o retorno descreve somente os checks implementados, não a aptidão universal da tabela.

## 2. Que problema este recurso resolve?

Ele responde: “Antes de confiar nesta fonte, há algum sinal básico e configurado de duplicidade, ausência ou defasagem que eu deveria investigar?”. Isso é especialmente útil quando uma tabela acabou de chegar a uma análise e ainda não existe um gate automatizado específico para ela.

O resultado ajuda a direcionar a investigação. Ele não decide sozinho se um job deve parar, se um dado deve ser descartado ou se uma fonte está homologada.

## 3. Quando faz sentido usar?

Faz sentido no recebimento de uma tabela, em investigação ad hoc, em smoke checks antes de exploração ou para acompanhar a mesma fonte sob uma política estável. A utilidade aumenta quando a chave candidata e o ritmo esperado de atualização já foram definidos por quem conhece a fonte.

Também serve como diagnóstico complementar a uma análise: por exemplo, antes de interpretar uma mudança de média, verificar se o volume cresceu por duplicação da chave.

## 4. Quando não usar?

Não use como substituto de regras operacionais de pipeline. Se a exigência é “linhas inválidas devem falhar, ser descartadas ou monitoradas em toda atualização”, codifique a regra no mecanismo de qualidade do pipeline e monitore a execução. O Databricks recomenda expectations para restrições em Lakeflow pipelines; este helper é diagnóstico sob demanda.

Outro contraexemplo é uma tabela mensal avaliada com `freshness_days=2`. O código pode retornar `fail` todos os dias, embora a fonte esteja perfeitamente no prazo. O erro está na política, não necessariamente nos dados.

## 5. Como funciona, intuitivamente?

A função resolve a sessão Spark e abre `table_name`. Em uma agregação, conta linhas, nulos de cada coluna, componentes nulos da chave e, opcionalmente, a maior data. Em outra ação, conta combinações distintas das colunas de chave e calcula `duplicate_rows = total - distinct_pk`.

Para cada coluna, converte a taxa de nulos em `pass`, `warn` ou `fail` segundo `null_warn` e `null_fail`. Para atualidade, compara a maior data com `date.today()` do processo Python. Por fim, agrega os alertas em um status geral e num score heurístico.

O score é `100 - 25 × falhas - 5 × avisos`, limitado inferiormente a zero. Essa fórmula é convenção local da implementação; não é escala estatística nem padrão Databricks.

## 6. Exemplo de situação

Imagine uma view de clientes com 500 linhas, chave `id_cliente`, 4% de nulos em renda e datas de uma carga antiga. A chave pode estar única e a taxa de nulos dentro do limite, mas o resultado ainda ser `fail` porque `freshness_days=2` não combina com a periodicidade daquela fonte.

O [notebook de exemplo](exemplo_data_quality_check.py) mostra também uma duplicação seletiva: adicionar novamente clientes de um estado altera o peso desse segmento e move uma prevalência que, à primeira vista, ainda parece plausível. O check de chave revela a expansão que a média sozinha não denuncia.

## 7. O que você precisa antes de usar?

`table_name` precisa ser resolvível por `spark.table` e legível pelo usuário. `pk_columns` deve conter ao menos um nome de coluna existente. `date_column`, quando informado, também precisa existir.

Os defaults são `null_warn=5.0`, `null_fail=20.0` e `freshness_days=2.0`. A função exige `0 <= null_warn <= null_fail <= 100` e prazo de atualidade não negativo. Esses valores são configuração do Hub, não exigência da plataforma.

Confirme o grão e o significado da chave antes da chamada. O código não sabe se `id_cliente` deveria ser único por cliente, por cliente e mês ou por evento. Também não valida se a coluna de data representa efetivamente disponibilidade da informação.

## 8. O que este recurso entrega?

O retorno é um dicionário:

| Campo | Significado |
|---|---|
| `status` | `pass`, `warn` ou `fail` conforme os alertas produzidos. |
| `score` | Heurística de 0 a 100 derivada da quantidade de falhas/avisos. |
| `thresholds` | Limiares efetivamente aplicados. |
| `checks.row_count` | Número total de linhas. |
| `checks.pk_uniqueness` | Colunas, linhas duplicadas, linhas com componente de chave nulo e status. |
| `checks.nulls` | Contagem, percentual e status de nulos para cada coluna. |
| `checks.freshness` | Quando solicitado: maior valor, idade em dias e status. |
| `alerts` | Lista estruturada dos checks que não ficaram em `pass`. |

`null_pct` está em percentual de 0 a 100. O check usa `isNull`; string vazia, sentinelas como `-999` e `NaN` não são automaticamente tratados como `NULL`.

## 9. Como usar este recurso no Hub?

Comece pelo [notebook de exemplo](exemplo_data_quality_check.py), que usa dados sintéticos e views temporárias. Revise os nomes dessas views se estiver em sessão compartilhada.

A API pública é:

```python
from hub_scripts.data_quality_check import data_quality_check

resultado = data_quality_check(
    "catalogo.schema.tabela",
    pk_columns=["id_cliente"],
    date_column="dt_referencia",
    thresholds={"null_warn": 5.0, "null_fail": 20.0, "freshness_days": 7},
)
```

O consumidor decide o que fazer com `warn` e `fail`. Não transforme um status em bloqueio automático sem que essa reação esteja explicitamente prevista na política do processo.

## 10. Decisões e configurações que mais importam

A escolha de `pk_columns` define o grão cuja duplicidade será medida. Trocar uma chave simples por uma composta muda o significado do check.

Os limites de nulos são inclusivos: percentual `>= null_fail` vira `fail`; caso contrário, percentual `>= null_warn` vira `warn`. `freshness_days` é comparado com a idade inteira em dias do maior valor de data.

O relógio de referência é `date.today()` no processo Python, não um parâmetro da chamada. Para reprocessamentos históricos ou calendários específicos, essa escolha pode não corresponder à pergunta desejada.

## 11. Limitações, riscos e armadilhas

A função dispara ações Spark sobre a tabela inteira. Há uma agregação larga para nulos e uma contagem de chaves distintas; volume, largura, particionamento e cardinalidade afetam custo.

`duplicate_rows = total - distinct_pk` é uma medida de excesso de linhas em relação às combinações distintas da chave, não uma lista de registros duplicados. Nulidade da chave é reportada separadamente. Para investigação, ainda é necessário localizar quais chaves repetem e por quê.

O score pode dar a mesma penalidade a falhas muito diferentes e não incorpora severidade de negócio. Use-o, no máximo, como sinal de acompanhamento sob a mesma configuração; não compare tabelas diferentes como se fosse uma nota universal.

Atualidade baseada apenas no máximo da coluna também não detecta lacunas, atraso por partição, carga parcial ou atraso de publicação de campos específicos.

## 12. Quais são as alternativas?

Para uma primeira fotografia mais ampla, use [quick_profile](../quick_profile/README.md). Para olhar apenas nulos em um DataFrame já disponível, consulte [`null_summary`](../../hub_snippets/spark/null_summary/README.md).

Para enforcement em Lakeflow pipelines, use expectations e o event log do pipeline conforme a documentação Databricks. Para regras específicas, uma consulta Spark/SQL dirigida pode ser mais clara e barata que executar todos os checks deste script.

## 13. Como saber se o resultado faz sentido?

Reconte uma chave conhecida com `groupBy(...).count()` e confira algumas duplicidades. Recalcule um percentual de nulos como `100 * null_count / row_count`. Para atualidade, compare o maior valor da coluna com o calendário real da fonte.

Teste uma tabela pequena controlada: chave única sem nulos deve passar no check de chave; inserir uma linha repetida deve aumentar `duplicate_rows`; inserir uma chave com componente nulo deve aumentar `null_key_rows`.

Se o status geral surpreender, leia primeiro `alerts` e `thresholds`. A pergunta é qual regra disparou — não “por que o score não ficou alto”.

## 14. Arquivos relacionados e próximos passos

A [implementação](data_quality_check.py) contém os checks e a fórmula do score; a [fachada](__init__.py) expõe `data_quality_check` e `DEFAULT_THRESHOLDS`; o [exemplo](exemplo_data_quality_check.py) demonstra calibração de atualidade e duplicidade seletiva. O [catálogo de Hub Scripts](../README.md) posiciona o utilitário entre os demais diagnósticos.

Depois de um alerta, transforme a hipótese em uma investigação específica. Se o check tiver de virar política operacional recorrente, registre essa decisão no mecanismo de pipeline em vez de depender de execução manual.

## 15. Referências

O contrato específico é sustentado pela implementação, fachada e notebook vinculados acima, revisados na R04-B em 12/09/2026. O texto foi confrontado com o comportamento do código; revisão pelo próprio autor não é auditoria independente.

A documentação Databricks de [boas práticas de governança e qualidade](https://docs.databricks.com/aws/en/lakehouse-architecture/data-governance/best-practices) e de [patterns de expectations](https://docs.databricks.com/aws/en/ldp/expectation-patterns) sustenta a distinção entre diagnóstico ad hoc e regra de pipeline. Fontes consultadas em 12/09/2026.

A validação específica da R04-B, incluindo Spark real, é registrada no relatório da sprint após a execução. Não há, nesta redação, alegação de publicação ou homologação em workspace Databricks.