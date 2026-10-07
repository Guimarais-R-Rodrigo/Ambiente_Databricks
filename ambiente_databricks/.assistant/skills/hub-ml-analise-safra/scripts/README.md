# Safras mensais binárias: execução e verificação

Requer Python com pandas/NumPy/Plotly e os componentes do Hub íntegros. A raiz de trabalho é `.assistant`; `run(request, run_id=...)` retorna resultado/trace/Receipt em memória. A CLI de run imprime JSON; `verify.py` expõe API Python, sem CLI equivalente. O schema e o preflight exigem roster completo em MOB0, corte mensal, origem coerente e modo `EVENT` ou `CUMULATIVE`.

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
script_dir = root / "skills/hub-ml-analise-safra/scripts"
def load_script(filename):
    name = "readme_analise_safra_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
runner = load_script("run.py")
verifier = load_script("verify.py")
origin = "2026-01-01T00:00:00Z"
request = {
    "schema_version": "SER03-REQUEST-1", "profile": "MONTHLY_BINARY_PILOT_V1",
    "synthetic": True, "population_id": "readme-safra-ficticia", "cutoff": origin,
    "max_mob": 0, "semantic_mode": "CUMULATIVE", "periodicity": "MONTH",
    "duplicate_policy": "REJECT", "absence_policy": "MISSING_ROW_NOT_ZERO",
    "denominator": "MOB0_UNIQUE_IDS_FIXED_PER_COHORT",
    "estimand": "BINARY_CUMULATIVE_INCIDENCE", "requested_effect": "NONE",
    "cohort_roster": [{"id": "a", "originated_at": origin}, {"id": "b", "originated_at": origin}],
    "rows": [{"id": uid, "originated_at": origin, "observed_at": origin, "mob": 0, "target": target}
             for uid, target in [("a", 1), ("b", 0)]]}
# Conta independente: 1 evento / 2 pessoas; cobertura 2/2.
expected_table = [{"safra": "2026-01", "mob": 0, "n_contratos_safra": 2,
    "n_contratos_observados": 2, "n_eventos_acumulados": 1,
    "cobertura_observada": 1.0, "taxa_acumulada": 0.5, "taxa": 0.5}]
run_id = "readme-safra-tentativa-001"
payload = runner.run(request, run_id=run_id)
assert payload["status"] == "PASS", payload
checked = verifier.verify(payload, expected_request=request,
    expected_run_id=run_id, expected_table=expected_table)
assert checked["valid"], checked
```

`EVENT` acumula eventos e rejeita lacunas com reentrada; `CUMULATIVE` exige sequência não decrescente. O denominador fica fixo no roster. `IMMATURE`, `NO_OBSERVATIONS` e `INCOMPLETE` não são zeros observados. O oráculo da receita só cobre o caso explícito; não o derive de `payload["result"]`. Não há trimestral, Spark/join nem conclusão L4 nesta rota.
## Contrato e limites por rota

Esta pasta contém `preflight.py`, `run.py` e `verify.py`. As fachadas canônicas SEF são reutilizadas. `current_level` na policy não é alterado por estes arquivos.

As entradas são fechadas pelo código e descritas em [input.schema.json](../input.schema.json). O [contrato](../execution_contract.json) usa schema SEF 0.1, modo audit.

Os campos sintéticos e o perfil explícito são obrigatórios. Nenhum comando aqui grava output de domínio em disco: a função retorna estruturas em memória e a CLI emite JSON ASCII-safe. A coleta de evidência será responsabilidade da campanha autorizada.

Somente o perfil descrito foi implementado. Suporte a trimestre/comparações e join/Spark/Postflight L4 não deve ser inferido. O manifesto e os hashes não autenticam um usuário e não autorizam publicação.

O perfil cobre EVENT e CUMULATIVE, denominador fixo por roster, imaturidade e observações incompletas. O resultado sintético não homologa análises de crédito reais.
