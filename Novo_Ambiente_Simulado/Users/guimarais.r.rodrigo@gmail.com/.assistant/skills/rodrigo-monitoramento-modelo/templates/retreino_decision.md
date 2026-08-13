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

## Decisão: [RETREINAR / MANTER / INVESTIGAR]

### Se RETREINAR:
| Aspecto | Decisão |
|---|---|
| Estratégia | [Full retrain / Incremental / Sliding window] |
| Dados de treino | [período] |
| Abordagem | [Champion-Challenger] |
| Timeline | [dias] |
| Validação | [métricas a atingir] |

### Se MANTER:
- Próxima revisão em [N] dias
- Monitorar especialmente: [features / métricas]

### Se INVESTIGAR:
- Causa raiz provável: [mudança de negócio / bug / seasonalidade]
- Ações: [lista]

---

#### 📌 Semáforo de decisão

| Indicador | Valor | Limiar | Status |
|---|---|---|---|
| PSI do score | [X] | [limiar aprovado] | 🟢 / 🟡 / 🔴 |
| Queda de AUC | [X]pp | [limiar aprovado] | 🟢 / 🟡 / 🔴 |
| Janelas em alerta | [N] | [limiar aprovado] | 🟢 / 🟡 / 🔴 |
