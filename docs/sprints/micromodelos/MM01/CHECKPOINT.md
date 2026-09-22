# MM01 — Checkpoint

Status: **NONA REAUDITORIA FINAL INDEPENDENTE `NAO_APTA` PRESERVADA; D-01/R02 CORRIGIDO; SUÍTE PERMANENTE 47 + 3 R02 + 1 R03; RECONCILIAÇÃO COM V13 S2 REALIZADA; CERTIFICAÇÃO DA ÁRVORE FINAL E NOVA REAUDITORIA INDEPENDENTE PENDENTES; NÃO ACEITA; NÃO INTEGRADA**

## Fonte de verdade e estado operacional

- branch: `micromodelos/mm01-contrato-canonico`;
- PR: `#51`;
- matriz final congelada: `docs/sprints/micromodelos/MM01/MATRIZ_ACEITE_FINAL.md`;
- relatório independente mais recente: `docs/auditoria/2026-09-14_micromodelos-mm01/12_resultado_a1_reauditoria_9.md`;
- último HEAD auditado de forma independente: `4dc6bb12d2e4df6c3dbff7aa4711a99bf660bb6b`;
- veredito desse relatório: `NAO_APTA`, exclusivamente pelo `D-01` de R02;
- `CHANGELOG.md`: deliberadamente pré-fechamento; não deve ser sincronizado como conclusão antes de nova reauditoria independente limpa e contraditório final;
- MM02: bloqueada até reauditoria limpa, contraditório, fechamento documental, aceite explícito e integração da MM01.

A `main` avançou durante a correção. A candidata foi reconciliada por merge real com `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`, que incorpora V13 S1 e S2. O merge de reconciliação MM01 é `877a3b9325281de3a276c909cabe6dfed4913b79`. Como outras iniciativas podem continuar avançando em paralelo, `main`, merge-base e `behind_by` precisam ser reconfirmados novamente imediatamente antes do próximo congelamento.

## O que a MM01 entrega

1. schema formal Draft 2020-12, versão `1.0.0`, para `micromodelo.yaml`;
2. template YAML inicial válido e sanitizado;
3. máquina de fases com rework explícito e `PUBLICADO` terminal por versão;
4. distinção entre validação de snapshot e certificação de evolução histórica por `--previous`;
5. condições operacionais ortogonais à fase: `ATIVO`, `BLOQUEADO`, `SUSPENSO` e `DEPRECATED`;
6. proveniência estruturada com invariantes locais;
7. materialidade textual Unicode baseada em NFKC, remoção de `Default_Ignorable_Code_Point` e presença de letra/número Unicode;
8. equivalência editorial conservadora entre `TRUE`, `FALSE` e `INDETERMINADO`, sem equivalência semântica geral;
9. política estruturada de ausência de evidência;
10. política estruturada de publicação de `INDETERMINADO`, com `indeterminado_vira_false=false`;
11. score 0–100 com natureza definida por `tipo_semantica` e normalização estruturada;
12. calibração probabilística dependente de experimento existente, executado e medido;
13. limiares/pesos progressivos antes do gate e aprovados em `EM_VALIDACAO+`;
14. decisão humana final coerente com `validacao.status`;
15. escopo de fontes fail-closed em `CATALOGO_PRODUTO`;
16. recusa de chaves YAML/JSON duplicadas e IDs duplicados em coleções controladas;
17. conteúdo material mínimo ao entrar em `EM_VALIDACAO`;
18. coerência entre fase e status de publicação;
19. tracking de runs mantido fora do YAML, preservando a fronteira com MM06;
20. validador de referência/CI, fixtures sintéticos e suíte permanente;
21. gate `.github/workflows/micromodelos-mm01-ci.yml` read-only, sem acesso ao ambiente corporativo;
22. pacote de auditoria histórico, com relatórios independentes preservados sem reclassificação retroativa.

## Fronteiras preservadas

A MM01 não cria nem antecipa:

- fingerprint ou identidade material da MM02;
- crawler ou binding corporativo real da MM03;
- skill `hub-ml-micromodelos` ou sétimo tipo funcional do Hub da MM04;
- contrato definitivo de MLflow da MM06;
- publicação corporativa real;
- ACL real;
- leitura de dado corporativo real;
- migração de legado;
- integração visual própria.

A autoridade final de publicação continua `GOVERNANCA_EXTERNA`.

## Autoridades congeladas R01–R08

### R01 — materialidade textual Unicode

A autoridade é `_has_material_text` e o formato `material-text`. NFKC é aplicado, `Default_Ignorable_Code_Point` é removido e precisa restar pelo menos uma letra ou número Unicode. Whitespace, pontuação, símbolos, combining marks isolados e fillers invisíveis não satisfazem materialidade por si sós.

### R02 — equivalência editorial conservadora

A normalização autorizada é:

1. NFKC;
2. `casefold`;
3. remoção de `Default_Ignorable_Code_Point`;
4. normalização de whitespace;
5. tolerância somente à pontuação **terminal** explicitamente definida.

Diacríticos, operadores, pontuação interna e pontuação inicial permanecem potencialmente semânticos. A MM01 não tenta resolver equivalência geral de linguagem natural.

### R03 — domínio numérico canônico

A API Python aceita `int` Python e `float` Python finito. `NaN` e `±Infinity` são recusados. Tipos numéricos externos, inclusive escalares NumPy e `Decimal`, não pertencem ao domínio canônico e são recusados deterministicamente.

### R04–R08

- R04: decisão humana é intrinsecamente coerente;
- R05: invariantes de proveniência são locais e sempre válidos;
- R06: resultado observado só existe após execução;
- R07: snapshot e evolução histórica são garantias diferentes;
- R08: o schema oficial segue o perfil de autoria congelado, sem pretensão de resolver toda composição Draft 2020-12.

## Histórico de auditoria preservado

As auditorias anteriores permanecem historicamente verdadeiras no SHA que cada uma julgou. Correções posteriores não reclassificam relatórios antigos.

- A1 inicial: `03_resultado_a1.md` — `NAO_APTA`;
- reauditoria: `04_resultado_a1_reauditoria.md` — `NAO_APTA`;
- rodadas seguintes: `05_resultado_a1_reauditoria_2.md` a `09_resultado_a1_reauditoria_6.md` — `APTA_COM_CORRECOES` nos respectivos SHAs;
- oitava A1: `10_resultado_a1_reauditoria_7.md` — `NAO_APTA`;
- auditoria final fechada: `11_resultado_a1_reauditoria_8.md` — `NAO_APTA_PARA_FECHAMENTO_DOCUMENTAL`;
- nona reauditoria final independente: `12_resultado_a1_reauditoria_9.md` — `NAO_APTA` por R02.

`MATRIZ_ACEITE_FINAL.md` foi congelada após o contraditório da oitava A1 justamente para impedir expansão indefinida do threat model. Um novo adversarial só pode bloquear se demonstrar violação de R01–R08 ou de ADR já aceito.

## Auditoria final fechada anterior — R03 e sincronização

O relatório `11_resultado_a1_reauditoria_8.md`, sobre `337055d70a28c6d595594fa1e8c351a47615e66b`, encontrou dois bloqueios:

1. R03: `np.float64` atravessava o checker por `isinstance(value, float)`;
2. gate final: a candidata estava atrasada em relação à `main` vigente.

As correções foram estreitas:

- `_check_finite_number_format` passou a definir positivamente o domínio por identidade estrita de `int`/`float` Python;
- `tools/tests/test_micromodelo_mm01_r03.py` protege `np.float64` em limiar e peso;
- a branch foi reconciliada por merge real com a `main` então vigente.

R03 permaneceu PASS na nona reauditoria.

## Nona reauditoria final independente — `NAO_APTA`

A nona reauditoria julgou `4dc6bb12d2e4df6c3dbff7aa4711a99bf660bb6b` e encontrou um único bloqueio material:

**D-01 / R02 / DIVERGE / BLOQUEANTE** — `_normalize_editorial_text` usava `strip(_EDITORIAL_EDGE_PUNCTUATION)`, que remove a pontuação configurada nas duas bordas. A matriz, porém, autoriza tolerância somente à pontuação terminal. Como consequência, entradas como `?resultado` ou `…resultado` podiam colapsar indevidamente para a mesma canonicalização de `resultado`, gerando falso `AMBIGUOUS_BINARY_SEMANTICS`.

O relatório está preservado em `12_resultado_a1_reauditoria_9.md` com veredito `NAO_APTA`. A sanitização posterior do identificador do owner e a expansão de um SHA abreviado foram apenas higiene necessária para o gate do repositório; achados, evidências, classificação e veredito não foram alterados.

## Correção D-01 / R02

A correção substitui a remoção bilateral de pontuação por remoção exclusivamente terminal:

```python
normalized = normalized.strip()
return normalized.rstrip(_EDITORIAL_EDGE_PUNCTUATION).rstrip()
```

Isso preserva o restante do contrato R02:

- NFKC continua ativo;
- `casefold` continua ativo;
- DICP continua removido;
- whitespace continua normalizado;
- pontuação terminal configurada continua tolerada;
- pontuação inicial deixa de ser apagada;
- pontuação interna, diacríticos e operadores continuam preservados.

A implementação foi publicada em `b6c266924fcbc387f826c08aa4c0f275746fa5bf`.

## Regressões permanentes após D-01

O gate MM01 executa três conjuntos separados:

- `tools/tests/test_micromodelo_mm01.py`: **47 métodos canônicos** da matriz;
- `tools/tests/test_micromodelo_mm01_r02.py`: **3 métodos dedicados R02**;
- `tools/tests/test_micromodelo_mm01_r03.py`: **1 método dedicado R03**.

A regressão R02 prova simultaneamente que:

- pontuação terminal editorial permanece equivalente;
- `?resultado` permanece diferente de `resultado`;
- `…resultado` permanece diferente de `resultado` após NFKC — NFKC pode representar a elipse como `...`, mas a borda inicial continua materialmente preservada para a canonicalização;
- pontuação inicial não cria falso `AMBIGUOUS_BINARY_SEMANTICS` em validação end-to-end.

No run intermediário `35044200964`, os **47 + 3 + 1 métodos** passaram em Python 3.12.14. O run ainda falhou no gate estrutural exclusivamente porque o relatório histórico recém-preservado continha um identificador pessoal e depois um SHA abreviado que colidia com o detector genérico de higiene. Esses dois pontos documentais foram corrigidos sem alterar o julgamento histórico e precisam ser recertificados na árvore final.

## Reconciliação com V13

Durante esta rodada a `main` avançou primeiro para V13 S1 e depois para V13 S2. A candidata não foi congelada contra uma base obsoleta. Foi criado merge real:

`877a3b9325281de3a276c909cabe6dfed4913b79` — `chore(mm01): reconciliar main apos V13 S2`

O merge possui como pai da `main` `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8` e preserva as mudanças V13 S1/S2 sem reimplementá-las pela MM01.

Logo após a reconciliação, o compare confirmou `behind_by=0`. Isso não elimina a obrigação de reconfirmar a `main` imediatamente antes do próximo congelamento, porque V13 continua evoluindo em paralelo.

## Evidência transitória que não conta como certificação funcional

Foi tentado um workflow corretivo temporário no início da rodada. O run `35043439501` terminou antes de abrir jobs (`jobs=[]`) e não publicou a correção técnica. O mecanismo foi abandonado e removido da árvore. Ele é registro administrativo/transitório, não evidência de falha funcional da MM01.

A correção foi aplicada posteriormente pela API GitHub, protegida pelos workflows permanentes.

## Dívida documental deliberada

O bloco MM01 de `CHANGELOG.md` continua pré-fechamento. Isso é intencional.

Não atualizar o changelog como fechamento enquanto não houver:

1. árvore técnica/documental certificada;
2. nova reauditoria final independente limpa contra a matriz congelada;
3. contraditório final;
4. sincronização byte-preserving do bloco MM01 do changelog;
5. revalidação exata da árvore após essa sincronização;
6. aceite explícito do usuário.

## Gates restantes

A sequência obrigatória é:

1. recertificar todos os workflows aplicáveis na árvore documental final;
2. reconfirmar HEAD, `main`, merge-base, `ahead_by`, `behind_by`, estado/mergeabilidade da PR e merge-ref;
3. exigir `behind_by=0` e equivalência material entre HEAD e merge-ref;
4. congelar o novo SHA candidato;
5. realizar **nova reauditoria final independente**, em contexto separado desta sessão de implementação;
6. executar contraditório final sobre qualquer finding material dentro da matriz;
7. se a reauditoria for limpa, sincronizar somente o bloco MM01 de `CHANGELOG.md`, preservando byte a byte o restante;
8. revalidar a árvore exata resultante;
9. pedir aceite explícito do usuário;
10. somente depois integrar a PR #51.

Enquanto qualquer item estiver pendente, **MM01 não está aceita nem integrada e MM02 permanece bloqueada**.


## Mudança operacional — MM01 Local Certification v1

GitHub Actions não é mais tratado como autoridade executora obrigatória. A mudança é somente do canal de execução da evidência.

Foi introduzido `tools/mm01_local_certify.py` e formalizado `LOCAL_CERTIFICATION_V1.md`. O executor é fail-closed, vinculado ao SHA, exige `behind_by=0`, worktree limpa, runtime controlado, executa os gates derivados dos workflows permanentes e produz bundle probatório com logs, exit codes, snapshots Git, ambiente e SHA-256.

Após a reconciliação operacional desta rodada, a branch absorveu a `main` vigente por merge real `25ca58c4e7d55d4b68caebd3e3f75357599f9e53`. Em seguida, o mecanismo de drift foi endurecido para pin exato dos workflows: `b9bfec9912ea79781eb6e355c881c2f3185acc4d`; as regressões correspondentes entraram em `e4487bec5655baaa05913ffef8f0af547a8a05ce`.

A candidata ainda não está congelada nem certificada localmente. O próximo gate é executar a certificação local sobre o novo HEAD técnico/documental, analisar o bundle e somente então submeter o SHA a auditoria independente.


## Primeira tentativa da certificação local — FAIL-closed

A primeira execução da MM01 Local Certification v1 sobre `5fd97a35426677c296078982bb58479c061d280c` preservou a identidade Git esperada, `behind_by=0`, worktree limpa e equivalência material HEAD × merge-ref, mas terminou antes do primeiro gate por uma incompatibilidade operacional do certifier no Windows.

O executor chamou `npm --version` diretamente via `subprocess.run(..., shell=False)`; no ambiente observado, npm estava disponível por shim `.cmd`, não por `npm.exe`. O bundle retornou `FAIL`, `steps=[]`, sem retry e sem substituição manual dos gates.

A tentativa está preservada em `LOCAL_CERTIFICATION_ATTEMPT_1.md`; SHA-256 do ZIP probatório: `32b7eb9c42b160113d671f331a2ad4a984a2781447bbd640545899e0aa7fc773`.

A correção operacional entrou em:

- `75c24e1649e94b225404ae9b9f23ecaca10980e9` — resolução portável de shims npm/pnpm, registro do comando resolvido e sanitização;
- `7e62ba0f3b9f8d877dfaacad783356661ce3482c` — regressões de resolução Windows/fail-closed/sanitização.

Essa correção não altera R01–R08, schema, contrato MM01 ou gates funcionais. A árvore corrigida ainda precisa de nova reconciliação com a `main` vigente, se houver avanço, e de uma nova certificação integral em diretório de saída novo.


## Segunda tentativa da certificação local — FAIL-closed de precondição

A R2 foi preparada para `b3c7d3c67b0436a060b69c5aac5ec8b0329b64af` contra `main=85474968f5548c13a9a41a3c84f99b3e18f6874c`, mas o `git fetch --all --prune` obrigatório observou `origin/main=17640a6a31f562e9979d235ede27cf44cef9ebbf`.

A candidata passou a `behind_by=7`. A certificação não foi iniciada: sem `--describe`, preflight, steps, bundle ou merge-ref R2. Nenhum arquivo versionado foi modificado localmente.

A tentativa está preservada em `LOCAL_CERTIFICATION_ATTEMPT_2.md`.

Os sete commits novos da `main` alteravam somente `CHANGELOG.md` e documentação SE08; nenhum dos nove workflows-fonte da certificação local mudou.

A reconciliação foi executada por merge real da PR operacional #97, produzindo `0224075a942d60fd5bf71449efbec3784ac10739`. Após a reconciliação, `behind_by=0` e todos os workflow Git blobs continuaram idênticos aos pins do certifier.

A próxima tentativa integral é R3, sobre o HEAD técnico/documental posterior a este registro, condicionada a nova confirmação imediata de `main`, merge-base e `behind_by=0`.


## Terceira tentativa da certificação local — interrupção no bootstrap

A R3 foi executada sobre `8e7c7a8d2b11f83b0d5f558239d881c1ce66cdc6` contra `main=17640a6a31f562e9979d235ede27cf44cef9ebbf`.

Desta vez o preflight canônico concluiu com sucesso:

- `behind_by=0`;
- HEAD/tree/main/merge-base corretos;
- worktree limpa;
- npm resolvido corretamente no Windows via shim `.CMD`;
- nove workflows com blobs iguais aos pins e zero snippets ausentes;
- hashes críticos capturados.

O primeiro step, `BOOTSTRAP_PYTHON`, foi iniciado, mas o processo global terminou com `0xC000013A` / `-1073741510` durante o bootstrap. A origem externa da interrupção não foi determinada. Nenhum gate posterior foi executado.

A tentativa está preservada em `LOCAL_CERTIFICATION_ATTEMPT_3.md` e permanece FAIL. Não houve manifest/postflight/ZIP final; inspeção read-only posterior confirmou worktree e 17 hashes críticos inalterados, sem substituir a exigência de postflight canônico.

O hardening probatório posterior entrou em:

- `72246b7b2a0c21f11ad3a2db2ef1626705ee2e72` — interrupção controlável passa a gerar `StepResult=INTERRUPTED`, log/reason e segue para o fechamento fail-closed quando o processo Python ainda mantém controle;
- `83aa8e6a23d7c3895eb5741ac6639ed96f05ff39` — regressão da interrupção estruturada.

Nenhum gate funcional foi relaxado. A próxima tentativa integral deve usar novo diretório probatório e novo SHA após este registro, condicionado novamente a `behind_by=0`.


### Hardening pós-R3 — streaming probatório

Além da interrupção estruturada, o executor foi endurecido para não bufferizar silenciosamente steps longos:

- `509ba1d30f47d241cfc8a0533e42056026925ead`: tee incremental sanitizado de stdout/stderr para log + console;
- `be9f854d018028949a5aeb5d75ce0cb1cc93c5b9`: regressões do streaming e persistência de output parcial.

Isso não altera gates nem critérios de PASS; reduz apenas a perda de evidência e o silêncio operacional durante bootstraps/testes longos.


## Quarta tentativa da certificação local — FAIL no CI_LOCAL

A R4 foi executada sobre `4cc537f0dd243773a4b250f5912fb7b4027bc6cc` contra `main=17640a6a31f562e9979d235ede27cf44cef9ebbf`.

O preflight passou, a worktree permaneceu limpa e os nove workflow pins coincidiram. Os cinco bootstraps, os 15 self-tests, MM01 canônica (47 testes), R02 (3), R03 (1) e `validate_assistant --root ambiente_fonte` passaram.

O bloqueio ocorreu em `CI_LOCAL`: somente os subgates `validacao` e `sef` falharam, ambos pelo mesmo snapshot stale do `README.md`:

```text
repo (identidade): colado 1638; real 1669
```

No subgate SEF, as 18 etapas anteriores ao `readme_snapshot` passaram. V00/V01/V02/V10/V11/V12/V13 ficaram `NOT_RUN` por fail-closed.

O ZIP R4 é íntegro e possui SHA-256 `2a66d6c5135f3816f25b4b7fd907d3930028428becbbe8e1e0e0c1c761e447a0`.

A tentativa está preservada em `LOCAL_CERTIFICATION_ATTEMPT_4.md` e permanece FAIL.

### Reconciliação posterior

Depois da R4, a PSEF00 foi integrada em `main@11851e137dd7793b351ac08fc211c0be90005dee` pela PR #98, adicionando sete documentos `.md`. A branch MM01 foi reconciliada por merge real da PR operacional #100, commit `1dd69d21d1d28231b92ed34ee654bcab7cee10e2`.

### Hardening secundário

O self-test R4 também revelou `ResourceWarning` não bloqueante no teste de streaming. O pipe passou a ser fechado explicitamente em `0d43519c000e107460f2d36c4aa04b9441d4ce60`; a regressão `46a32fd5ceaaa272911aaa38b67f87f87750381b` transforma novo leak desse tipo em erro de teste.

Nenhum gate funcional foi relaxado.


## Quinta tentativa da certificação local — PASS mecânico, bundle não conforme

A R5 foi executada sobre `3e3e105f60e92f6ca58502cf0c92f4f461a84b04` contra `main=11851e137dd7793b351ac08fc211c0be90005dee`.

O executor terminou com exit code 0, `status=PASS`, `preflight_ok=true`, `postflight_ok=true` e `failure=null`. Todos os 49 steps executáveis passaram e somente `V12_SCOPE_STRICT` foi `SKIP_ALLOWED`. O ZIP `c812454ecd011e99172f802d06ae556c830486fd2afd21bf5aec035bf72cf3fb` teve 54/54 checksums internos válidos.

Os gates MM01 e transversais passaram integralmente, incluindo `CI_LOCAL=PASS`, V00–V13 e snapshot `1677/2109/0`.

A revisão posterior dos bytes do bundle, porém, detectou paths locais do diretório pessoal persistidos em sete logs quando subprocessos imprimiam caminhos Windows em representação escapada. Isso viola as regras de sanitização já declaradas em `LOCAL_CERTIFICATION_V1.md`.

Assim:

- o veredito mecânico do manifest R5 permanece historicamente PASS;
- os gates funcionais R5 permanecem historicamente PASS;
- o bundle R5 não é aceito como bundle final de certificação v1;
- auditoria independente final deve aguardar uma rodada integral com evidência sanitizada.

Correção:

- `cb9f97375e6effaddbfff7569c64c3cafdbce503` — redige variantes literais/normalizadas/escapadas de paths locais;
- `74b0929433a58b4a17959fbb84cc85bb06407127` — regressão das variantes escapadas.

Nenhum gate funcional foi relaxado.
