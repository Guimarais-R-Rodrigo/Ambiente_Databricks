# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A V13 está em execução incremental. Cada sprint só é integrada depois de aceite explícito e certificação pós-merge da `main`.

Histórico integrado:

- S0 — PR #59, merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`;
- S1 — PR #60, merge `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`, pós-merge 15/15 `success`;
- S2 — PR #61, merge `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`, pós-merge 15/15 `success`;
- S3 — PR #62, merge `298dfb986f67cc4c560ae22b59d2fccad0716ec0`, pós-merge 15/15 `success`;
- S4 — PR #63, merge `29c3f1afa9147286627b18325380ce5b3c811331`, pós-merge 15/15 `success`;
- S5 — PR #64, merge `11e4e17f02d4ba7846f5b80bd88c0180124b5772`, pós-merge 15/15 `success`.

A etapa vigente é **S6 — ensaios operacionais por superfície**, em branch separada criada diretamente do merge S5 certificado.

Para um operador novo: a S6 prova o ciclo `PREPARE → PREFLIGHT → PACKAGE → STAGE → VERIFY → ROLLBACK` nas superfícies exercitáveis localmente ou com fixtures. Ela **não** transforma esse exercício em autorização de ambiente.

Leitura operacional da candidata:

- [S6 — ensaios operacionais por superfície](S6_ENSAIOS_OPERACIONAIS.md).

**S7 não foi iniciada.**

## Baseline certificado da S6

A branch S6 nasce diretamente de:

`11e4e17f02d4ba7846f5b80bd88c0180124b5772`

Esse SHA é o merge da S5 na `main`.

Antes da abertura da S6 foram confirmados:

- PR #64 integrada pelo HEAD S5 certificado `515c23be131b9e78f8816e9a851099154f5a0332`;
- `main` apontando para o merge S5;
- **15 workflows de `push`** associados ao merge;
- **15/15 `success`**;
- workflow V13 pós-merge com S1–S5, regressões, V00, validador e fronteiras verdes;
- nenhuma mutação Databricks executada pela S5;
- issue #57 permanecendo aberta com `A11-01 = FAIL`.

A S6 não reaproveita a branch S5 como base paralela.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o contrato de escopo.

A ordem permanece:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A S6 implementa exclusivamente **ensaios operacionais por superfície**.

Ordem preferencial preservada:

1. notebook/Plotly/HTML local;
2. Visual Lab local/simulado;
3. bundle V09;
4. App V10 em build/dry-run local;
5. AI/BI V11 com fixtures e export real somente quando já disponível/autorizado;
6. ambiente Databricks real somente com autorização específica.

Nesta candidata, os cinco primeiros itens são exercitados localmente ou com fixture. O ambiente Databricks real permanece fora da autorização concedida para iniciar S6.

## Artefatos históricos preservados

Os artefatos de sprints integradas são históricos e não são reescritos para simular estado atual:

- [checkpoint S0](CHECKPOINT_S0.md);
- [inventário operacional S1](S1_INVENTARIO_OPERACIONAL.md);
- [checkpoint S1](CHECKPOINT_S1.md);
- [matriz operacional S1](MATRIZ_OPERACIONAL.json);
- [S2 — preflight operacional](S2_PREFLIGHT_OPERACIONAL.md);
- [checkpoint S2](CHECKPOINT_S2.md);
- [S3 — release, instalação, atualização e rollback](S3_RELEASE_OPERACIONAL.md);
- [checkpoint S3](CHECKPOINT_S3.md);
- [S4 — observabilidade e diagnóstico](S4_OBSERVABILIDADE_DIAGNOSTICO.md);
- [checkpoint S4](CHECKPOINT_S4.md);
- [S5 — compatibilidade e acessibilidade operacional](S5_COMPATIBILIDADE_ACESSIBILIDADE.md);
- [checkpoint S5](CHECKPOINT_S5.md).

Exemplo: a matriz S1 mantém `S2_NOT_IMPLEMENTED` porque registra o estado da S1. A S6 não reescreve essa evidência histórica.

## Artefatos próprios da S6

A candidata adiciona:

- `tools/temas_v13_ensaios.py`;
- `tools/tests/test_temas_v13_s6.py`;
- [S6 — ensaios operacionais por superfície](S6_ENSAIOS_OPERACIONAIS.md);
- evolução do workflow V13 para S1 + S2 + S3 + S4 + S5 + S6.

A candidata não adiciona:

- cliente Databricks;
- token/secret;
- acesso de rede;
- deploy remoto;
- alteração de dashboard real;
- alteração de workspace theme;
- `Publish`;
- novo schema/token/binding/role policy;
- segundo empacotador V09/V10;
- automação de `approximated`/`unsupported`;
- suporte genérico inventado a `cellFormat`.

## Relação S2 → S3 → S4 → S5 → S6

### S2 — readiness

Pergunta: “a operação está preparada?”

Saída: relatório local `V13-S2`.

### S3 — ciclo local de release

Pergunta: “o artefato pode ser staged/verificado e o rollback local pode ser provado?”

Saída: relatório local `V13-S3`.

### S4 — diagnóstico

Pergunta: “onde a decisão ocorreu e qual é a próxima ação segura?”

Saída: diagnóstico local `V13-S4`.

### S5 — compatibilidade/acessibilidade

Pergunta: “o estado visual explicitamente observado é compatível com o critério aplicável e o que ainda não foi exercitado?”

Saída: relatório local `V13-S5` + matriz documental de compatibilidade.

### S6 — ensaio operacional

Pergunta: “as etapas aplicáveis do ciclo operacional podem ser executadas e revertidas usando os owners existentes, sem publicação implícita?”

Saída: relatório local `V13-S6`, com cada superfície e cada fase explicitamente classificada.

S6 compõe os owners anteriores; não modifica relatórios S2/S3/S4/S5 nem redefine seus contratos.

## Superfícies da S6

| Superfície | Ensaio permitido nesta candidata |
|---|---|
| notebook/Plotly/HTML | aplicação opt-in somente em memória + invariantes + descarte do stage |
| Visual Lab | preset sintético + proposta + save/reopen temporário + restore |
| V09 | build local + S2 + staging S3 + rollback dry-run |
| V10 | build local do App + S2 + staging S3 + rollback dry-run |
| AI/BI | projeção/binding somente em fixture local + invariantes semânticos |
| workspace theme | apenas provar `BLOCKED` no preflight local |

A existência de um PASS local para Visual Lab, App ou AI/BI não reclassifica os casos ambientais V12.

## Estados herdados preservados

A S6 não altera os resultados V12:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance de ambiente observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 evidenciado;
- `A11-01 = FAIL`, issue #57 aberta;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Os três casos `BLOQUEADO_AUTORIZACAO` só podem ser reexecutados como ensaio real com autorização nova e específica. O aceite para iniciar S6 não é essa autorização.

## CI e fronteiras

O workflow V13 permanece:

- `permissions: contents: read`;
- checkout com `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

A candidata executa S1/S2/S3/S4/S5/S6 antes das regressões completas.

Fronteiras vivas S6:

- `V13_S6_NETWORK=0`;
- `V13_S6_REMOTE_MUTATION=0`;
- `V13_S6_IMPLICIT_PUBLICATION=0`;
- `V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5`;
- `V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3`;
- `V13_S7_NOT_STARTED=1`.

A asserção `V13_S6_NOT_STARTED=1` permanece apenas como comentário histórico do checkpoint S5.

## Métricas do README raiz

O protocolo permanece o mesmo:

1. first head S6 sem alterar `README.md` raiz;
2. runner mede identidade/links reais;
3. qualquer failure fica preservado;
4. README raiz é reconciliado somente com números observados;
5. checkpoint S6 é acrescentado depois;
6. a árvore muda e é medida novamente;
7. o SHA final é certificado de novo.

Nenhuma contagem será estimada.

## Próxima ação

A candidata S6 deve:

1. executar a suíte própria e os ensaios locais/simulados;
2. repetir S1/S2/S3/S4/S5;
3. manter os três casos ambientais V12 bloqueados;
4. executar regressões V01–V13 e V00;
5. validar documentação;
6. preservar failures intermediários;
7. reconciliar métricas somente pelo runner;
8. criar `CHECKPOINT_S6.md`;
9. recertificar o HEAD exato;
10. reconfirmar `main`, merge-base, ahead/behind, diff, issue #57 e concorrência;
11. parar para aceite.

**S7 não foi iniciada.**
