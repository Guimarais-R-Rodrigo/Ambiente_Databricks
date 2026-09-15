# Checkpoint V13 — S0: reconciliação pós-V12 e freeze de escopo

Data: 15/09/2026.

Branch: `codex/temas-v13-s0-reconciliacao-20260915`.

PR: #59, mantida em draft durante a certificação.

Estado deste documento: **candidata S0 consolidada; S1 não iniciada**. A escrita deste próprio checkpoint gera um novo SHA. Por isso, o SHA exato que contém este documento e a reconciliação final contra a `main` vigente são certificados depois deste commit e registrados na descrição da PR #59 e no checkpoint entregue ao mantenedor. Um run de SHA anterior nunca é apresentado como certificação deste commit.

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

Na abertura da S0 havia seis PRs paralelas abertas. As frentes com sobreposição documental relevante eram #56 e #51 em `README.md`; #26 em `README.md`, `docs/sprints/README.md` e `docs/sprints/sistema_temas/README.md`; e #6/#5 em `README.md`, `docs/sprints/README.md` e `CHANGELOG.md`. A PR #4 não apresentava sobreposição material com os índices vivos do Sistema de Temas. Por essa razão, `CHANGELOG.md` foi deliberadamente excluído desta S0.

## 2. Documentação auditada e classificação

### Documentação viva ou mista

| Caminho | Classificação | Ação S0 |
|---|---|---|
| `README.md` | viva | reconciliar estado atual V12/V13 e manter métricas somente após medição |
| `docs/sprints/README.md` | mista: índice vivo + cronologia histórica | atualizar somente o bloco corrente do Sistema de Temas |
| `docs/sprints/sistema_temas/README.md` | mista: estado vigente + registros históricos | atualizar somente o estado vigente e a navegação corrente |
| `docs/sprints/sistema_temas/V13/README.md` | viva, criada na S0 | registrar estado, limites, owners e próxima ação |
| `docs/sprints/sistema_temas/V13/CHECKPOINT_S0.md` | evidência da execução S0 | registrar baseline, findings, gates, failures e certificação |

### Contratos e evidências preservados

Foram lidos e classificados sem modernização retroativa, entre outros:

- `docs/sprints/sistema_temas/V13/PLANO_MESTRE.md` — contrato de planejamento aceito; texto integrado pela PR #58 preservado;
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
- `.github/workflows/temas-v12-ci.yml` — manutenção pós-PR #58 preservada sem alteração.

Frases de época como “V12 candidata” ou “V13 não iniciada” dentro de checkpoints/relatos históricos não são erro do documento histórico. O erro ocorre quando uma superfície viva apresenta essas frases como estado corrente.

## 3. Arquivos alterados pela S0

A candidata modifica somente cinco caminhos:

1. `README.md` — estado vivo V12/V13 e métricas verificáveis medidas;
2. `docs/sprints/README.md` — bloco corrente do Sistema de Temas;
3. `docs/sprints/sistema_temas/README.md` — estado vigente e navegação corrente;
4. `docs/sprints/sistema_temas/V13/README.md` — superfície viva V13/S0;
5. `docs/sprints/sistema_temas/V13/CHECKPOINT_S0.md` — evidência desta execução.

Não há edição de `CHANGELOG.md`, `.assistant`, `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, workflows, scripts, snippets, App, binder AI/BI, schema, tokens ou consumidores.

## 4. Findings da reconciliação

### F-S0-01 — índices vivos defasados

**Estado:** confirmado e corrigido na candidata S0.

`README.md`, `docs/sprints/README.md` e `docs/sprints/sistema_temas/README.md` ainda descreviam V12 como candidata/não integrada, apesar do merge da PR #54, e não apresentavam o Plano Mestre V13 como já integrado pela PR #58.

Tratamento: somente os blocos vivos foram corrigidos; cronologia e documentos históricos foram preservados.

### F-S0-02 — concorrência documental real

**Estado:** confirmado; mitigado por escopo mínimo e reconciliação final obrigatória.

Há frentes paralelas que tocam os mesmos índices. A S0 trabalha sobre a `main` real, não edita `CHANGELOG.md`, mantém o diff mínimo e exige nova comparação com a `main` imediatamente antes do aceite.

### F-S0-03 — dívida de acessibilidade herdada

**Estado:** conhecido, preservado e não corrigido na S0.

A issue #57 preserva `A11-01 = FAIL` para contraste de formatação condicional explícita do dashboard. A S0 não amplia a matriz V11, não converte `cellFormat` em token do Hub e não fecha a issue.

### F-S0-04 — bloqueios ambientais herdados

**Estado:** conhecidos e preservados.

`V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecem `BLOQUEADO_AUTORIZACAO`. A S0 não executa os ensaios nem reclassifica os bloqueios.

### F-S0-05 — métricas verificáveis mudaram com os dois artefatos V13

**Estado:** confirmado pelo primeiro gate, corrigido de forma aditiva e revalidado.

A candidata inicial acrescentou dois arquivos V13 e novos links documentais. O README ainda declarava as métricas da `main` (`1425` arquivos e `1894` links), enquanto o validador mediu `1427` arquivos e `1918` links. O failure foi preservado; a correção alterou somente essas duas linhas para os valores observados e os gates foram repetidos em novo SHA.

## 5. Escopo congelado V13 × V14

O Plano Mestre permanece a fonte canônica da fronteira.

V13 cobre consolidação operacional: inventário, preflight, release/install/update/rollback, smoke/invariantes, observabilidade técnica, diagnóstico, compatibilidade/acessibilidade operacional, ensaios autorizados e handoff.

V14 cobre production readiness e operação sustentada: ownership definitivo/substitutos, suporte sustentado, incidentes/severidades, SLA/SLO apenas quando houver base real, custos observados, retenção/housekeeping final, escalonamento/canais, revisão/depreciação e decisão final de go-live.

S0 não implementa nenhum item operacional de S1–S7.

## 6. Owners V01–V12 confirmados

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

## 7. Dívidas herdadas

Baseline S0:

- issue #57 / `A11-01 = FAIL`;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

A busca inicial de issues abertas encontrou somente a #57. Nenhuma dívida adicional foi inventada por hipótese e nenhuma issue existente foi encerrada.

## 8. Contratos explicitamente preservados

- `ResolvedTheme` segue fonte configurável de verdade;
- `context="aibi"` segue reservado;
- V11 segue com 48 tokens = 3 `translated` + 23 `approximated` + 22 `unsupported`;
- permanecem somente `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette` e `card.radius_px -> widget.corner_radius` como bindings diretos;
- `dashboard_sintetico.json` segue não importável;
- `approximated`/`unsupported` não são automatizados;
- dashboard theme ≠ workspace theme;
- `Import theme` ≠ `Publish`;
- V01–V12 continuam donos dos contratos que já possuíam;
- `ambiente_fonte/` é fonte editável; `Novo_Ambiente_Simulado/` é derivado;
- Git é a fonte canônica do projeto.

## 9. Não-escopo comprovável da S0

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

Também não há mutação Databricks, deploy, ACL, workspace theme, `Import theme`, `Publish`, alteração de dashboard ou persistência no workspace.

## 10. Failure intermediário preservado

### Head inicial da candidata

SHA: `581ff75ecbff467e87294983b8e7787cdf1586cc`.

Sete workflows de PR foram acionados. Resultados:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35033917990` | `success` |
| Contrato de temas V01 | `35033917978` | `success` |
| Núcleo de temas V02 | `35033918044` | `success` |
| Databricks App de gestão visual V10 | `35033917989` | `failure` |
| Temas nativos AI/BI V11 | `35033918002` | `failure` |
| Homologação de jornadas V12 | `35033917982` | `failure` |
| CI local reproduzível | `35033917983` | `failure` |

Os quatro failures tinham a mesma causa documental: o validador mediu `repo (identidade) = 1427` e `repo (links) = 1918`, enquanto o README ainda declarava `1425` e `1894`. O `ci_local.py` passou nos demais grupos e reprovou apenas em `validacao` por essas duas divergências.

Antes de chegar à validação que falhou, o workflow V12 deste head já havia comprovado:

- protocolo/mutantes V12: **47/47**;
- evidência real V12: **11/11**;
- regressões V01–V12: **515/515**;
- compatibilidade V00: **12/12**.

Como o workflow interrompeu na validação, a aplicabilidade do escopo estrito V12 ainda não havia sido observada nesse head. O failure não foi apagado, reexecutado como se fosse o mesmo SHA nem reclassificado.

### Correção aditiva

Commit `01406315e1d8c01b2f8008bc1b27c8372c83b628` alterou exclusivamente as duas métricas verificáveis do README para `1427` arquivos e `1918` links, exatamente como medidas. Nenhum gate, allowlist ou regra de CI foi enfraquecido.

## 11. Gates da candidata reconciliada

SHA certificado antes da consolidação deste checkpoint: `01406315e1d8c01b2f8008bc1b27c8372c83b628`.

Os sete workflows de PR concluíram com `success`:

| Workflow | Run | Resultado |
|---|---:|---|
| Databricks App de gestão visual V10 | `35034337218` | `success` |
| CI local reproduzível | `35034337236` | `success` |
| Contrato de temas V01 | `35034337323` | `success` |
| Temas nativos AI/BI V11 | `35034337321` | `success` |
| Núcleo de temas V02 | `35034337212` | `success` |
| Homologação de jornadas V12 | `35034337250` | `success` |
| Regressões da instrumentação V00 | `35034337392` | `success` |

No run V12 `35034337250`, foram observados no mesmo SHA:

- protocolo e mutantes negativos V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões de temas V01–V12: **515/515 PASS**;
- compatibilidade visual V00: **12/12 PASS**;
- validador estrutural/documental: **APROVADO — 0 falhas / 0 avisos**;
- `V12_SCOPE=NOT_APPLICABLE` para esta PR não-V12;
- etapa `Escopo V12 e higiene`: `skipped`, exatamente porque o gate estrito é não aplicável; isso não é descrito como PASS.

A manutenção da PR #58 foi, portanto, preservada: regressões e validador V12 continuam ativos em documentação compartilhada, mas o allowlist histórico da candidata V12 não foi ampliado para aceitar V13.

## 12. Métricas realmente medidas

No SHA `01406315...`, o validador conferiu as 19 linhas verificáveis do README contra a execução real. Entre as métricas observadas:

- skills: `14`, sendo `14/14` com as 5 seções estruturais;
- prompts: `16`, com `161` campos com guia e contrato humano;
- helpers citados: `92` caminhos verificados;
- Markdown: `222` arquivos / `1395` links relativos na raiz analisada;
- notebooks: `80` / `101` links relativos;
- READMEs de objeto: `76/76` operacionais, `3/3` exemplares, `0` pendentes estruturais;
- pastas de objeto: `62`;
- forma da pasta: `60`;
- contratos de dados: `62`; contratos de entrada: `60`;
- notebooks com saída colada: `79`, `0` sem;
- docstrings verificadas: `62`, `0` em inglês;
- normas do molde: `72`, `0` violações;
- notebooks que exercitam o objeto: `60`, `0` somente-import;
- Python AST: `221` arquivos;
- instruções: `9043/20000` caracteres;
- repositório editável/derivado: **1427 arquivos**;
- links fora da raiz analisada: **1918**;
- worktree extras: `0`;
- resultado: **0 falhas / 0 avisos**.

Nenhuma métrica foi estimada.

## 13. Estado Git/PR antes do commit de consolidação

No SHA `01406315...`, antes de atualizar este checkpoint:

- PR #59: aberta, `draft=true`, `merged=false`, `mergeable=true`;
- base registrada pela PR: `main` em `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`;
- branch S0: `01406315e1d8c01b2f8008bc1b27c8372c83b628`;
- arquivos alterados: `5`;
- commits da PR naquele ponto: `6`;
- o diff continuava exclusivamente documental.

A comparação anterior ao commit de métricas registrou merge-base `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`, `ahead_by=5` e `behind_by=0`; depois da correção de métricas a branch ganhou mais um commit sem incorporar mudanças da `main`.

Este documento gera mais um commit documental. O fechamento só pode considerar a S0 certificada depois de reconfirmar, no SHA exato resultante deste checkpoint: HEAD da branch, HEAD da `main`, merge-base, `ahead_by`/`behind_by`, mergeabilidade, diff, PRs paralelas, issue #57 e todos os workflows disparados. Esses dados finais são registrados na descrição da PR #59 e na entrega ao mantenedor, sem atribuir ao SHA final os testes de `01406315...`.

## 14. Limitações e evidência não produzida

A S0 produz evidência Git/CI/documental. Ela não produz nem reivindica:

- homologação adicional Databricks;
- browser/runtime do Visual Lab;
- deploy/rollback real do App;
- workspace theme/admin;
- nova evidência humana/UAT;
- correção de `A11-01`;
- autorização permanente derivada de capacidades técnicas ou de uma homologação anterior.

Os três bloqueios de autorização continuam bloqueios, não failures técnicos.

## 15. O que fica para S1

Somente após aceite explícito da S0:

- inventário operacional estruturado;
- decisão e construção de `MATRIZ_OPERACIONAL.json` ou equivalente, se ainda justificada pelo Plano Mestre;
- mapeamento superfície → owner → artefato → preflight → autorização → smoke → rollback;
- estados estruturados das superfícies ainda não homologadas;
- qualquer ferramenta operacional de preflight.

A S0 **não** cria nem antecipa esses artefatos.

## 16. Ponto de parada

Depois da certificação do SHA exato que contém este checkpoint, a PR #59 permanece em draft e sem merge até decisão explícita do mantenedor.

**Parar antes da S1.**
