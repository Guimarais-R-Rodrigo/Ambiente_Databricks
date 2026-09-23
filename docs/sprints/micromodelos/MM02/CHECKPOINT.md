# MM02 — checkpoint

## Estado

```text
MM02 = POS_CERTIFICACAO
BASE_MAIN = 86d1ff6a52d8ef03f6d5567afed6897c1b96c8c3
BRANCH = micromodelos/mm02-spec-fingerprint
CERTIFIED_SHA = 3d3c6d40263a253449b448a3bcca679143252e54
CANDIDATE_FREEZE = REACHED
PRE_CERTIFICATION_SMOKE = PASS
FULL_CERTIFICATION = PASS
INDEPENDENT_AUDIT = APTA_COM_CORRECAO_PROBATORIA
AUDIT_FINDINGS_OPEN = 0
DOC_CLOSE_MINIMO = IN_PROGRESS
FINAL_TREE_REVALIDATION = PENDING
PR = #109 OPEN_DRAFT
```

## Escopo implementado repo-side

Até este checkpoint foram materializados:

- algoritmo `mm02-spec-fingerprint-v1`;
- SHA-256 sobre JSON canônico UTF-8;
- validação obrigatória pelo contrato MM01 antes do hash;
- perfil explícito de campos materiais versus ciclo de vida;
- reutilização da equivalência editorial MM01;
- canonicalização de coleções não ordenadas;
- deduplicação de listas editoriais após equivalência MM01;
- canonicalização numérica `int/float` equivalente;
- suíte metamórfica permanente;
- documentação de limites e smoke.

## Decisões da sprint

### Definição versus evidência

O fingerprint identifica a **definição analítica material**.

Ficam fora da identidade:

- fase/condição;
- versão humana;
- proveniência;
- aprovação;
- medição;
- experimento/resultado observado;
- validação;
- tracking;
- governança;
- status institucional de publicação.

Isso preserva a separação arquitetural já aceita:

```text
YAML = definição
fingerprint = identidade material da definição
run / evidence = execução
approval = governança
publication = autoridade externa
```

### Identidade humana

`identidade.nome`, `titulo` e `micromodel_version` não entram no preimage.

O fingerprint pode coincidir entre artefatos distintos quando a definição material for a mesma. Nome e versão humana continuam disponíveis separadamente para rastreabilidade.

### Texto

Não existe normalização semântica geral.

Somente textos normativos selecionados usam a equivalência editorial conservadora já implementada pela MM01. Identificadores operacionais permanecem exatos.

### Números

Valores numéricos materiais usam representação decimal determinística para que `70` e `70.0` sejam equivalentes.

O domínio aceito continua sendo o domínio validado pela MM01.

### Referências materiais versus audit trail

A revisão estática distinguiu referências que apenas provam uma decisão das que definem uma regra:
- `score.semantica_ref` só entra para `OUTRA_APROVADA`;
- `score.normalizacao.referencia` só entra para `CUSTOM_APROVADO`;
- `score.calibracao.evidencia_ref` entra como identidade da calibração escolhida;
- resultados, run IDs, timestamps, responsáveis e proveniência continuam fora.

## Não implementado

- persistência de `spec_fingerprint` no YAML;
- alteração do schema MM01;
- skill;
- prompt;
- metadata crawler;
- MLflow;
- Receipt/Postflight;
- publicação;
- integração Databricks;
- persistência do fingerprint em artefato runtime;
- homologação Databricks/Genie;
- merge/aceite humano.

## Certificação observada

```text
SMOKE_S1 = PASS
FULL_R1 = PASS
MM02_TESTS = 30/30
MM01_CANONICAL = 47/47
MM01_R02 = 3/3
MM01_R03 = 1/1
SPEC_FINGERPRINT = 4c88baa416dc4de6edc1f196416e9c12272962703eb3d26cd6790d653fd73eac
SNAPSHOT = 1707/2151/0
CI_LOCAL = 10/10
RETRIES = 0
PATCHES = 0
COMMITS_DURING_FULL = 0
PUSHES = 0
MERGES = 0
```

Bundle fonte: SHA-256 `4c06fa14470464c311c43920affcfba43796b521bcd7a79c1876d8bf758f3ed0`.

A auditoria independente encontrou somente `A1-BUNDLE-01`, sanitização residual de paths HOME escapados no G07. O contraditório manteve o finding como exclusivamente probatório e confirmou que nenhuma reexecução funcional era necessária. Derivado sanitizado auditável: SHA-256 `0acbddd116dd4fad2a78aa7b08e6fc45baf832903acee526cec283e38628df34`; zero findings abertos.

## Próximo gate

Aplicar apenas fechamento documental mínimo e executar `FINAL_TREE_REVALIDATION` sobre a árvore resultante. A FULL não deve ser repetida se o compare `CERTIFIED_SHA → final` permanecer exclusivamente documental e fora dos inputs/gates certificados.

PR #109 permanece Draft. Aceite humano e merge continuam bloqueados até a revalidação final.
