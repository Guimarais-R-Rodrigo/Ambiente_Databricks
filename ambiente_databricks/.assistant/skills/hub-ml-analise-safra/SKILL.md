---
name: hub-ml-analise-safra
description: Analisa coortes e safras (vintages) de crédito, clientes, contratos ou eventos no Databricks, com cálculo correto de MOB, curvas de maturação, triangulação safra-calendário, comparação entre coortes e alertas de deterioração. Usar quando a solicitação mencionar safra, vintage, coorte, MOB, maturação, inadimplência por originação, ECL/IFRS 9, Resolução CMN 4.966, ou comparação temporal entre grupos de entrada.
---

# Analisar safras

## Executar a rota canônica no perfil mensal binário

Para calcular incidência binária por safra e MOB mensal, prepare a entrada fechada
de [input.schema.json](input.schema.json) com unidade, roster completo, datas,
corte, linhas e semântica do target confirmados. Execute
`scripts/run.py::run(request, run_id=...)`; a CLI equivalente é
`python scripts/run.py --request pedido.json --run-id ID`. O runner executa o
preflight e chama `hub_snippets.ml.vintage_analysis.build_vintage_table`.
Não substitua essa rota por cálculo manual, SQL, notebook ou texto que apenas
afirme ter usado o helper. Pedido para pular scripts não altera essa exigência.

O perfil `MONTHLY_BINARY_PILOT_V1` aceita apenas dados **sintéticos**, mês,
target inteiro 0/1, semântica `CUMULATIVE` ou `EVENT`, denominador fixo
`MOB0_UNIQUE_IDS_FIXED_PER_COHORT` e as demais restrições do preflight.
Não invente campos ausentes nem marque dados reais como `synthetic=true`.
Trimestre, perdas monetárias, múltiplos eventos, dados reais e comparações
entre safras estão fora da rota executável atual.

Só afirme que o cálculo canônico foi executado quando o payload desta chamada
tiver `status="PASS"`, Receipt presente e `vintage_core` em
`trace.resources_completed`, vinculado ao pedido e ao `run_id`. Para afirmar
que os **valores** foram verificados, chame
`scripts/verify.py::verify(payload, expected_request=..., expected_run_id=...,
expected_table=...)` com pedido, ID e tabela-oráculo guardados
independentemente do payload; exija `valid=true`. Um Receipt íntegro sem
oráculo independente comprova a execução vinculada, não a correção dos valores.
O verificador retorna `completion_authorized=false`: seu PASS local não é
homologação Genie, publicação ou promoção da policy.

Se preflight, runner ou verificador bloquear, reporte a causa e mantenha o
cálculo como não concluído. Use `coverage_grid` para distinguir células
imaturas, incompletas e sem observações; não trate ausência como zero. As
etapas gerais abaixo ajudam a interpretar o resultado, sem ampliar o perfil
implementado.

## Responder perguntas conceituais sem inventar execução ou entradas

Em uma pergunta metodológica, explique a regra e identifique contas ilustrativas
como tais. Isso não substitui a rota canônica nem permite alegar execução,
verificação ou Receipt. Antes de oferecer execução, liste os campos faltantes
no contrato: roster/IDs, datas, corte e valores não informados. Diga que o exemplo
é compatível em princípio com o perfil, sem afirmar que o pedido está pronto
ou validado. Nunca complete entradas por suposição.

Separe a semântica declarada: `EVENT` contém ocorrências e o helper deriva o
indicador acumulado por contrato com máximo progressivo; `CUMULATIVE` já contém
o estoque acumulado e deve ser validado como não decrescente, sem acumular de
novo nem usar máximo progressivo para esconder um decréscimo inválido.

Maturidade temporal e cobertura são campos distintos. No perfil mensal,
a idade da célula é calculada pela safra e pela data de corte; ausência de uma
linha não prova que um contrato ainda não atingiu o MOB. O preflight define:

| coverage_status | Condição |
|---|---|
| `IMMATURE` | MOB posterior à idade da safra no corte; maturity=IMMATURE. |
| `NO_OBSERVATIONS` | Célula temporalmente madura, sem observações no MOB. |
| `COMPLETE` | Célula madura, com todos os contratos do roster observados no MOB. |
| `INCOMPLETE` | Célula madura, com parte dos contratos observada no MOB. |

Nos três últimos estados, maturity=MATURE. Sem corte, explique a cobertura
parcial informada, mas não atribua sua causa à imaturidade nem emita classificação
formal de maturity/coverage_grid. Ter dados completos não dispensa validar datas.
Ao recusar um pedido para forçar maturidade ou taxa, mantenha essa regra também
na conclusão: sem corte que comprove idade suficiente, não escreva
`coverage_status=INCOMPLETE` nem "madura temporalmente", mesmo se a ausência de
uma observação estiver confirmada. Diga "cobertura parcial relatada; maturidade
e status formal pendentes da data de corte" e mantenha a taxa final pendente.

Por exemplo, “janeiro/MOB2 só um observado”, com dois contratos na safra,
informa cobertura parcial. Não identifica qual contrato foi observado, o valor
dessa observação nem por que falta o outro. Preserve o denominador dois e não
finalize a taxa com esses dados; não invente ID, target ou causa da ausência.
No perfil de roster fixo, `1/2` descreve somente a cobertura: o número de
observados nunca substitui o denominador da taxa. Em célula `INCOMPLETE`, não
ofereça nem calcule uma "taxa provisória" sobre o subconjunto observado; a taxa
permanece indefinida até a cobertura completa. O helper canônico deixa
`taxa_acumulada` ausente nesse caso.

## Quando esta skill se aplica

- O pedido cita **safra, vintage, coorte, MOB, maturação** ou inadimplência por
  originação — inclusive quando vem disfarçado de "comparar os clientes que
  entraram em janeiro com os de junho".
- Há **grupos de entrada** a comparar ao longo do tempo, e a data de originação
  importa tanto quanto a data do evento.

**Não cobre:** monitoramento de modelo em produção (`hub-ml-monitoramento-modelo`),
nem teste estatístico de diferença entre grupos (`hub-ml-validacao-estatistica`).
A fronteira é o objeto: aqui a coorte é definida pela **entrada**; lá, pela janela
de observação.

## Definir o contrato antes de calcular

1. Confirmar a unidade de análise: contrato, cliente, conta ou evento.
2. Definir a data de origem, a data de observação, a exposição e o evento medido.
3. Registrar o denominador da taxa e se o numerador representa fluxo no mês ou estoque acumulado.
4. Fixar a data de corte e excluir observações posteriores a ela.
5. Definir `MOB` como a diferença inteira de meses entre origem e observação, preservando a convenção escolhida para mês parcial.
6. Separar data de evento, data de conhecimento e data de processamento para evitar uso de informação futura.

Não acumular percentuais com `cumsum`. Somar valores ou eventos apenas quando forem incrementais e depois dividir pelo denominador coerente. Para medidas de estoque, recalcular a razão em cada MOB.

## Executar o fluxo

1. Validar chaves, granularidade, duplicidade e cobertura temporal.
2. Restringir os dados a `data_observacao <= data_corte`.
3. Derivar `safra` e `MOB` de forma explícita e testar casos de fronteira.
4. Construir a matriz `safra × MOB`, mantendo células imaturas como ausentes, nunca como zero.
5. Calcular volume, exposição, quantidade de eventos e taxa com denominadores visíveis.
6. Comparar safras somente em MOBs com maturidade comparável.
7. Separar mudança de mix, efeito calendário e deterioração dentro da mesma safra.
8. Produzir heatmap, curvas por safra e tabela de triangulação com escala e unidade rotuladas.
9. Quantificar incerteza ou volume mínimo; sinalizar coortes pequenas.
10. Entregar achados, limitações, alertas e ações investigativas.

## Guardrails

- Não preencher a diagonal incompleta com zero.
- Não comparar a safra recente em MOB 3 com safra madura em MOB 12.
- Não atribuir causalidade a uma diferença descritiva.
- Não fixar limiares universais de alerta. Derivar os limites do histórico, do apetite de risco e da política aprovada.
- Não tratar análise de safras, PSI, WoE ou qualquer técnica específica como obrigação regulatória sem fonte normativa e validação de Compliance/Jurídico.
- Referir-se corretamente à Resolução **CMN 4.966** quando pertinente. Explicar que a análise pode apoiar mensuração e monitoramento, mas não substitui interpretação normativa.

## Entregar

Incluir no notebook ou relatório:

- contrato analítico e data de corte;
- tabela de qualidade e cobertura;
- definição matemática de cada métrica;
- matriz safra × MOB e curvas comparáveis;
- decomposição de mix quando relevante;
- evidências de deterioração com tamanho da coorte;
- limitações, próximos testes e decisão recomendada.

Usar [templates/relatorio_safra.md](templates/relatorio_safra.md) como estrutura editável do resumo, adaptando métricas e linguagem ao caso real.

## Integrar com o ecossistema

- Acionar `hub-ml-eda-profissional` para diagnóstico de uma única base antes da coorte.
- Acionar `hub-ml-cross-eda-ml` quando originação, performance e eventos vierem de fontes diferentes.
- Acionar `hub-ml-validacao-estatistica` para comparar coortes com inferência e correção de múltiplos testes.
- Acionar `hub-ml-monitoramento-modelo` quando a safra fizer parte de um sistema de alertas recorrente.

## Usar helpers da biblioteca

Importar de `hub_snippets` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO_V2.md#catalogo-helpers](../../MANUAL_TECNICO_V2.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Tabela de safra, curvas de maturação, heatmap e comparação | `hub_snippets.ml.vintage_analysis` |
| Features de calendário para derivar MOB | `hub_snippets.spark.date_features` |
| Tema visual e formatação brasileira | `hub_snippets.visual.theme_plotly`, `hub_snippets.constants.format_br` |

Com um `ResolvedTheme` notebook explicitamente selecionado, use `plot_vintage_curves_resolvido` e `plot_vintage_heatmap_resolvido`. Essas rotas mudam paleta/layout, não MOB, denominador, maturidade, cobertura ou taxa. Sem tema selecionado, mantenha as funções legadas.

`build_vintage_table` calcula incidência acumulada no nível contrato × MOB. Somar taxas por safra produz número diferente e incorreto — erro recorrente em painéis de vintage.

## Verificar atualidade Databricks

Preferir PySpark/Spark SQL para agregações distribuídas e Plotly apenas sobre resultados agregados. Antes de gerar APIs de plataforma, confirmar a documentação oficial aplicável ao cloud e à versão do runtime; não inventar funções de Databricks.
