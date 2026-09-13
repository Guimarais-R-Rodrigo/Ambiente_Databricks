# `performance_monitor` — acompanhar deterioração sem automatizar decisões de retreino

<!-- readme-objeto: 1.0.0 -->

Este objeto guarda métricas por período em memória e compara sua deterioração com uma referência fixa e uma política explícita. Organiza sinais para investigação; não é serviço de monitoramento nem um mecanismo de retreino automático.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Histórico local de métricas com classificação por política. |
| Para que serve? | Identificar deterioração e sua persistência nas entradas fornecidas. |
| Use quando... | Você tem baseline comparável, métricas realizadas e limiares justificados. |
| Evite quando... | Precisa agendar tarefas, persistir alertas ou decidir implantação automaticamente. |
| Precisa de... | Métricas finitas, política e constantes do Hub; Plotly para a figura. |
| Entrega... | Histórico, status, orientação de investigação, Markdown e figura opcional. |

Consulte a [implementação](performance_monitor.py), a [fachada](__init__.py) e o [notebook](exemplo_performance_monitor.py). O exemplo não escreve tabelas; reiniciar a sessão perde o histórico em memória.

## 1. O que é?

Monitorar desempenho significa comparar uma capacidade medida hoje com uma referência definida antes. A referência, ou baseline, pode ser um período de teste representativo; a política define quanto de piora merece atenção.

`PerformanceMonitor` recebe métricas já calculadas. Não consulta previsões, não calcula AUC, não busca rótulos e não sabe se uma mudança é ruído estatístico ou deterioração real. A classificação é uma aplicação de regras numéricas.

## 2. Que problema este recurso resolve?

Responde “quanto esta métrica piorou em relação ao baseline?” e “há alertas nas últimas entradas?”. Padroniza como relatar isso sem deixar cada pessoa escolher uma interpretação depois de ver o resultado.

O nome `should_retrain` é legado. Seu retorno orienta a investigar uma candidatura a retreino, mantendo `automatic_retrain_authorized=False` quando há períodos. Uma recomendação não executa treinamento, notificação ou publicação.

## 3. Quando faz sentido usar?

Use em uma análise periódica com alvo já realizado e população comparável. Pode apoiar um notebook de acompanhamento mensal ou um processo externo que forneça os valores e cuide de persistência, agenda e revisão.

É adequado quando a política distingue métricas em que maior é melhor, como AUC, daquelas em que menor é melhor, como RMSE, e quando as escalas estão documentadas.

## 4. Quando não usar?

Não preencha métricas com rótulos provisórios para tornar o painel “atual”. Em crédito ou retenção, o horizonte do evento pode ainda não ter terminado; a comparação seria enviesada mesmo sem erro de código.

Não use a classe sozinha como monitor de produção. Ela não agenda execuções, salva histórico durável, trata eventos duplicados ou envia alertas. Para drift de entrada sem rótulos, use outro diagnóstico, não invente AUC.

## 5. Como funciona, intuitivamente?

Para `direction="higher"`, deterioração é `baseline − atual`; para `"lower"`, é `atual − baseline`. Com `delta="absolute"`, mantém a unidade; com `"relative"`, divide por `abs(baseline)`.

Por exemplo, AUC de 0,78 para 0,72 representa queda absoluta de 0,06. RMSE de 100 para 115 representa piora relativa de 0,15, ou 15%. Não confunda queda absoluta de 0,06 com queda relativa de 6%.

Cada valor recebe verde, amarelo ou vermelho por comparação com `warning` e `critical`, incluindo igualdade no corte. Melhoras produzem deterioração negativa e não disparam esses alertas unilaterais.

## 6. Exemplo de situação

Uma equipe adota, apenas como ilustração, aviso para queda absoluta de AUC de 0,03 e crítico a partir de 0,05. Com baseline 0,78 e valor atual 0,70, a queda de 0,08 torna o período crítico nessa política.

Isso não demonstra que 0,70 seja universalmente ruim ou que 0,05 seja um limite adequado. A equipe ainda precisa examinar tamanho de amostra, maturidade dos rótulos, distribuição dos clientes e causas da mudança.

## 7. O que você precisa antes de usar?

Forneça um dicionário baseline não vazio, com valores numéricos finitos e sem booleanos. Cada métrica monitorada precisa de política com `warning`, `critical`, `direction` e `delta`. Exige-se `0 <= warning < critical`; deterioração relativa não aceita baseline zero.

A classe não valida se AUC está entre zero e um, nem verifica horizonte, população ou comparabilidade. `n_predictions` aceita inteiro não negativo, mas não é usado para ajustar limiares ou calcular incerteza.

Declare as métricas obrigatórias. O relatório usa `auc_roc`, enquanto a política de exemplo usa `auc`. A função `selecionar_metricas_do_relatorio` traduz essa chave e filtra métricas sem política; passar o dicionário completo de [`metrics_report`](../metrics_report/README.md) diretamente ao monitor pode falhar.

## 8. O que este recurso entrega?

`add_period` acrescenta uma entrada a `history`, sem retorno de relatório. Guarda período, contagem, métricas, ausentes, deterioração e status por métrica. `get_current_status` retorna sem dados, incompleto, saudável, atenção ou crítico.

`should_retrain` retorna `NO_EVIDENCE` sem períodos. Havendo períodos, devolve `NO_TRIGGER` ou `INVESTIGATE_RETRAINING_CANDIDATE`, métricas críticas, quantidade de alertas consecutivos, origem declarada da política e próximos passos de governança.

`generate_report` devolve Markdown sobre a situação atual. `plot_timeline(metric)` devolve `go.Figure`, com baseline e linhas de aviso/crítico, não uma página publicada.

## 9. Como usar este recurso no Hub?

Este exemplo usa números ilustrativos e só modifica memória:

```python
from hub_snippets.ml.performance_monitor import (
    PerformanceMonitor, selecionar_metricas_do_relatorio,
)

politica = {"auc": {"warning": 0.03, "critical": 0.05,
                    "direction": "higher", "delta": "absolute"}}
base = selecionar_metricas_do_relatorio(
    {"auc_roc": 0.78, "auc_pr": 0.20}, politica,
    metricas_obrigatorias=["auc"],
)
monitor = PerformanceMonitor(base, model_name="demonstracao", policy=politica)
monitor.add_period("2026-09", {"auc": 0.70}, n_predictions=1000)
print(monitor.get_current_status())
print(monitor.should_retrain()["automatic_retrain_authorized"])
```

A [demonstração](exemplo_performance_monitor.py) mostra uma série de períodos. Ela passa explicitamente `EXAMPLE_THRESHOLDS`: apesar de o retorno registrar política fornecida pelo chamador, os números continuam sendo exemplos, não uma política calibrada.

## 10. Decisões e configurações que mais importam

Com `policy=None`, usa-se uma cópia de `EXAMPLE_THRESHOLDS` e o monitor informa que a política exige calibração. Fornecer uma política explicitamente não comprova sua aprovação ou procedência: a marca de origem distingue como ela chegou, não sua qualidade.

`require_complete_metrics=True` exige todas as métricas do baseline a cada período. Com `False`, ausências ficam registradas e o status global fica incompleto; mesmo assim, uma métrica crítica presente ainda pode produzir recomendação de investigação.

`consecutive_alert_periods=3` conta entradas consecutivas com algum alerta. Elas podem envolver métricas diferentes. Não são necessariamente três meses consecutivos, porque datas não são verificadas.

## 11. Limitações, riscos e armadilhas

Períodos são guardados na ordem das chamadas, sem ordenação cronológica nem recusa de duplicatas. Repetir o mesmo período pode aumentar a persistência registrada. Valide unicidade e sequência antes de chamar.

O histórico e baseline expostos podem ser modificados diretamente; prefira a interface pública. Não há persistência, cálculo de significância ou ponderação pelo número de previsões. Um painel verde significa apenas ausência de violação dos cortes nas métricas fornecidas.

`ks_pct` conserva a escala 0–100: KS 40 continua 40. A classe usa cores legadas e `plotly_white`; não recebe tema resolvido V04. A documentação desta sprint não migra aparência ou algoritmo.

## 12. Quais são as alternativas?

[`metrics_report`](../metrics_report/README.md) calcula as métricas; [`drift_detection`](../drift_detection/README.md) compara distribuições. [`mlflow_run`](../mlflow_run/README.md) registra experimentos, mas não substitui a persistência e a rotina de monitoramento.

Para uma análise isolada, uma tabela com baseline, valor atual e diferença pode ser suficiente. Para produção, é preciso integrar a agenda, o armazenamento, os responsáveis e o processo de revisão, em escopo separado.

## 13. Como saber se o resultado faz sentido?

Confira manualmente pelo menos uma deterioração absoluta e uma relativa. Verifique que uma melhora não gera alerta de piora e que as linhas da figura correspondem aos cortes na escala original da métrica.

Teste métrica faltante, baseline zero em regra relativa e entrada duplicada. Confira que AUC não desapareceu na seleção de nomes. Antes de considerar retreino, revise qualidade de dados/rótulos, drift, comparação offline e aprovação de governança.

## 14. Arquivos relacionados e próximos passos

A [implementação](performance_monitor.py) define política e estados; a [fachada](__init__.py) expõe a classe e o seletor; o [notebook](exemplo_performance_monitor.py) ilustra o uso. O [catálogo](../../README.md) e o [Manual](../../../MANUAL_TECNICO.md) ajudam a localizar os componentes adjacentes.

O próximo passo operacional é definir quem fornece cada métrica, como verifica maturidade e quem recebe uma recomendação de investigação. O monitor não decide esses responsáveis.

## 15. Referências

A política, estados e semântica de `should_retrain` são contratos locais: [implementação](performance_monitor.py) e [fachada](__init__.py). Para a diferença entre medir e monitorar, consulte os guias locais de [métricas](../metrics_report/README.md) e [drift](../drift_detection/README.md).

Autorrevisão R09, com casos sintéticos registrados no relatório da sprint. Nenhum limiar de exemplo é norma da Databricks ou recomendação universal; sem homologação operacional, de política ou auditoria independente.
