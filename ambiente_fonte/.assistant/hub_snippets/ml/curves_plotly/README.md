# `curves_plotly` — ROC, Precision-Recall, lift e KS em Plotly

<!-- readme-objeto: 1.0.0 -->

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

```python
from hub_snippets.ml.curves_plotly import plot_pr_curve

fig = plot_pr_curve(y_true, y_prob, title="PR — validação")
fig.show()
```

## 10. Decisões e configurações que mais importam

Em lift, `n_bins` define os pontos cumulativos e deve estar entre 2 e o tamanho da amostra. O primeiro ponto equivale a `1/n_bins` da base; com `n_bins=10`, é top-10%.

A paleta local tem seis cores, enquanto a paleta compartilhada do Hub tem dez. Isso é dívida conhecida e pode mudar aparência se for unificada.

## 11. Limitações, riscos e armadilhas

`n` não limita custo. Para bases grandes, amostre explicitamente antes de chamar. As funções não calculam intervalos de confiança.

A curva KS deste helper usa o mesmo eixo FPR para desenhar TPR e diagonal; não confunda sua apresentação com a convenção de KS em pontos percentuais de `metrics_report`.

A paleta local repete cores depois da sexta série se for reutilizada para gráficos com mais séries.

## 12. Quais são as alternativas?

Use funções do scikit-learn quando precisar dos arrays numéricos sem Plotly. [`metrics_report`](../metrics_report/README.md) consolida métricas escalares. Para calibração, use ferramentas específicas de calibration curve/Brier.

## 13. Como saber se o resultado faz sentido?

Cheque prevalência, número de eventos, baseline da PR e consistência da AUC com `roc_auc_score`. Em lift, valide manualmente o primeiro segmento. Compare sempre na mesma população e janela.

## 14. Arquivos relacionados e próximos passos

A [implementação](curves_plotly.py) contém as quatro curvas; a [fachada](__init__.py) reexporta também constantes visuais; o [notebook](exemplo_curves_plotly.py) usa uma fixture rara sintética.

Depois da avaliação visual, registre métricas com [`metrics_report`](../metrics_report/README.md) e monitore somente com política explícita.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da R09. Referências primárias: documentação do scikit-learn para ROC, Precision-Recall, AUC/AP e documentação do Plotly para `graph_objects`.

As curvas descrevem comportamento na amostra fornecida; não estabelecem causalidade, calibração ou aprovação de produção.