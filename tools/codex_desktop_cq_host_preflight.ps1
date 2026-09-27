param(
    [string]$OutputRoot = "$HOME\codex-scratch\Ambiente_Databricks"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "ser/B1-ser03-ser05-authoring"
$ExpectedRepoFragment = "Guimarais-R-Rodrigo/Ambiente_Databricks"
$ExpectedPythonMajor = 3
$ExpectedPythonMinor = 12
$NetworkProbeHost = "github.com"
$NetworkProbePort = 443
$NetworkProbeTimeoutMs = 5000

function Write-Utf8NoBom([string]$Path, [string]$Text) {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $encoding)
}

function Add-PythonCandidate([System.Collections.Generic.List[string]]$List, [string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return }
    try { $full = [System.IO.Path]::GetFullPath($Value.Trim()) } catch { return }
    if ((Test-Path -LiteralPath $full) -and -not $List.Contains($full)) { $List.Add($full) }
}

function Invoke-CapturedProcess([string]$FilePath, [string[]]$ArgumentList, [string]$StdoutPath, [string]$StderrPath) {
    Remove-Item -LiteralPath $StdoutPath -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $StderrPath -Force -ErrorAction SilentlyContinue
    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -WorkingDirectory (Get-Location).Path -Wait -PassThru -NoNewWindow -RedirectStandardOutput $StdoutPath -RedirectStandardError $StderrPath
    return $process.ExitCode
}

function Test-TcpEndpointSingleShot([string]$Ip, [int]$Port, [int]$TimeoutMs) {
    $client = New-Object System.Net.Sockets.TcpClient -ArgumentList ([System.Net.Sockets.AddressFamily]::InterNetwork)
    $async = $null
    try {
        $async = $client.BeginConnect($Ip, $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs)) {
            return [pscustomobject]@{ connected=$false; outcome="TIMEOUT"; exception_type=$null; socket_error_code=$null; native_error_code=$null; hresult=$null; message="TCP connect timed out" }
        }
        $client.EndConnect($async)
        return [pscustomobject]@{ connected=$true; outcome="CONNECTED"; exception_type=$null; socket_error_code=$null; native_error_code=$null; hresult=$null; message=$null }
    }
    catch [System.Net.Sockets.SocketException] {
        $e = $_.Exception
        return [pscustomobject]@{ connected=$false; outcome="SOCKET_EXCEPTION"; exception_type=$e.GetType().FullName; socket_error_code=[string]$e.SocketErrorCode; native_error_code=$e.NativeErrorCode; hresult=("0x{0:X8}" -f ($e.HResult -band 0xffffffff)); message=$e.Message }
    }
    catch {
        $e = $_.Exception
        return [pscustomobject]@{ connected=$false; outcome="OTHER_EXCEPTION"; exception_type=$e.GetType().FullName; socket_error_code=$null; native_error_code=$null; hresult=("0x{0:X8}" -f ($e.HResult -band 0xffffffff)); message=$e.Message }
    }
    finally {
        if ($async -and $async.AsyncWaitHandle) { $async.AsyncWaitHandle.Close() }
        $client.Close()
    }
}

$rootText = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $rootText) { throw "CQ_HOST_PREFLIGHT_NOT_GIT_REPOSITORY" }
$root = [System.IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
Set-Location $root
$initialStatus = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $initialStatus.Count -ne 0) { throw "CQ_HOST_PREFLIGHT_WORKTREE_DIRTY" }
$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) { throw "CQ_HOST_PREFLIGHT_BRANCH_MISMATCH:$branch" }
$origin = (& git remote get-url origin).Trim()
if ($LASTEXITCODE -ne 0 -or $origin -notmatch [regex]::Escape($ExpectedRepoFragment)) { throw "CQ_HOST_PREFLIGHT_REMOTE_MISMATCH" }
& git fetch origin $ExpectedBranch
if ($LASTEXITCODE -ne 0) { throw "CQ_HOST_PREFLIGHT_FETCH_FAILED" }
$head = (& git rev-parse HEAD).Trim()
$originHead = (& git rev-parse "origin/$ExpectedBranch").Trim()
$tree = (& git rev-parse 'HEAD^{tree}').Trim()
if ($head -ne $originHead) { throw "CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:${head}:${originHead}" }

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$outputRootFull = [System.IO.Path]::GetFullPath($OutputRoot)

$sourcePaths = [ordered]@{
    config = ".codex\config.toml"
    envelope = "docs\operations\autonomy\B1_AUTONOMY_ENVELOPE.json"
    validator = "tools\validate_codex_autonomy.py"
    metatests = "tools\tests\test_codex_autonomy.py"
    delta_checker = "tools\check_codex_autonomy_delta.py"
    network_probe_script = ".codex\probes\cq3_executor_network_probe.ps1"
}
$sourceHashes = [ordered]@{}
foreach ($key in $sourcePaths.Keys) {
    $path = Join-Path $root $sourcePaths[$key]
    if (-not (Test-Path -LiteralPath $path)) { throw "CQ_HOST_PREFLIGHT_SOURCE_MISSING:$key" }
    $sourceHashes[$key] = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
}
$projectConfig = Join-Path $root ".codex\config.toml"
$userConfig = Join-Path $HOME ".codex\config.toml"
$userConfigExists = Test-Path -LiteralPath $userConfig
$userConfigSha256 = $null
if ($userConfigExists) { $userConfigSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $userConfig).Hash }

$candidates = New-Object 'System.Collections.Generic.List[string]'
if ($env:CODEX_CQ_PYTHON) { Add-PythonCandidate $candidates $env:CODEX_CQ_PYTHON }
foreach ($name in @("python.exe", "python3.exe")) { $cmd = Get-Command $name -ErrorAction SilentlyContinue; if ($cmd) { Add-PythonCandidate $candidates $cmd.Source } }
$py = Get-Command "py.exe" -ErrorAction SilentlyContinue
if ($py) {
    foreach ($selector in @("-3.12", "")) {
        try {
            if ($selector) { $resolved = (& $py.Source $selector -c "import sys; print(sys.executable)" 2>$null) } else { $resolved = (& $py.Source -c "import sys; print(sys.executable)" 2>$null) }
            if ($LASTEXITCODE -eq 0 -and $resolved) { Add-PythonCandidate $candidates ($resolved | Select-Object -First 1) }
        } catch {}
    }
}
$python = $null
foreach ($candidate in $candidates) {
    try {
        $candidateFull = [System.IO.Path]::GetFullPath($candidate)
        $probe = (& $candidateFull -c "import json,sys,importlib.metadata as m; print(json.dumps({'executable':sys.executable,'python_version':sys.version.split()[0],'major':sys.version_info.major,'minor':sys.version_info.minor,'implementation':sys.implementation.name,'jsonschema_version':m.version('jsonschema')}))" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $probe) {
            $candidateInfo = ($probe | Select-Object -First 1) | ConvertFrom-Json
            if ($candidateInfo.implementation -ne "cpython") { continue }
            if ([int]$candidateInfo.major -ne $ExpectedPythonMajor -or [int]$candidateInfo.minor -ne $ExpectedPythonMinor) { continue }
            $candidateInfo.executable = [System.IO.Path]::GetFullPath($candidateInfo.executable)
            $python = $candidateInfo
            break
        }
    } catch {}
}
if (-not $python) { throw "CQ_HOST_PREFLIGHT_NO_QUALIFIED_CPYTHON312_WITH_JSONSCHEMA" }

$validatorStdout = Join-Path $outputRootFull "CQ_HOST_VALIDATOR.stdout.txt"
$validatorStderr = Join-Path $outputRootFull "CQ_HOST_VALIDATOR.stderr.txt"
$metatestStdout = Join-Path $outputRootFull "CQ_HOST_METATESTS.stdout.txt"
$metatestStderr = Join-Path $outputRootFull "CQ_HOST_METATESTS.stderr.txt"
$validatorExit = Invoke-CapturedProcess -FilePath $python.executable -ArgumentList @("-B", "tools/validate_codex_autonomy.py", "--json") -StdoutPath $validatorStdout -StderrPath $validatorStderr
try { $validatorPayload = Get-Content -LiteralPath $validatorStdout -Raw | ConvertFrom-Json } catch { throw "CQ_HOST_PREFLIGHT_VALIDATOR_OUTPUT_NOT_JSON" }
if ($validatorExit -ne 0 -or $validatorPayload.status -ne "PASS") { throw "CQ_HOST_PREFLIGHT_VALIDATOR_FAILED:${validatorExit}:$($validatorPayload.status)" }
$metatestExit = Invoke-CapturedProcess -FilePath $python.executable -ArgumentList @("-B", "-m", "unittest", "tools.tests.test_codex_autonomy", "-v") -StdoutPath $metatestStdout -StderrPath $metatestStderr
$metatestText = ""
if (Test-Path -LiteralPath $metatestStdout) { $metatestText += Get-Content -LiteralPath $metatestStdout -Raw }
if (Test-Path -LiteralPath $metatestStderr) { $metatestText += [Environment]::NewLine + (Get-Content -LiteralPath $metatestStderr -Raw) }
if ($metatestExit -ne 0) { throw "CQ_HOST_PREFLIGHT_METATESTS_FAILED:$metatestExit" }
if ($metatestText -notmatch "Ran\s+(\d+)\s+tests?") { throw "CQ_HOST_PREFLIGHT_METATEST_COUNT_NOT_OBSERVED" }
$runtimeTestCount = [int]$Matches[1]
$testSourceText = Get-Content -LiteralPath (Join-Path $root "tools\tests\test_codex_autonomy.py") -Raw
$staticTestCount = [regex]::Matches($testSourceText, "(?m)^\s+def test_").Count
if ($runtimeTestCount -ne $staticTestCount) { throw "CQ_HOST_PREFLIGHT_METATEST_COUNT_MISMATCH:${runtimeTestCount}:${staticTestCount}" }

$networkProbeScript = Join-Path $root ".codex\probes\cq3_executor_network_probe.ps1"
$networkSelfTestStdout = Join-Path $outputRootFull "CQ_HOST_NETWORK_PROBE_SELFTEST.stdout.txt"
$networkSelfTestStderr = Join-Path $outputRootFull "CQ_HOST_NETWORK_PROBE_SELFTEST.stderr.txt"
$powershellExe = (Get-Command "powershell.exe" -ErrorAction Stop).Source
$networkSelfTestExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", $networkProbeScript, "-SelfTest") -StdoutPath $networkSelfTestStdout -StderrPath $networkSelfTestStderr
if ($networkSelfTestExit -ne 0) { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_EXIT:${networkSelfTestExit}" }
try { $networkSelfTestPayload = Get-Content -LiteralPath $networkSelfTestStdout -Raw | ConvertFrom-Json }
catch { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_INVALID_JSON" }
$networkSelfTestCases = @($networkSelfTestPayload.cases)
$networkSelfTestResults = @($networkSelfTestCases | ForEach-Object { [string]$_.result } | Sort-Object)
$networkSelfTestExpected = @("FAIL_NETWORK_BOUNDARY_OPEN", "NOT_PROVEN", "PASS_NETWORK_DENIED" | Sort-Object)
if (
    $networkSelfTestPayload.schema_version -ne "AC-R2-CQ3-NETWORK-PROBE-SELFTEST-1" -or
    $networkSelfTestPayload.result -ne "PASS" -or
    [int]$networkSelfTestPayload.network_attempt_count -ne 0 -or
    [int]$networkSelfTestPayload.case_count -ne 3 -or
    [string]::Join("|", $networkSelfTestResults) -ne [string]::Join("|", $networkSelfTestExpected)
) {
    throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_CONTRACT_FAIL"
}

$networkProbeAddresses = @(
    [System.Net.Dns]::GetHostAddresses($NetworkProbeHost) |
        Where-Object { $_.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork } |
        ForEach-Object { $_.ToString() } |
        Sort-Object -Unique
)
if ($networkProbeAddresses.Count -lt 1) { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_NO_IPV4" }
$networkProbeIp = [string]$networkProbeAddresses[0]
$networkBaseline = Test-TcpEndpointSingleShot -Ip $networkProbeIp -Port $NetworkProbePort -TimeoutMs $NetworkProbeTimeoutMs
if (-not $networkBaseline.connected) {
    throw "CQ_HOST_PREFLIGHT_NETWORK_BASELINE_FAILED:$($networkBaseline.outcome):$($networkBaseline.socket_error_code):$($networkBaseline.native_error_code)"
}

$finalStatus = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $finalStatus.Count -ne 0) { throw "CQ_HOST_PREFLIGHT_FINAL_WORKTREE_DIRTY" }
$finalHead = (& git rev-parse HEAD).Trim()
$finalTree = (& git rev-parse 'HEAD^{tree}').Trim()
if ($finalHead -ne $head -or $finalTree -ne $tree) {
    throw "CQ_HOST_PREFLIGHT_GIT_IDENTITY_CHANGED_DURING_HOST_VALIDATION"
}

$prEvidence = [ordered]@{ state = "DEFERRED_TO_EXTERNAL_ADJUDICATION"; source = "NONE" }
$gh = Get-Command "gh.exe" -ErrorAction SilentlyContinue
if ($gh) { try { $ghRaw = (& $gh.Source pr view 115 --repo Guimarais-R-Rodrigo/Ambiente_Databricks --json state,isDraft,mergedAt,headRefName,headRefOid 2>$null); if ($LASTEXITCODE -eq 0 -and $ghRaw) { $parsed = $ghRaw | ConvertFrom-Json; $prEvidence = [ordered]@{ state="OBSERVED_HOST_GH"; source="gh"; pr_state=$parsed.state; draft=$parsed.isDraft; merged_at=$parsed.mergedAt; head_ref=$parsed.headRefName; head_sha=$parsed.headRefOid } } } catch {} }
$recordedAt = [DateTimeOffset]::Now
$payload = [ordered]@{
    schema_version = "AC-R2-DESKTOP-HOST-PREFLIGHT-5"
    result = "PASS"
    client_surface = "CODEX_DESKTOP_WINDOWS"
    recorded_at = $recordedAt.ToString("o")
    recorded_at_unix_seconds = $recordedAt.ToUnixTimeSeconds()
    git = [ordered]@{ root=$root; branch=$branch; head=$head; tree=$tree; final_head=$finalHead; final_tree=$finalTree; origin_identity=$ExpectedRepoFragment; origin_tracking_ref=$originHead; fetch="PASS"; initial_clean=$true; final_clean=$true }
    python = [ordered]@{ executable=$python.executable; python_version=$python.python_version; implementation=$python.implementation; jsonschema_version=$python.jsonschema_version; execution_surface="HOST_ONLY" }
    project = [ordered]@{ config_path=$projectConfig; config_sha256=$sourceHashes.config; user_config_exists=$userConfigExists; user_config_sha256=$userConfigSha256 }
    source_sha256 = $sourceHashes
    host_validation = [ordered]@{
        validator = [ordered]@{ exit_code=$validatorExit; status=$validatorPayload.status; schema_version=$validatorPayload.schema_version; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $validatorStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $validatorStderr).Hash }
        metatests = [ordered]@{ exit_code=$metatestExit; result="PASS"; runtime_test_count=$runtimeTestCount; static_test_count=$staticTestCount; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $metatestStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $metatestStderr).Hash }
    }
    network_probe = [ordered]@{
        serialization_selftest = [ordered]@{
            result = "PASS"
            exit_code = $networkSelfTestExit
            network_attempt_count = [int]$networkSelfTestPayload.network_attempt_count
            case_count = [int]$networkSelfTestPayload.case_count
            cases = @($networkSelfTestPayload.cases)
            stdout_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $networkSelfTestStdout).Hash
            stderr_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $networkSelfTestStderr).Hash
        }
        hostname = $NetworkProbeHost
        port = $NetworkProbePort
        selected_ipv4 = $networkProbeIp
        resolved_ipv4 = $networkProbeAddresses
        host_baseline = [ordered]@{ result="PASS"; attempt_count=1; timeout_ms=$NetworkProbeTimeoutMs; outcome=$networkBaseline.outcome }
        executor_oracle = [ordered]@{ access_denied_socket_error="AccessDenied"; access_denied_native_error=10013; connected="FAIL_NETWORK_BOUNDARY_OPEN"; other_error="NOT_PROVEN" }
    }
    pr_115 = $prEvidence
    scratch_root = $outputRootFull
}
$jsonPath = Join-Path $outputRootFull "CQ_HOST_PREFLIGHT.json"
$shaPath = Join-Path $outputRootFull "CQ_HOST_PREFLIGHT.sha256"
$json = $payload | ConvertTo-Json -Depth 10
Write-Utf8NoBom $jsonPath $json
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $jsonPath).Hash
Write-Utf8NoBom $shaPath ($sha + "  CQ_HOST_PREFLIGHT.json" + [Environment]::NewLine)
Write-Host "CQ_HOST_PREFLIGHT = PASS"
Write-Host "HOST_VALIDATOR = PASS"
Write-Host "HOST_METATESTS = PASS ($runtimeTestCount/$staticTestCount)"
Write-Host "NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS (3/3; network_attempts=0)"
Write-Host ("HOST_NETWORK_BASELINE = PASS ({0}:{1})" -f $networkProbeIp, $NetworkProbePort)
Write-Host "HEAD = $head"
Write-Host "TREE = $tree"
Write-Host "ORIGIN_HEAD = $originHead"
Write-Host "PYTHON = $($python.executable)"
Write-Host "JSONSCHEMA = $($python.jsonschema_version)"
Write-Host "EVIDENCE = $jsonPath"
Write-Host "EVIDENCE_SHA256 = $sha"
