# Template: Checklist MLflow

> **[N/8]** checks OK | **[X]** tags registradas | **[Y]** artefatos salvos


## Uso
Checklist de registro obrigatório em MLflow para cada run.

## Checklist

- ✅ `mlflow.set_experiment()` com path padronizado
- ✅ `mlflow.set_registry_uri("databricks-uc")`
- ✅ `mlflow.start_run(run_name=...)` com nome descritivo
- ✅ **Params**: todos os hiperparâmetros logados
- ✅ **Metrics**: todas as métricas por split (treino/val/teste)
- ✅ **Tags obrigatórias**:
  - ✅ `type` (baseline/tuning/retrain/comparison/trivial)
  - ✅ `suite` (B1/B2/B3/B4/B5/B6/B7)
  - ✅ `algorithm` (lightgbm/xgboost/catboost/prophet/etc.)
  - ✅ `author`/`owner` (valor fornecido pelo projeto)
  - ✅ `skill_version` (1.0)
  - ✅ `dataset` (catalog.schema.tabela)
  - ✅ `target` (coluna target)
  - ✅ `split_strategy` (temporal/stratified/group/walk_forward)
- ✅ **Model**: `mlflow.sklearn.log_model()` ou equivalente
- ✅ **Signature**: `infer_signature(X, y_pred)`
- ✅ **Input**: `mlflow.log_input()` com dataset de teste
- ✅ **Artifacts**: feature_importance.png, context_card.json
- ✅ **Registro no UC**: `mlflow.register_model(name="catalog.schema.model")`

## Convenção de nomes

| Elemento | Padrão | Exemplo |
|---|---|---|
| Experiment | `/Users/{user}/experiments/{dominio}/{problema}` | `/Users/<usuario>/experiments/crm/churn_prev` |
| Run name | `{tipo}_{algoritmo}_v{N}` | `baseline_lgbm_v1` |
| Model name (UC) | `{catalog_ml}.{dominio}.{problema}_{produto}` | `ml_models.crm.churn_previdencia` |

---

#### 💼 Resumo de conformidade

| Item | Status | Observação |
|---|---|---|
| Run logged | ✅ / ❌ | [run_id ou motivo] |
| Params completos | ✅ / ❌ | [N params] |
| Metrics registradas | ✅ / ❌ | [lista] |
| Tags obrigatórias | ✅ / ❌ | [N/8 presentes] |
| Artefatos | ✅ / ❌ | [N salvos] |
