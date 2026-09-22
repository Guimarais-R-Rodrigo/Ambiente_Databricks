# SE04 — runbook Databricks Free

## Objetivo

Homologar no Databricks Free pessoal a emissão e a verificação do `ExecutionReceiptV1` usando apenas dados sintéticos. Nenhuma etapa deste runbook autoriza publicação no workspace corporativo.

## Pré-condição

Só publicar a candidata depois de observar no mesmo HEAD:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE04_LOCAL
DERIVED_STALE       = false
failures            = 0
```

## 1. Autenticação

No PowerShell:

```powershell
$PROFILE = "FREE"
$DBX_HOST = "https://dbc-72c8503a-bc27.cloud.databricks.com"

databricks --profile $PROFILE auth describe -o json
databricks --profile $PROFILE current-user me -o json
```

Não use `$HOST`, pois ele colide case-insensitively com `$Host` no PowerShell.

## 2. Dry-run, publicação e verify

```powershell
python tools/publicar_free.py --profile $PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --execute --profile $PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --verify --rapido --profile $PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --verify --profile $PROFILE --expected-host $DBX_HOST
```

Depois preserve um verify por conteúdo:

```powershell
$EVID = Join-Path $HOME ".ambiente_databricks\sef_certifications"
New-Item -ItemType Directory -Force -Path $EVID | Out-Null
$HEAD12 = (git rev-parse HEAD).Substring(0,12)

python tools/publicar_free.py --verify --conteudo `
  --profile $PROFILE `
  --expected-host $DBX_HOST `
  --relatorio (Join-Path $EVID "se04_free_verify_$HEAD12.json")
```

Ausentes ou obsoletos do pacote controlado reprovam a publicação. Arquivos gerenciados pela plataforma devem permanecer classificados separadamente.

## 3. Importar o probe

```powershell
$ME = databricks --profile $PROFILE current-user me -o json | ConvertFrom-Json
$DBX_HOME = "/Users/$($ME.userName)"
$TEST_DIR = "$DBX_HOME/sef-tests"
$PROBE_PATH = "$TEST_DIR/SE04_Free_Probe"
$LOCAL_PROBE = Join-Path (Get-Location) "tools\skill_enforcement\se04_free_probe.py"

$TMP_EXPORT = Join-Path $env:TEMP "SE04_Free_Probe_export.py"

databricks --profile $PROFILE workspace mkdirs $TEST_DIR

databricks --profile $PROFILE workspace import $PROBE_PATH `
  --file $LOCAL_PROBE `
  --format SOURCE `
  --language PYTHON `
  --overwrite
```

Se o import individual sofrer erro de transporte, pode-se usar o fallback `workspace import-dir` já documentado na SE03. Falha de transporte não deve ser reclassificada como falha funcional do probe.

## 4. Verificar conteúdo do probe remoto

```powershell
if (Test-Path $TMP_EXPORT) { Remove-Item -Force $TMP_EXPORT }

databricks --profile $PROFILE workspace export $PROBE_PATH `
  --format SOURCE `
  --file $TMP_EXPORT

if ($LASTEXITCODE -ne 0) { throw "Falha ao exportar probe SE04." }

$LOCAL_TEXT = [System.IO.File]::ReadAllText($LOCAL_PROBE).Replace("`r`n", "`n").TrimEnd("`r", "`n")
$REMOTE_TEXT = [System.IO.File]::ReadAllText($TMP_EXPORT).Replace("`r`n", "`n").TrimEnd("`r", "`n")

if ($LOCAL_TEXT -ne $REMOTE_TEXT) { throw "Probe SE04 remoto diverge do arquivo local." }
```

## 5. Executar

Abra:

```text
/Users/<usuario>/sef-tests/SE04_Free_Probe
```

Execute `Run all` e preserve integralmente o JSON final.

Saída global esperada:

```text
marker = SE04_FREE_PROBE_V1
status = PASS
published_package_mutated = false
persistent_writes_performed = false
```

Casos esperados:

- `R01_valid_receipt`: verifier `VALID`;
- `R05_tampered_receipt`: `INVALID`;
- `R06_tampered_output`: `INCOMPATIBLE`;
- `R07_stale_receipt`: `STALE_REPLAYED`;
- `R02_R04_manual_without_receipt`: `ABSENT`;
- `R03_direct_primitive_without_receipt`: `ABSENT`;
- `R11_release_integrity_broken`: `BLOCKED`, sem Receipt, somente em fixture temporária;
- `R10_provenance_conflict`: `BLOCKED`, sem Receipt;
- `R12_primitive_failure_no_fallback`: `FAIL`, sem Receipt e sem fallback.

## 6. Classificação

Só registrar:

```text
DATABRICKS_FREE = PASS
```

quando publicação/verify e o probe acima tiverem sido realmente executados com evidência preservada. Preparar o probe não equivale a PASS.

Testes de Genie Code, se repetidos, continuam classificados separadamente e não substituem o gate determinístico do Receipt.
