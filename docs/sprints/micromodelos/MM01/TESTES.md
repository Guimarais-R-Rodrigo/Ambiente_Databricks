# MM01 — Plano e evidências de testes

## Escopo

Os testes da MM01 exercitam o contrato estrutural e semântico. Não acessam Databricks, Unity Catalog, MLflow, dados reais, ACLs nem publicação externa. Todos os recursos usados são sintéticos.

## Matriz de comportamento

| ID | Caso | Resultado esperado |
|---|---|---|
| T01 | JSON Schema Draft 2020-12 | schema formal aceito |
| T02 | `micromodelo.template.yaml` | APROVADO |
| T03 | fixture `VALIDADO` completo | APROVADO |
| T04 | grupo obrigatório ausente | `SCHEMA` |
| T05 | salto `IDEIA → EM_VALIDACAO` | `STATE_TRANSITION` |
| T06 | score habilitado sem semântica | `SCORE_SEMANTICS` |
| T07 | limiar material ainda `PROPOSTO` | `THRESHOLD_APPROVAL` |
| T08 | resultado `MEDIDO` sem referência de execução | `PROV_MEASUREMENT_REQUIRED` |
| T09 | fase `PUBLICADO` sem validação/saída/publicação externa | gates de fase/publicação |
| T10 | fonte com `catalogo_ref` não autorizado | `CATALOG_SCOPE` |
| T11 | definições TRUE/FALSE/INDETERMINADO semanticamente iguais | `AMBIGUOUS_BINARY_SEMANTICS` |
| T12 | `PROBABILIDADE_CALIBRADA` sem calibração | `CALIBRATION_REQUIRED` |
| T13 | evidência referencia fonte inexistente | `UNKNOWN_SOURCE_REF` |
| T14 | score desabilitado com resíduos de score | `SCORE_DISABLED` |
| T15 | decisão humana diverge do `validacao.status` | `VALIDATION_HUMAN_GATE` |
| T16 | skips de fase e retorno de `PUBLICADO` | recusados pela tabela de transições |
| T17 | linguagem probabilística em score não calibrado | `SCORE_PROBABILITY_LANGUAGE` |
| T18 | probabilidade calibrada com evidência `MEDIDO` | APROVADO |
| T19 | IDs duplicados em componentes/experimentos | `DUPLICATE_ID` |
| T20 | `EM_VALIDACAO+` com fontes/evidências/contra-evidências/critérios vazios | `PHASE_CONTENT_GATE` |
| T21 | status de publicação incompatível com fase | `PUBLICATION_STATUS_PHASE` |
| T22 | caminhos positivos `CANDIDATO_PRODUTO → EM_VALIDACAO_GOVERNANCA → PUBLICADO` | APROVADOS |
| T23 | propriedade material desconhecida | `SCHEMA` |
| T24 | YAML/JSON com chave duplicada | erro de carga fail-closed |
| T25 | CLI válido/inválido e tentativa de `--catalog-ref` não contratada | exit 0/1/2 |
| T26 | gate estrutural do repositório | `tools/validate_assistant.py` sem FAIL |
| T27 | CI agregado da PR | regressão zero no head final técnico |

A suíte `tools/tests/test_micromodelo_mm01.py` contém **17 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz acima. `casos_invalidos.json` mantém nove mutações negativas determinísticas além dos casos adversariais construídos diretamente pela suíte.

## Teste específico de YAML

O template não usa chaves literais `true:`/`false:`. PyYAML pode interpretar essas palavras como booleanos; por isso o contrato usa `quando_true`, `quando_false` e `quando_indeterminado`.

Além disso, o carregador customizado rejeita chaves duplicadas em YAML e JSON. A MM01 não aceita o comportamento “última chave vence”, porque uma especificação material poderia aparentar um valor na revisão humana e efetivamente validar outro.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém:

- `valido_validado.json`: caso completo em fase `VALIDADO`;
- `casos_invalidos.json`: nove mutações negativas aplicadas à base válida.

Os testes adversariais adicionais criam cópias em memória para evitar inflar fixtures com variações mecânicas: duplicidade de IDs, equivalência semântica cosmética, linguagem probabilística, coleções vazias em fase avançada, status de publicação incompatível, chaves duplicadas e tentativa de ampliar catálogo pela CLI.

## Evidências históricas preservadas

### Materialização inicial — failure de transporte

- run `34899029039`;
- **failure** antes da instalação/testes por corrupção do pacote gzip usado como transporte transitório;
- nenhum artefato de produto foi publicado por essa execução;
- a falha é histórica e não foi reclassificada como teste funcional.

### Materialização validada

- run `34899617125`: **success**;
- materialização com allowlist, instalação, suíte então vigente e gate estrutural;
- workflow transitório removido antes da composição final.

### Reconciliação com a `main` pós-V10

- base reconciliada: `a9480391c78e2402986885db0ce08b10e0619a1a`;
- run `34900062786`: **success**;
- merge local fail-closed, reinstalação, suíte MM01 e gate estrutural antes do push;
- workflow transitório removido.

### Gate permanente e endurecimento adversarial

- `.github/workflows/micromodelos-mm01-ci.yml` é permanente e read-only;
- run `34903052597` sobre o endurecimento adversarial: **success**;
- run `34903285176` sobre o caminho positivo de publicação: **success**;
- o gate específico instala dependências de manutenção, executa `test_micromodelo_mm01.py -v`, executa `validate_assistant.py --root ambiente_fonte` e declara explicitamente a fronteira sem acesso corporativo.

No mesmo head técnico do segundo run, V00, V01 e V02 também concluíram com `success`; o CI agregado foi disparado normalmente. A validação da árvore documental final será registrada na descrição da PR #51, para não gerar um novo commit apenas com os IDs dos próprios runs.

## Auditoria A1

**Pendente.** O pacote está em `docs/auditoria/2026-09-14_micromodelos-mm01/`.

O auditor deverá trabalhar em sessão nova, executar os gates e criar casos adversariais próprios. `CHANGELOG.md`, histórico Git, relatórios prévios e a documentação narrativa de autoria da sprint ficam vedados; schema/template, validador, testes, fixtures e ADRs aceitos formam o conjunto permitido de evidências primárias.

A auditoria não será executada pela sessão implementadora e não será substituída pelo CI verde.
