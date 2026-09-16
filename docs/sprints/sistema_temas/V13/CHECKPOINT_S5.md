# Checkpoint V13 — S5: compatibilidade e acessibilidade operacional

Data: 16/09/2026.

Branch: `codex/temas-v13-s5-compatibilidade-acessibilidade-20260916`.

Estado deste documento: **candidata S5 em certificação final**. O HEAD imediatamente anterior à criação deste checkpoint, `d467c57ee9008f3a3ca2b2f198e2d24f1ac5adad`, concluiu 8/8 workflows de PR com `success`. Como este checkpoint acrescenta um novo arquivo à árvore, o novo HEAD precisa ser medido e certificado novamente antes de qualquer aceite.

## 1. Baseline de abertura

A S5 só foi iniciada depois do fechamento completo da S4:

- S4 aceita e integrada pela PR #63;
- merge S4 na `main`: `29c3f1afa9147286627b18325380ce5b3c811331`;
- pós-merge S4: **15/15 workflows de `push` com `success`**;
- branch S5 criada diretamente desse merge certificado;
- nenhuma mutação Databricks foi autorizada ou executada pela S5;
- S6 não foi iniciada.

A S5 não reutilizou a branch S4 como base paralela.

## 2. Escopo canônico recuperado do Plano Mestre

A S5 implementa exclusivamente **compatibilidade e acessibilidade operacional**.

Entregáveis canônicos:

- decisão operacional sobre a issue #57;
- preflight de contraste/formato quando suportado por evidência real;
- matriz de compatibilidade por superfície;
- limites Light/Dark/High Contrast explícitos;
- política fail-closed para consumidor ou formatação fora do contrato.

Gates canônicos:

- ratios sem arredondamento para aprovação;
- A11 histórico continua reproduzível como FAIL até correção e nova evidência;
- cor explícita não vira automaticamente token do Hub;
- V11 não é ampliada silenciosamente;
- estado não exercitado não é inferido.

Ensaios operacionais por superfície pertencem à S6 e não foram antecipados.

## 3. Decisão da issue #57

A decisão operacional da S5 é:

`PREFLIGHT_FAIL_CLOSED`

A S5 adota preflight local de contraste para pares de foreground/background explicitamente fornecidos como provenientes de export real revisado.

A issue #57 permanece aberta.

A S5 não corrige os pares observados na V12, não altera `cellFormat`, não produz nova evidência de ambiente e não transforma o finding histórico em PASS.

`A11-01 = FAIL` continua verdadeiro no alcance observado e continua reproduzível pela suíte S5.

## 4. Contratos congelados preservados

Continuam sem modificação:

- `ResolvedTheme` é a fonte configurável de verdade;
- `context="aibi"` permanece reservado;
- 48 tokens notebook continuam 3 `translated`, 23 `approximated` e 22 `unsupported`;
- os únicos bindings diretos continuam:
  - `surface.card -> widget.background`;
  - `palette.categorical -> visualization.categorical_palette`;
  - `card.radius_px -> widget.corner_radius`;
- `dashboard_sintetico.json` não é import nativo;
- `approximated` e `unsupported` não são automatizados;
- dashboard theme e workspace theme continuam superfícies separadas;
- `Import theme` e `Publish` continuam gates diferentes;
- `cellFormat` não vira token do Hub.

## 5. Artefatos próprios da candidata

A S5 adiciona:

- `tools/temas_v13_compatibilidade.py`;
- `tools/tests/test_temas_v13_s5.py`;
- `docs/sprints/sistema_temas/V13/S5_COMPATIBILIDADE_ACESSIBILIDADE.md`;
- este checkpoint.

Também evolui:

- `.github/workflows/temas-v13-ci.yml`;
- `docs/sprints/sistema_temas/V13/README.md`;
- `README.md`, somente depois da primeira medição real do runner.

Não houve alteração em `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, matriz S1, preflight S2, executor S3, diagnóstico S4, App V10, binder V11, schema/tokens ou contratos funcionais V01–V12.

## 6. Preflight local S5

Ferramenta:

`tools/temas_v13_compatibilidade.py`

Características:

- engine `V13-S5`;
- superfície atual suportada: `aibi_dashboard`;
- evidence basis exigida: `REVIEWED_REAL_EXPORT`;
- export declarado por SHA-256 completo;
- `synthetic_fixture_used=false` obrigatório;
- pares de contraste fornecidos explicitamente;
- somente pares `observed=true` são medidos;
- estados não exercitados não recebem ratio inferido;
- saída declara `evidence_authenticated=false`;
- nenhuma leitura de Databricks;
- nenhum parser inventado de schema global nativo;
- nenhuma alteração remota.

O preflight não autentica a prova externa. Ele valida somente o request e calcula contraste para os pares explicitamente fornecidos.

## 7. Cálculo e modos

A ferramenta usa luminância relativa sRGB/WCAG e compara ratio bruto.

Limiar:

- `NORMAL = 4.5:1`;
- `LARGE = 3.0:1` somente quando explicitamente declarado.

Modos:

- `LIGHT`;
- `DARK`;
- `HIGH_CONTRAST`.

Um par não exercitado recebe:

- `status = NOT_APPLICABLE`;
- `code = STATE_NOT_EXERCISED`;
- `ratio = null`.

Ausência de observação não vira PASS.

## 8. Reprodução permanente do A11 histórico

A suíte S5 reproduz os quatro pares observados e também verifica que eles continuam ancorados em `docs/sprints/sistema_temas/V12/TESTES.md`.

- `#9C2638` sobre `#E8F4FD` — Light: `6.837793163467097:1` — PASS;
- `#9C2638` sobre `#11171C` — Dark: `2.3624715346329377:1` — **FAIL**;
- `#FFD465` sobre `#E8F4FD` — Light: `1.264684095079348:1` — **FAIL**;
- `#FFD465` sobre `#11171C` — Dark: `12.773222792356847:1` — PASS.

Resultado agregado: **FAIL**.

Esse FAIL não é arredondado para aprovação e não é mascarado por outras combinações que passem.

## 9. Matriz de compatibilidade

A documentação S5 cobre exatamente as seis superfícies da matriz S1 e referencia seus owners:

- `notebook_visual_core` — owner V02;
- `visual_lab` — owner V05;
- `transition_bundle` — owner V09;
- `databricks_app` — owner V10;
- `aibi_dashboard` — owner V11;
- `workspace_theme` — owner V11.

A matriz S5 é uma visão operacional. Ela não substitui `MATRIZ_OPERACIONAL.json` nem cria nova fonte canônica.

Light/Dark/High Contrast usam marcadores explícitos como `CONTRACT_ONLY`, `REAL_OBSERVED_A11`, `NOT_EXERCISED` e `NOT_APPLICABLE`; não existe PASS universal fabricado.

## 10. Fronteira operacional

O núcleo S5 não importa:

- `requests`;
- `socket`;
- `urllib`;
- `httpx`;
- cliente `databricks`;
- `subprocess`;
- `shutil`.

O workflow permanece `contents: read`, checkout `persist-credentials: false` e sem credenciais Databricks.

Fronteiras vivas:

- `V13_S5_NETWORK=0`;
- `V13_S5_REMOTE_MUTATION=0`;
- `V13_S5_CONTRAST_PREFLIGHT_LOCAL=1`;
- `V13_S6_NOT_STARTED=1`.

A asserção histórica `V13_S5_NOT_STARTED=1` permanece apenas como comentário no step S4 do workflow.

## 11. Suíte permanente S5

`tools/tests/test_temas_v13_s5.py` contém **32 testes**.

Cobertura inclui:

- ratio preto/branco conhecido;
- reprodução dos quatro ratios A11;
- ancoragem dos dados A11 em evidência V12;
- ausência de arredondamento para PASS;
- limiares normal/grande;
- Light/Dark/High Contrast;
- `NOT_EXERCISED` explícito;
- FAIL dominando pares que passam;
- PASS limitado ao preflight local;
- output sem rede/mutação/binding novo;
- type/shape/version fechados;
- superfície atual restrita;
- evidence basis real revisada;
- SHA-256 válido;
- fixture sintético recusado como export real;
- lista de pares não vazia;
- shape de par fechado;
- `pair_id` sanitizado e único;
- cor `#RRGGBB` sem alpha/atalhos/nomes;
- enum de modo;
- enum de classe de texto;
- booleano de observação;
- determinismo;
- ausência de imports de rede/cliente/shell;
- seis superfícies/owners da S1;
- decisão `PREFLIGHT_FAIL_CLOSED`;
- issue #57 aberta e V11 congelada;
- documentação Light/Dark/High Contrast;
- workflow read-only;
- S6 não iniciada.

## 12. First head e failure preservado

Primeiro HEAD S5:

`d8cdaf27646033af0868319b3199400567783377`.

Workflows observados:

- V00 `35085657846` — `success`;
- V01 `35085657775` — `success`;
- V02 `35085657824` — `success`;
- CI geral `35085658821` — `failure`;
- V13 `35085657843` — `failure`.

No V13 first head:

- S1: PASS;
- validador S1: PASS;
- S2: PASS;
- S3: PASS;
- S4: PASS;
- S5: **32/32 PASS**;
- regressões V01–V13: **645/645 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador estrutural/documental: FAIL somente por métricas README;
- fronteiras S1/S2/S3/S4/S5: `skipped`, não PASS.

No CI geral first head:

- suíte `temas`: PASS;
- biblioteca: PASS;
- ferramentas: PASS;
- transição: PASS;
- READMEs: PASS;
- Concierge: PASS nos gates aplicáveis;
- validador mediu **1447 arquivos / 1918 links**;
- README raiz ainda declarava 1444/1916;
- única causa do failure: duas divergências documentais de métrica;
- nenhuma falha funcional S5 foi observada.

O failure permanece histórico e não foi reclassificado.

## 13. Correção aditiva do first head

Commit:

`d467c57ee9008f3a3ca2b2f198e2d24f1ac5adad`.

Alteração exclusiva: `README.md` raiz.

Mudanças:

- estado vivo reconciliado para S4 integrada/S5 candidata;
- `repo (identidade)` de 1444 para **1447**;
- `repo (links)` de 1916 para **1918**.

Nenhum gate, allowlist, contrato ou suíte foi relaxado.

## 14. Certificação do segundo head

O SHA `d467c57ee9008f3a3ca2b2f198e2d24f1ac5adad` acionou 8 workflows reais de PR, todos concluídos com `success`:

- V00 `35086013151` — `success`;
- V01 `35086013166` — `success`;
- V02 `35086013229` — `success`;
- CI geral `35086013165` — `success`;
- V10 `35086013302` — `success`;
- V11 `35086013139` — `success`;
- V12 `35086013140` — `success`;
- V13 `35086013133` — `success`.

No V13, no mesmo SHA:

- S1: **20/20 PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- S4: **30/30 PASS**;
- S5: **32/32 PASS**;
- regressões V01–V13: **645/645 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador estrutural/documental: **APROVADO — 0 falhas / 0 avisos**;
- métricas: **1447 arquivos / 1918 links**;
- worktree extras: 0;
- fronteiras S1/S2/S3/S4/S5: PASS.

Fronteira S5 confirmada:

- `V13_S5_NETWORK=0`;
- `V13_S5_REMOTE_MUTATION=0`;
- `V13_S5_CONTRAST_PREFLIGHT_LOCAL=1`;
- `V13_S6_NOT_STARTED=1`.

## 15. Preservação V12 no segundo head

Workflow V12: `35086013140`.

No mesmo SHA:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões transversais: **645/645 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- métricas: **1447/1918**;
- aplicabilidade do escopo estrito: `success` com saída `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

A allowlist V12 não foi ampliada.

## 16. Estados herdados preservados

A S5 mantém separadamente:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 já evidenciado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

A S5 não fecha, reclassifica ou mascara a issue #57.

A decisão S5 define o gate operacional para contraste, mas o finding só pode mudar com correção e nova evidência aplicável.

## 17. Ausência de mutação Databricks

A S5 não executou:

- deploy de App;
- ACL/grupos;
- workspace theme;
- `Import theme` remoto;
- `Publish`;
- edição de dashboard;
- persistência no workspace;
- criação/alteração de UC Volume;
- qualquer outra mutação Databricks.

Git/CI continuam evidência técnica, não homologação de ambiente.

## 18. Efeito deste checkpoint na árvore

Este arquivo é um novo caminho versionado. Portanto, as métricas **1447/1918** pertencem ao HEAD anterior `d467c57e...` e **não são presumidas para o HEAD que contém este checkpoint**.

O próximo gate é:

1. observar todos os workflows do novo SHA;
2. registrar a medição real do validador;
3. preservar qualquer failure de métrica;
4. corrigir o README raiz somente com a saída real;
5. atualizar este checkpoint com a nova evidência sem criar outro arquivo;
6. recertificar o SHA resultante;
7. reconfirmar `main`, merge-base, ahead/behind, diff, mergeabilidade, issue #57 e concorrência;
8. parar para aceite explícito.

## 19. Ponto de parada

S6 permanece não iniciada.

A S5 só poderá ser integrada depois de:

- certificação do HEAD final exato;
- preservação dos failures intermediários;
- `main` sem divergência não tratada;
- PR mergeável;
- issue #57 preservada;
- aceite explícito do mantenedor.

**Não iniciar S6 por esta PR.**
