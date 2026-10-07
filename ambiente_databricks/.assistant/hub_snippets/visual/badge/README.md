# `badge` — selos para comunicar um estado

<!-- readme-objeto: 1.0.0 -->

> Um badge é um selo curto de status. Este helper formata a mensagem; somente a função de score aplica faixas internas, que não substituem uma política de negócio.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Funções que devolvem selos HTML. |
| Para que serve? | Destacar estado ou score junto da evidência. |
| Use quando... | O estado já foi apurado e pode ser resumido. |
| Evite quando... | Uma cor seria usada para aprovar um modelo sem critérios. |
| Precisa de... | Texto controlado; score numérico e escala conhecida quando aplicável. |
| Entrega... | String HTML; a renderização fica com o notebook. |

**Acesso direto:** [exemplo](exemplo_badge.py) · [implementação](badge.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

Um **badge** é uma etiqueta visual compacta, como “Atenção” ou “Concluído”. Pode reduzir a procura por um estado no relatório, desde que o motivo continue acessível.

O caminho legado fornece `badge_status`, `badge_score` e `badge_inline`. As variantes `_resolvido` mudam somente a apresentação quando recebem um tema explícito. O módulo não é um motor de qualidade de dados: `badge_status` recebe o estado escolhido e `badge_score` continua usando os mesmos limites fixos.

## 2. Que problema este recurso resolve?

“Como tornar visível a conclusão de uma checagem sem obrigar o leitor a interpretar todos os números primeiro?” O selo comunica essa conclusão. A evidência, a regra e as exceções não deixam de ser necessárias: um selo verde sem critério pode esconder mais do que esclarecer.

## 3. Quando faz sentido usar?

Use `badge_status` para um diagnóstico já calculado, acompanhado da condição que o produziu. Use `badge_inline` para uma observação neutra. Considere `badge_score` somente quando a escala tiver sentido e seus cortes internos forem adequados ao contexto.

Por exemplo, “Chave única: 20/20” pode resumir uma checagem de unicidade. O texto precisa distinguir “teste passou” de “resultado ainda não conferido”.

## 4. Quando não usar?

Não transforme AUC, PSI ou risco em selo positivo apenas porque o número se encaixa num corte visual. Esses indicadores têm interpretações próprias e não compartilham necessariamente uma escala “quanto maior, melhor”.

Se a política não usar os cortes de 0,5 e 0,8 da função de score, prefira calcular a classificação fora dela e usar `badge_status`, deixando a regra visível. Não use `max=0` para representar avaliação válida.

## 5. Como funciona, intuitivamente?

`badge_status` seleciona CSS conforme `tipo`, converte a mensagem para texto e aplica `html.escape` antes de inseri-la em um elemento `span`. Essa conversão faz caracteres especiais aparecerem como texto, em vez de serem interpretados como marcação HTML.

`badge_score` divide `valor` por `max`, escolhe `ok` a partir de 0,8, `warn` a partir de 0,5 e `fail` abaixo disso. Depois formata os números sem casas decimais. `badge_inline` equivale ao tipo informativo.

## 6. Exemplo de situação

Um diagnóstico sintético encontrou três registros sem identificação em 100 contatos. Você decide que a revisão é necessária e escreve “Atenção: 3/100 sem identificação”, usando `badge_status(..., "warn")`.

O helper não leu a tabela nem validou o denominador. O selo resume uma conclusão já produzida; o relatório deve manter a contagem e a regra que justificaram o estado.

## 7. O que você precisa antes de usar?

A biblioteca precisa estar importável. O módulo usa a biblioteca padrão de Python e cores do Hub; não exige Spark para produzir a string. Para renderização, é necessário um destino HTML, como o `displayHTML` documentado para notebooks Databricks.

Para score, confira valores numéricos finitos, escala e máximo positivo antes da chamada. A anotação de tipo não impõe essas condições. O notebook existente usa `spark` para preparar o caminho do pacote; não grava tabelas de negócio.

APIs públicas (retorno `str`; `theme` é um `ResolvedTheme` de contexto `notebook` nas variantes resolvidas):

- `badge_status(texto: str, tipo: str='ok')`
- `badge_score(valor: float, max: float=100)`
- `badge_inline(texto: str)`
- `badge_status_resolvido(texto: str, theme: ResolvedTheme, tipo: str='ok')`
- `badge_score_resolvido(valor: float, theme: ResolvedTheme, max: float=100)`
- `badge_inline_resolvido(texto: str, theme: ResolvedTheme)`

A geração legada usa Python e o Hub. As rotas resolvidas revalidam o tema e exigem as [dependências de validação](../../requirements-temas.txt), sem instalação automática.

## 8. O que este recurso entrega?

O retorno é texto HTML, não um objeto de gráfico nem uma decisão persistida. `badge_status` aceita `ok`, `warn`, `fail` e `info`; um tipo desconhecido utiliza silenciosamente o estilo `info`. Isso não confirma que o argumento estava correto.

O score exibe números arredondados, mas decide a faixa usando a razão original. Assim, `79.6/100` pode aparecer como `Score: 80/100` no estilo de atenção. A diferença não é um novo corte; é efeito da apresentação.

## 9. Como usar este recurso no Hub?

No [exemplo](exemplo_badge.py), o notebook chama `displayHTML` para exibir os selos. Ele não persiste tabelas. Após preparar a importação pela [coleção](../../README.md), este trecho gera um selo de texto:

```python
from hub_snippets.visual.badge import badge_status
html = badge_status("Atenção: 3/100 sem identificação", "warn")
print("3/100" in html)
```

Saída portátil conferida: `True`. Para ver o selo, renderize o retorno no ambiente apropriado. Não foi o helper que realizou a contagem citada.

### Tema explícito — badge com tema explícito

```python
from hub_snippets.visual.badge import badge_status_resolvido
from hub_snippets.visual.tema import load_reference_theme

tema = load_reference_theme("notebook")
html = badge_status_resolvido("Conferido", tema, "ok")
```

Os cortes de `badge_score` não viram tokens e não mudam com o tema. Apenas `status.*`, superfície informativa e dimensões do badge são materializados pelo tema. Um tipo desconhecido continua caindo no estilo informativo.

## 10. Decisões e configurações que mais importam

Em `badge_status`, escolha `tipo` de modo explícito; o padrão é `"ok"`. Em `badge_score`, o máximo padrão é 100. Os limiares não são parâmetros configuráveis: estão no corpo da função.

Se um número estiver perto do corte, apresente a precisão necessária em texto ao lado ou use mensagem própria em `badge_status`. Não ajuste o valor real só para alinhar a cor à impressão causada pelo arredondamento.

## 11. Limitações, riscos e armadilhas

`max=0` produz razão interna zero e pode exibir algo como `Score: 1/0` em estado de falha; não há recusa do caso. Valores negativos ou acima do máximo também não são limitados automaticamente. Essa tolerância é limitação de validação, não recomendação de uso.

O estilo `warn` usa texto `#B26A00` sobre `#FFF8E1`, com contraste calculado próximo de **3,99:1**, inferior a 4,5:1 para texto comum; a fonte declarada é de 11px. A [WCAG](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) orienta a avaliação. Não declare o componente plenamente acessível; valide a combinação efetivamente usada.

Na rota resolvida, cores e dimensões de estado vêm de `constants.styles` materializado a partir do tema; a rota legada preserva os valores históricos. O escape de HTML não anonimiza conteúdo: mensagens ainda podem expor dados se o autor os inserir.

## 12. Quais são as alternativas?

Texto direto ou uma coluna de status pode ser melhor para muitos registros. [kpi_card](../kpi_card/README.md) reúne valores de resumo sem aplicar essas faixas. Uma classificação externa seguida de `badge_status` preserva uma política distinta sem alterar o helper.

## 13. Como saber se o resultado faz sentido?

Confira a evidência e o tipo escolhido. Teste os valores imediatamente abaixo e no corte: 49/50 e 79/80, com máximo 100. Compare também valores decimais próximos para perceber o arredondamento.

Se o estado estiver incorreto, revise regra, escala e argumento; não troque somente a cor. Confira contraste e legibilidade no destino e mantenha uma descrição textual independente do estilo.

## 14. Arquivos relacionados e próximos passos

[badge.py](badge.py) define estilo, escape e cortes; [__init__.py](__init__.py) expõe as funções; [exemplo_badge.py](exemplo_badge.py) demonstra seu uso. [colors](../../constants/colors/README.md) explica as cores compartilhadas e a [coleção](../../README.md) orienta a navegação.

## 15. Referências

O [código](badge.py) fundamenta os cortes e a ausência de validações mencionadas. [Python — html.escape](https://docs.python.org/3/library/html.html#html.escape) explica o tratamento do texto; [Databricks — HTML](https://docs.databricks.com/aws/en/notebooks/notebook-media#include-html) documenta a renderização; [WCAG — contraste](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) fundamenta a ressalva. Consulta em 12/09/2026.

A [implementação](badge.py) e a [fachada](__init__.py) delimitam o contrato. Confira conteúdo, escape e aparência no destino: gerar uma string não homologa a interface nem acessibilidade.

[Registro técnico de referência](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/readmes_objetos/RELATORIO_R03A.md): consulte data, ambiente e alcance de cada teste; o registro não é homologação do destino.
