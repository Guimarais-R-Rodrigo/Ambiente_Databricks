# Checkpoint V13 — S2: preflight operacional unificado

Data: 15/09/2026.

Branch: `codex/temas-v13-s2-preflight-operacional-20260915`.

Estado deste documento: **candidata S2 em certificação final**. O HEAD imediatamente anterior à criação deste checkpoint, `5467ea634fd6e51c8992aa4fd48ab25859aab16a`, concluiu 8/8 workflows de PR com `success`. Como este checkpoint adiciona um arquivo à árvore, o novo HEAD precisa ser medido e certificado novamente antes de qualquer aceite.

## 1. Baseline de abertura

- S1 aceita e integrada pela PR #60;
- merge S1 na `main`: `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`;
- pós-merge S1: 15/15 workflows de `push` com `success`, 0 failures;
- branch S2 criada diretamente desse merge certificado;
- issue aberta herdada do Sistema de Temas: #57, `A11-01 = FAIL`;
- nenhuma mutação Databricks foi autorizada ou executada pela S2;
- S3 não foi iniciada.

A S2 não reutilizou a branch S1 como base paralela: nasceu da `main` já integrada e certificada.

## 2. Escopo implementado

A S2 implementa somente o preflight operacional unificado previsto no Plano Mestre V13.

Artefatos próprios da candidata:

- `tools/temas_v13_preflight.py`;
- `tools/tests/test_temas_v13_s2.py`;
- `docs/sprints/sistema_temas/V13/S2_PREFLIGHT_OPERACIONAL.md`;
- evolução de `.github/workflows/temas-v13-ci.yml` para executar S1 e S2;
- atualização de `docs/sprints/sistema_temas/V13/README.md`;
- atualização do estado vivo e das métricas realmente medidas em `README.md`.

Este checkpoint é um novo caminho documental e, por isso, exige uma nova medição de identidade antes do HEAD final.

Não houve alteração em `ambiente_fonte/`, `Novo_Ambiente_Simulado/`, contratos funcionais V01–V12, `MATRIZ_OPERACIONAL.json`, `tools/temas_v13_operacional.py`, `CHANGELOG.md`, App, binder AI/BI, schema ou tokens.

## 3. Decisão arquitetural

A S2 é uma camada de composição, não uma nova fonte de verdade.

Ela reutiliza:

- V02: `load_theme()` para schema, SHA-256, contexto e integridade;
- V09: `validate_theme_zip()` para o bundle de transição e `theme_contract`;
- V10: `verify()` para o bundle candidato do Databricks App;
- V11: `project_theme()`, `bind_native_template()` e a política local de workspace theme;
- S1: matriz operacional para superfícies, ações, owners, autorização e rollback.

A S2 não copia:

- tokens de tema;
- política de papéis/transições V01;
- schema/parsing/validação V02;
- lista de nove caminhos protegidos V09;
- três bindings diretos V11;
- matriz V11 48 = 3/23/22;
- schema nativo AI/BI;
- contexto `aibi`;
- manifesto de implantação.

A matriz S1 e o validador S1 não foram reescritos para remover a frase histórica `S2_NOT_IMPLEMENTED`. Essa frase continua correta sobre a S1: a S1 não implementou o preflight. A implementação S2 vive em artefato próprio.

## 4. Contrato do preflight

A entrada usa `request_version = 1` e possui dois modos:

- `surface`: exatamente uma operação;
- `aggregate`: uma ou mais operações, ordenadas deterministicamente por `surface_id` e `action_id`.

Cada operação informa:

- `surface_id`;
- `action_id`;
- `inputs`.

Pares repetidos `surface_id + action_id` são recusados.

A saída usa:

- `report_version = 1`;
- `engine = V13-S2`;
- `overall_status`;
- checks de request;
- operações e checks por operação;
- `network_access = false`;
- `remote_mutation_performed = false`.

Não há timestamp, UUID ou consulta remota, para que a mesma entrada sobre os mesmos bytes gere a mesma saída.

## 5. Estados do preflight

A S2 usa quatro estados distintos:

| Estado | Semântica |
|---|---|
| `PASS` | checks aplicáveis e demonstráveis localmente foram satisfeitos |
| `BLOCKED` | condição necessária não pode ser fabricada pela S2, como autorização, identidade efetiva ou rollback ainda bloqueado pelo owner |
| `FAIL` | contrato ou pré-requisito verificável localmente falhou |
| `NOT_APPLICABLE` | check não pertence à ação |

Precedência agregada:

`FAIL > BLOCKED > PASS > NOT_APPLICABLE`.

Um `BLOCKED` nunca é promovido a `PASS`.

## 6. Fail-closed de tema, bundle e AI/BI

A ferramenta possui códigos estáveis para falhas, incluindo:

- `THEME_INVALID`;
- `THEME_HASH_STALE`;
- `CONTEXT_INCOMPATIBLE`;
- `BUNDLE_INCOMPLETE`;
- `APP_BUNDLE_INVALID`;
- `APP_STORAGE_PRECONDITION`;
- `NATIVE_TEMPLATE_HASH_STALE`;
- `JSON_POINTER_MISSING`;
- `AIBI_CAPABILITY_FORBIDDEN`;
- `NATIVE_TEMPLATE_SYNTHETIC`.

O fixture `hub_v11_synthetic_dashboard_draft` continua proibido como export nativo.

O binder V11 continua sendo a autoridade para os campos diretos existentes; a S2 não automatiza capacidades `approximated` ou `unsupported`.

## 7. Fail-closed de autorização

Para ações mutáveis que não estão canonicamente bloqueadas, a S2 exige `authorization_ref` explícita.

A presença dessa referência não significa que a S2 concedeu ou autenticou autorização.

Se a matriz S1 mantém a ação como:

- `BLOQUEADO_AUTORIZACAO`; ou
- `NOT_AUTHORIZED`;

a S2 retorna `AUTHORIZATION_CANONICALLY_BLOCKED` e o request não consegue substituir esse estado.

## 8. Identidade não é autoafirmada como prova

Para `persistent_mutation` e `remote_mutation`:

- sem referência: `IDENTITY_REQUIRED`;
- com referência local: `IDENTITY_LIVE_UNVERIFIED`.

Mesmo uma `identity_ref` presente continua `BLOCKED`, porque o núcleo S2 é offline e não autentica identidade efetiva no Databricks.

Essa escolha impede false reassurance e false approval.

## 9. Rollback

Quando a matriz exige rollback, o request precisa declarar:

- `prepared = true`;
- `state_ref` não vazio.

Ausência ou shape incompleto retorna `ROLLBACK_NOT_PREPARED`.

Quando a estratégia da própria matriz ainda é `blocked_until_*`, a S2 retorna `ROLLBACK_CANONICALLY_BLOCKED`; um campo fornecido pelo chamador não elimina essa dívida canônica.

A S2 não executa rollback. O ciclo operacional de release/install/update/rollback pertence à S3.

## 10. Proteção de referências

Os valores arbitrários recebidos em:

- `authorization_ref`;
- `identity_ref`;
- `rollback.state_ref`;

não são reproduzidos na saída.

A suíte injeta uma string com formato sensível e verifica que ela não aparece no relatório.

## 11. Ausência de rede e mutação

O núcleo S2 não importa:

- `requests`;
- `socket`;
- `urllib`;
- `httpx`;
- cliente `databricks`;
- `subprocess`;
- `shutil`.

A S2 usa apenas rotas de verificação existentes. Ela não chama builders, deploy, import remoto, publish ou qualquer mutação Databricks.

O workflow mantém:

- `permissions: contents: read`;
- checkout com `persist-credentials: false`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

## 12. Suíte permanente S2

`tools/tests/test_temas_v13_s2.py` contém 27 testes.

A cobertura inclui:

- tema válido;
- determinismo;
- modo agregado;
- request malformado;
- operação duplicada;
- superfície desconhecida;
- ação desconhecida;
- tema inválido;
- hash de tema stale;
- contexto incompatível;
- bundle V09 incompleto;
- autorização ausente;
- rollback ausente;
- bundle V09 válido;
- bundle V10 inválido;
- storage V10 incompatível;
- JSON Pointer inexistente;
- SHA stale do template nativo;
- fixture sintético proibido;
- binding local válido com identidade remota ainda bloqueada;
- referência de identidade sem promoção a prova viva;
- `Publish` canonicamente bloqueado;
- workspace theme canonicamente bloqueado;
- ausência de eco de referências sensíveis;
- códigos emitidos pertencentes ao registro estável;
- ausência de imports de rede/Databricks/mutação;
- workflow read-only executando S1 e S2.

## 13. First head e failure intermediário preservado

Primeiro HEAD S2:

`1c68c587ea0a0ad2fe2acbf967b288ecfbfdcc62`.

Workflows de PR desse SHA:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35040053887` | `success` |
| Contrato de temas V01 | `35040053940` | `success` |
| Núcleo de temas V02 | `35040053903` | `success` |
| CI local reproduzível | `35040053914` | `failure` |
| Contrato operacional V13 | `35040053952` | `failure` |

As duas falhas foram exclusivamente documentais e ocorreram depois dos testes funcionais.

No workflow V13, antes do failure:

- S1: **20/20 PASS**;
- validador S1: **PASS**;
- S2: **27/27 PASS**;
- regressões `test_temas*.py`: **562/562 PASS**;
- V00: **12/12 PASS**.

O validador mediu:

- `repo (identidade) = 1435`;
- `repo (links) = 1912`;
- 0 arquivos locais extras.

O README raiz ainda declarava 1432/1922.

A redução de 10 links resultou da reescrita mais enxuta do README V13. Nenhum link artificial foi adicionado para tentar preservar a contagem anterior.

No first head, os steps `Fronteira S1 preservada` e `Fronteira S2` ficaram `skipped` por causa do failure anterior. Eles não são reclassificados como PASS.

## 14. Correção aditiva do first head

Commit:

`5467ea634fd6e51c8992aa4fd48ab25859aab16a`.

A correção alterou somente `README.md`:

- atualizou o estado vivo para S1 integrada e S2 candidata;
- registrou `repo (identidade) = 1435`;
- registrou `repo (links) = 1912`.

Os links de navegação existentes foram mantidos sem adicionar uma nova rota apenas para influenciar a métrica.

Nenhum gate foi relaxado. Nenhuma allowlist V12 foi ampliada. Nenhuma falha histórica foi apagada.

## 15. Certificação do segundo head

O SHA `5467ea634fd6e51c8992aa4fd48ab25859aab16a` acionou 8 workflows reais de PR e todos concluíram com `success`:

| Workflow | Run | Resultado |
|---|---:|---|
| Regressões da instrumentação V00 | `35040399512` | `success` |
| Contrato de temas V01 | `35040399470` | `success` |
| Núcleo de temas V02 | `35040399494` | `success` |
| CI local reproduzível | `35040399493` | `success` |
| Databricks App de gestão visual V10 | `35040399462` | `success` |
| Temas nativos AI/BI V11 | `35040399471` | `success` |
| Homologação de jornadas V12 | `35040399458` | `success` |
| Contrato operacional V13 | `35040399454` | `success` |

No workflow V13 `35040399454`, no mesmo SHA:

- S1: **20/20 PASS**;
- validador S1: **PASS**;
- S2: **27/27 PASS**;
- regressões V01–V13: **562/562 PASS**;
- compatibilidade V00: **12/12 PASS**;
- validador estrutural/documental: **APROVADO — 0 falhas / 0 avisos**;
- `repo (identidade) = 1435`;
- `repo (links) = 1912`;
- `V13_S1_REMOTE_MUTATION=0`;
- `V13_S2_NETWORK=0`;
- `V13_S2_REMOTE_MUTATION=0`;
- `V13_S3_NOT_STARTED=1`.

Os dois steps de fronteira concluíram com `success` nesse SHA.

## 16. Preservação V12 no segundo head

No workflow V12 `35040399458`, no mesmo SHA:

- protocolo/mutantes V12: **47/47 PASS**;
- evidência real V12: **11/11 PASS**;
- regressões transversais incluindo S1/S2: **562/562 PASS**;
- V00: **12/12 PASS**;
- validador: **0 falhas / 0 avisos**, 1435/1912;
- `V12_SCOPE=NOT_APPLICABLE`;
- `Escopo V12 e higiene`: **skipped**, não PASS.

A manutenção integrada pela PR #58 permanece preservada e a allowlist V12 não foi ampliada.

## 17. Estados herdados preservados

A S2 mantém separadamente:

- `DOC-02 = PASS`;
- `DOC-03 = PASS`;
- `SEC-01 = PASS` de ambiente;
- `UAT-01 = PASS` somente textual;
- `V12-AIBI-01 = PASS` somente no escopo real já evidenciado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

Não existe `PASS` agregado que esconda o FAIL ou os bloqueios.

## 18. Ausência de mutação Databricks

A S2 não executou:

- deploy de App;
- criação/alteração de ACL ou grupos;
- workspace theme;
- `Import theme` remoto adicional;
- `Publish`;
- edição de dashboard;
- persistência no workspace;
- criação/alteração de UC Volume;
- qualquer outra mutação Databricks.

Git/CI permanecem evidência técnica, não homologação de ambiente.

## 19. Métricas verificáveis antes deste checkpoint

No SHA `5467ea634fd6e51c8992aa4fd48ab25859aab16a`, antes da criação deste arquivo, o validador mediu:

- `repo (identidade) = 1435` arquivos;
- `repo (links) = 1912` links fora da raiz analisada;
- 0 arquivos locais extras;
- 0 falhas e 0 avisos.

A criação deste checkpoint altera a árvore e exige nova medição. Nenhum número posterior é estimado neste documento.

## 20. Estado Git/PR antes do checkpoint final

Antes da criação deste arquivo:

- base da PR #61: `main` no merge S1 `70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`;
- HEAD: `5467ea634fd6e51c8992aa4fd48ab25859aab16a`;
- PR #61: aberta e draft;
- S3 não iniciada.

A reconciliação final de `main`, merge-base, `ahead_by`/`behind_by`, mergeabilidade, diff, PRs paralelas, issue #57 e workflows será preenchida na descrição da PR após a certificação do HEAD que contém este checkpoint.

## 21. O que fica para S3

Somente após aceite explícito da S2:

- runbook consolidado de release/install/update/rollback;
- staging ou execução operacional autorizada quando aplicável;
- definição de last known good;
- smoke pós-ação;
- recibo de release;
- dry-run/ensaio de rollback dentro do contrato S3;
- demais entregas definidas pelo Plano Mestre para S3.

A S2 **não** antecipa esses itens.

## 22. Ponto de parada

Após medir a árvore com este checkpoint, reconciliar o README apenas com números observados, certificar o SHA final e reconfirmar a `main`, a PR #61 deve permanecer sem merge até aceite explícito do mantenedor.

**Parar antes da S3.**
