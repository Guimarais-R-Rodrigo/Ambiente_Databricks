# `correlation_matrix` — entenda relações entre variáveis numéricas

<!-- readme-objeto: 1.0.0 -->
<!-- sistema-temas-v07: consumidores -->
> **Atualização V07 — estado atual.** `plot_correlation` e
> `plot_correlation_matrix` continuam sendo as rotas legadas. Para aplicar um
> `ResolvedTheme` notebook/light de forma opt-in, use
> `plot_correlation_resolvido` ou `plot_correlation_matrix_resolvido`. A rota
> temática usa `palette.diverging` somente na escala de cor; seleção de colunas,
> descarte de faltantes, cálculo Spark, método e `strong_pairs` permanecem na
> mesma implementação. Um tema inválido falha antes do cálculo.

> Compare como variáveis se movimentam em conjunto e encontre pares para investigar, sem confundir associação com causa.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Mapa de correlações calculadas pelo Spark. |
| Para que serve? | Investigar relações e possível redundância entre variáveis. |
| Use quando... | Há colunas numéricas com significado e observações comparáveis. |
| Evite quando... | A pergunta é causal ou as colunas são códigos sem ordem substantiva. |
| Precisa de... | DataFrame Spark, APIs de `pyspark.ml` compatíveis e Plotly. |
| Entrega... | Figura Plotly e lista de pares que atingem o corte declarado. |

**Acesso direto:** [exemplo](exemplo_correlation_matrix.py) · [implementação](correlation_matrix.py) · [API pública](__init__.py). Leia os requisitos e os efeitos na seção 9 antes de executar o notebook inteiro.

## 1. O que é?

Uma correlação resume como duas medidas variam juntas. Quando valores maiores de uma costumam acompanhar valores maiores da outra, a associação pode ser positiva; quando acompanham valores menores, pode ser negativa. A matriz reúne essas comparações em uma tabela quadrada. O mapa de calor representa os coeficientes por cores, ajudando a localizar padrões sem ler cada célula isoladamente.

Neste objeto, `plot_correlation` calcula os coeficientes no Spark e monta a figura no Plotly. `plot_correlation_matrix` é outro nome para a mesma função, não um método diferente. O recurso não treina um modelo nem decide quais variáveis eliminar.

## 2. Que problema este recurso resolve?

“Quais medidas parecem trazer informação parecida, ou apresentam relações que merecem investigação?” Essa pergunta aparece antes de selecionar variáveis para um modelo e durante uma análise exploratória de dados, também chamada EDA.

O retorno organiza uma investigação. Um par muito correlacionado pode refletir uma transformação conhecida, uma característica legítima do negócio ou uma informação indevidamente disponível. O coeficiente sozinho não identifica qual dessas explicações é correta.

## 3. Quando faz sentido usar?

Faz sentido comparar medidas na mesma unidade de observação: por exemplo, uma linha por cliente e mês, com renda e limite referentes àquela data. Isso evita misturar relações entre clientes com repetições de uma mesma pessoa.

Use Pearson para investigar associação linear: pontos que se aproximam de uma reta crescente ou decrescente. Spearman compara posições ordenadas e é útil para relações monotônicas, nas quais o sentido da variação se mantém mesmo sem uma reta. A escolha depende da pergunta; mudar o método não dispensa revisar valores extremos e a população analisada.

## 4. Quando não usar?

Não use correlação de códigos de agência para descobrir “agências parecidas”: os números identificam categorias, mas sua distância não representa uma quantidade econômica. Uma troca de códigos poderia mudar a resposta sem mudar os clientes.

Também não use este mapa como teste causal, detector completo de vazamento de informação ou filtro automático de variáveis. Associação baixa de Pearson pode coexistir com relação não linear importante. Uma coluna constante não oferece variação para esse cálculo; exclua-a da comparação e investigue sua origem.

## 5. Como funciona, intuitivamente?

O helper seleciona as colunas, elimina as linhas que tenham nulo ou NaN em qualquer uma das selecionadas e reúne os valores de cada linha em um vetor, isto é, uma sequência numérica. `Correlation.corr` produz a matriz; só então essa matriz é trazida à memória do processo coordenador, o driver, e convertida em mapa de calor.

Por fim, o código percorre cada par distinto uma vez. Entra na lista o par cujo valor absoluto da correlação alcança `threshold_highlight`. O sinal original é mantido: −0,9 e +0,9 podem entrar pelo mesmo corte, mas expressam sentidos opostos. **O corte filtra a lista; não desenha um destaque adicional nas células da figura.**

## 6. Exemplo de situação

Imagine uma base fictícia com renda mensal, um limite calculado como três vezes a renda e idade. A pergunta é se o limite realmente acrescenta informação diferente da renda.

Sem ruído, e com renda variando, a construção produz correlação de Pearson +1 entre renda e limite. É uma referência didática conhecida, não um resultado obtido de clientes reais. O bloco da seção 9 reproduz esse caso controlado. Em uma base real, investigue a regra de cálculo e a disponibilidade temporal antes de retirar uma coluna.

## 7. O que você precisa antes de usar?

É necessário um DataFrame Spark e pelo menos duas colunas numéricas existentes, com nomes únicos. Prefira declarar `cols` como lista: a seleção automática considera tipos numéricos, mas não entende que um inteiro pode ser um identificador. A lista vazia equivale à seleção automática, não à solicitação de zero colunas.

Confira linhas completas suficientes, valores finitos e variação nas colunas. O helper valida nomes, quantidade selecionada e método, mas não faz uma análise completa de qualidade. Evite uma coluna selecionada chamada `features`, pois esse também é o nome usado internamente pelo `VectorAssembler`.

O ambiente precisa oferecer Spark e suporte às APIs `pyspark.ml.feature.VectorAssembler` e `pyspark.ml.stat.Correlation`, além de NumPy e Plotly. A execução em Spark local não certifica serverless, Spark Connect ou um runtime Databricks. Consulte as limitações oficiais e teste o compute escolhido; não presuma equivalência entre ambientes.

## 8. O que este recurso entrega?

O retorno é a tupla `(fig, strong_pairs)`. `fig` é uma figura Plotly; `strong_pairs` é uma lista de tuplas `(coluna_1, coluna_2, coeficiente)`. A lista segue a ordem de varredura das colunas, não uma ordenação por força. A diagonal da matriz não entra na lista.

Os coeficientes são adimensionais, entre −1 e +1 quando definidos. NaN significa resultado indefinido, não correlação zero. O helper não retorna contagem das linhas descartadas, significância estatística nem intervalos de confiança. Um `strong_pairs` vazio pode significar que ninguém atingiu o corte, mas também exige verificar NaNs e qualidade da entrada.

## 9. Como usar este recurso no Hub?

No notebook do Hub, configure o caminho de importação conforme o [guia da coleção](../../README.md) e use a sessão `spark` existente. O exemplo abaixo cria somente dados sintéticos em memória; não cria sessão, tabela persistente ou arquivo.

```python
from hub_snippets.display.correlation_matrix import plot_correlation

base = spark.createDataFrame(
    [(1.0, 3.0), (2.0, 6.0), (3.0, 9.0), (4.0, 12.0)],
    "renda double, limite double",
)
fig, pares = plot_correlation(base, cols=["renda", "limite"])
assert len(pares) == 1 and abs(pares[0][2] - 1.0) < 1e-10
print(pares)
```

Para explorar a figura no notebook, use `fig.show()`. O [notebook didático](exemplo_correlation_matrix.py) configura o import pelo usuário da sessão e preserva uma falha histórica de execução no laboratório. Essa transcrição não é resultado novo nem prova de incompatibilidade em todo ambiente. O helper lê os dados e coleta a matriz; não grava tabelas.

## 10. Decisões e configurações que mais importam

`method="pearson"` é o padrão; a alternativa implementada é `"spearman"`. `threshold_highlight=0.8` define a seleção dos pares por valor absoluto. Esse número é uma convenção do helper, não um limite científico universal. O intervalo do parâmetro não é validado: um corte acima de 1 ou negativo pode tornar a seleção inútil.

A lista `cols` muda tanto os pares comparados quanto as linhas mantidas. Acrescentar uma coluna com muitos nulos pode modificar a correlação de duas colunas anteriores, porque o conjunto de observações completas também muda.

## 11. Limitações, riscos e armadilhas

O trabalho distribuído continua dependendo do número de linhas; não existe custo independente do volume. A matriz coletada tem tamanho quadrático no número de colunas. Spearman acrescenta ordenações para construir as posições, o que pode elevar o custo. Reduza o escopo com base na pergunta, não por um número universal de colunas.

A escala `Blues` é sequencial e fixa de −1 a +1: uma associação negativa forte fica clara, embora seja forte em módulo. Leia sinal e coeficiente, não interprete “mais escuro” como “mais forte em qualquer direção”. A rota legada não troca essa escala automaticamente; a rota `_resolvido` usa `palette.diverging` com o mesmo domínio simétrico de −1 a +1.

A exclusão conjunta de nulos pode mudar a população representada. Valores infinitos, colunas constantes e casos muito pequenos exigem checagem. Mesmo uma matriz correta não elimina efeitos de composição de grupos, tempo ou seleção da amostra.

## 12. Quais são as alternativas?

Para um par específico, um gráfico de dispersão permite enxergar curvas, grupos e pontos extremos que um coeficiente esconde. Para comparar distribuições individuais, use [distribution_grid](../distribution_grid/README.md), que responde outra pergunta.

Em dados locais pequenos, uma correlação em pandas pode ser suficiente. Compare resultados somente após alinhar o tratamento de faltantes: o descarte conjunto deste helper não é necessariamente o mesmo de um cálculo por pares. Para causalidade, formule um desenho de identificação adequado; trocar Pearson por Spearman não resolve essa necessidade.

## 13. Como saber se o resultado faz sentido?

Comece pelo caso controlado da seção 9: a matriz deve ser simétrica e o par conhecido deve estar próximo de +1. Depois confira quantas linhas têm todos os campos selecionados preenchidos e compare com o total anterior ao descarte.

Na análise real, investigue NaNs, unidades de observação e nomes repetidos; confronte os pares selecionados com gráficos e regras de negócio. Teste também uma relação invertida conhecida para não esquecer os sinais negativos. Se o mapa divergir da referência, suspenda a interpretação e revise entrada, método e recorte antes de discutir seleção de variáveis.

## 14. Arquivos relacionados e próximos passos

A [implementação](correlation_matrix.py) define o cálculo e o retorno; a [fachada](__init__.py) declara os dois nomes públicos. O [exemplo](exemplo_correlation_matrix.py) oferece o cenário mais longo e sua evidência histórica. Consulte também o [tema](../../visual/theme_plotly/README.md) para entender o que é apresentação e o [guia da coleção](../../README.md) para preparar imports.

## 15. Referências

A [API do Spark Correlation](https://spark.apache.org/docs/4.2.0/api/python/reference/api/pyspark.ml.stat.Correlation.html) sustenta os métodos, o uso de posições e o exemplo com NaN; a versão da página não é uma alegação de versão instalada. As [limitações serverless da Databricks](https://docs.databricks.com/aws/en/compute/serverless/limitations) são referência de plataforma, não homologação deste helper. Fontes consultadas em 2026-09-12.

A procedência do comportamento específico é a [implementação local](correlation_matrix.py), lida na base `c60f1e5`. Os casos reproduzíveis desta sprint ficam nas evidências R03-B do repositório. Conferência de cálculo e geração de figura não equivalem a teste visual no workspace. Revisão própria de ChatGPT; não houve auditoria independente.
