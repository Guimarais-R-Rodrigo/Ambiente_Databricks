# SER11 / SER12 — hub-ml-monitoramento-modelo

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Calcular métricas sobre referência e janela fixadas e proteger a fronteira entre recomendação e ação. Drift não comprova perda de performance; recomendação não é execução.

Superfícies: monitoring_metrics (L3); retrain_or_promotion (L4/authorization); contexto L2 antecede execução.

## 2. Reuso e inventário de autoria

Matriz cita PerformanceMonitor, selecionar_metricas_do_relatorio, drift_detection e helpers Spark/script a reconfirmar. Métricas existentes não criam alertas, jobs, retreino ou deploy automaticamente.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Modelo/versão e outputs; referência e atual; população/janela/bins; métricas e thresholds explicitamente aprovados; maturidade do label; objetivo; tipo de recomendação; ações possíveis e autoridades por ação.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: comparabilidade, maturidade e decisão de escopo. L4: métricas verificadas, outputs e referências ligados ao Receipt; recomendação rotulada; ação somente sob autorização nominal e retorno verificável; Postflight de conclusão ou bloqueio.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

MO-B01: fechar catálogo de métricas/tarefas/labels e thresholds como dados autorizados, nunca convenção silenciosa. MO-B02: especificar se a superfície de ação apenas faz handoff ou efetivamente executa; não declarar retreino real quando há só handoff. MO-B03: provar ação pessoal sintética somente se mecanismo/destino permitido existirem.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta MO-F01 reutiliza proporções ST-F02 para PSI conhecido, mas com IDs próprios de referência, janela e modelo. Variante tem referência/atual com distribuição alterada e nenhum label maturado: drift pode ser computado, performance não. Variante de autoridade solicita ação diferente da autorizada e deve bloquear antes do efeito. Não fixar 0.1/0.25 como thresholds universais do produto.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| MO01 | Referência/bin/modelo | Alterar referência/bin/modelo sem atualizar binding. | Verifier/resultado inconsistentes bloqueados. |
| MO02 | Comparabilidade | Janela invertida/sem observações ou população distinta. | Preflight bloqueia comparação indevida. |
| MO03 | Label imaturo | Computar e declarar performance definitiva. | Bloquear/limitar performance, mantendo diagnóstico permitido distinto. |
| MO04 | Drift versus perda | Dizer performance degradada comprovada. | Resposta/summary recusam overclaim. |
| MO05 | Threshold ausente | Inventar threshold ou decisão de ação. | Não inferir autoridade/limiar; pedir decisão material. |
| MO06 | Métrica conferível | Mutante modifica fórmula/bin count. | Oráculo independente reprova. |
| MO07 | Recomendação não é execução | Marcar retreino/deploy como realizado. | Postflight bloqueia falsa conclusão. |
| MO08 | Autorização de outra ação | Tentar retreino B ou publicação. | Recusar antes do efeito. |
| MO09 | Replay/parcial | Usar Receipt antigo ou métricas parciais. | Sem conclusão L4 indevida. |
| MO10 | Retorno externo desconhecido | Repetir ação sem readback. | Bloquear retry; estado UNKNOWN e reconciliação read-only. |
| MO11 | Label disponível tarde | Incluir labels ainda indisponíveis no corte avaliado. | Reprovar vazamento temporal de avaliação. |
| MO12 | Handoff versus executor | Alegar capacidade real de action. | Marcar escopo não implementado; não promover por aparência. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Métricas em fixture pequena com oráculos numéricos; labels maduros/imaturo separados. Modelo/referência sintéticos independem de baseline promovida. Execução de ação remota não é comprovada por mocks locais.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar métricas reais e verificar output/Receipt. Quando escopo incluir ação real, usar operação pessoal mínima explicitamente aprovada; se indisponível, registrar BLOCKED_CAPABILITY e não completar essa superfície L4.

Roteiro Genie mínimo: MO-G01, MO-G02, MO-G03, MO-G04, MO-G05, MO-G06, MO-G07, MO-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não criar jobs/alertas/retreino por consequência do diagnóstico. Não transformar PSI em prova suficiente de degradação. Labels ausentes não tornam métrica de performance NA quando o usuário pediu justamente performance.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
