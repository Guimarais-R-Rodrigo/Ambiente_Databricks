# SER01 A4-FREE — publicação e probe do verifier no Databricks Free

## Objetivo

Executar no workspace pessoal Free uma prova ambiental proporcional da superfície `object_validation`, sem fingir que a primitive repo-side viaja no produto. O canal Free prova publicação/conteúdo e portabilidade do verifier; **não** prova execução do produtor `tools/skill_enforcement/ser01_object_validation.py`.

Base local já certificada antes desta etapa:

```text
A3_R3_SHA = fcec3e34898006081b3e9063c627b5783108687f
SER-CERT-1 = PASS
verify_certification = VALID
CURRENT_LEVEL = L2
```

A4 adiciona somente este probe e documentação fora de `ambiente_fonte/`; antes da publicação confirme que o pacote `.assistant` continua byte-idêntico ao protegido na A3.

## 1. Precondições

Use somente o workspace pessoal/Free já autorizado. Não use workspace corporativo.

```powershell
$DBX_PROFILE = "FREE"
$DBX_HOST = "<host HTTPS exato já configurado no profile>"

databricks --profile $DBX_PROFILE auth describe -o json
databricks --profile $DBX_PROFILE current-user me -o json
```

Registre os outputs sanitizados. Se host/profile divergir, pare.

Confirme no Git local:

```powershell
git status --short
git rev-parse HEAD
git diff --name-only fcec3e34898006081b3e9063c627b5783108687f..HEAD -- ambiente_fonte Novo_Ambiente_Simulado
```

O último comando deve ficar vazio. Caso contrário, A4 alterou o produto e precisa voltar ao ChatGPT.

## 2. Publicação e verificação

Execute uma vez cada etapa, preservando stdout/stderr/exit code:

```powershell
python tools/publicar_free.py --profile $DBX_PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --execute --profile $DBX_PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --verify --rapido --profile $DBX_PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --verify --profile $DBX_PROFILE --expected-host $DBX_HOST
```

Depois preserve verify por conteúdo:

```powershell
$EVID = Join-Path $HOME ".ambiente_databricks\ser01_a4_free"
New-Item -ItemType Directory -Force -Path $EVID | Out-Null
$REPORT = Join-Path $EVID "publish_verify_content.json"

python tools/publicar_free.py --verify --conteudo `
  --profile $DBX_PROFILE `
  --expected-host $DBX_HOST `
  --relatorio $REPORT
```

Exigir zero ausentes/obsoletos do pacote controlado, skills 14/14 e conteúdo comparado sem divergência. Arquivos gerenciados pela plataforma ficam separados.

## 3. Importar o probe

O probe não faz parte de `.assistant`; é instrumento externo:

```text
tools/skill_enforcement/ser01_free_probe.py
```

Resolva o usuário atual e importe uma única vez:

```powershell
$ME = databricks --profile $DBX_PROFILE current-user me -o json | ConvertFrom-Json
$DBX_HOME = "/Users/$($ME.userName)"
$TEST_DIR = "$DBX_HOME/ser01-tests"
$PROBE_PATH = "$TEST_DIR/SER01_A4_Free_Probe"
$LOCAL_PROBE = Join-Path (Get-Location) "tools\skill_enforcement\ser01_free_probe.py"
$TMP_EXPORT = Join-Path $env:TEMP "SER01_A4_Free_Probe_export.py"

databricks --profile $DBX_PROFILE workspace mkdirs $TEST_DIR
databricks --profile $DBX_PROFILE workspace import $PROBE_PATH `
  --file $LOCAL_PROBE `
  --format SOURCE `
  --language PYTHON `
  --overwrite
```

Falha de transporte é `BLOCKED_INFRA`, não motivo para retry-until-green nem para editar o probe.

## 4. Conferir bytes do probe remoto

```powershell
if (Test-Path $TMP_EXPORT) { Remove-Item -Force $TMP_EXPORT }

databricks --profile $DBX_PROFILE workspace export $PROBE_PATH `
  --format SOURCE `
  --file $TMP_EXPORT

$LOCAL_TEXT = [System.IO.File]::ReadAllText($LOCAL_PROBE).Replace("`r`n", "`n").TrimEnd("`r", "`n")
$REMOTE_TEXT = [System.IO.File]::ReadAllText($TMP_EXPORT).Replace("`r`n", "`n").TrimEnd("`r", "`n")

if ($LOCAL_TEXT -ne $REMOTE_TEXT) { throw "Probe remoto diverge do arquivo local." }
```

## 5. Executar no Free

Abra `/Users/<usuario>/ser01-tests/SER01_A4_Free_Probe`, execute **Run all uma vez** e preserve o JSON final integral.

Saída global esperada:

```text
marker = SER01_A4_FREE_PROBE_V1
status = PASS
fixture_scope = INTEGRITY_ONLY_NOT_EXECUTION_PROOF
persistent_writes_performed = false
published_package_mutated = false
```

Casos mínimos:

- `F01_release_and_route_contract`: release/contrato íntegros; produtor repo-side declarado e não publicado; `workspace_without_repo_checkout=NOT_AVAILABLE`;
- `F02_fixture_receipt_with_record`: fixture **sintética** de integridade valida Receipt+record e mantém todos os claims fracos; não é prova de execução;
- `F03_receipt_without_record`: inválido com `LOCAL_RECORD_REQUIRED`;
- `F04_missing_receipt`: inválido;
- `F05_tamper_and_replay`: adulteração/replay inválidos;
- `F06_policy_remains_pre_promotion`: L2→L3 em `audit`, sem promoção;
- `F07_published_package_unchanged`: hashes protegidos iguais antes/depois.

## 6. Verificação pós-probe

Execute novamente somente o verify por conteúdo, sem republicar:

```powershell
python tools/publicar_free.py --verify --conteudo `
  --profile $DBX_PROFILE `
  --expected-host $DBX_HOST `
  --relatorio (Join-Path $EVID "post_probe_verify_content.json")
```

## 7. Classificação

Somente com publicação/verify e probe reais:

```text
A4_FREE = PASS
```

`A4_FREE=PASS` não significa `object_validation` executada no Free. A primitive é deliberadamente repo-side; no workspace a rota operacional permanece `NOT_AVAILABLE` e o comportamento correspondente é testado separadamente no A4-GENIE.

Não alterar policy, não promover L3 e não usar este gate para autorizar apply.
