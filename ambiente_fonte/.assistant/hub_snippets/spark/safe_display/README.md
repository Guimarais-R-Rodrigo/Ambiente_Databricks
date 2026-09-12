# `safe_display` — limitar a prévia antes de chamar o renderer

<!-- readme-objeto: 1.0.0 -->

Exibir poucas linhas não significa que toda transformação anterior foi barata, mas inserir um `limit` antes do renderer evita pedir uma prévia ilimitada por descuido. `safe_display` faz esse recorte, informa se havia mais linhas e delega a renderização a uma função explícita.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Wrapper de prévia para DataFrame Spark, com limite e renderer injetável. |
| Para que serve? | Evitar exibição acidentalmente grande e tornar truncamento explícito. |
| Use quando... | Você quer inspecionar uma prévia e aceita que ela não é uma amostra estatística. |
| Evite quando... | Precisa filtrar casos específicos, estimar a população ou reduzir custo de agregação já feita. |
| Precisa de... | DataFrame, `limit > 0` e normalmente `display_fn=display` no notebook. |
| Entrega... | Nenhum objeto; chama o renderer com até `limit` linhas e pode imprimir aviso. |

Leia a [implementação](safe_display.py), a [fachada](__init__.py) e o [notebook](exemplo_safe_display.py). O helper não coleta a tabela inteira para Python, mas executa uma contagem limitada e a ação realizada pelo renderer.

## 1. O que é?

`safe_display` é um wrapper customizado para prévias de DataFrames Spark. Ele cria `df.limit(limit + 1)`, conta esse prefixo para descobrir se houve truncamento e entrega `preview.limit(limit)` à função de exibição.

Ele não é uma API nativa do Databricks e não substitui `display`. O parâmetro `display_fn` existe porque uma biblioteca importada não herda automaticamente a função `display` injetada no escopo de um notebook.

## 2. Que problema este recurso resolve?

A pergunta é: “Como mostrar uma prévia com um teto explícito e deixar claro que existem mais linhas?”. Isso reduz o risco de confundir a interface truncada com a população completa e torna o renderer substituível em testes.

Ele não transforma um pipeline caro em barato. Se o DataFrame depende de uma agregação global, join complexo ou outra etapa que precisa ser executada antes do limite, esse custo continua existindo.

## 3. Quando faz sentido usar?

Use durante exploração para inspecionar schema/valores e mostrar um número pequeno de linhas. Também é útil em testes, passando uma função simples que registra o DataFrame recebido em vez de depender da interface do notebook.

O helper faz mais sentido quando o objetivo é **prévia**, não amostragem representativa.

## 4. Quando não usar?

Não use para localizar uma linha específica: filtre pela condição. Não use para estimar distribuição, média ou prevalência; o prefixo limitado não é amostra aleatória.

Contraexemplo: um `groupBy(...).count()` sobre bilhões de linhas é passado a `safe_display(limit=10)`. O resultado exibido tem dez linhas, mas a agregação necessária para produzi-las pode continuar processando a base inteira.

## 5. Como funciona, intuitivamente?

1. valida `limit > 0`;
2. cria uma prévia de até `limit + 1` linhas;
3. conta somente essa prévia;
4. se houver a linha adicional, considera o resultado truncado;
5. opcionalmente imprime `Displaying N+ rows (limit=N).`;
6. resolve o renderer: `display_fn` informado ou `globals().get("display")` dentro do módulo;
7. chama o renderer com no máximo `limit` linhas.

Na importação normal, o `display` do notebook não faz parte dos globais do módulo; passe-o explicitamente.

## 6. Exemplo de situação

Uma base sintética tem 5.000 linhas e você quer somente verificar algumas colunas. `safe_display(base, limit=10, display_fn=display)` conta no máximo 11 linhas na prévia para detectar truncamento e entrega dez ao renderer.

A saída textual `10+` informa que havia mais dados; não informa quantas linhas existem no total.

## 7. O que você precisa antes de usar?

Você precisa de DataFrame PySpark e `limit` positivo. No notebook, passe `display_fn=display`; fora dele, forneça qualquer callable compatível com um DataFrame Spark.

`msg=False` desativa apenas a mensagem; não elimina a contagem limitada usada para detectar truncamento. O helper não valida a assinatura do callable antes de chamá-lo.

## 8. O que este recurso entrega?

A função retorna `None`. Seu efeito é chamar o renderer. Quando `msg=True`, imprime a quantidade mostrada e acrescenta `+` quando observou `limit + 1` linhas.

Não retorna o DataFrame limitado, não retorna total de linhas e não persiste o resultado.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.spark.safe_display import safe_display

safe_display(df, limit=100, display_fn=display)
```

O [notebook](exemplo_safe_display.py) demonstra a exceção quando `display_fn` não é passado, a chamada correta e a injeção de um renderer de teste. Ele usa somente dados sintéticos.

## 10. Decisões e configurações que mais importam

`limit=1000` é apenas o default local. Escolha um número pequeno o bastante para a tarefa de inspeção. `msg=True` torna o truncamento visível fora da renderização.

`display_fn` é a decisão de integração: no Databricks notebook, passe a função `display` disponível naquele escopo; em teste, use uma função controlada.

## 11. Limitações, riscos e armadilhas

O helper realiza pelo menos a ação `preview.count()` e o renderer normalmente dispara outra ação. Não use “não faz count da tabela inteira” como sinônimo de “não custa nada”.

`limit` pode ser empurrado no plano em alguns casos, mas transformações anteriores podem precisar de processamento amplo. O helper não impede `collect`, `toPandas` ou outras ações em código ao redor.

Sem `display_fn`, a chamada importada normalmente gera `RuntimeError`. Isso é comportamento atual do contrato, não detecção automática confiável da interface.

## 12. Quais são as alternativas?

Para uma inspeção pontual, `df.limit(n).show()` é mais simples e funciona fora da interface rica. Para obter uma amostra aleatória/estratificada, use [`smart_sample`](../smart_sample/README.md). Para reduzir dados por condição de negócio, use `filter`.

A alternativa certa depende de querer prévia, amostra ou subconjunto lógico — são operações diferentes.

## 13. Como saber se o resultado faz sentido?

Passe um DataFrame pequeno e um renderer de teste que conte as linhas recebidas. Com cinco linhas e `limit=3`, o renderer deve receber três e a mensagem deve indicar `3+`. Com duas linhas e o mesmo limite, recebe duas sem `+`.

Teste também `limit=0` para confirmar a recusa. Se a preocupação é custo, examine o plano do DataFrame real; o tamanho da prévia por si só não demonstra economia de processamento.

## 14. Arquivos relacionados e próximos passos

- [Implementação](safe_display.py): recorte, contagem e renderer.
- [Fachada](__init__.py): exporta `safe_display`.
- [Notebook](exemplo_safe_display.py): comportamento com e sem `display_fn`.
- [`smart_sample`](../smart_sample/README.md): amostragem em vez de prévia.
- [Coleção](../../README.md): demais operações Spark.

## 15. Referências

O comportamento foi conferido em `safe_display.py`, na fachada e no notebook desta pasta. As afirmações de custo ficam deliberadamente limitadas ao que a função faz: prefixo limitado, uma contagem desse prefixo e chamada do renderer.

A R04-A testa o helper com renderer injetado e Spark local no runner. Isso não é benchmark nem homologação da interface Databricks.
