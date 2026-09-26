# Template: Análise SHAP Técnica (E2)

> **[N]** observações | **[M]** features | **[Método]** SHAP type | **[Top-1]** feature mais importante


## Uso
Estrutura do notebook técnico de explicabilidade com todos os artefatos SHAP.

---

## Análise de Explicabilidade — Documentação Técnica

### Metadata
- **Modelo**: [algorithm] ([MLflow run_id])
- **Dataset de explicação**: [N] observações × [M] features
- **Método SHAP**: [TreeSHAP / KernelSHAP / DeepSHAP]
- **Base value (E[f(x)])**: [valor]
- **Tempo de cálculo**: [X] segundos

### 1. SHAP Global — Summary (Beeswarm)

[Inserir plot shap.summary_plot()]

**Observações**:
- Feature mais importante: [nome] (mean |SHAP| = [X])
- Não-linearidades detectadas em: [features]
- Features com efeito bimodal: [features]

### 2. SHAP Global — Bar (Mean |SHAP|)

[Inserir plot shap.summary_plot(plot_type="bar")]

**Comparação com feature importance nativa**:

| Rank | SHAP ranking | Native importance ranking | Concordância |
|---|---|---|---|
| 1 | [feature] | [feature] | [✅/❌] |
| 2 | [feature] | [feature] | [✅/❌] |
| ... | ... | ... | ... |

Spearman correlation (top-20): ρ = [X.XX]

### 3. Dependence Plots (Top-5)

Para cada feature no top-5:

#### Feature: [nome]
[Inserir dependence plot]

- **Relação**: [linear / não-linear / step function]
- **Threshold**: efeito muda em [valor]
- **Interação principal**: com [outra feature]
- **Interpretação**: [descrição do padrão]

### 4. SHAP Local — Exemplos

#### Exemplo 1: Alta probabilidade (p = [X.XX])
[Inserir waterfall plot]
- Principais drivers: [feature] (+[X.XX]), [feature] (+[X.XX])
- Interpretação: [por que essa observação tem score alto]

#### Exemplo 2: Baixa probabilidade (p = [X.XX])
[Inserir waterfall plot]
- Principais drivers: [feature] (-[X.XX]), [feature] (-[X.XX])

#### Exemplo 3: Caso borderline (p ≈ 0.50)
[Inserir waterfall plot]
- Fatores pró e contra quase equilibrados

### 5. Interações SHAP

| Par de features | Interação média | Interpretação |
|---|---|---|
| [feat_A] × [feat_B] | [X.XXX] | [descrição] |
| [feat_A] × [feat_C] | [X.XXX] | [descrição] |
| ... | ... | ... |

### 6. Análise por Cohort

| Cohort | N | Top-1 feature | Mean |SHAP| top-1 | Diferença vs global |
|---|---|---|---|---|
| [segmento 1] | [N] | [feature] | [X.XX] | [+/-X]% |
| [segmento 2] | [N] | [feature] | [X.XX] | [+/-X]% |

### 7. Validação de consistência

| Teste | Resultado | Status |
|---|---|---|
| SHAP vs native importance (Spearman) | ρ = [X.XX] | [✅ >0.7 / ⚠️ 0.5-0.7 / ❌ <0.5] |
| Bootstrap estabilidade (top-5) | [X]/5 estáveis | [✅ 5/5 / ⚠️ 4/5 / ❌ <4/5] |
| Additivity check | max error = [X.XX] | [✅ <0.01 / ❌] |
| Monotonicidade (features monotônicas) | [X]/[Y] consistentes | [✅/❌] |

### 8. Artefatos gerados

| Artefato | Path | Tamanho |
|---|---|---|
| shap_values.parquet | mlflow artifacts | [X] MB |
| shap_summary.html | mlflow artifacts | [X] KB |
| shap_dependence/ | mlflow artifacts | [X] plots |
| shap_waterfall/ | mlflow artifacts | [X] plots |
| context_card_updated.json | mlflow artifacts | [X] KB |
