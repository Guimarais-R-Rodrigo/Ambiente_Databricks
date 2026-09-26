# Template: Justificativa DL vs LightGBM

## Uso
> **[AUC LGB]** LightGBM | **[AUC DL]** Deep Learning | **[Δ]** Diferença | **[Veredicto]** Decisão


Template para documentar a decisão de usar (ou não) Deep Learning
em vez de LightGBM para problemas tabulares.

## Critérios de decisão

### Quando DL PODE se justificar (pré-requisitos)
- [ ] LightGBM já foi treinado e estabelece um baseline reproduzível
- [ ] Há features categóricas com cardinalidade > 100
- [ ] O volume e a diversidade dos dados suportam a capacidade do modelo proposto
- [ ] GPU está disponível (ou CPU é aceitável para o timeline)
- [ ] O ganho potencial na métrica primária justifica a complexidade

### Quando DL NÃO se justifica (usar LightGBM)
- [ ] A amostra/variabilidade é insuficiente para validar a capacidade adicional
- [ ] O baseline já atende aos critérios e o ganho incremental não compensa o custo
- [ ] Interpretabilidade é mais importante que performance marginal
- [ ] Time-to-production é crítico (DL demora mais para deploy)
- [ ] Não há GPU disponível e o dataset é grande

## Tabela comparativa obrigatória

```markdown
## Comparação: LightGBM vs [DL Model]

| Aspecto | LightGBM | [TabNet/MLP] | Δ | Decisão |
|---|---|---|---|---|
| **AUC teste** | [X] | [X] | [±Xpp] | [DL justificado?] |
| **KS teste** | [X] | [X] | [±X] | — |
| **Tempo de treino** | [X] min | [X] min | [×N] | [aceitável?] |
| **Tempo de inferência** | [X] ms/batch | [X] ms/batch | [×N] | [aceitável?] |
| **Interpretabilidade** | Alta (SHAP nativo) | [Média/Baixa] | — | — |
| **Complexidade de deploy** | Baixa | [Média/Alta] | — | — |
| **Manutenção** | Fácil | [Média/Difícil] | — | — |
```

## Decisão final (template)

```markdown
### Decisão: [USAR DL / MANTER LIGHTGBM]

**Justificativa**: [DL superou em Xpp / DL não superou / DL empatou]

**Se USAR DL**:
- Registrar AMBOS os modelos no MLflow
- LightGBM como fallback (se DL falhar em produção)
- Monitorar performance de ambos em paralelo (primeiros 3 meses)

**Se MANTER LIGHTGBM**:
- Registrar apenas LightGBM como modelo principal
- Documentar: "DL testado, não justificado (Δ AUC = Xpp)"
- Próximos passos: [mais features / mais dados / aceitar performance atual]
```

## Regra de ouro

> DL em dados tabulares só se justifica se:
> 1. Superar LightGBM em ≥ 1pp na métrica principal
> 2. O custo de complexidade for aceitável (treino, deploy, manutenção)
> 3. O ganho traduzir em impacto de negócio mensurável

---

#### 💼 Interpretação executiva

> "O modelo [DL/LightGBM] apresenta [melhoria/piora] de [X]pp em AUC
> comparado ao baseline. Considerando o trade-off entre performance e
> complexidade operacional, recomendamos [manter LGB / adotar DL]."

#### ➡️ Decisão

| Critério | LightGBM | Deep Learning | Vencedor |
|---|---|---|---|
| AUC | [X] | [X] | [🟢/🔴] |
| Tempo de treino | [X]min | [X]min | [🟢/🔴] |
| Interpretabilidade | ✅ Alta | ⚠️ Baixa | [🟢/🔴] |
| Complexidade operacional | ✅ Baixa | 🔴 Alta | [🟢/🔴] |
