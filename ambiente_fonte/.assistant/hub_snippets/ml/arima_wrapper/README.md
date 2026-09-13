# `arima_wrapper` — auto-ARIMA como candidato de previsão, não como validação automática

<!-- readme-objeto: 1.0.0 -->

ARIMA modela uma série a partir da relação entre valores passados, diferenciações e erros passados. Este helper usa `pmdarima.auto_arima` para procurar uma ordem dentro do espaço configurado, gerar previsões e resumir o ajuste in-sample. A busca automatiza parte da escolha de especificação; ela **não demonstra que o processo gerador foi identificado nem que a previsão generaliza fora da amostra**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper local de `pmdarima.auto_arima`. |
| Para que serve? | Ajustar um candidato ARIMA/SARIMA e produzir forecast de horizonte fixo. |
| Use quando... | Houver uma série univariada ordenada, frequência compreendida e avaliação temporal separada. |
| Evite quando... | A métrica in-sample for a única evidência, houver covariáveis essenciais ou o histórico não sustentar a sazonalidade proposta. |
| Precisa de... | `pmdarima`, NumPy e MLflow se `log_mlflow=True`. |
| Entrega... | Modelo ajustado, vetor de forecast e dicionário de métricas in-sample. |

Consulte a [implementação](arima_wrapper.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_arima_wrapper.py). O notebook instala `pmdarima==2.0.4` com `numpy==1.23.5` e reinicia o Python; isso é uma decisão de ambiente do exemplo, não uma dependência versionada pelo pacote do Hub.

## 1. O que é?

Um modelo ARIMA é descrito por `(p, d, q)`: termos autorregressivos, ordem de diferenciação e termos de média móvel. No caso sazonal, acrescenta-se uma ordem sazonal `(P, D, Q, m)`. O objetivo é representar dependência temporal em uma série depois que as transformações de diferenciação tornaram o componente modelado compatível com a especificação.

`train_arima` delega a seleção de ordem a `pmdarima.auto_arima` em modo `stepwise=True`. O helper não expõe o espaço completo de busca nem o critério de informação; portanto usa os defaults da biblioteca para os argumentos não declarados.

## 2. Que problema este recurso resolve?

Ele reduz o trabalho mecânico de testar manualmente várias ordens ARIMA/SARIMA e padroniza três saídas: objeto ajustado, previsão e métricas do ajuste. Isso é útil como baseline de séries temporais ou como candidato em uma comparação temporal controlada.

O problema que ele **não** resolve é validação futura. AIC, BIC, RMSE in-sample e MAPE in-sample descrevem o ajuste à história usada no treino; não estimam, por si, o erro nos próximos períodos.

## 3. Quando faz sentido usar?

Use quando o target é uma série univariada com ordem temporal conhecida, as observações têm uma frequência coerente com `m` e existe histórico suficiente para estimar a estrutura desejada. Para um baseline mensal sazonal, por exemplo, `m=12` pode representar um ciclo anual se cada observação realmente corresponder a um mês.

Também faz sentido comparar o candidato com uma referência mais simples e com outro método de forecast sob o mesmo protocolo de `walk_forward` ou corte temporal. A seleção de ordem e a avaliação devem ser tratadas como etapas diferentes.

## 4. Quando não usar?

Não use as métricas retornadas como aprovação de forecast. Elas são calculadas sobre a própria amostra ajustada. Não use `m=12` apenas porque a série é “mensal” sem verificar se existe evidência e extensão histórica para uma sazonalidade anual.

O wrapper é univariado: não recebe regressoras exógenas. Se variáveis externas são materialmente importantes para previsão, o contrato atual não as representa.

## 5. Como funciona, intuitivamente?

A função chama `pm.auto_arima` com `seasonal`, `m`, busca stepwise, supressão de warnings e `error_action="ignore"`. Depois chama `predict(..., return_conf_int=True)` para o horizonte pedido.

Os resíduos do modelo são usados para RMSE e MAPE in-sample. O intervalo de confiança também é calculado pela biblioteca, mas o helper atual **descarta `conf_int` no retorno**. Quando `log_mlflow=True`, parâmetros básicos e métricas numéricas são enviados ao MLflow.

Um detalhe importante do contrato real: o código passa `random_state=42` e `n_fits=50`, mas a documentação de `pmdarima` define esses parâmetros para a busca aleatória (`random=True`, com `stepwise=False`). Como este helper usa `stepwise=True` e não ativa `random`, não trate `SEED` ou `n_fits=50` como garantia de uma busca aleatória de 50 modelos.

## 6. Exemplo de situação

Imagine uma série mensal de volume com quatro anos de histórico. Você quer um baseline univariado para os próximos seis meses. Primeiro separa uma janela histórica de avaliação; depois ajusta `train_arima` somente no trecho de treino e compara as previsões com o período futuro reservado.

A informação útil é “esta especificação escolhida pela busca teve este desempenho fora da amostra neste protocolo”. Não é correto concluir que uma ordem `(0,1,0)` prova que o processo real é um passeio aleatório apenas porque ela minimizou o critério usado dentro do espaço pesquisado.

## 7. O que você precisa antes de usar?

A série deve estar em ordem cronológica, ser unidimensional e compatível com `pmdarima`. O helper não valida explicitamente tamanho mínimo, finitude, `NaN`, frequência, espaçamento temporal ou quantidade de ciclos sazonais antes de chamar a biblioteca.

`forecast_periods` precisa fazer sentido operacionalmente; o wrapper também não valida se é positivo antes da chamada subjacente. Para MAPE, zeros são excluídos pelo `mask = series != 0`; se todos os valores forem zero, a média é calculada sobre conjunto vazio e pode resultar em `NaN`.

O módulo importa `mlflow` no topo. Portanto MLflow precisa estar importável mesmo quando `log_mlflow=False`. `pmdarima` é importado apenas dentro da função.

## 8. O que este recurso entrega?

O retorno é `(model, forecast, metrics)`.

`forecast` contém somente a previsão pontual para os `forecast_periods`. O dicionário `metrics` contém `aic`, `bic`, `order`, `seasonal_order`, `rmse_insample` e `mape_insample`. `order` e `seasonal_order` são convertidos para string no dicionário.

O intervalo calculado por `predict(..., return_conf_int=True)` não é devolvido. Se a decisão depende de incerteza preditiva, o consumidor precisa usar o modelo retornado ou outro fluxo que preserve os intervalos.

## 9. Como usar este recurso no Hub?

Depois de tornar `.assistant` importável:

```python
from hub_snippets.ml.arima_wrapper import train_arima

model, forecast, metrics = train_arima(
    serie,
    m=12,
    forecast_periods=6,
    seasonal=True,
    log_mlflow=False,
)
```

O [notebook de exemplo](exemplo_arima_wrapper.py) instala dependências e reinicia o interpretador. Revise a política do ambiente antes de reproduzir essa célula. No exemplo, o logging é desligado para evitar efeito externo.

## 10. Decisões e configurações que mais importam

`seasonal` e `m` mudam o espaço de modelos. `m` representa número de observações por ciclo sazonal, não uma unidade de calendário detectada automaticamente. Uma série mensal regular pode usar 12 para anualidade; uma série irregular exige preparação anterior.

`forecast_periods` define o horizonte. Horizonte maior normalmente aumenta a dependência de hipóteses estruturais; o wrapper não faz backtest automático para mostrar como o erro cresce.

A seleção usa os defaults de `auto_arima` para argumentos não expostos, inclusive o critério de informação. Se esse contrato precisar mudar, a implementação deverá evoluir explicitamente; não presuma parâmetros invisíveis pela documentação do notebook.

## 11. Limitações, riscos e armadilhas

As métricas são in-sample. AIC/BIC ajudam a comparar especificações sob hipóteses e amostra dadas, não são métricas de negócio nem teste futuro. `error_action="ignore"` também reduz a visibilidade de combinações que falharam durante a busca.

O intervalo de confiança é descartado. O wrapper não recebe regressoras exógenas, não testa autocorrelação residual, não verifica quebra estrutural e não implementa validação walk-forward.

O notebook histórico afirma que a ordem escolhida é a “melhor descrição” e associa uma ordem observada diretamente ao processo gerador. A R06 qualifica essa leitura: é a especificação selecionada pelo procedimento, no espaço e critério usados, para aquela amostra.

## 12. Quais são as alternativas?

[prophet_wrapper](../prophet_wrapper/README.md) representa tendência, sazonalidades e feriados de outra forma. [walk_forward](../walk_forward/walk_forward.py) fornece um protocolo de avaliação por múltiplos cortes. Baselines simples como último valor, média sazonal ou regressão temporal também são comparações importantes.

Para séries com regressoras exógenas ou estruturas específicas, uma API de SARIMAX ou outro modelo pode ser mais adequada que este wrapper reduzido.

## 13. Como saber se o resultado faz sentido?

Reserve períodos posteriores e compare forecast com observações que não participaram da seleção nem do ajuste. Examine resíduos, erro por horizonte e estabilidade da ordem entre janelas. Compare com um baseline ingênuo.

Confira `model.order`, `model.seasonal_order` e o resumo do modelo. Se `seasonal=True`, valide se `m` corresponde à periodicidade real. Não use apenas um RMSE in-sample baixo como evidência de generalização.

## 14. Arquivos relacionados e próximos passos

A [implementação](arima_wrapper.py) define o wrapper; a [fachada](__init__.py) exporta `SEED` e `train_arima`; o [notebook](exemplo_arima_wrapper.py) demonstra uma série sintética. Para avaliação temporal, consulte [walk_forward](../walk_forward/walk_forward.py) e [split_temporal](../split_temporal/split_temporal.py).

Depois de escolher um candidato, o próximo passo é medir fora da amostra e documentar o protocolo, não promover a ordem escolhida a verdade sobre o processo.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. Fontes primárias consultadas em 12/09/2026: documentação `AutoARIMA`/`auto_arima` do pmdarima 2.0.x e exemplo oficial de `auto_arima`. A documentação da biblioteca informa que `d` pode ser selecionado por teste de raiz unitária, que a busca stepwise procura uma especificação segundo o critério configurado e que `random_state`/`n_fits` pertencem à busca aleatória, não ao caminho stepwise usado aqui.

O notebook fixa `pmdarima==2.0.4`; em 12/09/2026 o PyPI aponta `pmdarima 2.1.1` como release mais recente. A evidência de runtime desta R06 será registrada no relatório da sprint. Este README não presume publicação no Databricks, homologação em workspace nem auditoria independente.
