# Template: Estratégia de Split

## Definir antes do treino
- Uso futuro, instante de decisão, disponibilidade das features e target: [contrato]
- Coluna temporal/frequência, entidade e unidade: [confirmadas]
- Divisões, janelas e gap: [valores e justificativa do caso]
- Critério de overlap de entidades: [proibir ou permitir histórico em painel, com motivo]
- Estado da validação: [NÃO EXECUTADO/parcial/executado e evidência]

## Seleção
1. Previsão futura: usar divisão temporal e teste fora do tempo.
2. Entidades repetidas: definir se devem ser disjuntas entre partições. Em painéis,
   histórico da mesma entidade pode ser legítimo; disponibilidade temporal continua obrigatória.
3. Aleatório/estratificado: apenas quando tempo e entidade não causarem vazamento.
4. Proporções não são universais; considerar quantidade de períodos, eventos,
   maturidade do target e orçamento, mantendo teste intocado.

## Rota temporal canônica
Consultar [`temporal_split`](../../../hub_snippets/ml/split_temporal/README.md).
Assinatura efetiva: `temporal_split(df, date_col, train_pct=0.70,
val_pct=0.15, gap_periods=1, period_unit="M", *, group_col=None)`.
Os defaults são da API, não recomendação universal. No perfil sintético
`BINARY_TEMPORAL_LOCAL_V1`, prevalecem os valores fixos do perfil e seu runner.

Pseudocódigo de preparação, não célula executável:
```text
confirmar calendário, datas válidas, unidade, cortes e política de entidades
chamar temporal_split com os parâmetros aprovados do contrato
conferir limites reais de treino/validação/teste e exclusões
ajustar preprocessamento somente no treino; avaliar com teste intocado
```

O helper normaliza datas em `period_unit` e divide períodos observados inteiros,
sem cortar por fração de linhas. `gap_periods` pula buckets observados; se faltam
meses/dias, isso não garante um gap exato em tempo corrido. Conferir períodos
ausentes e as fronteiras reais antes de considerar o contrato satisfeito.
`group_col` exclui da validação entidades vistas no treino, e do teste as vistas
antes; pode esvaziar partições e falhar. Quantificar essas exclusões.

## Conferência
- [ ] Datas, fuso, fronteiras e disponibilidade até cada decisão comprovados
- [ ] Nenhum bucket temporal foi dividido por posição de linha
- [ ] Gap observado cumpre o contrato de horizonte/atraso
- [ ] Overlap de entidade tratado conforme uso, sem exclusão silenciosa
- [ ] Binning, imputação, scaling e seleção ajustados apenas no treino
- [ ] N/eventos e período de cada partição registrados; vazio/uma classe tratados
- [ ] Receipt/verificador da rota conferidos quando aplicáveis

Sem dados ou execução, manter checagens pendentes. Este guia não implementa
split alternativo nem autoriza treino ou efeitos persistentes.
