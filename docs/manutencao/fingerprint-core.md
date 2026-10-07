# Fingerprint dos testes core entre versões Python

Owner executável: [package_boundary.py](../../tools/package_boundary.py).
Regressões: [test_readme_package_boundary.py](../../tools/tests/test_readme_package_boundary.py).
Contrato: [package_contract.json](../../tools/tests/runtime/package_contract.json).

## Defeito e correção de 06/10/2026

O kit do merge `f17355424134b019f69c19ec3e02ba842f23d0f4` reprovou no
Python 3.11, embora os 45 testes core executados tivessem passado. A guarda
comparava `ast.dump` ao hash congelado no Python 3.12. Nessa versão,
[`FunctionDef`, `AsyncFunctionDef` e `ClassDef` ganharam `type_params`](https://docs.python.org/3.12/library/ast.html#ast.FunctionDef),
inclusive quando a lista está vazia. A serialização textual bruta mudou.

`core-tests-ast-v2` usa uma representação JSON tipada e determinística:

- Classes e métodos `test_` conservam seus nomes; nomes duplicados são erro.
- O corpo completo de cada método síncrono ou assíncrono é representado,
  incluindo asserções, negativos, decorators, argumentos e anotações.
- Todo nó tem tipo e pares campo/valor ordenados; listas preservam a ordem.
- Constantes carregam tipo e `repr`, distinguindo `True`, `1`, `1.0`, bytes,
  números complexos, `None` e `Ellipsis`.
- Somente posições do AST, comentários e `type_params=[]` nos três tipos de
  definição acima são neutros. Parâmetros genéricos não vazios e outros campos
  permanecem na assinatura. Metadados inesperados e campos ausentes reprovam.
- O JSON usa `sort_keys=True`, `ensure_ascii=True`, separadores `(',', ':')`
  e UTF-8; SHA-256 identifica esse conteúdo. O contador é conferido à parte.

A guarda cobre a identidade/conteúdo dos métodos core, não uma equivalência
semântica geral de todo o módulo. Bases, decorators e parâmetros genéricos da
classe externa não pertencem ao subtree dos métodos. Código de setup, imports
e recursos runtime continuam cobertos pelos outros testes e contratos de distribuição. Não há
fallback por versão Python nem aceitação automática de um hash novo. Schema,
campos extras, proveniência e JSON com chaves duplicadas são fail-closed.

## Migração reproduzível, sem reescrever o passado

O campo histórico `core_assertion_ast_sha256` foi mantido intacto. O novo campo
`core_assertion_fingerprint` documenta schema, digest e proveniência:

- Commit de origem: `126a2e125cca2251527f187a58696243414c6859`.
- Fonte original: `ambiente_fonte/.assistant/hub_snippets/tests/test_core.py`.
- SHA-256 dos bytes originais: `b48baa202b292fb2070b8bbb207d0bbb0a1e27ec2e73b3398b9d67b094ce8491`.
- AST textual legado, Python 3.12: `62652bb85dbe70936d1bee99098ed87a556de7245ed83c7c2acbb85e87e663b8`.
- Fingerprint v2, original e realocado: `f76821ddb5fc879a9d95a2f2e614527079bcd58f69438a830c756f1dc09fb4c3`.

O teste de migração lê o blob original com `git show` no commit fixado, verifica
seus bytes contra o manifesto congelado, recalcula v2 e compara ao realocado.
No Python 3.12, também reconstrói a assinatura legada. Precisa do histórico Git
contendo esse commit; checkout raso sem o objeto é pré-requisito ausente, não PASS.
A CI usa `fetch-depth: 0`. Não atualize hashes para fazer um mutante passar.

```sh
python -B tools/tests/test_readme_package_boundary.py -v
python -B tools/package_boundary.py
python -B tools/tests/runtime/test_core.py -v
```

## Execução integral, separada do fingerprint

Desde a correção de 07/10/2026, a etapa `biblioteca` do agregado usa
[`run_core_tests.py`](../../tools/run_core_tests.py). Ele primeiro confere o
schema, a proveniência, o digest e a contagem do contrato existente, sem mudar
seus hashes. Em seguida exige cada ID protegido iniciado, concluído e aprovado
exatamente uma vez. Skip, inclusive em setup de módulo/classe, duplicação,
filtragem por `load_tests`, ausência de casos, falha e erro impedem PASS.

```sh
python -B tools/run_core_tests.py -v
```

O JSON de stdout registra IDs esperados, iniciados, concluídos, aprovados,
faltantes, extras, duplicados e skips; o log de execução fica em stderr. A CLI
`test_core.py` permanece disponível para diagnóstico, mas seu exit 0 sozinho
pode incluir skips. O novo runner é o gate de execução integral. Isso não amplia
a semântica coberta pelo fingerprint para todo o módulo, nem comprova runtime
Databricks. O mapeamento B0 desse comando continua coletando os métodos da suíte
real e recusa argumentos que desviem a coleta.

## Prova cross-version e limites

O [workflow do kit](../../.github/workflows/kit-transicao-trabalho.yml) executa,
para PRs que afetam a receita, a mesma sequência completa nos interpretadores
reais 3.11 e 3.12: validação, render/check, agregado, V09, contratos Spark local,
geração e conferência do ZIP. As duas pernas devem passar. Artefatos de PR têm
nome de teste e não são a release integrada de `main`. Main/manual preservam
`preparar` e Python 3.11. Permissões continuam somente `contents: read`.

Mutantes testam remoção/troca de asserção, renomeação/remoção de teste,
constantes tipadas, genéricos, metadados inesperados e schema desconhecido.
O caso de sintaxe PEP 695 é explicitamente não aplicável a 3.11; sua execução
real pertence à perna 3.12. Um teste sintético de AST sozinho não substitui a
matriz real nem os estágios downstream da receita.

## B0: contrato e execução separados

O fingerprint de métodos em
[`skill_enforcement/parallel/coverage.py`](../../tools/skill_enforcement/parallel/coverage.py)
é outro contrato: permanece inalterado, inclusive hashes históricos. Usa
`ast.dump` bruto com hashes originados no AST do CPython 3.12; não herda a
normalização `core-tests-ast-v2`. Seu runtime de referência para esta reprodução
é CPython 3.12. Nem `ci_local.py::ETAPAS` nem `PROFILE_STEPS['se08']` executam
`test_ser_parallel_b0` ou o inventário B0. O verde da matriz do kit em 3.11/3.12
não comprova compatibilidade cross-version desse fingerprint.

Execute as rotas próprias no ambiente de referência já preparado, separadamente
do agregado e sem instalar dependências como consequência implícita:

```sh
python -B -m unittest tools.tests.test_ser_parallel_b0 -v
python -B -m tools.skill_enforcement.parallel.coverage
```

O primeiro comando executa regressões; o segundo confronta identidade e coleta,
não executa todos os IDs coletados nem qualifica host/campanha. Registre versão
Python, SHA, comando e resultado. Outro interpretador exige verificação específica;
divergência de AST não autoriza recalcular hashes históricos. Na auditoria de
06/10/2026 do SHA `2c5975c0718ef9e30ec3fc26998338036262e87c`, a coleta direta
passou em 3.12. A análise de 3.11 foi apenas projeção do schema AST; a execução
do helper em 3.13.5 encontrou dois digests divergentes e não qualifica esse runtime.

Esta correção documental não reclassifica a falha histórica SER L2 versus L3
nem certifica Windows, Databricks, ACLs, ambiente institucional, transporte ou
promoção de policy.
