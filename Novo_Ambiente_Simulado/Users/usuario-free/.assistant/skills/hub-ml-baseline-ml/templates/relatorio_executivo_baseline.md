# Template: Relatório Executivo Baseline

> **[Métrica]** performance | **[Target]** evento | **[N]** base | **[Decisão]** veredicto


## Uso
Estrutura do relatório executivo ao final do notebook, proporcional ao perfil e ao pedido. Se só planejado, registrar NÃO EXECUTADO e substituir a narrativa de treino por seu plano. Sem critério/evidência para um semáforo, usar NÃO CLASSIFICADO; sem medição, NÃO CALCULADO.

## Formato

```markdown
## Relatório Executivo — Baseline [Contexto]

### Resumo (3 frases)
O modelo de [tipo] para [problema] foi treinado com [N] observações e
[M] features, usando [algoritmo] com split [tipo].
Performance: [métrica principal] = [valor] ([qualidade]) —
[X] pontos acima do baseline trivial.
Recomendação: [prosseguir com `@hub-ml-explainability` | melhorar features | coletar mais dados].

### Semáforo de qualidade
| Aspecto | Status | Justificativa |
|---|---|---|
| Performance vs trivial | [✅/🟡/🔴] | [Δ AUC = +X pontos] |
| Overfitting | [✅/🟡/🔴] | [Gap treino-teste = X%] |
| Estabilidade de features | [✅/🟡/🔴] | [Top-5 estáveis / instáveis] |
| Volume de dados | [✅/🟡/🔴] | [N suficiente / insuficiente] |

### Top-k Features (se importância calculada)
Método: [gain/permutation/SHAP/outro]; conjunto: [fonte]; escala/unidade: [valor].
Normalização: [denominador e regra ou nenhuma]. Percentual só quando calculado
com essa regra; não equivale a percentual de decisões nem efeito causal.
1. **[Feature 1]** ([valor na escala declarada]): [interpretação em 1 frase]
2. **[Feature 2]** ([valor na escala declarada]): [interpretação]
3. **[Feature 3]** ([valor na escala declarada]): [interpretação]
4. **[Feature 4]** ([valor na escala declarada]): [interpretação]
5. **[Feature 5]** ([valor na escala declarada]): [interpretação]

### Próximos passos (priorizados)
1. [Ação 1 — mais impactante]
2. [Ação 2]
3. [Ação 3]

### Limitações declaradas
- [Limitação 1]
- [Limitação 2]
```
