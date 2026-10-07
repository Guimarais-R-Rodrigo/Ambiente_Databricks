# Template: Análise SHAP Técnica

Camada editorial técnica; não indica workspace corporativo nem nível de
homologação.

> **[N]** observações | **[M]** features | **[Método]** SHAP type | **[Top-1]** feature mais importante


## Uso
Estrutura de explicabilidade adaptada ao método e ao perfil executados.
Plots, interações, métricas de comparação e MLflow são condicionais, não uma
lista obrigatória de artefatos. Marcar NÃO EXECUTADO, NÃO CALCULADO ou NÃO
SUPORTADO/NÃO APLICÁVEL com motivo, sem preencher resultados para completar layout.
O perfil `LINEAR_REGRESSION_SYNTHETIC_V1` verifica contribuições numéricas brutas;
não produz por isso plots, interações ou logging. Respeitar Receipt e verificador
com entradas independentes; valores verificados não autorizam conclusão/promoção.

---

## Análise de Explicabilidade — Documentação Técnica

### Metadata
- **Modelo**: [algorithm, identidade/versão observada; MLflow run_id somente se existente]
- **Dataset de explicação**: [N] observações × [M] features
- **Método SHAP**: [linear/TreeSHAP/KernelSHAP/DeepSHAP/outro suportado; versão]
- **Escala/classe**: [saída bruta/log-odds/probabilidade/valor previsto, classe e unidade]
- **Background e amostra**: [origem, seleção, seed, N, ordem das features]
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

Probabilidade somente se essa for a saída explicada. Para regressão, reportar
predição e contribuições na unidade do target; não chamar valor bruto de p.

#### Exemplo 1: Predição/score alto na escala declarada ([valor e unidade])
[Inserir waterfall plot]
- Principais drivers: [feature] (+[X.XX]), [feature] (+[X.XX])
- Interpretação: [por que essa observação tem score alto]

#### Exemplo 2: Predição/score baixo na escala declarada ([valor e unidade])
[Inserir waterfall plot]
- Principais drivers: [feature] (-[X.XX]), [feature] (-[X.XX])

#### Exemplo 3: Caso próximo do threshold definido no estudo (se aplicável)
[Inserir waterfall plot]
- Fatores pró e contra quase equilibrados

### 5. Interações SHAP

| Par de features | Interação média | Interpretação |
|---|---|---|
| [feat_A] × [feat_B] | [X.XXX] | [descrição] |
| [feat_A] × [feat_C] | [X.XXX] | [descrição] |
| ... | ... | ... |

### 6. Análise por Cohort

| Cohort | N | Top-1 feature | mean(abs(SHAP)) top-1 | Diferença vs global |
|---|---|---|---|---|
| [segmento 1] | [N] | [feature] | [X.XX] | [+/-X]% |
| [segmento 2] | [N] | [feature] | [X.XX] | [+/-X]% |

### 7. Validação de consistência

| Teste | Resultado | Status |
|---|---|---|
| SHAP vs native importance (Spearman) | ρ = [X.XX] | [critério justificado; métodos medem importâncias distintas] |
| Bootstrap estabilidade (top-5) | [X]/5 estáveis | [variabilidade, seleção do top-k e critério do estudo] |
| Additivity check | max error = [X.XX] | [tolerância justificada pela escala/método e fonte do contrato] |
| Monotonicidade (features monotônicas) | [X]/[Y] consistentes | [✅/❌] |

A aditividade vale na escala retornada pelo explicador. Transformar log-odds em
probabilidade não conserva contribuições aditivas nessa nova escala. Critérios
fechados do verificador do perfil prevalecem; não recalibrá-los neste relatório.

### 8. Artefatos gerados (apenas os observados; paths seguros)

Logging só quando aplicável e autorizado. A tabela é um menu de artefatos
possíveis, não prova de persistência. Se a rota for local, usar NÃO APLICÁVEL.

| Artefato | Path | Tamanho |
|---|---|---|
| shap_values.parquet | mlflow artifacts | [X] MB |
| shap_summary.html | mlflow artifacts | [X] KB |
| shap_dependence/ | mlflow artifacts | [X] plots |
| shap_waterfall/ | mlflow artifacts | [X] plots |
| context_card_updated.json | mlflow artifacts | [X] KB |
