# Template: Decisão de Retreino

> **[Decisão]** RETREINAR/MANTER | **[PSI]** score drift | **[ΔAUC]** queda | **[Urgência]** nível


## Contexto
- **Modelo**: [nome]
- **Em produção desde**: [data]
- **Motivo da avaliação**: [drift detectado / queda performance / rotina]

## Evidências

| Evidência | Valor | Limiar | Veredicto |
|---|---|---|---|
| PSI do score | [X] | [limiar aprovado] | [excede/OK] |
| Queda de AUC | [X]pp | [limiar aprovado] | [excede/OK] |
| Features com drift severo | [N]/[M] | [limiar aprovado] | [excede/OK] |
| Janelas consecutivas com alerta | [N] | [limiar aprovado] | [excede/OK] |

## Recomendação técnica: [RETREINAR / MANTER / INVESTIGAR / PENDENTE]

Esta tabela não dispara retreino. Drift não prova degradação; performance exige
labels maduras e comparação coerente. Sem dados ou limiares aprovados, usar
NÃO CALCULADO/NÃO CLASSIFICADO e registrar a evidência faltante.

- **Tomador de decisão**: [responsável identificado ou NÃO INFORMADO]
- **Aprovação**: [PENDENTE/aprovada/recusada; fonte, data e escopo]
- **Execução autorizada**: [ação, dados, ambiente, destino e limites; ou NÃO AUTORIZADA]
- **Execução observada**: [NÃO EXECUTADO/parcial/executado, com evidência]
- **Promoção/alias/deploy**: decisão separada, nunca consequência automática deste parecer.

### Plano proposto se a autoridade decidir retreinar:
| Aspecto | Decisão |
|---|---|
| Estratégia | [Full retrain / Incremental / Sliding window] |
| Dados de treino | [período] |
| Abordagem | [Champion-Challenger] |
| Timeline | [dias] |
| Validação | [métricas a atingir] |

### Plano proposto se a autoridade decidir manter:
- Próxima revisão em [N] dias
- Monitorar especialmente: [features / métricas]

### Plano proposto para investigar:
- Causa raiz provável: [mudança de negócio / bug / seasonalidade]
- Ações: [lista]

---

#### 📌 Semáforo de decisão

| Indicador | Valor | Limiar | Status |
|---|---|---|---|
| PSI do score | [X] | [limiar aprovado] | 🟢 / 🟡 / 🔴 |
| Queda de AUC | [X]pp | [limiar aprovado] | 🟢 / 🟡 / 🔴 |
| Janelas em alerta | [N] | [limiar aprovado] | 🟢 / 🟡 / 🔴 |
