# Checkpoint V13 — S6: ensaios operacionais por superfície

Data: 16/09/2026.

Branch: `codex/temas-v13-s6-ensaios-operacionais-20260916`.

Estado deste documento: **candidata S6 em certificação final**. Este checkpoint consolida o escopo, as decisões, os failures intermediários e a certificação observada até o HEAD `b9e11db2be94bde6dc2a39eeb1b60206f408153a`. Como a atualização deste próprio arquivo cria um novo HEAD, a certificação desse SHA anterior não é transferida automaticamente: o SHA resultante desta atualização precisa ser recertificado integralmente antes de aceite ou integração.

## 1. Baseline de abertura

A S6 só foi iniciada depois do fechamento completo da S5:

- S5 aceita e integrada pela PR #64;
- merge S5 na `main`: `11e4e17f02d4ba7846f5b80bd88c0180124b5772`;
- pós-merge S5: **16/16 workflows de `push` concluídos com `success`**;
- branch S6 criada diretamente desse merge certificado;
- nenhuma mutação Databricks foi autorizada ou executada para abrir a S6;
- S7 não foi iniciada.

O aceite para iniciar a S6 não foi interpretado como autorização para reexecutar operações remotas V12.

## 2. Escopo canônico recuperado do Plano Mestre

A S6 implementa exclusivamente **ensaios operacionais por superfície**.

Ciclo canônico:

`PREPARE → PREFLIGHT → PACKAGE → STAGE → VERIFY → ROLLBACK`

Ordem preferencial preservada:

1. notebook/Plotly/HTML local;
2. Visual Lab local/simulado;
3. bundle V09;
4. App V10 em build/dry-run local;
5. AI/BI V11 com fixtures/export real somente quando já disponível e autorizado;
6. ambiente Databricks real somente com autorização específica.

Nesta candidata, as cinco primeiras rotas são exercitadas localmente ou com fixtures. O ambiente Databricks real permanece fora do alcance autorizado.

Gates canônicos preservados:

- invariantes de dados e semântica;
- idempotência onde aplicável;
- rollback verificável;
- evidência sanitizada;
- nenhuma publicação implícita;
- PASS local não é promovido a PASS remoto.

## 3. Owners reutilizados

A S6 não cria segunda implementação funcional.

Owners compostos:

- notebook: V02 + V03 + V04;
- Visual Lab: V05;
- bundle de transição: V09 + S2 + S3;
- App: V10 + S2 + S3;
- AI/BI: V11 + S2;
- workspace theme: V11 + S2, somente para provar o bloqueio canônico.

A matriz S1 permanece o inventário canônico das superfícies. A S6 registra execução; não substitui `MATRIZ_OPERACIONAL.json`.

## 4. Artefatos da candidata

A S6 adiciona:

- `tools/temas_v13_ensaios.py`;
- `tools/tests/test_temas_v13_s6.py`;
- `docs/sprints/sistema_temas/V13/S6_ENSAIOS_OPERACIONAIS.md`;
- este checkpoint.

Também evolui:

- `.github/workflows/temas-v13-ci.yml`;
- `docs/sprints/sistema_temas/V13/README.md`;
- `tools/tests/test_temas_v13_s5.py`, somente para transformar a antiga guarda de transição “S6 não iniciada” em evidência histórica e exigir S5 integrada/S6 vigente/S7 não iniciada;
- `README.md`, somente depois de medição real do runner.

Não houve alteração em:

- `ambiente_fonte/`;
- `Novo_Ambiente_Simulado/`;
- schema ou tokens;
- matriz S1;
- engines S2, S3, S4 ou S5;
- App V10;
- binder V11;
- contratos funcionais V01–V12.

## 5. Ensaio notebook/Plotly/HTML

A rota local:

- carrega `ResolvedTheme` notebook pelo owner V02;
- executa preflight S2 para a rota notebook;
- exporta o tema em memória;
- aplica V03 somente a uma cópia da figura Plotly;
- renderiza KPI V04 com o mesmo tema;
- verifica preservação de dados, eixos, range, cor explícita da série e default Plotly global;
- prova rollback pelo descarte do stage, mantendo o original inalterado.

Esse PASS é local e não representa homologação Databricks.

## 6. Ensaio Visual Lab

A rota usa somente preset sintético V05:

- preflight S2 de `preview_proposal`;
- criação de draft;
- alteração validada de token;
- save em diretório temporário;
- reopen e verificação do fingerprint da proposta;
- `restore()` e verificação do fingerprint da base;
- descarte do diretório temporário.

Isso prova o roundtrip local V05.

`V12-LAB-01 = BLOQUEADO_AUTORIZACAO` permanece inalterado.

## 7. Ensaio bundle V09

A S6 reutiliza o builder canônico `tools/bundle_implantacao.py`.

O artefato temporário:

- é criado sob `.artifacts/`;
- passa pelo preflight S2;
- entra no ciclo local S3;
- é staged e verificado pelo owner V09;
- executa rollback dry-run local;
- é removido com o diretório temporário.

Transporte continua distinto de instalação, ativação ou publicação.

## 8. Ensaio App V10

A S6 reutiliza `tools/temas_v10_app.py` para build do bundle local.

Depois:

- executa S2 para `build_app_bundle`;
- executa S3 em modo local;
- comprova staging temporário;
- revalida o bundle V10;
- comprova rollback dry-run local.

`deploy_app` não é executado.

`V12-APP-01 = BLOQUEADO_AUTORIZACAO` permanece inalterado.

## 9. Ensaio AI/BI V11

A rota local:

- carrega tema notebook V02;
- executa `project_theme()`;
- exporta a projeção V11;
- aplica somente os três bindings diretos autorizados a um template local com caminhos existentes;
- preserva campo desconhecido;
- usa `dashboard_sintetico.json` somente para fingerprint semântico, nunca como import nativo;
- prova que adicionar identidade de projeção não altera queries/filtros;
- prova rollback descartando a cópia bound.

Continuam congelados:

- `ResolvedTheme` como fonte configurável de verdade;
- 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- `context="aibi"` reservado;
- bindings diretos limitados a `surface.card -> widget.background`, `palette.categorical -> visualization.categorical_palette` e `card.radius_px -> widget.corner_radius`;
- `dashboard_sintetico.json` não é import nativo;
- `cellFormat` não vira token;
- `approximated`/`unsupported` não são automatizados;
- dashboard theme e workspace theme permanecem superfícies distintas;
- `Import theme` e `Publish` permanecem gates distintos.

O PASS histórico `V12-AIBI-01` não é reexecutado nem ampliado por este ensaio local.

## 10. Workspace theme e Databricks real

A S6 executa somente o preflight local S2 para a ação de workspace theme e exige `BLOCKED`.

As fases remotas posteriores ficam `NOT_APPLICABLE`, não PASS, porque nenhuma mutação ocorreu.

Sem nova autorização específica permanecem fora do alcance:

- alterar workspace theme;
- importar tema em dashboard real;
- publicar dashboard;
- criar ou atualizar Databricks App;
- alterar ACL/grupos;
- persistir sessão em workspace;
- criar/alterar UC Volume;
- qualquer outra mutação Databricks.

## 11. Estados herdados preservados

A candidata mantém separadamente:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 já evidenciado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Os três casos ambientais bloqueados aparecem explicitamente no relatório S6 como `BLOQUEADO_AUTORIZACAO`. Nenhum é contado como PASS ou SKIP.

`A11-01 = FAIL` continua verdadeiro e a issue #57 permanece aberta até correção + nova evidência aplicável.

## 12. Fronteira operacional

O núcleo S6 não importa cliente Databricks nem bibliotecas de rede.

O uso de `subprocess` é limitado à chamada local do builder canônico V09; não executa CLI Databricks, rede ou shell remoto.

O workflow permanece:

- `permissions: contents: read`;
- checkout `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

Fronteiras vivas S6:

- `V13_S6_NETWORK=0`;
- `V13_S6_REMOTE_MUTATION=0`;
- `V13_S6_IMPLICIT_PUBLICATION=0`;
- `V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5`;
- `V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3`;
- `V13_S7_NOT_STARTED=1`.

A antiga asserção `V13_S6_NOT_STARTED=1` permanece somente como comentário histórico da S5.

## 13. Suíte permanente S6

`tools/tests/test_temas_v13_s6.py` contém **28 testes**.

A cobertura inclui:

- identidade/versão/escopo do relatório;
- ordem exata das seis superfícies;
- seis fases explícitas por superfície;
- cinco ensaios locais/simulados em PASS;
- workspace theme em BLOCKED;
- invariantes notebook e rollback por descarte;
- save/reopen/restore V05;
- stage/verify/rollback V09;
- stage/verify/rollback V10;
- binding local V11 e invariantes semânticos;
- exatamente três casos ambientais bloqueados;
- A11 FAIL e issue #57 preservados;
- S7 não iniciada;
- sem rede/mutação remota/publicação;
- evidência sanitizada e relativa ao repositório;
- ausência de caminhos temporários, segredo, e-mail/PII;
- vocabulário fechado de status;
- ausência de inferência de PASS remoto;
- ausência de imports de rede/cliente Databricks;
- subprocess restrito ao builder local V09;
- documentação e workflow S6;
- ausência de artefato S6 em produto/simulado;
- serialização JSON determinística do relatório.

## 14. First head — failure S5 preservado

Primeiro HEAD S6:

`86543855ae10453eb25ba87c179c9189b3510d20`.

Workflows observados:

- V00 `35089624398` — `success`;
- V02 `35089624342` — `success`;
- V01 `35089624444` — `success`;
- V13 `35089624432` — `failure`;
- CI geral `35089624364` — `failure`.

No V13:

- S1–S4: PASS;
- S5: **31/32**;
- única falha S5: guarda de transição ainda exigia literalmente “S6 não foi iniciada” no README vivo;
- step S6: `skipped`;
- regressões posteriores, V00, validador e fronteiras: `skipped`.

Portanto **não existe PASS S6 nesse HEAD**.

No CI geral houve duas causas independentes:

1. suíte `temas` falhou pela mesma guarda S5 desatualizada;
2. validador mediu **1451 arquivos / 1920 links**, enquanto o README ainda declarava 1448/1918 — **2 divergências documentais / 0 avisos**.

Os demais grupos aplicáveis do CI passaram. O failure permanece histórico.

## 15. Correção de transição S5

Commit:

`f8e311524abef36ae86ae5cd0c88ed3b14079cef`.

Alteração exclusiva:

`tools/tests/test_temas_v13_s5.py`.

A guarda passou a exigir:

- S5 integrada pela PR #64;
- merge S5 `11e4e17f02d4ba7846f5b80bd88c0180124b5772` registrado;
- S6 vigente;
- S7 não iniciada.

Nenhum teste funcional S5, contrato S5, gate ou allowlist foi relaxado.

## 16. Segundo head — failure de bootstrap S6 preservado

HEAD:

`f8e311524abef36ae86ae5cd0c88ed3b14079cef`.

Workflows:

- V02 `35089942965` — `success`;
- V00 `35089942930` — `success`;
- V01 `35089942920` — `success`;
- V13 `35089942925` — `failure`;
- CI geral `35089942927` — `failure`.

No V13:

- S1–S5: PASS;
- S5: **32/32 PASS**;
- step S6 falhou antes de executar qualquer teste com `ModuleNotFoundError: No module named 'tools'` ao invocar diretamente `tools/tests/test_temas_v13_s6.py`;
- regressões, V00, validador e fronteiras posteriores: `skipped`.

Portanto **os 28 testes S6 não foram executados nesse HEAD**.

O failure permanece registrado como problema de bootstrap da suíte, não como PASS parcial.

## 17. Correção de bootstrap S6

Commit:

`3e8720a537978fd01fea84b26a551420ada26311`.

Alteração exclusiva:

`tools/tests/test_temas_v13_s6.py`.

Correção:

- adiciona a raiz do repositório a `sys.path` antes do import `tools.temas_v13_ensaios` quando a suíte é executada diretamente;
- engine S6 e asserts funcionais permanecem inalterados.

## 18. Terceiro head — implementação funcional verde, documentação divergente

HEAD:

`3e8720a537978fd01fea84b26a551420ada26311`.

Workflows:

- V01 `35090259962` — `success`;
- V02 `35090260151` — `success`;
- V00 `35090259765` — `success`;
- CI geral `35090259806` — `failure`;
- V13 `35090259861` — `failure`.

No V13:

- S1: **20/20 PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- S4: **30/30 PASS**;
- S5: **32/32 PASS**;
- S6: **28/28 PASS**;
- regressões V01–V13: **673/673 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: FAIL somente por README 1448/1918 versus medição real **1451/1920**;
- fronteiras S1–S6: `skipped`, não PASS.

No CI geral:

- `temas`: PASS;
- `validacao`: FAIL — **2 falhas / 0 avisos**, somente métricas README;
- biblioteca: PASS;
- ferramentas: PASS;
- transição: PASS nos testes executados, com skips opcionais preservados;
- READMEs: PASS;
- Concierge: somente os gates locais aplicáveis; nada disso homologa roteamento/Databricks/permissões reais.

Esse HEAD é a primeira evidência funcional completa da S6, mas não é candidato final por causa do drift documental.

## 19. Reconciliação medida pré-checkpoint

Commit/HEAD:

`fccbc5c33052a541b90c2022a1020454ac9278b0`.

Alteração exclusiva:

`README.md` raiz.

Mudanças:

- estado vivo reconciliado para S5 integrada/S6 candidata;
- `repo (identidade)` de 1448 para **1451**;
- `repo (links)` de 1918 para **1920**.

Nenhum gate, contrato, allowlist ou suíte foi relaxado.

## 20. Certificação do HEAD pré-checkpoint

O SHA `fccbc5c33052a541b90c2022a1020454ac9278b0` acionou 8 workflows reais de PR, todos concluídos com `success`:

- V00 `35090730140`;
- V01 `35090730128`;
- V02 `35090730138`;
- V10 `35090730141`;
- V11 `35090730127`;
- V12 `35090730136`;
- V13 `35090730137`;
- CI geral `35090730130`.

No V13, no mesmo SHA:

- S1: **20/20 PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- S4: **30/30 PASS**;
- S5: **32/32 PASS**;
- S6: **28/28 PASS**;
- regressões V01–V13: **673/673 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: **APROVADO — 0 falhas / 0 avisos**;
- métricas: **1451 arquivos / 1920 links**;
- worktree extras: 0;
- fronteiras S1–S6: `success`.

## 21. Preservação V12 no HEAD pré-checkpoint

Workflow V12 `35090730136`:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões transversais: **673/673 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- métricas: **1451/1920**;
- aplicabilidade do escopo estrito: `success` com `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

A allowlist V12 não foi ampliada.

## 22. Head com checkpoint — failure documental preservado

A inclusão deste arquivo produziu o HEAD:

`f9cbdfcc30ef5556526c3874cb45b022bf354993`.

Workflows observados:

- V00 `35091303955` — `success`;
- V01 `35091303868` — `success`;
- V02 `35091303928` — `success`;
- CI `35091303978` — `failure`;
- V10 `35091303975` — `failure`;
- V11 `35091303906` — `failure`;
- V12 `35091303930` — `failure`;
- V13 `35091303968` — `failure`.

No V13:

- S1: **20/20 PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- S4: **30/30 PASS**;
- S5: **32/32 PASS**;
- S6: **28/28 PASS**;
- regressões V01–V13: **673/673 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador mediu **1452 arquivos / 1920 links** e falhou somente porque o README ainda declarava 1451 arquivos;
- fronteiras S1–S6: `skipped`, não PASS.

No CI geral, os grupos funcionais passaram; o validador teve **1 falha / 0 avisos**, exclusivamente `repo (identidade)` 1451→1452.

No V10/V11/V12, as suítes próprias e regressões anteriores ao validador passaram; os steps posteriores ao validador ficaram `skipped` quando aplicável.

Nenhum failure funcional S6 foi observado nesse HEAD.

## 23. Reconciliação medida pós-checkpoint

Commit/HEAD:

`b9e11db2be94bde6dc2a39eeb1b60206f408153a`.

Alteração exclusiva desse commit:

`README.md` raiz.

Mudanças:

- pós-merge S5 corrigido de 15/15 para **16/16 workflows de `push` com `success`**;
- `repo (identidade)` de 1451 para **1452**;
- `repo (links)` mantido em **1920**.

Nenhum gate, contrato, allowlist ou suíte foi relaxado.

## 24. Certificação do HEAD reconciliado

O SHA `b9e11db2be94bde6dc2a39eeb1b60206f408153a` acionou 8 workflows reais de PR, todos concluídos com `success`:

- V00 `35094080674` — `success`;
- V01 `35094080602` — `success`;
- V02 `35094080564` — `success`;
- V10 `35094080572` — `success`;
- V11 `35094080638` — `success`;
- V12 `35094080570` — `success`;
- V13 `35094080568` — `success`;
- CI geral `35094080575` — `success`.

No V13, no mesmo SHA:

- S1: **20/20 PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- S4: **30/30 PASS**;
- S5: **32/32 PASS**;
- S6: **28/28 PASS**;
- regressões V01–V13: **673/673 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: **APROVADO — 0 falhas / 0 avisos**;
- métricas: **1452 arquivos / 1920 links**;
- worktree extras: 0;
- fronteiras S1/S2/S3/S4/S5/S6: `success`;
- `V13_S6_NETWORK=0`;
- `V13_S6_REMOTE_MUTATION=0`;
- `V13_S6_IMPLICIT_PUBLICATION=0`;
- `V13_S6_LOCAL_OR_SIMULATED_REHEARSALS=5`;
- `V13_S6_REAL_ENVIRONMENT_CASES_BLOCKED=3`;
- `V13_S7_NOT_STARTED=1`.

## 25. Preservação V12 no HEAD reconciliado

Workflow V12 `35094080570`, no mesmo SHA:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões transversais: **673/673 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- métricas: **1452/1920**;
- aplicabilidade do escopo estrito: `success` com `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

A allowlist V12 não foi ampliada.

## 26. Ausência de mutação Databricks

A S6 não executou:

- deploy de App;
- ACL/grupos;
- workspace theme;
- `Import theme` remoto;
- `Publish`;
- edição de dashboard real;
- persistência no workspace;
- criação/alteração de UC Volume;
- qualquer outra mutação Databricks.

Os três casos ambientais V12 permanecem `BLOQUEADO_AUTORIZACAO` e exigem autorização específica própria para eventual reexecução.

Git/CI continuam evidência técnica, não homologação de ambiente.

## 27. Efeito desta atualização do checkpoint

Esta atualização modifica um caminho já versionado e não adiciona um novo arquivo. Mesmo assim, ela cria um novo commit e um novo HEAD.

Por isso, a certificação 8/8 do HEAD `b9e11db2...` é evidência histórica imediatamente anterior, não certificação automática do novo SHA.

O próximo gate é:

1. observar todos os workflows do novo SHA;
2. confirmar a medição real do validador;
3. preservar qualquer failure, caso apareça;
4. reconfirmar `main`, merge-base, ahead/behind, diff, mergeabilidade, issue #57 e concorrência;
5. atualizar a descrição da PR com o SHA final exato sem alterar a branch;
6. parar para aceite explícito.

## 28. Ponto de parada

S7 permanece não iniciada.

A S6 só poderá ser integrada depois de:

- certificação do HEAD final exato;
- preservação dos failures intermediários;
- `main` sem divergência não tratada;
- PR mergeável;
- issue #57 preservada;
- três casos ambientais V12 ainda bloqueados sem autorização nova;
- aceite explícito do mantenedor.

**Não iniciar S7 por esta PR.**
