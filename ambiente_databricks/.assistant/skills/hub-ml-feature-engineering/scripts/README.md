# Features: lag local, composição e materialização PIT

| Rota | Efeito | Requer |
|---|---|---|
| Lag `FIXED_LAG_L1_V1` | cálculo em memória, sem fit/persistência | Python, pandas; inputs sintéticos UTC |
| Vista `COMPOSED_PIT_FEATURE_VIEW_V1` | Spark em memória após verificar PIT upstream | Spark UTC e inputs/IDs externos |
| Materialização PIT | cria/MERGE/lê/remove tabela Delta sintética | autorização exata de operação/destino, principal/namespace e cleanup |

Não há um schema JSON genérico para as três rotas. Escolha o contrato específico e confirme dependências antes de executar.

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
script_dir = root / "skills/hub-ml-feature-engineering/scripts"
def load_script(filename):
    name = "readme_feature_engineering_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def _request():
    def row(rid, entity, day, value):
        return {"id": rid, "entity_id": entity,
                "event_at": f"2026-01-{day:02d}T00:00:00+00:00",
                "available_at": f"2026-01-{day+1:02d}T00:00:00+00:00", "value": value}
    return {"schema_version": "SER07-REQUEST-1", "profile": "FIXED_LAG_L1_V1",
            "synthetic": True, "population_id": "synthetic-panel-01",
            "decision_at": "2026-01-10T00:00:00+00:00", "window_days": 4,
            "requested_effect": "NONE", "temporal": {
                "reference_column": "event_at", "availability_column": "available_at",
                "lag_kind": "CONSTANT", "lag_days": 1, "boundary": "LE",
                "timezone": "UTC", "tie_break": "REJECT", "bitemporal": False},
            "rows": [row("a7", "A", 7, 1), row("a8", "A", 8, 2),
                     row("a10", "A", 10, 5), row("a11", "A", 11, 7),
                     row("b7", "B", 7, 10), row("b8", "B", 8, 20)]}
request = _request()
expected_features = [{"id": "a8", "entity_id": "A", "event_at": "2026-01-08", "lag_1": 1.0},
                     {"id": "b8", "entity_id": "B", "event_at": "2026-01-08", "lag_1": 10.0}]
runner = load_script("run.py")
verifier = load_script("verify.py")
run_id = "readme-lag-tentativa-001"
payload = runner.run(request, run_id=run_id)
assert payload["status"] == "PASS", payload
checked = verifier.verify(payload, expected_request=request,
    expected_run_id=run_id, expected_features=expected_features)
assert checked["valid"], checked
```

`expected_features` é a conta externa de observações anteriores por entidade. Para a vista, `compose(context, datasets, spark, window_days=..., upstream_run_id=..., view_run_id=...)` exige IDs distintos; `verify` recebe `expected_context`, `expected_datasets`, `expected_window_days`, `expected_upstream_run_id`, `expected_view_run_id`. Materialização segue `effect_request` → autorização vinculada ao digest → `execute` → readback/replay → cleanup. `UNKNOWN` exige inspeção; nunca retry automático.
## Contrato e limites por rota

O perfil `FIXED_LAG_L1_V1` executa
`hub_snippets.ml.lgbm_temporal.create_temporal_features`, sem fit ou persistência.
O preflight fechado fica em `run.py::preflight`; `run.py::run` emite Receipt
e `verify.py::verify` recebe request, run_id e features esperadas independentes.

Campos exigidos: `schema_version=SER07-REQUEST-1`, profile, synthetic=true,
population_id, decision_at UTC, window_days inteiro entre 1 e 365,
requested_effect=NONE, temporal e rows. O contexto temporal exige
reference_column=event_at, availability_column=available_at, lag_kind=CONSTANT,
lag_days=1, boundary=LE, timezone=UTC, tie_break=REJECT, bitemporal=false.
Cada linha contém id, entity_id, event_at, available_at e value numérico finito
entre -1e9 e 1e9. Eventos são à meia-noite UTC, com disponibilidade um dia depois;
o grão entidade/instante e os IDs são únicos. No máximo 1.000 linhas.

A janela de eventos é inclusiva: [decision_at - window_days, decision_at].
Só entram linhas disponíveis até decision_at. O lag é a observação anterior
**dentro dessa janela elegível e da mesma entidade**, não o dia anterior.
O helper ordena as observações; warm-up sem histórico é removido.
`eligible_ids` mantém o denominador antes do warm-up; `features=[]` significa
que nenhuma linha tinha histórico suficiente, não sucesso analítico de negócio.

A receita completa acima usa dados fictícios independentes e já inclui todos os campos. Não marque dados reais como sintéticos.
Na raiz da skill, a entrada CLI aceita:

```text
python scripts/run.py --request request.json --run-id execution-id
```

Nunca marque dados reais como sintéticos. Receipts são evidência de integridade
e vínculos, não autenticação de origem ou homologação Genie.


## Vista de features derivada do PIT Cross-EDA

scripts/run_pit_features.py::compose chama run_pit, finalize e verify_finalized
do Cross-EDA para o perfil COMPOSED_PIT_FEATURE_VIEW_V1. Só projeta
feature_value e available_at por decision_id após a prova local PASS.
scripts/run_pit_features.py::verify recebe inputs/IDs esperados externos,
revalida o Postflight upstream e compara toda a projeção. O payload inclui
prova upstream literal e linhagem de hashes/cutoff/janela/Receipt/Postflight.
Sem Receipt FE novo, fit, materialização ou prontidão de negócio. O contrato
pit_view_contract.json limita a composição ao perfil sintético.
## Materialização PIT sintética autorizada

`run_pit_materialization.py::effect_request` recebe a view produzida por
`run_pit_features.py::compose` e os inputs externos originais. O digest desse
request compõe a autorização explícita para `execute`. A operação requer
Spark UTC, principal e namespace `workspace.default` correspondentes,
alvo pessoal novo `skills_delivery_<32 hex>` e cleanup `DROP_OWNED`.

O efeito usa o motor Delta compartilhado com Pipeline Builder, com perfil
fechado de cinco colunas. Preserva IDs texto, timestamps UTC de micros e
`feature_value` BIGINT nullable. Propriedades Delta ligam a tabela a hashes
da view, fontes, contexto, cutoff, Receipt e Postflight. O registro de efeito
separa versões observadas após primeiro MERGE e replay, hash do readback,
ID da tabela e resultado da remoção. Não executa fit nem materialização de
negócio; um `UNKNOWN` nunca autoriza retry automático.
O limite de valor aceito pelo PIT upstream continua [-1.000.000, 1.000.000];
`BIGINT` descreve o armazenamento, não amplia o domínio permitido.
