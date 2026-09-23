# Resultado da auditoria A1 final — MM01 — reauditoria 8

## 1. Identificação

| Item | Estado auditado |
|---|---|
| Repositório | `Guimarais-R-Rodrigo/Ambiente_Databricks` |
| Branch | `micromodelos/mm01-contrato-canonico` |
| PR | `#51` |
| HEAD esperado | `337055d70a28c6d595594fa1e8c351a47615e66b` |
| HEAD real auditado | `337055d70a28c6d595594fa1e8c351a47615e66b` |
| `main` vigente na reconfirmação final | `c339ed177f4b901a907ea6ad43f0803f5b7ccc09` |
| merge-base | `a6309a4d0b3a3530c52330e65ee5a18674118378` |
| `ahead_by` contra `main` vigente | `120` |
| `behind_by` contra `main` vigente | `4` |
| Status da comparação | `diverged` |
| Commits da PR | `120` |
| Arquivos alterados | `27` |
| Estado da PR | aberta; `merged=false`; `draft=false` |
| Mergeabilidade atual | `mergeable=false`; `rebaseable=false`; `mergeable_state=dirty` |
| merge-ref observado | `5694c05da90decbdddbce2f4541016f37067eaca` |
| Equivalência HEAD × merge-ref armazenado | mesma árvore `c6267b03da27ceb5920638a413a5e8b07ae5dbba`; sem diferença material de conteúdo entre aquele merge-ref e o HEAD |

Há uma distinção importante: o merge-ref armazenado foi criado como merge de `337055d…` sobre a antiga base `a6309a4…`, e não sobre a `main` atual `c339ed1…`. Portanto, sua equivalência material com o HEAD não demonstra compatibilidade com a `main` vigente. A comparação final com a `main` atual permanece divergente, com `behind_by=4`. A matriz exige explicitamente `behind_by=0`.

Ambiente limpo observado no GitHub Actions do próprio HEAD: Ubuntu 24.04.5, CPython 3.12.14, `jsonschema 4.26.0`, PyYAML 6.0.3, `regex 2026.9.10` e NumPy 2.5.3. O job funcional `validar-mm01` executou checkout, instalação, testes MM01 e gate estrutural, concluindo `success`.

O runner local usado para adversariais adicionais tinha Python 3.13.5, Linux x86_64, `jsonschema 4.26.0`, PyYAML 6.0.3, `regex 2026.5.9` e NumPy 2.3.5. O checkout Git direto não pôde ser repetido localmente porque esse runner não resolveu `github.com`; por isso, para a árvore completa, usei o HEAD exato obtido pelo conector GitHub e a execução limpa do Actions. Essa limitação não afetou a inspeção do código nem o adversarial bloqueante descrito abaixo.

## 2. Autoridades normativas utilizadas

A autoridade primária foi `docs/sprints/micromodelos/MM01/MATRIZ_ACEITE_FINAL.md`. A própria matriz declara-se congelada e restringe a auditoria a requisitos já assumidos, além de definir a API Python canônica e afirmar expressamente que tipos numéricos externos, incluindo escalares NumPy, devem ser recusados deterministicamente.

Foram lidos, na ordem prescrita:

1. `docs/sprints/micromodelos/MM01/MATRIZ_ACEITE_FINAL.md`;
2. `docs/auditoria/2026-09-14_micromodelos-mm01/01_contexto.md`;
3. `docs/auditoria/2026-09-14_micromodelos-mm01/02_prompt_auditoria.md`.

Também foram identificados e lidos os ADRs aceitos materialmente aplicáveis à MM01:

- ADR-0014 — micromodelo como artefato de domínio, sem criar sétimo tipo do Hub;
- ADR-0015 — YAML canônico e estados/proveniência;
- ADR-0016 — histórico de runs fora do YAML e contrato definitivo de tracking postergado;
- ADR-0017 — autoridade de publicação `GOVERNANCA_EXTERNA`;
- ADR-0018 — piloto greenfield antes de migração de legados;
- ADR-0019 — consumo do sistema existente de temas;
- ADR-0020 — fontes restritas ao binding simbólico autorizado, sem descoberta corporativa real.

Os relatórios `03_resultado_a1.md` a `10_resultado_a1_reauditoria_7.md` não foram usados para formar a conclusão, classificar os adversariais nem chegar ao veredito preliminar. Eles só foram consultados posteriormente para a verificação histórica da seção 10 deste relatório.

## 3. Execuções reproduzidas

| Execução | Resultado | Evidência objetiva |
|---|---|---|
| Instalação de `tools/requirements-dev.txt` no runner limpo | PASS | step real de instalação no job MM01 do HEAD |
| `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v` | PASS | 47 métodos, `OK` |
| `python -B tools/validate_assistant.py --root ambiente_fonte` | PASS | `0 falha(s), 0 aviso(s)` |
| `validate_assistant.py --conferir-readme` | PASS | executado no job funcional V12 antes do gate de escopo |
| Schema Draft 2020-12 | PASS | schema carregado/validado pela suíte e inspeção independente |
| Template MM01 | PASS | caminho positivo coberto |
| Fixture positiva `valido_validado.json` | PASS | caminho positivo coberto |
| Documentos inválidos | PASS | rejeitados pela suíte |
| Snapshot sem `--previous` | PASS | garantia de snapshot é distinguida de histórico certificado |
| Evolução válida com `--previous` | PASS | aprovada |
| Rewind/evolução inválida com `--previous` | PASS | rejeitada |
| Adversariais Unicode R01/R02 | PASS | comportamento compatível com política congelada |
| Adversariais numéricos R03 | FAIL parcial | `np.float64` revelou violação não coberta pela suíte |
| Mutações sintéticas R08 | PASS | guards detectaram as regressões do perfil de autoria |

O workflow MM01 é efetivamente read-only: `permissions: contents: read`, checkout com `persist-credentials: false` e Python 3.12.

A existência de 47 testes verdes não é suficiente para eliminar o finding R03: a própria suíte cobre `Decimal`, `np.float16` e `np.float32`, mas não inclui `np.float64`.

## 4. R01–R08

| Requisito | Resultado | Evidência | Bloqueio? |
|---|---|---|---|
| R01 — materialidade textual Unicode | PASS | `_has_material_text` exige `str`, aplica NFKC, remove `Default_Ignorable_Code_Point` e procura categoria Unicode `L*`/`N*`; adversariais com fillers, variation selectors, zero-width, whitespace, combining isolado e símbolos foram recusados; português acentuado, CJK, Devanagari, árabe, grego, cirílico, dígitos e combining legítimo foram preservados. | Não |
| R02 — equivalência editorial conservadora | PASS | NFKC + `casefold` + remoção de DICP + whitespace; diferenças em diacríticos, operadores e pontuação interna permaneceram distintas. | Não |
| R03 — números materiais finitos | FAIL | `np.float64(1.5)` é aceito pela API/schema porque `_check_finite_number_format` usa `isinstance(value, float)`; a matriz determina recusa determinística de tipos numéricos externos. | Sim — MATRIX_VIOLATION |
| R04 — decisão humana | PASS | aprovação/reprovação final exige metadados completos; decisão final é incompatível com `PENDENTE`/`EM_ANALISE`; troca isolada da string de status não fabrica aprovação | Não |
| R05 — proveniência | PASS | invariantes de `APROVADO` e `MEDIDO` são locais e aplicadas quando o bloco existe, inclusive em `saida.publicacao.politica_indeterminado` | Não |
| R06 — experimentos | PASS | `EXECUTADO` exige resultado material + proveniência `MEDIDO`; demais estados mantêm `resultado=null` | Não |
| R07 — snapshot × evolução | PASS | ausência de `--previous` não certifica histórico; com previous, identidade, versão, `fase_anterior`, rewind e reescrita histórica são controlados | Não |
| R08 — perfil de autoria JSON Schema | PASS | schema oficial permanece no perfil congelado; mutações com `allOf`, `oneOf`, `anyOf` indevido, `$ref` com constraint irmã, pattern textual e minLength sem política foram detectadas | Não |

A regra executável de R03 é particularmente clara:

- `int` → aceito;
- `float` → `math.isfinite`;
- outros → recusados.

O problema é que essa distinção foi implementada por `isinstance`, não por identidade estrita de tipo. Consequentemente, um objeto NumPy que se apresente como subtipo de `float` atravessa o ramo destinado ao `float` Python.

## 5. Requisitos materiais da seção 11

| Requisito material | Resultado | Evidência |
|---|---|---|
| Draft 2020-12 válido | PASS | schema e suíte compatíveis com `Draft202012Validator` |
| Objetos normativos fechados | PASS | inspeção integral do schema |
| `fase` separada de `condicao` | PASS | contratos distintos |
| Máquina de fases sem saltos não previstos | PASS | gate semântico presente |
| Proveniências `DESCOBERTO/INFERIDO/PROPOSTO/APROVADO/MEDIDO` distintas | PASS | schema e validações locais |
| Ausência/silêncio não vira `FALSE` sem regra aprovada | PASS | política de ausência controlada |
| Score 0–100 não implica probabilidade | PASS | contratos separados |
| Probabilidade exige calibração medida + referência | PASS | gates semânticos presentes |
| Pesos e limiares passam por aprovação quando exigido | PASS | gate formal preservado |
| Referências internas precisam resolver | PASS | integridade referencial validada |
| IDs controlados não colidem | PASS | invariantes de unicidade presentes |
| Chaves YAML/JSON duplicadas são recusadas | PASS | loaders estritos |
| Fontes limitadas a `CATALOGO_PRODUTO` | PASS | binding simbólico preservado |
| Saída publicada permanece BOOLEAN | PASS | schema preservado |
| `INDETERMINADO` possui tratamento explícito | PASS | política de publicação explícita |
| YAML não armazena histórico crescente de runs | PASS | fronteira preservada |
| Tracking definitivo não é antecipado | PASS | MM06 continua responsável pelo contrato futuro |
| Workflow MM01 read-only | PASS | `contents: read`, sem credencial persistida |
| Nenhuma ação corporativa real | PASS | sem leitura corporativa, ACL, publicação ou discovery real |

A matriz mantém explicitamente esses requisitos e, simultaneamente, esclarece que suporte positivo a NumPy/Decimal não é necessário. Isso não elimina a obrigação diferente de R03 de recusar deterministicamente um tipo externo quando fornecido diretamente à API.

As fronteiras da iniciativa também permaneceram preservadas: não identifiquei fingerprint/MM02, crawler/binding real/MM03, skill/MM04, sétimo tipo do Hub, contrato definitivo MLflow/MM06, publicação corporativa, ACL, Unity Catalog real, dados corporativos, migração de legado ou dependência funcional do Databricks no gate MM01. A autoridade de publicação permanece `GOVERNANCA_EXTERNA`.

## 6. Casos adversariais independentes

| Entrada/caso | Resultado observado | Esperado | Requisito | Classificação | Justificativa |
|---|---|---|---|---|---|
| fillers/DICP repetidos para satisfazer `minLength` | rejeitados | rejeitar | R01 | Conforme | não constituem materialidade |
| DICP no início/fim/interior de texto legítimo | texto continua material | aceitar | R01 | Conforme | DICP é removido antes da decisão |
| whitespace, combining isolado, pontuação/símbolo apenas | rejeitados | rejeitar | R01 | Conforme | nenhuma categoria `L*`/`N*` |
| português, CJK, Devanagari, árabe, grego, cirílico, dígitos Unicode | aceitos | aceitar | R01 | Conforme | positivos legítimos |
| diferenças de caixa/whitespace/DICP/pontuação editorial terminal | canonicalizadas como equivalentes | equivalência | R02 | Conforme | maquiagem editorial |
| `pode` × `pôde`, `>` × `<`, `≥` × `≤`, `+` × `-`, pontuação interna | permanecem distintos | distinção | R02 | Conforme | semântica linguística/operadores preservados |
| `"?true"` × `"true"` | canonicalizados como equivalentes pela remoção de pontuação também na borda inicial | matriz só especifica tolerância terminal, sem comportamento concreto para este caso | R02 | `BACKLOG_HARDENING` | comportamento merece eventual estreitamento, mas não há texto normativo suficiente para bloqueá-lo |
| `10**309` e inteiro ainda maior | tratados sem `OverflowError` | determinístico | R03 | Conforme | não há conversão obrigatória a float |
| `NaN`, `+Inf`, `-Inf` Python/YAML; constantes JSON não finitas | rejeitados | rejeitar | R03 | Conforme | finitude respeitada |
| `Decimal("1.5")` | rejeitado | rejeitar | R03 | Conforme | tipo externo |
| `np.float32(...)` / `np.int64(...)` | rejeitados | rejeitar | R03 | Conforme | tipos externos |
| `np.float64(1.5)` | aceito; zero erro de formato/schema no caminho reproduzido | rejeitar deterministicamente | R03 | `MATRIX_VIOLATION` | `np.float64` alcança o ramo `isinstance(value, float)` |
| aprovação final sem `por`/`em_utc`/`referencia` | rejeitada | rejeitar | R04 | Conforme | decisão humana local |
| decisão final com status técnico intermediário | rejeitada | rejeitar | R04 | Conforme | estados incoerentes |
| `MEDIDO` sem medição/execução material | rejeitado | rejeitar | R05 | Conforme | proveniência intrínseca |
| `PROPOSTO` com aprovação ou `INFERIDO` com medição | rejeitado | rejeitar | R05 | Conforme | bloco incompatível |
| experimento não executado com `resultado` material | rejeitado | rejeitar | R06 | Conforme | resultado significa observado |
| snapshot sem previous | válido, mas histórico declarado não certificado | essa distinção | R07 | Conforme | níveis de garantia separados |
| rewind/identidade incompatível/rewrite com previous | rejeitados | rejeitar | R07 | Conforme | evolução certificada |
| `allOf`, `oneOf`, `anyOf` indevido, sibling constraint em `$ref`, pattern textual | guard detectou | detectar | R08 | Conforme | perfil congelado protegido |

A suíte permanente explicita boa cobertura de externos, mas seus casos NumPy são `np.float16(1.5)` e `np.float32(inf)`; `np.float64` não está entre eles.

## 7. CI, workflows e merge-ref

### Checks funcionais reais

Foram observados jobs reais no HEAD `337055d…`. O job MM01 possui `head_sha` correto e todos os steps — checkout, Python, instalação, contrato/mutantes e gate estrutural — concluíram `success`.

Também foram inspecionados jobs reais e verdes de:

- CI local reproduzível;
- V00;
- V01;
- V02;
- V10;
- V11.

Esses resultados foram tratados como execução funcional, não apenas como status agregado.

### Workflow V12

O run funcional V12 executou código. Antes da falha:

- 47 testes específicos V12 passaram;
- 11 testes de evidência real passaram;
- 515 regressões de temas passaram;
- 12 testes visuais/legados passaram;
- `validate_assistant --conferir-readme` passou.

A única falha funcional do job foi o step de higiene/escopo, que marcou arquivos MM01 como `V12_SCOPE_FAIL` por não pertencerem à iniciativa V12.

Classificação:

`EXTERNAL_GATE_INCOMPATIBILITY`

Não há, nesse run, evidência de regressão funcional da MM01 demonstrada por V12. Logo, esse vermelho não é promovido a `MATRIX_VIOLATION`.

### Runs administrativos

Foram encontrados oito runs mais antigos do mesmo HEAD registrados como `failure`, mas cada um foi consultado individualmente e retorna:

`total_count=0`, `jobs=[]`.

Isso foi confirmado para V12, CI local, V10, V00, V11, MM01, V02 e V01.

Classificação:

`HISTORICAL_ADMIN_RUN`

Eles não representam testes funcionais executados.

### Merge-ref

O merge-ref observado é `5694c05…`. Seu commit declara merge de `337055d…` sobre `a6309a4…`, e sua árvore é `c6267b0…`.

O HEAD `337055d…` possui exatamente a mesma árvore `c6267b0…`; portanto, naquele merge-ref histórico, não havia diferença material de conteúdo.

Entretanto, a `main` vigente agora é `c339ed1…`, posterior à base desse merge-ref.

Logo:

- equivalência material do merge-ref armazenado com o HEAD: PASS;
- validade desse merge-ref como teste da integração com a `main` vigente: não aplicável, pois a referência está desatualizada;
- sincronização atual com `main`: FAIL, `behind_by=4`;
- PR atual: `mergeable=false`, `mergeable_state=dirty`.

## 8. Achados bloqueantes

### B01 — `MATRIX_VIOLATION` — R03 aceita `np.float64` diretamente

1. ID do requisito violado: R03 — números materiais finitos no domínio canônico.
2. Arquivo/função/campo: `tools/micromodelo_mm01_contract.py`, `_check_finite_number_format`; reprodução em `classificacao.limiares[].valor`. O mesmo formato também governa `score.componentes[].peso`.
3. Entrada exata: `np.float64(1.5)` em `classificacao.limiares[0].valor` de um documento válido.
4. Procedimento de reprodução: copiar a fixture válida; substituir `classificacao.limiares[0].valor` por `np.float64(1.5)`; executar o mesmo `Draft202012Validator` com o `FormatChecker` da candidata.
5. Resultado observado: o valor atravessa `_check_finite_number_format` pelo ramo `isinstance(value, float)` e não produz erro `finite-number`; no adversarial reproduzido, o schema retorna zero erros para essa substituição.
6. Resultado exigido: recusa determinística do tipo numérico externo.
7. Texto normativo: a matriz estabelece que tipos numéricos externos ao domínio canônico “devem ser recusados deterministicamente em vez de serem interpretados implicitamente”; a seção de entradas suportadas cita explicitamente escalares NumPy.
8. Por que está na superfície suportada: a matriz inclui expressamente o comportamento da API Python direta quando recebe tipos externos. O não requisito é suporte positivo a NumPy; não é permissão para aceitá-lo implicitamente.
9. Código/erro emitido: nenhum erro é emitido. A implementação é `bool → True; int → True; isinstance(value, float) → math.isfinite(value); outros → False`.
10. Impacto concreto: a API direta aceita um escalar NumPy externo como número canônico, contrariando o domínio congelado. O gate permanente não detecta a regressão porque testa NumPy `float16`/`float32`, mas não `float64`.

Conclusão: bloqueio contratual reproduzível.

### B02 — `FINAL_GATE_VIOLATION` — candidata está `behind_by=4`

1. ID do requisito violado: Gate final objetivo, seção 13, item 6.
2. Arquivo/função/campo: estado Git da branch/PR #51 contra `main`.
3. Entrada exata: base `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`; HEAD `337055d70a28c6d595594fa1e8c351a47615e66b`.
4. Procedimento de reprodução: comparar a `main` vigente com o HEAD imediatamente antes do veredito.
5. Resultado observado: `status=diverged`, `ahead_by=120`, `behind_by=4`; merge-base `a6309a4d0b3a3530c52330e65ee5a18674118378`.
6. Resultado exigido: `behind_by=0`.
7. Texto normativo: seção 13 da matriz exige literalmente `behind_by=0 contra a main vigente`.
8. Por que está na superfície suportada: é um gate final explicitamente congelado, não um adversarial novo.
9. Código/estado emitido: comparação GitHub `diverged`, `behind_by=4`; a PR simultaneamente aparece como `mergeable=false`, `rebaseable=false`, `mergeable_state=dirty`.
10. Impacto concreto: mesmo na ausência do finding R03, a candidata não pode ser declarada apta para fechamento documental enquanto não voltar a `behind_by=0` contra a `main` vigente.

Conclusão: bloqueio objetivo de gate final.

## 9. Observações não bloqueantes

### `BACKLOG_HARDENING`

A função de canonicalização editorial usa `strip(_EDITORIAL_EDGE_PUNCTUATION)` e, portanto, remove o conjunto editorial nas duas bordas. Isso faz `"?true"` e `"true"` convergirem. A matriz fala em pontuação terminal, mas não especifica normativamente a semântica de pontuação editorial na borda inicial de uma expressão. Sem texto concreto que imponha um resultado para esse adversarial, ele não foi promovido a bloqueio.

### `EXTERNAL_GATE_INCOMPATIBILITY`

O vermelho atual do job funcional V12 decorre exclusivamente do gate de escopo V12 rejeitando arquivos MM01. Os testes funcionais executados antes dele passaram. Não demonstra violação da matriz MM01.

### `HISTORICAL_ADMIN_RUN`

Os oito runs antigos marcados administrativamente como `failure` possuem `jobs=[]` e não são evidência de execução funcional.

### `OUT_OF_SCOPE_ADVERSARIAL`

Não foram transformados em requisitos retroativos:

- suporte positivo a `Decimal`;
- suporte positivo a escalares NumPy;
- interpretação geral de objetos numéricos externos;
- NLP/equivalência semântica geral;
- resolvedor universal Draft 2020-12;
- descoberta automática de histórico;
- fingerprint, crawler, skill, MLflow definitivo ou binding corporativo real.

A distinção é relevante para o finding R03: suportar NumPy positivamente permanece fora de escopo, mas recusar um escalar NumPy recebido diretamente é requisito textual da matriz.

## 10. Verificação histórica pós-julgamento

Somente após:

- inspeção independente da árvore;
- execução/análise dos gates;
- criação dos adversariais próprios;
- identificação independente do R03;
- constatação independente do `behind_by`;
- formação do veredito preliminar,

foram consultados os artefatos históricos.

Os relatórios anteriores permanecem preservados como documentos separados e vinculados aos HEADs de suas respectivas rodadas. As reauditorias históricas consultadas posteriormente registram, por exemplo, HEADs distintos como `b4717f…`, `259834…` e `fe3a9d…`; seus findings não foram usados para justificar os dois bloqueios desta auditoria.

Nenhum finding histórico foi promovido a requisito novo, e nenhum relatório anterior foi reclassificado.

## 11. Veredito final

`NAO_APTA_PARA_FECHAMENTO_DOCUMENTAL`

Justificativa: existem dois bloqueios independentes contra autoridades congeladas: uma `MATRIX_VIOLATION` em R03, pela aceitação de `np.float64` na API direta, e uma `FINAL_GATE_VIOLATION`, pois a candidata está `behind_by=4` contra a `main` vigente. Os demais R, requisitos materiais e gates funcionais auditados não produziram outro bloqueio.
