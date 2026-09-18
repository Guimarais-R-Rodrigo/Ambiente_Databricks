# SE05 — runbook Databricks Free

## Objetivo

Homologar o nível L4 da skill piloto no Databricks Free pessoal usando somente dados sintéticos. O gate precisa demonstrar que a conclusão homologada depende de Postflight `PASS`.

Nenhuma etapa deste runbook autoriza publicação no workspace corporativo.

## Pré-condição

Só publicar a candidata depois de observar no mesmo HEAD:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE05_LOCAL
DERIVED_STALE       = false
failures            = 0
```

A worktree deve estar limpa.

## 1. Autenticação

No PowerShell:

```powershell
$DBX_PROFILE = "FREE"
$DBX_HOST = "https://dbc-72c8503a-bc27.cloud.databricks.com"

databricks --profile $DBX_PROFILE auth describe -o json
databricks --profile $DBX_PROFILE current-user me -o json
```

Não use `$HOST`, pois colide case-insensitively com `$Host` no PowerShell.

## 2. Dry-run, publicação e verify

```powershell
python tools/publicar_free.py --profile $DBX_PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --execute --profile $DBX_PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --verify --rapido --profile $DBX_PROFILE --expected-host $DBX_HOST
python tools/publicar_free.py --verify --profile $DBX_PROFILE --expected-host $DBX_HOST
```

Preservar verify por conteúdo:

```powershell
$EVID = Join-Path $HOME ".ambiente_databricks\sef_certifications"
New-Item -ItemType Directory -Force -Path $EVID | Out-Null
$HEAD12 = (git rev-parse HEAD).Substring(0,12)

python tools/publicar_free.py --verify --conteudo `
  --profile $DBX_PROFILE `
  --expected-host $DBX_HOST `
  --relatorio (Join-Path $EVID "se05_free_verify_$HEAD12.json")
```

Ausentes/obsoletos do pacote controlado reprovam. Arquivos gerenciados pela plataforma permanecem classificados separadamente.

## 3. Importar o probe

```powershell
$ME = databricks --profile $DBX_PROFILE current-user me -o json | ConvertFrom-Json
$DBX_HOME = "/Users/$($ME.userName)"
$TEST_DIR = "$DBX_HOME/sef-tests"
$PROBE_PATH = "$TEST_DIR/SE05_Free_Probe"
$LOCAL_PROBE = Join-Path (Get-Location) "tools\skill_enforcement\se05_free_probe.py"

$TMP_ROOT = Join-Path $env:TEMP "se05_probe_import"
$TMP_FILE = Join-Path $TMP_ROOT "SE05_Free_Probe.py"
$TMP_EXPORT = Join-Path $env:TEMP "SE05_Free_Probe_export.py"

databricks --profile $DBX_PROFILE workspace mkdirs $TEST_DIR
```

Tentar o import individual até três vezes:

```powershell
$IMPORTED = $false
for ($i = 1; $i -le 3; $i++) {
    databricks --profile $DBX_PROFILE workspace import $PROBE_PATH `
      --file $LOCAL_PROBE `
      --format SOURCE `
      --language PYTHON `
      --overwrite

    if ($LASTEXITCODE -eq 0) {
        $IMPORTED = $true
        break
    }

    if ($i -lt 3) {
        Start-Sleep -Seconds (3 * $i)
    }
}
```

O endpoint `workspace/import` já apresentou `PROTOCOL_ERROR` neste workspace. Isso é falha de transporte, não falha funcional do probe.

Fallback documentado:

```powershell
if (-not $IMPORTED) {
    if (Test-Path $TMP_ROOT) {
        Remove-Item -Recurse -Force $TMP_ROOT
    }
    New-Item -ItemType Directory -Force -Path $TMP_ROOT | Out-Null
    Copy-Item $LOCAL_PROBE $TMP_FILE -Force

    databricks --profile $DBX_PROFILE workspace import-dir `
      $TMP_ROOT `
      $TEST_DIR `
      --overwrite

    if ($LASTEXITCODE -ne 0) {
        throw "Import do probe SE05 falhou também via import-dir."
    }
}
```

## 4. Confirmar e comparar conteúdo remoto

```powershell
databricks --profile $DBX_PROFILE workspace get-status $PROBE_PATH -o json
if ($LASTEXITCODE -ne 0) {
    throw "SE05_Free_Probe ausente."
}

if (Test-Path $TMP_EXPORT) {
    Remove-Item -Force $TMP_EXPORT
}

databricks --profile $DBX_PROFILE workspace export $PROBE_PATH `
  --format SOURCE `
  --file $TMP_EXPORT

if ($LASTEXITCODE -ne 0) {
    throw "Falha ao exportar probe SE05."
}

$LOCAL_TEXT = [System.IO.File]::ReadAllText($LOCAL_PROBE).Replace("`r`n", "`n").TrimEnd("`r", "`n")
$REMOTE_TEXT = [System.IO.File]::ReadAllText($TMP_EXPORT).Replace("`r`n", "`n").TrimEnd("`r", "`n")

if ($LOCAL_TEXT -ne $REMOTE_TEXT) {
    throw "Probe SE05 remoto diverge do arquivo local."
}
```

Depois remover os arquivos temporários locais.

## 5. Executar

Abrir:

```text
/Users/<usuario>/sef-tests/SE05_Free_Probe
```

Executar `Run all` e preservar o JSON final integral.

Global esperado:

```text
marker = SE05_FREE_PROBE_V1
status = PASS
published_package_mutated = false
persistent_writes_performed = false
```

Casos esperados:

### P01_l4_happy_path

```text
enforcement_status                = PASS
receipt_present                   = true
postflight_status                 = PASS
completion_authorized             = true
completion_status                 = COMPLETED
verification_status               = VALID
verification_valid                = true
verification_completion_authorized= true
completion_claim_consistent       = true
```

### P02_core_l3_cannot_finalize_l4

Core L3 pode possuir Receipt, mas completion deve continuar negada porque não há evidência da rota L4.

### P03_missing_required_input_fails_closed

Sem `pk_columns`, `data_quality_check` não recebe evidência de call/completion. Esperado:

```text
enforcement_status    = INCOMPLETE
postflight_status     = FAIL
completion_authorized = false
```

### P04_incomplete_handoff_not_completed

Handoff faltando campo obrigatório resulta em `REVIEW` e completion negada.

### P05_completion_claim_tamper_detected

Adulteração do claim de completion deve resultar em verifier `INVALID` e `completion_claim_consistent=false`.

## 6. Classificação

Só registrar:

```text
DATABRICKS_FREE = PASS
```

quando publicação/verify por conteúdo e `SE05_FREE_PROBE_V1` tiverem sido realmente executados com evidência preservada.

Preparar/importar o probe não equivale a PASS.

## 7. Limpeza

O probe cria somente uma view temporária sintética e a remove ao final.

Esperado:

```text
persistent_writes_performed = false
published_package_mutated   = false
```

Não criar tabelas persistentes, volumes, jobs, apps ou objetos corporativos para este gate.
