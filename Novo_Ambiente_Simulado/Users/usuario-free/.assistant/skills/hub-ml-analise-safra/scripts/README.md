# Scripts candidatos — SER03: perfil mensal binário candidato, com cálculo canônico e Receipt V1

Esta pasta contém `preflight.py`, `run.py` e `verify.py`. As fachadas canônicas SEF são reutilizadas. `current_level` na policy não é alterado por estes arquivos.

As entradas são fechadas pelo código e descritas em [input.schema.json](../input.schema.json). O [contrato](../execution_contract.json) usa schema SEF 0.1, modo audit.

Os campos sintéticos e o perfil explícito são obrigatórios. Nenhum comando aqui grava output de domínio em disco: a função retorna estruturas em memória e a CLI emite JSON ASCII-safe. A coleta de evidência será responsabilidade da campanha autorizada.

Somente o perfil descrito foi implementado. Suporte a trimestre/comparações e join/Spark/Postflight L4 não deve ser inferido. O manifesto e os hashes não autenticam um usuário e não autorizam publicação.

Estado local: runner integrado, testes de domínio e regressões executados, com renderer conferido. O perfil mensal cobre `semantic_mode=EVENT` e `CUMULATIVE`, denominador fixo pelo roster, imaturidade e observações incompletas. A homologação no Free/Genie é uma etapa separada; não inferir certificação ou promoção por este README.
