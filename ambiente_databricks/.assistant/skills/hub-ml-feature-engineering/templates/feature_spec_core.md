# Feature Spec — Core (definição e forma)

> ≤6 colunas. 1 linha por feature proposta. Manter conciso e sem ambiguidade.

## Instruções de preenchimento
- **feature_name**: `snake_case` com prefixo `feat_`. Nome autoexplicativo.
- **definicao**: 1 linha precisa. Verbo no presente ("Quantidade de...", "Razão entre...", "Flag indicando...").
- **tipo**: `int` | `float` | `bool` | `cat_woe` | `cat_ohe` | `cat_freq` | `date_diff` | `ratio`
- **granularidade**: nível da feature (deve ser = unidade de decisão).
- **janela**: período retroativo (`7d`, `30d`, `90d`, `all_time`, `N/A` para estáticas).
- **origem**: coluna(s) e tabela(s) fonte, separadas por vírgula.

## Contrato temporal vinculado

Manter a tabela compacta abaixo e um registro temporal por `feature_name`:
- `event_time`: coluna/semântica do evento ou validade, unidade e fuso;
- `available_at`: instante em que a informação ficou disponível, atraso e fonte de evidência;
- `cutoff`: instante de decisão e limite da janela;
- fronteira: LT (`<`) ou LE (`<=`) conforme contrato/perfil, incluindo limite inferior;
- chave/entidade, regra de join/agregação e tratamento de empate/atualização.

Nomes de campos aqui são da especificação: mapear para o schema real (por
exemplo, `event_at` no perfil de lag). Sem evidência de disponibilidade, marcar
PENDENTE; janela e origem sozinhas não comprovam ausência de leakage.

## Template

| feature_name | definicao | tipo | granularidade | janela | origem |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Exemplo ilustrativo fictício (banking — churn de cartão)

| feature_name | definicao | tipo | granularidade | janela | origem |
|---|---|---|---|---|---|
| feat_qtd_compras_30d | Quantidade de compras no cartão nos últimos 30 dias | int | cliente | 30d | transacoes.tipo=compra |
| feat_ticket_medio_90d | Valor médio por transação nos últimos 90 dias | float | cliente | 90d | transacoes.valor |
| feat_razao_uso_limite | Saldo utilizado / limite total do cartão | ratio | cliente | snapshot | saldos.utilizado, cartoes.limite |
| feat_dias_desde_ultima_compra | Dias entre data_referência e última compra | date_diff | cliente | all_time | transacoes.data (max) |
| feat_flag_renda_ausente | 1 se renda declarada é nula, 0 caso contrário | bool | cliente | N/A | cadastro.renda |
| feat_woe_uf | WoE da UF de residência (fit no treino) | cat_woe | cliente | N/A | cadastro.uf |
