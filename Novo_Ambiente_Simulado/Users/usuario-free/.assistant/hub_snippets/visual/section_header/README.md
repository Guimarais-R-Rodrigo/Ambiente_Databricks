# `section_header` — identifique a etapa que o leitor está vendo

<!-- readme-objeto: 1.0.0 -->

> Crie um cabeçalho visual consistente para orientar a leitura, usando o roteiro da EDA ou textos explícitos.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Gerador de cabeçalho HTML. |
| Para que serve? | Identificar uma seção com título e descrição. |
| Use quando... | A análise precisa de orientação visual consistente. |
| Evite quando... | Você precisa inferir etapas ou certificar sua execução. |
| Precisa de... | Python e constantes do Hub; renderizador para a visualização. |
| Entrega... | String HTML com emoji, título e descrição tratados como texto. |

**Acesso direto:** [exemplo](exemplo_section_header.py) · [implementação](section_header.py) · [API pública](__init__.py). Leia os requisitos e os efeitos na seção 9 antes de executar o notebook inteiro.

## 1. O que é?

Um cabeçalho marca uma nova parte do documento e ajuda a pessoa a reconhecer o assunto antes de ler os detalhes. `section_header_html` produz esse cabeçalho com um emoji, um título e uma descrição curta.

Ele pode preencher esses campos pelo número da etapa de EDA, isto é, análise exploratória de dados, ou receber uma seção personalizada. É apresentação de conteúdo declarado, não uma ferramenta que descobre onde termina a preparação e começa a modelagem.

## 2. Que problema este recurso resolve?

“Como evitar que cada notebook use um nome diferente para a mesma etapa?” Consultar o mapa comum reduz divergências de rótulos e ajuda uma pessoa que chega ao meio da análise a se localizar.

O resultado não certifica que a atividade mencionada aconteceu. Um cabeçalho de qualidade de dados pode existir antes da primeira verificação: sua presença é orientação, não evidência.

## 3. Quando faz sentido usar?

Use quando o notebook segue o roteiro do Hub e a etapa escolhida realmente descreve o conteúdo seguinte. Isso favorece consistência com o índice.

Também faz sentido em uma seção fora do roteiro, como uma comparação de políticas fictícias, desde que você forneça título e descrição próprios sem forçar uma numeração inadequada. Em documentos curtos, um título Markdown pode cumprir o mesmo objetivo com menos elementos visuais.

## 4. Quando não usar?

Não use um número apenas para obter um ícone bonito quando o conteúdo corresponde a outro assunto. Um cabeçalho “Qualidade de Dados” sobre uma seção de treinamento cria uma expectativa errada, mesmo que o HTML esteja perfeito.

Não use o retorno como barra de progresso, resultado de teste ou navegador clicável. O helper não gera badges de aprovação, não procura células e não insere links de salto.

## 5. Como funciona, intuitivamente?

Se `etapa` existe em `SECOES_EDA`, a função consulta o mapa para preencher campos não informados. Valores explicitamente fornecidos e não vazios têm prioridade. Depois, aplica padrões aos campos que continuarem vazios.

Antes de montar o HTML, o código converte os campos para texto e aplica `html.escape`, que representa sinais como `<` e `>` de modo que apareçam como conteúdo, não como marcação. A rota legada usa as constantes históricas; `section_header_html_resolvido` obtém container, título e descrição da materialização central da V04.

## 6. Exemplo de situação

Em um notebook fictício, a etapa 3 avalia faltantes e duplicações. Seu cabeçalho pode usar o nome do roteiro, com uma descrição particular informando o período examinado.

Em outra seção, “Comparação de políticas”, não existe correspondência obrigatória com as nove etapas. Nesse caso, informe textos explícitos. O critério é orientar o leitor sobre o conteúdo real, e não maximizar a quantidade de componentes padronizados.

## 7. O que você precisa antes de usar?

Para gerar a string, você precisa de Python e da importação do Hub configurada. Não são necessárias bibliotecas analíticas ou uma base de dados. Para visualizar o resultado, precisa de um ambiente capaz de renderizar HTML.

Escolha `etapa` entre as chaves do mapa ou omita-a para uma seção personalizada. O código não rejeita um número desconhecido: sem textos explícitos, pode produzir um cabeçalho genérico. Confira a entrada; não interprete ausência de erro como validação do roteiro.

## 8. O que este recurso entrega?

O retorno é uma string HTML com um título de nível `h3` e um parágrafo descritivo. Quando não há informações, os padrões são o emoji 📌, o título “Seção” e “Descrição não informada.”.

Campos vazios são substituídos pelo mapa ou pelos padrões. Por isso, passar `descricao=""` não é uma forma de remover o parágrafo. Marcação fornecida no título aparece como texto escapado, não como formatação HTML arbitrária.

## 9. Como usar este recurso no Hub?

Configure o import pelo [guia da coleção](../../README.md). Este bloco não consulta tabelas, altera sessão de tema nem grava arquivos.

```python
from hub_snippets.visual.section_header import section_header_html

cabecalho = section_header_html(
    etapa=3,
    descricao="Verificar faltantes e duplicações na base sintética.",
)
assert "Etapa 3" in cabecalho
assert "base sintética" in cabecalho
print(cabecalho[:80])
```

No notebook Databricks, `displayHTML(cabecalho)` mostra o resultado. O [exemplo completo](exemplo_section_header.py) consulta `current_user()` com Spark apenas para configurar o caminho da biblioteca. O helper é independente de Spark. O notebook não grava tabelas persistentes.

### Caminho V04 — cabeçalho com tema explícito

A função `section_header_html_resolvido(theme, ...)` mantém o preenchimento por `SECOES_EDA`, os defaults e o escape da rota legada. `brand.primary`, superfícies, texto, fonte e dimensões `section.*` passam a vir do `ResolvedTheme` notebook recebido explicitamente.

## 10. Decisões e configurações que mais importam

`etapa` determina o preenchimento pelo mapa, mas `emoji`, `titulo` e `descricao` podem substituí-lo com valores não vazios. Essa flexibilidade exige coerência: um número correto com título de outro assunto continua enganoso.

A ordem das chamadas e a escolha de números são responsabilidade do autor. A função não incrementa etapas automaticamente. Textos muito longos devem ser resumidos no cabeçalho e desenvolvidos na seção seguinte, para não transformar a orientação em outro bloco denso.

## 11. Limitações, riscos e armadilhas

Uma etapa inválida pode passar silenciosamente para padrões genéricos. Strings vazias não apagam campos. Duplicar a mesma etapa no notebook não é impedido.

Carregar outro tema não altera `section_header_html` nem HTML já exibido. Somente a chamada explícita de `section_header_html_resolvido(theme, ...)` usa os tokens do tema recebido. Escape de texto reduz a interpretação de marcação, mas não comprova acessibilidade, contraste suficiente ou semântica correta do título; essas checagens continuam necessárias no destino.

## 12. Quais são as alternativas?

Um título Markdown é apropriado quando a prioridade é estrutura, simplicidade e integração com o sumário nativo. O cabeçalho HTML pode complementá-lo, mas não deve ser presumido como substituto dessa navegação.

Para o roteiro inicial, consulte [index_generator](../index_generator/README.md). Para separar visualmente blocos sem anunciar um novo assunto, [divider](../divider/README.md) é uma alternativa menor. Esses componentes têm papéis diferentes.

## 13. Como saber se o resultado faz sentido?

Teste uma etapa conhecida e confira título e descrição contra o mapa. Teste também uma seção personalizada e um título contendo `<` e `>`: esses sinais devem permanecer texto na saída.

No documento final, verifique sequência, repetição de números e correspondência entre cabeçalho e conteúdo. Se surgir “Seção” ou a descrição genérica sem intenção, corrija os parâmetros. Confira a legibilidade no notebook real; obter uma string não garante um cabeçalho utilizável por todos os leitores.

## 14. Arquivos relacionados e próximos passos

A [implementação](section_header.py) define padrões, precedência e escape; a [fachada](__init__.py) define a função exportada. O [notebook](exemplo_section_header.py) demonstra etapas e personalização. [Emojis](../../constants/emojis/README.md) explica o mapa; [styles](../../constants/styles/README.md) esclarece os limites da centralização visual.

## 15. Referências

O comportamento foi confrontado com [section_header.py](section_header.py) na base `c60f1e5`. A documentação [html.escape](https://docs.python.org/3/library/html.html) sustenta o tratamento dos caracteres. A [organização de células Databricks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-cells) explica a navegação por títulos. Consulta em 2026-09-12.

Os testes R03-B verificam preenchimento, sobrescrita, fallback e escape. Não são homologação visual ou de acessibilidade no workspace. Autorrevisão de ChatGPT, sem auditoria independente.
