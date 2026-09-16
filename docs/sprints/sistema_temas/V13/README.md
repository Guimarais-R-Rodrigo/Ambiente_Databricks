# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A S0 foi **aceita e integrada** pela PR #59 no merge `1d46c9625fb5bfd6d1b666ddff055507238788bf`.

A S1 foi **aceita e integrada** pela PR #60 no merge `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`. Os **15/15 workflows de `push`** disparados por esse merge concluíram com `success`.

A etapa vigente é **S2 — preflight operacional unificado**, em branch candidata separada.

Para quem nunca entrou no Hub: a S2 funciona como uma lista de conferência automática antes de uma operação. Ela verifica o que pode ser provado localmente e distingue `PASS`, `BLOCKED`, `FAIL` e `NOT_APPLICABLE`. Ela não executa a mudança e não consulta o Databricks.

A leitura operacional da etapa começa em [S2 — preflight operacional unificado](S2_PREFLIGHT_OPERACIONAL.md).

**S3 não foi iniciada.** Release, instalação, atualização e rollback operacional consolidado continuam pertencendo à próxima subfase.

## Baseline certificado da S2

A branch S2 nasce diretamente de:

`70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`

Esse SHA é o merge da S1 na `main`.

O pós-merge da S1 foi certificado antes da abertura da S2:

- 15 workflows de `push`;
- 15 `success`;
- 0 failures;
- nenhuma mutação Databricks executada pelo fechamento S1.

A S2 não reaproveita a branch S1 como base paralela.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o contrato de escopo.

A ordem permanece:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A V13 continua responsável por consolidação operacional: inventário, preflight, release/install/update/rollback, observabilidade técnica, diagnóstico, compatibilidade/acessibilidade operacional, ensaios autorizados e handoff.

A V14 continua responsável por production readiness e suporte sustentado.

## S0 e S1 preservadas

Documentos históricos e de fechamento:

- [checkpoint S0](CHECKPOINT_S0.md);
- [inventário operacional S1](S1_INVENTARIO_OPERACIONAL.md);
- [checkpoint S1](CHECKPOINT_S1.md);
- [matriz operacional S1](MATRIZ_OPERACIONAL.json).

A S2 **consome** esses artefatos. Ela não reescreve o contrato S1 para remover a frase histórica `S2_NOT_IMPLEMENTED`.

Isso é intencional: o que a S1 dizia sobre si mesma continua verdadeiro.

## S2 — artefatos próprios

A candidata S2 adiciona:

- `tools/temas_v13_preflight.py`: porta de entrada local/read-only;
- `tools/tests/test_temas_v13_s2.py`: testes de contrato, falhas e determinismo;
- [S2 — preflight operacional unificado](S2_PREFLIGHT_OPERACIONAL.md): guia para público técnico e não técnico;
- evolução do workflow `.github/workflows/temas-v13-ci.yml` para executar S1 e S2 no mesmo gate V13.

A candidata não adiciona cliente Databricks, credencial, chamada de rede, deploy ou publicação.

## Modelo da S2

A entrada possui dois modos:

- `surface`: uma única superfície/ação;
- `aggregate`: várias operações em um relatório determinístico.

A saída possui quatro estados:

| Estado | Significado |
|---|---|
| `PASS` | checks localmente demonstráveis satisfeitos |
| `BLOCKED` | condição necessária não pode ser fabricada pelo preflight, como autorização ou identidade efetiva |
| `FAIL` | contrato ou pré-requisito local verificável falhou |
| `NOT_APPLICABLE` | check não pertence à ação |

Precedência:

`FAIL > BLOCKED > PASS > NOT_APPLICABLE`

## Composição com owners existentes

A S2 reutiliza:

| Necessidade | Owner composto |
|---|---|
| tema, schema, hash e contexto | V02 |
| bundle/`theme_contract` | V09 |
| bundle do Databricks App | V10 |
| projeção/binding AI/BI | V11 |
| owner, ação, autorização e rollback | matriz S1 |

A S2 não cria:

- segundo schema de tema;
- segunda matriz de bindings;
- segunda lista `theme_contract`;
- nova política de papéis;
- novo contexto `aibi`;
- nova regra de publicação.

## Seis superfícies preservadas

A S2 continua operando sobre as seis superfícies inventariadas na S1:

1. `notebook_visual_core`;
2. `visual_lab`;
3. `transition_bundle`;
4. `databricks_app`;
5. `aibi_dashboard`;
6. `workspace_theme`.

Nenhuma superfície nova é criada nesta etapa.

## Estados herdados preservados

| Caso | Estado |
|---|---|
| `DOC-02` | `PASS` |
| `DOC-03` | `PASS` |
| `SEC-01` | `PASS` de ambiente |
| `UAT-01` | `PASS` somente textual |
| `V12-AIBI-01` | `PASS` limitado a dashboard draft, dados sintéticos, import + rollback |
| `A11-01` | `FAIL`, issue #57 |
| `V12-LAB-01` | `BLOQUEADO_AUTORIZACAO` |
| `V12-APP-01` | `BLOQUEADO_AUTORIZACAO` |
| `V12-AIBI-02` | `BLOQUEADO_AUTORIZACAO` |

A S2 não permite que um campo fornecido no request sobrescreva um `BLOQUEADO_AUTORIZACAO` ou `NOT_AUTHORIZED` canônico.

## Identidade não é simulada como prova

O preflight local não autentica usuário ou administrador no Databricks.

Por isso:

- ausência de referência de identidade gera `IDENTITY_REQUIRED`;
- presença de referência local não vira prova viva e permanece `IDENTITY_LIVE_UNVERIFIED`.

Isso é fail-closed, não uma limitação escondida.

## Rollback

Toda ação mutável continua submetida ao rollback da matriz S1.

A S2 diferencia:

- rollback preparado e referenciado;
- rollback ausente;
- rollback canonicamente bloqueado porque o owner ainda depende de autorização/snapshot/procedimento futuro.

Ela não executa rollback. A operacionalização do ciclo completo é S3.

## AI/BI

A S2 preserva integralmente V11:

- somente três bindings diretos;
- `approximated` e `unsupported` não automatizados;
- JSON nativo não inventado;
- fixture sintético não importável;
- dashboard theme separado de workspace theme;
- `Import theme` separado de `Publish`.

O binder V11 é chamado por composição para detectar SHA stale, JSON Pointer inexistente e capacidade fora do contrato.

## CI e fronteiras

O workflow V13 permanece:

- `permissions: contents: read`;
- `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

A fronteira da S2 deve registrar:

- `V13_S2_NETWORK=0`;
- `V13_S2_REMOTE_MUTATION=0`;
- `V13_S3_NOT_STARTED=1`.

Git/CI continuam evidência técnica, não homologação de ambiente.

## Métricas do README raiz

A S2 não estima contagens do repositório.

O primeiro head candidato é executado antes de qualquer ajuste de `repo (identidade)` ou `repo (links)`. Se a árvore nova alterar essas métricas, o failure intermediário será preservado e o README raiz será corrigido **somente com os valores realmente medidos pelo runner**.

## Próxima ação

A candidata S2 deve:

1. executar a suíte própria;
2. executar regressões S1 e V01–V12;
3. validar o README/estrutura;
4. preservar qualquer failure intermediário;
5. produzir checkpoint S2;
6. reconfirmar `main`, merge-base, ahead/behind, mergeabilidade e concorrência.

**Parar antes da S3.**
