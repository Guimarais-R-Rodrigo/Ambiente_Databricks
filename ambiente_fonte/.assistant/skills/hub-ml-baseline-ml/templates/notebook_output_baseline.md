# Template: Estrutura do Notebook Baseline

## Uso
Estrutura sugerida para notebooks gerados com `@hub-ml-baseline-ml`.
Selecionar seções conforme o perfil realmente suportado. Um plano fica NÃO
EXECUTADO; resultado ausente fica NÃO CALCULADO; artefato fora do perfil fica
NÃO APLICÁVEL com motivo. Não gerar dados, treino, tracking ou plots só para
preencher o layout. Receipt e verifier da rota continuam obrigatórios quando
aplicáveis; este molde não os substitui.

## Estrutura

```markdown
# Baseline — [Contexto]

> **Suite**: [B1/B2/B3/B4/B5/B6/B7]
> **Modo**: [tabular/scorecard/temporal/dl/cluster/ranking/survival/anomaly]
> **Dataset**: [catalog.schema.tabela]
> **Target**: [coluna] (ou "nenhum" para B4/B7)
> **Split**: [temporal/estratificado/group/walk-forward]
> **Data**: [YYYY-MM-DD]
> **Autor**: [usuário]

---

## 1. Setup e Configuração
[Imports e seed confirmados; experimento/logging somente quando aplicáveis e autorizados]

## 2. Carga e Validação
[Load dataset, validar schema, importar Context Card se disponível]

## 3. Preparação
[Split, encoding, nulos, scaling se necessário]
[Declarar: N_treino, N_val, N_teste, N_features]

## 4. Baseline Trivial
[Baseline e métricas conforme rota; MLflow somente se autorizado, caso contrário NÃO APLICÁVEL]

## 5. Modelo Principal
[Treino pelo perfil disponível; tuning/early stopping somente se suportados e solicitados]

## 6. Avaliação Comparativa

### 6.1 Tabela de métricas (dual-layer)

#### Para executivos:
| Indicador | Resultado | Interpretação |
|---|---|---|
| [métrica] | [valor] | [frase em linguagem natural] |

#### Para técnicos:
| Métrica | Treino | Validação | Teste | IC 95% | vs Trivial |
|---|---|---|---|---|---|
| [métrica] | [val] | [val] | [val] | [lower-upper] | +Δ |

### 6.2 Curvas diagnósticas
[Somente curvas produzidas e pertinentes; indicar NÃO APLICÁVEL ou NÃO EXECUTADO]

## 7. Feature Importance
[Método de importância suportado, conjunto, escala, top-k e normalização declarados]
[SHAP/permutation/gain são condicionais ao modelo e à rota; sem resultado, NÃO CALCULADO]
[Importância relativa não é percentual de decisões nem efeito causal]

## 8. Diagnóstico de Overfitting
[Gap treino-teste + semáforo + recomendação]

## 9. Relatório Executivo Final
[3 frases + semáforo + próximos passos]

## 10. Context Card (handoff)
[Proveniência e limitações verificadas; handoff para `@hub-ml-explainability` se solicitado e aplicável]
```
