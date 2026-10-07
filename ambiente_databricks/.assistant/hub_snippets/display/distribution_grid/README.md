# `distribution_grid` — veja a forma das variáveis, não só a média

<!-- readme-objeto: 1.0.0 -->
<!-- sistema-temas-v07: consumidores -->
> **Tema explícito.** As rotas legadas `plot_distributions` e
> `plot_distribution_grid` permanecem disponíveis. Para aparência derivada de um
> `ResolvedTheme`, use `plot_distributions_resolvido` ou
> `plot_distribution_grid_resolvido`. O tema é validado antes da amostragem;
> `smart_sample`, conversão para pandas, colunas e valores dos histogramas não têm
> uma segunda implementação. A aplicação de tema não transforma a amostra em evidência da
> população inteira nem homologa a renderização no browser Databricks.

> Reúna histogramas de colunas numéricas para investigar concentração, assimetria e grupos, observando o alcance da amostra.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Grade de histogramas construída com Spark, pandas e Plotly. |
| Para que serve? | Examinar a distribuição individual de várias medidas. |
| Use quando... | Uma visão exploratória de um recorte limitado responde à pergunta. |
| Evite quando... | É preciso contar a população inteira ou garantir captura de eventos raros. |
| Precisa de... | DataFrame Spark, colunas numéricas, pandas e Plotly. |
| Entrega... | Figura com um histograma por coluna e N coletado no rodapé. |

**Acesso direto:** [exemplo](exemplo_distribution_grid.py) · [implementação](distribution_grid.py) · [API pública](__init__.py). Leia os requisitos e os efeitos na seção 9 antes de executar o notebook inteiro.

## 1. O que é?

Uma distribuição descreve como os valores se espalham: onde se concentram, que intervalos são raros e se existem grupos distintos. O histograma divide o eixo em intervalos e conta observações em cada um. Uma grade coloca vários desses gráficos lado a lado.

`plot_distributions` cria essa grade para colunas de um DataFrame Spark. `plot_distribution_grid` é um nome alternativo da mesma função. Cada painel olha uma variável isoladamente; a grade não calcula a relação entre elas.

## 2. Que problema este recurso resolve?

“O que a média está escondendo nesta base?” Uma média parecida pode resultar de valores concentrados no centro ou de dois grupos afastados. A grade ajuda a formular hipóteses antes de escolher transformações, tratar valores extremos ou investigar segmentos.

Ela não testa automaticamente normalidade, não classifica outliers e não identifica a causa de um pico. Uma forma visual merece investigação; não é um diagnóstico pronto.

## 3. Quando faz sentido usar?

Use no início de uma EDA, após definir qual população e período estão sendo analisados. É útil comparar a forma de renda, saldo e tempo de relacionamento, preservando a unidade de cada coluna.

Também ajuda a revisar uma transformação: uma medida original e sua versão transformada podem ocupar painéis diferentes. Para comparar versões, mantenha o mesmo recorte de dados. Não interprete escalas diferentes como diferenças diretamente comparáveis de magnitude.

## 4. Quando não usar?

Não use a grade amostral para afirmar que não existem operações raras. Um evento que não apareceu na amostra pode existir na base completa. Para contagem exata por faixa, agregue no Spark antes de construir um gráfico.

Não envie códigos de produto apenas porque são inteiros. A distância numérica entre os códigos não representa uma medida. Para categorias, uma tabela de frequências ou barras por categoria responde melhor. A função permite colunas explícitas, mas não valida todo seu significado ou tipo.

## 5. Como funciona, intuitivamente?

O helper seleciona colunas, chama `smart_sample`, converte o recorte para pandas e adiciona um `go.Histogram` para cada coluna. O número de linhas de painéis resulta da quantidade de variáveis dividida por `ncols`, arredondada para cima.

A amostragem usada aqui não é estratificada: não reserva observações para cada grupo. Na implementação de `smart_sample`, se a base cabe no limite, ela é devolvida inteira; caso contrário, o recorte de `sample` é limitado a no máximo `sample_n` linhas. Para `sample_n < total <= 1,2 × sample_n`, a fração pode ser 1: `limit` pode escolher um prefixo. Não há garantia geral de inclusão probabilística uniforme. Isso não garante exatamente aquela quantidade nem os mesmos registros após mudanças de particionamento.

O Plotly determina os intervalos do histograma. O helper não fornece número de intervalos nem normalização em sua assinatura.

## 6. Exemplo de situação

Imagine uma base fictícia com duas concentrações de saldo: uma perto de 20 e outra perto de 70. A média pode ficar no intervalo entre os grupos, onde há poucos registros. Você quer saber se um resumo único representa mal essa população.

O histograma permite visualizar essa hipótese. Uma análise posterior poderia examinar a origem dos grupos. Não rotule a separação como duas personas ou dois regimes econômicos sem validar seu significado. O bloco da seção 9 usa poucos valores conhecidos para conferir a montagem, não para inferência sobre uma população.

## 7. O que você precisa antes de usar?

Use a sessão Spark disponível e bibliotecas pandas e Plotly compatíveis com ela. O helper depende ainda de [smart_sample](../../spark/smart_sample/README.md) e do [tema do Hub](../../visual/theme_plotly/README.md). Não é necessário criar uma sessão Spark nova dentro do notebook gerenciado.

Declare `cols` como lista de colunas numéricas com nomes únicos e `ncols`/`sample_n` como inteiros positivos. A validação explícita checa valores positivos, nomes e ausência de seleção; não é uma checagem completa de tipos e de base vazia. Uma lista vazia de `cols` aciona seleção automática.

O limite é de linhas, não de bytes. Muitas colunas ou valores volumosos ainda podem consumir memória. A conversão para pandas traz os dados selecionados para o driver; o browser também recebe os valores usados nos histogramas.

## 8. O que este recurso entrega?

O retorno é uma `plotly.graph_objects.Figure`, com um trace de histograma por coluna. Trace é a camada de dados de um gráfico. Os nomes das colunas aparecem nos títulos dos painéis, e o rodapé informa `N` a partir das linhas efetivamente coletadas.

Esse N não é necessariamente o total da população nem a quantidade válida de cada coluna: faltantes podem reduzir as observações representadas em um painel. A altura das barras representa contagem, por padrão, não probabilidade. O resultado não retorna uma tabela pronta de contagens por intervalo; o Plotly calcula essas contagens no navegador.

## 9. Como usar este recurso no Hub?

Prepare o import seguindo o [guia da coleção](../../README.md). Este bloco usa somente um DataFrame sintético em memória e a sessão `spark` existente.

```python
from hub_snippets.display.distribution_grid import plot_distributions

base = spark.createDataFrame(
    [(20.0, 1.0), (21.0, 2.0), (69.0, 3.0), (70.0, 4.0)],
    "saldo double, tempo double",
)
fig = plot_distributions(base, cols=["saldo", "tempo"], ncols=2, sample_n=10)
assert len(fig.data) == 2
assert all(trace.type == "histogram" for trace in fig.data)
assert "N = 4" in fig.layout.annotations[-1].text
```

Use `fig.show()` no notebook para examinar a figura. O [exemplo completo](exemplo_distribution_grid.py) cria dados sintéticos, consulta a identidade da sessão para configurar imports e não grava tabela persistente. O helper faz contagens/amostragem no Spark e coleta o recorte para pandas; somente leitura não significa custo zero.

Na mesma base sintética, a rota resolvida exige `ResolvedTheme` de contexto `notebook` e modo `light`, com as [dependências de temas](../../requirements-temas.txt):

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.display.distribution_grid import plot_distributions_resolvido
tema = load_reference_theme("notebook")
fig = plot_distributions_resolvido(base, tema, cols=["saldo", "tempo"], ncols=2, sample_n=10)
```

O tema é validado antes do cálculo/amostragem. O alias resolvido recebe os mesmos argumentos; os dados não são reescritos.

## 10. Decisões e configurações que mais importam

`ncols=3` é o padrão da grade; `sample_n=10000` é o limite padrão solicitado de linhas. A escolha deve considerar espaço de tela, quantidade de variáveis e risco de perder eventos raros. Diminuir `sample_n` reduz a coleta, mas não elimina os trabalhos de contagem da amostragem.

Os intervalos são automáticos. Para uma comparação de frequências que exija faixas idênticas entre amostras ou datas, defina as faixas no processo de análise em vez de confiar em histogramas automáticos independentes. Na rota legada, aumentar o número de painéis não aumenta a altura fixa de 450; na resolvida, a altura vem de `chart.height_px`; ajuste a figura ou separe a apresentação depois de aplicar o helper.

## 11. Limitações, riscos e armadilhas

A seleção automática reconhece tipos numéricos, não relevância analítica. Faltantes, colunas constantes, extremos e combinações de grupos podem mudar a leitura. O limiar de “muitas colunas” é uma questão de legibilidade no destino, não uma regra universal de nove ou doze.

A amostra pode ter menos linhas que o limite e perder caudas raras. O helper não expõe a semente nem um campo de estratificação; usa os padrões do amostrador. A figura contém os valores coletados, não apenas barras agregadas: trate seu compartilhamento com o mesmo cuidado aplicado aos dados.

Os testes de construção da figura não confirmam o comportamento do browser nem a fidelidade visual de uma exportação. A renderização e as escalas precisam ser conferidas no ambiente final.

## 12. Quais são as alternativas?

Para distribuição integral em grandes volumes, agregue frequências por faixas no Spark e desenhe barras com as contagens resultantes. Isso permite controlar unidades, faixas e população representada.

Para um painel isolado ou intervalos customizados, use Plotly diretamente. Para relações entre variáveis numéricas, [correlation_matrix](../correlation_matrix/README.md) resume associações, e um gráfico de dispersão mostra sua forma. Essas escolhas são complementares, não substitutas de toda a EDA.

## 13. Como saber se o resultado faz sentido?

No exemplo controlado, confira dois histogramas e quatro valores por coluna. Na base real, compare N coletado, população de origem e quantidade de valores válidos de cada variável. Uma coluna vazia não comprova ausência do fenômeno.

Examine faixas e escalas antes de comparar painéis. Confronte extremos com mínimos, máximos e quantis calculados sobre o recorte apropriado; quando a pergunta depende de eventos raros, faça contagens específicas na população. Se a forma mudar muito ao variar uma amostra razoável, registre essa instabilidade em vez de apresentar um único desenho como definitivo.

## 14. Arquivos relacionados e próximos passos

A [implementação](distribution_grid.py) compõe a grade; a [fachada](__init__.py) exporta `plot_distributions`, seu alias `plot_distribution_grid`, `plot_distributions_resolvido` e seu alias `plot_distribution_grid_resolvido`. O [notebook](exemplo_distribution_grid.py) demonstra formas distintas. O [amostrador](../../spark/smart_sample/README.md) explica o limite de linhas e o [tema](../../visual/theme_plotly/README.md) explica dimensões e rodapé.

## 15. Referências

A referência [Histogram traces](https://plotly.com/python/reference/histogram/) documenta os dados e as opções dos histogramas. O guia [Histograms](https://plotly.com/python/histograms/) explica contagens, normalização e cálculo no navegador. A documentação [Arrow e pandas no Spark](https://spark.apache.org/docs/latest/api/python/tutorial/sql/arrow_pandas.html) alerta para a coleta na conversão `toPandas()`. Consulta em 2026-09-12.

A [implementação](distribution_grid.py) define a montagem e o [amostrador](../../spark/smart_sample/README.md) delimita o recorte. Construir a figura não certifica renderização nem representatividade.

[Registro técnico de referência](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/readmes_objetos/RELATORIO_R03B.md): consulte data, ambiente e alcance de cada teste; o registro não é homologação do destino.
