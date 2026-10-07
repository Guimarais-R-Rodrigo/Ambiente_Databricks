# Template: Guia de Walk-Forward Validation

## Uso
Planejar validação temporal que reproduza informação disponível em cada origem
de previsão. Para uso futuro, não substituir por split aleatório.

## Escolhas do estudo
- Frequência e `period_unit`: [unidade de calendário]
- Histórico mínimo de treino: [períodos e justificativa]
- Horizonte de teste, passo e gap: [contrato, atraso e disponibilidade]
- Entidades, períodos ausentes e custo por fold: [verificações]
- Métrica primária, baseline, agregação e incerteza: [definições]

Janela expansiva amplia treino a cada fold. Janela deslizante mantém extensão
fixa e exige rota que a suporte; não é opção do helper abaixo. Valores como
12 meses de treino ou 1 de teste são escolhas ilustrativas, não obrigação.

## API canônica
Consultar [`walk_forward_cv`](../../../hub_snippets/ml/walk_forward/README.md).
Assinatura efetiva: `walk_forward_cv(df, date_col, target_col, model_fn,
min_train_periods=12, test_periods=1, step=1, gap=0, *, period_unit="M")`.

- Executa janela expansiva e devolve lista de dicionários com métricas e
  `fold`, `train_end`, `test_start`, `n_train`, `n_test`.
- `model_fn(train_df, test_df)` deve ajustar modelo/preprocessamento somente
  no treino e retornar um dicionário de métricas do teste; confirmar esse
  contrato antes de autorizar execução. O helper chama a função em cada fold.
- Períodos são buckets de calendário observados. Meses/dias ausentes não são
  preenchidos: gap e horizonte contam esses buckets, não garantem duração
  corrida. Conferir datas efetivas, frequência e ausência de períodos.
- Pouco histórico pode produzir lista vazia. Isso é ausência de folds, não
  validação aprovada. Sobreposição dos testes afeta dependência das métricas.

Pseudocódigo conceitual, não implementação alternativa:
```text
confirmar entradas, calendário e contrato de cada fold
configurar callback autorizado que ajusta só no treino e avalia no teste
usar walk_forward_cv com parâmetros confirmados
conferir folds reais e reportar resultados observados e limites
```

## Relato de performance

| Fold | Treino/fim | Teste/início e fim conferidos | N | Métrica/baseline | Estado e evidência |
|---|---|---|---|---|---|
| [id] | [datas] | [datas] | [treino/teste] | [valores ou NÃO CALCULADO] | [NÃO EXECUTADO/parcial/executado] |

Reportar média e dispersão, pior fold e tendência quando existirem resultados.
Desvio entre folds não é automaticamente intervalo de confiança. Sem execução,
entregar plano; resultado parcial preserva falhas e não vira aprovação do modelo.
