# `styles` — aparência reutilizável para blocos HTML

<!-- readme-objeto: 1.0.0 -->

> CSS descreve como um elemento aparece. Este módulo oferece trechos de CSS para uso explícito; ele não é um painel central que reestiliza todo o Hub.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Strings de estilo e uma família de fontes. |
| Para que serve? | Reutilizar aparência em HTML montado pelo autor. |
| Use quando... | Você precisa compor um bloco próprio e entende onde aplicar o estilo. |
| Evite quando... | Você espera mudar todos os componentes editando este arquivo. |
| Precisa de... | Python, Hub e um destino que renderize HTML/CSS. |
| Entrega... | Textos de estilo; nenhum bloco renderizado automaticamente. |

**Acesso direto:** [exemplo](exemplo_styles.py) · [implementação](styles.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

HTML descreve elementos como um título ou uma linha. **CSS** descreve sua aparência: cor, espaço ao redor, borda e fonte. Aqui, cada constante `STYLE_*` é uma string com declarações CSS, pronta para o atributo `style` de um elemento.

O módulo também fornece `FONT_FAMILY`. Não contém um arquivo de fonte nem instala tipografia. **Na implementação lida, os componentes visuais da biblioteca não importam este módulo**; eles mantêm seus próprios estilos. O recurso serve a quem o usa explicitamente.

## 2. Que problema este recurso resolve?

“Como montar um cabeçalho próprio sem redigitar sua borda, fundo e espaçamento?” O módulo oferece esses trechos. Reduz repetição no código consumidor que os adota, mas não elimina as duplicações já existentes nos componentes.

## 3. Quando faz sentido usar?

Use uma constante ao construir um bloco HTML pequeno que ainda não esteja coberto por um componente. Por exemplo, `STYLE_SECTION_HEADER` pode organizar um aviso explicativo; `STYLE_INDEX_ITEM` pode dar aparência consistente a itens de navegação.

O uso é apropriado quando o autor controla a estrutura do HTML e os textos inseridos. Para uma função pronta de cartão ou selo, prefira o componente correspondente, sem pressupor que ele leia estas constantes.

## 4. Quando não usar?

Não use este arquivo como controle global de identidade visual. Alterar `STYLE_KPI_CARD` não muda automaticamente o retorno de `kpi_card_html`: são implementações distintas.

Não escolha CSS inline como solução completa para uma aplicação com temas, navegação e acessibilidade. Também não presuma que todo destino de e-mail ou documento processe o mesmo HTML. Verifique o renderizador; uma string válida não garante a aparência pretendida.

## 5. Como funciona, intuitivamente?

Na importação, o módulo monta strings. Parte das cores vem de `constants.colors`, usando expressões Python; outras continuam como valores literais. Quando o autor insere uma constante em um atributo `style`, o destino interpreta as declarações.

Os textos são montados naquele momento. Mudar uma variável de cor depois da importação não reconstrói automaticamente strings já criadas. O módulo não registra tema no Plotly nem muda o CSS de páginas já abertas.

## 6. Exemplo de situação

Você prepara um aviso sintético: “Base de demonstração; não usar para decisão comercial”. Um bloco com borda e espaço interno pode separar esse aviso das métricas.

`STYLE_SECTION_HEADER` oferece a aparência; o texto explica a condição. A solução não cria uma nova categoria de alerta e não altera os demais cabeçalhos do Hub.

## 7. O que você precisa antes de usar?

É necessário que `hub_snippets.constants.styles` e `colors` estejam importáveis. Nenhum dos dois calcula estatísticas ou exige Spark. Para visualizar, o destino precisa aceitar HTML/CSS. O notebook existente usa a preparação Databricks com `spark` e `displayHTML`.

Ao montar HTML manualmente, trate texto externo com `html.escape`. A constante de estilo não faz esse tratamento por você; ela contém somente CSS. A [documentação de Python](https://docs.python.org/3/library/html.html#html.escape) explica o escape de caracteres.

## 8. O que este recurso entrega?

Você recebe nove constantes públicas: uma família de fontes e oito trechos de estilo. Entre eles estão cabeçalho, cartão, divisórias leve/pesada, estados de badge e item de índice. Não há uma função que recebe dados e retorna um relatório.

`STYLE_BADGE_WARN`, por exemplo, descreve fundo, cor de texto, espaço e tamanho. O nome “warn” não confere a severidade de um problema nem a acessibilidade do par de cores.

## 9. Como usar este recurso no Hub?

Consulte o [exemplo](exemplo_styles.py) para visualizar os estilos no notebook. Não há gravação de tabelas; o exemplo compõe saídas HTML. Após a preparação da [coleção](../../README.md), este trecho gera texto HTML sem exibi-lo:

```python
from html import escape
from hub_snippets.constants.styles import STYLE_SECTION_HEADER
mensagem = "Base sintética: conferir antes de reutilizar."
html = f'<div style="{STYLE_SECTION_HEADER}">{escape(mensagem)}</div>'
print("border-left" in html)
```

O trecho portátil retorna `True` e foi conferido. Para renderizar no Databricks, a documentação indica `displayHTML`; isso é uma etapa do notebook, não uma chamada feita pelo módulo.

## 10. Decisões e configurações que mais importam

Escolha o estilo pelo papel do bloco e confira a combinação de texto, fundo e tamanho. `FONT_FAMILY` é uma lista de preferência: não incorpora fontes ao resultado. Na versão atual, os demais estilos já contêm suas próprias strings de fonte; reatribuir `FONT_FAMILY` não atualiza todas elas.

Evite modificações improvisadas na constante compartilhada. Uma necessidade de novo tema deve ser tratada como alteração de produto, com revisão dos consumidores e efeitos.

## 11. Limitações, riscos e armadilhas

Há duplicação de CSS com componentes da pasta `visual`. O módulo já importa `colors`, ao contrário do que dizia uma passagem antiga do notebook, mas isso não o transforma em fonte única de todos os estilos.

O par de atenção `#B26A00` sobre `#FFF8E1` tem contraste calculado de aproximadamente **3,99:1**, abaixo de 4,5:1 para texto comum, e o estilo declara 11px. Esta limitação foi documentada, não corrigida por troca silenciosa de cor. A [WCAG](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) orienta a avaliação; o nome de uma constante não constitui conformidade.

## 12. Quais são as alternativas?

[badge](../../visual/badge/README.md), [divider](../../visual/divider/README.md) e [kpi_card](../../visual/kpi_card/README.md) fornecem elementos completos para necessidades específicas. Texto Markdown pode ser suficiente quando a prioridade é portabilidade.

Para figuras Plotly, consulte [theme_plotly](../../visual/theme_plotly/theme_plotly.py). CSS inline de um bloco HTML não é a configuração interna de uma figura Plotly.

## 13. Como saber se o resultado faz sentido?

Confira o elemento no destino, o contraste, a quebra de linha e a leitura com zoom. Verifique se o texto sem decoração ainda informa a condição.

Se um componente não mudar após editar uma constante, consulte seus imports antes de insistir: ele pode não ser consumidor de `styles`. Um teste de igualdade de strings confirma o trecho gerado, não a renderização em cada cliente.

## 14. Arquivos relacionados e próximos passos

[styles.py](styles.py) define os trechos; [__init__.py](__init__.py) expõe os nomes; [exemplo_styles.py](exemplo_styles.py) demonstra sua aplicação. [colors](../colors/README.md) fornece parte das cores; a [coleção](../../README.md) apresenta as rotas.

## 15. Referências

O [módulo](styles.py) e os imports dos componentes delimitam o uso real. [Python — html.escape](https://docs.python.org/3/library/html.html#html.escape) sustenta o tratamento do texto. [Databricks — HTML em notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-media#include-html) explica o destino de renderização; [WCAG — contraste](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) sustenta a ressalva. Consulta em 12/09/2026.

Revisão R03-A: análise estática dos consumidores, testes portáteis e contraste numérico. Não houve mudança de CSS, homologação no workspace ou auditoria independente.
