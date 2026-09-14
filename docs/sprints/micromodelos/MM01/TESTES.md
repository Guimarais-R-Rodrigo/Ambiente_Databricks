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
| T07 | limiar/peso `PROPOSTO` antes de `EM_VALIDACAO` | permitido como proposta |
| T08 | limiar/peso não aprovado em `EM_VALIDACAO+` | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` |
| T09 | resultado `MEDIDO` sem referência material de execução | rejeição fail-closed |
| T10 | aprovação humana com referência vazia, whitespace ou caractere invisível | rejeição fail-closed |
| T11 | fase `PUBLICADO` sem validação/saída/publicação externa | gates de fase/publicação |
| T12 | `PUBLICADO` com referência externa vazia/whitespace | rejeição fail-closed |
| T13 | fonte com `catalogo_ref` não autorizado | `CATALOG_SCOPE` |
| T14 | definições TRUE/FALSE/INDETERMINADO semanticamente iguais | `AMBIGUOUS_BINARY_SEMANTICS` |
| T15 | `PROBABILIDADE_CALIBRADA` sem calibração | `CALIBRATION_REQUIRED` |
| T16 | calibração com `evidencia_ref` órfã ou experimento não executado/medido | `CALIBRATION_EVIDENCE_REF` |
| T17 | evidência referencia fonte inexistente | `UNKNOWN_SOURCE_REF` |
| T18 | score desabilitado com resíduos de score | `SCORE_DISABLED` |
| T19 | decisão humana diverge do `validacao.status` | `VALIDATION_HUMAN_GATE` |
| T20 | skips de fase e retorno declarado diretamente de `PUBLICADO` | recusados pela tabela de transições |
| T21 | especificação anterior `PUBLICADO` reescrita na mesma versão para fase anterior | `STATE_REWIND` |
| T22 | comparação com especificação anterior preserva identidade/versão e valida transição real | fail-closed |
| T23 | CLI `--previous` bloqueia rewind pós-publicação | exit não zero + diagnóstico |
| T24 | linguagem probabilística em score não calibrado | `SCORE_PROBABILITY_LANGUAGE` |
| T25 | probabilidade calibrada com evidência medida e experimento resolvido | APROVADO |
| T26 | IDs duplicados em componentes/experimentos | `DUPLICATE_ID` |
| T27 | `EM_VALIDACAO+` com fontes/evidências/contra-evidências/critérios vazios | `PHASE_CONTENT_GATE` |
| T28 | status de publicação incompatível com fase | `PUBLICATION_STATUS_PHASE` |
| T29 | política estruturada de `INDETERMINADO` contradiz descrição que manda converter para `FALSE` | `INDETERMINATE_POLICY_CONFLICT` |
| T30 | caminhos positivos `CANDIDATO_PRODUTO → EM_VALIDACAO_GOVERNANCA → PUBLICADO` | APROVADOS |
| T31 | propriedade material desconhecida | `SCHEMA` |
| T32 | YAML/JSON com chave duplicada | erro de carga fail-closed |
| T33 | CLI válido/inválido e tentativa de `--catalog-ref` não contratada | exit 0/1/2 |
| T34 | gate estrutural do repositório | `tools/validate_assistant.py` sem FAIL |
| T35 | CI agregado da PR | regressão zero no head final técnico |

A suíte `tools/tests/test_micromodelo_mm01.py` contém **24 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz acima. `casos_invalidos.json` mantém nove mutações negativas determinísticas além dos casos adversariais construídos diretamente pela suíte.

## Teste específico de YAML

O template não usa chaves literais `true:`/`false:`. PyYAML pode interpretar essas palavras como booleanos; por isso o contrato usa `quando_true`, `quando_false` e `quando_indeterminado`.

Além disso, o carregador customizado rejeita chaves duplicadas em YAML e JSON. A MM01 não aceita o comportamento “última chave vence”, porque uma especificação material poderia aparentar um valor na revisão humana e efetivamente validar outro.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém:

- `valido_validado.json`: caso completo em fase `VALIDADO`;
- `casos_invalidos.json`: nove mutações negativas aplicadas à base válida.

Os testes adversariais adicionais criam cópias em memória para evitar inflar fixtures com variações mecânicas. Após a primeira A1, a suíte passou a cobrir explicitamente rewind pós-`PUBLICADO` com especificação anterior confiável, referências materialmente vazias, proposta progressiva de limiares/pesos, contradição da política de `INDETERMINADO` e integridade referencial da calibração.

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

### Reconciliações de base

- a candidata foi reconciliada primeiro com a `main` pós-V10 e depois com a `main` pós-V11 antes da correção dos achados A1;
- as reconciliações preservaram a frente visual como base, sem reimplementá-la dentro da MM01;
- a PR voltou a `mergeable=true` antes das correções funcionais.

### Primeira A1 — `NAO_APTA`

A auditoria independente encontrou cinco bloqueios procedentes:

1. rewind pós-`PUBLICADO` não era verificável contra estado anterior confiável;
2. referências auditáveis podiam ser preenchidas apenas com whitespace;
3. limiares/pesos `PROPOSTO` eram rejeitados cedo demais;
4. a descrição da política de `INDETERMINADO` podia contradizer o tratamento estruturado;
5. `score.calibracao.evidencia_ref` aceitava referência órfã.

Nenhum achado foi descartado no contraditório. Todos foram tratados dentro do escopo da MM01.

### Reteste das correções A1

- run transitório final `34909835696`: **success**;
- 24 métodos de teste executados: `Ran 24 tests`, `OK`;
- o gate estrutural executado sobre a árvore preparada para publicação concluiu `APROVADO: 0 falha(s), 0 aviso(s)`;
- o mecanismo transitório e o script de aplicação foram removidos antes da publicação das correções;
- o commit publicado pela automação contém apenas os artefatos permanentes corrigidos e a métrica verificável do README.

O run transitório é evidência de construção, não substitui os workflows permanentes da candidata final. Os IDs dos checks permanentes do head final serão registrados na descrição da PR #51, evitando commits autorreferentes apenas para copiar seus próprios run IDs.

## Reauditoria A1

**Pendente.** A primeira A1 permanece historicamente `NAO_APTA`; seu resultado não será reescrito. A candidata corrigida precisa ser reavaliada em sessão independente contra um novo HEAD identificado.

A reauditoria deve repetir instalação, suíte MM01, gate estrutural, CLI do template e os adversariais de rewind pós-`PUBLICADO`, whitespace/invisíveis em provas auditáveis, `PROPOSTO` pré-gate, política contraditória de `INDETERMINADO` e calibração com referência órfã.

MM02 permanece bloqueada até reauditoria, aceite explícito e integração da MM01.
