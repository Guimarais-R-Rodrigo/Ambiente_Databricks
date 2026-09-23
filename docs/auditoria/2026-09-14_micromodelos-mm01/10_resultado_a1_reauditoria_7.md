# RELATÓRIO DE AUDITORIA A1 — MM01

## 1. Identificação

- Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`
- Branch: `micromodelos/mm01-contrato-canonico`
- HEAD esperado: `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630`
- HEAD auditado: `fe3a9d8b39c0016d9b487036f1d5e3ad38cb2630`
- Diferença entre HEAD esperado e HEAD auditado: nenhuma. O HEAD foi reconfirmado ao final da auditoria.
- HEAD atual de `main`: `28669f99db27cf23df73549297bbf57eda033f58`.
- Merge-base com main: `28669f99db27cf23df73549297bbf57eda033f58`
- `ahead_by`: `109`
- `behind_by`: `0`
- Quantidade de commits da candidata contra `main`: `109`
- Quantidade de arquivos alterados: `25`
- PR #51: `open`
- `merged`: `false`
- `draft`: `false`
- `mergeable`: `true`
- `mergeable_state`: `clean`
- Merge-ref atual: `36e963610163a89490306e15477585be2c6a39d0`
- Árvore do HEAD: `63727743927e10db19a6a00223f3ad07414f5ae0`.
- Árvore do merge-ref: `63727743927e10db19a6a00223f3ad07414f5ae0`. Portanto, a árvore do merge-ref atual é idêntica à árvore candidata.
- Python: runner funcional do HEAD em Python `3.12.14`; micro-harness adversarial independente em Python `3.13.5`, `jsonschema 4.26.0`, PyYAML `6.0.3` e NumPy `2.3.5`.
- Dependências: a instalação de `tools/requirements-dev.txt` concluiu com sucesso no job funcional do HEAD. O arquivo mantém PyYAML como dependência de manutenção e não introduz dependência de Databricks no gate MM01.
- Limitações de ambiente:
  - o sandbox local não conseguiu resolver `github.com`, portanto não foi possível fazer um segundo checkout Git independente autenticado e repetir os quatro comandos canônicos num clone local;
  - os gates integrais da candidata foram inspecionados no job real `35024471935`, executado sobre merge-ref cuja árvore foi verificada como idêntica ao HEAD;
  - os adversariais adicionais foram executados em memória/ambiente efêmero sobre as funções, predicados e fragmentos de schema exatos da candidata;
  - o CLI completo não foi relançado pelo auditor num checkout local; seu caminho positivo e negativo foi, porém, executado como subprocesso pela suíte corrente;
  - nenhum arquivo do repositório foi alterado, criado, commitado ou enviado;
  - relatórios A1 anteriores, `CHANGELOG.md`, documentação narrativa vedada, descrição da PR, comentários e mensagens de commit não foram usados como evidência de conformidade. A delimitação de fontes da auditoria determina expressamente essa independência.

A superfície de CI do HEAD contém sete check-runs funcionais `completed/success`. Foram confirmados também sete workflow-runs administrativos marcados como falha/action-required; todos retornaram `jobs=[]`, portanto não executaram código e não constituem regressão funcional. O workflow permanente MM01 possui somente `contents: read`, `persist-credentials: false` e executa instalação, suíte MM01 e `validate_assistant`.

## 2. Execuções reproduzidas

| ExecuçãoResultadoEvidência objetiva                             |                                    |                                                                                                                                                                           |
| --------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python -m pip install -r tools/requirements-dev.txt`           | PASS                               | Job real `35024471935`, HEAD auditado/árvore equivalente, instalação concluída                                                                                            |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS                               | Job `35024471935`: `Ran 39 tests`, `OK`                                                                                                                                   |
| `python -B tools/validate_assistant.py --root ambiente_fonte`   | PASS                               | Job `35024471935`: `APROVADO`, 0 falhas e 0 avisos                                                                                                                        |
| CLI do template com `--schema`                                  | PASS                               | A suíte corrente executa o CLI por subprocesso e exige `returncode=0`/`APROVADO`; o template canônico mantém `quando_true/false/indeterminado` sem chaves YAML booleanas. |
| `Draft202012Validator.check_schema` sobre o schema corrente     | PASS                               | Teste funcional verde e `$schema` explicitamente Draft 2020-12.                                                                                                           |
| Schema fechado em blocos materiais                              | PASS                               | Inspeção global encontrou `additionalProperties: false` nos objetos normativos relevantes.                                                                                |
| Enumeração de todos os `pattern`                                | PASS                               | Exatamente três: `$defs.id`, `identidade.nome` e `identidade.micromodel_version`; todos estruturais. Nenhum `pattern` textual genérico concorrente com `material-text`.   |
| Check-runs funcionais do HEAD                                   | PASS                               | 7 checks reais, todos `completed/success`                                                                                                                                 |
| Workflow-runs administrativos vermelhos                         | PASS quanto à distinção solicitada | 7 runs consultados; todos `jobs=[]`, sem execução de código                                                                                                               |
| Merge-ref × HEAD                                                | PASS                               | Mesmo tree SHA `63727743927e10db19a6a00223f3ad07414f5ae0`; comparação sem arquivos materiais distintos.                                                                   |
| Micro-harness Unicode/materialidade                             | FAIL                               | Encontrados bypasses reproduzíveis em `material-text` e equivalência semântica                                                                                            |
| Micro-harness `finite-number`                                   | FAIL                               | Encontrados bypasses com `Decimal`/NumPy e `OverflowError` com inteiro finito                                                                                             |
| Micro-harness das composições JSON Schema                       | FAIL                               | Guard de regressão não detecta constraints equivalentes divididos entre `allOf`/`$ref`                                                                                    |
| Micro-harness de loaders YAML/JSON                              | PASS parcial                       | Duplicatas e não finitos usuais fecham corretamente; encontrada ambiguidade de coerção numérica YAML descrita em `MELHORÁVEL-01`                                          |

## 3. Casos adversariais independentes

| CasoResultado observadoCódigo/erroMotivo correto?                                                          |                                                                                       |                                                                        |                                   |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------- |
| U+034F `COMBINING GRAPHEME JOINER` inserido no interior de `disponível`                                    | ACEITO como semanticamente diferente do original                                      | nenhum `AMBIGUOUS_BINARY_SEMANTICS`                                    | NÃO                               |
| U+180B `MONGOLIAN FREE VARIATION SELECTOR ONE` no interior da palavra                                      | ACEITO como semanticamente diferente                                                  | nenhum                                                                 | NÃO                               |
| U+2065 no interior da palavra                                                                              | ACEITO como semanticamente diferente                                                  | nenhum                                                                 | NÃO                               |
| U+115F `HANGUL CHOSEONG FILLER` no início, fim, interior e múltiplas posições                              | ACEITO como diferente em todas essas posições                                         | nenhum                                                                 | NÃO                               |
| Strings constituídas somente por U+115F/U+1160/U+3164/U+FFA0                                               | ACEITAS por `material-text` quando cumprem `minLength`                                | nenhum `SCHEMA`                                                        | NÃO                               |
| Português acentuado, CJK, Devanagari, árabe, dígitos árabe-indianos, grego, cirílico e base+combining mark | ACEITOS por `_has_material_text`                                                      | —                                                                      | SIM                               |
| `"score > 70"` versus `"score < 70"`                                                                       | REJEITADOS como equivalentes                                                          | `AMBIGUOUS_BINARY_SEMANTICS`                                           | NÃO                               |
| `"valor ≥ 10"` versus `"valor ≤ 10"`                                                                       | REJEITADOS como equivalentes                                                          | `AMBIGUOUS_BINARY_SEMANTICS`                                           | NÃO                               |
| `"o modelo pode concluir"` versus `"o modelo pôde concluir"`                                               | REJEITADOS como equivalentes                                                          | `AMBIGUOUS_BINARY_SEMANTICS`                                           | NÃO                               |
| Árabe `عَلَم` versus `عِلْم` no mesmo contexto textual                                                     | REJEITADOS como equivalentes após remoção das marcas                                  | `AMBIGUOUS_BINARY_SEMANTICS`                                           | NÃO                               |
| Schema sintético `allOf: [{type: string}, {minLength: 3}]` sem `material-text`                             | Guard retorna lista vazia; `" "` é aceito pelo Draft 2020-12                          | nenhum                                                                 | NÃO                               |
| Mesmo escape com `type: [string,null]` e `minLength` em outro ramo                                         | Guard não detecta                                                                     | nenhum                                                                 | NÃO                               |
| `$ref` para `$defs` contendo `type:string` + `minLength` no nó chamador                                    | Guard não detecta                                                                     | nenhum                                                                 | NÃO                               |
| `anyOf` contendo `allOf` dividido entre tipo/minLength                                                     | Guard não detecta                                                                     | nenhum                                                                 | NÃO                               |
| `float('nan')`, `float('inf')`, `float('-inf')` diretamente                                                | REJEITADOS                                                                            | `SCHEMA/finite-number`                                                 | SIM                               |
| `Decimal('NaN')`, `Decimal('Infinity')`, `Decimal('-Infinity')`                                            | ACEITOS pelo format checker                                                           | nenhum                                                                 | NÃO                               |
| `numpy.float16/float32` com NaN/±Inf                                                                       | ACEITOS pelo format checker                                                           | nenhum                                                                 | NÃO                               |
| JSON literal `NaN`, `Infinity`, `-Infinity`                                                                | REJEITADOS pelo loader                                                                | `ValueError: constante JSON não finita recusada`                       | SIM                               |
| JSON `1e400`/`-1e400`                                                                                      | Loader gera ±Inf e schema rejeita                                                     | `finite-number`                                                        | SIM                               |
| YAML `.nan`, `.NaN`, `.NAN`, `.inf`, `+.inf`, `-.inf`                                                      | REJEITADOS no schema após parsing                                                     | `finite-number`                                                        | SIM                               |
| `sys.float_info.max`, `-sys.float_info.max`, `10**308`                                                     | ACEITOS                                                                               | —                                                                      | SIM                               |
| Inteiro finito `10**309`                                                                                   | Validação levanta `OverflowError`                                                     | `int too large to convert to float`; CLI terminaria em `ERRO_DE_CARGA` | NÃO                               |
| Remoção de `classificacao.semantica.proveniencia.origem`                                                   | REJEITADA                                                                             | `SCHEMA`                                                               | SIM                               |
| Propriedade extra em objeto material aninhado                                                              | REJEITADA                                                                             | `SCHEMA`                                                               | SIM                               |
| Salto `EM_ESTUDO -> CANDIDATO_PRODUTO`                                                                     | REJEITADO                                                                             | `STATE_TRANSITION`                                                     | SIM                               |
| `VALIDADO` com aprovação humana final sem ator/referência                                                  | REJEITADO                                                                             | `VALIDATION_HUMAN_GATE`                                                | SIM                               |
| `validacao.status=PENDENTE` + `aprovacao_humana.status=APROVADO` + `por/em_utc/referencia=null`            | ACEITO                                                                                | nenhum                                                                 | NÃO                               |
| Ausência de evidência mapeada a `FALSE` sem regra aprovada                                                 | REJEITADA                                                                             | `MISSING_POLICY_APPROVAL`/`MISSING_POLICY_RULE_REF`                    | SIM                               |
| Peso/limiar não aprovado em fase formal                                                                    | REJEITADO                                                                             | `WEIGHT_APPROVAL`/`THRESHOLD_APPROVAL`                                 | SIM                               |
| Proveniência `MEDIDO` com timestamp mas sem `referencia_execucao`                                          | REJEITADA                                                                             | `SCHEMA` ou `PROV_MEASUREMENT_REQUIRED`, conforme a forma              | SIM                               |
| Calibração apontando para experimento existente mas não `EXECUTADO+MEDIDO`                                 | REJEITADA                                                                             | `CALIBRATION_EVIDENCE_REF`                                             | SIM                               |
| Score desabilitado deixando apenas um resíduo material                                                     | REJEITADO                                                                             | `SCORE_DISABLED`                                                       | SIM                               |
| Evidência apontando para fonte inexistente                                                                 | REJEITADA                                                                             | `UNKNOWN_SOURCE_REF`                                                   | SIM                               |
| `catalogo_ref="CATALOGO_PRODUTO\u200b"`                                                                    | REJEITADO por não ser binding exato                                                   | `CATALOG_SCOPE`                                                        | SIM                               |
| `PUBLICADO` com todos os demais gates mas `produto_dados_ref=null`                                         | REJEITADO                                                                             | `PUBLICATION_GATE`                                                     | SIM                               |
| Política de publicação com `indeterminado_vira_false=true`                                                 | REJEITADA                                                                             | `SCHEMA`                                                               | SIM                               |
| Experimento `PROPOSTO` com `resultado` material e proveniência `PROPOSTO`                                  | ACEITO                                                                                | nenhum                                                                 | NÃO                               |
| Fase `VALIDADO` com política de publicação já `APROVADO`, porém `aprovacao=null`                           | ACEITO porque a proveniência só é validada a partir de `CANDIDATO_PRODUTO`            | nenhum                                                                 | NÃO                               |
| Chave YAML duplicada em objeto aninhado                                                                    | REJEITADA pelo loader                                                                 | `ValueError: chave YAML duplicada recusada`                            | SIM                               |
| Chave JSON duplicada em objeto aninhado                                                                    | REJEITADA pelo loader                                                                 | `ValueError: chave duplicada recusada`                                 | SIM                               |
| YAML com chaves literais `true:`/`false:`                                                                  | PyYAML produz chaves booleanas; schema rejeita por required/additionalProperties      | `SCHEMA`                                                               | SIM                               |
| YAML `true:` + `True:`/`yes:`/`on:`                                                                        | Colisão detectada como chave duplicada                                                | `ValueError`                                                           | SIM                               |
| YAML merge key `<<:`                                                                                       | Loader recusa o construtor de merge                                                   | `ConstructorError`                                                     | SIM, em fail-closed               |
| YAML `010`, `012`, `1:20` em número material                                                               | ACEITOS e convertidos respectivamente em `8`, `10`, `80`; JSON equivalente é inválido | nenhum                                                                 | NÃO — risco de coerção silenciosa |
| Rewind de versão já publicada validando **sem** `--previous`                                               | ACEITO se o snapshot corrente declarar uma transição local válida                     | nenhum                                                                 | NÃO                               |
| O mesmo rewind fornecendo o snapshot publicado em `--previous`                                             | REJEITADO                                                                             | `STATE_REWIND`                                                         | SIM                               |
| Mesma fase/mesma versão com `fase_anterior` reescrita e `--previous`                                       | REJEITADA                                                                             | `PREVIOUS_HISTORY_REWRITE`                                             | SIM                               |

O schema corrente realmente usa `material-text` de forma ampla e os testes correntes contêm regressões para parte das famílias Unicode, arrays de tipos e floats não finitos; os bypasses acima exploram classes diferentes das já exercitadas.

## 4. Achados

### [QUEBRA-01] `material-text` considera fillers Unicode invisíveis como conteúdo auditável

- Severidade: BLOQUEANTE
- Arquivo/trecho: `tools/micromodelo_mm01_contract.py`, `_has_material_text()` e `MATERIAL_FORMAT_CHECKER`; campos `format: material-text` do schema.
- Como reproduzir: avaliar `"\u115f"`, `"\u1160"`, `"\u3164"` ou `"\uffa0"` — isoladamente ou repetidos até atingir `minLength`. Após NFKC, o predicado encontra categoria iniciada por `L` e retorna `True`. O Draft 2020-12 com o format checker da candidata aceita essas strings.
- Esperado: caracteres de preenchimento/invisíveis não devem, sozinhos, constituir ator, referência, origem, execução ou texto material.
- Observado: U+115F, U+1160, U+3164 e U+FFA0 satisfazem `_has_material_text`.
- Impacto: blocos `APROVADO` e `MEDIDO` podem receber `por`, `referencia`, `origem` ou `referencia_execucao` visualmente vazios e ainda satisfazer tanto o schema quanto `_validate_provenance`. O problema atinge diretamente auditabilidade humana e proveniência.
- Recomendação: fazer a autoridade textual excluir explicitamente a propriedade Unicode de caracteres default-ignorable/fillers antes da decisão `L/N`, mantendo a mesma autoridade no schema e nos gates imperativos. Adicionar regressões com fillers Hangul e outras categorias invisíveis não `Cf`.

### [QUEBRA-02] A equivalência semântica é simultaneamente burlável por invisíveis e excessivamente destrutiva para semântica legítima

- Severidade: BLOQUEANTE
- Arquivo/trecho: `_is_semantic_default_ignorable()` e `_normalize_semantic_text()` em `tools/micromodelo_mm01_contract.py`.
- Como reproduzir:
  - inserir U+034F, U+180B ou U+2065 no interior de `disponível`; o caractere não é removido pela allowlist atual e vira separador;
  - inserir U+115F; ele permanece no token normalizado;
  - colocar a string resultante de `quando_indeterminado` em `quando_false`;
  - inversamente, comparar `"score > 70"` com `"score < 70"`, `pode` com `pôde` ou palavras árabes distintas apenas por marcas significativas.
- Esperado: alterações puramente invisíveis/editoriais devem continuar equivalentes, enquanto diacríticos e operadores semanticamente significativos não devem ser apagados indiscriminadamente.
- Observado:
  - o bypass invisível produz normalizações diferentes e evita `AMBIGUOUS_BINARY_SEMANTICS`;
  - `>`/`<`, `≥`/`≤`, `+`/`-` e diacríticos semanticamente relevantes são removidos, podendo produzir falsos `AMBIGUOUS_BINARY_SEMANTICS`.
- Impacto: é possível disfarçar `FALSE` como `INDETERMINADO` usando invisíveis não cobertos; em sentido oposto, definições legitimamente diferentes podem ser recusadas. O requisito de distinção semântica deixa de ser confiável.
- Recomendação: redefinir a canonicalização como equivalência editorial conservadora: tratar de forma abrangente caracteres invisíveis/default-ignorable, mas preservar operadores e marcas capazes de alterar significado. Cobrir início, fim, interior e múltiplas posições, além de pares positivos multilíngues semanticamente distintos.

### [QUEBRA-03] `finite-number` não cobre o domínio de `number` reconhecido pelo JSON Schema e falha com inteiros finitos grandes

- Severidade: BLOQUEANTE
- Arquivo/trecho: `_check_finite_number_format()` em `tools/micromodelo_mm01_contract.py`; `classificacao.limiares[].valor` e `score.componentes[].peso`.
- Como reproduzir:
  - passar diretamente `Decimal("NaN")`, `Decimal("Infinity")`, `numpy.float16("nan")`, `numpy.float32("inf")`;
  - todos são aceitos por `jsonschema 4.26.0` como `type:number`, porém o checker retorna antecipadamente `True` porque não são `int`/`float`;
  - passar um inteiro finito de 310 algarismos, por exemplo `10**309`; `math.isfinite()` levanta `OverflowError`.
- Esperado: todo objeto reconhecido pelo JSON Schema como número material deve ter finitude corretamente determinada; números finitos permitidos pelo schema não devem derrubar a validação.
- Observado: números não finitos de subclasses/tipos numéricos escapam e inteiro finito grande quebra a função.
- Impacto: NaN/Inf podem atravessar o contrato por objetos Python, exatamente um dos caminhos exigidos nesta auditoria. Em outro extremo, documento JSON com inteiro finito válido pode produzir `ERRO_DE_CARGA` em vez de validação determinística.
- Recomendação: alinhar o checker ao type checker numérico do `jsonschema`, cobrindo `Decimal`/NumPy e tratando inteiros arbitrariamente grandes sem conversão overflow-prone.

### [QUEBRA-04] `aprovacao_humana.status=APROVADO` pode ser forjado enquanto a validação está pendente

- Severidade: BLOQUEANTE
- Arquivo/trecho: `validacao.aprovacao_humana` no schema e bloco de validação humana em `validate_spec()`. O schema permite `por`, `em_utc` e `referencia` nulos; o gate imperativo só os exige se `validacao.status` já for `APROVADO` ou `REPROVADO`.
- Como reproduzir: partir do template em `IDEIA`/`PENDENTE` e alterar apenas `validacao.aprovacao_humana.status` de `PENDENTE` para `APROVADO`, mantendo `por=null`, `em_utc=null` e `referencia=null`.
- Esperado: a string `APROVADO` jamais deve existir como decisão humana válida sem ator, instante e referência, independentemente da fase.
- Observado: nenhum `SCHEMA` ou `VALIDATION_HUMAN_GATE` é emitido nesse estado.
- Impacto: o YAML canônico pode afirmar aprovação humana sem qualquer evidência auditável, precisamente a classe de falsificação que o contrato deveria impedir.
- Recomendação: validar invariantes internas do bloco `aprovacao_humana` sempre. Se `status` for final, exigir todos os metadados e coerência com `validacao.status`; se a validação continuar pendente/em análise, não aceitar uma decisão humana final contraditória.

### [QUEBRA-05] Anti-rewind e monotonicidade são opcionais porque `--previous` é opcional

- Severidade: BLOQUEANTE
- Arquivo/trecho: `validate_spec(..., previous_spec=None)` e definição CLI opcional de `--previous`. A comparação histórica só é executada dentro de `if previous_spec is not None`.
- Como reproduzir:
  1. considerar um snapshot confiável já `PUBLICADO`;
  2. construir, na mesma versão, um snapshot corrente em fase anterior com um par local de fases permitido;
  3. validar sem `--previous`: somente a transição auto-declarada do snapshot corrente é examinada;
  4. validar exatamente o mesmo documento com o snapshot publicado em `--previous`: surge `STATE_REWIND`.
- Esperado: uma garantia declarada como “PUBLICADO não pode ser rebobinado na mesma versão” não deve poder ser desligada pela simples omissão de uma opção CLI.
- Observado: a proteção histórica só existe quando o chamador voluntariamente fornece o snapshot anterior.
- Impacto: o mesmo documento recebe resultado diferente conforme uma opção não obrigatória. Um rewind silencioso pode obter `APROVADO` em validação standalone.
- Recomendação: separar explicitamente validação estrutural de snapshot de validação certificadora de evolução; para qualquer evolução não inicial, tornar a referência anterior obrigatória/fail-closed ou marcar claramente a validação sem histórico como incapaz de certificar anti-rewind.

### [QUEBRA-06] Proveniência de política de publicação só é validada quando a fase já atingiu `CANDIDATO_PRODUTO`

- Severidade: BLOQUEANTE
- Arquivo/trecho: `saida.publicacao.politica_indeterminado.proveniencia`; `_validate_provenance()` é chamado apenas dentro de `if FASE_ORDEM[phase] >= FASE_ORDEM["CANDIDATO_PRODUTO"]`.
- Como reproduzir: manter fase `VALIDADO`, definir antecipadamente `saida.publicacao` e declarar sua política com `proveniencia.status=APROVADO`, `aprovacao=null`.
- Esperado: o significado operacional de `APROVADO` deve ser uniforme em qualquer bloco que utilize `$defs.proveniencia`.
- Observado: o objeto passa pelo schema e a proveniência não é semanticamente validada antes de `CANDIDATO_PRODUTO`.
- Impacto: o artefato canônico pode armazenar uma política aparentemente aprovada sem decisão auditável. A inconsistência apenas passa a ser detectada numa fase posterior.
- Recomendação: sempre validar a consistência intrínseca de qualquer bloco de proveniência existente; deixar para os gates de fase apenas a exigência adicional de qual status é necessário naquele momento.

### [DIVERGE-01] Experimento não executado pode armazenar `resultado` como se já existisse

- Severidade: BLOQUEANTE
- Arquivo/trecho: loop de `experimentos` em `validate_spec()`. Apenas `EXECUTADO` exige resultado+`MEDIDO`; estados não executados somente são recusados quando a proveniência é `MEDIDO`.
- Como reproduzir: criar experimento `status=PROPOSTO`, `resultado="resultado final observado"` e proveniência `PROPOSTO`.
- Esperado: resultados ainda não executados devem permanecer pendentes. Essa é uma consequência expressa da decisão canônica de separar especificação de operação.
- Observado: o contrato aceita o resultado material.
- Impacto: um resultado pode ser preenchido antes de qualquer execução e sobreviver no `micromodelo.yaml`, contrariando a semântica de ciclo de vida.
- Recomendação: fazer `resultado` permanecer `null` enquanto o experimento não estiver `EXECUTADO`, ou separar formalmente “resultado esperado” de “resultado observado”.

### [DIVERGE-02] Guard de materialidade do schema ainda é burlável por constraints compostos

- Severidade: BLOQUEANTE
- Arquivo/trecho: `_required_minlength_without_material_text()` nos testes MM01. O walker reconhece `type:string` ou arrays contendo `string`, mas só relaciona `type` e `minLength` quando ambos estão no mesmo nó.
- Como reproduzir:
  - `{"allOf":[{"type":"string"},{"minLength":3}]}`
  - `$ref` para um `$defs` contendo `type:string`, com `minLength` no nó chamador;
  - variantes nullable em `anyOf`.
- Esperado: qualquer representação Draft 2020-12 semanticamente capaz de aceitar string material obrigatória sem `material-text` deve ser identificada.
- Observado: os schemas sintéticos são válidos Draft 2020-12, aceitam `" "` e o helper retorna `[]`.
- Impacto: o schema oficial corrente está protegido, mas o guard de regressão que deveria preservar essa propriedade pode permanecer verde após uma refatoração semanticamente equivalente que retire a autoridade textual.
- Recomendação: substituir a análise puramente local de nós por verificação semântica que resolva `$ref` e composição, ou manter uma lista canônica de caminhos materiais e realizar mutantes adversariais sobre o schema resolvido.

### [MELHORÁVEL-01] Loader YAML mantém coerções numéricas YAML 1.1 capazes de alterar valor material

- Severidade: NÃO BLOQUEANTE
- Arquivo/trecho: `_load_yaml_without_duplicate_keys()` herda os resolvers implícitos de `yaml.SafeLoader`. PyYAML é a dependência declarada do gate.
- Como reproduzir: `010` vira inteiro `8`; `012` vira `10`; `1:20` vira `80`. As formas equivalentes nem sequer são JSON válido.
- Esperado: para números materiais como limiares/pesos, seria desejável minimizar coerções lexicais surpreendentes entre loaders.
- Observado: os valores são aceitos já convertidos pelo parser.
- Impacto: risco operacional de um valor visualmente interpretado como decimal chegar ao contrato com outro valor. Não foi encontrada violação explícita de ADR que exija YAML 1.2, por isso não classifico este ponto como bloqueante.
- Recomendação: fixar a semântica lexical numérica aceita, preferencialmente recusando formas YAML 1.1 ambíguas ou adotando resolver YAML 1.2 equivalente, com regressões cruzadas YAML/JSON.

## 5. Cobertura dos critérios

| CritérioStatusEvidência                                                                                            |      |                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------ | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Micromodelo continua artefato de domínio, sem sétimo tipo/skill antecipada                                      | PASS | ADR-0014 mantém explicitamente essa fronteira; `project_policy.py` não inclui `hub-ml-micromodelos` nas skills correntes; os 25 arquivos alterados não criam objeto em `.assistant`. |
| 2. Especificação canônica estruturada compatível com `micromodelo.yaml`                                            | PASS | Schema formal + template YAML presentes e coerentes.                                                                                                                                 |
| 3. Schema Draft 2020-12 e blocos materiais fechados                                                                | PASS | `$schema` correto; inspeção dos objetos normativos confirmou fechamento por `additionalProperties:false`.                                                                            |
| 4. `fase` e `condicao` distintas                                                                                   | PASS | Campos e enums separados no schema e gates próprios no validador.                                                                                                                    |
| 5. Máquina rejeita saltos e permite somente rework previsto                                                        | PASS | Tabela explícita e adversarial `EM_ESTUDO -> CANDIDATO_PRODUTO` rejeitado. A fragilidade histórica sem `--previous` é registrada separadamente no critério 6.                        |
| 6. `PUBLICADO` não pode ser rebobinado na mesma versão                                                             | FAIL | `QUEBRA-05`: com `--previous` bloqueia; sem ele, a garantia desaparece.                                                                                                              |
| 7. Proveniências/estados `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO`, `MEDIDO` têm significado distinto       | FAIL | `QUEBRA-06` e `DIVERGE-01`: há caminhos em que `APROVADO` não passa pelo guard de aprovação e resultado não executado pode ser materializado.                                        |
| 8. `APROVADO` exige decisão humana auditável                                                                       | FAIL | `QUEBRA-01` permite referências/atores invisíveis; `QUEBRA-04` permite `aprovacao_humana.status=APROVADO` sem evidência quando validação não é final.                                |
| 9. `MEDIDO` exige referência de execução                                                                           | FAIL | A estrutura existe e os casos usuais são bloqueados, mas `QUEBRA-01` permite uma `referencia_execucao` composta somente de fillers invisíveis.                                       |
| 10. `FALSE` é distinguível de `INDETERMINADO`                                                                      | FAIL | `QUEBRA-02`: equivalência pode ser burlada com invisíveis internos não cobertos.                                                                                                     |
| 11. Silêncio não vira `FALSE` sem regra explícita aprovada                                                         | PASS | Contrato estruturado distingue `INDETERMINADO` e `REGRA_EXPLICITA_APROVADA`, com `resultado_sem_evidencia` e `regra_ref`.                                                            |
| 12. Score habilitado tem semântica explícita e escala 0–100                                                        | PASS | Estrutura e gates de escala/semântica presentes.                                                                                                                                     |
| 13. Score 0–100 não vira automaticamente probabilidade                                                             | PASS | Semântica probabilística é enum separado e exige calibração.                                                                                                                         |
| 14. Probabilidade exige calibração observada/medida e execução                                                     | FAIL | Estrutura nominal é adequada, mas uma execução `MEDIDO` pode utilizar referência invisível por `QUEBRA-01`, comprometendo a auditabilidade material do gate.                         |
| 15. Pesos/limiares materiais não avançam sem aprovação humana                                                      | FAIL | O gate de status existe, porém `QUEBRA-01` permite tornar a aprovação formalmente completa usando ator/referência invisíveis.                                                        |
| 16. Fontes restritas a `CATALOGO_PRODUTO` e fixtures sintéticos                                                    | PASS | Runtime usa allowlist exata; fixture positiva usa apenas nomes sintéticos.                                                                                                           |
| 17. Referências de evidência/contra-evidência não apontam silenciosamente para fontes inexistentes                 | PASS | Adversarial órfão rejeitado com `UNKNOWN_SOURCE_REF`.                                                                                                                                |
| 18. Estudo preserva `TRUE`, `FALSE`, `INDETERMINADO`                                                               | PASS | `valores_classificacao` é `const` com os três valores.                                                                                                                               |
| 19. Publicação exige BOOLEAN e política explícita de `INDETERMINADO`, sem FALSE implícito                          | PASS | `campo_booleano.tipo=BOOLEAN` e `indeterminado_vira_false` é `const:false`.                                                                                                          |
| 20. Autoridade final de publicação permanece externa                                                               | PASS | `publicacao.autoridade` é `const: GOVERNANCA_EXTERNA`, coerente com ADR-0017.                                                                                                        |
| 21. YAML não armazena histórico crescente de runs                                                                  | PASS | `tracking.armazenar_historico_runs_no_yaml` é `const:false`, coerente com ADR-0016.                                                                                                  |
| 22. Não antecipa fingerprint, crawler, feature engineering, MLflow definitivo, visual, migração ou publicação real | PASS | Superfície alterada limitada à MM01; nenhuma `.assistant` nova; tracking permanece `PENDENTE_MM06`; workflow não acessa infraestrutura real.                                         |
| 23. Testes/fixtures independem de dado, ACL, workspace ou segredo corporativo real                                 | PASS | Fixture é explicitamente sintética e workflow não recebe credenciais corporativas.                                                                                                   |
| 24. Workflow permanente MM01 é read-only e sem ação corporativa                                                    | PASS | `permissions: contents: read`, `persist-credentials:false`; somente dependências, unittest e gate estrutural.                                                                        |

## 6. Veredito

VEREDITO: NAO\_APTA

Bloqueios para aceite:

- `QUEBRA-01` — `material-text` aceita fillers Unicode invisíveis como conteúdo auditável.
- `QUEBRA-02` — normalização semântica ainda admite bypasses invisíveis e produz falsos positivos semanticamente materiais.
- `QUEBRA-03` — `finite-number` aceita números não finitos reconhecidos pelo JSON Schema em tipos não `int/float` e quebra com inteiro finito grande.
- `QUEBRA-04` — aprovação humana pode ser declarada `APROVADO` sem ator/data/referência enquanto `validacao.status` não é final.
- `QUEBRA-05` — anti-rewind é contornável pela omissão de `--previous`.
- `QUEBRA-06` — proveniência de política de publicação pode declarar `APROVADO` sem aprovação antes de `CANDIDATO_PRODUTO`.
- `DIVERGE-01` — resultado material pode existir em experimento não executado, contrariando ADR-0015.
- `DIVERGE-02` — guard do schema não cobre constraints de string/minLength distribuídas por composição JSON Schema válida.

Melhorias não bloqueantes:

- `MELHORÁVEL-01` — eliminar ou explicitar coerções numéricas YAML 1.1 capazes de alterar silenciosamente números materiais.

Condições para reauditoria:

- corrigir todos os seis `QUEBRA`;
- corrigir os dois `DIVERGE` bloqueantes;
- incorporar regressões permanentes para U+034F, U+180B, U+2065, U+115F/U+1160/U+3164/U+FFA0 e posições inicial/final/interna/múltipla;
- incluir positivos que preservem diferenças semanticamente relevantes por diacríticos e operadores;
- testar `Decimal`, `numpy.float16/32`, inteiros finitos acima do intervalo de `float` e todos os caminhos Python/YAML/JSON;
- tornar o guard de materialidade consciente de `allOf`, `anyOf`, `oneOf`, `$defs`/`$ref` e constraints distribuídos;
- adicionar adversariais permanentes para aprovação humana final declarada durante status pendente;
- validar toda proveniência existente independentemente da fase, usando fase apenas para exigir status específico;
- impedir resultado observado em experimento ainda não executado;
- fechar o bypass de evolução sem `--previous` ou deixar de certificar anti-rewind em validação standalone;
- reproduzir novamente os gates canônicos em checkout limpo do novo HEAD;
- reconfirmar `main`, merge-base, `ahead_by`, `behind_by`, PR, merge-ref e superfície de check-runs no momento da nova A1;
- não fazer merge, não fechar `CHANGELOG.md` e não iniciar MM02 antes do contraditório/finalização previstos pela governança.
