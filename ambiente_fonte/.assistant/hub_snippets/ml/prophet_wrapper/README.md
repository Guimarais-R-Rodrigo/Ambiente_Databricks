# `prophet_wrapper` — forecast com tendência, sazonalidade e calendário sob validação temporal

<!-- readme-objeto: 1.0.0 -->

Prophet representa uma série como combinação de tendência, sazonalidades, feriados e erro. Este wrapper reduz a configuração para um caso univariado com calendário de país, gera histórico + horizonte futuro e calcula métricas **in-sample**. O valor do recurso está na construção de um candidato de forecast; as métricas retornadas não substituem backtest temporal.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um wrapper local da biblioteca Prophet. |
| Para que serve? | Ajustar tendência/sazonalidade/feriados e gerar forecast futuro. |
| Use quando... | A série tem datas regulares, um target univariado e componentes coerentes com a frequência. |
| Evite quando... | Métrica in-sample for a única validação, feriados não coincidirem com o grão agregado ou regressoras externas forem essenciais. |
| Precisa de... | pandas, NumPy, Prophet e MLflow importável. |
| Entrega... | Modelo Prophet, DataFrame completo de previsão e métricas in-sample. |

Consulte a [implementação](prophet_wrapper.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_prophet_wrapper.py). O exemplo instala `prophet` sem fixar versão e reinicia o Python; reproduzir essa célula pode mudar o ambiente.

## 1. O que é?

Prophet é um modelo aditivo para séries temporais. A previsão pode reunir uma tendência por partes, sazonalidades de Fourier, efeitos de feriados e componentes adicionais. O resultado inclui `yhat` e colunas de componentes que ajudam a inspecionar como o ajuste foi composto.

`train_prophet` cria um `Prophet` com sazonalidade anual/semanal configurável, sazonalidade diária desligada, `changepoint_prior_scale` controlado por argumento e, opcionalmente, feriados nacionais.

## 2. Que problema este recurso resolve?

Ele padroniza um baseline Prophet para uma série tabular com coluna de data e valor. O chamador não precisa renomear previamente para `ds`/`y`, montar calendário nacional ou escrever manualmente o código de forecast.

O wrapper não resolve seleção de frequência, qualidade dos componentes, regressoras externas, cross-validation, tuning nem decisão sobre implantação. Esses pontos continuam fora do contrato.

## 3. Quando faz sentido usar?

Use quando tendência e sazonalidade são hipóteses plausíveis, a frequência da série está definida e você quer um candidato interpretável por componentes. Em dados diários, por exemplo, feriados podem coincidir diretamente com observações e ser incorporados pelo calendário nacional.

Também faz sentido como uma das alternativas numa comparação walk-forward com ARIMA, baseline sazonal ou outro modelo, usando as mesmas janelas e a mesma métrica futura.

## 4. Quando não usar?

Não use `mape_insample`, `rmse_insample` ou `mae_insample` como prova de previsão futura. Todas são calculadas comparando `y` com `yhat` nas datas que participaram do ajuste.

Tenha cautela especial com séries agregadas semanalmente ou mensalmente. A documentação oficial do Prophet alerta que efeitos de feriados só aparecem quando a data do feriado coincide com uma observação agregada; em dados mensais iniciados no primeiro dia (`MS`), muitos feriados que ocorrem em outros dias do mês são ignorados. Se o efeito mensal de feriado importa, ele precisa ser representado de forma compatível com o grão.

## 5. Como funciona, intuitivamente?

A função renomeia `ds_col` e `y_col` para `ds` e `y`, descarta todas as outras colunas e converte `ds` com `pd.to_datetime`. Em seguida cria o modelo, adiciona feriados do país quando `country_holidays` é uma string não vazia e chama `fit`.

`make_future_dataframe(periods=..., freq=...)` gera datas futuras **incluindo o histórico por padrão**. Por isso o DataFrame `forecast` devolvido contém linhas da amostra de treino e linhas futuras.

As métricas são calculadas por merge entre o histórico e `forecast[["ds", "yhat"]]`. O wrapper não usa uma janela externa para esse cálculo.

## 6. Exemplo de situação

Imagine 48 meses de uma série com tendência e ciclo anual. Você quer prever seis meses. O wrapper pode ajustar um candidato com `yearly=True`, mas a avaliação honesta exige reservar meses posteriores ou rodar múltiplos cortes.

Se o MAPE in-sample for 2%, a conclusão correta é “o modelo reproduziu bem a própria amostra por essa métrica”, não “o erro futuro será 2%”. Componentes como `trend` e `yearly` também precisam ser avaliados por estabilidade e plausibilidade, não apenas porque somam ao `yhat`.

## 7. O que você precisa antes de usar?

O DataFrame precisa conter `ds_col` e `y_col`. O wrapper seleciona somente essas duas colunas; qualquer regressora adicional é descartada. Datas precisam ser convertíveis por pandas e o target precisa ser aceito pelo Prophet.

A função não valida explicitamente duplicidade de datas, frequência, nulos, tamanho mínimo, `periods`, `freq`, finitude ou zero no target antes da biblioteca. O MAPE faz divisão direta por `merged["y"]`: targets zero podem produzir infinito ou `NaN`.

O módulo faz `import mlflow` no topo, então MLflow precisa estar importável mesmo com `log_mlflow=False`. A constante `SEED=42` é exportada, mas **não é usada pela função** para controlar o Prophet ou seus intervalos.

## 8. O que este recurso entrega?

Retorna `(model, forecast, metrics)`.

`forecast` é o DataFrame produzido por `model.predict`, normalmente com `ds`, `yhat`, `yhat_lower`, `yhat_upper`, `trend` e componentes. Como `make_future_dataframe` inclui o histórico, o número de linhas tende a ser `histórico + periods`, sujeito à frequência e às regras da biblioteca.

`metrics` contém `mape_insample`, `rmse_insample` e `mae_insample`. Todas descrevem o ajuste sobre datas históricas usadas no treino.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.prophet_wrapper import train_prophet

model, forecast, metrics = train_prophet(
    df,
    ds_col="dt_ref",
    y_col="saldo",
    periods=6,
    freq="MS",
    yearly=True,
    country_holidays="BR",
    log_mlflow=False,
)
```

O [notebook de exemplo](exemplo_prophet_wrapper.py) instala Prophet sem pin e reinicia o interpretador. Em ambiente controlado, fixe e teste a versão antes de usar o notebook como especificação reprodutível.

## 10. Decisões e configurações que mais importam

`freq` precisa reproduzir o grão real das observações e do horizonte. `yearly` e `weekly` só fazem sentido quando a frequência e a quantidade de história permitem aprender esses padrões.

`changepoint_prior` controla a flexibilidade da tendência: valor maior permite mais adaptação a mudanças; isso pode melhorar ajuste e aumentar risco de sobreajuste. O helper não faz busca desse parâmetro.

`country_holidays` acrescenta calendário oficial, mas o efeito depende da coincidência entre datas de feriados e observações. Em grão mensal, não assuma que “feriados BR” significa automaticamente que Carnaval, Natal e outros eventos mensais estão representados como efeito agregado.

## 11. Limitações, riscos e armadilhas

O wrapper é univariado: outras colunas são descartadas e não há `add_regressor`. As métricas são in-sample e o MAPE não protege divisão por zero.

`SEED` não controla o modelo. Prophet calcula intervalos de incerteza por amostragem; a documentação oficial descreve Monte Carlo para incerteza, e o wrapper não fixa uma semente nessa etapa. Portanto `yhat_lower`/`yhat_upper` podem variar entre execuções mesmo quando o ponto `yhat` é estável.

Com dados mensais, o Prophet também alerta para não prever granularidade mais fina do que a observada e para possíveis problemas de identificabilidade da sazonalidade dentro do mês. Use frequência futura coerente com o histórico.

O notebook histórico contém interpretações fortes sobre número mínimo de ciclos e componentes. A R06 trata essas frases como heurísticas, não como cortes universais garantidos pela API.

## 12. Quais são as alternativas?

[arima_wrapper](../arima_wrapper/README.md) oferece outro baseline univariado. [walk_forward](../walk_forward/README.md) organiza múltiplas janelas de avaliação. Baselines ingênuos, média sazonal e regressões com features temporais são referências úteis.

Quando variáveis externas são essenciais, use um fluxo que exponha regressoras explicitamente ou uma família de modelo que as receba no contrato.

## 13. Como saber se o resultado faz sentido?

Faça backtest em datas posteriores, compare erro por horizonte e confronte com um baseline simples. Inspecione `yhat` e os componentes, mas não traduza automaticamente um componente estatístico para narrativa causal de negócio.

Em dados agregados, verifique quais feriados realmente coincidiram com as datas da série e do forecast. Se o target pode ser zero, calcule uma métrica alternativa ou MAPE com política explícita.

## 14. Arquivos relacionados e próximos passos

A [implementação](prophet_wrapper.py) define o wrapper; a [fachada](__init__.py) exporta `SEED` e `train_prophet`; o [notebook](exemplo_prophet_wrapper.py) demonstra uma série mensal sintética.

Para separar janelas consulte [split_temporal](../split_temporal/README.md); para vários cortes, [walk_forward](../walk_forward/README.md). A escolha de candidato deve ser seguida de avaliação temporal fora da amostra.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `cae94988cda66a8c61ecebbe6ceed487120a76f2`. Fontes primárias consultadas em 12/09/2026: documentação oficial do Prophet sobre início rápido, diagnósticos, dados não diários, sazonalidades/feriados/regressores e intervalos de incerteza.

Em 12/09/2026 o PyPI lista Prophet `1.4.0`; o repositório oficial informa modo de manutenção a partir dessa versão. O notebook da R06 não fixa versão. Este README não presume publicação no Databricks, homologação em workspace nem auditoria independente.
