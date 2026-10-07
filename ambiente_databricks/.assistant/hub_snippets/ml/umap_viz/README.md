# `umap_viz` — projeção UMAP para exploração visual de clusters, não prova de separação

<!-- readme-objeto: 1.0.0 -->
<!-- sistema-temas-v07: consumidores -->
Use plot_umap_clusters para a aparência legada ou plot_umap_clusters_resolvido(..., theme) para um ResolvedTheme notebook/light. A rota temática valida o tema antes do cálculo e conserva coordenadas, labels, opacidade e tamanho dos pontos. umap-learn continua carregado apenas quando a projeção é calculada.

Este objeto calcula embedding UMAP e cria um scatter Plotly colorido por label. Ele ajuda a **explorar vizinhanças em baixa dimensão**, mas a geometria do desenho depende de hiperparâmetros e não deve ser tratada como medida fiel das distâncias originais ou prova de que clusters “existem”.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Redução de dimensionalidade UMAP + visualização Plotly 2D. |
| Para que serve? | Explorar estrutura local e sobreposição de labels em dados multivariados. |
| Use quando... | Features e métrica de distância fazem sentido e a visualização é tratada como exploratória. |
| Evite quando... | Você precisa medir distâncias originais, provar clusters ou inferir significado dos eixos. |
| Precisa de... | NumPy, `umap-learn`, pandas/Plotly e constantes visuais do Hub. |
| Entrega... | `compute_umap`: array de embedding; rotas legada e `plot_umap_clusters_resolvido`: `go.Figure`. |

Consulte a [implementação](umap_viz.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_umap_viz.py).

## 1. O que é?

UMAP reduz dados de alta dimensão para um espaço menor a partir de relações de vizinhança. A função `compute_umap` desta pasta fixa `random_state=42` e expõe `n_components`, `n_neighbors` e `min_dist`.

`plot_umap_clusters` chama `compute_umap` internamente com os defaults e colore pontos pelos labels fornecidos.

## 2. Que problema este recurso resolve?

Ele responde: “como os labels de cluster se distribuem numa projeção 2D da vizinhança dos dados?”. A figura pode revelar mistura, ilhas e casos de fronteira que merecem investigação.

Ela não substitui métricas no espaço original nem valida o algoritmo que criou os labels.

## 3. Quando faz sentido usar?

Use como complemento visual após preparar features e escala. É útil para comunicação exploratória e para encontrar observações que parecem isoladas ou clusters que se sobrepõem na projeção.

Compare mais de uma configuração de UMAP quando a conclusão depender do desenho.

## 4. Quando não usar?

Não meça a distância entre centroides no gráfico como se fosse distância original. Não use uma ilha visual como prova estatística de um segmento.

Também não presuma que PCA “falha” e UMAP “funciona” por regra. PCA é linear e UMAP é não linear; qual representação ajuda depende da estrutura e da pergunta.

## 5. Como funciona, intuitivamente?

`compute_umap` chama `UMAP(...).fit_transform(X)` e devolve coordenadas. `n_neighbors` controla o tamanho da vizinhança usada na construção local; `min_dist` controla quão compactos os pontos podem ficar no embedding.

O plotter recomputa uma projeção 2D, cria DataFrame com `UMAP_1`, `UMAP_2` e `Cluster`, gera scatter Plotly e adiciona rodapé com N e quantidade de labels não-ruído.

## 6. Exemplo de situação

Uma base tem dez features padronizadas e três labels conhecidos. O notebook projeta em 2D e verifica visualmente se as cores formam regiões separadas.

Como os grupos foram plantados na fixture, sabemos a origem dos labels; em dados reais, o desenho sozinho não fornece esse ground truth.

## 7. O que você precisa antes de usar?

`X` precisa ser uma matriz numérica compatível com UMAP. A função não faz padronização; se escalas diferentes não representam distâncias desejadas, prepare-as antes.

`umap-learn` precisa estar instalado. O inventário do Hub registra pin histórico `umap-learn==0.5.5` para o runtime testado.

Para `plot_umap_clusters`, `labels` precisa ter o mesmo comprimento de `X_scaled`. O código não possui validação dedicada, então inconsistências aparecem no NumPy/pandas/UMAP.

## 8. O que este recurso entrega?

O retorno de `compute_umap` contém somente coordenadas; não inclui o transformador UMAP ajustado. O wrapper não permite persistir/reaplicar a mesma projeção out-of-sample. Chamar novamente ajusta outra projeção, mesmo com a mesma semente.

`compute_umap` retorna array `(n_amostras, n_components)`. Os eixos não carregam unidade de negócio.

`plot_umap_clusters` retorna uma figura Plotly 2D. O rodapé usa `n` se esse argumento for truthy; caso contrário mostra `len(X_scaled)`. Esse `n` é apenas texto de apresentação e não é conferido contra a base.

A contagem de clusters exclui label `-1`.

## 9. Como usar este recurso no Hub?

Para tema explícito, obtenha `theme` pela [resolução do Hub](../../visual/tema/README.md) no contexto notebook/light e mantenha labels como array:

```python
import numpy as np
from hub_snippets.ml.umap_viz import plot_umap_clusters_resolvido
labels = np.asarray(labels)
assert labels.ndim == 1 and len(labels) == len(X_scaled)
fig = plot_umap_clusters_resolvido(X_scaled, labels, theme=theme,
                                  title="Projeção exploratória")
```

A chamada valida o tema antes da projeção, calcula no driver e retorna figura em memória; não instala UMAP nem salva/publica o desenho.

```python
import numpy as np
from hub_snippets.ml.umap_viz import plot_umap_clusters

labels = np.asarray(labels)  # o plotter usa labels.astype(str)
assert labels.ndim == 1 and len(labels) == len(X_scaled)
fig = plot_umap_clusters(
    X_scaled,
    labels,
    title="Clusters em projeção UMAP",
)
fig.show()
```

O [notebook](exemplo_umap_viz.py) instala a versão UMAP registrada para a fixture e reinicia o Python.

## 10. Decisões e configurações que mais importam

Em `compute_umap`, `n_neighbors` muda o equilíbrio entre estrutura local e mais ampla; `min_dist` muda a compactação visual; `n_components` muda a dimensão de saída.

Esses parâmetros **não são expostos por `plot_umap_clusters`**: o plotter sempre recomputa com defaults `2/15/0.1`. Se você precisa comparar configurações, use `compute_umap` diretamente e construa a visualização correspondente, ou evolua a API em outra mudança funcional.

`cluster_names` mapeia strings `"0"`, `"1"`, ... pela posição da lista. Labels arbitrários ou `-1` podem virar valores ausentes no nome exibido.

## 11. Limitações, riscos e armadilhas

UMAP pode alterar aparência de grupos quando hiperparâmetros mudam. Mesmo com semente fixa, estabilidade visual não equivale a estabilidade da segmentação.

plot_umap_clusters usa a aparência legada e não recebe theme. Para um tema explícito, use plot_umap_clusters_resolvido; selecionar essa rota não muda a lógica da projeção.

Rodar clustering sobre um embedding pode ser uma estratégia válida em alguns pipelines, mas muda a geometria do problema e precisa ser validado; a projeção 2D não é neutra.

## 12. Quais são as alternativas?

PCA oferece uma projeção linear mais simples e com componentes interpretáveis como combinações lineares. t-SNE é outra técnica de visualização local.

[`clustering_suite`](../clustering_suite/README.md) cria/avalia agrupamentos; [`cluster_profiling`](../cluster_profiling/README.md) descreve clusters em features originais.

## 13. Como saber se o resultado faz sentido?

Compare `n_neighbors`/`min_dist` pela API `compute_umap` e confira métricas/perfis no espaço original. O wrapper fixa `random_state=42` e não aceita argumento `seed`: testar sementes diferentes exige a API UMAP direta ou uma mudança funcional separada.

Verifique labels ausentes após `cluster_names`, contagem de linhas e se o rodapé representa realmente o N que você quer comunicar.

## 14. Arquivos relacionados e próximos passos

A [implementação](umap_viz.py) contém embedding e figura; a [fachada](__init__.py) expõe a API; o [notebook](exemplo_umap_viz.py) mostra três grupos sintéticos em dez dimensões.

Se a decisão depender da estabilidade dos segmentos, volte ao espaço original e valide com métricas/perfis, não com a figura isolada.

## 15. Referências

Consulte a documentação UMAP sobre n_neighbors, min_dist e n_components. A projeção é exploratória e não comprova estabilidade dos clusters; o wrapper fixa a semente e não devolve o transformador ajustado.

Referências primárias de conceito/API: [Documentação primária de umap_viz](https://umap-learn.readthedocs.io/en/latest/parameters.html), [Documentação primária de umap_viz](https://umap-learn.readthedocs.io/en/latest/api.html).
