# `rfv_calculator` — recência, frequência e valor com corte temporal explícito

<!-- readme-objeto: 1.0.0 -->

RFV — recência, frequência e valor — resume o histórico de interação de uma entidade. O risco aparece quando o cálculo usa eventos posteriores à data em que uma decisão deveria ter sido tomada. `rfv_calculator` aplica uma data de referência inclusiva, produz medidas brutas e deixa score/segmentação para uma decisão posterior de negócio.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um script PySpark que agrega eventos por cliente até uma data de referência. |
| Para que serve? | Produzir recência, frequência e valor totais e em janelas recentes sem olhar eventos posteriores ao corte. |
| Use quando... | A fonte está em grão de evento/transação e existe uma data de decisão global coerente. |
| Evite quando... | Cada linha exige seu próprio instante de decisão, a disponibilidade difere da data do evento ou a fonte tem duplicidades não tratadas. |
| Precisa de... | Tabela, cliente, data, valor, referência e períodos positivos. |
| Entrega... | DataFrame Spark com RFV bruto e pares `frequencia_Nd`/`valor_Nd`. |

Consulte a [implementação](rfv_calculator.py), a [fachada](__init__.py) e o [notebook de exemplo](exemplo_rfv_calculator.py). O exemplo cria/substitui uma view temporária de transações sintéticas.

## 1. O que é?

RFV resume três ideias: **recência**, quantos dias se passaram desde o evento mais recente; **frequência**, quantos eventos ocorreram; e **valor**, quanto foi acumulado. A implementação calcula essas grandezas por `col_cliente` usando somente registros cuja data é menor ou igual a `dt_referencia`.

Além dos totais, gera frequência e valor para janelas configuráveis, por padrão 30, 60 e 90 dias. Não converte as medidas em quintis, score RFV ou segmento.

## 2. Que problema este recurso resolve?

Ele responde: “Como era o histórico de cada cliente **até esta data**, sem deixar transações futuras contaminarem as features?”. Essa separação é essencial quando RFV alimenta modelos, campanhas ou análises retrospectivas.

O helper também padroniza janelas inclusivas e nomes de saída, evitando que cada notebook implemente cortes ligeiramente diferentes.

## 3. Quando faz sentido usar?

Use em base transacional/evento com uma linha por ocorrência relevante, um identificador de cliente, uma data observável e um valor aditivo. Faz sentido quando todas as entidades estão sendo avaliadas no mesmo `dt_referencia`.

É útil para fotografia de carteira numa data, preparação de features históricas e análise de comportamento até um fechamento específico.

## 4. Quando não usar?

Não use uma única `dt_referencia` para um dataset em que cada observação representa uma decisão tomada em data diferente. Nesse caso, o mesmo corte para todos fica frouxo ou restritivo conforme a linha; a construção precisa ser point-in-time por observação.

Também não use o helper para resolver atraso de publicação. Um evento datado de segunda-feira, mas só disponível na sexta, continua sendo vazamento numa decisão de terça mesmo que sua data seja anterior ao corte. Para esse problema, veja [`pit_join`](../../hub_snippets/spark/pit_join/README.md).

## 5. Como funciona, intuitivamente?

A função converte a data de referência e a coluna de eventos para `date`, remove datas nulas e descarta eventos posteriores ao corte. Depois agrupa por cliente para encontrar última data, soma de valor e quantidade total de linhas. `recencia` é a diferença em dias entre referência e última data.

Para cada período `N`, filtra eventos desde `dt_referencia - (N - 1)` até o próprio corte, agrega frequência/valor e faz `left join` na base de clientes. Ausências nas janelas são preenchidas com zero.

Assim, uma janela de 30 dias inclui exatamente 30 datas de calendário quando os eventos cobrem dias discretos: o dia do corte e os 29 anteriores.

## 6. Exemplo de situação

O [notebook](exemplo_rfv_calculator.py) cria históricos não balanceados para 40 clientes e escolhe `2026-06-01` como data da decisão. Alguns clientes têm evento naquele dia, outros tiveram a última compra meses antes; por isso recência e frequência variam.

O exemplo também conta manualmente eventos até o corte e compara com `frequencia_total`. Zero divergências demonstra a ausência de transações posteriores naquela construção sintética.

## 7. O que você precisa antes de usar?

`table_name` precisa ser legível pela sessão Spark. `col_cliente`, `col_data` e `col_valor` devem existir. A função não valida o grão: você precisa garantir que cada linha represente a unidade que pretende contar como frequência.

`dt_referencia` precisa ser convertível pelo Spark para `date` no ambiente de execução. `periodos` é convertido para inteiros, deduplicado e ordenado; precisa conter ao menos um valor positivo.

O valor precisa admitir `sum`. O código não proíbe negativos, estornos ou nulos: decidir se eles fazem parte do “valor” correto é responsabilidade do domínio.

## 8. O que este recurso entrega?

O DataFrame retorna uma linha por cliente presente antes/no corte, com:

| Coluna | Significado |
|---|---|
| `ultima_data` | maior data válida do cliente até o corte. |
| `valor_total` | soma de `col_valor` em todo o histórico permitido. |
| `frequencia_total` | quantidade de linhas/eventos até o corte. |
| `recencia` | dias entre `dt_referencia` e `ultima_data`. |
| `frequencia_Nd` | quantidade de eventos na janela inclusiva de N dias. |
| `valor_Nd` | soma de valor na mesma janela. |

Os campos de janela ausentes são preenchidos com zero. `valor_total` não recebe esse preenchimento; se todas as observações de valor de um cliente forem nulas, a semântica de `sum` do Spark precisa ser considerada.

## 9. Como usar este recurso no Hub?

```python
from hub_scripts.rfv_calculator import rfv_calculator

rfv = rfv_calculator(
    "catalogo.crm.transacoes",
    col_cliente="id_cliente",
    col_data="dt_transacao",
    col_valor="valor",
    dt_referencia="2026-06-01",
    periodos=(30, 60, 90),
)
```

Abra o [exemplo](exemplo_rfv_calculator.py) para acompanhar a prova do corte e a inspeção de variabilidade entre clientes. O helper não grava o DataFrame resultante; persistência é decisão do consumidor.

## 10. Decisões e configurações que mais importam

`dt_referencia` define o universo permitido. Alterá-la muda totais, última data e todas as janelas.

`periodos` é tratado como conjunto de inteiros positivos. `(90, 30, 30)` produz janelas 30 e 90, nessa ordem crescente. Nomes de colunas são gerados a partir desses inteiros.

A definição de frequência é **contagem de linhas**, não contagem distinta de pedido, dia ou produto. Se o grão real for item do pedido e você queria pedidos, agregue antes.

## 11. Limitações, riscos e armadilhas

A conversão `to_date` descarta componente de horário. Se decisões dependem de hora/minuto, a granularidade não é suficiente.

O script filtra datas nulas depois da conversão. Entradas textuais malformadas podem ter comportamento dependente da configuração ANSI/versão do Spark; valide e normalize datas antes de confiar no corte.

Duplicidades na fonte inflam frequência e valor sem gerar alerta. Valores negativos são somados. Não há winsorization, moeda, conversão cambial ou regra de cancelamento.

Cada período cria uma nova agregação e um join. Muitas janelas ou tabelas grandes podem elevar custo; a função privilegia clareza do contrato, não otimização para centenas de janelas.

## 12. Quais são as alternativas?

Para decisões com instante por linha ou disponibilidade defasada, use construção point-in-time, como [`pit_join`](../../hub_snippets/spark/pit_join/README.md). Para segmentação RFV pronta, defina regras de score/cluster explicitamente depois das features; este helper não escolhe pesos.

Uma agregação Spark SQL manual pode ser melhor quando há uma única janela e uma definição de frequência muito específica.

## 13. Como saber se o resultado faz sentido?

Escolha um cliente pequeno e conte manualmente eventos até `dt_referencia`. Verifique `frequencia_total`, `ultima_data`, `recencia` e a soma de valor.

Confirme que nenhuma linha com data posterior entra. Para cada janela, teste as duas bordas: evento exatamente no corte e evento exatamente em `corte - (N - 1)` devem entrar; o dia anterior deve ficar fora.

Olhe `countDistinct` das colunas RFV no conjunto. Uma feature constante pode ser correta, mas frequentemente revela fonte balanceada ou grão inadequado para o exemplo/uso.

## 14. Arquivos relacionados e próximos passos

A [implementação](rfv_calculator.py) define corte e janelas; a [fachada](__init__.py) expõe a função; o [exemplo](exemplo_rfv_calculator.py) demonstra variabilidade e leakage check. O [catálogo](../README.md) distingue transformação RFV dos scripts de diagnóstico.

Depois das features, documente a regra de decisão que as consome. Score, segmentação e persistência não acontecem automaticamente.

## 15. Referências

O contrato específico é sustentado pelos arquivos locais vinculados, revisados na R04-B em 12/09/2026. A semântica de datas, `datediff`, `date_sub`, agregações e joins segue Apache Spark; os detalhes usados aqui estão explícitos na implementação.

A validação da sprint inclui casos sintéticos com Spark real para corte temporal e janelas. Revisão do texto pelo próprio autor não é auditoria independente nem homologação no Databricks.