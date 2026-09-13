# `performance_monitor` — métricas periódicas contra política explícita

<!-- readme-objeto: 1.0.0 -->

Este objeto mantém um histórico em memória de métricas de modelo e compara deterioração contra uma política declarada. Ele produz evidência para investigação; não agenda execução, não persiste dados, não envia alertas e não autoriza mudanças de modelo automaticamente.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Monitor em memória com baseline, thresholds e histórico periódico. |
| Para que serve? | Padronizar warning/critical e acompanhar persistência de deterioração. |
| Use quando... | Baseline, escala, periodicidade e política foram definidos. |
| Evite quando... | Você precisa de scheduler, persistência, target ainda imaturo ou decisão automática. |
| Precisa de... | Python; Plotly apenas para timeline. |
| Entrega... | Histórico, status, recomendação de investigação, Markdown e figura opcional. |

Consulte a [implementação](performance_monitor.py), a [fachada](__init__.py) e o [notebook](exemplo_performance_monitor.py).

## 1. O que é?

`PerformanceMonitor` compara métricas observadas com baseline e regras contendo `warning`, `critical`, `direction` e `delta`. O módulo também traduz algumas chaves de `metrics_report` para o vocabulário da política.

## 2. Que problema este recurso resolve?

Evita que cada queda mensal seja julgada visualmente sem uma régua prévia. A política explicita quanto de deterioração merece atenção e quanto merece investigação prioritária.

## 3. Quando faz sentido usar?

Use quando o target já maturou e as métricas periódicas são comparáveis ao baseline. É uma camada de evidência para rotinas de monitoramento e governança.

## 4. Quando não usar?

Não use thresholds de exemplo sem calibração. Não use com target ainda não realizado. O método legado `should_retrain()` retorna orientação de investigação e mantém `automatic_retrain_authorized=False`; não é ordem automática.

## 5. Como funciona, intuitivamente?

Para métricas `higher`, deterioração é `baseline - atual`; para `lower`, `atual - baseline`. O delta pode ser absoluto ou relativo. Cada período recebe status verde, amarelo ou vermelho.

A recomendação considera métricas críticas no último período e sequência recente de períodos com alerta.

## 6. Exemplo de situação

Uma AUC baseline de 0,78 é acompanhada mensalmente. Uma política calibrada define queda absoluta de 0,03 como warning e 0,05 como critical. O monitor registra a série e sinaliza investigação quando a régua é excedida.

## 7. O que você precisa antes de usar?

Baseline não vazio, numérico e finito. A política precisa cobrir todas as métricas monitoradas; `warning < critical`; direção deve ser `higher`/`lower`; delta `absolute`/`relative`. Delta relativo não é aceito para baseline zero.

## 8. O que este recurso entrega?

`history`, `get_current_status()`, `should_retrain()`, `generate_report()` e `plot_timeline()`. `EXAMPLE_THRESHOLDS` é apenas política ilustrativa.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.performance_monitor import PerformanceMonitor

policy = {"auc": {"warning": 0.03, "critical": 0.05,
                  "direction": "higher", "delta": "absolute"}}
monitor = PerformanceMonitor({"auc": 0.78}, policy=policy)
monitor.add_period("2026-08", {"auc": 0.73}, n_predictions=12000)
print(monitor.get_current_status())
```

O exemplo cria apenas estado em memória. Para uma rotina operacional, persista métricas e períodos fora da classe e interprete qualquer trigger como pedido de investigação, não como autorização de retreino.

## 10. Decisões e configurações que mais importam

A política é central. `require_complete_metrics=True` exige todas as métricas por período. `selecionar_metricas_do_relatorio` traduz `auc_roc -> auc` e preserva chaves compatíveis como `ks_pct`, `gini`, `rmse` e `mape`.

## 11. Limitações, riscos e armadilhas

Estado apenas em memória; sem persistência, maturação de target, intervalos de confiança ou teste de significância. `EXAMPLE_THRESHOLDS` precisa ser calibrado por modelo e risco.

A escala de `ks_pct` é 0–100. O nome legado `should_retrain` pode induzir leitura excessiva; leia `decision`, `automatic_retrain_authorized` e `required_next_steps`.

## 12. Quais são as alternativas?

Para orquestração e persistência, use jobs e tabelas institucionais. Para cálculo, veja [`metrics_report`](../metrics_report/README.md). Para mudança de distribuição de entrada, veja [`drift_detection`](../drift_detection/README.md).

## 13. Como saber se o resultado faz sentido?

Valide escala, direção e unidade de cada métrica. Simule valores exatamente nos thresholds e compare a política com variabilidade histórica e custo de falso alerta.

## 14. Arquivos relacionados e próximos passos

A [implementação](performance_monitor.py) contém política, tradução e monitor; a [fachada](__init__.py) expõe a API pública; o [notebook](exemplo_performance_monitor.py) demonstra degradação sintética.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da R09. Os thresholds são política local, não defaults de Databricks, MLflow ou scikit-learn. Para as figuras, consulte a documentação oficial do Plotly.