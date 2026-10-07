# Explicação sintética de regressão linear

Requer NumPy, pandas, scikit-learn e SHAP na chamada do helper. O request JSON não substitui objetos `model`, `X` e `background`. Features numéricas finitas devem conservar ordem, IDs, shape, amostra explícita e conversão exata para cópias float64. O perfil usa regressão linear escalar, uma linha de referência e saída bruta; sem classificação, árvores, KernelSHAP ou plots.

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
script_dir = root / "skills/hub-ml-explainability/scripts"
def load_script(filename):
    name = "readme_explainability_" + filename.replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
import json
import numpy as np
from sklearn.linear_model import LinearRegression
request = json.loads((script_dir.parent / "tests/linear_fixture.json").read_text())
model = LinearRegression().fit(np.array([[0, 0], [1, 0], [0, 1]], dtype=float),
                               np.array([3, 5, 2], dtype=float))
model.hub_model_id = request["model"]["model_id"]
X = np.array(request["X"], dtype=float)
background = np.array(request["background"], dtype=float)
runner = load_script("run.py")
verifier = load_script("verify.py")
run_id = "readme-linear-tentativa-001"
payload = runner.run(request, model=model, X=X, background=background, run_id=run_id)
assert payload["status"] == "PASS", payload
checked = verifier.verify(payload, expected_request=request, expected_model=model,
    expected_X=X, expected_background=background, expected_run_id=run_id)
assert checked["valid"], checked
# Conta independente: f(x)=3+2*x1-x2; background[0,0] => base3.
assert np.allclose(payload["result"]["shap_values"], [[2, -2], [4, -1]])
```

O request e os objetos/model_id são preparados antes da execução; não extraia expectativas do payload. SHAP aditivo explica previsões deste modelo, sem identificação causal. O verificador não autoriza conclusão L4 ou promoção; ausência de SHAP bloqueia a execução, não justifica um resultado fictício.
## Contrato e limites por rota

`preflight.py` fecha o pedido sintético; `run.py` vincula modelo e arrays em cópias `float64` de conversão exata, confere o release e executa o helper canônico; `verify.py` recebe entradas externas e compara SHAP com o oráculo analítico de regressão linear. O contrato SEF está em [execution_contract.json](../execution_contract.json), e a forma estrutural em [input.schema.json](../input.schema.json). Nenhum script persiste o resultado. O Receipt V1 vincula a execução local ao release atual, pedido e run_id; não autentica usuário nem autoriza promoção.

O perfil exige regressão linear escalar, uma linha de background e saída bruta. Não cobre classificação, árvores, KernelSHAP ou plots.
