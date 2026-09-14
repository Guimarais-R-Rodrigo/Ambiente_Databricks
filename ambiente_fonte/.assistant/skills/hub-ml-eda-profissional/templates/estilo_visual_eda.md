# Estilo Visual — EDA Profissional sobre o Sistema de Temas

Este template orienta **composição, hierarquia e leitura** de uma EDA. Ele não é fonte de paleta, token ou aprovação. As escolhas configuráveis pertencem ao contrato `hub_padroes/identidade_visual` e chegam ao consumidor por `ResolvedTheme`.

## 1. Fonte de verdade visual

- Não declare `PALETA_EDA`, `TEMA_EDA` ou dicionário paralelo de tema.
- Não copie valores de `TOKENS.md` para “congelar” uma aparência local.
- Não registre template global como preparação padrão do notebook; **não registre template global** apenas para aplicar uma proposta.
- Se não houver tema explicitamente selecionado, use as APIs legadas do Hub.
- Se houver tema notebook válido, use as rotas `_resolvido` do consumidor.

Fluxo mínimo para uma figura Plotly genérica:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

tema = load_reference_theme("notebook")
fig = ...  # mesmos dados, agregações e eixos da análise
aplicar_tema_resolvido(fig, tema, subtitulo="Recorte analisado", n=n_amostra)
fig.show()
```

Para componentes especializados, prefira a própria rota resolvida, por exemplo `plot_correlation_resolvido`, `plot_distributions_resolvido`, curvas `*_resolvido`, `plot_vintage_curves_resolvido` ou `plot_timeline_resolvido`. Isso evita reconstruir semântica de cor no notebook.

## 2. O que o tema pode e não pode mudar

O tema pode controlar propriedades visuais cobertas pelo contrato, como tipografia, dimensões, margens, paletas e cores semânticas. Ele **não** muda:

- filtro, população ou data de corte;
- amostragem, seed ou agregação;
- bins, denominadores e unidade;
- threshold analítico ou política de monitoramento;
- métrica, modelo ou conclusão de negócio.

Aparência consistente não valida a análise.

## 3. Escolha de gráficos

| Tipo de dado/pergunta | Visual sugerido | Cuidados |
| --- | --- | --- |
| numérica univariada | histograma, ECDF ou box plot | declarar amostra/agregação |
| categórica | barras ordenadas | mostrar denominador, top-N e cauda |
| temporal | linha em frequência regular | rotular janela e gaps |
| associação numérica | scatter/agregado ou correlação | sinal não implica causalidade |
| matriz com centro significativo | heatmap divergente | preservar centro e domínio |
| comparação de segmentos | small multiples ou barras | manter escala comparável |

Use Plotly para gráficos do relatório quando a interatividade ajudar. Visualização nativa pode ser melhor para exploração ou agregações que devem ficar no backend. Matplotlib permanece válido para casos estáticos específicos, mas não herda automaticamente o Sistema de Temas Plotly.

## 4. Anotações e rodapé

Todo gráfico material deve deixar explícitos, quando aplicável:

- N amostral ou volume agregado;
- fonte/snapshot;
- janela, segmento ou recorte;
- unidade e denominador;
- uma anotação de destaque somente quando houver achado realmente sustentado.

Não transforme anotação em conclusão causal. Em rotas Plotly do Hub, use os argumentos de rodapé do adaptador/consumidor em vez de criar um segundo estilo.

## 5. Hierarquia do notebook

- `#`: título único do notebook;
- `##`: etapas principais;
- `###`: subseções/resultados;
- `####`: tópicos internos quando necessários.

Evite profundidade excessiva. Emojis são semânticos e limitados; não substituem títulos informativos.

## 6. Números e tabelas

Formate números com `hub_snippets.constants.format_br` quando o público exigir padrão brasileiro. Não implemente formatação monetária/percentual em vários pontos do notebook.

Em tabelas Markdown:

- prefira até seis colunas por bloco legível;
- alinhe números à direita quando a superfície permitir;
- use nomes técnicos em backticks;
- destaque somente o que possui significado analítico;
- não esconda denominador ou unidade.

## 7. Componentes HTML e seções

Para índice, cabeçalho, badges, divisores e KPI cards, prefira os helpers `hub_snippets.visual`. Se houver um `ResolvedTheme`, use a rota `_resolvido` correspondente quando documentada. Não monte CSS/HTML manual apenas para contornar os componentes V04.

Uma célula pós-código pode resumir poucos KPIs materiais em uma linha de leitura rápida, mas o valor precisa vir da saída observada. Não invente número para completar layout.

## 8. Consumidores com limite explícito

- SHAP/Matplotlib: o theming V07 não cobre sua aparência interna nem o PNG salvo pelo helper.
- Kaplan–Meier: permanece com a ordem visual legada até existir token que represente sua semântica sem remapeamento silencioso.

Não prometa consistência temática para essas superfícies apenas porque o restante do notebook usa `ResolvedTheme`.

## 9. Referências do Hub

| Necessidade | Fonte/consumidor |
| --- | --- |
| contrato e primeiro uso | `hub_padroes/identidade_visual/README.md` e `GUIA_OPERACIONAL.md` |
| carregar/validar tema | `hub_snippets.visual.tema` |
| aplicar tema Plotly | `hub_snippets.visual.theme_plotly.aplicar_tema_resolvido` |
| correlação | `hub_snippets.display.correlation_matrix.plot_correlation_resolvido` |
| distribuições | `hub_snippets.display.distribution_grid.plot_distributions_resolvido` |
| índice/cabeçalho/cards | rotas `_resolvido` dos componentes `hub_snippets.visual` |
| autoria/comparação | `hub_snippets.visual.theme_lab` |

O template EDA organiza a apresentação. A fonte de verdade do tema permanece fora desta skill.
