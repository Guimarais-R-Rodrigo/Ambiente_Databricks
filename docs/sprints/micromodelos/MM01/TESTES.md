# MM01 — Plano e evidências de testes

## Escopo

Os testes da MM01 exercitam exclusivamente o contrato estrutural e semântico. Não acessam Databricks, Unity Catalog, MLflow real, dados corporativos, ACLs ou publicação externa. Todos os documentos de teste são sintéticos.

A autoridade de aceite permanece `MATRIZ_ACEITE_FINAL.md`. A suíte canônica possui 47 métodos e as regressões dedicadas de fechamento acrescentam 3 métodos R02 e 1 método R03.

## Matriz de comportamento

| ID | Caso | Resultado esperado |
|---|---|---|
| T01 | JSON Schema Draft 2020-12 | schema formal aceito |
| T02 | `micromodelo.template.yaml` | APROVADO |
| T03 | fixture `VALIDADO` completo | APROVADO |
| T04 | grupo obrigatório ausente | `SCHEMA` |
| T05 | salto `IDEIA → EM_VALIDACAO` | `STATE_TRANSITION` |
| T06 | score habilitado sem semântica estruturada | `SCORE_SEMANTICS` |
| T07 | limiar/peso `PROPOSTO` antes de `EM_VALIDACAO` | permitido como proposta |
| T08 | limiar/peso não aprovado em `EM_VALIDACAO+` | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` |
| T09 | resultado `MEDIDO` sem referência material de execução | rejeição fail-closed |
| T10 | aprovação humana com referência não material | rejeição fail-closed |
| T11 | fase `PUBLICADO` sem validação/saída/publicação externa | gates de fase/publicação |
| T12 | `PUBLICADO` com referência externa não material | rejeição fail-closed |
| T13 | fonte com `catalogo_ref` não autorizado | `CATALOG_SCOPE` |
| T14 | definições TRUE/FALSE/INDETERMINADO editorialmente duplicadas | `AMBIGUOUS_BINARY_SEMANTICS` |
| T15 | `PROBABILIDADE_CALIBRADA` sem calibração | `CALIBRATION_REQUIRED` |
| T16 | calibração com `evidencia_ref` órfã ou experimento não executado/medido | `CALIBRATION_EVIDENCE_REF` |
| T17 | evidência referencia fonte inexistente | `UNKNOWN_SOURCE_REF` |
| T18 | score desabilitado com resíduos de score | `SCORE_DISABLED` |
| T19 | decisão humana diverge de `validacao.status` | `VALIDATION_HUMAN_GATE` |
| T20 | skips de fase e retorno declarado diretamente de `PUBLICADO` | recusados pela tabela de transições |
| T21 | especificação anterior `PUBLICADO` reescrita na mesma versão para fase anterior | `STATE_REWIND` |
| T22 | comparação com especificação anterior preserva identidade/versão e transição | fail-closed |
| T23 | CLI `--previous` bloqueia rewind pós-publicação | exit não zero + diagnóstico |
| T24 | propriedade livre `score.semantica` tenta reintroduzir prosa probabilística | `SCHEMA` |
| T25 | `PROBABILIDADE_CALIBRADA` com calibração medida/resolvida | APROVADO |
| T26 | calibração presente em score não probabilístico | `CALIBRATION_UNEXPECTED` |
| T27 | normalização textual/legada em vez de contrato estruturado | `SCHEMA` |
| T28 | normalização `PENDENTE` ao chegar em `EM_VALIDACAO+` | `SCORE_NORMALIZATION` |
| T29 | IDs duplicados em componentes/experimentos | `DUPLICATE_ID` |
| T30 | `EM_VALIDACAO+` com fontes/evidências/contra-evidências/critérios vazios | `PHASE_CONTENT_GATE` |
| T31 | status de publicação incompatível com fase | `PUBLICATION_STATUS_PHASE` |
| T32 | política de ausência `INDETERMINADO` com resultado `FALSE` | `MISSING_POLICY_CONTRADICTION` |
| T33 | tentativa de reintroduzir descrição normativa livre em políticas fechadas | `SCHEMA` |
| T34 | `REGRA_EXPLICITA_APROVADA` com regra auditável | APROVADO |
| T35 | `indeterminado_vira_false=true` | `SCHEMA` / gate estruturado |
| T36 | caminhos positivos até `PUBLICADO` | APROVADOS |
| T37 | propriedade material desconhecida | `SCHEMA` |
| T38 | YAML/JSON com chave duplicada | erro de carga fail-closed |
| T39 | CLI válida/inválida e flag fora do contrato | exit 0/1/2 conforme caso |
| T40 | gate estrutural do repositório | `tools/validate_assistant.py` sem FAIL |
| T41 | CI agregado da PR | regressão zero no head final técnico |
| T42 | `material-text` com marcas/formatos/whitespace/pontuação/símbolo isolados | `SCHEMA` |
| T43 | materialidade Unicode positiva multilíngue | APROVADO |
| T44 | proveniência de topo e gates materiais usam a mesma política Unicode | coerência de rejeição/aceite |
| T45 | regras, hipótese/resultado, resumo e motivo operacional não materiais | `SCHEMA` / gate fail-closed |
| T46 | mesmos campos normativos com Unicode legítimo | APROVADO |
| T47 | textos obrigatórios adicionais com conteúdo não material que satisfaz `minLength` | `SCHEMA` |
| T48 | mesmos campos adicionais com Unicode legítimo | APROVADO |
| T49 | todo `type=string + minLength` possui política material explícita | invariável estrutural |
| T50 | qualquer `pattern` pertence à allowlist estrutural exata | invariável estrutural |
| T51 | `string + minLength + pattern` genérico sem `material-text` | detectado como violação |
| T52 | default-ignorables dentro de palavra em semânticas equivalentes | `AMBIGUOUS_BINARY_SEMANTICS` |
| T53 | `type=[string]` / `[string,null]` + `minLength` | detectado pelo guard |
| T54 | NaN/±Infinity em limiar/peso e constantes JSON não padrão | `SCHEMA` / carga fail-closed |
| T55 | fillers/default-ignorables Unicode como texto material | `SCHEMA` / `_has_material_text=False` |
| T56 | equivalência editorial com DICP + pares distintos por operador/diacrítico | invisíveis equivalentes; diferenças preservadas |
| T57 | inteiro acima do intervalo de float + tipos numéricos externos | inteiro aceito; externos rejeitados |
| T58 | aprovação humana final durante validação pendente ou sem metadados | `VALIDATION_HUMAN_GATE` |
| T59 | política de publicação antecipada com proveniência inválida | `PROV_APPROVAL_REQUIRED` |
| T60 | experimento não `EXECUTADO` com resultado observado | `EXPERIMENT_RESULT` |
| T61 | CLI sem/com `--previous` | `SNAPSHOT_VALIDO/HISTORICO_NAO_CERTIFICADO` vs `APROVADO_EVOLUCAO` |
| T62 | perfil de autoria do schema | recusa composição fora do perfil congelado |
| T63 | `np.float64` fornecido diretamente em limiar e peso | `SCHEMA`; tipo externo recusado deterministicamente |
| T64 | pontuação terminal vs pontuação inicial em R02 | terminal equivalente; inicial preservada; sem falso `AMBIGUOUS_BINARY_SEMANTICS` |

A tabela representa comportamentos e não uma relação 1:1 com métodos. Vários métodos canônicos usam subtests e percorrem múltiplas linhas.

## Composição da suíte permanente

### Suíte canônica — 47 métodos

```bash
python -B -m unittest tools/tests/test_micromodelo_mm01.py -v
```

Ela cobre o contrato geral, R01–R08, fixtures, CLI, perfil de autoria do schema, publicação, score, proveniência, decisão humana e histórico explícito.

### Regressão R02 — 3 métodos

```bash
python -B -m unittest tools/tests/test_micromodelo_mm01_r02.py -v
```

A regressão foi adicionada após a nona reauditoria final independente e prova três propriedades distintas:

1. pontuação terminal editorial continua sendo tolerada depois de NFKC/casefold/DICP/whitespace;
2. pontuação inicial não é apagada pela canonicalização;
3. em validação end-to-end, prefixos `?` e `…` não fabricam `AMBIGUOUS_BINARY_SEMANTICS` contra uma definição sem o prefixo.

A elipse Unicode merece atenção: NFKC pode transformá-la em `...`. O teste não exige preservar o code point original; exige preservar a **distinção de posição inicial** prevista em R02.

### Regressão R03 — 1 método

```bash
python -B -m unittest tools/tests/test_micromodelo_mm01_r03.py -v
```

O teste importa NumPy real e injeta `np.float64` em:

- `classificacao.limiares[].valor`;
- `score.componentes[].peso`.

O checker precisa recusar o tipo externo e a validação precisa retornar `SCHEMA`. A regra é positiva para `int`/`float` Python, não uma blacklist de NumPy.

### Gate estrutural

```bash
python -B tools/validate_assistant.py --root ambiente_fonte
```

O gate verifica integridade estrutural, higiene de conteúdo, links, READMEs, objetos Python e métricas congeladas do repositório. Ele é complementar à suíte MM01 e pode reprovar por documentação/higiene mesmo quando todos os testes do contrato passam.

## Teste específico de YAML/JSON

O template evita chaves literais `true:` e `false:` porque loaders YAML podem interpretá-las como booleanos. O contrato usa `quando_true`, `quando_false` e `quando_indeterminado`.

O loader customizado também rejeita chaves duplicadas em YAML e JSON. A MM01 não aceita “última chave vence”, pois isso poderia fazer a revisão humana enxergar valor diferente do efetivamente validado.

## Materialidade Unicode

R01 usa uma autoridade única. Após NFKC e remoção de `Default_Ignorable_Code_Point`, precisa restar letra ou número Unicode. A suíte contém negativos com marks isolados, zero-width, variation selectors, fillers, whitespace, pontuação e símbolos; e positivos multilíngues para impedir regressão ASCII-cêntrica.

## Equivalência editorial R02

O contrato não tenta inferir significado natural. A canonicalização deve ser previsível e conservadora. Ela preserva:

- diacríticos;
- `<`, `>`, `≤`, `≥`;
- `+` e `-`;
- pontuação interna;
- pontuação inicial.

Ela pode tolerar somente a pontuação terminal explicitamente configurada.

A nona reauditoria demonstrou que `str.strip(chars)` violava essa posição porque remove em ambas as extremidades. A correção usa `rstrip(chars)` depois do trim de whitespace.

## Domínio numérico R03

Os testes exercitam:

- `int` Python comum;
- inteiro Python arbitrariamente grande;
- `float` Python finito;
- `NaN`;
- `+Infinity`;
- `-Infinity`;
- constantes JSON não finitas;
- escalares NumPy fornecidos diretamente.

A implementação não converte inteiro enorme para float e não interpreta implicitamente tipos de bibliotecas externas.

## Snapshot e evolução R07

Sem `--previous`, a CLI deve retornar aprovação de snapshot com `HISTORICO_NAO_CERTIFICADO`. Com snapshot anterior confiável, deve retornar `APROVADO_EVOLUCAO` somente se identidade, versão e transição histórica forem coerentes.

Uma versão já `PUBLICADO` não pode ser reescrita para fase anterior na mesma versão.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém:

- `valido_validado.json`: caso completo e positivo em fase `VALIDADO`;
- `casos_invalidos.json`: mutações negativas determinísticas aplicadas à base válida.

Outros adversariais são construídos em memória para não inflar fixtures com variações mecânicas.

## Evidências históricas e auditorias

Os relatórios independentes são preservados no diretório `docs/auditoria/2026-09-14_micromodelos-mm01/`. Um relatório nunca muda de veredito só porque uma candidata posterior corrigiu o defeito.

A matriz final congelada surgiu após a oitava A1 para impedir crescimento ilimitado do threat model. Os requisitos materiais de fechamento são R01–R08.

### Auditoria final fechada anterior

`11_resultado_a1_reauditoria_8.md` encontrou:

- R03: aceitação indevida de `np.float64` por `isinstance(value, float)`;
- gate final: `behind_by` diferente de zero.

A regressão T63 e a reconciliação com `main` fecharam esses dois pontos. R03 passou na reauditoria seguinte.

### Nona reauditoria final independente

`12_resultado_a1_reauditoria_9.md` julgou `4dc6bb12d2e4df6c3dbff7aa4711a99bf660bb6b` e concluiu `NAO_APTA` por D-01/R02: pontuação inicial era apagada como se fosse terminal.

T64 e `tools/tests/test_micromodelo_mm01_r02.py` tornam a correção regressiva.

A sanitização de metadados do relatório histórico posterior à auditoria não altera o achado nem o veredito. Ela existe somente para satisfazer o gate de higiene do repositório.

## Evidência da rodada corretiva R02

No run `35044200964`, em Ubuntu 24.04.5 / CPython 3.12.14:

- suíte canônica: **47/47 OK**;
- regressão R02: **3/3 OK**;
- regressão R03: **1/1 OK**.

O run terminou vermelho somente no `validate_assistant` porque o relatório histórico recém-adicionado ainda continha padrões que o detector de higiene recusava. O primeiro era o owner do repositório; o segundo, um SHA abreviado que coincidiu acidentalmente com a regex genérica “letra + 6–8 dígitos”. Ambos foram sanitizados/expandidos sem alteração técnica do relatório.

Como a árvore foi modificada depois desse run, essa evidência é intermediária. A certificação relevante para congelamento é a execução sobre o HEAD documental final.

## Workflow corretivo transitório

O run `35043439501` pertence a um mecanismo temporário de correção que falhou antes de abrir jobs (`jobs=[]`). Nenhuma alteração técnica foi publicada por ele. O workflow temporário foi removido e não faz parte da árvore candidata.

## Reconciliação com outras iniciativas

A MM01 absorve a `main` como base; ela não reimplementa funcionalidades de Temas. Nesta rodada, V13 S1/S2 foram incorporadas por merge real `877a3b9325281de3a276c909cabe6dfed4913b79`.

Os gates transversais precisam permanecer verdes. Em particular, V12 deve detectar quando seu gate de escopo estrito não se aplica a uma PR de MM01, em vez de reprovar arquivos legítimos de outra iniciativa.

## Gate para a próxima candidata

Antes de considerar uma nova candidata congelada:

1. executar 47 + 3 + 1 testes permanentes no SHA exato;
2. executar `validate_assistant` sem falha/aviso;
3. verificar todos os workflows aplicáveis da PR, inclusive gates herdados de Temas;
4. reconfirmar `main`, merge-base e `behind_by=0`;
5. verificar merge-ref e equivalência material HEAD × merge-ref;
6. congelar o SHA;
7. submeter esse SHA a nova **reauditoria final independente** em contexto separado.

Mesmo com auditoria limpa, ainda não se faz merge imediatamente: vêm contraditório final, sincronização byte-preserving do bloco MM01 do `CHANGELOG.md`, revalidação da árvore exata e aceite explícito do usuário.

**MM02 permanece bloqueada.**


## MM01 Local Certification v1

Com GitHub Actions indisponível como canal executável, os requisitos técnicos continuam inalterados e a execução mecânica passa a ser feita por `tools/mm01_local_certify.py`, conforme `LOCAL_CERTIFICATION_V1.md`.

O certifier reproduz os comandos dos workflows permanentes relevantes, exige SHA/branch/`origin/main`/merge-base/`behind_by=0`, worktree limpa e checkout não-shallow, registra ambiente, exit codes e logs e gera bundle probatório com checksums.

A lista de workflows-fonte é fail-closed por identidade Git blob. Se qualquer workflow for alterado, inclusive pela inclusão de um novo gate, a certificação falha até que o plano local seja reconciliado deliberadamente. O teste `tools/tests/test_mm01_local_certify.py` protege o conjunto exato de fontes e os pins correntes.

Um bundle `PASS` não equivale a aceite MM01: ainda são obrigatórios auditoria independente, contraditório final, fechamento documental, revalidação da árvore e aceite humano explícito.
