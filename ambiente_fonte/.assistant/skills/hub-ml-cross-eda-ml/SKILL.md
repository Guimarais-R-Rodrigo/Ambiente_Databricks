---
name: hub-ml-cross-eda-ml
description: Consolida múltiplos EDAs e fontes para avaliar viabilidade de joins, resolução de entidade, alinhamento temporal, cobertura, complementaridade de sinal e prontidão para ML no Databricks. Usar quando pedirem cross-EDA, cruzamento de bases, integração de fontes, readiness para modelagem, análise de cobertura entre tabelas, definição de âncora ou riscos antes de feature engineering.
---

# Avaliar múltiplas fontes para ML

## Resolver o contexto antes de diagnosticar o join

Para o perfil sintético `CONTEXT_ONLY_PILOT_V1`, forme o objeto fechado de
[input.schema.json](input.schema.json) com as duas fontes, âncora, chaves,
grão, cardinalidade, instante de decisão e triestado PIT confirmados. Execute
`scripts/preflight.py::preflight(context)` (CLI:
`python scripts/preflight.py --context contexto.json`). Para afirmar que o
contexto L2 foi resolvido, exija `status="PASS"` e valide o payload com
`scripts/preflight.py::verify_preflight(payload, expected_context=...)`,
usando o contexto original guardado independentemente do payload.

Esse PASS confirma apenas metadados declarados: `source_identity_status`
permanece `DECLARED_NOT_READ`, `join_executed=false`,
`coverage_measured=false` e `ml_readiness="NOT_EVALUATED"`. Não transforme
cardinalidade declarada em prova observada nem converta PIT `UNKNOWN` em
`NOT_APPLICABLE`. Sem disponibilidade temporal confirmada, mantenha a
decisão de readiness pendente. O diagnóstico real por
`hub_snippets.spark.join_diagnostics.diagnosticar_join` requer DataFrames
Spark e execução própria; a rota L2 não o chama nem emite Receipt para ele.

Para o diagnóstico estático sintético com PIT `NOT_APPLICABLE`, execute
`scripts/run_diagnostic.py::run(context, datasets, spark, run_id=...)`.
Passe linhas das duas fontes com hashes que correspondam ao contexto; o runner
faz o preflight L2, chama `diagnosticar_join` em Spark e emite Receipt V1.
Só afirme cobertura medida se houver `status="PASS"`, Receipt e
`join_diagnostics` em `trace.resources_completed`. Para verificar os valores,
chame `scripts/verify_diagnostic.py::verify` com contexto, datasets, `run_id`
e oráculo de diagnóstico independentes do payload; exija `valid=true`.
O resultado mantém `join_executed=false`, `pit_executed=false` e readiness
pendente. PIT aplicável exige a rota SER06 descrita abaixo.


Para o perfil sintético PIT LOCAL_SYNTHETIC_PIT_V1, com atraso constante,
fuso UTC, fronteira inclusiva LE, empate rejeitado e sem bitemporalidade,
execute scripts/run_pit.py::run(context, datasets, spark, window_days=...,
run_id=...). As linhas das fontes devem ter as colunas e os hashes declarados.
A disponibilidade observada deve ser igual a referência + atraso declarado;
a rota bloqueia divergência, LT, latência variável, referências empatadas,
chaves nulas e alterações de dados durante a execução. O Spark deve usar UTC.
A janela limita a idade da referência; decisão exatamente no instante de
disponibilidade é elegível.

Após PASS e Receipt, execute scripts/verify_pit.py::finalize com os inputs,
janela e run_id originais; então verify_finalized com os mesmos valores
mantidos independentemente do payload. Só trate o perfil local como concluído
quando valid=true e scope_completion_authorized=true; o verificador
recalcula a seleção temporal e a cobertura sem chamar o helper. Isto não
declara readiness ML, homologação Genie ou publicação. Sem Postflight válido,
o perfil permanece pendente.

Se o preflight ou verificador bloquear, reporte o campo ou conflito e mantenha
o contexto não resolvido. As etapas abaixo orientam a investigação seguinte;
não substituem evidência de execução. Cobertura estática exige o diagnóstico
verificado acima; join de negócio e PIT continuam não executados.


## Quando esta skill se aplica

- Há **mais de uma fonte** e a pergunta é se elas se cruzam: viabilidade de join,
  resolução de entidade, alinhamento temporal, cobertura, sinal complementar.
- Pedem readiness para modelagem, definição de âncora, ou riscos **antes** de
  começar feature engineering.

**Não cobre:** a exploração de **uma** fonte (`hub-ml-eda-profissional`) nem a
construção das features depois de decidido o cruzamento
(`hub-ml-feature-engineering`).

## Receber o contexto

Confirmar a partir de informação fornecida ou de evidência identificada. Quando faltar um campo, registrar a pendência; propostas para esclarecimento não são entradas confirmadas:

Em perguntas conceituais, rotular cenários hipotéticos sem preencher a fonte real. Não inferir chave, grão, corte ou disponibilidade para obter PASS, nem transformar ausência de match em causa conhecida. A hipótese orienta o plano; cobertura, elegibilidade PIT e readiness continuam dependentes das evidências e gates acima.

Campos do contexto:

- pergunta e target;
- unidade de predição;
- instante de decisão e horizonte do target;
- fonte âncora;
- chaves de entidade e temporais;
- snapshots/filtros de cada EDA;
- restrições de uso e sensibilidade.

Sem instante de decisão, não aprovar prontidão para modelagem.

## Executar o fluxo

1. **Inventariar EDAs:** registrar fonte, granularidade, período, chave, qualidade e limitações.
2. **Resolver entidade:** medir unicidade, overlap e conflitos; documentar tabela de correspondência quando necessária.
3. **Alinhar tempo:** definir join point-in-time e garantir que cada atributo existia antes da decisão.
4. **Simular joins:** medir cobertura à esquerda, não match, multiplicidade e fator de expansão.
5. **Diagnosticar ausência:** distinguir ausência estrutural, indisponibilidade temporal e falha operacional; não declarar MCAR/MAR/MNAR sem evidência suficiente.
6. **Medir complementaridade:** comparar sinal incremental com validação adequada, não apenas correlação marginal.
7. **Avaliar qualidade combinada:** verificar duplicidade, conflito semântico, unidade e domínios após o join.
8. **Decidir readiness:** registrar bloqueadores, mitigação, owner e critério de aceite.

## Proteger contra leakage

Para cada feature candidata, registrar:

- `event_time` ou período de validade;
- momento de disponibilidade real;
- regra de lookback;
- atraso de publicação;
- fonte e transformação;
- relação com a data de decisão.

Usar join point-in-time quando houver histórico. Não usar o registro “mais recente” se ele puder ter sido conhecido somente depois do target.

## Interpretar métricas corretamente

- **Coverage:** calcular no denominador da fonte âncora e por janela/segmento.
- **Overlap/Jaccard:** usar para conjuntos, sem concluir qualidade do join.
- **Cramér's V/mutual information:** tratar como associação, não causalidade.
- **PSI:** calcular com bins/categorias fixados na referência, incluindo missing; definir limiares pela política e pelo histórico.
- **Sinal incremental:** preferir comparação out-of-time com e sem a fonte e mesma população.

## Produzir scorecard sem falsa precisão

Usar dimensões explicáveis — entidade, temporalidade, cobertura, qualidade, leakage, sinal incremental e governança — e registrar a evidência de cada nota. Não converter uma média em `GO` se houver veto de leakage, chave indefinida ou população sem representatividade.

Decidir:

- **GO:** contrato completo e riscos controlados;
- **CONDICIONAL:** lacunas mitigáveis com owners e critérios;
- **NO-GO:** ausência de chave/tempo, leakage material ou cobertura incompatível.

## O que nunca fazer

- **Cruzar sem checar cardinalidade.** Um join 1:N silencioso multiplica linhas e
  todas as métricas derivadas junto.
- **Ignorar o instante da informação.** Se a feature foi publicada depois da data
  da decisão, o cruzamento vaza — é o que o join point-in-time existe para evitar.
- **Concluir complementaridade a partir de correlação alta** entre fontes: isso é
  redundância, não sinal novo.
- **Declarar readiness sem cobertura medida.** "As bases se cruzam" precisa de um
  percentual e de um exemplo de chave órfã.

## Usar recursos

- [templates/inventario_edas.md](templates/inventario_edas.md)
- [templates/join_feasibility.md](templates/join_feasibility.md)
- [templates/coverage_matrix.md](templates/coverage_matrix.md)
- [templates/readiness_scorecard.md](templates/readiness_scorecard.md)
- [templates/notebook_output_cross_eda.md](templates/notebook_output_cross_eda.md)
- [templates/relatorio_executivo_cross_eda.md](templates/relatorio_executivo_cross_eda.md)

Adaptar thresholds e imports à implementação atual; templates são customizados e não recursos nativos do Genie Code.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Cobertura, multiplicidade e expansão antes do join | `hub_snippets.spark.join_diagnostics` |
| Alinhamento temporal por junção point-in-time | `hub_snippets.spark.pit_join` |
| Perfil comparável entre fontes | `hub_scripts.quick_profile` |
| Schema documentado para confronto de contratos | `hub_scripts.schema_to_yaml` |
| Nulos e cobertura por coluna | `hub_snippets.spark.null_summary` |
| Amostra reprodutível e exibição limitada | `hub_snippets.spark.smart_sample`, `hub_snippets.spark.safe_display` |
| Divergência de distribuição entre fontes ou janelas | `hub_snippets.spark.psi_calculator` |

PSI aqui mede comparabilidade entre fontes, não drift de modelo; interpretar apenas com limites calibrados para o caso.

## Entregar o handoff

Fornecer mapa de fontes, contrato de join point-in-time, matriz de cobertura, riscos, decisão e backlog para `hub-ml-feature-engineering`. Incluir consultas de validação reproduzíveis e data dos snapshots.
