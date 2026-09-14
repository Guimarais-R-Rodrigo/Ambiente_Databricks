# MM01 — Plano e evidências de testes

## Escopo

Os testes da MM01 exercitam o contrato estrutural e semântico. Não acessam Databricks, Unity Catalog, MLflow, dados reais, ACLs nem publicação externa. Todos os recursos usados são sintéticos.

## Matriz mínima

| ID | Caso | Resultado esperado |
|---|---|---|
| T01 | JSON Schema Draft 2020-12 | schema formal aceito pelo próprio validador de schema |
| T02 | `micromodelo.template.yaml` | APROVADO |
| T03 | fixture `VALIDADO` completo | APROVADO |
| T04 | grupo obrigatório ausente | `SCHEMA` |
| T05 | salto `IDEIA → EM_VALIDACAO` | `STATE_TRANSITION` |
| T06 | score habilitado sem semântica | `SCORE_SEMANTICS` |
| T07 | limiar material ainda `PROPOSTO` | `THRESHOLD_APPROVAL` |
| T08 | resultado `MEDIDO` sem referência de execução | `PROV_MEASUREMENT_REQUIRED` |
| T09 | fase `PUBLICADO` sem validação/saída/publicação externa | `PHASE_GATE` + gates de publicação |
| T10 | fonte com `catalogo_ref` não autorizado | `CATALOG_SCOPE` |
| T11 | definições de `FALSE` e `INDETERMINADO` iguais | `AMBIGUOUS_BINARY_SEMANTICS` |
| T12 | `PROBABILIDADE_CALIBRADA` sem calibração | `CALIBRATION_REQUIRED` |
| T13 | evidência referencia fonte inexistente | `UNKNOWN_SOURCE_REF` |
| T14 | score desabilitado com resíduos de score | `SCORE_DISABLED` |
| T15 | CLI em documento válido/inválido | exit code 0/1 respectivamente |
| T16 | gate estrutural do repositório | `tools/validate_assistant.py` sem FAIL |
| T17 | suíte agregada de manutenção na PR | regressão zero |

## Teste específico de YAML

O template não usa chaves literais `true:`/`false:`. PyYAML trata essas palavras como booleanos em modos compatíveis com YAML 1.1; por isso o contrato usa `quando_true`, `quando_false` e `quando_indeterminado`. T02 verifica que as chaves carregadas permanecem strings e que `True`/`False` não aparecem como chaves do mapping.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém `valido_validado.json` e `casos_invalidos.json`. O segundo descreve nove mutações negativas determinísticas aplicadas sobre a base válida; cada caso modifica apenas a dimensão que pretende quebrar sempre que possível, reduzindo duplicação e falso positivo por múltiplos defeitos independentes.

## Evidência local antes do primeiro commit

A suíte isolada foi executada em árvore temporária equivalente à estrutura final:

```text
Ran 9 tests
OK
```

As nove mutações negativas reprovaram pelo código esperado. O fixture positivo e o template foram aprovados. A suíte também confirma que uma decisão humana de validação não pode divergir do `validacao.status`.

## Evidências da branch

### Materialização inicial — falha histórica preservada

- run: `34899029039`;
- resultado: **failure** antes da instalação de dependências/testes;
- causa: corrupção do pacote gzip usado apenas como transporte transitório (`zlib.error: invalid distance too far back`);
- efeito na candidata: nenhum artefato de produto foi commitado por essa execução;
- tratamento: mecanismo de transporte substituído por três blobs menores com allowlist exata; a falha não foi apagada nem reclassificada como teste funcional.

### Materialização validada

- run: `34899617125`;
- resultado: **success**;
- executou materialização com allowlist, instalação de dependências, os 9 testes MM01 e `tools/validate_assistant.py --root ambiente_fonte`;
- o workflow transitório se removeu antes do commit final dos artefatos.

### Reconciliação com a `main` pós-V10

- `main` observada e fixada: `a9480391c78e2402986885db0ce08b10e0619a1a`;
- run transitório fail-closed: `34900062786`;
- resultado: **success**;
- executou merge local da base, reinstalação, 9 testes MM01 e gate estrutural antes do `push`;
- o workflow transitório de reconciliação se removeu antes da publicação da composição.

### Gate permanente MM01

- workflow: `.github/workflows/micromodelos-mm01-ci.yml`;
- primeiro head exercitado: `6ef778de8802967bdce0e99c4df2eeb6da96cc73`;
- run: `34900332458`;
- resultado: **success**;
- escopo: instalação limpa, `test_micromodelo_mm01.py -v`, `validate_assistant.py --root ambiente_fonte` e declaração explícita de que o gate não acessa sistemas/dados corporativos.

## Evidência de PR / suíte agregada

Pendente da abertura da PR. O CI geral (`.github/workflows/ci.yml`) não substitui o gate específico MM01: ele serve como regressão agregada do repositório. Ambos devem permanecer verdes no head final da candidata.

## Auditoria A1

Pendente. O auditor deverá trabalhar em sessão nova, executar os gates e criar casos adversariais próprios. `CHANGELOG.md`, histórico Git, relatórios prévios e a documentação narrativa de autoria da sprint ficam vedados; schema/template, validador, testes, fixtures e ADRs aceitos formam o conjunto permitido de evidências primárias.
