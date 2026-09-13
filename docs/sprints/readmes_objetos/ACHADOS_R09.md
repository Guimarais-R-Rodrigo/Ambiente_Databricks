# Achados R09 — avaliação, drift e MLOps

Base: `d5945e04328609878f63857cc15cf5e5039b3e75`.

1. `curves_plotly`: `n` é metadado visual; não limita a amostra. O helper é driver-side e a paleta local possui seis cores.
2. `curves_plotly`: o nome/docstring de lift usa linguagem de ganho acumulado, mas a implementação calcula lift cumulativo por fração da base ordenada.
3. `drift_detection`: sem política, o resultado é evidência `NOT_CLASSIFIED`; PSI/CSI/KS não provam degradação de performance.
4. `drift_detection`: no ramo categórico, `min_non_null` é comparado ao comprimento total da série, não à contagem não nula.
5. `drift_detection`: `severe_ks_threshold` pode ser informado sem `severe_psi_threshold`; ambos dependem da existência dos thresholds de warning.
6. `metrics_report`: KS é `ks_pct`, escala 0–100; não deve ser comparado diretamente com estatística KS 0–1.
7. `metrics_report`: MAPE exclui alvos iguais a zero e devolve NaN quando todos os alvos são zero.
8. `metrics_report`: métricas hard dependem do threshold; AUC/AP/Gini/Brier não usam o corte.
9. `mlflow_run`: `run_governado` exige parâmetros, métricas e assinatura no fechamento quando `exigir_completo=True`.
10. `mlflow_run`: `modelo()` usa o flavor `mlflow.sklearn`; modelos de outros ecossistemas precisam de registro apropriado fora desse método.
11. `mlflow_run`: a observação do notebook sobre serverless Free é evidência histórica datada, não garantia atual da plataforma.
12. `performance_monitor`: `EXAMPLE_THRESHOLDS` é política ilustrativa e precisa de calibração.
13. `performance_monitor`: `should_retrain()` não autoriza retreino; retorna candidato a investigação e passos de governança.
14. `performance_monitor`: `selecionar_metricas_do_relatorio` traduz `auc_roc` para `auc` e evita omissão silenciosa dessa métrica.
15. Os cinco objetos operam principalmente no driver; nenhum agenda monitoramento, publica modelo ou executa governança automaticamente.
