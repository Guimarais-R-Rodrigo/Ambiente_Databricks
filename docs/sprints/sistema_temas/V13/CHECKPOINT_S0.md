# Checkpoint V13 — S0: reconciliação pós-V12 e freeze de escopo

Data: 15/09/2026.

Branch: `codex/temas-v13-s0-reconciliacao-20260915`.

Estado deste documento: **candidata S0 em execução**. Os campos de certificação final serão atualizados somente com resultados observados no SHA exato apresentado para aceite.

## 1. Baseline inicial confirmado

- `main` esperada: `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`;
- `main` real na abertura da S0: `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`;
- divergência entre SHA esperado e real: nenhuma;
- PR #54: V12 integrada, merge `a6309a4d0b3a3530c52330e65ee5a18674118378`;
- PR #58: Plano Mestre V13 integrado, merge `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`;
- workflows de `push` do baseline `c339ed1...`: 14 execuções e 14 com conclusão `success`;
- issue aberta relevante ao Sistema de Temas: #57 (`A11-01`);
- nenhuma mutação Databricks autorizada ou executada pela S0.

A branch da S0 foi criada diretamente da `main` real. Não houve reset, rebase, force-push ou reescrita de histórico.

## 2. Documentação auditada e classificação

### Documentação viva ou mista

| Caminho | Classificação | Ação S0 |
|---|---|---|
| `README.md` | viva | reconciliar estado atual V12/V13 e manter métricas somente após medição |
| `docs/sprints/README.md` | mista: índice vivo + cronologia histórica | atualizar somente o bloco corrente do Sistema de Temas |
| `docs/sprints/sistema_temas/README.md` | mista: estado vigente + registros históricos | atualizar somente o estado vigente e a navegação corrente |
| `docs/sprints/sistema_temas/V13/README.md` | viva, criada na S0 | registrar estado, limites, owners e próxima ação |
| `docs/sprints/sistema_temas/V13/CHECKPOINT_S0.md` | evidência da execução S0 | registrar baseline, findings, gates e certificação final |

### Contratos e evidências preservados

Foram lidos e classificados sem modernização retroativa, entre outros:

- `docs/sprints/sistema_temas/V13/PLANO_MESTRE.md` — contrato de planejamento aceito; preservar o texto integrado pela PR #58;
- `docs/sprints/sistema_temas/V12/README.md` — evidência de fechamento pré-aceite;
- `docs/sprints/sistema_temas/V12/ESCOPO_E_ACEITE.md` — contrato/critério V12;
- `docs/sprints/sistema_temas/V11/README.md` — owner AI/BI e contrato 48 = 3/23/22;
- `docs/sprints/sistema_temas/V10/README.md` — owner Databricks App;
- `docs/sprints/sistema_temas/V09/README.md` — owner transporte/`theme_contract`;
- `docs/sprints/sistema_temas/V08/README.md` — owner integração transversal;
- `docs/sprints/sistema_temas/V07/README.md` — owner consumidores adicionais;
- `docs/sprints/sistema_temas/V06/README.md` — owner assets/geração;
- `docs/sprints/sistema_temas/V05/README.md` — owner Visual Lab e evidência histórica de sua candidata;
- `docs/sprints/sistema_temas/V04/README.md` e `V03/README.md` — consumers HTML/tabelas e Plotly;
- `docs/sprints/sistema_temas/V02/README.md` — owner schema/parsing/validação/`ResolvedTheme`;
- `docs/sprints/sistema_temas/V01/README.md` e `V01/PLANO_DOCUMENTACAO.md` — papéis/transições e política documental;
- `.github/workflows/temas-v12-ci.yml` — manutenção pós-PR #58 preservada.

Frases de época como “V12 candidata” ou “V13 não iniciada” dentro de checkpoints/relatos históricos não são erro do documento histórico. O erro ocorre quando uma superfície viva apresenta essas frases como estado corrente.

## 3. Findings da reconciliação

### F-S0-01 — índices vivos defasados

**Estado:** confirmado; correção S0 em andamento.

`README.md`, `docs/sprints/README.md` e `docs/sprints/sistema_temas/README.md` ainda descreviam V12 como candidata/não integrada, apesar do merge da PR #54, e não apresentavam o Plano Mestre V13 como já integrado pela PR #58.

Tratamento: corrigir apenas os blocos vivos, preservando cronologia e documentos históricos.

### F-S0-02 — concorrência documental real

**Estado:** confirmado; mitigado por escopo mínimo e reconciliação final obrigatória.

Na abertura da S0 existiam PRs paralelas que tocavam documentação compartilhada, incluindo `README.md`, `docs/sprints/README.md`, `docs/sprints/sistema_temas/README.md` e `CHANGELOG.md`. A S0 não editará `CHANGELOG.md` e reconfirmará essas frentes antes do aceite.

### F-S0-03 — dívida de acessibilidade herdada

**Estado:** conhecido, não corrigido na S0.

A issue #57 preserva `A11-01 = FAIL` para contraste de formatação condicional explícita do dashboard. A S0 não amplia a matriz V11, não converte `cellFormat` em token do Hub e não fecha a issue.

### F-S0-04 — bloqueios ambientais herdados

**Estado:** conhecidos, preservados.

`V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecem `BLOQUEADO_AUTORIZACAO`. A S0 não executa os ensaios nem reclassifica os bloqueios.

## 4. Escopo congelado V13 × V14

O Plano Mestre permanece a fonte canônica da fronteira.

V13 cobre consolidação operacional: inventário, preflight, release/install/update/rollback, smoke/invariantes, observabilidade técnica, diagnóstico, compatibilidade/acessibilidade operacional, ensaios autorizados e handoff.

V14 cobre production readiness e operação sustentada: ownership definitivo/substitutos, suporte sustentado, incidentes/severidades, SLA/SLO apenas quando houver base real, custos observados, retenção/housekeeping final, escalonamento/canais, revisão/depreciação e decisão final de go-live.

S0 não implementa nenhum item operacional de S1–S7.

## 5. Owners V01–V12 confirmados

| Owner | Responsabilidade referenciada pela V13 |
|---|---|
| V01 | papéis, estados e transições |
| V02 | schema, parsing, validação e `ResolvedTheme` |
| V03 | Plotly |
| V04 | HTML, estilos e tabelas |
| V05 | Visual Lab, draft, comparação, sessão e histórico |
| V06 | assets e geração editorial |
| V07 | consumidores visuais adicionais |
| V08 | integração transversal com skills/padrões/Manual |
| V09 | transporte, kit e `theme_contract` |
| V10 | Databricks App |
| V11 | AI/BI, fail-closed e três bindings diretos |
| V12 | protocolo, evidência e homologação |

O mapa serve para navegação e dependência. Ele não substitui os contratos canônicos de cada versão.

## 6. Dívidas herdadas

Baseline S0:

- issue #57 / `A11-01 = FAIL`;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

A busca inicial de issues abertas encontrou somente a #57. Nenhuma dívida adicional foi inventada por hipótese.

## 7. Contratos explicitamente preservados

- `ResolvedTheme` segue fonte configurável de verdade;
- `context="aibi"` segue reservado;
- V11 segue com 48 tokens = 3 `translated` + 23 `approximated` + 22 `unsupported`;
- permanecem somente três bindings diretos;
- `dashboard_sintetico.json` segue não importável;
- `approximated`/`unsupported` não são automatizados;
- dashboard theme ≠ workspace theme;
- `Import theme` ≠ `Publish`;
- `ambiente_fonte/` é fonte editável; `Novo_Ambiente_Simulado/` é derivado;
- Git é a fonte canônica do projeto.

## 8. Não-escopo comprovável da S0

A candidata S0 não deve conter alteração em:

- runtime `.assistant`;
- snippets/scripts;
- Databricks App;
- binder AI/BI;
- schema/tokens/consumidores;
- `Novo_Ambiente_Simulado/`;
- workflow V12;
- `CHANGELOG.md`;
- qualquer artefato S1 como `MATRIZ_OPERACIONAL.json` ou preflight.

Também não há mutação Databricks, deploy, ACL, workspace theme, `Import theme`, `Publish`, alteração de dashboard ou persistência no workspace.

## 9. Failures intermediários e correções

A preencher com execuções reais da candidata. Failure legítimo não será apagado nem reclassificado.

Estado inicial: **nenhum gate da candidata executado ainda**.

## 10. Testes, métricas e workflows da candidata

A preencher somente após execução no SHA correspondente.

- regressões V12: pendente;
- regressões V01–V12: pendente;
- V00: pendente;
- validador estrutural/documental: pendente;
- aplicabilidade do escopo estrito V12: esperada como `NOT_APPLICABLE` por ser PR não-V12, mas ainda não observada;
- métricas verificáveis do README: pendentes de medição;
- workflows totais do SHA final: pendentes.

## 11. Estado final Git/PR

A preencher no fechamento da S0:

- HEAD final da branch: pendente;
- HEAD final da `main`: pendente;
- merge-base: pendente;
- `ahead_by`/`behind_by`: pendente;
- mergeabilidade: pendente;
- diff final: pendente;
- PRs paralelas rechecadas: pendente;
- workflows do SHA exato: pendente.

## 12. O que fica para S1

Somente após aceite explícito da S0:

- inventário operacional estruturado;
- decisão sobre `MATRIZ_OPERACIONAL.json` ou equivalente;
- mapeamento superfície → owner → artefato → preflight → autorização → smoke → rollback;
- estados estruturados das superfícies ainda não homologadas.

A S0 **não** cria nem antecipa esses artefatos.

## 13. Ponto de parada

Quando este checkpoint estiver preenchido com o SHA final, os gates reais e a reconciliação contra a `main` vigente, a PR permanecerá sem merge até decisão explícita do mantenedor.

**Parar antes da S1.**
