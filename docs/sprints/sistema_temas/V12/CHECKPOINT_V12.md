# Checkpoint V12 — candidata Git/local pré-PR

Data: 14/09/2026.

Branch: `codex/temas-v12-homologacao-jornadas-20260914`.

Base congelada: `d106ef3158e5827a2eec3aa183dbb3b47885c960`.

Baseline técnico integralmente verde: `c2cf064b1d1bb9983af75932b22976765df51c56`.

## Estado

V12 está implementada no domínio Git/local e teve um primeiro workflow específico integralmente verde. V11 permanece fechada e não foi reaberta.

Este checkpoint distingue explicitamente:

- **Git/local**: validado no baseline técnico acima;
- **Databricks environment**: não executado nesta fase;
- **Human/UAT**: não executado nesta fase.

Nenhum desses estados é promovido por inferência. O fechamento documental que contém este checkpoint também precisa de CI próprio antes da abertura da PR draft; o run verde anterior não aprova automaticamente um commit posterior.

## Escopo canônico congelado

A V12 é a sprint de homologação formativa de jornadas com pessoas e ambiente. Ela cobre a instrumentação dos casos `DOC-02`, `DOC-03`, `A11-01`, `SEC-01` e `UAT-01`, além das superfícies Visual Lab, App V10 e AI/BI V11 somente na medida necessária para produzir evidência real quando houver ambiente e autorização apropriados.

V13/V14 continuam responsáveis pela consolidação de operação e suporte. A V12 não cria SLA, tamanho de amostra, readiness de produção ou política de suporte que o plano canônico não tenha definido.

## Decisões preservadas

- `ResolvedTheme` segue fonte configurável de verdade;
- `context="aibi"` segue reservado;
- matriz V11 continua 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- somente `widget.background`, `visualization.categorical_palette` e `widget.corner_radius` são diretos;
- JSON nativo não é inventado;
- export real precisa de bytes reais, SHA-256 exato e binding revisado;
- fixture sintético não é importável;
- workspace theme e dashboard theme continuam escopos distintos;
- import/select e publish continuam gates distintos;
- `approximated` e `unsupported` não são promovidos por observação informal;
- ausência de evidência, autorização ou rollback falha fechado.

## Evidência Git/local verde

Run `34910391401`, head `c2cf064b1d1bb9983af75932b22976765df51c56`: **SUCCESS**.

- V12 específica: **26/26 PASS**;
- regressões V01–V12: **483/483 PASS**;
- V00: **12/12 PASS**;
- validador estrutural/documental: **0 falhas / 0 avisos**;
- gate de escopo/higiene: **PASS**;
- `V12_SCOPE=PASS`;
- `V12_REMOTE_MUTATION=0`;
- checkout sem persistência de credenciais;
- nenhuma operação Databricks real.

A V12 não modifica a superfície de produto `.assistant`. As regressões cumulativas preservam as guardas permanentes de source/simulado e as interfaces V00–V11.

## Failures V12 preservados

Nenhum failure foi apagado, reclassificado ou chamado de sucesso:

| Run | Head | Estado | Causa principal |
|---|---|---|---|
| `34908962030` | `fb2d0eaf319a37a1a62e322e7f8458a47097b4f0` | **FAILURE** | métricas stale do README; escopo/higiene `SKIP` |
| `34909482529` | `a2347a3903ae3523d08da4fc83d16fa235a921b2` | **FAILURE** | fetch redundante incompatível com checkout deliberadamente sem credencial persistida |
| `34909599988` | `f1025c04cad574cd188c0809675a5edd1b9b7724` | **FAILURE** | repetição da mesma classe operacional durante a transição da correção |
| `34909800421` | `3b3538a5ad5a6b9bc4217d71a847651cb0bf83af` | **FAILURE** | auto-match da regex Shell de higiene contra a própria definição |
| `34910134591` | `53badbb723477e44d2df8f37b5ced7e025912c73` | **FAILURE** | autoinspeção Python ainda detectava literal proibido reconstruído no próprio workflow |

Em todos os failures posteriores ao primeiro, as suítes V12, cumulativa, V00 e o validador estrutural já estavam verdes; o workflow continuou corretamente marcado como `FAILURE` porque o último gate não concluiu.

## Homologações reais ainda pendentes

Continuam sem `PASS`:

- browser/runtime do Visual Lab;
- deploy e uso real do App V10;
- export real de theme AI/BI;
- binding revisado contra export real;
- import em dashboard draft real;
- preservação real de query, filtro, dataset e semântica de widget;
- light/dark real;
- permissões administrativas efetivas;
- workspace theme, snapshot e reaplicação;
- acessibilidade em render final;
- jornadas humanas `DOC-02`, `DOC-03`, `A11-01`, `SEC-01` e `UAT-01`.

Esses itens dependem de ambiente e, em alguns casos, de uma mutação remota que não foi autorizada pelo prompt de início da V12.

## Bloqueio operacional atual

Deploy de App, import de tema, alteração de workspace theme, alteração de ACL, criação/modificação/publicação de dashboard, compute e demais mutações reais permanecem bloqueados até autorização explícita adicional.

Antes da primeira mutação, a autorização deve identificar operação, ambiente, risco, rollback e evidência esperada. O bloqueio é estado correto, não failure do código.

## Trabalho paralelo e reconciliação

A PR paralela #51 de micromodelos é trabalho legítimo e toca documentos raiz, inclusive `README.md` e `CHANGELOG.md`. A V12 preserva esse trabalho e não faz force-push.

O `CHANGELOG.md` não será alterado neste fechamento pré-PR para evitar conflito documental artificial com a #51. O estado V12 e seus failures ficam registrados nos documentos da sprint e na futura PR. Após aceite, se a `main` tiver avançado, a reconciliação documental pós-merge deve incorporar de forma aditiva a entrada V12 sobre a base vigente, sem sobrescrever a frente paralela.

O `README.md` raiz já pertence ao diff V12 por necessidade de estado/métricas. Se a `main` avançar antes da integração, esse arquivo deve ser reconciliado com os commits concorrentes e todos os gates repetidos na nova composição.

## Próximo gate

1. criar um único commit de fechamento documental V12 sobre o baseline verde;
2. executar o workflow V12 nesse head exato;
3. confirmar novamente que a `main` não avançou ou reconciliar se avançou;
4. auditar o diff final contra a base vigente;
5. abrir a PR V12 como **draft** somente se o head documental estiver verde;
6. auditar todos os workflows reais do evento `pull_request` e confirmar `mergeable=true`;
7. apresentar a candidata para aceite explícito, sem ready/merge antecipado.

V13 permanece bloqueada.