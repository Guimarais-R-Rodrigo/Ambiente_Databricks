# `shap_explainer` — calcular atribuições SHAP com saída/classe explícita e limites de custo

<!-- readme-objeto: 1.0.0 -->

Este objeto encapsula cálculo SHAP para modelos de árvore, lineares e KernelSHAP, além de ranking global e plots. SHAP explica **o output do modelo no espaço escolhido pelo explainer**; não prova causalidade e não transforma automaticamente uma atribuição em justificativa de negócio.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Wrapper para calcular SHAP, ranquear mean \|SHAP\| e gerar plots global/local. |
| Para que serve? | Inspecionar contribuição das features para as previsões do modelo. |
| Use quando... | Modelo, classe/output e conjunto de dados a explicar estão explicitamente definidos. |
| Evite quando... | Você quer inferência causal, explicação sem conhecer o output ou custo KernelSHAP incompatível com a base. |
| Precisa de... | `shap`, NumPy/pandas; modelo suportado; Matplotlib para plots. |
| Entrega... | Matriz SHAP + base value; ranking DataFrame; plots são produzidos/fechados e não retornados. |

Consulte a [implementação](shap_explainer.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_shap_explainer.py).

## 1. O que é?

Valores SHAP atribuem a cada feature uma contribuição para a diferença entre um valor de referência e o output explicado do modelo. Esta pasta escolhe `TreeExplainer`, `LinearExplainer` ou `KernelExplainer` conforme `model_type`.

A camada local ainda normaliza formatos multi-output para uma matriz 2D, exigindo `output_index` quando necessário.

## 2. Que problema este recurso resolve?

Ele responde: “para este modelo e este output, quais features contribuíram mais globalmente e como contribuíram em cada linha?”. Também padroniza a seleção explícita de classe/output para evitar interpretar a saída errada silenciosamente.

## 3. Quando faz sentido usar?

Use para auditoria técnica, diagnóstico de comportamento do modelo, comparação de importância global e inspeção de casos individuais.

TreeSHAP é apropriado para árvores suportadas; LinearSHAP para modelos lineares compatíveis; KernelSHAP é model-agnostic, porém normalmente bem mais caro.

## 4. Quando não usar?

Não use como prova de que mudar uma feature causará mudança no fenômeno real. Não use um output multi-classe sem declarar qual saída está sendo explicada.

Não use `max_samples` esperando limitar custo de TreeSHAP ou LinearSHAP: na implementação atual ele só afeta o ramo `kernel`.

## 5. Como funciona, intuitivamente?

`compute_shap` cria o explainer, obtém os valores e chama uma rotina interna que aceita listas, matrizes 2D ou tensores 3D. Quando existem múltiplas saídas, `output_index` escolhe uma delas.

No ramo linear, `background=None` preserva o uso de `X` como referência. O keyword `background` permite uma referência externa numérica, finita, 2D e com a mesma largura de `X`; os ramos `tree` e `kernel` rejeitam esse argumento. A escolha muda o valor base e as atribuições, então registre sua origem e unidade.

O wrapper exige um `base_value` finito e constante entre linhas. No KernelSHAP, amostra no máximo `max_samples`, usa as primeiras até 100 linhas dessa amostra como background e explica apenas a amostra selecionada.

`get_feature_importance_shap` calcula mean |SHAP| por feature e divide pelo total de **todas** as features antes de truncar para `top_n`.

## 6. Exemplo de situação

Um classificador binário foi treinado com sinal sintético conhecido. O notebook calcula SHAP para a saída escolhida, verifica se features plantadas como relevantes aparecem no topo e observa que ruído pode receber importância pequena e não nula.

Isso é um sanity check útil da fixture; não demonstra que toda explicação SHAP futura esteja correta ou estável.

## 7. O que você precisa antes de usar?

`X` precisa ter número de colunas igual a `feature_names`. `max_samples` deve ser positivo e `task` deve ser `classification` ou `regression`.

`shap` é dependência opcional importada dentro de `compute_shap`. O inventário do Hub registra pin histórico `shap==0.44.1` para o runtime Databricks testado; revalide a compatibilidade no destino antes de instalar.

Para classificação multi-output, conheça a ordem das saídas do modelo. O wrapper não escolhe “classe positiva” por semântica.

## 8. O que este recurso entrega?

`compute_shap` devolve matriz 2D `(linhas, features)` e um `float` de base. No ramo KernelSHAP com subamostragem, o número de linhas do retorno pode ser menor que o `X` original.

`get_feature_importance_shap` devolve `rank`, `feature`, `mean_abs_shap`, `pct_importance` e `cumulative_pct`. Se `top_n` for menor que o total de features, `cumulative_pct` final pode ser menor que 100 porque as porcentagens foram calculadas antes do corte.

Os plotters fecham a figura e não retornam `Figure`.

## 9. Como usar este recurso no Hub?

Para KernelSHAP, controle a amostra **antes** do helper e guarde os índices. A subamostragem interna não retorna índices e pode reordenar as linhas: unir seus valores ao `X` original atribuiria explicações a entidades erradas.

```python
import numpy as np
from hub_snippets.ml.shap_explainer import compute_shap, plot_shap_global

# X é uma matriz numérica preparada com as mesmas colunas do treino.
X = np.asarray(X, dtype=float)
indices = np.random.default_rng(42).choice(len(X), min(200, len(X)), replace=False)
X_amostra = X[indices]
values, base = compute_shap(
    model, X_amostra, feature_names=names, model_type="kernel",
    task="classification", output_index=1, max_samples=len(X_amostra),
)
assert values.shape == X_amostra.shape
# Escolha um diretório existente e autorize a escrita/sobrescrita antes de usar:
# plot_shap_global(values, X_amostra, names, save_path="/tmp/shap_global.png")
```

Reutilize exatamente `X_amostra` nos plots e na direção do relatório; `indices` permite recuperar os IDs originais. O exemplo de caminho cria ou pode sobrescrever um PNG local. Sem `save_path`, os plotters fecham a figura sem retorná-la nem entregar um arquivo. Para modelo de regressão, use `task="regression"` e a saída pertinente.

```python
from hub_snippets.ml.shap_explainer import compute_shap, get_feature_importance_shap

values, base = compute_shap(
    model,
    X,
    feature_names=names,
    model_type="tree",
    output_index=1,
)
ranking = get_feature_importance_shap(values, names)
```

O [notebook](exemplo_shap_explainer.py) instala a versão de SHAP testada naquela fixture e reinicia o Python.

## 10. Decisões e configurações que mais importam

Se SHAP já retorna uma matriz 2D, `output_index` é ignorado: o argumento não prova que uma classe foi selecionada. Confirme a semântica da saída do estimador. Para lista/tensor multi-output, a seleção e a validação de índice são exigidas pelo wrapper.

`background` é opcional e só afeta `model_type="linear"`; com `None`, permanece o comportamento anterior.

`model_type` escolhe o algoritmo. `task` só altera qual método do modelo o KernelSHAP usa (`predict_proba` ou `predict`). `output_index` seleciona saída/classe quando o SHAP retorna múltiplas saídas.

`max_samples` limita apenas a quantidade explicada no KernelSHAP. O background Kernel é composto pelas primeiras até 100 linhas da amostra selecionada; essa escolha pode influenciar as atribuições.

`top_n` limita a tabela exibida, não a normalização das porcentagens.

## 11. Limitações, riscos e armadilhas

O espaço explicado varia por modelo/explainer. A documentação do SHAP destaca que, por exemplo, output “raw” de certos classificadores não é a mesma escala de `predict_proba`. Portanto `base_value` não deve ser chamado genericamente de prevalência.

Features dependentes/correlacionadas exigem cuidado porque diferentes pressupostos de background/dependência distribuem crédito de modos diferentes.

`plot_shap_global` só trata explicitamente `beeswarm` e `bar`; outro `plot_type` não gera erro explícito nessa função. `plot_shap_local` indexa `X[idx]`, portanto o caminho mais seguro é fornecer `np.ndarray`; em DataFrame, `X[idx]` tem semântica de coluna.

Importância pequena e não nula não prova ausência de sinal nem define um cutoff universal.

## 12. Quais são as alternativas?

Importância nativa do estimador pode ser mais barata, mas mede outra quantidade e sua definição varia. Permutation importance é outra alternativa global quando o custo é aceitável.

[`explainability_report`](../explainability_report/README.md) organiza a comunicação depois que as atribuições já foram calculadas.

## 13. Como saber se o resultado faz sentido?

Verifique additivity/escala quando suportado, classe/output, shape do retorno e casos sintéticos de sinal conhecido. Repita em amostras e backgrounds diferentes quando estabilidade importar.

Compare explicações com comportamento observado do modelo, não com uma história causal desejada. Em feature correlacionada, faça análises de sensibilidade.

## 14. Arquivos relacionados e próximos passos

A [implementação](shap_explainer.py) contém cálculo/ranking/plots; a [fachada](__init__.py) define a API pública; o [notebook](exemplo_shap_explainer.py) exercita TreeSHAP em classificação binária.

Depois do cálculo, use [`explainability_report`](../explainability_report/README.md) apenas como camada de comunicação.

## 15. Referências

Consulte TreeExplainer e a API SHAP da versão instalada. A soma das atribuições depende do output explicado e da referência adotada; revise classe, base_value, alinhamento de linhas e dependência entre features antes de interpretar.

Referências primárias de conceito/API: [`TreeExplainer`](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html), [API](https://shap.readthedocs.io/en/latest/api.html).
