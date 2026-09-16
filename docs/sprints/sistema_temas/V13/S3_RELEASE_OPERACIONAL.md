# V13 — S3: release, instalação, atualização e rollback

Status: **candidata S3**.

Baseline de abertura: merge certificado da S2 na `main`,
`76f8a2dcc6d5dd69bd6c1af726fb40e2eced8af8`.

Este documento é o runbook operacional da S3. Ele não concede autorização de
Databricks, não executa deploy remoto, não publica tema e não inicia a S4.

## Para quem é

Use este runbook se você precisa preparar um release do Sistema de Temas,
verificar um artefato candidato, planejar uma instalação/atualização ou provar
que existe um caminho de rollback antes de uma ação autorizada.

Para quem nunca operou o Hub, a regra prática é:

1. primeiro prove que o checkout e o artefato estão íntegros;
2. depois execute o preflight S2;
3. faça staging e rollback **local**;
4. só depois trate uma eventual aplicação remota, se existir autorização própria.

`READY_FOR_AUTHORIZED_APPLY` significa “o dry-run local terminou bem”. Não
significa “aplicado”, “publicado”, “homologado no ambiente” nem “autorizado”.

## Escopo canônico

A S3 implementa o trecho do Plano Mestre:

`PREPARE → PREFLIGHT → PACKAGE → STAGE → VERIFY → ROLLBACK dry-run`

Ações `APPLY` remotas continuam fora do executor local S3. Quando uma superfície
depender de Databricks real, identidade, permissão ou autorização, o operador
deve parar no gate correspondente.

Entregáveis deste documento:

- Runbook de release;
- Runbook de instalação e atualização;
- Runbook de rollback;
- Checklist de staging;
- estratégia de Last known good.

A ferramenta associada é `tools/temas_v13_release.py`. A suíte permanente é
`tools/tests/test_temas_v13_s3.py`.

## O que a S3 reutiliza

A S3 não cria um segundo sistema de empacotamento ou publicação.

| Necessidade | Owner canônico |
|---|---|
| tema/schema/hash/contexto | V02 |
| bundle geral e `theme_contract` | V09 |
| bundle do Databricks App | V10 |
| App deploy/rollback | `databricks_app/DEPLOY_ROLLBACK.md` |
| AI/BI e bindings diretos | V11 |
| evidência/homologação | V12 |
| superfície/ação/autorização/rollback | matriz S1 |
| readiness | preflight S2 |

A S3 usa os validadores existentes por composição. Ela não copia tokens, papéis,
bindings, schema, `theme_contract`, política V01 nem regras de Publish.

## Fronteira de segurança

A ferramenta S3:

- não importa cliente Databricks;
- não usa HTTP;
- não lê `DATABRICKS_TOKEN`;
- não faz `git push`, `git reset`, `git checkout`, `git clean`, `git add` ou
  `git commit`;
- usa Git somente para `rev-parse HEAD` e `status --porcelain`;
- exige worktree limpo;
- aceita artefatos somente sob `.artifacts/`, diretório ignorado pelo Git;
- faz staging em diretório temporário local;
- apaga o staging ao terminar;
- nunca executa `deploy_app`, `Import theme`, workspace theme ou `Publish`;
- nunca produz recibo de sucesso depois de falha parcial.

O workflow GitHub continua `contents: read` e sem credenciais Databricks.

## Identidade de release

A identidade técnica mínima de um artefato é:

- tipo (`transition_bundle` ou `app_bundle`);
- `source_commit`;
- versão do manifesto/contrato;
- fingerprint de conteúdo calculado sobre `path + sha256 + bytes` ordenados;
- hash do container quando aplicável.

### V09: ZIP de transição

O contrato V09 exige presença e SHA-256 dos arquivos transportados. O ZIP atual
também contém `generated_at_utc` e metadados do container; por isso a S3 **não**
inventa uma promessa de byte-identidade do ZIP inteiro entre duas gerações.

A reprodutibilidade que a S3 pode provar para V09 é a do conteúdo contratado:
mesmo inventário e mesmos hashes produzem o mesmo `content_fingerprint`. Cada ZIP
real continua podendo ter seu próprio `container_sha256`.

### V10: bundle de App

O bundle V10 é um diretório derivado do produto canônico. Duas gerações no mesmo
commit devem produzir o mesmo `content_fingerprint`. A suíte S3 executa esse
mutante positivo.

## Last known good

**Last known good (LKG)** é o último artefato cujo uso foi aceito em um processo
anterior. A S3 não concede esse aceite.

A referência técnica S3 contém:

- `kind`;
- caminho local sob `.artifacts/`;
- `source_commit`;
- `artifact_fingerprint`;
- `acceptance_ref`.

`acceptance_ref` é apenas uma referência sanitizada para o aceite anterior. A
ferramenta não autentica nem substitui a decisão humana/governança V01.

Ao receber um LKG, a S3 abre novamente o artefato, roda o validador canônico e
confere commit + fingerprint. Uma string dizendo “LKG” não basta.

Para App V10, a estratégia continua a do owner V10: identificar o commit anterior
ainda aprovado, regenerar/verificar seu bundle e manter o mesmo Volume. A S3 não
apaga sessões nem transforma rollback de código em rollback de tema publicado.

## Runbook de release

### Objetivo

Preparar um artefato local verificável a partir de checkout limpo e provar que ele
pode ser staged e removido/restaurado sem tocar em Databricks.

### Pré-requisitos

- checkout no commit que se pretende liberar;
- `git status` limpo;
- CI aplicável verde;
- dependências locais instaladas;
- artefato gerado sob `.artifacts/`;
- request S2 fixado ao **mesmo** artefato;
- autorização local explícita quando o owner exige geração de artefato;
- rollback declarado no preflight.

### Release V09

Gere o pacote pelo owner existente:

```powershell
python -B tools/bundle_implantacao.py --output .artifacts/ambiente-databricks-candidato.zip
```

Não use `--allow-dirty` para release. Essa flag continua destinada apenas a
revisão.

Valide o ZIP pelo contrato V09 e depois use o preflight S2/S3. A S3 recusa:

- hash divergente;
- arquivo obrigatório ausente;
- `worktree_dirty=true`;
- `source_commit` diferente do checkout;
- preflight S2 que não esteja apontando para o mesmo ZIP.

### Release V10

Gere e verifique:

```powershell
python -B tools/temas_v10_app.py --output .artifacts/v10-app
python -B tools/temas_v10_app.py --verify .artifacts/v10-app
```

Isso continua sendo apenas fonte implantável local. Nenhuma dessas linhas cria ou
atualiza Databricks App.

### Executar S3

Prepare um JSON de request. Exemplo conceitual para V09:

```json
{
  "request_version": 1,
  "mode": "release",
  "preflight": {
    "request_version": 1,
    "mode": "surface",
    "operations": [
      {
        "surface_id": "transition_bundle",
        "action_id": "build_transition_bundle",
        "inputs": {
          "bundle_path": ".artifacts/ambiente-databricks-candidato.zip",
          "authorization_ref": "referencia-sanitizada",
          "rollback": {
            "prepared": true,
            "state_ref": "discard-new-bundle"
          }
        }
      }
    ]
  },
  "artifact": {
    "kind": "transition_bundle",
    "path": ".artifacts/ambiente-databricks-candidato.zip"
  },
  "last_known_good": null
}
```

Execute:

```powershell
python -B tools/temas_v13_release.py --request .artifacts/request-s3.json
```

Só um `overall_status = PASS` pode emitir `receipt`.

No release inicial, o rollback dry-run esperado é descartar o staging local e
confirmar que nenhum artefato staged permaneceu.

## Checklist de staging

Antes de qualquer aplicação autorizada, confirme:

- [ ] checkout limpo;
- [ ] commit correto;
- [ ] artefato sob `.artifacts/`;
- [ ] artefato validado pelo owner V09 ou V10;
- [ ] `source_commit` igual ao checkout;
- [ ] preflight S2 apontando para o mesmo artefato;
- [ ] preflight S2 em `PASS`;
- [ ] staging temporário revalidado;
- [ ] rollback dry-run em `PASS`;
- [ ] LKG identificado para update;
- [ ] versão/contrato compatível para update;
- [ ] autorização remota separada, quando aplicável;
- [ ] identidade/permissão reais verificadas fora da CI, quando aplicável;
- [ ] smoke pós-ação definido antes de aplicar;
- [ ] evidência a registrar será sanitizada;
- [ ] `Publish` continua decisão separada.

Se qualquer item obrigatório falhar, pare.

## Runbook de instalação e atualização

### Instalação

A S3 divide instalação em duas partes.

**Parte A — preparação local coberta pela ferramenta S3**

1. validar checkout;
2. validar artefato;
3. executar S2;
4. stage local;
5. revalidar o stage;
6. provar rollback local;
7. emitir `READY_FOR_AUTHORIZED_APPLY`.

**Parte B — aplicação em ambiente**

Só existe quando a superfície possui autorização própria. A S3 desta candidata
não executa a Parte B.

Para V10, siga o owner
`ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md`
depois da autorização. O recibo S3 não substitui:

- identidade real;
- permissão no App;
- recurso `theme_storage`;
- smoke no browser;
- isolamento entre usuários;
- evidência de ambiente.

Para AI/BI, workspace theme e outras mutações remotas, S2 continua fail-closed. A
S3 não converte `BLOCKED` em PASS.

### Atualização

Update exige `last_known_good`.

A S3 valida o LKG e recusa atualização automática quando:

- tipo do artefato mudou;
- `schema_version` mudou;
- versão do contrato mudou;
- no V10, superfície/modo/persistência/resource key/publication divergiram.

Compatibilidade técnica não significa autorização de ambiente.

Antes de aplicar update remoto:

1. guarde a identidade técnica do LKG;
2. execute S3 em `mode = update`;
3. exija `UPDATE_COMPATIBLE`;
4. exija `STAGING_VERIFIED`;
5. exija `ROLLBACK_RESTORE_VERIFIED`;
6. só então passe ao procedimento autorizado do owner da superfície.

## Smoke pós-ação

A S3 não executa ambiente remoto, mas o operador precisa definir o smoke antes da
ação.

### V09

Smoke de transporte:

- ZIP abre;
- manifesto presente;
- `theme_contract` válido;
- hashes conferem;
- transporte não foi confundido com ativação.

### V10

Use o smoke do `DEPLOY_ROLLBACK.md`: abertura do App, preset, alteração, comparação,
save/reopen, histórico, isolamento com segunda identidade e ausência de
aprovar/publicar/promover.

### AI/BI

Preserve V11/V12:

- export/binding fixados;
- import somente em draft quando autorizado;
- semântica preservada;
- Light/Dark verificados quando aplicável;
- rollback comprovado;
- `Publish` separado.

`A11-01` continua **FAIL** na issue #57. S3 não fecha a dívida de contraste.

## Runbook de rollback

### Regra geral

Rollback deve ser planejado **antes** de uma mutação.

Não use force-push, exclusão recursiva, limpeza de Volume ou edição de hash para
“fazer passar”.

### Rollback dry-run S3

`mode = rollback_dry_run` exige LKG.

A ferramenta:

1. valida candidato;
2. valida LKG;
3. confirma compatibilidade de contrato;
4. copia o candidato para staging temporário;
5. revalida o candidato staged;
6. remove apenas o stage temporário;
7. copia o LKG para o mesmo stage;
8. revalida o conteúdo;
9. compara o fingerprint restaurado com o LKG;
10. emite recibo somente se a restauração for exata.

O staging temporário é destruído ao final.

### Rollback real V10

O owner V10 continua soberano:

1. identifique o commit anterior ainda aprovado;
2. regenere/verifique o bundle desse commit;
3. mantenha o mesmo Volume;
4. implante pelo mesmo canal autorizado;
5. repita o smoke mínimo;
6. registre motivo e resultado.

A S3 não executa essas etapas remotas.

### Rollback parcial ou falho

Se rollback local ou remoto não puder ser comprovado:

- classifique a operação como falha;
- não emita recibo de sucesso;
- preserve o estado e evidência disponíveis;
- não tente “consertar” manifesto/hash manualmente;
- pare e escale para o owner da superfície.

A taxonomia formal de diagnóstico pertence à S4; ela não é antecipada aqui.

## Recibo S3

O recibo de sucesso é técnico e sanitizado. Ele contém:

- versão;
- engine `V13-S3`;
- modo;
- resultado;
- `source_commit`;
- tipo;
- `artifact_fingerprint`;
- staging verificado;
- rollback dry-run verificado;
- LKG técnico, quando aplicável;
- `network_access = false`;
- `remote_mutation_performed = false`;
- `publication_performed = false`.

O recibo não contém caminho local, `authorization_ref`, `identity_ref`,
`acceptance_ref`, segredo ou timestamp.

`READY_FOR_AUTHORIZED_APPLY` não prova aplicação remota.

## Falhas que devem fechar o ciclo sem recibo

- worktree sujo;
- Git indisponível;
- preflight S2 `FAIL`;
- preflight S2 `BLOCKED`;
- preflight apontando para outro artefato;
- bundle adulterado;
- `source_commit` stale;
- LKG ausente ou divergente;
- update incompatível;
- erro de cópia;
- falha na revalidação de staging;
- falha na restauração.

## Superfícies e limite da S3

| Superfície | S3 local | Mutação remota |
|---|---|---|
| notebook/Plotly/HTML | runbook + S2 | não aplicável |
| Visual Lab | runbook; persistência continua bloqueada | não executada |
| bundle V09 | valida/stage/rollback local | transporte não é ativação |
| App V10 | valida bundle/stage/rollback local | deploy continua autorizado separadamente |
| AI/BI dashboard | runbook; S2 preservado | import/publicação não executados |
| workspace theme | runbook; S2 preservado | bloqueado sem autorização admin |

Estados herdados continuam separados:

- `V12-AIBI-01 = PASS` somente no escopo V12;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

## Evidência e CI

A suíte S3 deve provar, no mínimo:

- árvore limpa;
- bundle válido;
- bundle adulterado recusado;
- artefato stale recusado;
- update incompatível recusado;
- V10 reproduzível por fingerprint de conteúdo;
- staging verificado;
- rollback por descarte em release inicial;
- rollback para LKG em update;
- falha intermediária sem recibo;
- determinismo do relatório;
- ausência de rede e cliente Databricks;
- workflow read-only.

Git/CI continuam evidência técnica. Não são prova de deploy, identidade, permissão,
browser, acessibilidade ou publicação no Databricks.

## Ponto de parada

A S3 termina quando a candidata estiver documentada, testada e certificada no SHA
exato, com failures intermediários preservados e checkpoint próprio.

**Não iniciar S4 sem aceite explícito e certificação pós-merge da S3.**
