# Template: Métricas de Regressão

## Contexto e critério
- Target e unidade: [valor]
- População, período, split e tamanho avaliado: [fonte]
- Baseline e perda relevante ao uso: [definição]
- Critério aprovado e responsável: [valor ou NÃO INFORMADO]
- Estado: [NÃO EXECUTADO/executado/parcial]; métricas ausentes: NÃO CALCULADO.

## Métricas e interpretação

| Métrica | Resultado | Baseline | Incerteza/segmentos | Leitura |
|---|---|---|---|---|
| RMSE | [valor] | [valor] | [método] | Raiz do erro quadrático médio, na unidade do target; dá mais peso a erros grandes |
| MAE | [valor] | [valor] | [método] | Erro absoluto médio, na unidade do target |
| MAPE | [valor ou N/A] | [valor] | [regra para zero e valores pequenos] | Média dos erros absolutos relativos; não usar quando o denominador não faz sentido |
| R² | [valor ou indefinido] | [valor] | [população e definição] | Comparação quadrática com a média da amostra avaliada; não é percentual de acertos |

Não há faixas universais de qualidade para MAPE ou R². Comparar perda,
benchmark, unidade, população e custo do erro. RMSE/mean(y) só pode ser usado
como normalização declarada quando a média é não nula e tem significado;
não é obrigatório nem, em geral, o coeficiente de variação do erro.

## Investigações e limites
- MAE muito menor que RMSE sugere concentração de erros grandes: inspecionar
  resíduos e segmentos antes de atribuir causa a outliers.
- R² negativo significa desempenho quadrático pior que prever a média da
  amostra avaliada. Investigar generalização, split, distribuição e pipeline;
  não comprova bug isoladamente. Target constante requer tratamento explícito.
- MAPE com zero/próximo de zero pode ser indefinido/instável. MAE, WAPE ou sMAPE
  exigem sua própria adequação e proteção de denominador, sem troca automática.
- Normalização não muda a perda observada nem aprova o modelo.

## Texto executivo
"No período [X], o erro absoluto médio foi [MAE e unidade] e o RMSE foi [valor].
Frente ao baseline [Y], observamos [diferença e incerteza]. O critério [Z]
[foi/não foi/não pôde ser] avaliado. Recomendação técnica: [ação e limites]."
