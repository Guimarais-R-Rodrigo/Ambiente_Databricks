# `divider` — separadores para organizar o notebook

<!-- readme-objeto: 1.0.0 -->

> Um separador marca a passagem entre blocos. Estas funções produzem linhas HTML com pesos diferentes; os títulos continuam responsáveis por explicar o assunto.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Oito funções: quatro legadas e quatro variantes com tema explícito. |
| Para que serve? | Tornar fronteiras entre blocos mais fáceis de perceber. |
| Use quando... | Um notebook HTML precisa de hierarquia consistente. |
| Evite quando... | A linha substituiria títulos, contexto ou navegação. |
| Precisa de... | Biblioteca do Hub e destino HTML; nenhum dado. |
| Entrega... | String com uma ou duas linhas; sem efeitos na execução. |

**Acesso direto:** [exemplo](exemplo_divider.py) · [implementação](divider.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

Uma **divisória visual** é uma marca entre conteúdos, como um traço horizontal. Pode ajudar a perceber que um assunto terminou, mas não informa sozinha o que virá depois.

`divider_light`, `divider_medium`, `divider_heavy` e `divider_section` montam elementos HTML com espessuras e espaços diferentes. O nome “section” é uma convenção visual; não cria uma seção executável nem uma barreira de segurança no notebook.

## 2. Que problema este recurso resolve?

“Como mostrar a passagem de uma observação para outra seção sem repetir um traço idêntico em todo lugar?” O recurso fornece uma hierarquia visual pronta. Não organiza células automaticamente e não define ordem de execução.

## 3. Quando faz sentido usar?

Use uma linha leve entre observações próximas e uma mais destacada entre assuntos, mantendo títulos claros. A separação de seção pode introduzir um novo capítulo quando essa convenção for consistente no documento.

Em relatórios extensos, use divisórias com parcimônia: o propósito é ajudar a localizar o conteúdo, não aumentar o número de elementos decorativos.

## 4. Quando não usar?

Não coloque uma linha grossa no lugar de “Limitações da análise”. O leitor poderia reconhecer uma fronteira sem descobrir o tema nem encontrá-lo pelo título.

Para um documento Markdown simples, um separador `---` pode atender à necessidade com menos dependência de HTML. Não interprete uma divisória como garantia de que o bloco anterior foi executado ou validado.

## 5. Como funciona, intuitivamente?

Cada função devolve uma string. As três primeiras usam um elemento `hr`; a de seção combina dois `hr` em um `div`. Espessura, cor e margem são definidas no código.

O destino renderiza o HTML. A função não chama `displayHTML`, não modifica a sessão e não lê os dados mostrados antes ou depois da linha.

## 6. Exemplo de situação

Um relatório sintético apresenta o perfil de uma base e, em seguida, as limitações da amostra. Você mantém o título “Limitações” e insere uma divisória destacada antes dele.

A fronteira visual ajuda a localizar a mudança de assunto, mas não substitui a explicação do que a amostra deixa de representar. Nenhuma inferência analítica é produzida pelo separador.

## 7. O que você precisa antes de usar?

O pacote precisa estar visível ao Python. O módulo importa estilos de `constants.styles` e o tipo `ResolvedTheme` de `visual.tema`; não exige Spark ou Plotly. A visualização necessita de suporte a HTML/CSS no destino.

O notebook usa Spark apenas em sua preparação de caminho e `displayHTML` para apresentar os resultados. Não lê nem grava tabelas de negócio. As quatro funções legadas não recebem parâmetros; as quatro variantes `_resolvido` recebem `theme`.

APIs públicas (retorno `str`; `theme` é um `ResolvedTheme` de contexto `notebook` nas variantes resolvidas):

- `divider_light()`
- `divider_medium()`
- `divider_heavy()`
- `divider_section()`
- `divider_light_resolvido(theme: ResolvedTheme)`
- `divider_medium_resolvido(theme: ResolvedTheme)`
- `divider_heavy_resolvido(theme: ResolvedTheme)`
- `divider_section_resolvido(theme: ResolvedTheme)`

A geração legada usa Python e o Hub. As rotas resolvidas revalidam o tema e exigem as [dependências de validação](../../requirements-temas.txt), sem instalação automática.

## 8. O que este recurso entrega?

O retorno é HTML textual:

| Função | Elemento e diferença principal |
|---|---|
| `divider_light()` | Uma linha de 1px e margem vertical de 10px. |
| `divider_medium()` | Uma linha de 1,5px e margem de 14px. |
| `divider_heavy()` | Uma linha de 2px em azul e margem de 18px. |
| `divider_section()` | Duas linhas em um bloco com margem vertical de 20px. |

O HTML não contém um título, índice ou identificador de navegação. Sem renderização, você verá a string, não uma linha gráfica.

## 9. Como usar este recurso no Hub?

Abra o [exemplo](exemplo_divider.py) para comparar os quatro resultados no ambiente de notebook. Após a preparação descrita na [coleção](../../README.md), é possível conferir a composição sem renderizar:

```python
from hub_snippets.visual.divider import divider_light, divider_section
print(divider_light().count("<hr"), divider_section().count("<hr"))
```

Saída portátil conferida: `1 2`. O teste verifica os elementos gerados, não a aparência no workspace.

### Tema explícito — divisória com tema explícito

`divider_light_resolvido(theme)`, `divider_medium_resolvido(theme)`, `divider_heavy_resolvido(theme)` e `divider_section_resolvido(theme)` mantêm a mesma estrutura HTML das funções históricas. O tema troca apenas cores mapeadas; margens e a composição de duas linhas da divisória de seção continuam contrato do componente.

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.divider import divider_section_resolvido
html = divider_section_resolvido(load_reference_theme("notebook"))
assert html.count("<hr") == 2
```

A chamada gera HTML em memória; sua exibição é separada.

## 10. Decisões e configurações que mais importam

A configuração oferecida é a escolha da função. Não há argumento de espessura, largura ou margem. Um pedido de variação no componente exige outra alteração, com revisão de sua saída.

Mantenha o mesmo significado para cada peso ao longo do notebook. Não use a função mais forte em todos os blocos: isso eliminaria a hierarquia que motivou seu uso.

## 11. Limitações, riscos e armadilhas

O efeito visual depende do destino e de sua escala de exibição. Diferenças pequenas de espessura podem ser discretas; não há teste perceptual no módulo. A renderização Databricks é documentada, mas este README não comprova equivalência entre todos os ambientes.

As funções legadas preservam seus estilos históricos. Na rota resolvida, as variantes `_resolvido` usam `constants.styles`: `divider.light`, `divider.medium` e `brand.primary` chegam do tema validado. Nenhuma delas cria mecanismo de atualização global. Mantenha os títulos mesmo quando a linha parecer suficiente.

## 12. Quais são as alternativas?

Títulos e espaço em branco podem resolver a organização sem separadores. `---` atende a uma rota Markdown. [section_header](../section_header/README.md) oferece cabeçalho renderizado quando é necessário nomear a seção; [styles](../../constants/styles/README.md) concentra a materialização da rota resolvida, sempre por chamada explícita.

## 13. Como saber se o resultado faz sentido?

Confira se cada divisória separa assuntos de fato e se o título seguinte explica o novo bloco. Na versão renderizada, verifique continuidade, zoom e ausência de espaços excessivos.

Se o destino exibir tags literais, ele está mostrando texto ou não está interpretando o HTML da forma esperada. Use uma saída compatível, em vez de alterar a lógica analítica do notebook.

## 14. Arquivos relacionados e próximos passos

[divider.py](divider.py) contém a composição; [__init__.py](__init__.py) define os nomes públicos; [exemplo_divider.py](exemplo_divider.py) mostra as variantes. A [coleção](../../README.md) dá acesso aos demais componentes.

## 15. Referências

A [implementação](divider.py) sustenta dimensões e efeitos. [Databricks — HTML em notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-media#include-html), consultada em 12/09/2026, documenta `displayHTML` como rota de visualização.

A [implementação](divider.py) e a [fachada](__init__.py) delimitam o contrato. Confira conteúdo, escape e aparência no destino: gerar uma string não homologa a interface nem acessibilidade.

[Registro técnico de referência](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/readmes_objetos/RELATORIO_R03A.md): consulte data, ambiente e alcance de cada teste; o registro não é homologação do destino.
