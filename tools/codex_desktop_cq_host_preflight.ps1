param(
    [string]$OutputRoot = "$HOME\codex-scratch\Ambiente_Databricks"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "ser/B1-ser03-ser05-authoring"
$ExpectedRepoFragment = "Guimarais-R-Rodrigo/Ambiente_Databricks"

function Write-Utf8NoBom([string]$Path, [string]$Text) {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $encoding)
}

function Add-PythonCandidate([System.Collections.Generic.List[string]]$List, [string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return }
    try {
        $full = [System.IO.Path]::GetFullPath($Value.Trim())
    }
    catch { return }
    if ((Test-Path -LiteralPath $full) -and -not $List.Contains($full)) {
        $List.Add($full)
    }
}

$rootText = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $rootText) {
    throw "CQ_HOST_PREFLIGHT_NOT_GIT_REPOSITORY"
}
$root = [System.IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
Set-Location $root

$initialStatus = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $initialStatus.Count -ne 0) {
    throw "CQ_HOST_PREFLIGHT_WORKTREE_DIRTY"
}

$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) {
    throw "CQ_HOST_PREFLIGHT_BRANCH_MISMATCH:$branch"
}

$origin = (& git remote get-url origin).Trim()
if ($LASTEXITCODE -ne 0 -or $origin -notmatch [regex]::Escape($ExpectedRepoFragment)) {
    throw "CQ_HOST_PREFLIGHT_REMOTE_MISMATCH"
}

& git fetch origin $ExpectedBranch
if ($LASTEXITCODE -ne 0) {
    throw "CQ_HOST_PREFLIGHT_FETCH_FAILED"
}

$head = (& git rev-parse HEAD).Trim()
$originHead = (& git rev-parse "origin/$ExpectedBranch").Trim()
$tree = (& git rev-parse 'HEAD^{tree}').Trim()
if ($head -ne $originHead) {
    throw "CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:$head:$originHead"
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$outputRootFull = [System.IO.Path]::GetFullPath($OutputRoot)

$projectConfig = Join-Path $root ".codex\config.toml"
if (-not (Test-Path -LiteralPath $projectConfig)) {
    throw "CQ_HOST_PREFLIGHT_PROJECT_CONFIG_MISSING"
}
$projectConfigSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $projectConfig).Hash

$userConfig = Join-Path $HOME ".codex\config.toml"
$userConfigExists = Test-Path -LiteralPath $userConfig
$userConfigSha256 = $null
if ($userConfigExists) {
    $userConfigSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $userConfig).Hash
}

$candidates = New-Object 'System.Collections.Generic.List[string]'
if ($env:CODEX_CQ_PYTHON) {
    Add-PythonCandidate $candidates $env:CODEX_CQ_PYTHON
}

foreach ($name in @("python.exe", "python3.exe")) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) {
        Add-PythonCandidate $candidates $cmd.Source
    }
}

$py = Get-Command "py.exe" -ErrorAction SilentlyContinue
if ($py) {
    foreach ($selector in @("-3.12", "-3.13", "-3.11", "")) {
        try {
            if ($selector) {
                $resolved = (& $py.Source $selector -c "import sys; print(sys.executable)" 2>$null)
            }
            else {
                $resolved = (& $py.Source -c "import sys; print(sys.executable)" 2>$null)
            }
            if ($LASTEXITCODE -eq 0 -and $resolved) {
                Add-PythonCandidate $candidates ($resolved | Select-Object -First 1)
            }
        }
        catch {}
    }
}

$python = $null
foreach ($candidate in $candidates) {
    try {
        $probe = (& $candidate -c "import json,sys,importlib.metadata as m; print(json.dumps({'executable':sys.executable,'python_version':sys.version.split()[0],'implementation':sys.implementation.name,'jsonschema_version':m.version('jsonschema')}))" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $probe) {
            $python = ($probe | Select-Object -First 1) | ConvertFrom-Json
            $python.executable = [System.IO.Path]::GetFullPath($python.executable)
            break
        }
    }
    catch {}
}
if (-not $python) {
    throw "CQ_HOST_PREFLIGHT_NO_PYTHON_WITH_JSONSCHEMA"
}

$prEvidence = [ordered]@{
    state = "DEFERRED_TO_EXTERNAL_ADJUDICATION"
    source = "NONE"
}
$gh = Get-Command "gh.exe" -ErrorAction SilentlyContinue
if ($gh) {
    try {
        $ghRaw = (& $gh.Source pr view 115 --repo Guimarais-R-Rodrigo/Ambiente_Databricks --json state,isDraft,mergedAt,headRefName,headRefOid 2>$null)
        if ($LASTEXITCODE -eq 0 -and $ghRaw) {
            $parsed = $ghRaw | ConvertFrom-Json
            $prEvidence = [ordered]@{
                state = "OBSERVED_HOST_GH"
                source = "gh"
                pr_state = $parsed.state
                draft = $parsed.isDraft
                merged_at = $parsed.mergedAt
                head_ref = $parsed.headRefName
                head_sha = $parsed.headRefOid
            }
        }
    }
    catch {}
}

$finalStatus = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $finalStatus.Count -ne 0) {
    throw "CQ_HOST_PREFLIGHT_FINAL_WORKTREE_DIRTY"
}

$payload = [ordered]@{
    schema_version = "AC-R2-DESKTOP-HOST-PREFLIGHT-1"
    result = "PASS"
    client_surface = "CODEX_DESKTOP_WINDOWS"
    recorded_at = (Get-Date).ToString("o")
    git = [ordered]@{
        root = $root
        branch = $branch
        head = $head
        tree = $tree
        origin_url = $origin
        origin_tracking_ref = $originHead
        fetch = "PASS"
        initial_clean = $true
        final_clean = $true
    }
    python = [ordered]@{
        executable = $python.executable
        python_version = $python.python_version
        implementation = $python.implementation
        jsonschema_version = $python.jsonschema_version
    }
    project = [ordered]@{
        config_path = $projectConfig
        config_sha256 = $projectConfigSha256
        user_config_exists = $userConfigExists
        user_config_sha256 = $userConfigSha256
    }
    pr_115 = $prEvidence
    scratch_root = $outputRootFull
}

$jsonPath = Join-Path $outputRootFull "CQ_HOST_PREFLIGHT.json"
$shaPath = Join-Path $outputRootFull "CQ_HOST_PREFLIGHT.sha256"
$json = $payload | ConvertTo-Json -Depth 8
Write-Utf8NoBom $jsonPath $json
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $jsonPath).Hash
Write-Utf8NoBom $shaPath ($sha + "  CQ_HOST_PREFLIGHT.json" + [Environment]::NewLine)

Write-Host "CQ_HOST_PREFLIGHT = PASS"
Write-Host "HEAD = $head"
Write-Host "TREE = $tree"
Write-Host "ORIGIN_HEAD = $originHead"
Write-Host "PYTHON = $($python.executable)"
Write-Host "JSONSCHEMA = $($python.jsonschema_version)"
Write-Host "EVIDENCE = $jsonPath"
Write-Host "EVIDENCE_SHA256 = $sha"
