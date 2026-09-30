# Scripts candidatos — Cross-EDA

`preflight.py` preserva o contexto L2, fechado por [input.schema.json](../input.schema.json) e [execution_contract.json](../execution_contract.json). Ele não executa Spark nem comprova cobertura.

`run_diagnostic.py` executa o helper público `diagnosticar_join` em Spark para duas fontes sintéticas estáticas, com PIT `NOT_APPLICABLE`, chave da âncora única e cardinalidade sem expansão. Use `verify_diagnostic.py` com request e run_id esperados para conferir resultado, Receipt e integridade dos artefatos. O [contrato diagnóstico](../diagnostic_contract.json) e o [manifesto](../release_manifest.json) delimitam essa rota.

Os testes locais em `tools/tests/test_ser05_diagnostic.py` exercitam Spark real, cardinalidade, chaves inválidas, hashes e replay. O resultado comprova somente o diagnóstico estático; não entrega join de negócio, PIT temporal, postflight L4 ou autorização de publicação. Receipt e hashes não autenticam usuário nem substituem homologação Genie.

Nenhuma rota altera a policy. Os resultados ficam em memória; persistir evidência local não promove o candidato.

## PIT SER06 local

Use run_pit.py::run para executar pit_join no perfil LOCAL_SYNTHETIC_PIT_V1 e verify_pit.py::finalize + verify_finalized para Postflight e oráculo independente. Requer Spark UTC; fontes sintéticas limitadas a 500 linhas, atraso constante com disponibilidade explicitamente conferida, LE e janela positiva. Semânticas LT, variável e bitemporal bloqueiam. O PASS local não comprova readiness de negócio ou homologação Databricks.
