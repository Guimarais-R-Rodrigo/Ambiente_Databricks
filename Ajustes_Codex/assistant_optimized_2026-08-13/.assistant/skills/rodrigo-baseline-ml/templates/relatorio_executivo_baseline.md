# Template: Relatório Executivo Baseline

> **[Métrica]** performance | **[Target]** evento | **[N]** base | **[Decisão]** veredicto


## Uso
Estrutura obrigatória do relatório executivo ao final do notebook.

## Formato

```markdown
## Relatório Executivo — Baseline [Contexto]

### Resumo (3 frases)
O modelo de [tipo] para [problema] foi treinado com [N] observações e
[M] features, usando [algoritmo] com split [tipo].
Performance: [métrica principal] = [valor] ([qualidade]) —
[X] pontos acima do baseline trivial.
Recomendação: [prosseguir com `@rodrigo-explainability` | melhorar features | coletar mais dados].

### Semáforo de qualidade
| Aspecto | Status | Justificativa |
|---|---|---|
| Performance vs trivial | [✅/🟡/🔴] | [Δ AUC = +X pontos] |
| Overfitting | [✅/🟡/🔴] | [Gap treino-teste = X%] |
| Estabilidade de features | [✅/🟡/🔴] | [Top-5 estáveis / instáveis] |
| Volume de dados | [✅/🟡/🔴] | [N suficiente / insuficiente] |

### Top-5 Features (importância)
1. **[Feature 1]** ([X]%): [interpretação em 1 frase]
2. **[Feature 2]** ([X]%): [interpretação]
3. **[Feature 3]** ([X]%): [interpretação]
4. **[Feature 4]** ([X]%): [interpretação]
5. **[Feature 5]** ([X]%): [interpretação]

### Próximos passos (priorizados)
1. [Ação 1 — mais impactante]
2. [Ação 2]
3. [Ação 3]

### Limitações declaradas
- [Limitação 1]
- [Limitação 2]
```
