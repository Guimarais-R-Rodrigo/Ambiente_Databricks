# `explainability_report` — transformar importâncias em texto executivo/técnico sem confundir explicação com causa

<!-- readme-objeto: 1.0.0 -->

Este helper formata importâncias já calculadas em dois relatórios Markdown: uma visão executiva e um resumo técnico. Ele **não calcula SHAP sozinho**, não valida causalidade e não certifica uma decisão individual; organiza informação que o chamador já preparou.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Gerador de Markdown para comunicar importância/explicabilidade. |
| Para que serve? | Traduzir nomes técnicos e resumir ranking SHAP; opcionalmente comparar ranking SHAP e nativo. |
| Use quando... | As importâncias foram calculadas/validadas e você precisa comunicar o resultado em camadas. |
| Evite quando... | O objetivo é calcular SHAP, provar causalidade ou justificar sozinho uma decisão regulada. |
| Precisa de... | pandas/NumPy; `tabulate` para o resumo técnico; SciPy se comparar rankings. |
| Entrega... | Strings Markdown; não grava arquivos nem altera o modelo. |

Consulte a [implementação](explainability_report.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_explainability_report.py).

## 1. O que é?

A função executiva recebe uma tabela de importância SHAP e um dicionário de nomes de negócio. A técnica imprime a tabela e, opcionalmente, compara ranking SHAP com ranking nativo por Spearman.

O objeto é uma camada de **apresentação**. O cálculo de SHAP fica em [`shap_explainer`](../shap_explainer/README.md).

## 2. Que problema este recurso resolve?

Ele responde: “como transformar uma tabela técnica de importâncias em um texto que preserve limites essenciais e possa ser lido por públicos diferentes?”. Isso reduz a tentação de copiar números sem explicar escala, métrica ou causalidade.

## 3. Quando faz sentido usar?

Use depois de conferir a qualidade do modelo, o conjunto explicado e o método de importância. A visão executiva é útil quando nomes técnicos precisam ser traduzidos e o público precisa de poucos fatores principais.

O resumo técnico é útil para registrar a tabela completa e investigar divergência entre dois rankings, desde que ambos tenham colunas compatíveis.

## 4. Quando não usar?

Não use como calculadora de SHAP; ele espera `shap_importance` pronta. Não use o texto “fatores que influenciam” como evidência de intervenção causal.

Também não use o status de “consistência” entre rankings como gate universal: os thresholds são convenções fixas desta implementação.

## 5. Como funciona, intuitivamente?

`generate_executive_report` pega as cinco primeiras linhas **na ordem recebida**, traduz os nomes e classifica `pct_importance` em rótulos locais: acima de 15 “Alto”, acima de 8 “Médio” e o restante “Moderado”.

Se receber `shap_values`, `X` e `feature_names`, calcula a correlação entre valor da feature e SHAP daquela feature para gerar uma seta de associação.

`generate_technical_summary` usa `DataFrame.to_markdown()` e, com `native_importance`, faz merge por `feature`, calcula Spearman dos rankings e aplica thresholds locais de 0,7/0,5.

## 6. Exemplo de situação

Um modelo de risco já possui ranking SHAP validado. O time quer mostrar os cinco fatores mais importantes com nomes de negócio e manter, em anexo técnico, a tabela de importâncias e uma comparação com outra medida de importância.

O helper organiza essas duas camadas, mas a revisão metodológica continua fora dele.

## 7. O que você precisa antes de usar?

Para calcular direção, forneça `X` como `np.ndarray` 2D, pois o código usa `X[:, feat_idx]`; `shap_values` deve ter o mesmo shape e a mesma ordem de linhas/colunas. O merge técnico é uma interseção por `feature`, não a união: valide nomes únicos nos dois lados e registre features excluídas, pois duplicatas multiplicam pares. Correlações zero, quase zero ou indefinidas exigem revisão; uma seta é apenas uma heurística de associação.

A visão executiva exige `shap_importance` não vazia com `feature` e `pct_importance`. Se a ordem importa, **ordene antes de chamar**: a função não reordena.

Para direção, `X` e `shap_values` precisam estar alinhados por linha/feature e `feature_names` precisa conter os nomes usados no top 5.

O resumo técnico usa `pandas.DataFrame.to_markdown()`, que exige `tabulate`. Se `native_importance` for fornecida, a implementação atual espera que ambos os DataFrames tenham uma coluna `rank`, pois depois do merge acessa `rank_shap` e `rank_native`. O notebook histórico não fornece esses ranks e por isso instalar `tabulate` sozinho não torna aquela comparação completa.

## 8. O que este recurso entrega?

As duas funções retornam `str` em Markdown. Nenhuma escreve arquivo, publica artefato ou modifica o modelo.

A porcentagem exibida é `pct_importance` fornecida pelo chamador. O helper não verifica se soma 100 nem se veio de mean |SHAP|.

## 9. Como usar este recurso no Hub?

Resumo técnico mínimo com importâncias sintéticas, `tabulate` disponível e ranks preparados sobre as tabelas completas, antes de qualquer `top_n`:

```python
import pandas as pd
import tabulate  # pré-requisito de DataFrame.to_markdown()
from hub_snippets.ml.explainability_report import generate_technical_summary

shap_full = pd.DataFrame({"feature": ["a", "b", "c"],
                          "mean_abs_shap": [0.6, 0.3, 0.1]})
native_full = pd.DataFrame({"feature": ["a", "b", "c"],
                            "importance": [9.0, 2.0, 1.0]})
for frame, col in [(shap_full, "mean_abs_shap"), (native_full, "importance")]:
    assert frame["feature"].is_unique
    frame["rank"] = frame[col].rank(method="average", ascending=False)
assert set(shap_full["feature"]) == set(native_full["feature"])
texto_tecnico = generate_technical_summary(shap_full, native_importance=native_full)
```

O texto é retornado em memória. Este preparo não corrige automaticamente a célula do notebook adjacente que ainda omite `rank`: com três ou mais features em comum ela pode falhar com `KeyError`, mesmo após instalar `tabulate`.

```python
from hub_snippets.ml.explainability_report import generate_executive_report

texto = generate_executive_report(
    importance.sort_values("pct_importance", ascending=False),
    feature_business_names=nomes,
    target_description="evento em 12 meses",
    model_metric=0.78,
    metric_name="AUC",
)
```

O [notebook](exemplo_explainability_report.py) não grava dados; sua segunda célula técnica documenta limitações de dependência e contrato.

## 10. Decisões e configurações que mais importam

A ordem de `shap_importance` determina o top 5. `feature_business_names` altera apenas rótulos de apresentação.

Os cortes 15%/8% e Spearman 0,7/0,5 são **heurísticas de apresentação codificadas localmente**, não normas SHAP ou estatísticas universais.

`metric_name` e `model_metric` são texto/número fornecidos pelo chamador; o helper não sabe se a métrica foi calculada fora da amostra.

## 11. Limitações, riscos e armadilhas

A “direção” executiva é o sinal de uma correlação global feature × SHAP, não efeito causal nem explicação local de uma observação. Correlação exatamente zero e finita cai no ramo textual “associação negativa” na implementação atual; por isso, trate essa seta como heurística e revise casos próximos de zero.

Spearman pode ser indefinido em rankings degenerados; a função não possui validação explícita para esse caso.

Diferentes importâncias nativas de árvores podem representar ganho, contagem de splits, redução de impureza ou outra definição, dependendo do estimador. Compare definições antes de interpretar divergência.

## 12. Quais são as alternativas?

[`shap_explainer`](../shap_explainer/README.md) calcula valores SHAP e ranking global. Um relatório customizado pode ser melhor quando há requisitos de compliance, linguagem ou layout específicos.

Para explicação individual sob política/regulação, use o processo autorizado e evidência adequada; esta string Markdown não substitui esse processo.

## 13. Como saber se o resultado faz sentido?

Confira manualmente as cinco primeiras linhas, soma/escala de `pct_importance`, nomes traduzidos e a métrica informada. Se usar direção, compare com gráficos de dependência e inspecione correlações próximas de zero.

No resumo técnico, verifique que os dois rankings cobrem o mesmo conjunto de features e que o significado de “importância nativa” foi documentado.

## 14. Arquivos relacionados e próximos passos

A [implementação](explainability_report.py) gera os textos; a [fachada](__init__.py) exporta as duas funções; o [notebook](exemplo_explainability_report.py) mostra a camada executiva e registra a dependência escondida de `tabulate`.

Calcule as importâncias com [`shap_explainer`](../shap_explainer/README.md) e só depois use esta camada de comunicação.

## 15. Referências

Consulte a documentação do SHAP para o espaço de saída explicado e o significado das atribuições. Este gerador recebe importâncias prontas e devolve texto; o relatório não constitui evidência causal nem aprovação de decisão.

Referências primárias de conceito/API: [Documentação primária de explainability_report](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).
