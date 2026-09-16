# V13 — consolidação operacional do Sistema de Temas

## Estado vigente

A S0 foi **aceita e integrada** pela PR #59 no merge
`1d46c9625fb5bfd6d1b666ddff055507238788bf`.

A S1 foi **aceita e integrada** pela PR #60 no merge
`70f6a43748b9636f2bf8fe56aa07e9fb90a0d285`. Os 15/15 workflows de `push`
disparados por esse merge concluíram com `success`.

A S2 foi **aceita e integrada** pela PR #61 no merge
`76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`. A S3 só foi aberta depois de os
15/15 workflows de `push` desse merge concluírem com `success`.

A etapa vigente é **S3 — release, instalação, atualização e rollback**, em branch
candidata separada.

Para quem nunca entrou no Hub: a S3 pega um artefato que já passou pelo preflight
S2 e prova, localmente, que ele pode ser staged, verificado e revertido. Ela não
faz deploy no Databricks e não publica tema.

A leitura operacional começa em
[S3 — release, instalação, atualização e rollback](S3_RELEASE_OPERACIONAL.md).

**S4 não foi iniciada.**

## Baseline certificado da S3

A branch S3 nasce diretamente de:

`76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`

Esse SHA é o merge da S2 na `main`.

Antes da abertura da S3 foram confirmados:

- `main` no merge S2;
- árvore integrada idêntica à árvore candidata S2;
- PR #61 efetivamente `merged=true`;
- 15 workflows de `push`;
- 15 `success`;
- 0 failures;
- nenhuma mutação Databricks executada pela S2.

A S3 não reaproveita a branch S2 como base paralela.

## Plano canônico

O [Plano Mestre V13](PLANO_MESTRE.md), aceito pela PR #58, continua sendo o
contrato de escopo.

A ordem permanece:

`S0 → S1 → S2 → S3 → S4 → S5 → S6 → S7 → aceite → merge → auditoria pós-merge → V14`

A S3 implementa exclusivamente:

- runbook de release;
- runbook de instalação/atualização;
- runbook de rollback;
- checklist de staging;
- estratégia de last-known-good;
- testes de árvore limpa, integridade, compatibilidade, staging, rollback e falso
  recibo.

A S4 permanece responsável por observabilidade e diagnóstico.

## Artefatos históricos preservados

- [checkpoint S0](CHECKPOINT_S0.md);
- [inventário operacional S1](S1_INVENTARIO_OPERACIONAL.md);
- [checkpoint S1](CHECKPOINT_S1.md);
- [matriz operacional S1](MATRIZ_OPERACIONAL.json);
- [S2 — preflight operacional](S2_PREFLIGHT_OPERACIONAL.md);
- [checkpoint S2](CHECKPOINT_S2.md).

A S3 consome esses artefatos. Ela não reescreve a matriz S1 para remover
`S2_NOT_IMPLEMENTED`, porque essa frase continua sendo uma afirmação histórica
sobre o que a própria S1 implementava.

## S3 — artefatos próprios

A candidata S3 adiciona:

- `tools/temas_v13_release.py`;
- `tools/tests/test_temas_v13_s3.py`;
- [S3 — release, instalação, atualização e rollback](S3_RELEASE_OPERACIONAL.md);
- evolução do workflow V13 para S1 + S2 + S3.

A candidata não adiciona cliente Databricks, token, rede, deploy remoto ou
publicação.

## Ciclo operacional

A S3 trabalha sobre o ciclo do Plano Mestre:

1. `PREPARE`;
2. `PREFLIGHT`;
3. `PACKAGE`;
4. `STAGE`;
5. `VERIFY`;
6. `ROLLBACK` dry-run.

`APPLY` remoto e `ACCEPT` de ambiente não são simulados.

Um resultado `READY_FOR_AUTHORIZED_APPLY` significa somente que o ciclo local
terminou sem falha e que o rollback local foi demonstrado.

## Composição com owners existentes

| Necessidade | Owner |
|---|---|
| readiness | S2 |
| bundle geral / `theme_contract` | V09 |
| bundle do App | V10 |
| deploy/rollback do App | contrato V10 |
| tema/schema/hash | V02 |
| AI/BI | V11 |
| evidência | V12 |
| autorização/rollback por superfície | matriz S1 |

Não existe segundo manifesto, segundo schema, segunda política de papéis ou
segunda matriz de bindings.

## Artefatos executáveis localmente

A S3 automatiza dry-run somente para os dois tipos de artefato que já possuem
owner e verificador local claros:

### `transition_bundle`

Owner: V09.

- precisa estar sob `.artifacts/`;
- precisa passar `validate_theme_zip`;
- `worktree_dirty` deve ser `false`;
- `source_commit` deve ser o checkout atual;
- conteúdo é identificado por fingerprint ordenado de path/hash/bytes;
- transporte continua sem ativação/publicação.

### `app_bundle`

Owner: V10.

- precisa estar sob `.artifacts/`;
- precisa passar `tools.temas_v10_app.verify`;
- `source_commit` deve ser o checkout atual;
- duas gerações no mesmo commit devem ter o mesmo fingerprint de conteúdo;
- deploy continua fora da ferramenta S3.

## Last known good

Update e rollback exigem LKG.

A referência S3 contém identidade técnica do artefato anterior e uma
`acceptance_ref` sanitizada. A ferramenta confirma que commit e fingerprint
correspondem aos bytes reais.

A `acceptance_ref` não é autorização criada pela S3.

## Compatibilidade de update

A S3 falha fechado quando candidate e LKG divergem em:

- tipo de artefato;
- `schema_version`;
- versão do contrato;
- metadados estruturais V10 relevantes.

Não existe migração automática de versão nesta sprint.

## Staging e rollback

O staging ocorre em diretório temporário local.

Release inicial:

- copia e revalida candidato;
- remove o stage;
- comprova retorno ao estado sem artefato.

Update/rollback:

- copia e revalida candidato;
- substitui o stage pelo LKG;
- revalida LKG;
- exige fingerprint restaurado idêntico.

O diretório temporário é destruído ao final.

## Recibo

Recibo existe somente em PASS.

Ele registra de forma sanitizada:

- engine/versão;
- modo;
- commit;
- tipo/fingerprint;
- staging verificado;
- rollback dry-run verificado;
- LKG técnico quando aplicável;
- rede = 0;
- mutação remota = 0;
- publicação = 0.

Falha em qualquer etapa termina sem recibo de sucesso.

## Superfícies remotas continuam separadas

### Visual Lab

`V12-LAB-01` continua `BLOQUEADO_AUTORIZACAO`. Persistência real não é executada
pela S3.

### Databricks App

`V12-APP-01` continua `BLOQUEADO_AUTORIZACAO`. A S3 prepara o bundle e o dry-run;
deploy real continua no runbook V10 e exige autorização própria.

### AI/BI

`V12-AIBI-01` continua PASS somente no escopo limitado já evidenciado.
`publish_dashboard` continua não autorizado. A S3 não executa `Import theme` nem
`Publish`.

### Workspace theme

`V12-AIBI-02` continua `BLOQUEADO_AUTORIZACAO`. Nenhuma mutação administrativa é
executada.

### Acessibilidade

`A11-01` continua **FAIL**, issue #57. A S3 não fecha essa dívida; o tratamento
operacional específico permanece previsto para S5.

## CI e fronteiras

O workflow V13 deve permanecer:

- `permissions: contents: read`;
- checkout com `persist-credentials: false`;
- sem `DATABRICKS_HOST`;
- sem `DATABRICKS_TOKEN`;
- sem `secrets.*`.

Fronteiras esperadas:

- `V13_S1_REMOTE_MUTATION=0`;
- `V13_S2_NETWORK=0`;
- `V13_S2_REMOTE_MUTATION=0`;
- `V13_S3_NETWORK=0`;
- `V13_S3_REMOTE_MUTATION=0`;
- `V13_S3_LOCAL_DRY_RUN_ONLY=1`;
- `V13_S4_NOT_STARTED=1`.

## Métricas do README raiz

A S3 segue o mesmo protocolo da S2:

1. primeiro head funcional;
2. runner mede identidade e links;
3. qualquer failure de métrica é preservado;
4. `README.md` raiz só é corrigido com números observados;
5. checkpoint S3 é adicionado depois;
6. a árvore com checkpoint é medida novamente.

Nenhuma contagem será estimada.

## Próxima ação

A candidata S3 deve:

1. executar os testes S3;
2. repetir S1/S2 e regressões V01–V13;
3. validar documentação/README;
4. preservar failures intermediários;
5. reconciliar métricas somente pelo runner;
6. adicionar checkpoint S3;
7. recertificar o SHA exato;
8. reconfirmar `main`, merge-base, ahead/behind, diff e mergeabilidade;
9. parar para aceite.

**Não iniciar S4.**
