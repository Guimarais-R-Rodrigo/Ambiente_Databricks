# `monitoramento_modelo` — monitorar modelo sem transformar variação em incidente

<!-- readme-objeto: 1.0.0 -->

Briefing para monitoramento técnico, de dados, drift e performance. O prompt organiza o pedido, mas não executa a tarefa sozinho.

**Preparo persistente:** o notebook sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual`. Ler e preencher o briefing não exige executar essas células.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para monitoramento técnico, de dados, drift e performance. |
| Para que serve? | Ligar baseline, janela, atraso do rótulo, direção das métricas e owners. |
| Use quando... | Modelo, referência e janelas podem ser identificados. |
| Evite quando... | A conclusão exige performance com rótulos imaturos ou um limite sem calibração. |
| Precisa de... | Modelo, caminho de inferência, baseline, janela, label delay, métricas, segmentos e owners. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](monitoramento_modelo.md) e leia o [notebook de exemplo](exemplo_monitoramento_modelo.py).

## 1. O que é?

Briefing para monitoramento técnico, de dados, drift e performance. O arquivo `monitoramento_modelo.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Drift, qualidade de dados, falha operacional e queda de performance são fenômenos diferentes. Misturá-los cria alarmes sem ação.

## 3. Quando faz sentido usar?

Use quando modelo, referência e janelas podem ser identificados. Ligar baseline, janela, atraso do rótulo, direção das métricas e owners.

## 4. Quando não usar?

Não conclua performance preditiva com rótulos imaturos. Ainda é possível desenhar monitoramento e observar saúde operacional, cobertura/latência de rótulos e drift, com limites explícitos. Limite copiado sem calibração permanece proposta, não regra de incidente.

## 5. Como funciona, intuitivamente?

Separe saúde operacional, dados, drift, performance e negócio; alinhe predição e rótulo antes do alerta.

## 6. Exemplo de situação

Comparar duas janelas sintéticas com prevalência e nulidade diferentes, enquanto o rótulo do período atual só amadurece após 30 dias. Pedir desenho e diagnóstico de drift; performance atual fica pendente. As tabelas não comprovam predição ou serving de um modelo real.

## 7. O que você precisa antes de usar?

Tenha modelo, caminho de inferência, baseline, janela, label delay, métricas, segmentos e owners. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Solicita mapa de monitoramento; catálogo de métricas com fórmula, fonte, janela, direção, limite e owner; diagnóstico com evidência e severidade; código opcional; e runbook de investigação, rollback e eventual retreino. Incidente, variação esperada e causa hipotética são separados.

## 9. Como usar este recurso no Hub?

Preencha [monitoramento_modelo.md](monitoramento_modelo.md). Siga a [skill correspondente](../../skills/hub-ml-monitoramento-modelo/SKILL.md) e consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json): `current_level` descreve a capacidade vigente; `target_level` não autoriza promoção. Os perfis `DRIFT_NUMERIC_LOCAL_V1` e `BINARY_MATURE_PERFORMANCE_V1` tratam escopos diferentes; performance exige labels maduras e sua finalização/verificação próprias. O perfil implementado tem escopo e evidência próprios; não equivale a homologação de todo pedido deste briefing.

O [exemplo](exemplo_monitoramento_modelo.py) sobrescreve `workspace.default.hub_exemplo_monitor_ref` e `workspace.default.hub_exemplo_monitor_atual`. Não prova inferências, serving, métricas ou tracking de um modelo real. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Baseline, label delay, direção/unidade, janela, mínimo N, limite e owner.

## 11. Limitações, riscos e armadilhas

Performance sobre rótulo imaturo, `abs(delta)` e retreino por um único ponto. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para checks de dados, use [Qualidade](../data_quality/README.md); para avaliação inicial de modelo, [Baseline](../baseline_orchestration/README.md).

## 13. Como saber se o resultado faz sentido?

Teste melhora, piora, baixo volume, nulos e ausência de rótulo; confira denominadores. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](monitoramento_modelo.md), o [notebook](exemplo_monitoramento_modelo.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](monitoramento_modelo.md) define os campos e a entrega; o [notebook](exemplo_monitoramento_modelo.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
