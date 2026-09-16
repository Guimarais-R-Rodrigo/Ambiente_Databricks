# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A V13 está em execução incremental, com cada sprint integrada somente depois de
aceite explícito e certificação pós-merge da `main`.

Histórico integrado:

- S0 — PR #59, merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- S1 — PR #60, merge `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`, pós-merge 15/15 `success`;
- S2 — PR #61, merge `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`, pós-merge 15/15 `success`;
- S3 — PR #62, merge `298dfb986f67cc4c560ae22b59d2fccad0716ec0`, pós-merge 15/15 `success`.

A etapa vigente é **S4 — observabilidade e diagnóstico**, em branch candidata
separada criada diretamente do merge S3 certificado.

Para quem nunca operou o Hub: a S4 não tenta “consertar” automaticamente uma
falha. Ela recebe um relatório estruturado do preflight S2 ou do ciclo S3,
classifica onde o problema ocorreu, mostra a próxima ação segura e evidencia
quando uma classe de prova está faltando — sem copiar mensagem sensível do log de
origem.

Leitura operacional da candidata:

- [S4 — observabilidade e diagnóstico](S4_OBSERVABILIDADE_DIAGNOSTICO.md).

**S5 não foi iniciada.**

## Baseline certificado da S4

A branch S4 nasce diretamente de:

`298dfb986f67cc4c560ae22b59d2fccad0716ec0`

Esse SHA é o merge da S3 na `main`.

Antes da abertura da S4 foram confirmados:

- PR #62 integrada pelo HEAD S3 certificado `ee8f8198485a255ba5b4a79fba03d5f69d6d0ac0`;
- `main` apontando para o merge S3;
- **15 workflows de `push`** associados ao merge;
- **15/15 `success`**;
- nenhuma mutação Databricks executada pela S3;
- issue #57 permanecendo aberta com `A11-01 = FAIL`.

A S4 não reaproveita a branch S3 como base paralela.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o
contrato de escopo.

A ordem permanece:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A S4 implementa exclusivamente:

- taxonomia de falhas;
- relatório sanitizado de execução;
- runbook de diagnóstico;
- checklist de evidência;
- regras de logging sem PII/segredo;
- mutantes/fixtures para as classes de falha;
- distinção explícita entre `PASS`, `BLOCKED`, `FAIL` e `NOT_APPLICABLE`;
- fail-closed quando falta evidência.

A S5 permanece responsável por compatibilidade e acessibilidade operacional,
incluindo a decisão da issue #57.

## Artefatos históricos preservados

Os artefatos de sprints integradas são históricos e não devem ser reescritos para
simular o estado atual:

- [checkpoint S0](CHECKPOINT_S0.md);
- [inventário operacional S1](S1_INVENTARIO_OPERACIONAL.md);
- [checkpoint S1](CHECKPOINT_S1.md);
- [matriz operacional S1](MATRIZ_OPERACIONAL.json);
- [S2 — preflight operacional](S2_PREFLIGHT_OPERACIONAL.md);
- [checkpoint S2](CHECKPOINT_S2.md);
- [S3 — release, instalação, atualização e rollback](S3_RELEASE_OPERACIONAL.md);
- [checkpoint S3](CHECKPOINT_S3.md).

Exemplo: a matriz S1 ainda contém `S2_NOT_IMPLEMENTED` porque registra o que a S1
implementava naquele momento. A S4 não “corrige” essa frase histórica.

## Artefatos próprios da S4

A candidata adiciona:

- `tools/temas_v13_diagnostico.py`;
- `tools/tests/test_temas_v13_s4.py`;
- [S4 — observabilidade e diagnóstico](S4_OBSERVABILIDADE_DIAGNOSTICO.md);
- evolução do workflow V13 para S1 + S2 + S3 + S4.

A candidata não adiciona:

- cliente Databricks;
- token/secret;
- rede;
- deploy remoto;
- publicação;
- alteração de App/dashboard/workspace;
- novo schema/token/binding/role policy;
- score/severidade/incidente/SLA/SLO.

## Relação S2 → S3 → S4

### S2 — readiness

Pergunta: “a operação está preparada?”

Saída: relatório local `V13-S2` com estados/códigos estáveis.

### S3 — ciclo local de release

Pergunta: “o artefato pode ser staged/verificado e o rollback local pode ser
provado?”

Saída: relatório local `V13-S3`; recibo existe somente em PASS.

### S4 — diagnóstico

Pergunta: “onde a decisão ocorreu, o que falta de evidência e qual é a próxima
ação segura?”

Entrada: somente relatórios estruturados S2/S3 + classes de evidência sanitizadas.

Saída: diagnóstico local `V13-S4`.

A S4 observa. Ela não executa novamente a operação e não muta o source report.

## Estados continuam canônicos

A S4 reutiliza exatamente:

- `PASS`;
- `BLOCKED`;
- `FAIL`;
- `NOT_APPLICABLE`.

Não existe um quinto status, nota, score ou “PASS parcial”.

A prioridade fail-closed permanece:

`FAIL > BLOCKED > PASS > NOT_APPLICABLE`.

Assim:

- uma lacuna de evidência pode tornar um source `PASS` em diagnóstico `BLOCKED`;
- uma lacuna de evidência não apaga um `FAIL` já observado;
- `NOT_APPLICABLE` nunca é contado como PASS.

## Taxonomia S4

A candidata classifica códigos dos owners em 11 classes diagnósticas:

1. `INPUT_CONTRACT`;
2. `CANONICAL_CONTRACT`;
3. `ARTIFACT_INTEGRITY`;
4. `GIT_STATE`;
5. `PREFLIGHT_READINESS`;
6. `GOVERNANCE_AUTHORIZATION`;
7. `ENVIRONMENT_IDENTITY`;
8. `RECOVERY_ROLLBACK`;
9. `COMPATIBILITY_LKG`;
10. `STAGING_EXECUTION`;
11. `EVIDENCE_GAP`.

A taxonomia não muda o código original. `safe_code` continua sendo o código
estável S2/S3; `stage` é apenas a classificação diagnóstica S4.

A suíte exige igualdade exata entre o registry S4 e `STABLE_CODES` dos owners S2
e S3 para impedir drift silencioso.

## Sanitização

O diagnóstico nunca ecoa:

- `message` de origem;
- `check_id` de origem;
- conteúdo arbitrário do `receipt`;
- path local;
- `/Volumes/...`;
- `authorization_ref`;
- `identity_ref`;
- `state_ref`;
- `acceptance_ref`;
- token/PAT/secret;
- e-mail/username/workspace id.

A saída usa somente códigos/status/classes previamente conhecidos e mensagens
definidas no próprio diagnóstico.

Código desconhecido vira `SOURCE_CODE_UNREGISTERED`; o texto recebido não é
copiado para o relatório.

## Evidência

O request S4 não transporta a referência sensível. Ele transporta apenas:

- `kind`;
- `state`.

Kinds atuais:

- `git_ci`;
- `artifact`;
- `authorization`;
- `environment_identity`;
- `rollback`;
- `human`;
- `browser_runtime`.

States:

- `REFERENCED`;
- `MISSING`;
- `NOT_APPLICABLE`.

A S4 sempre declara `references_authenticated = false`. Ela não acessa o ambiente
para provar que a referência é verdadeira.

## Logging seguro

Formato determinístico:

```text
NNN|STATUS|STAGE|SAFE_CODE[|EVIDENCE_KIND]
```

Exemplo:

```text
001|FAIL|ARTIFACT_INTEGRITY|BUNDLE_INCOMPLETE
002|BLOCKED|EVIDENCE_GAP|EVIDENCE_MISSING|artifact
```

Não há timestamp gerado pela S4, texto bruto da exceção de origem ou referência
privada no log.

## Coerência fail-closed

A S4 recusa:

- engine fora de S2/S3;
- shape divergente;
- status desconhecido;
- código desconhecido;
- status de operação S2 incompatível com checks;
- `overall_status` incompatível com checks;
- S3 PASS sem recibo;
- S3 não-PASS com recibo;
- relatório que declare rede/mutação remota;
- relatório S3 que declare publicação;
- evidence kind/state desconhecido;
- evidence kind duplicado.

A S4 não tenta “ser tolerante” a relatório que não pertence ao contrato.

## Estados herdados preservados

A observabilidade não altera os resultados V12:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance de ambiente observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

S4 não amplia bindings V11, não automatiza `approximated`/`unsupported` e não
trata cores de formatação condicional como tokens do Hub.

## CI e fronteiras

O workflow V13 deve permanecer:

- `permissions: contents: read`;
- checkout com `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

A candidata executa em sequência S1/S2/S3/S4 antes das regressões completas.

Fronteiras vivas S4:

- `V13_S4_NETWORK=0`;
- `V13_S4_REMOTE_MUTATION=0`;
- `V13_S4_DIAGNOSIS_READ_ONLY=1`;
- `V13_S5_NOT_STARTED=1`.

A asserção histórica `V13_S4_NOT_STARTED=1` permanece apenas como comentário no
workflow, porque a suíte S3 comprova o estado do checkpoint S3. Ela não representa
o estado vivo desta branch.

## Métricas do README raiz

O protocolo permanece o mesmo:

1. primeiro head S4 sem alterar `README.md` raiz;
2. runner mede identidade e links reais;
3. qualquer failure fica preservado;
4. README raiz é reconciliado apenas com números observados;
5. checkpoint S4 é acrescentado depois;
6. o checkpoint muda a árvore e exige nova medição;
7. o SHA final é certificado de novo.

Nenhuma contagem será estimada.

## Próxima ação

A candidata S4 deve:

1. executar a suíte S4 e seus mutantes;
2. repetir S1/S2/S3;
3. executar regressões V01–V13 e V00;
4. validar documentação;
5. preservar failures intermediários;
6. reconciliar métricas apenas pelo runner;
7. criar `CHECKPOINT_S4.md`;
8. recertificar o HEAD exato;
9. reconfirmar `main`, merge-base, ahead/behind, diff, issue #57 e concorrência;
10. parar para aceite.

**Não iniciar S5.**
