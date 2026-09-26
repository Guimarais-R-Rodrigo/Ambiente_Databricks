# V13 — S4: observabilidade e diagnóstico

Status: **candidata S4**.

Baseline de abertura: merge S3 certificado na `main`,
`298dfb986f67cc4c560ae22b59d2fccad0716ec0`.

A S4 torna falhas e bloqueios interpretáveis sem transformar observabilidade em
um novo executor. Ela recebe somente relatórios estruturados S2/S3 e uma lista de
classes de evidência; não acessa Databricks, não autentica referências e não
altera ambiente, artefato, Git ou produto.

## Para quem é

Use este runbook quando um preflight S2 ou um ciclo local S3 terminou em
`PASS`, `BLOCKED`, `FAIL` ou `NOT_APPLICABLE` e você precisa responder, de forma
segura:

1. em que etapa a decisão foi produzida;
2. qual classe de evidência falta;
3. qual é a próxima ação segura;
4. o que **não** deve ser feito para contornar o gate.

A S4 não decide acessibilidade/compatibilidade da S5, não fecha a issue #57 e não
concede autorização.

## Escopo canônico

A S4 implementa exclusivamente o trecho do Plano Mestre “Observabilidade e
diagnóstico”:

- Taxonomia de falhas;
- Relatório sanitizado de execução;
- Runbook de diagnóstico;
- Checklist de evidência;
- Logging sem PII/segredo.

Os estados continuam exatamente os mesmos de S1/S2/S3:

- `PASS`;
- `BLOCKED`;
- `FAIL`;
- `NOT_APPLICABLE`.

A S4 não cria score, severidade, SLA/SLO, incidente, ranking nem um segundo status
agregado. Operação sustentada/incident management pertence à V14.

## Owners consumidos

A ferramenta `tools/temas_v13_diagnostico.py` aceita somente relatórios com
`engine = V13-S2` ou `engine = V13-S3`.

O conjunto de códigos aceitos é espelhado **somente para validação de entrada** e
a suíte exige igualdade exata com `STABLE_CODES` dos owners S2/S3. Se um owner
mudar o vocabulário, o teste S4 falha fechado até a taxonomia ser revisada.

A mensagem arbitrária de origem nunca é reutilizada como log ou explicação.

## Taxonomia de falhas

A classificação operacional da S4 é:

| Classe | O que significa | Evidência mínima típica | Próxima ação segura |
|---|---|---|---|
| `INPUT_CONTRACT` | request, caminho ou seleção não atendem ao contrato | `git_ci` | corrigir forma/entrada e repetir o owner |
| `CANONICAL_CONTRACT` | schema/contexto/política/binding canônico recusou | `git_ci` | voltar ao owner; não inventar campo/capacidade |
| `ARTIFACT_INTEGRITY` | hash, inventário, manifesto ou identidade de artefato não fecha | `artifact` | regenerar/revalidar; nunca editar hash manualmente |
| `GIT_STATE` | checkout/árvore não atende ao gate | `git_ci` | restaurar checkout limpo e identificável |
| `PREFLIGHT_READINESS` | S2 não liberou a operação | `git_ci` | resolver a causa S2 antes de avançar |
| `GOVERNANCE_AUTHORIZATION` | autorização exigida está ausente/bloqueada | `authorization` | obter autorização específica no fluxo existente |
| `ENVIRONMENT_IDENTITY` | identidade, permissão ou recurso real não foi comprovado | `environment_identity` | verificar no ambiente autorizado |
| `RECOVERY_ROLLBACK` | rollback requerido não está preparado/comprovado | `rollback` | preparar/provar rollback antes de mutação |
| `COMPATIBILITY_LKG` | LKG/compatibilidade de update não fecha | `artifact` + `rollback` | identificar LKG real e compatível |
| `STAGING_EXECUTION` | staging/restauração local falhou | `artifact` + `rollback` | interromper, preservar evidência e corrigir causa |
| `EVIDENCE_GAP` | classe de evidência obrigatória não foi referenciada | depende do gate | coletar evidência; ausência nunca vira PASS |

Cada classe possui fixture ou mutante permanente em
`tools/tests/test_temas_v13_s4.py`.

A taxonomia é diagnóstica, não altera os códigos dos owners e não substitui os
runbooks S2/S3.

## Relatório sanitizado de execução

A entrada S4 tem apenas:

```json
{
  "diagnostic_version": 1,
  "source_report": {},
  "evidence": [
    {"kind": "git_ci", "state": "REFERENCED"}
  ]
}
```

`source_report` deve ser um relatório S2/S3 estruturado. A lista `evidence`
aceita apenas enums sanitizados.

Tipos de evidência suportados:

- `git_ci`;
- `artifact`;
- `authorization`;
- `environment_identity`;
- `rollback`;
- `human`;
- `browser_runtime`.

Estados de evidência:

- `REFERENCED` — existe uma referência no processo externo;
- `MISSING` — não foi fornecida;
- `NOT_APPLICABLE` — declarada fora do alcance para aquela operação.

A S4 **não recebe** o valor da referência. Dessa forma, um token, caminho,
e-mail, nome de workspace ou identificador corporativo não precisa entrar no
request diagnóstico.

O relatório de saída contém:

- `source_engine` e `source_status`;
- `diagnostic_status` usando os quatro estados já existentes;
- eventos sanitizados;
- contagem por status;
- classes de evidência requeridas/ausentes;
- `references_authenticated = false`;
- próximas ações estáticas;
- `safe_log` determinístico;
- `network_access = false`;
- `remote_mutation_performed = false`.

`REFERENCED` significa somente “o operador declarou que há referência”. A S4 não
prova que a evidência é verdadeira. Gates reais de ambiente/humano continuam
separados.

### Ausência de evidência

Se o source report é `PASS`, a S4 exige ao menos `git_ci = REFERENCED` para que o
diagnóstico também possa permanecer `PASS`.

Se a evidência requerida estiver ausente, o diagnóstico vira `BLOCKED`, nunca
PASS.

Um `FAIL` de origem permanece `FAIL` mesmo quando também existem lacunas de
evidência; o gap não mascara a falha mais forte.

## Runbook de diagnóstico

### 1. Preserve o relatório original

Não edite código, hash ou manifesto para “fazer o status mudar”. O relatório S2
ou S3 é a evidência do ponto de falha.

### 2. Monte somente o checklist de classes

Não cole token, URL privada, path de Volume, username ou texto de erro bruto no
request S4. Marque somente `kind` e `state`.

### 3. Execute localmente

```powershell
python -B tools/temas_v13_diagnostico.py --request .artifacts/request-s4.json
```

A ferramenta lê o JSON local e escreve JSON no stdout. Ela não persiste arquivo,
não usa rede e não chama Databricks.

### 4. Leia primeiro `source_status`

- `FAIL`: existe falha objetiva no owner de origem;
- `BLOCKED`: a operação não pode prosseguir no estado atual;
- `PASS`: o owner terminou sem falha, mas ainda confira evidência;
- `NOT_APPLICABLE`: o passo não pertence ao alcance observado.

### 5. Leia `diagnostic_status`

O diagnóstico pode ficar mais conservador que a origem quando faltar evidência.
Exemplo: source `PASS` + `git_ci` ausente = diagnostic `BLOCKED`.

Ele nunca deve transformar `FAIL` em PASS ou `BLOCKED` em PASS por simples texto
do operador.

### 6. Use `stage` + `safe_code`

`stage` localiza a camada; `safe_code` preserva o código estável do owner. A S4
não ecoa o `message` original, `check_id`, recibo arbitrário ou referência.

### 7. Siga `next_actions`

As ações são estáticas e orientadas a parar/voltar ao owner certo. Elas não
contêm comando de bypass, autorização implícita ou mutação remota.

### 8. Reexecute somente depois da causa corrigida

Um novo diagnóstico é uma nova leitura. Não altere manualmente o relatório
anterior.

## Checklist de evidência

Antes de afirmar que uma operação está pronta/diagnosticada, confira:

- [ ] source report é S2 ou S3 reconhecido;
- [ ] `overall_status` é coerente com os checks;
- [ ] códigos pertencem ao owner atual;
- [ ] nenhuma fronteira declara rede/mutação remota/publicação;
- [ ] `git_ci` está referenciada quando exigida;
- [ ] integridade de artefato está referenciada quando aplicável;
- [ ] autorização específica está referenciada quando a causa é governança;
- [ ] identidade/permissão/recurso reais estão referenciados quando a causa é ambiente;
- [ ] rollback está referenciado quando exigido;
- [ ] evidência humana/browser não é inferida a partir de CI;
- [ ] `MISSING` não foi reclassificado como PASS;
- [ ] `NOT_APPLICABLE` não foi chamado de PASS;
- [ ] nenhuma referência sensível foi colada no request S4.

### Evidência por superfície

- notebook/Plotly/HTML local: Git/CI pode ser suficiente para contratos locais;
- Visual Lab real: browser/runtime e autorização continuam separadas;
- bundle V09: integridade/manifesto são artefato local; transporte não é ativação;
- App V10: bundle local não prova deploy, identidade, permissões ou Volume;
- AI/BI: import draft, Publish e workspace theme continuam gates distintos;
- workspace theme: identidade/admin/rollback exigem evidência específica.

## Logging sem PII/segredo

O log S4 é derivado somente de enums previamente conhecidos:

```text
001|FAIL|ARTIFACT_INTEGRITY|BUNDLE_INCOMPLETE
002|BLOCKED|EVIDENCE_GAP|EVIDENCE_MISSING|artifact
```

Regras obrigatórias:

1. não copiar `message` do source report;
2. não copiar `check_id`;
3. não copiar `receipt` arbitrário;
4. não copiar caminhos locais ou `/Volumes/...`;
5. não copiar `authorization_ref`, `identity_ref`, `state_ref` ou `acceptance_ref`;
6. não copiar token/PAT/secret;
7. não copiar e-mail, username ou nome de workspace;
8. aceitar somente código de owner registrado;
9. código desconhecido vira `SOURCE_CODE_UNREGISTERED` sem ecoar o valor recebido;
10. log tem ordem determinística e nenhuma data/timestamp gerada pela S4.

A suíte injeta deliberadamente uma string com aparência de token, e-mail e path
privado na mensagem/check id/receipt de origem e exige que nenhum trecho apareça
na saída.

## Validação de coerência

A S4 falha fechado se:

- engine não for S2/S3;
- shape do relatório não corresponder ao owner esperado;
- status do check for desconhecido;
- código não estiver no registry do owner;
- status da operação divergir de seus checks;
- `overall_status` divergir dos checks;
- S3 `PASS` estiver sem receipt;
- S3 não-PASS carregar receipt de sucesso;
- relatório declarar rede ou mutação remota;
- S3 declarar publicação;
- classe/estado de evidência for desconhecido ou duplicado.

A S4 valida coerência da evidência **referenciada**, não autenticidade da prova.

## Estados herdados que não mudam

A observabilidade não altera homologação anterior:

- `V12-AIBI-01 = PASS` somente no escopo já evidenciado;
- `A11-01 = FAIL`, issue #57;
- `V12-LAB-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-APP-01 = BLOQUEADO_AUTORIZACAO`;
- `V12-AIBI-02 = BLOQUEADO_AUTORIZACAO`.

A decisão operacional de contraste/compatibilidade de `A11-01` pertence à **S5**.
A S4 apenas mantém a falha visível; ela não amplia bindings V11 nem converte
cores explícitas em tokens do Hub.

## Fronteira operacional

A S4 não altera:

- Databricks;
- workspace;
- App;
- dashboard;
- ACL/grupos;
- Volume;
- artefatos V09/V10;
- source/derivado;
- matriz S1;
- preflight S2;
- release executor S3;
- schema/tokens/bindings.

A ferramenta usa somente `argparse`, `json`, `re`, `pathlib` e tipos Python.
Não importa `requests`, `socket`, `urllib`, `httpx`, `databricks`, `subprocess` ou
`shutil`.

## CI

O workflow V13 executa permanentemente:

1. S1;
2. S2;
3. S3;
4. S4;
5. regressões V01–V13;
6. V00;
7. validador documental;
8. fronteiras.

Fronteira S4 viva:

- `V13_S4_NETWORK=0`;
- `V13_S4_REMOTE_MUTATION=0`;
- `V13_S4_DIAGNOSIS_READ_ONLY=1`;
- `V13_S5_NOT_STARTED=1`.

A antiga asserção `V13_S4_NOT_STARTED=1` permanece no workflow apenas como
**comentário histórico da S3**, para que a regressão S3 continue comprovando o
checkpoint histórico sem representar o estado atual.

## Limitações explícitas

- S4 não consulta logs reais de Databricks;
- S4 não autentica evidência referenciada;
- S4 não substitui browser/runtime/identidade humana;
- S4 não calcula contraste nem decide compatibilidade S5;
- S4 não define severidade/incidente/SLA/SLO V14;
- S4 não fecha issue #57;
- S4 não executa correção automática.

## Ponto de parada

A S4 termina somente após first-head observado, failures preservados, checkpoint
próprio, métricas reconciliadas pelo runner e certificação exata do HEAD final.

**Não iniciar S5 sem aceite explícito e certificação pós-merge da S4.**
