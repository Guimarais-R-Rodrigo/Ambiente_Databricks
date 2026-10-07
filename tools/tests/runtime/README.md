# Núcleo realocado e contratos de preservação

Apesar do nome `runtime`, esta pasta pertence aos testes do Git. Não é instalada
no workspace. O núcleo foi retirado do payload e preservado aqui com proveniência.

| Arquivo | Responsabilidade |
|---|---|
| [test_core.py](test_core.py) | Casos do núcleo; executar pela receita de `run_core_tests.py` |
| [package_contract.json](package_contract.json) | Recursos protegidos e fingerprint AST dos casos/assertions |
| [relocation_manifest.json](relocation_manifest.json) | Caminhos, bytes e hashes no commit original da realocação |
| [visual_successor.json](visual_successor.json) | Sucessão restrita da metadata do diagrama da raiz, com predecessor Git e deltas autorizados |

Owners executáveis: [run_core_tests.py](../../run_core_tests.py) e
[package_boundary.py](../../package_boundary.py). Da raiz:

```sh
python -B tools/run_core_tests.py
python -B tools/package_boundary.py
```

Os nomes antigos em `source`/proveniência identificam o blob original; não devem
acompanhar renomeações da fonte atual. O consumidor faz o mapeamento autorizado.
O ledger visual não libera outras figuras, campos, recursos ou mudanças de hashes.
Sem histórico Git completo a prova do predecessor fica bloqueada. Para evolução
do fingerprint, consulte [migração entre runtimes](../../../docs/manutencao/fingerprint-core.md).
[Voltar às suítes](../README.md).
