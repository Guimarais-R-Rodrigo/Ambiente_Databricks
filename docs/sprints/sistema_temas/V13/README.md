# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A V13 está em execução incremental. Cada sprint só é integrada depois de aceite
explícito e certificação pós-merge da `main`.

Histórico integrado:

- S0 — PR #59, merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- S1 — PR #60, merge `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`, pós-merge 15/15 `success`;
- S2 — PR #61, merge `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`, pós-merge 15/15 `success`;
- S3 — PR #62, merge `298dfb986f67cc4c560ae22b59d2fccad0716ec0`, pós-merge 15/15 `success`;
- S4 — PR #63, merge `29c3f1afa9147286627b18325380ce5b3c811331`, pós-merge 15/15 `success`.

A etapa vigente é **S5 — compatibilidade e acessibilidade operacional**, em branch
separada criada diretamente do merge S4 certificado.

Para um operador novo: S5 não altera dashboard ou workspace. Ela acrescenta uma
verificação local de contraste para pares explicitamente extraídos de export real
revisado, documenta compatibilidade/limites por superfície e transforma a issue
#57 em uma decisão operacional fail-closed sem apagar o FAIL histórico.

Leitura operacional da candidata:

- [S5 — compatibilidade e acessibilidade operacional](S5_COMPATIBILIDADE_ACESSIBILIDADE.md).

**S6 não foi iniciada.**

## Baseline certificado da S5

A branch S5 nasce diretamente de:

`29c3f1afa9147286627b18325380ce5b3c811331`

Esse SHA é o merge da S4 na `main`.

Antes da abertura da S5 foram confirmados:

- PR #63 integrada pelo HEAD S4 certificado `9b693845184877b18bf178d637a2cf25b0f18ebe`;
- `main` apontando para o merge S4;
- **15 workflows de `push`** associados ao merge;
- **15/15 `success`**;
- nenhuma mutação Databricks executada pela S4;
- issue #57 permanecendo aberta com `A11-01 = FAIL`.

A S5 não reaproveita a branch S4 como base paralela.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o
contrato de escopo.

A ordem permanece:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A S5 implementa exclusivamente:

- decisão operacional da issue #57;
- preflight de contraste/formato quando há evidência real aplicável;
- matriz de compatibilidade por superfície;
- limites Light/Dark/High Contrast explicitados;
- política fail-closed para consumidor ou formatação fora do contrato;
- regressão permanente do FAIL histórico A11.

A S6 permanece responsável pelos ensaios operacionais por superfície.

## Artefatos históricos preservados

Os artefatos de sprints integradas são históricos e não são reescritos para
simular estado atual:

- [checkpoint S0](CHECKPOINT_S0.md);
- [inventário operacional S1](S1_INVENTARIO_OPERACIONAL.md);
- [checkpoint S1](CHECKPOINT_S1.md);
- [matriz operacional S1](MATRIZ_OPERACIONAL.json);
- [S2 — preflight operacional](S2_PREFLIGHT_OPERACIONAL.md);
- [checkpoint S2](CHECKPOINT_S2.md);
- [S3 — release, instalação, atualização e rollback](S3_RELEASE_OPERACIONAL.md);
- [checkpoint S3](CHECKPOINT_S3.md);
- [S4 — observabilidade e diagnóstico](S4_OBSERVABILIDADE_DIAGNOSTICO.md);
- [checkpoint S4](CHECKPOINT_S4.md).

Exemplo: a matriz S1 mantém `S2_NOT_IMPLEMENTED` porque registra o estado da S1.
S5 não reescreve essa evidência histórica.

## Artefatos próprios da S5

A candidata adiciona:

- `tools/temas_v13_compatibilidade.py`;
- `tools/tests/test_temas_v13_s5.py`;
- [S5 — compatibilidade e acessibilidade operacional](S5_COMPATIBILIDADE_ACESSIBILIDADE.md);
- evolução do workflow V13 para S1 + S2 + S3 + S4 + S5.

A candidata não adiciona:

- cliente Databricks;
- token/secret;
- rede;
- deploy remoto;
- alteração de dashboard;
- alteração de workspace theme;
- `Publish`;
- novo schema/token/binding/role policy;
- automação de `approximated`/`unsupported`;
- suporte genérico inventado a `cellFormat`.

## Decisão da issue #57

A decisão S5 é:

`PREFLIGHT_FAIL_CLOSED`

A S5 adota preflight local de contraste para pares de foreground/background
explicitamente fornecidos a partir de export real revisado e identificado por
SHA-256.

A issue #57 permanece aberta porque a S5 não corrige os pares observados na V12 e
não produz nova evidência de ambiente. `A11-01 = FAIL` continua reproduzível.

A decisão não altera a V11:

- `ResolvedTheme` continua fonte configurável de verdade;
- `context="aibi"` continua reservado;
- 48 tokens continuam 3 `translated`, 23 `approximated`, 22 `unsupported`;
- os três bindings diretos permanecem os únicos bindings diretos;
- formatação condicional explícita não vira token do Hub.

## Relação S2 → S3 → S4 → S5

### S2 — readiness

Pergunta: “a operação está preparada?”

Saída: relatório local `V13-S2`.

### S3 — ciclo local de release

Pergunta: “o artefato pode ser staged/verificado e o rollback local pode ser
provado?”

Saída: relatório local `V13-S3`.

### S4 — diagnóstico

Pergunta: “onde a decisão ocorreu e qual é a próxima ação segura?”

Saída: diagnóstico local `V13-S4`.

### S5 — compatibilidade/acessibilidade

Pergunta: “o estado visual explicitamente observado é compatível com o critério
aplicável e o que ainda não foi exercitado?”

Saída: relatório local `V13-S5` para o preflight de contraste suportado + matriz
documental de compatibilidade.

S5 não executa S2/S3/S4 novamente e não modifica seus relatórios.

## Contraste S5

O núcleo calcula luminância relativa sRGB/WCAG e usa o ratio bruto:

- texto `NORMAL`: 4,5:1;
- texto `LARGE`: 3,0:1 somente quando declarado;
- sem arredondamento para PASS.

Modos:

- `LIGHT`;
- `DARK`;
- `HIGH_CONTRAST`.

Estados não observados recebem `NOT_APPLICABLE` / `STATE_NOT_EXERCISED` e não
recebem ratio calculado.

O preflight atual é intencionalmente limitado a `aibi_dashboard`. Outros
consumidores permanecem cobertos por seus owners e pela matriz S5; não são
generalizados silenciosamente.

## Estados herdados preservados

A S5 não altera os resultados V12:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance de ambiente observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

## CI e fronteiras

O workflow V13 permanece:

- `permissions: contents: read`;
- checkout com `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

A candidata executa S1/S2/S3/S4/S5 antes das regressões completas.

Fronteiras vivas S5:

- `V13_S5_NETWORK=0`;
- `V13_S5_REMOTE_MUTATION=0`;
- `V13_S5_CONTRAST_PREFLIGHT_LOCAL=1`;
- `V13_S6_NOT_STARTED=1`.

A asserção histórica `V13_S5_NOT_STARTED=1` permanece apenas como comentário no
step S4 do workflow, porque ela representa o checkpoint S4, não o estado vivo.

## Métricas do README raiz

O protocolo continua:

1. primeiro head S5 sem alterar `README.md` raiz;
2. runner mede identidade/links reais;
3. qualquer failure fica preservado;
4. README raiz é reconciliado somente com números observados;
5. checkpoint S5 é acrescentado depois;
6. a árvore muda e é medida novamente;
7. o SHA final é certificado de novo.

Nenhuma contagem será estimada.

## Próxima ação

A candidata S5 deve:

1. executar 32 testes próprios e mutantes;
2. repetir S1/S2/S3/S4;
3. reproduzir A11 histórico como FAIL;
4. executar regressões V01–V13 e V00;
5. validar documentação;
6. preservar failures intermediários;
7. reconciliar métricas somente pelo runner;
8. criar `CHECKPOINT_S5.md`;
9. recertificar o HEAD exato;
10. reconfirmar `main`, merge-base, ahead/behind, diff, issue #57 e concorrência;
11. parar para aceite.

**Não iniciar S6.**
