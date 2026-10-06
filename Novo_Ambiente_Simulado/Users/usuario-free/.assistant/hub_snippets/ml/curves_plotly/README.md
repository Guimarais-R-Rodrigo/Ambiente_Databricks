# `curves_plotly` — ROC, Precision-Recall, lift e KS em Plotly

<!-- readme-objeto: 1.0.0 -->
<!-- sistema-temas-v07: consumidores -->
Para usar um tema explícito, escolha plot_roc_curve_resolvido, plot_pr_curve_resolvido, plot_lift_curve_resolvido ou plot_ks_curve_resolvido e passe um ResolvedTheme compatível com notebook/light. As funções legadas continuam disponíveis. A rota temática conserva a paleta específica de seis cores e os cálculos; pode produzir HTML local. PNG Plotly, PDF e PPTX não estão homologados nesse contrato.

Este objeto produz quatro visualizações diagnósticas para classificação binária com tema local do Hub. Ele facilita leitura e comunicação, mas não escolhe threshold, não mede calibração e não substitui validação estatística ou de negócio.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Conjunto de funções Plotly para ROC, PR, lift cumulativo e KS. |
| Para que serve? | Visualizar separação, precisão/recall e concentração de eventos. |
| Use quando... | Há rótulos 0/1 e probabilidades válidas de uma população de avaliação definida. |
| Evite quando... | Você quer calibração, multiclasses ou processamento distribuído. |
| Precisa de... | NumPy, Plotly e scikit-learn. |
| Entrega... | `plotly.graph_objects.Figure`. |

Consulte a [implementação](curves_plotly.py), a [fachada](__init__.py) e o [notebook](exemplo_curves_plotly.py).

## 1. O que é?

São quatro helpers de visualização: `plot_roc_curve`, `plot_pr_curve`, `plot_lift_curve` e `plot_ks_curve`. Todos validam classificação binária e probabilidades finitas em `[0,1]`.

## 2. Que problema este recurso resolve?

Padroniza curvas recorrentes e reduz a chance de comparar gráficos com tema, baseline ou convenção visual diferentes. Cada curva responde uma pergunta distinta; o objeto não declara uma delas como universalmente superior.

## 3. Quando faz sentido usar?

Use ROC para separação global, PR quando prevalência e precisão operacional importarem, lift para concentração de eventos na base ordenada e KS para máxima separação entre acumuladas.

## 4. Quando não usar?

Não use como prova de calibração. Não use diretamente em multiclasses. Não interprete uma curva bonita como autorização de uso do modelo. O módulo é driver-side.

## 5. Como funciona, intuitivamente?

ROC compara TPR e FPR; PR compara precision e recall e mostra a prevalência como baseline. Lift ordena por score e compara eventos capturados com o esperado sem modelo. KS usa `tpr - fpr` e destaca a maior distância.

## 6. Exemplo de situação

Em uma base rara, ROC pode parecer excelente enquanto a PR revela baixa precisão em grande parte da faixa de recall. Lift mostra quanto o topo da lista concentra eventos e KS resume a maior separação.

## 7. O que você precisa antes de usar?

`y_true` e `y_prob` devem ser arrays 1-D, não vazios e de mesmo tamanho. As duas classes 0 e 1 precisam estar presentes; probabilidades devem ser finitas e estar em `[0,1]`.

## 8. O que este recurso entrega?

Cada função retorna um `Figure`. ROC inclui AUC; PR inclui Average Precision e baseline; lift anota o primeiro segmento; KS anota a estatística máxima.

O argumento `n` altera apenas o N exibido no rodapé; não subamostra os dados.

## 9. Como usar este recurso no Hub?

Para tema explícito, obtenha um `ResolvedTheme` pela [rota de resolução](../../visual/tema/README.md). As assinaturas públicas são:

```python
plot_roc_curve_resolvido(y_true, y_prob, theme, title="Curva ROC", show_auc=True, n=None)
plot_pr_curve_resolvido(y_true, y_prob, theme, title="Curva Precision-Recall", n=None)
plot_lift_curve_resolvido(y_true, y_prob, theme, title="Curva de Lift", n_bins=10, n=None)
plot_ks_curve_resolvido(y_true, y_prob, theme, title="Curva KS", n=None)
```

Com `theme` já resolvido e compatível com notebook/light:

```python
from hub_snippets.ml.curves_plotly import plot_pr_curve_resolvido
fig = plot_pr_curve_resolvido(y_true, y_prob, theme=theme)
```

Essas chamadas retornam figuras em memória. `fig.write_html(destino)` é uma ação separada de escrita local que exige escolher e conferir o destino.

```python
from hub_snippets.ml.curves_plotly import plot_pr_curve

fig = plot_pr_curve(y_true, y_prob, title="PR — validação")
fig.show()
```

A chamada acima usa todos os elementos de `y_true` e `y_prob`; `n`, quando informado, só muda o texto do rodapé. Em base grande, faça a redução de volume antes de chamar o helper.

## 10. Decisões e configurações que mais importam

Em lift, `n_bins` define os pontos cumulativos e deve estar entre 2 e o tamanho da amostra. O primeiro corte é nominalmente `1/n_bins`: seleciona `k = ceil(N/n_bins)` linhas, com cobertura real `k/N`. Para `N=21` e `n_bins=10`, usa três observações, `3/21 ≈ 14,29%`; a anotação top-10% é nominal, não a cobertura efetiva.

A família de curvas usa deliberadamente seis cores próprias, diferentes das dez cores da paleta categórica geral. Essa separação é parte do contrato visual; não substitua uma pela outra implicitamente.

## 11. Limitações, riscos e armadilhas

`n` não limita custo. Para bases grandes, amostre explicitamente antes de chamar. As funções não calculam intervalos de confiança.

O KS da figura é unilateral: `max(TPR − FPR)`, em escala 0–1, desenhado sobre FPR. Já `metrics_report.ks_pct` usa a distância bilateral absoluta de `ks_2samp`, multiplicada por 100. Não reconcilie os dois apenas multiplicando a figura por 100. Com `y_true=[0,0,1,1]` e `y_prob=[0.9,0.8,0.2,0.1]`, o ranking está perfeitamente invertido: o KS da figura é 0 e o bilateral é 100. Nenhum desses valores, isolado da direção do score, aprova o modelo.

A paleta local repete cores depois da sexta série se for reutilizada para gráficos com mais séries.

## 12. Quais são as alternativas?

Use funções do scikit-learn quando precisar dos arrays numéricos sem Plotly. [`metrics_report`](../metrics_report/README.md) consolida métricas escalares. Para calibração, use ferramentas específicas de calibration curve/Brier.

## 13. Como saber se o resultado faz sentido?

Cheque prevalência, número de eventos, baseline da PR e consistência da AUC com `roc_auc_score`. Em lift, valide manualmente o primeiro segmento. Compare sempre na mesma população e janela.

## 14. Arquivos relacionados e próximos passos

A [implementação](curves_plotly.py) contém as quatro curvas; a [fachada](__init__.py) reexporta também constantes visuais; o [notebook](exemplo_curves_plotly.py) usa uma fixture rara sintética.

Depois da avaliação visual, registre métricas com [`metrics_report`](../metrics_report/README.md) e monitore somente com política explícita.

## 15. Referências

Consulte as definições de ROC, Precision-Recall e Average Precision do scikit-learn e a API graph_objects do Plotly. Os gráficos descrevem apenas a amostra recebida; não validam calibração nem aprovam o uso do modelo.