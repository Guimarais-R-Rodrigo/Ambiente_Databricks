# SER01 — checkpoint A1 para laboratório delegado

## Identidade e autoridade

Base de autoria `dedde0741ed4c387c3a500adfbf7de2c6166aba5`. Branch `ser/SER01-criar-objeto-l3`. Início autorizado em 2026-09-23; promoção L2→L3, merge e SER02 continuam não autorizados. A SER00 foi integrada pela PR #101; frases de pending nos seus documentos de candidata não reabrem a sprint histórica.

ChatGPT mantém arquitetura, implementação e revisão. O executor Cloud recebe somente uma missão delimitada. O prompt anterior que delegava toda a SER01 ao Cloud foi substituído por este modelo; não deve ser usado para ampliar a missão.

## Delta de autoria

Duas ferramentas de código/teste novas, sete documentos SER01 e atualização do índice vivo SER. As rotas existentes do produto e seus manifests permanecem intactos. A entrada do changelog está preparada; o laboratório aplicará essa entrada e atualizará exclusivamente o censo medido do README antes do freeze.

## O que já foi observado

24 testes unitários PASS; sete integrações NOT_RUN/skip explícito. Três cenários externos de orquestração com infraestrutura sintética passaram, sem representar integração canônica. Logs de desenvolvimento mantêm inclusive as duas falhas iniciais de expectativa da allowlist.

## O que o Cloud deve fazer

Obter checkout completo com acesso já autorizado; confirmar identidade/host; preservar trabalho antigo; preparar dependências declaradas; aplicar a entrada e medir snapshot; commit estritamente documental de preparação; congelar SHA limpo; executar a suíte nova e gates canônicos uma vez; preservar qualquer falha e devolver bundle. Não editar implementação, testes, schema, scope, policy ou histórico.

## Critério de parada

Falha de acesso/host material, divergência de main, sujeira não explicada, delta de preparação fora de README/CHANGELOG, falha de teste obrigatório, drift inesperado ou perda de evidência encerram a rodada. Não é permitido alterar expectativas, reescrever lógica ou repetir comandos para alcançar verde. Negativos sintéticos previstos são avaliados pelo seu oráculo, não confundidos com falha da campanha.

## Gate posterior

O retorno do laboratório será auditado aqui. Mesmo com A1-LAB PASS, a SER01 continua em implementação: será necessário ligar a primitive ao fluxo da skill e fechar a prova/identidade prospectiva antes da proposta de promoção. `current_level=L2`, `target_level=L3`, `rollout_mode=audit` permanecem como estão.

## Reconciliação antes da publicação

Durante a autoria, a main avançou de `dedde0741ed4c387c3a500adfbf7de2c6166aba5` para `86d1ff6a52d8ef03f6d5567afed6897c1b96c8c3`, por integração da revisão documental pós-MM01. A comparação mostrou seis commits e onze arquivos documentais, sem mudança de skills, policy, helpers, validators, certifier, testes ou dependências. Todos foram preservados pela construção da candidata diretamente sobre a tree nova. A base inicial acima permanece referência de autoria; a base de integração e do laboratório é `86d1ff6a52d8ef03f6d5567afed6897c1b96c8c3`. Não foi necessário repetir testes de código por esse delta exclusivamente documental. A contagem do README será medida no checkout composto, não herdada da base anterior.

## A1-LAB R1 e corretiva R2 (registro aditivo, 2026-09-23)

```text
A1_LAB_R1_SHA = 5d61b8e52b4c3ebd0d40e142a71de6b5c66869a1
A1_LAB_R1_HOST = Windows 11 / NTFS / Python 3.12.10
A1_LAB_R1_RESULT = FAIL (G1)
A1_LAB_R1_G1 = 31 coletados, 30 executados, 29 PASS, 1 FAIL, 0 SKIP, 1 não iniciado (failfast)
A1_LAB_R1_FAILED_TEST = test_real_script_validation -> BLOCKED CONTENT_REQUIRES_UTF8_LF
A1_LAB_R1_G2_G8 = NOT_RUN_PREVIOUS_GATE_FAILED
CAUSE = fixture positiva de script herdou README legado sem LF terminal
PRODUCTION_VALIDATOR = UNCHANGED
LF_FAIL_CLOSED_RULE = UNCHANGED
LEGACY_SOURCE = UNCHANGED
CORRECTION = canonicalização da fixture positiva apenas (replica() no teste)
R2 = PENDING
CURRENT_LEVEL = L2_UNCHANGED
MERGE = NOT_AUTHORIZED
```

A R1 não é reclassificada por qualquer resultado posterior: pertence ao SHA acima. O fonte `hub_scripts/data_quality_check/README.md` termina sem LF no próprio Git; a fixture positiva é um candidato novo (nome, destino e referências já são trocados) e por isso passa a cumprir também o contrato UTF-8/LF antes de chegar à primitive. Candidatos sem LF continuam `BLOCKED`.

## A1-LAB R2 e corretiva R3 (registro aditivo, 2026-09-23)

```text
A1_LAB_R2_SHA = 4992f10d5892cf804340316cec79e42420097e68
A1_LAB_R2_PUSH = NO (commit apenas local)
A1_LAB_R2_RESULT = FAIL_G1
A1_LAB_R2_G1 = 31 coletados, 30 executados, 29 PASS, 1 FAIL, 0 SKIP, 1 não iniciado (failfast)
R1_FIX = PASS_CAUSALLY_CONFIRMED (envelope aceitou o pacote script)
R2_FAILED_TEST = test_real_script_validation
R2_FAILURE = canonical_public_api
CAUSE = transporte de newline do stdout no Windows (CRLF) versus candidato canônico LF
API_CONTENT_AFTER_CRLF_NORMALIZATION = EXACT_MATCH (152 bytes/7 CR -> 145 bytes = __init__.py)
PRODUCTION_API_TOOL = UNCHANGED (tools/api_publica.py)
CANDIDATE_LF_RULE = UNCHANGED
R3_CORRECTION = CRLF->LF somente no stdout de api_publica na comparação da SER01
R3 = PENDING
CURRENT_LEVEL = L2_UNCHANGED
MERGE = NOT_AUTHORIZED
```

Na R2, o negativo `test_incorrect_public_api_is_rejected_without_repairing_candidate` passava sem discriminar no Windows, porque qualquer fachada reprovava pelo CRLF. A R3 deve mostrar fachada correta PASS e fachada incorreta FAIL no mesmo host. R1 e R2 não são reclassificadas por resultado posterior.

## A1-LAB R3 verde local e reconciliação R4 (registro aditivo, 2026-09-23)

```text
R3_SHA = 101afff9092dd7e8645ef49e131ddb5a24646a77
R3_LOCAL_CERTIFICATION = PASS
R3_G1 = 32/32 PASS
R3_G2_TO_G8 = PASS
R3_FULL_SE08 = 21/21 PASS (HISTORICAL_SE08_REGRESSION)
R3_PUSH = NO
R3_PUBLICATION = BLOCKED_CONCURRENT_REPOSITORY_CHANGE
CONCURRENT_MAIN = 073762fd8e38afadf27aca0f4d77351d9bfb627f
CONCURRENT_FRONT = MM02 / PR #109
OVERLAP = CHANGELOG.md + README.md only
PROTECTED_SER01_PATHS_CHANGED_BY_MM02 = NO
R4 = RECONCILIATION_AND_RECERTIFICATION_PENDING
CURRENT_LEVEL = L2_UNCHANGED
MERGE = NOT_AUTHORIZED
```

O PASS da R3 pertence somente a `101afff9092d` sobre a base `86d1ff6a`. A R4 incorpora a `main` por merge preservador (sem rebase), mantém R1–R3 como ancestrais e exige nova campanha completa sobre o SHA composto antes de qualquer publicação. A matriz de cobertura não é alterada nesta etapa.

## A1-LAB R4 concluída e abertura A2 (registro aditivo, 2026-09-23)

```text
R4_SHA = aef0f10886689a0018635535c0af105e62629de1
R4_RESULT = PASS_RECONCILED
R4_G1 = 32/32 PASS
R4_G2_TO_G8 = PASS
R4_FULL_SE08 = 21/21 PASS (HISTORICAL_SE08_REGRESSION)
R4_PUSH = PASS_FAST_FORWARD
R4_HOST = Windows 11 / NTFS / Python 3.12.10
PR108_AFTER_R4 = OPEN / DRAFT / MERGEABLE
MAIN_AFTER_R4 = 073762fd8e38afadf27aca0f4d77351d9bfb627f
A1_LAB = COMPLETE
A2 = PREPARED_NOT_CERTIFIED
CURRENT_LEVEL = L2_UNCHANGED
POLICY_PROMOTION = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

A R4 prova a validação estrutural local no host Windows/NTFS para snippet, script,
prompt, notebook e README agregador. Não prova execução do notebook, apply desses
tipos, Linux, Databricks Free/Genie ou autenticação humana. A2 liga a superfície
`object_validation` à skill publicada por Receipt de domínio próprio, sem reutilizar
semanticamente o Receipt EDA V1 e sem mudar a policy. O SHA A2 exige nova campanha;
nenhum PASS da A1 é transportado.

## A2-LAB concluída e abertura A3 (registro aditivo, 2026-09-23)

```text
A2_SHA = 8c33a765f9387a743456ea0aba26f3cec63d4421
A2_RESULT = A2_LAB_PASS
A2_G1 = 35/35 PASS
A2_LEGACY_CREATE = 35/35 PASS
A2_CONTRACTS = 5/5 PASS
A2_POLICY = 14/14 PASS; current_level=L2
A2_VALIDATOR = PASS
A2_RENDERER_DRIFT = PASS
A2_CI_LOCAL = 10/10 PASS
A2_FULL_SE08 = 21/21 PASS (HISTORICAL_SE08_REGRESSION)
A2_POSITIVE_RECEIPTS = 5/5
A2_NEGATIVE_RECEIPTS = 2/2 absent
A2_SHARE_MANIFEST = 458/458 hashes and sizes verified independently
A2_PUSH = PASS_FAST_FORWARD
A2_HOST = Windows 11 / NTFS / Python 3.12.10
A2 = COMPLETE
A3_AUTHORING_HEAD = df66c9a21ce2680cf07e08b295072922f87c725a
A3 = PREPARED_NOT_CERTIFIED
CURRENT_LEVEL = L2_UNCHANGED
POLICY_PROMOTION = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

A2 prova a ligação do record repo-side ao Receipt de domínio e seu verifier no host
observado, com replay/tamper/missing Receipt bloqueados. O bundle SHARE é derivado
sanitizado; a autenticidade da execução continua dependendo do RAW/auditoria, não do
hash isolado.

A3 cria a primeira certificação prospectiva SER com identidade `SER-CERT-1` e perfil
`ser01-object-validation-pre-promotion`. Ela exige o record local junto do Receipt,
fecha esse bypass estrutural, reexecuta a rota canônica e mantém o perfil histórico
`se08` apenas como canal separado. A3 não muda policy e exige campanha própria.

## A3 SER-CERT R1 — FAIL de verificação e corretiva R2 (registro aditivo, 2026-09-23)

```text
A3_R1_LOCAL_FREEZE_SHA = 1ff6d563824ecf3dfd80fb86c1420bb46329cf5d
A3_R1_LOCAL_TREE = 704df6500e8f01c35fd660c9d48d512cc9b0c19c
SER_CERT_PRODUCER_STATUS = PASS
SER_CERT_PRODUCER_EXIT = 0
VERIFY_CERTIFICATION = FAIL
FIRST_FAILURE = STEP_SET_INVALID
PUSH = NO
REMOTE_BRANCH_REMAINED = 98c886a972d85c6b0918510f55bb8586e103708b
```

A causa é interna ao certifier, não à rota A2: `_git_state` registrava os oito
probes Git antes e depois com os mesmos nomes na lista única de `steps`, enquanto
`verify_certification` exige unicidade de nomes. Assim uma campanha real completa
produzia 27 steps com oito nomes duplicados, embora todos os gates materiais
tivessem exit 0 e cleanup completo.

A corretiva R2 distingue explicitamente `git_before_*` de `git_after_*`, passa a
exigir os 27 nomes únicos no verifier e adiciona self-verification fail-closed no
próprio produtor: um summary `PASS` que não seja verificável é convertido em
`FAIL` antes do exit code. A R1 permanece vermelha e não foi publicada.
