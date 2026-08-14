---
name: rodrigo-analise-safra
description: Analisa coortes e safras (vintages) de crédito, clientes, contratos ou eventos no Databricks, com cálculo correto de MOB, curvas de maturação, triangulação safra-calendário, comparação entre coortes e alertas de deterioração. Usar quando a solicitação mencionar safra, vintage, coorte, MOB, maturação, inadimplência por originação, ECL/IFRS 9, Resolução CMN 4.966, ou comparação temporal entre grupos de entrada.
---

# Analisar safras

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

- Acionar `rodrigo-eda-profissional` para diagnóstico de uma única base antes da coorte.
- Acionar `rodrigo-cross-eda-ml` quando originação, performance e eventos vierem de fontes diferentes.
- Acionar `rodrigo-validacao-estatistica` para comparar coortes com inferência e correção de múltiplos testes.
- Acionar `rodrigo-monitoramento-modelo` quando a safra fizer parte de um sistema de alertas recorrente.

## Usar helpers da biblioteca

Importar de `x_snippets` em vez de reimplementar a lógica. Catálogo completo: [x_docs/catalogo_helpers.md](../../x_docs/catalogo_helpers.md).

| Demanda | Módulo |
|---|---|
| Tabela de safra, curvas de maturação, heatmap e comparação | `x_snippets.ml.vintage_analysis` |
| Features de calendário para derivar MOB | `x_snippets.spark.date_features` |
| Tema visual e formatação brasileira | `x_snippets.visual.theme_plotly`, `x_snippets.constants.format_br` |

`build_vintage_table` calcula incidência acumulada no nível contrato × MOB. Somar taxas por safra produz número diferente e incorreto — erro recorrente em painéis de vintage.

## Verificar atualidade Databricks

Preferir PySpark/Spark SQL para agregações distribuídas e Plotly apenas sobre resultados agregados. Antes de gerar APIs de plataforma, confirmar a documentação oficial aplicável ao cloud e à versão do runtime; não inventar funções de Databricks.
