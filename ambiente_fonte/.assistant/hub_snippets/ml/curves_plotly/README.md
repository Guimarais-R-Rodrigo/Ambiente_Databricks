# `curves_plotly` — quatro visões complementares de um classificador binário

<!-- readme-objeto: 1.0.0 -->

Este snippet transforma eventos observados e probabilidades em figuras ROC, precisão-recall, lift e KS. Ajuda a discutir desempenho sem reduzir tudo a um número, mas não escolhe o corte nem aprova um modelo.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Quatro geradores de figuras Plotly para classificação binária. |
| Para que serve? | Explorar ordenação, captura de eventos e compromisso entre acertos e erros. |
| Use quando... | Há rótulos realizados e scores da classe `1` na mesma população. |
| Evite quando... | Você precisa provar calibração, causalidade ou desempenho multiclasse. |
| Precisa de... | NumPy, scikit-learn, Plotly e constantes do Hub; memória local suficiente. |
| Entrega... | Uma `go.Figure` por chamada; não um relatório ou monitor automático. |

Veja a [implementação](curves_plotly.py), a [fachada](__init__.py) e o [notebook](exemplo_curves_plotly.py). O exemplo usa dados sintéticos, sem gravação de tabelas.

## 1. O que é?

Uma curva diagnóstica mostra como o resultado muda quando variamos a regra de seleção. ROC relaciona a fração de eventos encontrados à fração de não eventos marcados. Precisão-recall relaciona cobertura dos eventos à qualidade da seleção. Lift compara a concentração de eventos nos maiores scores com a concentração na população.

A função chamada `plot_ks_curve` merece atenção: ela desenha TPR contra FPR e destaca a maior diferença **direcional** `TPR − FPR`. Não desenha duas distribuições acumuladas contra o valor do score.

## 2. Que problema este recurso resolve?

Ajuda a responder “quanto capturo ao aceitar mais falsos positivos?” e “o topo dos scores concentra eventos?”. As figuras apoiam uma escolha de operação, desde que população, horizonte e classe positiva estejam claros.

Nenhuma delas calcula ganho financeiro ou efeito de uma intervenção. Encontrar clientes propensos a um evento não prova que uma campanha mudará o comportamento deles.

## 3. Quando faz sentido usar?

Use na comparação de classificadores sobre a mesma população de teste ou para comunicar o comportamento de um score a quem define a capacidade de atuação. Quando o evento é raro, examine PR e lift junto da ROC: uma taxa de falsos positivos aparentemente pequena pode representar muitos casos diante de poucos eventos.

ROC continua informativa sobre discriminação em bases desbalanceadas. O cuidado é não interpretá-la sozinha como taxa de acerto entre os clientes selecionados.

## 4. Quando não usar?

Não use estas curvas para avaliar uma previsão contínua, várias classes diretamente ou alvos que ainda não tiveram tempo de ocorrer. Não trate score bruto fora de `[0, 1]` como entrada válida desta API, mesmo que certas métricas subjacentes aceitem scores sem essa restrição.

Um exemplo de uso inadequado é comparar PR de uma amostra balanceada artificialmente com PR da produção e atribuir toda a diferença ao modelo: a proporção de eventos também mudou.

## 5. Como funciona, intuitivamente?

ROC e PR percorrem cortes sobre as probabilidades. Na ROC, a diagonal representa a referência sem discriminação. Na PR, a linha horizontal marca a prevalência da amostra; é uma referência, não a curva empírica necessariamente reta de todo score aleatório.

Para lift, as linhas são ordenadas por score decrescente. Em cada fração `p`, o código seleciona `ceil(p × N)` observações e divide os eventos capturados pelos esperados numa seleção aleatória do mesmo tamanho. O resultado é lift **cumulativo**, não ganho acumulado percentual nem lift isolado de cada decil.

No KS visual, a função destaca `max(TPR − FPR)` entre pontos da ROC. Essa orientação pressupõe que scores maiores identifiquem o evento.

## 6. Exemplo de situação

Uma equipe pode analisar até 10% de uma base. Em uma ilustração, a taxa de eventos na base é 20% e, no topo selecionado, 60%: lift três. Isso comunica concentração, não o lucro esperado, que depende do custo e do resultado da ação.

O [notebook](exemplo_curves_plotly.py) usa uma fixture de 8.000 linhas. Os números históricos ali preservados não são resultados de produção nem uma nova execução desta sprint.

## 7. O que você precisa antes de usar?

Prepare vetores 1D não vazios de igual tamanho, rótulos `0/1` com ambas as classes e probabilidades finitas em `[0, 1]`. Cada posição precisa representar a mesma linha nos dois vetores. Uma série pandas fora de ordem não é realinhada automaticamente.

As funções trabalham no driver e não coletam nem amostram Spark. Defina a amostra antes de chamar, sem perder representatividade ou o alinhamento das previsões. O tamanho total e a quantidade de scores distintos afetam memória e custo.

## 8. O que este recurso entrega?

Cada função retorna uma figura editável. ROC traz AUC, PR traz Average Precision (AP), lift usa eixo X em porcentagem da base e eixo Y em multiplicador; KS é anotado na escala 0–1.

**KS aqui não é intercambiável com `ks_pct` do relatório.** O relatório usa máximo absoluto bilateral e escala 0–100. Para scores perfeitamente invertidos, a curva pode anotar zero enquanto o relatório informa 100. Nesse caso a AUC revela a inversão; KS bilateral alto não significa orientação correta.

A figura não devolve o melhor limiar operacional, intervalos de confiança ou probabilidades calibradas. AP não é a área trapezoidal sob a linha desenhada.

## 9. Como usar este recurso no Hub?

Com o Hub no caminho de importação, gere uma figura sem escrita externa:

```python
from hub_snippets.ml.curves_plotly import plot_roc_curve

y = [0, 1, 0, 1]
p = [0.1, 0.8, 0.3, 0.6]
fig = plot_roc_curve(y, p, title="ROC — demonstração sintética")
```

No notebook, exiba `fig` ou use seu método `show()`. A [demonstração completa](exemplo_curves_plotly.py) apresenta as quatro funções; não é preciso copiar sua implementação.

## 10. Decisões e configurações que mais importam

`n` altera **somente o texto do rodapé**: não limita a amostra, não muda cálculos e não valida a contagem informada. Um valor zero é substituído pelo tamanho real porque o código usa `n or len(y_true)`.

`n_bins=10` em lift significa dez pontos cumulativos, com primeiro ponto em 10%. Use inteiro entre dois e o número de linhas; com quatro pontos, o primeiro é 25%. O eixo mostra fração nominal, mas a quantidade de observações é arredondada para cima.

`show_auc=False` remove somente a anotação central da ROC; AUC permanece na legenda e no rodapé. Não interprete essa opção como desativação do cálculo.

## 11. Limitações, riscos e armadilhas

O KS direcional pode esconder uma separação na direção oposta. Empates na fronteira do topo não têm desempate de negócio próprio. Mudanças de amostra, prevalência e horizonte alteram a interpretação das curvas; não há teste estatístico automático de diferença entre modelos.

O tema é local e legado: usa `TEMA_BASE`, seis cores em `PALETA_CATEGORICA` e `_aplicar_tema` interno. Este objeto não recebe `ResolvedTheme` nem aplica automaticamente a rota V04. As quatro funções, por si, não criam sete séries; a repetição após seis cores interessa a composições que reutilizem essa paleta.

O layout e o rodapé podem exigir conferência de legibilidade no destino. A criação de uma figura em teste não é homologação visual no navegador ou no Databricks.

## 12. Quais são as alternativas?

Use [`metrics_report`](../metrics_report/README.md) para valores tabulares ou scikit-learn diretamente quando precisar dos arrays e limiares das curvas. Um gráfico de calibração responde a outra pergunta: se probabilidades previstas correspondem a frequências observadas.

Para evolução por período, [`performance_monitor`](../performance_monitor/README.md) compara métricas com uma política explícita; não substitui estas curvas de diagnóstico.

## 13. Como saber se o resultado faz sentido?

Confira quantidade de eventos, orientação do score e prevalência usada na PR. Em uma fixture perfeitamente ordenada, AUC deve ser 1; invertendo os scores, deve ser 0. Use essa inversão para perceber a diferença entre KS visual direcional e KS bilateral.

O lift no ponto de 100% deve ser um. Altere apenas `n` e confirme que os dados dos traços não mudam. Compare figuras somente depois de conferir população, horizonte e unidade dos indicadores.

## 14. Arquivos relacionados e próximos passos

A [implementação](curves_plotly.py) define os cálculos e o layout; a [fachada](__init__.py) expõe os quatro geradores e constantes legadas; o [notebook](exemplo_curves_plotly.py) orienta a leitura. O [catálogo](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md) organizam as demais peças.

Escolha as figuras que respondem à decisão e registre também os critérios de corte e as limitações, em vez de apresentar apenas a figura mais favorável.

## 15. Referências

Comportamento local conferido na implementação/fachada da base R09. Referências primárias: [ROC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html), [precisão-recall](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html), [AP](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html) e [KS bilateral](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html). Consultadas em 13/09/2026; a última descreve a alternativa bilateral, não redefine o KS desta figura.

Autorrevisão documental R09; execução sintética registrada no relatório da sprint, sem homologação visual ou de modelos.
