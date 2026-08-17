# Template: Relatório de Drift

> **[PSI]** drift score | **[N features]** com alerta | **[Dias]** em produção | **[Status]** saúde


## Status: [🟢 Saudável / 🟡 Atenção / 🔴 Crítico]

### Resumo
- **Modelo**: [nome] (MLflow run_id: [X])
- **Período de referência**: [data treino]
- **Período atual**: [janela analisada]
- **Dias em produção**: [N]

### PSI Global (Score Distribution)
| Métrica | Valor | Limiar | Status |
|---|---|---|---|
| PSI (score) | [X.XXX] | [limiar aprovado] | [🟢/🟡/🔴] |
| KS (score) | [X.XXX] | [limiar aprovado] | [🟢/🟡/🔴] |

### Drift por Feature (Top-10 maiores PSI)
| Feature | PSI | KS | Direção | Interpretação |
|---|---|---|---|---|
| [feature] | [X.XXX] | [X.XX] | [shift up/down/spread] | [explicação] |

### Performance em Produção (se labels disponíveis)
| Métrica | Baseline (treino) | Produção atual | Δ | Status |
|---|---|---|---|---|
| AUC | [X] | [X] | [±Xpp] | [🟢/🟡/🔴] |

### Decisão e Recomendação
- **Ação recomendada**: [nenhuma / monitorar / retreinar / escalar]
- **Justificativa**: [razão]
- **Próxima revisão**: [data]
