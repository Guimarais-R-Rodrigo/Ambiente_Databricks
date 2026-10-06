# `kaplan_meier` — sobrevivência e comparação de grupos com censura explícita

<!-- readme-objeto: 1.0.0 -->

Kaplan–Meier estima a probabilidade de permanecer sem o evento ao longo do tempo usando também observações censuradas. Este helper ajusta curvas com `lifelines`, constrói uma figura Plotly e oferece teste log-rank para dois ou mais grupos. Ele ajuda a descrever tempo até evento; **não identifica causalidade nem garante que a censura seja não informativa**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Wrapper local para curvas Kaplan–Meier e testes log-rank. |
| Para que serve? | Descrever sobrevivência/tempo até evento e comparar curvas entre grupos. |
| Use quando... | Houver duração, indicador de evento e censura à direita compatíveis com o método. |
| Evite quando... | A censura for informativa, houver entrada tardia não representada ou a pergunta for efeito causal ajustado. |
| Precisa de... | pandas, Plotly e `lifelines` na chamada. |
| Entrega... | Figura Plotly e dicionário de resultados do log-rank. |

Consulte a [implementação](kaplan_meier.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_kaplan_meier.py). O notebook instala `lifelines` e reinicia o Python; isso é uma ação de ambiente do exemplo.

## 1. O que é?

A curva Kaplan–Meier estima a função de sobrevivência `S(t)`: a probabilidade estimada de ainda não ter ocorrido o evento até o tempo `t`. Quando uma observação termina sem evento, ela contribui até seu tempo de censura e depois deixa o conjunto em risco sem ser contada como evento.

`plot_kaplan_meier` ajusta uma curva global ou uma por grupo. `log_rank_test` compara as curvas segundo o teste log-rank.

## 2. Que problema este recurso resolve?

Contar eventos ignora o tempo de acompanhamento e trata observações recentes como se tivessem tido a mesma oportunidade de falhar que observações antigas. O helper organiza esse problema de tempo até evento e censura.

Ele não resolve confundimento entre grupos. Uma curva diferente entre segmentos pode refletir composição, seleção ou covariáveis omitidas.

## 3. Quando faz sentido usar?

Use em churn, inadimplência, tempo até recompra, falha de equipamento ou outro evento em que parte da população ainda não tenha experimentado o evento quando a janela de observação termina.

Para comparação descritiva de grupos, declare `group_col`. Para investigar associações ajustadas por covariáveis, o Cox pode ser mais apropriado.

## 4. Quando não usar?

Não use se a forma de censura for incompatível com o desenho. A implementação de log-rank usada aqui é para censura à direita. Se a saída da observação estiver relacionada ao risco do evento, a interpretação padrão pode ficar enviesada.

Não use p-valor do log-rank como medida de magnitude ou causalidade. Curvas que se cruzam também exigem cautela: o log-rank padrão tem sua melhor propriedade de potência sob riscos proporcionais.

## 5. Como funciona, intuitivamente?

Para cada grupo, o helper cria `KaplanMeierFitter`, ajusta `duration_col` e `event_col`, extrai `survival_function_`, mediana e intervalo de confiança. A figura é construída manualmente com Plotly.

Com dois grupos, `log_rank_test` devolve `statistic` e `p_value`. Com mais de dois, primeiro executa teste global multivariado e depois todos os pares, aplicando correção de Holm implementada localmente.

## 6. Exemplo de situação

Uma carteira acompanha clientes por até 24 meses. Parte cancela antes; parte chega ao fim sem cancelar. A curva Kaplan–Meier permite comparar a permanência de dois segmentos sem transformar os censurados em “não eventos definitivos”.

Se a curva de um grupo cair mais lentamente, isso descreve a experiência observada. A conclusão não deve ser “pertencer ao grupo causa maior retenção” sem desenho causal.

## 7. O que você precisa antes de usar?

Pré-validações do chamador para a rota de teste (não são garantias implementadas pelo helper):

```python
import numpy as np
assert not df.empty
assert df[["duracao", "evento", "segmento"]].notna().all().all()
assert np.isfinite(df["duracao"].to_numpy(dtype=float)).all()
assert (df["duracao"] >= 0).all()  # confirme se zero é admissível no desenho
assert df["evento"].isin([0, 1]).all()
assert df["segmento"].nunique() >= 2
```

Use unidades e origem temporal comuns; não descarte censurados para satisfazer essas verificações.

`duration_col` precisa representar tempo coerente desde a origem definida; `event_col` precisa representar evento observado versus censura conforme o contrato do `lifelines`. O helper atual não valida explicitamente duração positiva, binariedade, nulos ou grupos vazios antes da biblioteca subjacente.

Quando `group_col` existe, valores nulos merecem tratamento explícito. O `groupby` da figura e o uso de `unique()` no teste não constituem uma política de missingness documentada pelo helper.

## 8. O que este recurso entrega?

Estruturas de retorno ilustrativas, sem inventar valores observados:

- Dois grupos A/B: `{"statistic": ..., "p_value": ...}`; sem flag booleana.
- Três grupos A/B/C: `{"global": {"statistic": ..., "p_value": ..., "significant_0_05": ...}, "pairwise_holm": {"A_vs_B": {...}, "A_vs_C": {...}, "B_vs_C": {...}}`.
- Cada par contém `statistic` (estatística do teste), `p_value_raw` (bruto), `p_value_holm` (ajustado no conjunto de pares) e `significant_holm_0_05` (`p_value_holm < 0.05`). Nomes e ordem dos pares seguem os grupos encontrados.

As flags usam um corte local de 0,05 e não medem relevância prática ou causalidade.

`plot_kaplan_meier(...)` devolve `plotly.graph_objects.Figure`. A legenda inclui tamanho do grupo e `median_survival_time_`; se a mediana não for atingida no horizonte observado, o `lifelines` pode representar a mediana como infinito.

`log_rank_test(...)` muda de formato conforme o número de grupos. Para dois grupos retorna um dicionário simples. Para mais de dois retorna `global` e `pairwise_holm`, com p-valores brutos e ajustados de Holm.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.kaplan_meier import plot_kaplan_meier, log_rank_test

fig = plot_kaplan_meier(
    df,
    duration_col="duracao",
    event_col="evento",
    group_col="segmento",
)
resultado = log_rank_test(df, "duracao", "evento", "segmento")
```

A função devolve a figura; a renderização (`fig.show()`) continua sendo decisão do notebook.

## 10. Decisões e configurações que mais importam

A definição do tempo zero, do evento e da censura domina a interpretação. Mudar qualquer uma altera o estimando, mesmo com o mesmo código.

`ci=True` inclui faixa de confiança de 95% na figura. `group_col=None` gera curva global. Em mais de dois grupos, a correção de Holm reduz o risco de interpretar vários testes par-a-par como se cada um fosse o único teste feito.

## 11. Limitações, riscos e armadilhas

O estimador é Kaplan–Meier, mas a figura Plotly conecta os pontos com linhas padrão, sem `line_shape="hv"`. Não a descreva como desenho em degraus nem como prova de evolução linear entre eventos. Alterar a geometria requer uma mudança funcional separada.

A figura usa a censura no estimador, mas não exibe marcadores de censura nem tabela de indivíduos em risco. Não há argumentos de entrada tardia ou pesos. O retorno de log_rank_test para dois grupos contém statistic e p_value, sem flag booleana de significância.

P-valor pequeno não mede tamanho de efeito. Para muitos grupos, os testes par-a-par são ajustados por Holm, mas a escolha do conjunto de comparações ainda pertence à análise.

## 12. Quais são as alternativas?

[survival_cox](../survival_cox/README.md) ajusta associações de covariáveis sob riscos proporcionais. Modelos AFT ou outros métodos de sobrevivência podem ser preferíveis quando a estrutura do problema não cabe no Cox/log-rank.

Para uma pergunta de incidência por safra e maturidade, [vintage_analysis](../vintage_analysis/README.md) responde a outro desenho e não deve ser confundido com sobrevivência individual.

## 13. Como saber se o resultado faz sentido?

Confira número de observações, eventos e censurados por grupo. Veja se a cauda é sustentada por quantidade suficiente de indivíduos em risco. Compare a definição do tempo com o processo operacional real.

Para o log-rank, examine as curvas antes de resumir tudo a um p-valor, especialmente quando elas cruzam. Em mais de dois grupos, leia primeiro o teste global e depois as comparações ajustadas.

## 14. Arquivos relacionados e próximos passos

A [implementação](kaplan_meier.py) contém plot e testes; a [fachada](__init__.py) exporta `plot_kaplan_meier` e `log_rank_test`; o [notebook](exemplo_kaplan_meier.py) demonstra censura sintética.

Depois da descrição não ajustada, defina se a pergunta pede associação multivariada, predição ou efeito causal antes de escolher a próxima técnica.

## 15. Referências

Consulte KaplanMeierFitter e os testes logrank_test/multivariate_logrank_test do lifelines. O contrato usa censura à direita; curvas cruzadas, tamanho dos grupos e indivíduos ainda sob risco precisam entrar na interpretação.