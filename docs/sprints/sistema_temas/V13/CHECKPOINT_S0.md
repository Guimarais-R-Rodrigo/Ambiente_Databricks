# Checkpoint V13 — S0: reconciliação pós-V12 e freeze de escopo

Data: 15/09/2026.

Branch: `codex/temas-v13-s0-reconciliacao-20260915`.

Estado deste documento: **S0 aceita pelo mantenedor em 15/09/2026; candidata certificada no HEAD `b827063d45a42d2e76dac4b8b94241c529d8eed6`; integração autorizada.** O merge e os checks de `push` da `main` são verificados fora deste documento para não invalidar o SHA certificado antes da integração.

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

**Estado:** confirmado e corrigido na candidata S0.

`README.md`, `docs/sprints/README.md` e `docs/sprints/sistema_temas/README.md` ainda descreviam V12 como candidata/não integrada, apesar do merge da PR #54, e não apresentavam o Plano Mestre V13 como já integrado pela PR #58.

Tratamento: somente os blocos vivos foram corrigidos; cronologia e documentos históricos foram preservados.

### F-S0-02 — concorrência documental real

**Estado:** confirmado; mitigado por escopo mínimo e reconciliação final.

Na abertura e no fechamento da S0 existiam PRs paralelas que tocavam documentação compartilhada, incluindo `README.md`, `docs/sprints/README.md`, `docs/sprints/sistema_temas/README.md` e `CHANGELOG.md`. A S0 não editou `CHANGELOG.md`. A `main` não avançou durante a certificação da candidata.

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

A busca inicial e a reconfirmação final de issues abertas encontraram somente a #57. Nenhuma dívida adicional foi inventada por hipótese.

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

A candidata S0 não contém alteração em:

- runtime `.assistant`;
- snippets/scripts;
- Databricks App;
- binder AI/BI;
- schema/tokens/consumidores;
- `Novo_Ambiente_Simulado/`;
- workflow V12;
- `CHANGELOG.md`;
- qualquer artefato S1 como `MATRIZ_OPERACIONAL.json` ou preflight.

Também não houve mutação Databricks, deploy, ACL, workspace theme, `Import theme`, `Publish`, alteração de dashboard ou persistência no workspace.

## 9. Failures intermediários e correções

Primeiro head completo: `581ff75ecbff467e87294983b8e7787cdf1586cc`.

Sete workflows de PR foram acionados nesse SHA:

- V00 `35033917990` — `success`;
- V01 `35033917978` — `success`;
- V02 `35033918044` — `success`;
- V10 `35033917989` — `failure`;
- V11 `35033918002` — `failure`;
- V12 `35033917982` — `failure`;
- CI local `35033917983` — `failure`.

A causa comum dos quatro failures foi o validador estrutural/documental: a candidata acrescentou dois arquivos V13 e novos links, levando a medição real para **1427 arquivos** e **1918 links**, enquanto o README ainda declarava 1425/1894. Todas as demais etapas do `ci_local.py` haviam passado.

No run V12 `35033917982`, antes da falha de validação, foram observados:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões de temas V01–V12: **515/515 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- validador: `FAIL` somente pelas duas métricas do README;
- aplicabilidade do gate V12 e escopo/higiene posteriores: `skipped` por interrupção após o failure do validador.

Correção aditiva: commit `01406315e1d8c01b2f8008bc1b27c8372c83b628`, alterando somente as duas linhas de métricas do README para 1427/1918. Nenhum gate foi relaxado, allowlist ampliado ou failure reclassificado.

Segunda rodada no SHA `01406315...`: **7/7 workflows de PR concluíram com `success`**. No run V12 `35034337250`, o validador passou e o log registrou `V12_SCOPE=NOT_APPLICABLE`; a etapa `Escopo V12 e higiene` ficou `skipped`, não PASS.

O checkpoint foi então consolidado no commit `b827063d45a42d2e76dac4b8b94241c529d8eed6`, que exigiu nova certificação no próprio SHA.

## 10. Testes, métricas e workflows do HEAD final

HEAD certificado: `b827063d45a42d2e76dac4b8b94241c529d8eed6`.

Workflows de PR observados no SHA final:

| Workflow | Run | Resultado |
|---|---:|---|
| Contrato de temas V01 | `35034678651` | `success` |
| Databricks App de gestão visual V10 | `35034678646` | `success` |
| Temas nativos AI/BI V11 | `35034678724` | `success` |
| Núcleo de temas V02 | `35034678639` | `success` |
| Homologação de jornadas V12 | `35034678732` | `success` |
| Regressões da instrumentação V00 | `35034678705` | `success` |
| CI local reproduzível | `35034678745` | `success` |

Total do SHA final: **7/7 workflows de PR com `success`**.

No run V12 final `35034678732`, no mesmo HEAD:

- `python -B tools/tests/test_temas_v12.py -v`: **47/47 PASS**;
- `python -B tools/tests/test_temas_v12_evidencia_real.py -v`: **11/11 PASS**;
- `python -B -m unittest discover -s tools/tests -p 'test_temas*.py' -v`: **515/515 PASS**;
- `python -B tools/tests/test_visual_legado_v00.py`: **12/12 PASS**;
- `python -B tools/validate_assistant.py --conferir-readme`: **APROVADO, 0 falhas, 0 avisos**;
- `repo (identidade)`: **1427 arquivos**;
- `repo (links)`: **1918 links fora da raiz analisada**;
- `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

A manutenção integrada pela PR #58 foi, portanto, preservada: regressões e validador V12 executam nesta PR não-V12, mas a guarda estrita histórica não é aplicada fora de candidata V12.

## 11. Estado final Git/PR antes do aceite

Reconfirmação imediatamente anterior ao aceite:

- HEAD da branch: `b827063d45a42d2e76dac4b8b94241c529d8eed6`;
- HEAD da `main`: `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`;
- merge-base: `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`;
- comparação: `ahead_by=7`, `behind_by=0`;
- PR #59: aberta, draft, `mergeable=true`, não integrada;
- diff final: **5 arquivos** — `README.md`, `docs/sprints/README.md`, `docs/sprints/sistema_temas/README.md`, `V13/README.md` e `V13/CHECKPOINT_S0.md`;
- `PLANO_MESTRE.md`, workflow V12, runtime, produto, derivado e `CHANGELOG.md` não aparecem no diff;
- `main` não avançou durante a S0.

Concorrência final observada: além da PR #59, permaneciam seis PRs abertas. Sobreposições documentais continuavam presentes especialmente nas PRs #56, #51, #26, #6 e #5; a #4 não tocava os índices vivos do Sistema de Temas. Nenhuma dessas frentes entrou na `main` durante a certificação da S0.

## 12. O que fica para S1

Somente após integração da S0 aceita:

- inventário operacional estruturado;
- decisão e implementação de `MATRIZ_OPERACIONAL.json` ou equivalente justificado;
- mapeamento superfície → owner → artefato → preflight → autorização → smoke → rollback;
- estados estruturados das superfícies ainda não homologadas;
- testes que recusem entrada sem owner, rollback ou autorização.

A S0 **não** criou nem antecipou esses artefatos.

## 13. Aceite e ponto de parada

Em 15/09/2026, o mantenedor respondeu explicitamente **“Aceito, siga”** ao checkpoint que separava duas autorizações: integrar a S0 e, após a integração, iniciar a S1.

Esse aceite autoriza o merge da PR #59 no HEAD certificado e a abertura posterior de uma frente S1 separada a partir da `main` integrada. Não altera os bloqueios Databricks herdados e não concede autorização de mutação remota.

**S1 deve começar somente após o merge da S0 e a confirmação da nova `main`.**
