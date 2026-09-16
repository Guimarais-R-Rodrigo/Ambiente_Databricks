# Checkpoint V13 — S4: observabilidade e diagnóstico

Data: 16/09/2026.

Branch: `codex/temas-v13-s4-observabilidade-diagnostico-20260916`.

Estado deste documento: **candidata S4 em certificação final**. O HEAD imediatamente anterior à criação deste checkpoint, `c769812fe9b34d96d81eef08e9bbd9a737d9f72b`, concluiu 8/8 workflows de PR com `success`. Como este checkpoint acrescenta um arquivo à árvore, o novo HEAD precisa ser medido e certificado novamente antes de qualquer aceite.

## 1. Baseline de abertura

A S4 só foi iniciada depois do fechamento completo da S3:

- S3 aceita e integrada pela PR #62;
- merge S3 na `main`: `298dfb986f67cc4c560ae22b59d2fccad0716ec0`;
- pós-merge S3: **15/15 workflows de `push` com `success`**;
- branch S4 criada diretamente desse merge certificado;
- nenhuma mutação Databricks foi autorizada ou executada pela S4;
- S5 não foi iniciada.

A S4 não reutilizou a branch S3 como base paralela.

## 2. Escopo canônico recuperado do Plano Mestre

A S4 implementa exclusivamente **observabilidade e diagnóstico**.

Entregáveis canônicos:

- taxonomia de falhas;
- relatório sanitizado de execução;
- runbook de diagnóstico;
- checklist de evidência;
- logging sem PII/segredo.

Gates canônicos:

- cada classe de falha possui fixture ou mutante;
- mensagem/log não ecoa conteúdo sensível;
- logs distinguem `PASS`, `BLOCKED`, `FAIL` e `NOT_APPLICABLE`;
- diagnóstico não altera ambiente;
- ausência de evidência nunca é promovida a PASS.

Compatibilidade/acessibilidade operacional pertence à S5 e não foi antecipada.

## 3. Artefatos próprios da candidata

A S4 adiciona:

- `tools/temas_v13_diagnostico.py`;
- `tools/tests/test_temas_v13_s4.py`;
- `docs/sprints/sistema_temas/V13/S4_OBSERVABILIDADE_DIAGNOSTICO.md`;
- este checkpoint.

Também evolui:

- `.github/workflows/temas-v13-ci.yml`;
- `docs/sprints/sistema_temas/V13/README.md`;
- `README.md`, somente depois da primeira medição real do runner.

Não houve alteração em `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, matriz S1, preflight S2, executor S3, schema/tokens, App V10, binder V11 ou contratos funcionais V01–V12.

## 4. Decisão arquitetural

A S4 é uma camada de diagnóstico local/read-only. Ela não reexecuta a operação e não cria um novo executor.

Entradas suportadas:

- relatório estruturado `V13-S2`;
- relatório estruturado `V13-S3`;
- lista sanitizada de classes de evidência.

A S4 não aceita texto livre como autoridade diagnóstica.

Os códigos de origem aceitos são espelhados somente para validação de entrada. A suíte exige igualdade exata entre o registry S4 e `STABLE_CODES` dos owners S2/S3. Qualquer drift faz a suíte falhar fechado.

## 5. Estados preservados

A S4 reutiliza exatamente os quatro estados existentes:

- `PASS`;
- `BLOCKED`;
- `FAIL`;
- `NOT_APPLICABLE`.

Não existe score, nota, severidade, “PASS parcial”, incidente, SLA ou SLO.

Prioridade fail-closed:

`FAIL > BLOCKED > PASS > NOT_APPLICABLE`.

Consequências:

- uma lacuna de evidência pode tornar source `PASS` em diagnóstico `BLOCKED`;
- uma lacuna de evidência nunca apaga source `FAIL`;
- `NOT_APPLICABLE` nunca é contado como PASS.

## 6. Taxonomia de falhas

A candidata define 11 classes diagnósticas:

1. `INPUT_CONTRACT`;
2. `CANONICAL_CONTRACT`;
3. `ARTIFACT_INTEGRITY`;
4. `GIT_STATE`;
5. `PREFLIGHT_READINESS`;
6. `GOVERNANCE_AUTHORIZATION`;
7. `ENVIRONMENT_IDENTITY`;
8. `RECOVERY_ROLLBACK`;
9. `COMPATIBILITY_LKG`;
10. `STAGING_EXECUTION`;
11. `EVIDENCE_GAP`.

A classe `stage` não substitui `safe_code`; o código do owner é preservado quando registrado.

Cada classe tem fixture/mutante permanente na suíte S4.

## 7. Evidência

Kinds sanitizados:

- `git_ci`;
- `artifact`;
- `authorization`;
- `environment_identity`;
- `rollback`;
- `human`;
- `browser_runtime`.

States sanitizados:

- `REFERENCED`;
- `MISSING`;
- `NOT_APPLICABLE`.

A S4 não recebe o valor da referência sensível. Ela não autentica a prova e declara explicitamente:

`references_authenticated = false`.

Para source `PASS`, a candidata exige `git_ci = REFERENCED` como evidência mínima; se faltar, o diagnóstico torna-se `BLOCKED`.

## 8. Logging sem PII/segredo

O `safe_log` é derivado apenas de enums/códigos previamente conhecidos:

`NNN|STATUS|STAGE|SAFE_CODE[|EVIDENCE_KIND]`

A saída não ecoa:

- `message` de origem;
- `check_id`;
- conteúdo arbitrário do `receipt`;
- path local ou `/Volumes/...`;
- `authorization_ref`;
- `identity_ref`;
- `state_ref`;
- `acceptance_ref`;
- token/PAT/secret;
- e-mail/username/workspace id.

Código desconhecido vira `SOURCE_CODE_UNREGISTERED` sem reproduzir o valor recebido.

A suíte injeta uma string com formato de token, e-mail e path privado e verifica que ela não aparece no diagnóstico.

## 9. Coerência fail-closed

A S4 recusa:

- engine fora de S2/S3;
- shape divergente;
- status desconhecido;
- código não registrado;
- status de operação S2 incompatível com seus checks;
- `overall_status` incompatível com checks;
- S3 PASS sem receipt;
- S3 não-PASS com receipt de sucesso;
- relatório que declare rede ou mutação remota;
- S3 que declare publicação;
- evidence kind/state desconhecido;
- evidence kind duplicado.

A candidata valida coerência da referência declarada, não autenticidade da evidência externa.

## 10. Fronteira operacional

O núcleo S4 não importa:

- `requests`;
- `socket`;
- `urllib`;
- `httpx`;
- cliente `databricks`;
- `subprocess`;
- `shutil`.

Não há rede, shell, Git, escrita de artefato ou mutação remota no diagnóstico.

O workflow permanece `contents: read`, com checkout `persist-credentials: false` e sem credenciais Databricks.

Fronteiras vivas:

- `V13_S4_NETWORK=0`;
- `V13_S4_REMOTE_MUTATION=0`;
- `V13_S4_DIAGNOSIS_READ_ONLY=1`;
- `V13_S5_NOT_STARTED=1`.

A asserção histórica `V13_S4_NOT_STARTED=1` permanece apenas como comentário no step S3 do workflow, para preservar o checkpoint histórico S3 sem representar o estado vivo.

## 11. Suíte permanente S4

`tools/tests/test_temas_v13_s4.py` contém **30 testes**.

Cobertura:

- registry S2 igual ao owner;
- registry S3 igual ao owner;
- fixture/mutante para todas as 11 classes;
- falta de evidência vira BLOCKED;
- evidência referenciada não é autenticada;
- FAIL de origem não é ocultado por gap;
- NOT_APPLICABLE permanece distinto;
- safe log diferencia os quatro estados;
- segredo/PII/path em message/check_id/receipt não é ecoado;
- código desconhecido é recusado sem eco;
- mismatch de overall status;
- mismatch de status de operação S2;
- violação de fronteira;
- S3 PASS sem receipt;
- S3 não-PASS com receipt;
- evidence shape/kind/state/duplicidade inválidos;
- determinismo;
- cobertura de todas as classes;
- ausência de rede/cliente/mutação;
- workflow read-only;
- documentação dos cinco entregáveis S4.

## 12. First head e failure preservado

Primeiro HEAD S4:

`ffc80e08ffeab4d7a67dea39892bc34becc4cd19`.

Workflows disparados:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35075638943` | `success` |
| Contrato de temas V01 | `35075638940` | `success` |
| Núcleo de temas V02 | `35075638949` | `success` |
| CI local reproduzível | `35075638986` | `failure` |
| Contrato operacional V13 | `35075639053` | `failure` |

No V13 first head:

- S1: PASS;
- validador S1: PASS;
- S2: PASS;
- S3: PASS;
- S4: PASS;
- regressões V01–V13: PASS;
- compatibilidade V00: PASS;
- validador estrutural/documental: FAIL somente por métricas README;
- fronteiras S1/S2/S3/S4: `skipped`, não PASS.

No CI geral first head:

- suíte `temas`: PASS;
- biblioteca: PASS;
- ferramentas: PASS;
- transição: PASS;
- READMEs: PASS;
- Concierge: PASS nos gates aplicáveis;
- validador mediu **1443 arquivos / 1916 links**;
- README raiz ainda declarava 1440/1914;
- única causa do failure: duas divergências documentais de métrica;
- nenhuma falha funcional S4 foi observada.

O failure permanece histórico e não foi reclassificado.

## 13. Correção aditiva do first head

Commit:

`c769812fe9b34d96d81eef08e9bbd9a737d9f72b`.

Alteração exclusiva: `README.md` raiz.

Mudanças:

- estado vivo reconciliado para S3 integrada/S4 candidata;
- `repo (identidade)` de 1440 para **1443**;
- `repo (links)` de 1914 para **1916**.

Nenhum gate, allowlist, contrato ou suíte foi relaxado.

## 14. Certificação do segundo head

O SHA `c769812fe9b34d96d81eef08e9bbd9a737d9f72b` acionou 8 workflows reais de PR, todos concluídos com `success`:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35075971893` | `success` |
| Contrato de temas V01 | `35075971976` | `success` |
| Núcleo de temas V02 | `35075972034` | `success` |
| CI local reproduzível | `35075971981` | `success` |
| Databricks App V10 | `35075971884` | `success` |
| Temas nativos AI/BI V11 | `35075971972` | `success` |
| Homologação V12 | `35075971878` | `success` |
| Contrato operacional V13 | `35075971892` | `success` |

No V13, no mesmo SHA:

- S1: **20/20 PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- S4: **30/30 PASS**;
- regressões V01–V13: **613/613 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador estrutural/documental: **APROVADO — 0 falhas / 0 avisos**;
- métricas: **1443 arquivos / 1916 links**;
- worktree extras: 0;
- fronteira S1: PASS;
- fronteira S2: PASS;
- fronteira S3: PASS;
- fronteira S4: PASS.

## 15. Preservação V12 no segundo head

Workflow V12: `35075971878`.

No mesmo SHA:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões transversais: **613/613 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**;
- métricas: **1443/1916**;
- aplicabilidade do escopo estrito: `success` com saída `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

A allowlist V12 não foi ampliada.

## 16. Estados herdados preservados

A S4 mantém separadamente:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` somente no alcance observado;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 já evidenciado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

A S4 não fecha, reclassifica ou mascara a issue #57.

A decisão operacional sobre compatibilidade/acessibilidade de `A11-01` pertence à S5.

## 17. Ausência de mutação Databricks

A S4 não executou:

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

Este arquivo é um novo caminho versionado. Portanto, as métricas **1443/1916** pertencem ao HEAD anterior `c769812f...` e **não são presumidas para o HEAD que contém este checkpoint**.

O próximo gate é:

1. observar todos os workflows do novo SHA;
2. registrar a medição real do validador;
3. preservar qualquer failure de métrica;
4. corrigir o README raiz somente com a saída real;
5. recertificar o SHA resultante;
6. reconfirmar `main`, merge-base, ahead/behind, diff, mergeabilidade, issue #57 e concorrência;
7. parar para aceite explícito.

## 19. Medição do head com checkpoint

HEAD medido:

`5d0067157f2f1c38182e73a1ac6f85ce3937e5d1`.

Workflows observados:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35076472206` | `success` |
| Contrato de temas V01 | `35076472123` | `success` |
| Núcleo de temas V02 | `35076472296` | `success` |
| CI local reproduzível | `35076472185` | `failure` |
| Databricks App V10 | `35076472144` | `failure` |
| Temas nativos AI/BI V11 | `35076472202` | `failure` |
| Homologação V12 | `35076472132` | `failure` |
| Contrato operacional V13 | `35076472111` | `failure` |

O runner mediu **1444 arquivos / 1916 links**. O checkpoint acrescentou exatamente um arquivo e nenhum link novo.

No CI geral:

- suíte `temas`: PASS;
- biblioteca, ferramentas, transição, READMEs e Concierge aplicável: PASS;
- validador: **1 falha / 0 avisos**;
- única divergência: README ainda declarava 1443 arquivos enquanto a árvore real possuía 1444;
- links permaneceram 1916;
- worktree extras: 0.

No V13:

- S1: PASS;
- S2: PASS;
- S3: PASS;
- S4: PASS;
- regressões V01–V13: PASS;
- compatibilidade V00: PASS;
- validador estrutural/documental: FAIL somente em 1443→1444;
- fronteiras S1/S2/S3/S4: **skipped**, não PASS.

No V12:

- protocolo/mutantes: PASS;
- evidência real: PASS;
- regressões transversais: PASS;
- compatibilidade V00: PASS;
- validador: FAIL somente em 1443→1444;
- aplicabilidade do escopo estrito: **skipped**;
- `Escopo V12 e higiene`: **skipped**.

Neste SHA não se declara `V12_SCOPE=NOT_APPLICABLE`, porque o passo de aplicabilidade não chegou a executar após a falha do validador.

A correção final deve alterar somente o snapshot do README de **1443 para 1444**, mantendo **1916 links**, sem adicionar arquivo nem expandir qualquer gate/allowlist.

## 20. Ponto de parada

S5 permanece não iniciada.

A S4 só poderá ser integrada depois de:

- certificação do HEAD final exato;
- preservação dos failures intermediários;
- `main` sem divergência não tratada;
- PR mergeável;
- issue #57 preservada;
- aceite explícito do mantenedor.

**Não iniciar S5 por esta PR.**
