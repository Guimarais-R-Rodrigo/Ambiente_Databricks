# `pit_join` — reconstruir a informação disponível no momento da decisão

<!-- readme-objeto: 1.0.0 -->

Uma junção point-in-time procura, para cada decisão, a versão mais recente de uma informação que já podia ser conhecida naquele instante. Este helper do Hub faz essa seleção em PySpark e explica por que algumas decisões ficam sem informação elegível.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Junção temporal, também chamada as-of, com atraso de publicação declarado. |
| Para que serve? | Evitar que um histórico forneça informação futura à base de decisões. |
| Use quando... | A informação tem versões e cada decisão possui um instante de referência. |
| Evite quando... | A disponibilidade histórica é desconhecida ou já se perdeu na origem. |
| Precisa de... | DataFrames Spark de fatos e histórico, chaves, datas e atraso em dias. |
| Entrega... | DataFrame enriquecido e diagnóstico de cobertura por linha de fato. |

Leia a [implementação](pit_join.py), a [fachada](__init__.py) ou o [notebook](exemplo_pit_join.py). O helper e o exemplo não persistem tabelas, mas executam operações e contagens Spark: “sem escrita” não significa “sem custo”.

## 1. O que é?

Ao juntar uma tabela de decisões a um histórico, não basta identificar a mesma entidade. É preciso saber qual versão estava disponível no momento relevante. *Point-in-time* significa reconstruir essa visão do passado. Usar informação que só surgiu depois é um tipo de vazamento temporal e pode distorcer uma avaliação preditiva.

Aqui, **fato** é cada linha que representa uma decisão; **feature** é uma característica que será associada a ela. Um *timestamp* registra data e horário. PySpark é a interface Python do Spark, usada para trabalhar com essas tabelas e operações. Assim, os nomes `fatos`, `features` e `ts_decisao` identificam papéis diferentes, não apenas três tabelas quaisquer.

Este é um helper customizado, não uma chamada ao serviço de Feature Store. A [documentação Databricks sobre junções point-in-time](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series) explica o conceito em seu próprio serviço; o contrato desta pasta é definido por `pit_join.py` e inclui uma convenção específica de atraso fixo.

## 2. Que problema este recurso resolve?

A pergunta é: “Qual valor desta característica poderíamos ter usado para esta decisão?”. A função ajuda a montar a base histórica e a distinguir falta de chave, falta de histórico e histórico inelegível na data. Não calcula a decisão, não treina modelo e não certifica a ausência de qualquer forma de vazamento no restante do projeto.

## 3. Quando faz sentido usar?

Use quando uma mesma entidade aparece em várias datas de decisão e a característica muda ao longo do tempo, com versões históricas preservadas. Uma aplicação fictícia seria relacionar cada contato comercial ao último indicador de relacionamento disponível antes do contato.

Também ajuda quando a fonte publica com atraso conhecido e quando valores muito antigos precisam ser rejeitados. A janela máxima torna explícito que “estava disponível” e “ainda era atual o suficiente” são condições diferentes. Antes de adotá-la, confirme se atraso fixo em dias representa a fonte adequadamente.

## 4. Quando não usar?

Não use a tabela de valores atuais para reconstruir o passado se as versões antigas foram sobrescritas. Uma data antiga na linha atual não restaura o valor que era conhecido naquela data. Esse é um contraexemplo em que a consulta pode retornar linhas sem responder à pergunta histórica.

Se a fonte tem atrasos variáveis, horários específicos ou revisões retroativas, a soma de um atraso fixo pode não representar disponibilidade real. É necessário preparar a fonte ou escolher uma implementação que modele esses eventos. Uma data de corte comum pode simplificar o problema, mas um filtro sozinho ainda pode deixar várias versões por entidade; a escolha da última versão continua necessária.

## 5. Como funciona, intuitivamente?

A função calcula um instante de disponibilidade para cada versão:

`disponibilidade = timestamp de referência + atraso_publicacao_dias`.

Só considera versões cuja disponibilidade seja menor ou igual ao instante da decisão. Quando há janela, também exige que a **referência** seja maior ou igual a `decisão − janela_maxima_dias`. Entre as elegíveis, escolhe a disponibilidade mais recente e trata empates conforme a política.

Depois, devolve a seleção às linhas originais de fatos. Várias linhas com a mesma combinação de entidade e decisão recebem a mesma versão, mas continuam sendo várias linhas: o helper não deduplica o negócio. Sem versão elegível, preserva a linha de fato e preenche as características com nulos.

## 6. Exemplo de situação

Uma decisão fictícia ocorre em 12/01/2026. Existem versões de uma característica referidas a 08/01 e 11/01. Com atraso de três dias, elas passam a estar disponíveis em 11/01 e 14/01, respectivamente. A decisão do dia 12 pode usar a primeira, não a segunda.

Com janela máxima de cinco dias, a referência de 08/01 permanece elegível; com janela de dois dias, fica antiga demais e nenhuma versão atende às duas condições. Essa é uma demonstração aritmética da regra, não uma saída Spark inventada. Datas sem horário precisam ainda de uma convenção clara de instante e fuso.

## 7. O que você precisa antes de usar?

`fatos` e `features` são DataFrames PySpark. Informe `chave` como nome de coluna ou sequência de nomes presentes nos dois lados; `ts_decisao` identifica a data dos fatos e `ts_feature` a referência do histórico. As colunas temporais precisam ter tipos ou valores interpretáveis no ambiente, e as chaves precisam representar a mesma entidade.

`atraso_publicacao_dias` é obrigatório, inteiro não negativo e sem default. Zero é permitido quando a disponibilidade imediata foi estabelecida, não como substituto de uma informação ausente. O código converte referências para timestamp; uma data diária representa a meia-noite no fuso da sessão. Um snapshot que só fica pronto ao fechamento não pode ser tratado como conhecido no início do dia.

Confirme as colunas a trazer, os tipos e os nomes internos que não devem colidir. Nem todo erro de coluna ou conversão é validado antecipadamente pela função: alguns aparecem na análise ou execução Spark. A compatibilidade com um runtime específico deve ser testada, não deduzida apenas de “usa PySpark”.

Pré-validação externa recomendada: evite/renomeie colunas chamadas `__disponivel_em`, `__ts_feature_ref`, `__rank`, `__empatados` e prefixos `__pit_*` nas entradas. O código usa esses auxiliares e não verifica todas as colisões. A guarda da coluna `__feature_disponivel_em` com sufixo não substitui essa revisão.

## 8. O que este recurso entrega?

A tupla `(saida, diagnostico)` contém o DataFrame enriquecido e um dicionário de diagnóstico. O retorno tabular mantém as colunas de fatos e acrescenta as selecionadas, com sufixo quando informado. Não inclui automaticamente a referência do histórico.

| Campo do diagnóstico | Significado |
|---|---|
| `linhas_fato` | Quantidade total de linhas de decisão diagnosticadas. |
| `com_feature` | Linhas com uma versão temporal elegível, mesmo que um valor trazido seja nulo. |
| `sem_chave_ou_data` | Linhas de fato com chave ou data de decisão nula. |
| `entidade_sem_historico` | Linhas válidas cuja entidade não tem histórico. |
| `sem_feature_disponivel_na_data` | Há histórico, mas nenhuma versão satisfaz as condições temporais. |
| `cobertura_pct_linhas_validas` | `100 × com_feature / (linhas_fato − sem_chave_ou_data)`. |

As quatro categorias reconciliam com o total. O diagnóstico também informa referências nulas no histórico, empates na versão escolhida, parâmetros, fuso e colunas trazidas. “100% de cobertura” usa o denominador de linhas válidas e não garante características não nulas. Se não há linhas válidas, o código devolve 0.0 para a cobertura; isso não significa população saudável.

## 9. Como usar este recurso no Hub?

Configure o caminho da biblioteca conforme o [guia da coleção](../../README.md) e importe `pit_join` de `hub_snippets.spark.pit_join`. O [notebook](exemplo_pit_join.py) cria DataFrames sintéticos e contrasta a junção ingênua com a seleção temporal. Leia a seção de atraso antes de executar a chamada.

A função dispara contagens para empates e diagnósticos e coleta um pequeno agregado de categorias no processo Python. Não coleta todas as linhas de fatos para pandas, mas a junção por intervalo pode gerar muitos candidatos e movimentar dados entre processos Spark. Examine o plano e um volume representativo; não trate a ausência de escrita como execução barata.

O exemplo não escreve tabela persistente. Testes locais de um helper Spark e os números históricos do notebook não certificam permissões, Spark Connect ou desempenho no workspace de destino. As [limitações atuais de serverless](https://docs.databricks.com/aws/en/compute/serverless/limitations) são específicas desse ambiente e precisam ser verificadas separadamente.

Caso sintético completo em sessão Spark existente, com datas sem hora e fuso já confirmado:

```python
from datetime import datetime
from pyspark.sql import functions as F
from hub_snippets.spark.pit_join import pit_join
fatos = spark.createDataFrame([(1, datetime(2026, 1, 12))], "id int, decisao timestamp")
features = spark.createDataFrame(
    [(1, datetime(2026, 1, 8), 10.0), (1, datetime(2026, 1, 11), 20.0)],
    "id int, referencia timestamp, valor double",
)
saida, diagnostico = pit_join(
    fatos, features, "id", "decisao", "referencia",
    atraso_publicacao_dias=3, janela_maxima_dias=5,
    colunas_feature=["valor"], sufixo="_hist",
    politica_empate="erro", devolver_disponibilidade=True,
)
assert saida.count() == fatos.count()
assert saida.filter(F.col("__feature_disponivel_em_hist") > F.col("decisao")).count() == 0
assert saida.first()["valor_hist"] == 10.0
```

As asserções disparam ações, não escritas. A expectativa vem das datas de referência + três dias, independentemente do diagnóstico devolvido.

## 10. Decisões e configurações que mais importam

`janela_maxima_dias=None` não limita a idade. Quando informada, deve ser um inteiro positivo e mede idade da referência, não tempo desde a publicação. `colunas_feature=None` traz as colunas não chave e não temporais do histórico; selecionar apenas as necessárias torna a intenção mais clara.

`politica_empate="erro"` interrompe quando decisões recebem versões empatadas no instante selecionado. `"menor"` e `"maior"` escolhem pelos valores das colunas trazidas, na ordem configurada. Isso dá um critério reprodutível, não comprova qual versão é verdadeira. Empates mais antigos que não foram selecionados não tornam o diagnóstico uma auditoria de todas as duplicidades do histórico.

`sufixo` evita colisões ao encadear junções. Com `devolver_disponibilidade=True`, aparece a coluna `__feature_disponivel_em` acrescida do sufixo. Ela ajuda a conferir a elegibilidade temporal sem atribuir ao score ou a outro valor o papel de relógio.

## 11. Limitações, riscos e armadilhas

A regra depende de a história ser verdadeira e de o atraso representar disponibilidade real. Correções feitas hoje em um registro antigo podem exigir modelar também o momento da revisão; o helper não reconstrói esse histórico automaticamente. Não há calendário de dias úteis nem atraso individual por registro no argumento de dias.

Além disso, a cobertura diagnóstica não avalia utilidade preditiva, causalidade ou qualidade dos valores trazidos. Uma transformação ajustada conjuntamente no treino e no teste, uma característica calculada com o desfecho posterior à decisão ou uma separação inadequada entre conjuntos podem introduzir outros vazamentos. Já observar uma resposta futura para construir o alvo é esperado em previsão: o problema é deixar essa informação entrar nas características ou violar a disponibilidade e o desenho da avaliação. Use os nomes internos do helper com cuidado em schemas não usuais; a ausência de uma validação explícita não prova que não há colisão.

## 12. Quais são as alternativas?

Uma junção por chave pode atender dados estáticos sem versões temporais. Para um único corte, um filtro seguido de seleção da última versão por entidade pode ser suficiente. Não elimine a seleção da versão quando o filtro deixa várias candidatas.

A funcionalidade [point-in-time do Feature Store](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series) é outra solução, sujeita ao contrato do serviço; não é executada por este helper. No Hub, [join_diagnostics](../join_diagnostics/README.md) ajuda a examinar cruzamentos e [split_temporal](../../ml/split_temporal/README.md) trata a separação da base. São complementos com responsabilidades próprias.

## 13. Como saber se o resultado faz sentido?

Confira que a quantidade de linhas retornadas é igual à de fatos, inclusive quando há fatos repetidos. Refaça manualmente a escolha para poucas entidades com versões conhecidas, contendo uma versão futura, uma antiga demais e uma ausência de histórico.

Ative a devolução da disponibilidade e confira que nenhum valor selecionado ultrapassa a decisão. Some as quatro categorias e recompute a cobertura no denominador correto. Teste a política de empate deliberadamente. Cobertura inesperada pede revisão de atraso, janela, tipo temporal e fuso; não ajuste parâmetros apenas para aumentar o percentual.

## 14. Arquivos relacionados e próximos passos

A [implementação](pit_join.py) é dona das condições e do diagnóstico; a [fachada](__init__.py) exporta a função e as políticas; o [notebook](exemplo_pit_join.py) contém a demonstração. Consulte o [Manual](../../../MANUAL_TECNICO_V2.md#catalogo-helpers) para encaixar o recurso no fluxo. O primeiro passo é confirmar com a fonte o significado de referência e disponibilidade.

## 15. Referências

O contrato local está na [implementação](pit_join.py). A [documentação de point-in-time joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series), consultada em 12/09/2026, sustenta o conceito, não a equivalência deste helper ao serviço. A [referência de limitações serverless](https://docs.databricks.com/aws/en/compute/serverless/limitations), na mesma data, delimita o ambiente; não é uma homologação do código.

| Evidência | Alcance |
|---|---|
| [Teste sintético registrado em 12/09/2026](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982), PySpark 4.0.1 | elegibilidade, empate, janela e fatos repetidos naquela execução |
| Ambiente de destino | exige conferência própria; o registro acima não certifica Databricks, Spark Connect, escala ou auditoria independente |
