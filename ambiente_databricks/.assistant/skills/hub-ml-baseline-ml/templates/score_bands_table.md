# Template: Tabela de Score Bands

> **[N]** observações | **[K]** faixas | **[KS]** KS máximo | **[Gini]** Gini


## Uso
Formato para análise técnica de faixas de score; não aprova clientes nem define política de crédito. Declarar população, período, direção do score, maturidade dos labels, fronteiras dos intervalos e critérios aprovados. Sem política, estado NÃO CLASSIFICADO.

## Formato

| Faixa | Score min | Score max | N | % base | Bons | Maus | Taxa default | Volume acum. |
|---|---|---|---|---|---|---|---|---|
| A (melhor) | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| B | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| C | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| D | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |
| E (pior) | [X] | [X] | [N] | [X]% | [N] | [N] | [X]% | [X]% |

## Critérios de qualidade das faixas

- N mínimo/volume por faixa: [critério do estudo, incerteza e responsável]
- Monotonicidade esperada: [direção do score e justificativa; investigar desvios]
- Taxa relativa por faixa: [benchmark e critério aprovado, sem corte universal]
- Estabilidade por período/segmento: [método, evidência e limitação]
- Corte candidato: [simulação técnica]; qualquer decisão sobre clientes exige política e autoridade próprias.

## Interpretação executiva

"Na simulação do corte [X], [Y]% da população avaliada está incluída, com taxa observada [Z]% e incerteza [IC/método]. Essa análise não autoriza aprovação de clientes nem garante taxa futura."

---

#### 📊 Faixas de score e risco

| Faixa | Score range | N | % base | Taxa evento | Risco |
|---|---|---|---|---|---|
| A (baixo risco) | [X]-[X] | [N] | [X]% | [X]% | [critério/ NÃO CLASSIFICADO] |
| B | [X]-[X] | [N] | [X]% | [X]% | [critério/ NÃO CLASSIFICADO] |
| C | [X]-[X] | [N] | [X]% | [X]% | [critério/ NÃO CLASSIFICADO] |
| D | [X]-[X] | [N] | [X]% | [X]% | [critério/ NÃO CLASSIFICADO] |
| E (alto risco) | [X]-[X] | [N] | [X]% | [X]% | [critério/ NÃO CLASSIFICADO] |
