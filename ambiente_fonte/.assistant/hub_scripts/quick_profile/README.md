# `quick_profile` — conhecer uma tabela sem confundir amostra com população

<!-- readme-objeto: 1.0.0 -->

Um perfil de dados é um primeiro retrato de uma tabela: suas colunas, quantidade de linhas, ausências e alguns valores característicos. Este script ajuda a começar essa investigação. Parte do retrato usa a tabela inteira; outra parte usa uma amostra. Saber qual parte você está lendo é tão importante quanto obter o resultado.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um script Python que consulta uma tabela ou view pela sessão Spark. |
| Para que serve? | Entender estrutura, nulos e estatísticas selecionadas antes de aprofundar uma análise. |
| Use quando... | Precisar de um diagnóstico inicial e puder autorizar as leituras necessárias. |
| Evite quando... | Precisar comprovar unicidade, qualidade integral ou estatísticas exatas de todas as colunas. |
| Precisa de... | Nome de recurso acessível, PySpark, sessão ativa e tipos de coluna compatíveis. |
| Entrega... | Dicionário com metadados, nulos da tabela inteira e resumos amostrais delimitados. |

Consulte a [implementação](quick_profile.py), sua [fachada](__init__.py) e o [notebook de exemplo](exemplo_quick_profile.py). O exemplo cria ou substitui a view temporária de sessão `vw_exemplo_perfil`. O script não grava na origem, mas tenta usar e liberar cache; valores categóricos podem aparecer sem mascaramento na saída.

## 1. O que é?

Antes de analisar uma base, precisamos saber o que ela contém. *Schema* é sua estrutura de nomes e tipos; completude indica quanto está preenchido; cardinalidade é a quantidade de valores diferentes em uma coluna. Um perfil combina observações desse tipo para orientar as próximas perguntas.

`quick_profile` automatiza um recorte desse trabalho. Recebe o endereço da tabela, e não um DataFrame já carregado, resolve a sessão Spark e calcula os resumos implementados. Não é um certificado de qualidade nem uma EDA completa — análise exploratória que também investiga relações, hipóteses e adequação ao objetivo.

## 2. Que problema este recurso resolve?

A pergunta é: “O que existe nesta fonte e quais pontos merecem investigação antes de usá-la?”. O retorno permite identificar colunas ausentes com frequência, tipos inesperados ou faixas amostrais que justificam uma checagem específica.

Ele apoia a escolha do próximo diagnóstico. Não determina sozinho se a base está apta para modelagem, se a chave é única ou se uma diferença encontrada representa erro de cadastro. Essas conclusões exigem regras e conhecimento do domínio que não entram na assinatura.

## 3. Quando faz sentido usar?

Use para conhecer uma tabela acessível no início de um trabalho ou reexaminar uma fonte conhecida após uma mudança. É útil quando há muitas colunas e você precisa distinguir estrutura, preenchimento global e características de uma amostra.

O custo precisa ser aceitável: a função calcula contagens de linhas e nulos na tabela completa. Uma amostra pequena nos demais resumos não transforma essa etapa em uma leitura pequena. A configuração faz mais sentido quando uma inspeção inicial limitada é suficiente e a população consultada já está delimitada no recurso de entrada.

## 4. Quando não usar?

Não use `cardinality_sample` para certificar que `id_cliente` é uma chave única. O cálculo considera apenas algumas colunas string, usa a amostra e é aproximado. Mesmo com `sample_fraction=1`, continua chamando `approx_count_distinct`, que estima, em vez de contar exatamente, os valores distintos.

Outro contraexemplo é consultar uma tabela com nomes ou identificadores pessoais e publicar o dicionário inteiro em um relatório. `top_values_sample` pode carregar esses valores sem máscara. Prefira uma fonte previamente autorizada e minimizada ou diagnósticos específicos sem exposição de categorias sensíveis.

## 5. Como funciona, intuitivamente?

Primeiro, a função confere a fração solicitada, acessa a tabela e identifica seus tipos. Uma agregação calcula a quantidade total de linhas e os nulos de todas as colunas. Depois, produz uma amostra aleatória sem reposição, ou usa todas as linhas quando a fração é 1.

Essa segunda base alimenta cardinalidade aproximada, categorias frequentes, mínimos, máximos e médias selecionados. O código tenta mantê-la em cache, uma forma de reutilizar dados entre operações em vez de recalculá-los, e depois liberar esse armazenamento. Por fim, reúne resultados e metadados em um dicionário.

A seleção aleatória não garante exatamente a fração solicitada; a [documentação de `DataFrame.sample`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.sample.html) faz essa distinção. Confira `sample_rows`, não apenas o parâmetro solicitado.

## 6. Exemplo de situação

Imagine uma tabela fictícia de contatos de campanha, com renda, data de referência e canal. Você quer decidir quais checks construir antes de preparar características para um modelo.

O perfil pode mostrar que renda tem muitos nulos na tabela inteira e que a amostra observada contém poucos canais. A primeira conclusão descreve a completude global daquela coluna; a segunda não prova que todos os canais da população apareceram. O próximo passo seria investigar a origem dos nulos e medir categorias relevantes de forma dirigida. Este cenário ilustra uma decisão, sem inventar valores executados.

## 7. O que você precisa antes de usar?

`table_name` é uma string resolvida por `spark.table`: normalmente um nome qualificado de tabela, ou uma view que exista na sessão. Uma view é um resultado de consulta acessível por um nome; quando temporária, seu uso depende da sessão que a contém. `sample_fraction` deve estar no intervalo maior que zero e até 1; `max_categories` precisa ser positivo. `seed`, informado somente por nome, controla a semente da amostragem.

A função exige PySpark e uma sessão capaz de ler o recurso. Ela procura a sessão ativa e, na ausência, tenta obter ou criar outra. A permissão de leitura e a disponibilidade do objeto não são concedidas pelo script.

O suporte de tipos não é geral. A implementação identifica colunas numéricas por trechos de texto no dtype; tipos complexos como `array<int>` podem ser classificados inadequadamente e falhar nas agregações. Confirme o schema e prefira colunas escalares compatíveis. Os limites de seleção seguem a ordem das colunas: isso deve ser considerado ao preparar uma view para inspeção.

## 8. O que este recurso entrega?

Para comparação entre perfis, registre **fora do retorno** a versão da tabela, filtros, horário de leitura e ambiente. A API não produz esse envelope de proveniência; seed isolada não identifica a população.

| Campo | Significado e alcance |
|---|---|
| `table`, `total_rows`, `total_columns`, `dtypes` | Recurso consultado, tamanho e estrutura completos. |
| `sample_fraction`, `sample_seed`, `sample_rows` | Configuração e quantidade efetiva de linhas da segunda base. |
| `null_summary_full_table` | Lista com `column`, `null_count` e `null_pct` sobre todas as linhas, ordenada por percentual decrescente. |
| `cardinality_sample` | Contagem aproximada de valores diferentes nas primeiras dez colunas string. |
| `top_values_sample` | Categorias e contagens nas primeiras cinco colunas string, limitadas por `max_categories`. |
| `numeric_summary_sample` | Mínimo, máximo e média das primeiras dez colunas identificadas como numéricas. |
| `date_range_sample` | Mínimo e máximo das primeiras cinco colunas identificadas como datas ou timestamps. |

Os percentuais de nulos usam escala de 0 a 100. A verificação emprega `isNull`: vazio textual, código sentinela e `NaN` não são equivalentes a NULL nessa contagem. Uma estimativa de cardinalidade pode ultrapassar o número de linhas da amostra; isso não deve ser interpretado como contagem exata impossível.

Na tabela vazia, o código devolve percentual de nulos igual a zero. Isso significa convenção de retorno para denominador vazio, não “qualidade perfeita”. Uma amostra sem linhas também limita a utilidade de seus resumos.

## 9. Como usar este recurso no Hub?

Antes do import, confira a [preparação comum](../README.md#preparacao-comum): raiz `.assistant` no `sys.path`, Python e, para este helper, PySpark/Spark e acesso ao recurso.

Chamada mínima, após revisar fonte, tipos, PII e custo:

```python
from hub_scripts.quick_profile import quick_profile

perfil = quick_profile("catalogo.schema.tabela", sample_fraction=0.1, max_categories=10, seed=42)
print(perfil["total_rows"], perfil["sample_rows"])
print(perfil["null_summary_full_table"])
```

Não imprima `top_values_sample` indiscriminadamente: categorias podem conter PII sem máscara. O [exemplo](exemplo_quick_profile.py) cria/substitui uma view temporária; reveja o nome se a sessão for compartilhada. Esse cenário não homologa qualquer fonte ou runtime.

## 10. Decisões e configurações que mais importam

Uma preparação possível, quando autorizada, é selecionar colunas escalares e aplicar o recorte em uma view de análise antes da chamada. Isso é orientação de preparo, não uma view criada automaticamente pelo helper.

A fração padrão é `0.1`, mas a amostra resultante não tem tamanho máximo garantido. Aumentá-la pode melhorar a observação de categorias raras, com mais processamento, sem tornar a cardinalidade exata. A fração 1 elimina a amostragem, não a aproximação do estimador.

`max_categories=20` limita as linhas devolvidas por coluna na lista de categorias; não limita todo o trabalho de agrupamento anterior. `seed=42` ajuda a repetir o sorteio sob condições equivalentes, mas não substitui registrar versão da fonte, filtros e condições de leitura. Uma base alterada não vira a mesma população por repetir a semente.

Não há parâmetro para escolher colunas ou filtros. Delimite o recurso antes da chamada por um mecanismo autorizado, como uma view preparada para a análise, e registre essa preparação.

## 11. Limitações, riscos e armadilhas

| Condição | Tratamento |
|---|---|
| Fração fora de `(0,1]` ou `max_categories<=0` | `ValueError` |
| Tabela, permissão, sessão ou tipo complexo incompatível | erro de runtime |
| Amostra vazia com tabela não vazia | retorno amostral limitado; não prova tabela vazia |

Há leituras completas, ações Spark e agrupamentos. O código coleta resumos no processo coordenador, não converte a tabela inteira para pandas; ainda assim, tipos, largura e cardinalidade podem tornar a consulta cara.

O cache é tentado e exceções são ignoradas nesses auxiliares. Isso não garante reutilização nem valida todo modo de compute. Com fração 1, o objeto usado pode compartilhar estado de cache com a sessão; sua liberação precisa ser considerada em fluxos compartilhados. Se `sample.count()` falhar antes do bloco `try/finally`, a liberação não está protegida por esse bloco.

O perfil não calcula quantis, duplicidade de chave, relações entre variáveis, semântica de domínio ou todos os resumos de todas as colunas. Datas e extremos amostrais não representam necessariamente os limites da tabela completa. Não converta ausência de evidência em ausência de problema.

## 12. Quais são as alternativas?

Para completude em um DataFrame já disponível, examine [null_summary](../../hub_snippets/spark/null_summary/null_summary.py). Para regras e um diagnóstico de qualidade configurado, consulte [data_quality_check](../data_quality_check/data_quality_check.py). Leia seus contratos: eles não são apenas outros nomes para este perfil.

Uma consulta Spark SQL dirigida é preferível quando você já sabe qual regra precisa conferir, como duplicidade por chave e período. O [prompt de perfil rápido](../../hub_prompts/eda_rapida/eda_rapida.md) ajuda a estruturar a investigação com uma IA, mas não substitui a execução e a inspeção das evidências.

## 13. Como saber se o resultado faz sentido?

Confira primeiro recurso, filtros e total de linhas. Compare uma coluna de nulos com uma agregação independente e verifique que `null_pct` corresponde a `100 * null_count / total_rows`, quando o denominador é positivo.

Depois separe os campos completos dos amostrais. Observe tamanho efetivo da amostra, colunas selecionadas e campos vazios. Para uma decisão sobre unicidade ou categoria rara, faça a checagem específica na população pertinente; não arredonde a estimativa até ela parecer uma contagem exata.

Se surgir um resultado estranho, registre o schema, a versão da fonte e a configuração antes de mudar parâmetros. Retirar a coluna problemática ou aumentar a amostra sem documentar a mudança impede comparar as duas execuções.

## 14. Arquivos relacionados e próximos passos

A [implementação](quick_profile.py) define campos e limites; a [fachada pública](__init__.py) expõe a função; o [notebook](exemplo_quick_profile.py) demonstra o alcance da amostra. O [Hub Scripts](../README.md) apresenta outros diagnósticos, e o [Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers) mantém o catálogo integrado.

Depois do perfil, escolha um check concreto para cada achado relevante. Não há etapa automática de correção, escrita ou aprovação de dados neste recurso.

## 15. Referências

Contrato: [implementação](quick_profile.py), [fachada](__init__.py) e [exemplo](exemplo_quick_profile.py). Referências Apache Spark: [sample](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.sample.html) e [approx_count_distinct](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.approx_count_distinct.html), consultadas em 12/09/2026. A fração pedida não fixa N; cardinalidade permanece aproximada; os limites de colunas vêm do Hub.
