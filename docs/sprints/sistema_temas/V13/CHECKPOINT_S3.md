# Checkpoint V13 — S3: release, instalação, atualização e rollback

Data: 15/09/2026.

Branch: `codex/temas-v13-s3-release-operacional-20260915`.

Estado deste documento: **candidata S3 em certificação final**. O HEAD imediatamente anterior à criação deste checkpoint, `135b875bedb826fae62f9400d54650f2d7a8015e`, concluiu 8/8 workflows de PR com `success`. Como este checkpoint acrescenta um arquivo à árvore, o novo HEAD precisa ser medido e certificado novamente antes de qualquer aceite.

## 1. Baseline de abertura

A S3 só foi iniciada depois do fechamento completo da S2:

- S2 aceita e integrada pela PR #61;
- merge S2 na `main`: `76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`;
- árvore do merge S2 idêntica à árvore candidata certificada;
- pós-merge S2: **15/15 workflows de `push` com `success`**;
- branch S3 criada diretamente do merge certificado;
- nenhuma mutação Databricks foi autorizada ou executada pela S3;
- S4 não foi iniciada.

A S3 não reutilizou a branch S2 como base paralela.

## 2. Escopo canônico recuperado do Plano Mestre

A S3 implementa exclusivamente **release, instalação, atualização e rollback**.

Entregáveis canônicos:

- runbook de release;
- runbook de instalação/atualização;
- runbook de rollback;
- checklist de staging;
- estratégia de identificação de last-known-good (LKG).

Gates canônicos:

- release parte de árvore limpa;
- artefato derivado é reproduzível no alcance definido pelo contrato;
- bundle adulterado é recusado;
- versão incompatível de update é recusada;
- rollback dry-run restaura bytes/estado esperado;
- falha intermediária não gera falso recibo de sucesso.

A taxonomia formal de observabilidade/diagnóstico pertence à S4 e não foi antecipada.

## 3. Artefatos próprios da candidata

A S3 adiciona:

- `tools/temas_v13_release.py`;
- `tools/tests/test_temas_v13_s3.py`;
- `docs/sprints/sistema_temas/V13/S3_RELEASE_OPERACIONAL.md`;
- este checkpoint.

Também evolui:

- `.github/workflows/temas-v13-ci.yml`;
- `docs/sprints/sistema_temas/V13/README.md`;
- `README.md`, apenas depois da primeira medição real do runner.

Não houve alteração em `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, schema/tokens, matriz S1, executor S1, preflight S2, App V10, binder V11 ou contratos funcionais V01–V12.

## 4. Decisão arquitetural

A S3 é uma camada de orquestração local/dry-run. Ela não cria um segundo sistema de empacotamento, deploy ou publicação.

Owners reutilizados:

- V02: tema, schema, hash e contexto;
- V09: bundle de transição e `theme_contract`;
- V10: bundle do App e verificador;
- contrato V10 `DEPLOY_ROLLBACK.md`: procedimento remoto de App e estratégia de commit anterior ainda aprovado;
- V11: fronteiras AI/BI;
- V12: evidência e homologação;
- matriz S1: superfície, ação, autorização e rollback;
- S2: readiness/preflight.

A S3 não copia tokens, papéis, bindings, schema, manifesto de implantação ou política de publicação.

## 5. Ciclo operacional implementado

A ferramenta local cobre:

`PREPARE → PREFLIGHT → PACKAGE/VERIFY → STAGE → VERIFY → ROLLBACK dry-run`

Ela **não** executa `APPLY` remoto nem transforma CI em `ACCEPT` de ambiente.

`READY_FOR_AUTHORIZED_APPLY` significa somente que o ciclo local terminou corretamente. O recibo S3 **não autoriza** aplicação remota.

## 6. Tipos de artefato suportados

### `transition_bundle`

Owner: V09.

A S3 exige:

- caminho sob `.artifacts/`;
- `validate_theme_zip()` aprovado;
- `worktree_dirty = false`;
- `source_commit` válido e igual ao checkout atual;
- `theme_contract` válido;
- fingerprint de conteúdo derivado do inventário ordenado `path + sha256 + bytes`.

O ZIP V09 inclui metadados como timestamp. Por isso a S3 não afirma byte-identidade do container inteiro entre gerações; prova reprodutibilidade no nível do conteúdo contratado.

### `app_bundle`

Owner: V10.

A S3 exige:

- caminho sob `.artifacts/`;
- `tools.temas_v10_app.verify()` aprovado;
- `source_commit` igual ao checkout;
- fingerprint de conteúdo do manifesto.

A suíte comprova que duas gerações V10 no mesmo commit produzem o mesmo fingerprint de conteúdo.

## 7. Árvore limpa e Git

O executor usa Git somente para leitura:

- `git rev-parse HEAD`;
- `git status --porcelain --untracked-files=all`.

Árvore suja retorna `TREE_DIRTY` e encerra o ciclo sem recibo.

A S3 não executa `push`, `reset`, `checkout`, `clean`, `add` ou `commit`.

## 8. Composição obrigatória com o preflight S2

O request S3 carrega um request S2.

A S3 exige que o preflight esteja fixado ao **mesmo artefato e à mesma ação local**:

- V09 → `transition_bundle/build_transition_bundle` + mesmo `bundle_path`;
- V10 → `databricks_app/build_app_bundle` + mesmo `app_bundle_dir`.

Preflight `BLOCKED` continua `BLOCKED`.

Preflight `FAIL` continua `FAIL`.

A S3 nunca promove um estado S2 não-PASS a sucesso.

## 9. Last known good

Update e rollback dry-run exigem LKG.

A referência técnica contém:

- `kind`;
- caminho local sob `.artifacts/`;
- `source_commit`;
- `artifact_fingerprint`;
- `acceptance_ref`.

A ferramenta reabre e revalida os bytes reais antes de confiar em commit/fingerprint.

`acceptance_ref` é apenas referência sanitizada a um aceite anterior. A S3 não autentica nem cria esse aceite e não reproduz seu valor no relatório.

## 10. Compatibilidade de update

A S3 recusa update automático quando candidate e LKG divergem em:

- tipo de artefato;
- `schema_version`;
- versão do contrato;
- metadados estruturais relevantes do App V10.

Não existe migração automática de versão na S3.

## 11. Staging e rollback dry-run

O staging ocorre somente em diretório temporário local.

### Release inicial

- copia candidato;
- revalida candidato staged;
- remove stage;
- comprova retorno ao estado sem artefato.

### Update/rollback

- copia candidato;
- revalida candidato staged;
- substitui stage pelo LKG;
- revalida LKG;
- compara fingerprint restaurado com o LKG.

O diretório temporário é destruído ao final.

## 12. Recibo fail-closed

Recibo existe somente depois de staging e rollback dry-run completos.

Campos técnicos incluem:

- versão/engine;
- modo;
- resultado;
- `source_commit`;
- tipo/fingerprint;
- `staging_verified`;
- `rollback_dry_run_verified`;
- LKG técnico quando aplicável;
- `network_access = false`;
- `remote_mutation_performed = false`;
- `publication_performed = false`.

Não há timestamp, caminho local, `authorization_ref`, `identity_ref`, `acceptance_ref` ou segredo no recibo.

Falha intermediária retorna `LOCAL_OPERATION_FAILED` sem `receipt`.

## 13. Fronteira de rede e Databricks

O núcleo S3 não importa:

- `requests`;
- `socket`;
- `urllib`;
- `httpx`;
- cliente `databricks`.

Ele não lê `DATABRICKS_TOKEN` e não chama deploy/import/publish.

`subprocess` é usado somente para os dois comandos Git read-only descritos acima; `shutil` é usado somente para staging local temporário.

O workflow mantém:

- `permissions: contents: read`;
- checkout com `persist-credentials: false`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

## 14. Suíte permanente S3

`tools/tests/test_temas_v13_s3.py` contém **21 testes**.

A cobertura inclui:

- release com árvore limpa;
- árvore suja;
- bundle adulterado;
- `source_commit` stale;
- S2 `BLOCKED` preservado;
- binding S2 para o mesmo artefato;
- update sem LKG;
- update com versão incompatível;
- update compatível;
- rollback dry-run restaurando LKG;
- falha no meio da operação sem recibo;
- LKG divergente dos bytes;
- `acceptance_ref` não ecoada;
- determinismo;
- reprodutibilidade do fingerprint V10;
- release inicial sem LKG;
- registro estável de códigos;
- ausência de rede/cliente Databricks;
- Git subprocess read-only;
- workflow S1/S2/S3 somente leitura;
- cobertura documental dos cinco entregáveis do Plano Mestre.

## 15. First head e failures intermediários preservados

Primeiro HEAD S3:

`290729f6ba33ab6f0beb8e7148777fbec47cf4c7`.

Workflows:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35042751435` | `success` |
| Contrato de temas V01 | `35042751473` | `success` |
| Núcleo de temas V02 | `35042751488` | `success` |
| CI local reproduzível | `35042751508` | `failure` |
| Contrato operacional V13 | `35042751510` | `failure` |

No V13:

- S1: **20/20 PASS**;
- validador S1: **PASS**;
- S2: **27/27 PASS**;
- S3: **20/21 PASS**;
- a única falha S3 foi editorial: o teste exigia a formulação explícita `não autoriza`, enquanto o runbook dizia `não concede autorização`;
- regressões/V00/validador/fronteiras posteriores ficaram `skipped` e não são reclassificados como PASS.

No CI geral:

- a etapa `temas` falhou pela mesma única asserção editorial S3;
- o validador mediu **1439 arquivos / 1914 links**;
- o README raiz ainda declarava 1436/1912;
- validação registrou exatamente **2 falhas / 0 avisos**, ambas de métricas do README;
- biblioteca, ferramentas, transição, READMEs e Concierge permaneceram verdes.

Nenhuma dessas falhas foi apagada do histórico.

## 16. Correção aditiva do first head

Commit:

`135b875bedb826fae62f9400d54650f2d7a8015e`.

Alterações exclusivas:

- `S3_RELEASE_OPERACIONAL.md`: explicita que o recibo S3 **não autoriza** aplicação remota;
- `README.md`: atualiza o estado vivo para S2 integrada/S3 candidata e reconcilia somente os valores medidos **1439/1914**.

Nenhum gate foi relaxado. Nenhuma suíte foi reduzida. Nenhuma autorização foi ampliada.

## 17. Certificação do segundo head

O SHA `135b875bedb826fae62f9400d54650f2d7a8015e` acionou 8 workflows reais de PR, todos concluídos com `success`:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35043073353` | `success` |
| Contrato de temas V01 | `35043073288` | `success` |
| Núcleo de temas V02 | `35043073351` | `success` |
| CI local reproduzível | `35043073289` | `success` |
| Databricks App de gestão visual V10 | `35043073279` | `success` |
| Temas nativos AI/BI V11 | `35043073281` | `success` |
| Homologação de jornadas V12 | `35043073319` | `success` |
| Contrato operacional V13 | `35043073328` | `success` |

No V13, no mesmo SHA:

- S1: **20/20 PASS**;
- validador S1: **PASS**;
- S2: **27/27 PASS**;
- S3: **21/21 PASS**;
- regressões V01–V13: **PASS**;
- compatibilidade V00: **PASS**;
- validador estrutural/documental: **PASS**;
- fronteira S1: **PASS**;
- fronteira S2: **PASS**;
- fronteira S3: **PASS**.

O validador permanece reconciliado em **1439 arquivos / 1914 links**, sem arquivos locais extras.

## 18. Preservação V12 no segundo head

O workflow V12 `35043073319` concluiu `success` no mesmo SHA.

Passaram:

- protocolo/mutantes V12;
- evidência real V12;
- regressões transversais;
- V00;
- validação estrutural/documental;
- aplicabilidade do escopo estrito.

`Escopo V12 e higiene` ficou **skipped**, não PASS, porque a branch S3 não é escopo V12. A allowlist V12 não foi ampliada.

## 19. Estados herdados preservados

A S3 mantém separadamente:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` de ambiente;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no alcance V12 já evidenciado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Não existe PASS agregado que esconda FAIL ou bloqueios.

## 20. Ausência de mutação Databricks

A S3 não executou:

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

## 21. Efeito deste checkpoint na árvore

Este arquivo é um novo caminho versionado. Portanto, as métricas 1439/1914 pertencem ao HEAD anterior `135b875b...` e **não são presumidas para o HEAD que contém este checkpoint**.

O próximo gate é:

1. observar todos os workflows do novo SHA;
2. registrar a medição real do validador;
3. corrigir o README raiz somente se a saída real divergir;
4. recertificar o SHA resultante;
5. reconfirmar `main`, merge-base, ahead/behind, diff e mergeabilidade;
6. parar para aceite explícito.

## 22. Ponto de parada

S4 permanece não iniciada.

A S3 só poderá ser integrada depois de:

- certificação do HEAD final exato;
- preservação dos failures intermediários;
- `main` sem divergência não tratada;
- PR mergeável;
- issue #57 preservada;
- aceite explícito do mantenedor.

**Não iniciar S4 por esta PR.**
