# Template: Relatório de Drift

> **[PSI ou NÃO CALCULADO]** drift score | **[N features ou NÃO INFORMADO]** com alerta | **[Dias ou NÃO INFORMADO]** em produção | **[Status ou NÃO CLASSIFICADO]** saúde


## Status: [🟢 Saudável / 🟡 Atenção / 🔴 Crítico / NÃO CLASSIFICADO — política não fornecida]

Classifique apenas com limiares aprovados e evidência suficiente. Sem eles,
use NÃO CLASSIFICADO; campo ausente fica NÃO INFORMADO. Valores de exemplo não
são execução, nem evidência de alerta ou produção.

### Resumo
- **Modelo**: [nome] (MLflow run_id: [X])
- **Período de referência**: [data treino]
- **Período atual**: [janela analisada]
- **Dias em produção**: [N]

### PSI Global (Score Distribution)
| Métrica | Valor | Limiar | Status |
|---|---|---|---|
| PSI (score) | [X.XXX ou NÃO CALCULADO] | [limiar aprovado ou NÃO INFORMADO] | [🟢/🟡/🔴 ou NÃO CLASSIFICADO] |
| KS (score) | [X.XXX ou NÃO CALCULADO] | [limiar aprovado ou NÃO INFORMADO] | [🟢/🟡/🔴 ou NÃO CLASSIFICADO] |

### Drift por Feature (Top-10 maiores PSI)
| Feature | PSI | KS | Direção | Interpretação |
|---|---|---|---|---|
| [feature] | [X.XXX] | [X.XX] | [shift up/down/spread] | [explicação] |

### Performance em Produção (se labels disponíveis)
| Métrica | Baseline (treino) | Produção atual | Δ | Status |
|---|---|---|---|---|
| AUC | [X] | [X] | [±Xpp] | [🟢/🟡/🔴] |

### Decisão e Recomendação
- **Ação recomendada**: [nenhuma / monitorar / investigar / escalar / decisão pendente]
- **Justificativa**: [razão]
- **Próxima revisão**: [data]
