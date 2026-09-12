# `index_generator` — apresente o roteiro de uma análise

<!-- readme-objeto: 1.0.0 -->

> Gere uma lista coerente das etapas que você declara para o notebook, sem prometer navegação automática nem execução da análise.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Gerador de índice descritivo de EDA. |
| Para que serve? | Apresentar o roteiro adotado e a numeração canônica. |
| Use quando... | O notebook segue as etapas do Hub e você informa as que estão presentes. |
| Evite quando... | É preciso descobrir células, medir conclusão ou gerar links clicáveis. |
| Precisa de... | Python, mapa `SECOES_EDA` e importação configurada. |
| Entrega... | String HTML ou Markdown com as etapas solicitadas. |

**Acesso direto:** [exemplo](exemplo_index_generator.py) · [implementação](index_generator.py) · [API pública](__init__.py). Leia os requisitos e os efeitos na seção 9 antes de executar o notebook inteiro.

## 1. O que é?

Um índice orienta o leitor sobre o que encontrará em um documento. Neste caso, EDA significa análise exploratória de dados: um roteiro que organiza o reconhecimento, a qualidade e a interpretação dos dados.

`gerar_indice_eda` lê os nomes e descrições do mapa do Hub e monta uma lista de etapas. O recurso não examina o notebook. Ele apresenta uma declaração feita por quem escreve a análise, não um inventário verificado das células.

## 2. Que problema este recurso resolve?

“Como mostrar o escopo desta análise usando os mesmos nomes que os demais notebooks?” A função evita redigitar rótulos e preserva a numeração das etapas selecionadas.

Ela ajuda a comunicar escopo, mas não comprova que uma etapa foi executada. Uma etapa ausente da lista pode estar fora do escopo, ter sido omitida por erro ou ainda estar planejada. Essa distinção precisa aparecer na explicação do notebook.

## 3. Quando faz sentido usar?

Use em um notebook extenso que siga o roteiro do Hub. Declare somente as etapas pertinentes e presentes, para que o índice seja um acordo claro com o leitor.

Também serve quando dois notebooks cobrem recortes diferentes do mesmo roteiro: manter os números originais facilita compará-los. Escolha HTML para um bloco visual no notebook ou Markdown para uma representação textual simples.

## 4. Quando não usar?

Não use como auditor de completude: pedir `[1, 3, 8]` não prova que inventário, qualidade e relatório foram feitos. Da mesma forma, pedir todas as etapas não cria as células correspondentes.

Para um documento que exige navegação clicável, prefira um sumário apropriado ao renderizador. O helper não cria links nem âncoras. Para um roteiro diferente do mapa do Hub, escreva um índice que reflita aquele processo em vez de atribuir significados diferentes aos mesmos números.

## 5. Como funciona, intuitivamente?

A entrada é uma sequência de números de etapas. Para cada número, a função consulta `SECOES_EDA` e adiciona emoji, título e descrição. Se `etapas_ativas` for `None`, ela percorre os números de 0 a 8. Se for uma lista, conserva a ordem e as repetições recebidas.

O parâmetro `markdown` muda apenas o formato da string. Não há varredura de células, ordenação automática, deduplicação ou acompanhamento de progresso. Os estilos HTML são montados no próprio módulo com cores importadas.

## 6. Exemplo de situação

Uma análise fictícia fará inventário inicial, avaliação de qualidade, análise de cada variável e síntese executiva. A pessoa responsável declara `[1, 3, 4, 8]`.

O índice mantém esses quatro números, em vez de renumerar como 1, 2, 3 e 4. Isso ajuda quem conhece o mapa a reconhecer o recorte. Ao lado do índice, o autor deve explicar por que as demais etapas não aparecem; o código não consegue distinguir uma exclusão justificada de uma omissão.

## 7. O que você precisa antes de usar?

O cálculo do texto usa Python e os módulos de constantes do Hub, sem pandas, Plotly ou Spark. Configure o caminho de importação. Para visualizar HTML é necessário um renderizador, como `displayHTML` no notebook Databricks; para apenas obter o texto, não.

Use uma lista de inteiros correspondentes às chaves de `SECOES_EDA`. Uma etapa inexistente resulta em `KeyError`, não é descartada. Texto como `"3"` não é automaticamente convertido no inteiro 3. Não use um conjunto quando a ordem for importante.

## 8. O que este recurso entrega?

O retorno é uma string. Em Markdown, ela contém um título e itens com descrição; em HTML, contém blocos visuais. A lista vazia produz apenas a estrutura de abertura, sem etapas. Repetições na entrada aparecem repetidas na saída.

Nenhum resultado representa estado “concluído”, qualidade medida, permissão ou execução. Também não há destinos de navegação no HTML: um item visual não é um botão.

## 9. Como usar este recurso no Hub?

Após preparar imports pelo [guia da coleção](../../README.md), execute este bloco, que não lê dados nem modifica arquivos.

```python
from hub_snippets.visual.index_generator import gerar_indice_eda

indice = gerar_indice_eda(etapas_ativas=[1, 3, 4, 8], markdown=True)
assert indice.index("Etapa 1") < indice.index("Etapa 3")
assert "Etapa 2" not in indice
print(indice)
```

Para a versão visual, obtenha `gerar_indice_eda([1, 3, 4, 8])` e apresente a string com `displayHTML`. O [notebook completo](exemplo_index_generator.py) usa a sessão Spark somente na preparação do caminho de importação; a função não precisa de Spark para montar o índice. Não há escrita persistente.

## 10. Decisões e configurações que mais importam

A decisão principal é o conteúdo de `etapas_ativas`. `None` inclui todas as nove etapas, enquanto `[]` não inclui nenhuma. A ordem solicitada é a ordem mostrada. Uma duplicação acidental não será corrigida pela função.

`markdown=False` é o padrão visual; `True` devolve Markdown. Mudar esse formato não torna os itens clicáveis. Alterações aprovadas no mapa de constantes podem afetar futuras gerações, mas não reescrevem strings já produzidas.

## 11. Limitações, riscos e armadilhas

Mesmo quando o roteiro é adequado, o índice pode envelhecer se o notebook mudar e ninguém atualizar a lista. Valide a correspondência a cada reorganização.

O HTML usa os textos do mapa diretamente, sem uma camada geral de escape. Preserve esse mapa como conteúdo controlado; não o substitua por texto externo arbitrário. Aparência e emojis variam conforme fonte e renderizador. Uma lista legível não substitui títulos reais de seção nem uma revisão de acessibilidade.

## 12. Quais são as alternativas?

Um índice manual curto pode ser mais adequado para um roteiro específico. Para navegação automática no Databricks, o sumário nativo usa títulos Markdown e títulos de células; ele tem papel diferente deste índice descritivo.

Use [section_header](../section_header/README.md) para os cabeçalhos visuais correspondentes e [emojis](../../constants/emojis/README.md) para entender o mapa. Nenhum desses recursos verifica sozinho a execução das etapas.

## 13. Como saber se o resultado faz sentido?

Compare os itens com as seções realmente presentes e com a ordem de leitura. Teste uma seleção pequena e confirme que os números originais foram preservados.

Quando faltar uma etapa, revise a lista antes de concluir que a análise está incompleta. Se aparecer `KeyError`, confira o número contra `SECOES_EDA`. Se os itens não forem clicáveis, isso é o contrato esperado; a solução é usar o mecanismo de navegação adequado, não repetir a chamada.

## 14. Arquivos relacionados e próximos passos

A [implementação](index_generator.py) define a montagem; a [fachada](__init__.py) exporta a função. O [exemplo](exemplo_index_generator.py) mostra versão completa e filtrada. O [mapa de etapas](../../constants/emojis/README.md) é a origem do vocabulário; o [guia da coleção](../../README.md) explica a preparação.

## 15. Referências

O contrato específico é verificado em [index_generator.py](index_generator.py) e no [mapa](../../constants/emojis/emojis.py), base `c60f1e5`. A documentação oficial [Organize Databricks notebook cells](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-cells) descreve o sumário nativo e seus títulos; consultada em 2026-09-12.

Os testes R03-B conferem ordem, repetições, formato e recusa de chave inexistente. Isso não é teste de navegação no workspace nem auditoria de um notebook real. Revisão própria de ChatGPT, sem auditoria independente.
