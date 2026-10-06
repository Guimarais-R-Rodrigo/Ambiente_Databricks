---
name: hub-ml-monitoramento-modelo
description: Desenha e implementa monitoramento de modelos no Databricks para qualidade de dados, drift, performance, calibração, fairness, latência, custo e decisão de retreino, integrando MLflow, Models in Unity Catalog, Lakehouse Monitoring e tabelas de inferência quando aplicável. Usar quando pedirem monitoramento, PSI/CSI/KS, drift, degradação, alerta, dashboard, endpoint, inference table, retreino, champion/challenger ou operação de modelo.
---

# Monitorar modelos em produção

## Drift numérico sintético

Para pedido explícito do perfil `DRIFT_NUMERIC_LOCAL_V1`, use
`input.schema.json` e `scripts/preflight.py::preflight` antes de
`scripts/run.py::run`. Verifique Receipt, janelas, bins e métricas com
`scripts/verify.py::verify` usando request e run_id mantidos pelo invocador.
Esta rota calcula PSI e KS de score numérico sintético em duas janelas
disjuntas, com quantis de referência, bucket de nulos e smoothing explícito.
O perfil é candidato não promovido e não avalia labels, performance ou
degradação; não cria alertas, jobs, retreino ou ação remota. Pedidos fora
dele seguem o fluxo de planejamento abaixo e não recebem Receipt executável
por aproximação. Um pedido genérico para examinar scores/bins não declara esse
perfil. Se oferecer um exemplo executável, identifique separadamente a proposta
do perfil e cada metadado criado para demonstração (IDs, datas/janelas, modelo,
população, n_bins e eps); não apresente esses valores como fornecidos pelo usuário
nem como monitoramento real. Sem contexto suficiente, mantenha o resultado
limitado a análise conceitual ou peça os campos necessários.

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

- Congelar bins/categorias na referência. Definir também o tratamento das caudas
  fora da faixa observada na referência (por exemplo, limites externos infinitos);
  não usar valores da janela atual para construir nem ampliar esses limites.
  Se usar bins manuais em uma ilustração, declarar os limites e sua origem;
  não chamá-los de quantis da referência quando não forem quantis.
- Incluir missing e categoria nova explicitamente.
- Usar smoothing documentado para evitar log de zero.
- Reportar volume, período, referência e incerteza.
- Avaliar drift por segmento e não apenas média global.
- Tratar PSI/CSI/KS como sinais diagnósticos, não prova de queda de performance.

Não substituir PSI por deslocamento absoluto da média. Não aplicar limites `0,1/0,25` como padrão universal; calibrar pela variabilidade histórica, risco e política.
Sem limiar aprovado ou calibração fornecida, reporte o valor e o movimento por bin,
mas não classifique severidade operacional, alerta ou saúde por adjetivos como
"severo" ou "crítico". Identifique a sensibilidade do valor a n, bins e eps.
Com amostra pequena, mostre n, bins e eps. Um bin vazio em ambas as janelas
recebe eps em ambas e contribui zero ao PSI. O smoothing pode dominar o PSI
quando há massa em um lado e zero no outro; identifique qual bin e sua
contribuição, sem atribuir o efeito aos bins vazios nas duas janelas.
O valor numérico não é decisão operacional.
O p-valor do KS não mede potência, equivalência ou ausência de drift. Com n
pequeno, registre a limitação para inferência. Não diga que o teste "não tem
poder" ou que sua potência é "mínima"/"baixa", nem explique p=1 pela potência,
sem alternativa, alfa e cálculo ou simulação de potência específicos. Diga
somente que estes dados não rejeitaram a hipótese nula no teste aplicado.
Não conclua performance sem labels.

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

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica, inclusive
em exemplos exploratórios executados em notebook. `calculate_psi` retorna só o
total. Para explicar bins/contribuições, uma decomposição didática separada pode
reproduzir exatamente a política e os parâmetros do helper (quantis da
referência, caudas, bucket de nulos e eps), identificar essa derivação e
conferir sua soma contra o total oficial com tolerância numérica explícita.
Se usar política de bins ou fórmula diferente, identificar a ilustração como
resultado distinto, sem atribuí-la ao helper nem comparar os totais como se
tivessem a mesma definição. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| PSI/CSI nativo em escala | `hub_snippets.spark.psi_calculator` |
| PSI, KS, CSI e varredura de features driver-side | `hub_snippets.ml.drift_detection` |
| Comparar duas coortes de uma tabela | `hub_scripts.drift_detector` |
| Acompanhar métricas contra política calibrada | `hub_snippets.ml.performance_monitor` |
| Métricas e curvas de performance | `hub_snippets.ml.metrics_report`, `hub_snippets.ml.curves_plotly` |

Se a entrega usar um `ResolvedTheme` notebook validado, `PerformanceMonitor.plot_timeline_resolvido` e as curvas `*_resolvido` podem ajustar a aparência. O tema não recalibra threshold, baseline, direção da métrica, status nem decisão de retreino; política e evidência continuam independentes da camada visual.

`interpretar_psi` só classifica quando recebe os limites do consumidor — não há faixa universal. `PerformanceMonitor` sinaliza degradação e nunca autoriza retreino: a decisão exige investigação, champion-challenger e aprovação.

## Entregar

Fornecer arquitetura, tabelas, métricas, baseline, thresholds justificados, queries/jobs, dashboard, alertas, runbook e matriz de decisão. Listar o que é monitorado automaticamente e o que depende de labels ou revisão humana.

## Performance binária sintética com labels maduras

Para o perfil sintético `BINARY_MATURE_PERFORMANCE_V1`, usar
`scripts/preflight_performance.py::preflight`, depois
`scripts/run_performance.py::run`, e conferir o payload com
`scripts/verify_performance.py::verify` usando pedido e run_id independentes.
Antes de montar o request, confirme que as linhas são realmente sintéticas.
`synthetic: true` declara origem, não formato: copiar, amostrar, agregar ou
anonimizar previsões/labels reais não os torna sintéticos. Origem não
informada exige confirmação; dados reais de modelo implantado ficam fora
desta rota piloto. Nesse caso, planeje a análise e explicite a lacuna, sem
prometer executar SER12 com a tabela real.
Para encerrar somente o diagnóstico local, executar `finalize` e depois
`verify_finalized`; runner e Receipt sozinhos ainda deixam o escopo pendente.
O pedido deve declarar as duas janelas, `evaluation_at`, labels disponíveis até
essa data e limiares de AUC `warning`/`critical` de direção `higher` e delta
`absolute`. O runner chama `calculate_binary_metrics` e
`PerformanceMonitor` com política fornecida pelo solicitante. O Receipt
atesta a execução sintética e o verificador recalcula AUC, KS e Brier.
A verificação compara métricas publicadas na precisão do helper (AUC/Brier:
quatro casas; KS: uma casa) com oráculos independentes sem arredondamento,
admitindo no máximo meia unidade da casa publicada nas fronteiras. A decisão
de limiar usa a AUC reportada depois dessa validação.
Status crítico indica investigação, sem retreino, alerta ou promoção automática.
