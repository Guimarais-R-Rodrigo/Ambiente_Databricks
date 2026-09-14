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
| T17 | suíte agregada de manutenção | regressão zero |

## Teste específico de YAML

O template não usa chaves literais `true:`/`false:`. PyYAML trata essas palavras como booleanos em modos compatíveis com YAML 1.1; por isso o contrato usa `quando_true`, `quando_false` e `quando_indeterminado`. T02 verifica que as chaves carregadas permanecem strings e que `True`/`False` não aparecem como chaves do mapping.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém `valido_validado.json` e `casos_invalidos.json`. O segundo descreve nove mutações negativas determinísticas aplicadas sobre a base válida; cada caso modifica apenas a dimensão que pretende quebrar sempre que possível, reduzindo duplicação e falso positivo por múltiplos defeitos independentes.

## Evidência local antes do commit

A suíte isolada foi executada em árvore temporária equivalente à estrutura final:

```text
Ran 9 tests
OK
```

As nove mutações negativas reprovaram pelo código esperado. O fixture positivo e o template foram aprovados. A suíte também confirma que uma decisão humana de validação não pode divergir do `validacao.status`.

## Evidência de CI da branch

Pendente até o primeiro commit da candidata. Esta seção deve ser atualizada com SHA e runs reais antes do checkpoint final.

## Auditoria A1

Pendente. O prompt independente deverá proibir `CHANGELOG.md`, histórico do Git, `docs/auditoria/` e a documentação narrativa de autoria da sprint. Como o schema/template são o próprio objeto auditado e vivem em `docs/sprints/micromodelos/MM01/`, eles serão uma exceção de leitura explicitamente enumerada; `README.md`, `CONTRATO_MICROMODELO.md`, `ESTADOS_E_PROVENIENCIA.md`, `TESTES.md` e `CHECKPOINT.md` permanecerão vedados ao auditor.
