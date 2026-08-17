# Template: Tabela de Score Bands

> **[N]** observações | **[K]** faixas | **[KS]** KS máximo | **[Gini]** Gini


## Uso
Formato padronizado para tabela de faixas de score.

## Formato

| Faixa | Score min | Score max | N | % base | Bons | Maus | Taxa default | Aprov. acum. |
|---|---|---|---|---|---|---|---|---|
| A (melhor) | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| B | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| C | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| D | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| E (pior) | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |

## Critérios de qualidade das faixas

- Mínimo 5% da base por faixa (representatividade)
- Taxa de default monotonicamente crescente de A→E
- Faixa A deve ter taxa ≤ 50% da taxa média
- Faixa E deve ter taxa ≥ 200% da taxa média
- Ponto de corte: definir entre quais faixas aprovamos/reprovamos

## Interpretação executiva

"Ao aprovar até a faixa [X], incluímos [Y]% dos clientes e esperamos
uma taxa de inadimplência de [Z]% — comparada com [W]% sem modelo."

---

#### 📊 Faixas de score e risco

| Faixa | Score range | N | % base | Taxa evento | Risco |
|---|---|---|---|---|---|
| A (baixo risco) | [X]-[X] | [N] | [X]% | [X]% | 🟢 |
| B | [X]-[X] | [N] | [X]% | [X]% | 🟢 |
| C | [X]-[X] | [N] | [X]% | [X]% | 🟡 |
| D | [X]-[X] | [N] | [X]% | [X]% | 🟡 |
| E (alto risco) | [X]-[X] | [N] | [X]% | [X]% | 🔴 |
