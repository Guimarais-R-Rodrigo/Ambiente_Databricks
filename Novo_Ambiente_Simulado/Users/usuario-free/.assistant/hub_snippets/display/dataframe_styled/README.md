# `dataframe_styled` — apresente uma tabela sem mudar seus dados

<!-- readme-objeto: 1.0.0 -->

> Transforme uma pequena tabela pandas em HTML legível, com formatos declarados e realce limitado a números negativos.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Apresentação HTML de uma tabela pandas. |
| Para que serve? | Facilitar a leitura de resultados já calculados. |
| Use quando... | A tabela é pequena e seu conteúdo é confiável. |
| Evite quando... | É preciso processar toda uma base Spark ou renderizar texto não confiável. |
| Precisa de... | pandas, Jinja2 e importação do Hub configurada. |
| Entrega... | Texto HTML; o helper não exibe nem salva automaticamente. |

**Acesso direto:** [exemplo](exemplo_dataframe_styled.py) · [implementação](dataframe_styled.py) · [API pública](__init__.py). Leia os requisitos e os efeitos na seção 9 antes de executar o notebook inteiro.

## 1. O que é?

Uma tabela estilizada conserva os valores de origem e altera sua apresentação: cabeçalho, cores e representação dos números. HTML descreve os elementos da página; CSS descreve sua aparência. O `Styler` do pandas é o componente que organiza essa apresentação.

`display_styled` é uma função do Hub que usa esse componente e devolve o HTML pronto. Não é uma planilha interativa, um exportador de dados ou um diagnóstico automático de qualidade.

## 2. Que problema este recurso resolve?

“Como tornar uma tabela de resultados fácil de ler, sem repetir a configuração visual?” Isso ajuda a apresentar variações, contagens e indicadores já calculados.

O helper não decide se um resultado é bom ou ruim. Seu realce tem uma regra concreta e estreita: em colunas declaradas, valores reconhecidos como `int` ou `float` e menores que zero recebem destaque. Um número positivo muito preocupante não ganha destaque por isso.

## 3. Quando faz sentido usar?

Use em uma tabela agregada, como uma linha por segmento com volume e variação mensal. Poucas linhas permitem comparar valores sem rolar uma página extensa.

É útil também quando colunas precisam de representações diferentes: um percentual, uma contagem e uma medida contínua. Mantenha as unidades explícitas nos títulos ou na explicação; a cor não substitui a leitura do valor e do contexto.

## 4. Quando não usar?

Não passe um DataFrame Spark esperando processamento distribuído. O recurso usa `.style`, uma interface pandas. Antes de uma conversão, selecione e limite os dados para que caibam em memória.

Não o use para destacar automaticamente “nulos acima de 20%”: números positivos não atendem ao teste de negatividade. Também não renderize conteúdo externo não confiável com esta função como única proteção. Ela não habilita explicitamente escape de HTML.

## 5. Como funciona, intuitivamente?

O pandas monta um objeto de apresentação sobre a tabela. O helper define o estilo dos cabeçalhos, percorre as colunas indicadas para realçar negativos e aplica o dicionário de formatos. A chamada final a `to_html()` produz uma string, isto é, um texto.

O teste de negatividade considera o valor original, não o texto formatado. Por isso, converter uma coluna numérica inteira para texto antes do realce pode impedir a identificação dos negativos. A tabela de entrada não é transformada em HTML nem substituída pelo retorno.

## 6. Exemplo de situação

Considere uma tabela fictícia com dois segmentos, variação de saldo de −2,5% e +1,2% e contagens de clientes. Você quer chamar atenção para a queda, mas preservar os valores numéricos para outros cálculos.

A escolha é apresentar uma cópia ou visão da tabela, realçando a coluna de variação. Essa é uma convenção de leitura: uma redução de despesa, por exemplo, pode ser favorável. O significado do sinal continua sendo explicado pela pessoa responsável.

## 7. O que você precisa antes de usar?

Forneça um DataFrame pandas com nomes de colunas únicos e valores compatíveis com os formatos pedidos. Jinja2 é dependência de renderização do Styler; importar o módulo sem erro não prova que a chamada inteira funcionará.

`highlight_cols` deve ser uma lista de nomes. Um nome ausente é silenciosamente ignorado pelo helper; não há diagnóstico de digitação. `format_dict` associa nomes de colunas a formatos, como `"{:.1f}"`. Tipos numéricos especiais, como `Decimal`, não são garantidos pelo teste `isinstance(v, (int, float))`.

Defina uma quantidade pequena de linhas e não coloque dados pessoais em uma saída compartilhável. HTML pode carregar todos os valores que você entregou, não apenas aqueles para os quais o leitor olhou.

## 8. O que este recurso entrega?

O resultado é `str`, contendo estilos e tabela HTML. Use um renderizador para visualizar; `print(html)` mostra o código da apresentação. Os números originais continuam no DataFrame.

A exibição de `"{:.1f}%"` apenas acrescenta o símbolo: 0,025 aparece como 0,0%, não como 2,5%. `"{:.1%}"` interpreta a entrada como proporção e a representa multiplicada por cem. Esses formatos Python usam ponto decimal; a função não converte automaticamente a convenção para português brasileiro.

## 9. Como usar este recurso no Hub?

Prepare a importação conforme o [guia da coleção](../../README.md). Este bloco usa dados sintéticos locais e não instala pacotes, reinicia a sessão nem grava arquivos.

```python
import pandas as pd
from hub_snippets.display.dataframe_styled import display_styled

resumo = pd.DataFrame({"segmento": ["A", "B"], "variacao": [-0.025, 0.012]})
html = display_styled(
    resumo,
    highlight_cols=["variacao"],
    format_dict={"variacao": "{:.1%}"},
)
assert isinstance(html, str) and "-2.5%" in html
assert resumo.loc[0, "variacao"] == -0.025
```

No Databricks, `displayHTML(html)` apresenta a string. O [notebook de exemplo](exemplo_dataframe_styled.py) é diferente deste bloco: executa `%pip install jinja2` e `%restart_python` antes de preparar imports. Isso modifica o ambiente Python e reinicia seu estado. Leia essas células antes de executar; o notebook não grava tabela persistente.

### Caminho V04 — tabela com tema explícito

```python
from hub_snippets.display.dataframe_styled import display_styled_resolvido
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
html = display_styled_resolvido(resumo, tema, highlight_cols=["variacao"])
```

A rota V04 usa `brand.primary` no cabeçalho, `table.header_text` no texto do cabeçalho e `semantic.negative` no realce de negativos. O DataFrame, `highlight_cols` e `format_dict` mantêm o contrato histórico. A fonte da tabela permanece fixa porque o contrato V01 não atribui `font.family` a esse consumidor.

## 10. Decisões e configurações que mais importam

Escolha `highlight_cols` pelo significado do sinal. `format_dict` muda representação, não unidades armazenadas. Formatar antes ou durante a renderização são escolhas distintas: preformatar em texto pode perder o realce numérico.

Para apresentação brasileira, consulte [format_br](../../constants/format_br/README.md) e seus limites ou configure o Styler diretamente. Não suponha que `"{:,.0f}"` produza `1.000`: esse padrão usa vírgula para milhares. A função não expõe parâmetros de escape, paginação ou limite de linhas.

## 11. Limitações, riscos e armadilhas

Mesmo em uma escolha adequada, uma coluna errada pode ficar sem realce sem emitir erro. Valores `Decimal` negativos e strings `"-3"` não obedecem necessariamente à mesma regra dos números Python. HTML sem escape explícito pode interpretar marcação de célula; a documentação do pandas recomenda entrada segura e escape quando o conteúdo não é confiável.

O estilo pode depender de opções globais do pandas, da versão instalada e do renderizador. IDs de tabela gerados automaticamente podem mudar entre chamadas, sem mudar os dados. Comparar o HTML inteiro por igualdade literal não é um teste estável de conteúdo. Não trate a cor como alerta acessível completo nem a página como evidência de cálculo correto.

## 12. Quais são as alternativas?

Para inspeção rápida, uma tabela comum evita complexidade visual. Para realce por limites de negócio, escape e formatação avançada, configure o Styler do pandas de maneira explícita, mantendo testes.

Para poucos indicadores destacados, [kpi_card](../../visual/kpi_card/README.md) atende a outro formato de apresentação. Para armazenar resultados, use a saída de dados apropriada ao processo; este helper devolve uma representação HTML, não um contrato de intercâmbio tabular.

## 13. Como saber se o resultado faz sentido?

Compare a tabela antes e depois da chamada: valores e tipos devem permanecer iguais. Inclua no teste um negativo, um zero e um positivo, conferindo se somente o negativo na coluna selecionada recebe a regra de destaque.

Verifique manualmente uma proporção conhecida, como 0,025, contra a unidade exibida. Se a coluna esperada não for destacada, examine nome, tipo e sinal antes de interpretar como ausência de problema. Com texto externo, não experimente a segurança no navegador de produção: use uma camada de renderização com política de escape explicitamente validada.

## 14. Arquivos relacionados e próximos passos

A [implementação](dataframe_styled.py) define a regra de realce; a [fachada](__init__.py) exporta `display_styled`. O [notebook](exemplo_dataframe_styled.py) demonstra também a formatação de contagens. O [guia da coleção](../../README.md) orienta a preparação do import.

## 15. Referências

A documentação [Styler](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.io.formats.style.Styler.html) sustenta a distinção entre apresentação e dados e a orientação sobre conteúdo não confiável. [Styler.format](https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.format.html) explica formatos, escape e opções. Consulta em 2026-09-12; documentação vigente não comprova a versão do seu workspace.

O comportamento do Hub foi confrontado com [código](dataframe_styled.py), [API](__init__.py) e exemplo na base `c60f1e5`. Testes R03-B verificam conteúdo HTML e preservação dos dados; isso não homologa a renderização visual no Databricks. Autorrevisão de ChatGPT, sem auditoria independente.
