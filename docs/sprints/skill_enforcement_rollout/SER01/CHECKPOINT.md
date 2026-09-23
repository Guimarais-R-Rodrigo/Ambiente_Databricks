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
