# `score_bands` — bandas quantílicas para diagnóstico de score, não política de aprovação pronta

<!-- readme-objeto: 1.0.0 -->

Este helper divide um vetor de scores em faixas quantílicas, ordena essas faixas da melhor para a pior direção declarada e resume volume e taxa do evento. Ele serve para inspecionar concentração, monotonicidade e cobertura acumulada; **não escolhe um cutoff de negócio nem transforma automaticamente banda em decisão de crédito**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Resumo pandas de bandas quantílicas de um score. |
| Para que serve? | Ver distribuição do score, taxa do evento e cobertura acumulada por faixa. |
| Use quando... | A direção do score e o significado de `y_true=1` estiverem claros. |
| Evite quando... | Precisar de cortes fixos entre populações, política de aprovação ou calibração probabilística. |
| Precisa de... | NumPy e pandas; arrays unidimensionais alinhados. |
| Entrega... | DataFrame ordenado com score mínimo/máximo, volume, evento e cobertura cumulativa. |

Consulte a [implementação](score_bands.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_score_bands.py).

## 1. O que é?

`generate_score_bands` usa `pandas.qcut` para formar grupos por quantis do score. Quantis procuram distribuir observações por posição na amostra, não por distâncias iguais no valor do score.

Depois, o helper ordena os intervalos segundo `higher_score_is_better` e calcula estatísticas em cada banda.

## 2. Que problema este recurso resolve?

Uma AUC ou uma média de score não mostra como o risco se distribui ao longo da carteira. As bandas permitem responder perguntas como: “os eventos se concentram nas piores faixas?” e “quanto da base está coberto até esta faixa?”.

Isso é diagnóstico. A função não conhece custo de falso positivo, capacidade operacional, apetite a risco ou restrições regulatórias.

## 3. Quando faz sentido usar?

Use para validar ordenação de um score numa população específica, comparar taxas do evento entre quantis e preparar discussão de cutoffs.

Também é útil para revelar empates de score, concentração em piso/teto e perda de resolução efetiva.

## 4. Quando não usar?

Não use as faixas de duas amostras independentes como se os limites fossem os mesmos. Cada chamada recalcula quantis na própria base.

Não use `aprovacao_acum` como aprovação realizada. O nome histórico da coluna representa a **fração cumulativa de observações percorridas da melhor para a pior banda**, segundo a direção declarada. Só vira taxa de aprovação de uma política se um cutoff e uma regra operacional realmente forem aplicados nessa ordem.

## 5. Como funciona, intuitivamente?

A função valida scores finitos e target binário, executa `qcut(..., duplicates="drop")`, ordena os intervalos pelo ponto médio do intervalo quantílico (`interval.mid`), não pela mediana dos scores observados e percorre as bandas acumulando `pct_base`.

Como `y_true=1` é assumido como evento adverso, `n_mau` é a soma do target e `n_bom` é o restante. O nome `taxa_default` também herda essa convenção de crédito.

## 6. Exemplo de situação

Um score de risco maior significa maior chance de inadimplência. Você chama `higher_score_is_better=False` e pede dez bandas. A tabela deve começar pela faixa de menor score e, se o modelo ordena bem, a taxa de evento tende a crescer ao avançar para bandas piores.

Isso não significa que a curva precise ser perfeitamente monotônica em toda amostra; ruído amostral e empates podem produzir desvios.

## 7. O que você precisa antes de usar?

O helper recusa `n_bands < 2` e exige pelo menos dois valores distintos de score. Score constante não produz uma banda válida nessa API; trate-o como diagnóstico de falta de variação, sem fabricar faixas artificiais.

`scores` e `y_true` devem ser vetores 1D, não vazios e do mesmo tamanho. Scores precisam ser finitos. `y_true` aceita apenas 0 e 1 e a implementação interpreta 1 como evento adverso.

É necessário conhecer a direção do score. O parâmetro possui default `True`; portanto a direção **não é exigida sintaticamente**, apesar de ser obrigatória conceitualmente. Passe o valor explicitamente em código de produção para evitar ambiguidade.

## 8. O que este recurso entrega?

O DataFrame contém `faixa`, `score_min`, `score_max`, `n`, `pct_base`, `n_bom`, `n_mau`, `taxa_default`, `aprovacao_acum` e `higher_score_is_better`.

O número de linhas pode ser menor que `n_bands`: a implementação usa `duplicates="drop"` e elimina cortes quantílicos repetidos quando muitos scores estão empatados.

## 9. Como usar este recurso no Hub?

Caso sintético mínimo e recusa esperada de score constante:

```python
from hub_snippets.ml.score_bands import generate_score_bands
bandas = generate_score_bands([10, 20, 30, 40], [0, 0, 1, 1],
                              n_bands=2, higher_score_is_better=False)
assert bandas["n"].tolist() == [2, 2]
assert bandas["taxa_default"].tolist() == [0.0, 100.0]
assert bandas["aprovacao_acum"].tolist() == [50.0, 100.0]
try:
    generate_score_bands([600, 600], [0, 1], n_bands=2)
except ValueError as erro:
    assert "scores must vary" in str(erro)
else:
    raise AssertionError("score constante deveria ser recusado")
```

Esses números apenas conferem a fixture; uma banda com evento de 100% não é uma regra de decisão automática.

```python
from hub_snippets.ml.score_bands import generate_score_bands

bandas = generate_score_bands(
    score,
    y_true,
    n_bands=10,
    higher_score_is_better=False,
)
```

Confira `len(bandas)` antes de fornecer rótulos ou assumir que todos os quantis pedidos existem.

## 10. Decisões e configurações que mais importam

`higher_score_is_better` determina a ordem das faixas e, por consequência, o sentido da acumulação. Uma configuração errada produz uma tabela coerente matematicamente, mas semanticamente invertida.

`n_bands` controla granularidade. Muitas bandas com pouca amostra elevam variância; poucas bandas escondem estrutura. `labels`, quando fornecido, precisa ter exatamente o número de bandas efetivas após a remoção de bordas duplicadas.

## 11. Limitações, riscos e armadilhas

`qcut` cria cortes específicos da amostra. Para monitoramento longitudinal com limites fixos, salve e reutilize uma definição de bins; este helper não oferece esse contrato.

O nome `taxa_default` é específico de crédito, mas a função tecnicamente aceita qualquer target binário. Se o evento não for default, renomeie ou documente a coluna no consumo para evitar interpretação errada.

`aprovacao_acum` é cobertura cumulativa, não decisão. A função não mede lucro, perda esperada, capacidade, fairness ou restrição de política.

## 12. Quais são as alternativas?

Use [scorecard_builder](../scorecard_builder/README.md) para construir contribuições de pontos e [metrics_report](../metrics_report/README.md) para métricas globais. Para comparar populações com as mesmas fronteiras, use bins fixos versionados; este helper recalcula quantis a cada chamada.

## 13. Como saber se o resultado faz sentido?

Confira se `pct_base` soma aproximadamente 100%, se `aprovacao_acum` termina em aproximadamente 100% e se `n_bom + n_mau == n` por faixa. Valide também a direção do score contra uma amostra conhecida.

Observe empates e o número real de bandas. Compare taxas com intervalos de incerteza quando a decisão depender de diferenças pequenas entre faixas.

## 14. Arquivos relacionados e próximos passos

A [implementação](score_bands.py) define o resumo; a [fachada](__init__.py) exporta `generate_score_bands`; o [notebook](exemplo_score_bands.py) mostra colapso de quantis causado por score empatado.

Depois de diagnosticar a ordenação, uma política de corte precisa incorporar custo, restrições e validação fora da amostra.

## 15. Referências

Consulte pandas.qcut para a remoção de limites quantílicos repetidos. O número de bandas pode ser menor que o solicitado. A tabela é diagnóstica; decisões de corte exigem política e validação próprias.