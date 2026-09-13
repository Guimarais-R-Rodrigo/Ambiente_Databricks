# `kpi_card` — indicadores resumidos com contexto

<!-- readme-objeto: 1.0.0 -->

> Um cartão de indicador destaca um valor já calculado. Este helper monta HTML ou Markdown; não calcula a métrica, não valida a fonte e não escolhe o que é bom.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Duas funções de apresentação de indicadores. |
| Para que serve? | Mostrar um resumo legível antes dos detalhes. |
| Use quando... | As métricas já têm significado, unidade e período definidos. |
| Evite quando... | O cartão esconderia limitações ou substituiria a análise. |
| Precisa de... | Dicionário de rótulos e valores; texto pronto para apresentação. |
| Entrega... | String HTML ou linha Markdown; sem cálculo nem gravação. |

**Acesso direto:** [exemplo](exemplo_kpi_card.py) · [implementação](kpi_card.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

KPI é a sigla de **indicador-chave de desempenho**. Um cartão de KPI é a apresentação compacta de um indicador, normalmente com valor e rótulo.

Neste módulo, o nome não restringe o conteúdo a desempenho: pode-se apresentar volume, período ou uma ressalva. `kpi_card_html` e `kpi_card_markdown` recebem métricas já prontas. Não consultam uma tabela nem calculam a cobertura exibida.

## 2. Que problema este recurso resolve?

“Como colocar os números essenciais e suas ressalvas perto do início do relatório?” O recurso transforma um dicionário em apresentação compacta, evitando montar o mesmo bloco manualmente.

O autor continua responsável por escolher poucos indicadores pertinentes. Um resumo que omite período, população ou limitações pode ser visualmente organizado e analiticamente enganoso.

## 3. Quando faz sentido usar?

Use HTML em uma saída que o renderize, quando o objetivo for um conjunto de cartões com aparência do Hub. Use Markdown para um resumo textual em um destino compatível.

A escolha é adequada para indicadores já validados e acompanhados de contexto. Uma ressalva curta, como “amostra parcial”, pode ser tão importante quanto o valor de cobertura.

## 4. Quando não usar?

Não passe um DataFrame esperando agregação. Tampouco passe `0.928` supondo que o helper o transforme em `92,8%`: a formatação é responsabilidade anterior à chamada.

Para dezenas de indicadores ou comparação entre vários períodos, uma tabela pode ser mais clara. Não apresente apenas números favoráveis retirando o aviso necessário para interpretá-los.

## 5. Como funciona, intuitivamente?

As funções percorrem `metricas.items()`. Na versão HTML, rótulo e valor passam por `str` e `html.escape`, antes de entrar em um `span` com fundo e tipografia definidos.

Na versão Markdown, o código converte chaves/valores para texto, escapa o caractere `|` e monta uma linha de citação iniciada por `>`. Essa função não faz escape geral de Markdown ou HTML.

## 6. Exemplo de situação

Um resumo sintético pode conter `{"Linhas": "1.000", "Cobertura": "92,8%", "Período": "ago/2026", "Ressalva": "amostra parcial"}`. A cobertura foi fornecida, não calculada pelo cartão.

Antes de publicar, o autor precisa explicar no relatório a população de referência e o denominador da cobertura. O componente ajuda a encontrar a informação; não resolve sua validade.

## 7. O que você precisa antes de usar?

Forneça um dicionário com rótulos textuais únicos e valores pequenos, já formatados para leitura. Chaves diferentes que se tornam a mesma string podem colidir na preparação da versão Markdown: use consistentemente `str` para rótulos.

A importação utiliza Python e cores do Hub. Para HTML, é necessário um destino compatível; o notebook existente usa `displayHTML` e prepara o caminho com Spark. Ele não lê nem grava tabelas de negócio. Não inclua dados pessoais apenas porque o retorno será um cartão.

## 8. O que este recurso entrega?

`kpi_card_html` devolve a sequência de cartões HTML, sem moldura de relatório. `kpi_card_markdown` devolve uma única linha Markdown. Nenhuma função acrescenta unidade, arredonda valores ou atribui status.

Com dicionário vazio, a versão HTML retorna `""` e a Markdown retorna `"> "`. Isso não é um diagnóstico de ausência de dados; é a consequência de não haver itens para exibir. `None` vira texto, não “não disponível” automaticamente.

## 9. Como usar este recurso no Hub?

Consulte o [notebook](exemplo_kpi_card.py) para comparar os formatos, conferindo a preparação antes da execução. Após tornar o pacote acessível pela [coleção](../../README.md):

```python
from hub_snippets.visual.kpi_card import kpi_card_markdown
metricas = {"Linhas": "1.000", "Cobertura": "92,8%"}
print(kpi_card_markdown(metricas))
```

Saída portátil conferida: `> **1.000** Linhas | **92,8%** Cobertura`. Os números foram fornecidos pelo exemplo. A chamada não mede cobertura nem materializa uma tabela.

### Caminho V04 — KPI HTML com tema explícito

```python
from hub_snippets.visual.kpi_card import kpi_card_html_resolvido
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
html = kpi_card_html_resolvido({"Linhas": "1.000"}, tema)
```

A V04 não tematiza `kpi_card_markdown`: Markdown permanece textual. O tema controla somente a apresentação HTML do card; valores, ordem, unidades e contexto continuam responsabilidade do chamador.

## 10. Decisões e configurações que mais importam

Escolha formato, ordem dos indicadores, precisão e contexto antes de chamar a função. O dicionário preserva a sequência de inserção; o helper não prioriza automaticamente métricas.

Para padrão brasileiro, considere [format_br](../../constants/format_br/README.md), observando seus limites de precisão. Depois mantenha também o valor numérico original para cálculos; a string do cartão é apresentação, não substituto da medida.

## 11. Limitações, riscos e armadilhas

O HTML escapa caracteres especiais, mas não anonimiza nem julga o conteúdo. A versão Markdown escapa apenas `|`: caracteres como `*`, quebras de linha e marcação HTML podem continuar alterando a apresentação no destino. Use rótulos controlados e confira o renderizador antes de transportar texto externo.

A conversão de chaves para string pode descartar uma entrada Markdown se, por exemplo, o dicionário tiver as chaves `1` e `"1"`. Essa limitação foi reproduzida; a recomendação é usar rótulos textuais únicos desde a entrada. Na V04, `kpi_card_html_resolvido` obtém o CSS de `constants.styles`; `kpi_card_html` continua no caminho legado e não muda por carregar um tema.

## 12. Quais são as alternativas?

Uma tabela é preferível para muitos indicadores, unidades heterogêneas ou comparações por período. Texto comum pode comunicar uma única métrica com menos estrutura.

[badge](../badge/README.md) oferece estados e faixas, mas exige revisar o significado dos cortes. [dataframe_styled](../../display/dataframe_styled/dataframe_styled.py) é uma opção para tabelas pandas com apresentação mais detalhada. A escolha depende do conteúdo, não de um formato universalmente superior.

## 13. Como saber se o resultado faz sentido?

Compare cada valor com o cálculo de origem e confira unidade, período, população e denominador. O cartão deve dizer o mesmo que a tabela ou análise detalhada.

Confira ainda se todas as entradas aparecem, se texto vazio ou `None` tem interpretação clara e se o resultado permanece legível no destino. Se perder uma entrada Markdown, examine chaves e conversão para texto; não complete manualmente o resumo sem corrigir a origem da apresentação.

## 14. Arquivos relacionados e próximos passos

[kpi_card.py](kpi_card.py) define as duas saídas; [__init__.py](__init__.py) expõe as funções; [exemplo_kpi_card.py](exemplo_kpi_card.py) as demonstra. [format_br](../../constants/format_br/README.md) trata a formatação numérica e a [coleção](../../README.md) mantém a navegação.

## 15. Referências

A [implementação](kpi_card.py) sustenta a transformação e suas limitações. [Python — html.escape](https://docs.python.org/3/library/html.html#html.escape) explica o tratamento do HTML. [Databricks — HTML](https://docs.databricks.com/aws/en/notebooks/notebook-media#include-html) sustenta a rota de renderização em notebooks. Consulta em 12/09/2026.

Revisão R03-A: testes portáteis de texto, ordem, escape, entrada vazia e colisão de chaves. Não houve alteração de CSS, cálculo de indicadores reais, execução no Databricks ou auditoria independente.
