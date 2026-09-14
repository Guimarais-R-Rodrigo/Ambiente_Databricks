# V09 — testes e evidências

## Estado

Candidata em fechamento técnico. Este documento registra successes e failures sem reclassificar resultados históricos.

## Suíte específica

`tools/tests/test_temas_v09.py` cobre:

- existência real de todos os caminhos obrigatórios no produto sanitizado;
- metadados fail-closed de transporte, ativação e publicação;
- mutante negativo removendo, um a um, cada caminho obrigatório;
- coerência entre inventário e bloco `theme_contract`;
- integração da guarda ao gerador antes da escrita do ZIP;
- preservação de `schema_version = 2`;
- instrução operacional no checklist;
- workflow permanente read-only;
- ZIP sintético válido com conferência dos bytes reais;
- ZIP com arquivo temático ausente ou adulterado recusado;
- ambos os workflows executando a validação pós-build, com o workflow operacional verificando antes do upload.

## Gate V09

O workflow `.github/workflows/temas-v09-ci.yml` executa:

```bash
python -B tools/tests/test_temas_v09.py -v
python -B tools/tests/test_transicao_trabalho.py -v
python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v
python -B tools/tests/test_visual_legado_v00.py
python -B tools/kit_transicao_trabalho.py --output .artifacts/v09-kit
python -B tools/temas_v09_transicao.py --kit-dir .artifacts/v09-kit
python -B tools/validate_assistant.py --conferir-readme
```

A geração e inspeção do kit são locais ao runner e não usam credenciais Databricks. O workflow permanente declara `contents: read` e o checkout usa `persist-credentials: false`.

## Failures preservados

### `34877035267` — FAILURE de oráculo textual da suíte V09

No head `17a95762b9f6dc19c13cf008ee581bc7c1041d26`, sete dos oito testes V09 passaram. O único failure foi `test_transition_checklist_names_theme_contract`: o checklist registra corretamente a chave real `manual_opt_in`, mas o teste procurava a expressão inexistente `manual/opt-in`. A implementação do contrato não foi alterada para acomodar o teste; o oráculo foi corrigido no commit seguinte. As etapas posteriores foram puladas porque a suíte específica já havia reprovado.

Esse run permanece **FAILURE**.

### `34877297808` — FAILURE documental após todos os gates funcionais passarem

No head `b7d16ab6eccf59a266353dc74502cf51703ad8c3` passaram:

- V09 específica: **8/8**;
- regressões do kit de transição: **43 testes executados, 36 PASS e 7 SKIP** porque a chamada dessa etapa não usa `--spark`;
- regressões cumulativas V01–V09: **413/413**;
- compatibilidade V00: **12/12**;
- geração real do kit offline: **535 arquivos + `MANIFEST.json`**, commit do kit `b7d16ab6eccf...`.

O único bloqueio foi `validate_assistant.py --conferir-readme`: a execução mediu `1355` arquivos no repositório editável/derivado, enquanto o README raiz ainda continha `1350`. O validador terminou com **1 falha e 0 avisos**. A correção altera somente esse número colado no README; nenhum contrato ou runtime foi relaxado.

Esse run permanece **FAILURE**.

## Gate completo verde de referência

### `34878578986` — SUCCESS no head `6c19ef6da1012b4c33bd0e15c1bb332a6cb046a3`

O run executou a versão já endurecida com verificação pós-build do ZIP:

- V09 específica: **11/11 PASS**;
- regressões do kit de transição: **43 testes**, com **36 PASS e 7 SKIP** porque essa etapa deliberadamente não usa `--spark`; os sete casos Spark permanecem cobertos pelo workflow operacional do kit com `--spark`;
- regressões cumulativas V01–V09: **416/416 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- bundle real: **535 arquivos + `MANIFEST.json`**;
- commit gravado no kit: `6c19ef6da1012b4c33bd0e15c1bb332a6cb046a3`;
- SHA256 do manifesto: `5a2df33ce8c97b426efd0fd231f2e4974fa505c507753cf0a0698274430ff1a7`;
- inspeção pós-build: `theme_contract v1`, **9 caminhos obrigatórios presentes e com SHA256 válido**, `manual_opt_in`, `not_performed`;
- validador: **APROVADO — 0 falhas / 0 avisos**;
- métricas vivas do validador: 14 skills, 16 prompts/161 campos, 92 helpers citados, 217 Markdown/1382 links relativos, 80 notebooks/101 links, 76/76 READMEs de objeto + 3/3 exemplares, 62 pastas de objeto, 60 formas de pasta, 62 contratos de saída, 60 contratos de entrada, 79 notebooks com saída colada, 62 docstrings e 0 em inglês, 72 arquivos de molde e 0 violações, 60 objetos exercitados, 217 arquivos Python AST, instruções 9043/20000, 1355 arquivos de identidade, 1850 links fora da raiz e 0 extras locais;
- `GITHUB_TOKEN`: `Contents: read`, `Metadata: read`;
- escopo final do workflow confirmou explicitamente ausência de publicação/ativação Databricks.

Depois desse run foram feitas somente reconciliações documentais dos índices vivos; nenhuma implementação, contrato ou arquivo `.assistant` foi alterado. O head que for levado à PR deve receber novo gate exato antes de ser considerado candidato final.

## O que PASS não prova

- importação real no workspace corporativo;
- render visual no navegador Databricks;
- acessibilidade ou UAT humano;
- ativação ou promoção de tema;
- permissão/ACL do destino;
- publicação Databricks.
