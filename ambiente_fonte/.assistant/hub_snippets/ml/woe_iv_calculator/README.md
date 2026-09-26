# `woe_iv_calculator` — WOE/IV distribuído como diagnóstico, não selo automático de qualidade

<!-- readme-objeto: 1.0.0 -->

WOE (*Weight of Evidence*) compara a distribuição de bons e maus dentro de cada faixa; IV (*Information Value*) agrega a separação entre essas distribuições. Este helper calcula ambos em PySpark para uma feature já categorizada/discretizada. Ele ajuda a diagnosticar separação; **não cria binning, não evita leakage e não transforma faixas clássicas de IV em norma regulatória**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Cálculo Spark de WOE por faixa e IV total. |
| Para que serve? | Medir separação de uma feature binned/categórica contra target binário. |
| Use quando... | Binning e target já estiverem definidos na população de treino apropriada. |
| Evite quando... | A variável ainda for contínua sem discretização, houver leakage ou se pretende seleção automática só por IV. |
| Precisa de... | PySpark e DataFrame com feature + target 0/1. |
| Entrega... | DataFrame Spark por faixa e um `float` de IV total. |

Consulte a [implementação](woe_iv_calculator.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_woe_iv_calculator.py).

## 1. O que é?

Para cada faixa, o helper calcula proporções suavizadas de “bons” (`target=0`) e “maus” (`target=1`). O WOE local é `ln(pct_bom / pct_mau)`. A contribuição de IV é `(pct_bom - pct_mau) × WOE`; o IV total é a soma das contribuições.

A função `classify_iv` aplica uma régua histórica codificada no projeto para rotular o valor total.

## 2. Que problema este recurso resolve?

WOE permite enxergar a direção e intensidade de separação por faixa, enquanto IV resume essa separação em um número. É útil em scorecards e análise de variáveis quando as faixas foram definidas de maneira válida.

O helper não responde se a variável estava disponível no instante da decisão nem se o binning foi ajustado usando informação de teste.

## 3. Quando faz sentido usar?

Use numa população de desenvolvimento bem delimitada, depois de definir faixas/categorias e orientação do target. Mantenha a definição de bins versionada para aplicar depois em validação/teste.

Também faz sentido investigar IV excepcionalmente alto como possível sinal de proxy do target, concentração, binning agressivo ou leakage.

## 4. Quando não usar?

Não passe uma variável contínua crua esperando que o helper descubra cortes: ele fará `groupBy` nos valores distintos, o que não equivale a um binning adequado.

Não selecione features automaticamente por `classify_iv`. As faixas codificadas são uma convenção heurística local e não substituem estabilidade, temporalidade, causalidade, custo ou governança.

## 5. Como funciona, intuitivamente?

Primeiro a função faz uma agregação global e coleta `total_bom`, `total_mau` e quantidade de targets inválidos. Depois agrega por `feature_col`, conta o número de bins, calcula proporções com smoothing e o WOE/IV distribuídos. Por fim coleta a soma de `iv_partial` para produzir o `float` total.

Há portanto ações Spark reais, inclusive `collect()` de escalares agregados e `count()` dos bins; “sem `toPandas`” não significa “sem ação ou sem coleta alguma”.

## 6. Exemplo de situação

Uma variável `faixa_renda` já foi discretizada no treino. O helper devolve WOE para baixa/média/alta e um IV total. Esse valor pode ajudar a priorizar investigação.

Se uma variável criada depois do default tiver IV enorme, isso é precisamente um motivo para investigar disponibilidade temporal — não para promovê-la ao modelo.

## 7. O que você precisa antes de usar?

As duas colunas precisam existir. `target_col` não pode conter nulos nem valores fora de 0/1 e precisa ter ambas as classes. `smoothing` deve ser positivo.

A política para nulos em `feature_col` deve ser consciente: Spark `groupBy` pode tratar `NULL` como uma faixa própria. O helper não renomeia nem explica essa categoria automaticamente.

## 8. O que este recurso entrega?

`calculate_woe_iv` devolve `(woe_df, iv_total)`. `woe_df` contém a própria coluna de feature, `n_bom`, `n_mau`, `n_total`, `pct_bom`, `pct_mau`, `woe` e `iv_partial`.

A coluna da faixa **mantém o nome de `feature_col`**, não `faixa`. Para usar com `scorecard_builder`, é necessário coletar deliberadamente o pequeno resultado para pandas e renomear essa coluna.

`classify_iv` devolve texto para cinco faixas e adiciona aviso investigativo a IV ≥ 0,50.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.woe_iv_calculator import calculate_woe_iv, classify_iv

woe_df, iv = calculate_woe_iv(
    sdf,
    feature_col="faixa_renda",
    target_col="flag_default",
    smoothing=0.5,
)
print(iv, classify_iv(iv))
```

Para alimentar scorecard pandas, colete apenas a tabela agregada se ela tiver cardinalidade compatível com o driver.

## 10. Decisões e configurações que mais importam

A definição das faixas domina o IV. Dois binnings diferentes da mesma variável podem produzir IVs diferentes. O helper não persiste nem aplica regras de binning fora da base recebida.

`smoothing` evita proporções zero e WOE infinito, mas também altera o valor estimado, especialmente em bins pequenos. Compare resultados sob amostra suficiente e política estável.

## 11. Limitações, riscos e armadilhas

A classificação `Inútil/Fraca/Média/Forte/Elevada` está hard-coded no projeto. Ela deve ser tratada como referência histórica, não como requisito da Databricks, regulador ou literatura universal aplicável a todo domínio.

IV mede associação/separação na população usada. Pode ser alto por leakage, proxy, seleção de amostra ou bins superajustados. Calcular WOE/IV na base inteira antes de separar validação também transfere informação do target.

O cálculo faz múltiplas ações Spark. Em feature de cardinalidade muito alta, `groupBy`, `count` e ordenação podem ser caros, além de tornarem o conceito de WOE por “faixa” pouco útil.

## 12. Quais são as alternativas?

Para transformar coeficientes + WOE em pontos, veja [scorecard_builder](../scorecard_builder/README.md). Para diagnóstico geral de associação ou desempenho, use métricas apropriadas ao problema em vez de IV isolado.

Em variáveis contínuas, um processo explícito de binning treinado e versionado deve anteceder este helper.

## 13. Como saber se o resultado faz sentido?

Confira se as proporções suavizadas de bons e maus somam aproximadamente 1 entre as faixas e se `iv_total` é a soma de `iv_partial`. Inspecione bins pequenos, nulos e sinais do WOE.

Repita em janela temporal ou amostra de validação usando **os mesmos cortes**, sem recalibrar os bins com o target de validação, para avaliar estabilidade.

## 14. Arquivos relacionados e próximos passos

A [implementação](woe_iv_calculator.py) calcula WOE/IV e classificação; a [fachada](__init__.py) exporta `calculate_woe_iv` e `classify_iv`; o [notebook](exemplo_woe_iv_calculator.py) demonstra uma variável vazada com IV extremo.

Depois do diagnóstico, documente regras de binning e faça validação temporal/fora da amostra antes de usar a transformação em scorecard.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. A fórmula, smoothing e faixas de classificação descritas aqui são as que o código do Hub implementa; as faixas de IV não são apresentadas como norma externa obrigatória.

Este README não presume seleção automática de variável, aprovação regulatória, publicação no Databricks nem auditoria independente.