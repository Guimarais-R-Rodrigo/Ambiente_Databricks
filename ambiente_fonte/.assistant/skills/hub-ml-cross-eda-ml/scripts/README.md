# Cross-EDA: contexto, diagnóstico e join point-in-time

| Rota | O que confere | Efeito/dependência |
|---|---|---|
| Contexto | `input.schema.json` e semântica declarada | sem Spark, cobertura não medida |
| Diagnóstico | cardinalidade/cobertura entre duas fixtures | sessão Spark, ações de cálculo; não produz join de negócio |
| PIT local | disponibilidade temporal e janela | Spark UTC, perfil sintético, finalização/verificação independentes |

A raiz é `.assistant`; componentes SEF devem estar íntegros. O schema de contexto não é schema universal das demais rotas. PASS no diagnóstico não prova prontidão para ML ou conclusão L4.

## Receita sintética e conferência

Os exemplos seguintes são receitas documentais. A execução exige as dependências e o ambiente indicados; não é autorização de efeito remoto. Preserve request/inputs e run_id fora do payload para verificar. Asserts abaixo são conferências didáticas, não substitutos dos gates canônicos.

```python
from pathlib import Path
import importlib.util
import sys

root = Path.cwd().resolve()  # execute da raiz .assistant autorizada
assert (root / "hub_scripts").is_dir(), "Confirme a raiz .assistant"
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
script_dir = root / "skills/hub-ml-cross-eda-ml/scripts"
def load_script(filename):
    name = "readme_cross_eda_ml_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
from hub_scripts.skill_execution.domain_context import digest
datasets = {
    "anchor_snapshot": [{"entity_id": "a", "value": 1}, {"entity_id": "b", "value": 2}, {"entity_id": "c", "value": 3}],
    "attributes_snapshot": [{"entity_id": "a", "flag": 1}, {"entity_id": "b", "flag": 0}]}
context = {"schema_version": "SER05-CONTEXT-1", "profile": "CONTEXT_ONLY_PILOT_V1",
    "synthetic": True, "anchor": "anchor_snapshot", "entity_keys": ["entity_id"],
    "anchor_grain": "ONE_ROW_PER_ENTITY_DECISION", "cardinality": "N:1",
    "decision_at": "2026-01-01T00:00:00Z", "pit": "NOT_APPLICABLE", "temporal": None,
    "not_applicable_reason": "Duas fixtures estáticas sem atributo temporal para decisão real",
    "null_key_policy": "REJECT", "requested_effect": "NONE",
    "sources": [{"id": name, "snapshot_id": "synthetic-"+name, "content_sha256": digest(rows),
                 "grain": "ONE_ROW_PER_ENTITY_DECISION", "columns": list(rows[0])}
                for name, rows in datasets.items()]}
# Conta independente:3âncoras,2matches,1ausente,sem expansão.
expected_diagnostic = {
    "linhas_esquerda": 3, "linhas_direita": 2, "chaves_nulas_esquerda": 0,
    "chaves_nulas_direita": 0, "linhas_descartadas_chave_nula": 0, "linhas_com_match": 2,
    "linhas_sem_match_chave_valida": 1, "cobertura_pct_chaves_validas": 66.67,
    "multiplicidade_max_direita": 1, "multiplicidade_media_direita": 1.0,
    "relacao": "1:1 ou N:1 — join preserva a cardinalidade", "linhas_apos_join_left": 3,
    "linhas_apos_join_inner": 2, "expansao_prevista_left": 1.0, "expansao_prevista_inner": 0.667,
    "exemplos_sem_match": [{"entity_id": "c"}], "exemplos_chave_nula": []}
preflight = load_script("preflight.py")
pre = preflight.preflight(context)
assert preflight.verify_preflight(pre, expected_context=context)["valid"]
# A chamada seguinte exige sessão Spark autorizada; não cria compute.
runner = load_script("run_diagnostic.py")
verifier = load_script("verify_diagnostic.py")
run_id = "readme-cross-tentativa-001"
payload = runner.run(context, datasets, spark, run_id=run_id)
checked = verifier.verify(payload, expected_context=context, expected_datasets=datasets,
    expected_run_id=run_id, expected_diagnostic=expected_diagnostic)
assert checked["valid"], checked
```

## Chamada PIT e inputs próprios

O [contrato PIT](../pit_contract.json) exige fontes reais da fixture: fatos com `decision_id`, `entity_id`, `decision_at`; histórico com `entity_id`, `reference_at`, `available_at`, `feature_value`, hashes e contexto correspondentes. A API `prepare(context, datasets, window_days=...)` confere essas entradas sem executar Spark. No exemplo conceitual de três decisões em 10/01 e janela5: histórico de a disponível10/01 com valor2 entra; observação disponível11/01 não entra; b observado01/01 fica fora da janela; c sem histórico fica nulo. Resultado esperado `[2, None, None]` só vale para esse caso descrito.

```python
# Receita de chamada: context/datasets devem satisfazer o contrato PIT específico.
# NÃO reutilize o contexto NOT_APPLICABLE da receita de diagnóstico acima.
runner = load_script("run_pit.py")
verifier = load_script("verify_pit.py")
payload = runner.run(context, datasets, spark, window_days=window_days, run_id=run_id)
final = verifier.finalize(payload, expected_context=context, expected_datasets=datasets,
    expected_window_days=window_days, expected_run_id=run_id)
checked = verifier.verify_finalized(final, expected_context=context, expected_datasets=datasets,
    expected_window_days=window_days, expected_run_id=run_id)
assert checked["valid"], checked
```

Conserve contexto/datasets/janela/run_id de fonte externa ao payload. Não construa o oráculo copiando seu resultado. `LT`, atraso variável e bitemporalidade bloqueiam. Falha ou `BLOCKED` encerra a tentativa sem fallback manual; finalização ausente não é conclusão.
## Contrato e limites por rota

`preflight.py` preserva o contexto L2, fechado por [input.schema.json](../input.schema.json) e [execution_contract.json](../execution_contract.json). Ele não executa Spark nem comprova cobertura.

`run_diagnostic.py` executa o helper público `diagnosticar_join` em Spark para duas fontes sintéticas estáticas, com PIT `NOT_APPLICABLE`, chave da âncora única e cardinalidade sem expansão. Use `verify_diagnostic.py` com contexto, datasets, run_id e diagnóstico esperado independentes para conferir resultado, Receipt e integridade dos artefatos. O [contrato diagnóstico](../diagnostic_contract.json) e o [manifesto](../release_manifest.json) delimitam essa rota.

O diagnóstico confere cardinalidade e cobertura no perfil sintético. Não produz join de negócio nem demonstra prontidão para ML.

## Join point-in-time local sintético

Join point-in-time local sintético. Exige UTC, disponibilidade conferida, fronteira inclusiva e janela positiva; atraso variável e bitemporalidade não são suportados. O perfil `LOCAL_SYNTHETIC_PIT_V1` limita cada fonte a 500 linhas; finalize e reverifique o resultado.
