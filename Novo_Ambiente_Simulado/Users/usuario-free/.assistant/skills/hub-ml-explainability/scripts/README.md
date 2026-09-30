# Scripts candidatos de Explainability

`preflight.py` fecha o pedido sintético; `run.py` vincula modelo e arrays em cópias `float64` de conversão exata, confere o release e executa o helper canônico; `verify.py` recebe entradas externas e compara SHAP com o oráculo analítico de regressão linear. O contrato SEF está em [execution_contract.json](../execution_contract.json), e a forma estrutural em [input.schema.json](../input.schema.json). Nenhum script persiste o resultado. O Receipt V1 vincula a execução local ao release atual, pedido e run_id; não autentica usuário nem autoriza promoção.

Exemplo sintético em `tools/tests/test_skill_enforcement_explainability.py` no repositório de autoria. O perfil aceita uma única linha de background, `sklearn.LinearRegression` escalar e saída bruta. Classificação, árvores, KernelSHAP e plots ficam fora desta rota candidata. O teste local não é homologação de Databricks/Genie.
