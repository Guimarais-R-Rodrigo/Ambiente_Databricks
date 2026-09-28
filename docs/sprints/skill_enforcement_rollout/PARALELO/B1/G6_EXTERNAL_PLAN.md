# B1 G6 — plano externo preparado, não autorizado para execução

> **HISTORICAL_PRE_EXECUTION_PLAN — NOT LIVE STATE.**
> Os `NOT_RUN/NOT_AUTHORIZED` abaixo registram o estado anterior à execução G6.
> R10, full-content verify e a tentativa parcial de probes ocorreram depois.
> Estado vivo: `B1/AUTHORING_STATE.json`.


## Autoridade

Este documento prepara o próximo gate após R7 `LOCAL_PASS/AUDIT_PASS`.

```text
G6_EXTERNAL_EXECUTION = NOT_AUTHORIZED
DATABRICKS_FREE = NOT_RUN
GENIE = NOT_RUN
REMOTE_EFFECTS = NONE
POLICY_CHANGE = NONE
PROMOTION = NOT_AUTHORIZED
```

A execução exige autorização humana específica. Nada neste plano autoriza login, publicação, criação de destino, alteração de workspace ou uso de dados corporativos.

## SER03 — hub-ml-analise-safra / L3

O dossiê exige:

- executar o núcleo real no Databricks Free;
- usar apenas dados sintéticos;
- exportar tabela/metadata;
- preservar limitação de safras imaturas;
- nenhum baseline-ML/modelo de crédito é necessário.

### Free — escopo mínimo a materializar antes da execução

A preparação G6 deve produzir um pacote externo SHA-bound com:
- fixture sintética cumulativa;
- fixture sintética de eventos;
- launcher/notebook read-only;
- outputs esperados e tolerâncias;
- captura de runtime/Spark/host aplicável;
- export read-only da tabela/metadata;
- verificação de ausência de escrita persistente;
- negative checks para ausência≠zero, maturidade e replay/estimando fora do escopo.

Nenhum notebook/prompt remoto é executado até o pacote estar congelado.

### Genie — roteiro mínimo

Casos obrigatórios do dossiê:

`VF-G01` a `VF-G08`, mais dois pedidos negativos vizinhos pré-congelados.

Antes da execução, materializar para cada caso:
- prompt literal;
- variante, se houver;
- resposta/oráculo esperado por classe;
- critérios de overclaim;
- observabilidade mínima;
- evidence grade;
- regra de novo chat por caso.

Não escolher casos depois de observar resultados.

## SER05 — hub-ml-cross-eda-ml / L2

R7 prova apenas contexto/preflight L2, sem join material.

O dossiê conjunto SER05/06 exige evidência externa para o skill antes de promoção, mas a prova Spark/join material pertence à progressão SER06/L4. Portanto o G6 de SER05 L2 deve permanecer limitado ao contrato/contexto aprovado e não alegar que join_diagnostics/PIT L4 foram exercitados.

### Free — escopo L2 a materializar

Preparar um probe read-only que demonstre em runtime Free:
- carregamento/validação dos contextos sintéticos L2;
- temporal APPLICABLE e estático NOT_APPLICABLE;
- timezone/boundary/tie/lag/bitemporal fail-closed;
- nenhum join material;
- nenhuma tabela persistente;
- `join_executed=false`;
- `coverage_measured=false`;
- `ml_readiness=NOT_EVALUATED`;
- `promotion_authorized=false`.

Qualquer prova de Spark join material fica fora do G6 de SER05 L2 e pertence à SER06.

### Genie — roteiro mínimo

Casos obrigatórios do dossiê:

`CE-G01` a `CE-G08`, mais dois pedidos negativos vizinhos pré-congelados.

Os prompts precisam distinguir:
- contexto suficiente versus insuficiente;
- PIT UNKNOWN versus NOT_APPLICABLE;
- limites de latência variável/bitemporalidade;
- não alegar join executado;
- não alegar ML readiness;
- não converter source identity declarada em fonte realmente lida.

## Próxima decisão humana

Antes de qualquer execução externa, apresentar ao usuário:
1. pacote Free SER03;
2. pacote Free SER05-L2;
3. manifesto Genie VF/CE;
4. efeitos esperados = NONE;
5. dados = sintéticos;
6. destinos = nenhum persistente;
7. rollback = não aplicável para read-only;
8. limitações explicitamente fora do escopo.

Somente autorização explícita libera o G6.


## Correção de efeitos antes da execução

O planejamento inicial dizia `REMOTE_EFFECTS=NONE` de forma ampla demais. Isso vale somente para a reconciliação read-only e para a computação dos probes. Publicar o pacote ou importar notebooks de probe são efeitos remotos persistentes/temporários e exigem autorização separada.

Estados preparados:

```text
G6.READ_ONLY_RECONCILE = effect NONE / NOT_AUTHORIZED
G6.PRODUCT_PUBLISH_IF_NEEDED = REMOTE_PACKAGE_WRITE / NOT_AUTHORIZED
G6.PROBE_IMPORT = TEMPORARY_WORKSPACE_OBJECT_CREATE / NOT_AUTHORIZED
G6.FREE_PROBE_RUN = COMPUTE_ONLY_EXPECTED / NOT_AUTHORIZED
G6.GENIE = CONVERSATION_HISTORY_CREATE / NOT_AUTHORIZED
```

Não existe autorização implícita para overwrite ou cleanup.
