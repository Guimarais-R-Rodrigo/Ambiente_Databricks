---
name: hub-ml-monitoramento-modelo
description: Desenha e implementa monitoramento de modelos no Databricks para qualidade de dados, drift, performance, calibração, fairness, latência, custo e decisão de retreino, integrando MLflow, Models in Unity Catalog, Lakehouse Monitoring e tabelas de inferência quando aplicável. Usar quando pedirem monitoramento, PSI/CSI/KS, drift, degradação, alerta, dashboard, endpoint, inference table, retreino, champion/challenger ou operação de modelo.
---

# Monitorar modelos em produção

## Quando esta skill se aplica

- Pedem **monitoramento, PSI/CSI/KS, drift, degradação, alerta, dashboard,
  inference table, retreino ou champion/challenger**.
- O modelo **já está em produção** — ou está prestes a entrar, e a pergunta é o
  que observar.

**Não cobre:** comparar coortes de originação (`hub-ml-analise-safra`) nem
explicar por que o modelo decide o que decide (`hub-ml-explainability`).

## Definir o contrato operacional

Registrar modelo/alias, versão, endpoint ou job, população, frequência, SLA, target disponível/atraso, baseline de referência, owners, canal de alerta e runbook. Não criar trigger de retreino sem owner e validação.

## Monitorar em camadas

1. **Serviço:** disponibilidade, erro, latência, throughput, fila e custo.
2. **Dados:** freshness, schema, nulos, volume, domínio e cobertura.
3. **Drift:** distribuições de features, score e população.
4. **Performance:** métrica primária, calibração e threshold quando o label chegar.
5. **Segmentos:** cohorts críticos, fairness e estabilidade.
6. **Negócio:** KPI downstream e guardrails, sem confundir correlação com efeito causal.

Usar Lakehouse Monitoring, tabelas de inferência e capacidades de Model Serving somente quando disponíveis no workspace/cloud. Confirmar a documentação oficial e permissões atuais antes de gerar instruções.

## Calcular drift corretamente

- Congelar bins/categorias na referência.
- Incluir missing e categoria nova explicitamente.
- Usar smoothing documentado para evitar log de zero.
- Reportar volume, período, referência e incerteza.
- Avaliar drift por segmento e não apenas média global.
- Tratar PSI/CSI/KS como sinais diagnósticos, não prova de queda de performance.

Não substituir PSI por deslocamento absoluto da média. Não aplicar limites `0,1/0,25` como padrão universal; calibrar pela variabilidade histórica, risco e política.

## Avaliar performance

Comparar na mesma definição/população e considerar atraso de labels. Distinguir deterioração de melhoria: calcular delta com direção correta para cada métrica. Para AUC, maior costuma ser melhor; para erro, menor costuma ser melhor.

Monitorar intervalos/variabilidade e tamanho amostral. Não ordenar retreino por uma mudança pequena sem significância operacional ou sem investigar dados/processo.

## Decidir a resposta

Separar:

- manter e observar;
- investigar dados/pipeline;
- recalibrar threshold/probabilidade;
- reprocessar features;
- treinar challenger;
- promover após validação;
- rollback emergencial.

Exigir validação out-of-time e gates de governança antes de promover um novo modelo. Não alterar alias de produção automaticamente.

## Registrar e alertar

Persistir métricas em tabela governada com `model_name`, versão/alias, janela, referência, segmento, métrica, valor, limite, status e timestamp. Registrar artefatos/links no MLflow sem PII. Configurar alertas com deduplicação, cooldown e runbook.

## O que nunca fazer

- **Fixar limiar universal.** PSI > 0,2 não é regra da natureza: o limite vem do
  histórico da feature, do apetite de risco e da política aprovada.
- **Alertar sobre drift sem olhar volume.** Uma fatia pequena move o índice sem
  significar nada.
- **Confundir drift de entrada com queda de performance.** Os dois existem
  separados, e a resposta a cada um é diferente.
- **Decidir retreino por um único ponto no tempo.**
- **Prometer Lakehouse Monitoring ou inference table sem confirmar** que estão
  habilitados no workspace: no Free, não estão.

## Usar recursos

- Usar [templates/drift_report.md](templates/drift_report.md) para o relatório periódico.
- Usar [templates/retreino_decision.md](templates/retreino_decision.md) para a decisão.

Tratar valores dos templates como placeholders. Substituir por limites aprovados e direção correta da métrica.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| PSI/CSI nativo em escala | `hub_snippets.spark.psi_calculator` |
| PSI, KS, CSI e varredura de features driver-side | `hub_snippets.ml.drift_detection` |
| Comparar duas coortes de uma tabela | `hub_scripts.drift_detector` |
| Acompanhar métricas contra política calibrada | `hub_snippets.ml.performance_monitor` |
| Métricas e curvas de performance | `hub_snippets.ml.metrics_report`, `hub_snippets.ml.curves_plotly` |

`interpretar_psi` só classifica quando recebe os limites do consumidor — não há faixa universal. `PerformanceMonitor` sinaliza degradação e nunca autoriza retreino: a decisão exige investigação, champion-challenger e aprovação.

## Entregar

Fornecer arquitetura, tabelas, métricas, baseline, thresholds justificados, queries/jobs, dashboard, alertas, runbook e matriz de decisão. Listar o que é monitorado automaticamente e o que depende de labels ou revisão humana.
