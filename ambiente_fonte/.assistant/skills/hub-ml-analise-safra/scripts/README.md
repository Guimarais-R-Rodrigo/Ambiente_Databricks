# Scripts candidatos — SER03: perfil mensal binário candidato, com cálculo canônico e Receipt V1

Esta pasta contém `preflight.py`, `run.py` e `verify.py`. As fachadas canônicas SEF são reutilizadas. `current_level` na policy não é alterado por estes arquivos.

As entradas são fechadas pelo código e descritas em [input.schema.json](../input.schema.json). O [contrato](../execution_contract.json) usa schema SEF 0.1, modo audit.

Os campos sintéticos e o perfil explícito são obrigatórios. Nenhum comando aqui grava output de domínio em disco: a função retorna estruturas em memória e a CLI emite JSON ASCII-safe. A coleta de evidência será responsabilidade da campanha autorizada.

Somente o perfil descrito foi implementado. Suporte a trimestre/comparações e join/Spark/Postflight L4 não deve ser inferido. O manifesto e os hashes não autenticam um usuário e não autorizam publicação.

Estado desta entrega: testes nativos de domínio executados; integração completa com o checkout, renderer e B0 ainda não validada. Não usar como handoff de certificação.
