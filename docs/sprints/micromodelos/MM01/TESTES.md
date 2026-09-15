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
| T06 | score habilitado sem semântica estruturada | `SCORE_SEMANTICS` |
| T07 | limiar/peso `PROPOSTO` antes de `EM_VALIDACAO` | permitido como proposta |
| T08 | limiar/peso não aprovado em `EM_VALIDACAO+` | `THRESHOLD_APPROVAL` / `WEIGHT_APPROVAL` |
| T09 | resultado `MEDIDO` sem referência material de execução | rejeição fail-closed |
| T10 | aprovação humana com referência vazia, whitespace, zero-width ou marca Unicode isolada | rejeição fail-closed |
| T11 | fase `PUBLICADO` sem validação/saída/publicação externa | gates de fase/publicação |
| T12 | `PUBLICADO` com referência externa vazia, whitespace ou marca Unicode isolada | rejeição fail-closed |
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
| T24 | propriedade livre `score.semantica` tenta reintroduzir prosa probabilística | `SCHEMA` |
| T25 | `tipo_semantica=PROBABILIDADE_CALIBRADA` com calibração medida/resolvida | APROVADO |
| T26 | calibração presente em score não probabilístico | `CALIBRATION_UNEXPECTED` |
| T27 | normalização textual/legada em vez de contrato estruturado | `SCHEMA` |
| T28 | normalização `PENDENTE` ao chegar em `EM_VALIDACAO+` | `SCORE_NORMALIZATION` |
| T29 | IDs duplicados em componentes/experimentos | `DUPLICATE_ID` |
| T30 | `EM_VALIDACAO+` com fontes/evidências/contra-evidências/critérios vazios | `PHASE_CONTENT_GATE` |
| T31 | status de publicação incompatível com fase | `PUBLICATION_STATUS_PHASE` |
| T32 | política de ausência `INDETERMINADO` com `resultado_sem_evidencia=FALSE` | `MISSING_POLICY_CONTRADICTION` |
| T33 | tentativa de reintroduzir `descricao` normativa em ausência/publicação | `SCHEMA` |
| T34 | política `REGRA_EXPLICITA_APROVADA` com regra auditável | APROVADO |
| T35 | `indeterminado_vira_false=true` | `SCHEMA` / gate estruturado |
| T36 | caminhos positivos `CANDIDATO_PRODUTO → EM_VALIDACAO_GOVERNANCA → PUBLICADO` | APROVADOS |
| T37 | propriedade material desconhecida | `SCHEMA` |
| T38 | YAML/JSON com chave duplicada | erro de carga fail-closed |
| T39 | CLI válido/inválido e tentativa de `--catalog-ref` não contratada | exit 0/1/2 |
| T40 | gate estrutural do repositório | `tools/validate_assistant.py` sem FAIL |
| T41 | CI agregado da PR | regressão zero no head final técnico |
| T42 | política `material-text`: marcas/formatos/whitespace/pontuação/símbolo isolados | `SCHEMA` |
| T43 | materialidade Unicode positiva (`é`, CJK, algarismos Unicode, Devanagari, combining mark com base material) | APROVADO |
| T44 | proveniência de topo e gates materiais usam a mesma política Unicode | rejeição/aceite coerentes |
| T45 | regras de evidência, hipótese/resultado experimental, resumo de validação e motivo operacional não materiais | `SCHEMA` / gate fail-closed |
| T46 | os mesmos campos normativos com conteúdo Unicode legítimo multilíngue | APROVADO |
| T47 | textos obrigatórios adicionais com conteúdo não material que ainda satisfaz `minLength` | `SCHEMA` |
| T48 | os mesmos campos adicionais com conteúdo Unicode legítimo multilíngue | APROVADO |
| T49 | todo `type=string` + `minLength` possui `material-text` | invariável estrutural fail-closed |
| T50 | qualquer `pattern` do schema pertence à allowlist estrutural exata por path + regex | invariável estrutural |
| T51 | nó sintético `string + minLength + pattern: .*\\S.*` sem `material-text` | detectado como violação |
| T52 | default-ignorables dentro de palavra em semânticas equivalentes | `AMBIGUOUS_BINARY_SEMANTICS` |
| T53 | `type=[string]` / `[string,null]` + `minLength`, inclusive aninhado | detectado pelo guard |
| T54 | NaN/±Infinity em limiar/peso e constantes JSON não padrão | `SCHEMA` / carga fail-closed |
| T55 | fillers/default-ignorables Unicode (`U+115F/U+1160/U+3164/U+FFA0`) como texto material | `SCHEMA` / `_has_material_text=False` |
| T56 | equivalência editorial com invisíveis em múltiplas posições + pares distintos por operador/diacrítico | invisíveis equivalentes; diferenças semânticas preservadas |
| T57 | inteiro finito acima do intervalo de float + tipos numéricos externos | inteiro aceito; tipos externos rejeitados deterministicamente |
| T58 | aprovação humana final durante validação pendente ou sem metadados | `VALIDATION_HUMAN_GATE` |
| T59 | política de publicação antecipada com proveniência intrinsecamente inválida | `PROV_APPROVAL_REQUIRED` |
| T60 | experimento não `EXECUTADO` com resultado observado material | `EXPERIMENT_RESULT` |
| T61 | CLI sem/com `--previous` | `SNAPSHOT_VALIDO/HISTORICO_NAO_CERTIFICADO` vs `APROVADO_EVOLUCAO` |
| T62 | perfil canônico de autoria do schema | recusa `allOf`/`oneOf`, `anyOf` fora da allowlist e constraints irmãs de `$ref` |
| T63 | `np.float64(1.5)` fornecido diretamente em limiar e peso | `SCHEMA`; tipo numérico externo recusado deterministicamente |

A suíte canônica `tools/tests/test_micromodelo_mm01.py` contém **47 métodos de teste**; alguns métodos percorrem múltiplos casos/subtests da matriz. A regressão permanente `tools/tests/test_micromodelo_mm01_r03.py` adiciona **1 método dedicado** ao achado R03 da auditoria final, exercitando `np.float64` tanto em limiar quanto em peso. O workflow MM01 executa, portanto, **47 + 1** métodos permanentes. `casos_invalidos.json` mantém nove mutações negativas determinísticas além dos casos adversariais construídos diretamente pelas suítes.

## Teste específico de YAML

O template não usa chaves literais `true:`/`false:`. PyYAML pode interpretar essas palavras como booleanos; por isso o contrato usa `quando_true`, `quando_false` e `quando_indeterminado`.

Além disso, o carregador customizado rejeita chaves duplicadas em YAML e JSON. A MM01 não aceita o comportamento “última chave vence”, porque uma especificação material poderia aparentar um valor na revisão humana e efetivamente validar outro.

## Regressões de materialidade Unicode

As auditorias exploratórias demonstraram que categorias Unicode e listas manuais de code points não bastam para materialidade. A suíte cobre marcas, variation selectors e fillers como U+115F/U+1160/U+3164/U+FFA0. A autoridade agora usa a propriedade Unicode `Default_Ignorable_Code_Point`: após NFKC e remoção desses caracteres, precisa restar letra ou número Unicode. Os positivos multilíngues continuam protegidos.

## Semântica executável sem regex de intenção

A segunda A1 também demonstrou que listas abertas de verbos/sinônimos não conseguem garantir coerência semântica. A correção removeu esse mecanismo:

- `classificacao.ausencia_evidencia` é estruturada por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência;
- `saida.publicacao.politica_indeterminado` não possui descrição normativa livre; `indeterminado_vira_false=false` é estrutural;
- `score.tipo_semantica` é a autoridade executável; `score.semantica` livre deixou de fazer parte do schema;
- `score.normalizacao` é um objeto estruturado, não uma frase livre.

Os testes verificam tanto os caminhos positivos quanto tentativas de reintroduzir os campos livres legados, que devem falhar com `SCHEMA`.

## Matriz de aceite final e condição de término

A oitava A1 (`NAO_APTA`) foi preservada em `10_resultado_a1_reauditoria_7.md`. O contraditório posterior congelou `MATRIZ_ACEITE_FINAL.md` para separar requisitos materiais de hardening e adversariais fora do threat model. As regressões T55–T62 exercitam diretamente R01–R08 no conjunto canônico.

A auditoria final fechada posterior foi executada sobre `337055d70a28c6d595594fa1e8c351a47615e66b` e está preservada em `11_resultado_a1_reauditoria_8.md`. Ela identificou a violação R03 por `np.float64` e o `behind_by=4` como bloqueios independentes. T63 e a suíte dedicada tornam a primeira violação regressiva; a reconciliação com `main` trata o segundo gate. A candidata corrigida precisa agora de **reauditoria final independente contra a mesma matriz congelada**. O threat model não é reaberto: suporte positivo a `Decimal`/NumPy, resolução universal de composição JSON Schema e coerções históricas YAML 1.1 continuam não requisitos.

## Fixtures

`tools/tests/fixtures/micromodelos_mm01/` contém:

- `valido_validado.json`: caso completo em fase `VALIDADO`;
- `casos_invalidos.json`: nove mutações negativas aplicadas à base válida.

Os testes adversariais adicionais criam cópias em memória para evitar inflar fixtures com variações mecânicas.

## Evidências históricas preservadas

### Materialização inicial — failure de transporte

- run `34899029039`;
- **failure** antes da instalação/testes por corrupção do pacote gzip usado como transporte transitório;
- nenhum artefato de produto foi publicado por essa execução;
- a falha é histórica e não foi reclassificada como teste funcional.

### Primeira A1 — `NAO_APTA`

A primeira auditoria independente encontrou cinco bloqueios procedentes: rewind pós-`PUBLICADO`, referências semanticamente vazias, gate prematuro para `PROPOSTO`, contradição de `INDETERMINADO` por prosa e `evidencia_ref` de calibração órfã. O relatório permanece versionado em `03_resultado_a1.md`.

### Reteste das correções da primeira A1

- run transitório final `34909835696`: **success**;
- 24 métodos: `OK`;
- gate estrutural: `APROVADO`, zero falhas/avisos;
- mecanismos transitórios removidos antes da publicação.

### Segunda A1 — `NAO_APTA`

A reauditoria independente sobre `2783bcbd6ad7f07f9f3893c66c9dc36d0557f57e` encontrou três novos bloqueios procedentes:

1. marcas Unicode `M*` ainda satisfaziam provas auditáveis;
2. proteção `FALSE` × `INDETERMINADO` ainda dependia de regex sobre prosa livre;
3. interpretação probabilística ainda podia escapar por sinônimos não cobertos.

O relatório histórico está versionado em `04_resultado_a1_reauditoria.md` e não será reclassificado.

### Reteste das correções da segunda A1

- workflow transitório `34912665666`: **success**;
- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`: **26 métodos, OK**;
- `python -B tools/validate_assistant.py --root ambiente_fonte`: **APROVADO, 0 falhas, 0 avisos**;
- script e workflow transitórios foram removidos antes do commit permanente `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`;
- a correção não introduziu fingerprint, crawler, MLflow definitivo, publicação real, visual próprio ou migração.

O run transitório é evidência de construção, não substitui os workflows permanentes da candidata documental final. Os IDs dos checks permanentes do HEAD congelado são mantidos na conversação da PR #51 para evitar commits autorreferentes.

## Terceira A1 — `APTA_COM_CORRECOES`

A terceira auditoria independente concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, e registrou três divergências bloqueantes de materialidade textual/Unicode:

1. `$defs.material_ref` impunha ASCII no schema enquanto o validador aceitava letra/número Unicode;
2. `proveniencia.pedido_original_ref`, `proveniencia.gerado_por` e `proveniencia.registros[].alvo` escapavam da política material;
3. semânticas obrigatórias, critérios, nomes de fonte e campos de saída podiam satisfazer gates com whitespace, zero-width, pontuação ou símbolos sem conteúdo material.

O resultado histórico está versionado em `05_resultado_a1_reauditoria_2.md` e permanece `APTA_COM_CORRECOES`, independentemente das correções posteriores.

### Reteste das correções da terceira A1

O mecanismo transitório foi executado novamente no run `34955861169`. Antes de publicar qualquer artefato permanente, ele removeu seus próprios arquivos e concluiu com sucesso:

- instalação por `python -m pip install -r tools/requirements-dev.txt`;
- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`, com **29 métodos**;
- CLI direta sobre template, fixture positiva, caso Unicode positivo, caso Unicode negativo e continuidade por `--previous`;
- `python -B tools/validate_assistant.py --root ambiente_fonte`;
- publicação do commit permanente `4f686e5de163b649c4ee5e7643f75ecd56db47e7`.

Esse reteste é evidência de construção. A candidata documental final ainda precisava dos workflows permanentes verdes no SHA exato e de auditoria independente.

## Quarta A1 — `APTA_COM_CORRECOES`

A quarta auditoria independente sobre `c0b6f5872f47f8e37ed8f55f262c276b8c105063` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com uma divergência bloqueante: a autoridade comum `material-text` já era única, porém campos normativos/materialmente decisivos equivalentes ainda dependiam apenas de `minLength` ou `.strip()`.

O achado alcançou `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e `identidade.estado.motivo_condicao`. O resultado histórico está preservado em `06_resultado_a1_reauditoria_3.md` e não é reclassificado pelas correções posteriores.

### Reteste das correções da quarta A1

A correção reutilizou exclusivamente a autoridade existente `material-text` → `_has_material_text`:

- os seis campos citados passaram a usar `format: material-text` no schema;
- os gates semânticos de resultado `EXECUTADO` e motivo de condição não `ATIVO` deixaram de usar `.strip()` e passaram a chamar `_has_material_text`;
- a suíte ganhou adversariais permanentes para `Mn`, `Mc`, `Me`, `Cf`, zero-width, espaços Unicode, pontuação, símbolos e combinações, além de caminhos positivos multilíngues.

O run transitório `34960256357` removeu seus próprios mecanismos e concluiu com sucesso **31 métodos**, CLI direta positiva/negativa/`--previous`, `validate_assistant`, métrica congelada e invariantes históricos antes de publicar o commit permanente `8fd8e7892ead1bb63a554b5283f7062adf582976`.

## Quinta A1 — `APTA_COM_CORRECOES`

A quinta auditoria independente sobre `0b7a712cd2c897483da34517f10516012711f153` concluiu `APTA_COM_CORRECOES`, sem `QUEBRA`, com `DIVERGE-01` bloqueante: campos centrais ainda podiam satisfazer `minLength` usando apenas pontuação, zero-width, marks, whitespace ou símbolos. O resultado histórico permanece em `07_resultado_a1_reauditoria_4.md` e não é reclassificado por correções posteriores.

### Correção da quinta A1

A correção fecha a classe de defeito: textos obrigatórios com `minLength` precisam usar `material-text`, `pattern` ou constar na exceção narrativa explícita `governanca.observacoes[]`. `_has_material_text` e o `FormatChecker` não foram alterados. A suíte passa a **34 métodos**, com adversariais que deliberadamente excedem `minLength` usando conteúdo não material e positivos multilíngues.

## Próxima auditoria A1

Uma **sexta A1 independente** era obrigatória porque a candidata havia mudado materialmente depois da quinta A1. Esse registro é histórico; a sexta A1 foi executada e está descrita abaixo.

## Sexta A1 — `APTA_COM_CORRECOES`

A sexta auditoria independente identificou duas divergências bloqueantes preservadas em `08_resultado_a1_reauditoria_5.md`: três regex genéricas `.*\S.*` ainda coexistiam com `material-text`, e o guard estrutural aceitava qualquer `pattern` como política suficiente.

### Correção da sexta A1

- removidos os três `pattern: ".*\\S.*"` concorrentes de proveniência/aprovação;
- todo `type=string + minLength` passa a exigir `format: material-text`;
- os patterns remanescentes são congelados por allowlist exata de path + regex e correspondem somente a ID interno, nome técnico e versão;
- um adversarial sintético prova que `minLength + pattern: .*\\S.*` sem `material-text` não satisfaz a invariável;
- a suíte passa a **36 métodos**, preservando os adversariais Unicode e os caminhos positivos multilíngues.

## Sétima A1 — `APTA_COM_CORRECOES`

A sétima auditoria independente sobre `9e3ce44ae0750321802b95d96ff43bb29468eab2` encontrou três divergências bloqueantes: caracteres Unicode default-ignorable podiam mascarar equivalência `FALSE` × `INDETERMINADO`; o guard de `string + minLength` ignorava `type` em array; e NaN/±Infinity atravessavam limiares/pesos. O relatório histórico permanece em `09_resultado_a1_reauditoria_6.md`.

As regressões adicionadas após o contraditório cobrem os três vetores: default-ignorables em posição interna, arrays de tipos e branches aninhados, além de valores não finitos via objeto Python, YAML e constantes JSON permissivas.

## Oitava A1 — `NAO_APTA` e contraditório de escopo

A oitava auditoria independente sobre `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630` encontrou seis `QUEBRA`, dois `DIVERGE` bloqueantes e uma melhoria; o resultado histórico permanece em `10_resultado_a1_reauditoria_7.md`. O contraditório confirmou defeitos materiais, mas classificou suporte positivo a tipos numéricos externos, resolução universal de JSON Schema e coerções YAML 1.1 como fora do gate final.

A matriz final congelada levou a suíte de 39 para **47 métodos**. O run de construção correspondente permanece como evidência técnica da correção.

## Auditoria final fechada — `NAO_APTA_PARA_FECHAMENTO_DOCUMENTAL`

A auditoria final fechada sobre `337055d70a28c6d595594fa1e8c351a47615e66b` foi a primeira aplicação integral da matriz congelada como gate de encerramento. O relatório preservado em `11_resultado_a1_reauditoria_8.md` identificou:

- **B01 / R03:** `np.float64(1.5)` era aceito pela API direta por causa de `isinstance(value, float)`;
- **B02 / gate final:** a branch estava `behind_by=4` contra a `main` vigente.

A correção B01 troca classificação por subtipo por identidade estrita do domínio Python canônico e adiciona T63 em suíte dedicada. A correção B02 reconcilia a branch por merge real com a `main` vigente. Nenhum desses reparos reabre a matriz ou promove o `BACKLOG_HARDENING` editorial a requisito.

## Reteste da correção final

O gate permanente MM01 executa agora, em sequência:

- os **47 métodos** da suíte canônica;
- **1 regressão R03** dedicada para `np.float64` em limiar e peso;
- `validate_assistant.py --root ambiente_fonte`;
- fronteira read-only, sem Databricks/Unity Catalog/MLflow/ACL/dado corporativo/publicação externa.

A correção técnica e a reconciliação já foram certificadas em runner real antes desta sincronização documental. Como a documentação atual altera o HEAD, a árvore resultante deve ser recertificada integralmente. Depois disso, o próximo gate é uma **reauditoria final independente**, contra a mesma matriz congelada, antes de qualquer atualização do `CHANGELOG.md`, aceite ou merge.

**MM02 permanece bloqueada.**
