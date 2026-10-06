# Template: Métricas de Séries Temporais

## Contrato do estudo
- Série/entidade, target e unidade: [informados]
- Frequência, horizonte, sazonalidade e períodos ausentes: [validados ou pendentes]
- Backtesting: [folds, janelas, gap e cortes]
- Baseline naïve/sazonal: [regra, período sazonal e amostra de escala]
- Métrica primária e critério aprovado: [responsável, perda/custo e incerteza]
- Execução: [NÃO EXECUTADO/parcial/executado; fonte de evidência]

## Interpretação das métricas

| Métrica | Significado | Limite a declarar |
|---|---|---|
| MAE/RMSE | Erro absoluto médio/raiz do erro quadrático médio na unidade do target | RMSE dá mais peso a erros grandes; não equivale a MAE |
| MAPE | Média dos erros absolutos divididos por valores reais absolutos | Zero é indefinido; valores próximos de zero dominam; declarar população excluída |
| sMAPE | Erro percentual com denominador dependente de real e previsão | Declarar fórmula e regra para ambos zero; não herda faixas de MAPE |
| MASE | MAE de avaliação dividido pelo erro naïve in-sample definido para escala | Declarar período sazonal, treino e denominador; escala zero invalida a razão |
| Cobertura do intervalo de previsão | Fração dos valores observados dentro do intervalo | Ler com nível nominal, largura, horizonte, N e variabilidade |

MASE ≥ 1 indica erro pelo menos tão grande quanto o denominador usado na escala;
não prova que um naïve avaliado no mesmo teste venceria nem ordena descarte.
Comparar os dois fora da amostra. Nenhuma faixa de MAPE, MASE ou cobertura
aprova implantação. Governança, validação e decisão humana são separadas.

## Comparação fora da amostra

| Modelo | Fold/horizonte | MAE | MAPE (se válido) | MASE | RMSE | Cobertura/largura | Critério e estado |
|---|---|---|---|---|---|---|---|
| Naïve sazonal | [recorte] | [valor] | [valor ou N/A] | [calculado, não fixar 1] | [valor] | [valor ou N/A] | [baseline] |
| [Candidato] | [mesmo recorte] | [valor] | [valor ou N/A] | [valor] | [valor] | [valor ou N/A] | [NÃO AVALIADO/critério] |

Resultados não observados ficam NÃO CALCULADO. Reportar distribuição por fold,
pior período, drift e limitações; médias podem ocultar falhas por horizonte.

## Texto executivo
"Em [janelas], o modelo teve [métrica e unidade], contra [baseline comparável],
com [incerteza]. A cobertura observada dos intervalos foi [valor] para nível
nominal [nível], com largura [valor]. Isso descreve este backtest; não garante
cobertura futura nem constitui autorização de uso em produção."
