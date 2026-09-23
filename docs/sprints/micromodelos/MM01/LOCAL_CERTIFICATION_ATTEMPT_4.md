# MM01 — Local Certification v1 — tentativa 4

Data da execução: 2026-09-22

Status: **FAIL no gate transversal CI_LOCAL**

## Identidade certificada

- repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`;
- branch: `micromodelos/mm01-contrato-canonico`;
- HEAD: `4cc537f0dd243773a4b250f5912fb7b4027bc6cc`;
- tree: `c1bf7d1fc3ab4ab34531c4ec1477a09a2d690c05`;
- `origin/main`: `17640a6a31f562e9979d235ede27cf44cef9ebbf`;
- merge-base: `17640a6a31f562e9979d235ede27cf44cef9ebbf`;
- `ahead_by=168`;
- `behind_by=0`;
- checkout não shallow;
- worktree limpa;
- merge-ref PR #51: `5dfe155e59abcf96d5553fe35f526ac907700544`;
- tree do merge-ref: `c1bf7d1fc3ab4ab34531c4ec1477a09a2d690c05`;
- diff material HEAD × merge-ref: vazio.

## Resultado mecânico

O manifest registrou:

- `status=FAIL`;
- `preflight_ok=true`;
- `postflight_ok=false`;
- `failure=StepFailed: CI_LOCAL failed with exit code 1`;
- exit code global 1;
- nenhum retry.

SHA-256 do ZIP original:

`2a66d6c5135f3816f25b4b7fd907d3930028428becbbe8e1e0e0c1c761e447a0`

O hash produzido pelo certifier e o hash recalculado independentemente coincidiram. Os 16 entries de `SHA256SUMS.txt` foram validados e o ZIP continha 17 entries coerentes com o bundle em disco.

## Gates que passaram antes do bloqueio

- `BOOTSTRAP_PYTHON=PASS`;
- `BOOTSTRAP_IPYWIDGETS=PASS`;
- `BOOTSTRAP_APP=PASS`;
- `BOOTSTRAP_PNPM=PASS`;
- `BOOTSTRAP_VISUAL=PASS`;
- `CERT_SELFTEST=PASS` com 15 testes;
- `MM01_CANONICAL=PASS` com 47 testes;
- `MM01_R02=PASS` com 3 testes;
- `MM01_R03=PASS` com 1 teste;
- `MM01_VALIDATE_ASSISTANT=PASS`, 0 falhas / 0 avisos.

Todos os nove workflows-fonte apresentaram `blob_matches=true` e `missing_snippets=[]`.

A portabilidade Windows foi exercitada: npm e pnpm foram resolvidos como shims `.CMD` via `cmd.exe /d /c call`. O streaming incremental também funcionou durante bootstraps e testes.

## Finding material R4

`CI_LOCAL` falhou depois de aproximadamente 213 segundos.

Os subgates `temas`, `biblioteca`, `ferramentas`, `transicao`, `readmes` e todos os gates Concierge passaram.

Somente `validacao` e `sef` reprovaram, e ambos apontaram a mesma causa:

```text
README.md snapshot:
colado = repo (identidade) : 1638
real   = repo (identidade) : 1669
```

No subgate SEF, as 18 etapas anteriores ao `readme_snapshot` passaram; o failure ocorreu exclusivamente no snapshot do README.

Consequentemente, V00/V01/V02/V10/V11/V12/V13 não foram executados pela política fail-closed.

## Classificação do finding

O finding é um drift documental derivado do inventário versionado, não uma regressão funcional da MM01 ou do SEF.

A correção autorizada é atualizar a saída colada do README para a árvore final real, preservando o validador. Não é permitido relaxar `validate_assistant.py`, `ci_local.py` ou o gate SE08 para aceitar snapshot stale.

## Anomalia secundária

O `CERT_SELFTEST` passou, mas emitiu `ResourceWarning` no teste de streaming porque o pipe `proc.stdout` não era fechado explicitamente depois do tee.

A correção deve ser estritamente operacional: fechar o pipe em bloco `finally`/context manager e proteger a ausência de `ResourceWarning` por regressão. Isso não altera comando, output esperado, exit code ou critério de PASS.

## Estado após a R4

Depois da R4, a PSEF00 foi integrada em `main` pela PR #98:

`main=11851e137dd7793b351ac08fc211c0be90005dee`

O delta PSEF00 contém somente sete documentos `.md` em `docs/sprints/hub_prompts_sef/`, sem alterar workflows, certifier MM01, policy ou superfícies produtivas.

A branch MM01 foi reconciliada com essa `main` por merge real da PR operacional #100:

`1dd69d21d1d28231b92ed34ee654bcab7cee10e2`

A tentativa R4 permanece historicamente FAIL; a reconciliação posterior não a reclassifica.

## Próximo passo

Após:

1. corrigir o fechamento do pipe do streaming;
2. atualizar o snapshot do README para a árvore final resultante;
3. confirmar novamente `main`, merge-base, `behind_by=0`, workflow pins e merge-ref;

deverá ser executada uma nova certificação integral em diretório probatório novo.

MM01 continua não aceita e não integrada. MM02 permanece bloqueada.
