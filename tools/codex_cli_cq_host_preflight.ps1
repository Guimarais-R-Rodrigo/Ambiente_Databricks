param(
    [string]$OutputRoot = "$HOME\codex-scratch\Ambiente_Databricks"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "ser/B1-ser03-ser05-authoring"
$ExpectedRepoFragment = "Guimarais-R-Rodrigo/Ambiente_Databricks"
$ExpectedRemotes = @(
    "https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks.git",
    "https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks",
    "git@github.com:Guimarais-R-Rodrigo/Ambiente_Databricks.git",
    "ssh://git@github.com/Guimarais-R-Rodrigo/Ambiente_Databricks.git"
)
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

function Normalize-GitMetadataPath([string]$Value) {
    $trimChars = [char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
    return [System.IO.Path]::GetFullPath($Value.Trim()).TrimEnd($trimChars)
}

function Quote-NativeArgument([string]$Value) {
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $escaped = [regex]::Replace($Value, '(\\*)"', '$1$1\"')
    $escaped = [regex]::Replace($escaped, '(\\+)$', '$1$1')
    return '"' + $escaped + '"'
}

function Show-CapturedDiagnostic([string]$Path) {
    Write-Host ("--- " + [IO.Path]::GetFileName($Path) + " ---")
    if (Test-Path -LiteralPath $Path) {
        $text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
        if ($text) { Write-Host $text } else { Write-Host "<empty>" }
    } else { Write-Host "<not created>" }
}

function Invoke-CapturedProcess([string]$FilePath, [string[]]$ArgumentList, [string]$StdoutPath, [string]$StderrPath) {
    Remove-Item -LiteralPath $StdoutPath -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $StderrPath -Force -ErrorAction SilentlyContinue
    $quoted = @($ArgumentList | ForEach-Object { Quote-NativeArgument $_ }) -join ' '
    Write-Host ("HOST_STEP = " + [IO.Path]::GetFileName($StdoutPath))

    # Windows PowerShell 5.1 can leave ExitCode unset on a Start-Process
    # -PassThru object even after WaitForExit() when redirected streams are used.
    # Use System.Diagnostics.Process directly and finalize async readers first.
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $FilePath
    $psi.Arguments = $quoted
    $psi.WorkingDirectory = (Get-Location).Path
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    try {
        if (-not $process.Start()) {
            throw "CQ_HOST_PREFLIGHT_CHILD_START_FAILED"
        }

        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()

        if (-not $process.WaitForExit(600000)) {
            try { $process.Kill() } catch {}
            $process.WaitForExit()
            $stdout = [string]$stdoutTask.Result
            $stderr = [string]$stderrTask.Result
            Write-Utf8NoBom $StdoutPath $stdout
            Write-Utf8NoBom $StderrPath $stderr
            Show-CapturedDiagnostic $StdoutPath
            Show-CapturedDiagnostic $StderrPath
            throw "CQ_HOST_PREFLIGHT_CHILD_TIMEOUT_NO_RETRY"
        }

        $process.WaitForExit()
        $stdout = [string]$stdoutTask.Result
        $stderr = [string]$stderrTask.Result
        $process.Refresh()
        $exitCode = [int]$process.ExitCode

        Write-Utf8NoBom $StdoutPath $stdout
        Write-Utf8NoBom $StderrPath $stderr

        if ($exitCode -ne 0) {
            Show-CapturedDiagnostic $StdoutPath
            Show-CapturedDiagnostic $StderrPath
        }
        return $exitCode
    }
    finally {
        if ($null -ne $process) { $process.Dispose() }
    }
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

$canonicalOutputRoot = [IO.Path]::GetFullPath((Join-Path $HOME "codex-scratch\Ambiente_Databricks"))
if (-not [string]::Equals([IO.Path]::GetFullPath($OutputRoot).TrimEnd('\','/'), $canonicalOutputRoot.TrimEnd('\','/'), [StringComparison]::OrdinalIgnoreCase)) {
    throw "CQ_HOST_PREFLIGHT_OUTPUT_ROOT_MUST_MATCH_CONSUMERS"
}
New-Item -ItemType Directory -Force -Path $canonicalOutputRoot | Out-Null
$readyPath = Join-Path $canonicalOutputRoot "CQ_LAUNCH_READY.json"
$runId = [Guid]::NewGuid().ToString("N")
$ready = [ordered]@{ schema_version="SER-CQ-LAUNCH-READY-1"; run_id=$runId; result="IN_PROGRESS"; phase="HOST_PREFLIGHT_ONLY" }
Write-Utf8NoBom $readyPath ($ready | ConvertTo-Json -Depth 6)
$previousPythonEncoding = $env:PYTHONIOENCODING
$env:PYTHONIOENCODING = "utf-8"
try {
$rootText = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $rootText) { throw "CQ_HOST_PREFLIGHT_NOT_GIT_REPOSITORY" }
$root = [System.IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
Set-Location $root

$gitDirText = (& git rev-parse --path-format=absolute --git-dir 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $gitDirText) { throw "CQ_HOST_PREFLIGHT_GIT_DIR_UNRESOLVED" }
$gitCommonDirText = (& git rev-parse --path-format=absolute --git-common-dir 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $gitCommonDirText) { throw "CQ_HOST_PREFLIGHT_COMMON_DIR_UNRESOLVED" }
$gitDir = Normalize-GitMetadataPath (($gitDirText | Select-Object -First 1).Trim())
$gitCommonDir = Normalize-GitMetadataPath (($gitCommonDirText | Select-Object -First 1).Trim())
$expectedGitMetadataDir = Normalize-GitMetadataPath (Join-Path $root ".git")
if (
    -not [string]::Equals($gitDir, $expectedGitMetadataDir, [StringComparison]::OrdinalIgnoreCase) -or
    -not [string]::Equals($gitCommonDir, $expectedGitMetadataDir, [StringComparison]::OrdinalIgnoreCase)
) {
    throw "CQ_HOST_PREFLIGHT_LINKED_WORKTREE_UNSUPPORTED"
}
$checkoutMode = "STANDALONE"

$initialStatus = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $initialStatus.Count -ne 0) { throw "CQ_HOST_PREFLIGHT_WORKTREE_DIRTY" }
$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) { throw "CQ_HOST_PREFLIGHT_BRANCH_MISMATCH:$branch" }
$origin = (& git remote get-url origin).Trim()
$pushOrigin = (& git remote get-url --push origin).Trim()
if (
    $LASTEXITCODE -ne 0 -or
    $ExpectedRemotes -notcontains $origin -or
    $ExpectedRemotes -notcontains $pushOrigin
) { throw "CQ_HOST_PREFLIGHT_REMOTE_MISMATCH" }
& git fetch origin $ExpectedBranch
if ($LASTEXITCODE -ne 0) { throw "CQ_HOST_PREFLIGHT_FETCH_FAILED" }
$head = (& git rev-parse HEAD).Trim()
$originHead = (& git rev-parse "origin/$ExpectedBranch").Trim()
$tree = (& git rev-parse 'HEAD^{tree}').Trim()
if ($head -ne $originHead) { throw "CQ_HOST_PREFLIGHT_LOCAL_REMOTE_DIVERGENCE:$($head):$($originHead)" }

$validatorModeRow = (& git ls-files -s -- tools/validate_codex_autonomy.py).Trim()
if (
    $LASTEXITCODE -ne 0 -or
    $validatorModeRow -notmatch "^100755\s+([0-9a-f]{40})\s+0\s+tools/validate_codex_autonomy.py$"
) { throw "CQ_HOST_PREFLIGHT_VALIDATOR_MODE_NOT_100755" }
$validatorBlob = $Matches[1]

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$outputRootFull = [System.IO.Path]::GetFullPath($OutputRoot)

$codexCli = [System.IO.Path]::GetFullPath((Join-Path $env:APPDATA "npm\codex.cmd"))
if (-not (Test-Path -LiteralPath $codexCli)) { throw "CQ_HOST_PREFLIGHT_CODEX_CLI_MISSING:$codexCli" }
$codexVersionStdout = Join-Path $outputRootFull "CQ_HOST_CODEX_CLI_VERSION.stdout.txt"
$codexVersionStderr = Join-Path $outputRootFull "CQ_HOST_CODEX_CLI_VERSION.stderr.txt"
$codexVersionExit = Invoke-CapturedProcess -FilePath $codexCli -ArgumentList @("--version") -StdoutPath $codexVersionStdout -StderrPath $codexVersionStderr
if ($codexVersionExit -ne 0) { throw "CQ_HOST_PREFLIGHT_CODEX_CLI_VERSION_FAILED:$codexVersionExit" }
$codexVersion = (Get-Content -LiteralPath $codexVersionStdout -Raw -Encoding UTF8).Trim()
if ([string]::IsNullOrWhiteSpace($codexVersion) -or $codexVersion -notmatch "^codex-cli\s+\S+") { throw "CQ_HOST_PREFLIGHT_CODEX_CLI_VERSION_UNPARSEABLE:$codexVersion" }

$sourcePaths = [ordered]@{
    config = ".codex\config.toml"
    envelope = "docs\operations\autonomy\B1_AUTONOMY_ENVELOPE.json"
    envelope_schema = "docs\operations\autonomy\autonomy-envelope.schema.json"
    agents_md = "AGENTS.md"
    controller_skill = ".agents\skills\ser-autonomous-controller\SKILL.md"
    validator = "tools\validate_codex_autonomy.py"
    metatests = "tools\tests\test_codex_autonomy.py"
    delta_checker = "tools\check_codex_autonomy_delta.py"
    network_probe_script = ".codex\probes\cq3_executor_network_probe.ps1"
    transport = ".codex\transport\a1_git_transport.ps1"
    operational_transport = ".codex\transport\a1_operational_git_transport.ps1"
    operational_policy = "docs\operations\autonomy\A1_OPERATIONAL_POLICY.json"
    rules = ".codex\rules\a1_git_transport.rules"
    executor_agent = ".codex\agents\executor.toml"
    explorer_agent = ".codex\agents\explorer.toml"
    domain_auditor_agent = ".codex\agents\domain-auditor.toml"
    evidence_auditor_agent = ".codex\agents\evidence-auditor.toml"
    architecture_auditor_agent = ".codex\agents\architecture-auditor.toml"
    protocol = "docs\operations\CODEX_AUTONOMOUS_PROTOCOL.md"
    runtime_contract = "docs\operations\CODEX_RUNTIME_QUALIFICATION.md"
    cli_contract = "docs\operations\CODEX_CLI_WINDOWS_CQ.md"
    cli_preflight = "tools\codex_cli_cq_host_preflight.ps1"
    start_prompt = "docs\operations\CODEX_AUTONOMOUS_START_PROMPT.md"
    hooks = ".codex\config.toml"
    pre_scope_guard = ".codex\hooks\pre_scope_guard.ps1"
    pre_scope_guard_python = ".codex\hooks\pre_scope_guard.py"
    post_scope_guard = ".codex\hooks\post_scope_guard.ps1"
    post_scope_guard_python = ".codex\hooks\post_scope_guard.py"
    external_surface_guard = ".codex\hooks\external_surface_guard.ps1"
    external_surface_guard_python = ".codex\hooks\external_surface_guard.py"
    tool_surface_policy = "docs\operations\autonomy\CODEX_CLI_TOOL_SURFACE_POLICY.json"
    prompt_template = "docs\operations\CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md"
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
try { $validatorPayload = Get-Content -LiteralPath $validatorStdout -Raw -Encoding UTF8 | ConvertFrom-Json } catch { throw "CQ_HOST_PREFLIGHT_VALIDATOR_OUTPUT_NOT_JSON" }
if ($validatorExit -ne 0 -or $validatorPayload.status -ne "PASS") { throw "CQ_HOST_PREFLIGHT_VALIDATOR_FAILED:$($validatorExit):$($validatorPayload.status)" }
if ($validatorPayload.schema_version -ne "SER-CODEX-AUTONOMY-VALIDATION-21") { throw "CQ_HOST_PREFLIGHT_VALIDATOR_SCHEMA:$($validatorPayload.schema_version)" }
$metatestExit = Invoke-CapturedProcess -FilePath $python.executable -ArgumentList @("-B", "-m", "unittest", "tools.tests.test_codex_autonomy", "-v") -StdoutPath $metatestStdout -StderrPath $metatestStderr
$metatestText = ""
if (Test-Path -LiteralPath $metatestStdout) { $metatestText += Get-Content -LiteralPath $metatestStdout -Raw -Encoding UTF8 }
if (Test-Path -LiteralPath $metatestStderr) { $metatestText += [Environment]::NewLine + (Get-Content -LiteralPath $metatestStderr -Raw -Encoding UTF8) }
if ($metatestExit -ne 0) { throw "CQ_HOST_PREFLIGHT_METATESTS_FAILED:$metatestExit" }
if ($metatestText -match "skipped=[1-9][0-9]*") { throw "CQ_HOST_PREFLIGHT_WINDOWS_TESTS_SKIPPED" }
if ($metatestText -notmatch "Ran\s+(\d+)\s+tests?") { throw "CQ_HOST_PREFLIGHT_METATEST_COUNT_NOT_OBSERVED" }
$runtimeTestCount = [int]$Matches[1]
$testSourceText = Get-Content -LiteralPath (Join-Path $root "tools\tests\test_codex_autonomy.py") -Raw -Encoding UTF8
$staticTestCount = [regex]::Matches($testSourceText, "(?m)^\s+def test_").Count
if ($runtimeTestCount -ne $staticTestCount) { throw "CQ_HOST_PREFLIGHT_METATEST_COUNT_MISMATCH:$($runtimeTestCount):$($staticTestCount)" }

$networkProbeScript = Join-Path $root ".codex\probes\cq3_executor_network_probe.ps1"
$networkSelfTestStdout = Join-Path $outputRootFull "CQ_HOST_NETWORK_PROBE_SELFTEST.stdout.txt"
$networkSelfTestStderr = Join-Path $outputRootFull "CQ_HOST_NETWORK_PROBE_SELFTEST.stderr.txt"
$powershellExe = (Get-Command "powershell.exe" -ErrorAction Stop).Source
$networkSelfTestExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", $networkProbeScript, "-SelfTest") -StdoutPath $networkSelfTestStdout -StderrPath $networkSelfTestStderr
if ($networkSelfTestExit -ne 0) { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_SELFTEST_EXIT:$($networkSelfTestExit)" }
try { $networkSelfTestPayload = Get-Content -LiteralPath $networkSelfTestStdout -Raw -Encoding UTF8 | ConvertFrom-Json }
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

$networkOfflineStdout = Join-Path $outputRootFull "CQ_HOST_NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST.stdout.txt"
$networkOfflineStderr = Join-Path $outputRootFull "CQ_HOST_NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST.stderr.txt"
$networkOfflineExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", $networkProbeScript, "-OfflineRuntimeSelfTest") -StdoutPath $networkOfflineStdout -StderrPath $networkOfflineStderr
if ($networkOfflineExit -ne 0) { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST_EXIT:$($networkOfflineExit)" }
try { $networkOfflinePayload = Get-Content -LiteralPath $networkOfflineStdout -Raw -Encoding UTF8 | ConvertFrom-Json }
catch { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST_JSON" }
if (
    $networkOfflinePayload.schema_version -ne "AC-R2-CQ3-NETWORK-PROBE-OFFLINE-RUNTIME-SELFTEST-1" -or
    $networkOfflinePayload.result -ne "PASS" -or
    [int]$networkOfflinePayload.parameter_assignment_collisions -ne 0 -or
    [int]$networkOfflinePayload.network_attempt_count -ne 0
) { throw "CQ_HOST_PREFLIGHT_NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST_CONTRACT" }

$mcpGuardStdout = Join-Path $outputRootFull "CQ_HOST_EXTERNAL_SURFACE_GUARD_SELFTEST.stdout.txt"
$mcpGuardStderr = Join-Path $outputRootFull "CQ_HOST_EXTERNAL_SURFACE_GUARD_SELFTEST.stderr.txt"
$mcpGuardExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $root ".codex\hooks\external_surface_guard.ps1"), "-SelfTest") -StdoutPath $mcpGuardStdout -StderrPath $mcpGuardStderr
if ($mcpGuardExit -ne 0) { throw "CQ_HOST_PREFLIGHT_MCP_GUARD_SELFTEST_EXIT:$($mcpGuardExit)" }
try { $mcpGuardPayload = Get-Content -LiteralPath $mcpGuardStdout -Raw -Encoding UTF8 | ConvertFrom-Json }
catch { throw "CQ_HOST_PREFLIGHT_MCP_GUARD_SELFTEST_JSON" }
if ($mcpGuardPayload.result -ne "PASS") { throw "CQ_HOST_PREFLIGHT_MCP_GUARD_SELFTEST_CONTRACT" }

$preGuardStdout = Join-Path $outputRootFull "CQ_HOST_PRE_SCOPE_GUARD_SELFTEST.stdout.txt"
$preGuardStderr = Join-Path $outputRootFull "CQ_HOST_PRE_SCOPE_GUARD_SELFTEST.stderr.txt"
$preGuardExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $root ".codex\hooks\pre_scope_guard.ps1"), "-SelfTest") -StdoutPath $preGuardStdout -StderrPath $preGuardStderr
if ($preGuardExit -ne 0) { throw "CQ_HOST_PREFLIGHT_PRE_SCOPE_GUARD_SELFTEST_EXIT:$($preGuardExit)" }

$postGuardStdout = Join-Path $outputRootFull "CQ_HOST_POST_SCOPE_GUARD_SELFTEST.stdout.txt"
$postGuardStderr = Join-Path $outputRootFull "CQ_HOST_POST_SCOPE_GUARD_SELFTEST.stderr.txt"
$postGuardExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $root ".codex\hooks\post_scope_guard.ps1"), "-SelfTest") -StdoutPath $postGuardStdout -StderrPath $postGuardStderr
if ($postGuardExit -ne 0) { throw "CQ_HOST_PREFLIGHT_POST_SCOPE_GUARD_SELFTEST_EXIT:$($postGuardExit)" }

$operationalTransportStdout = Join-Path $outputRootFull "CQ_HOST_A1_OPERATIONAL_TRANSPORT_SELFTEST.stdout.txt"
$operationalTransportStderr = Join-Path $outputRootFull "CQ_HOST_A1_OPERATIONAL_TRANSPORT_SELFTEST.stderr.txt"
$operationalTransportExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $root ".codex\transport\a1_operational_git_transport.ps1"), "-SelfTest") -StdoutPath $operationalTransportStdout -StderrPath $operationalTransportStderr
if ($operationalTransportExit -ne 0) { throw "CQ_HOST_PREFLIGHT_A1_OPERATIONAL_TRANSPORT_SELFTEST_EXIT:$($operationalTransportExit)" }
try { $operationalTransportPayload = Get-Content -LiteralPath $operationalTransportStdout -Raw -Encoding UTF8 | ConvertFrom-Json }
catch { throw "CQ_HOST_PREFLIGHT_A1_OPERATIONAL_TRANSPORT_SELFTEST_JSON" }
if ($operationalTransportPayload.result -ne "PASS") { throw "CQ_HOST_PREFLIGHT_A1_OPERATIONAL_TRANSPORT_SELFTEST_CONTRACT" }
$transportStdout = Join-Path $outputRootFull "CQ_HOST_A1_GIT_TRANSPORT_SELFTEST.stdout.txt"
$transportStderr = Join-Path $outputRootFull "CQ_HOST_A1_GIT_TRANSPORT_SELFTEST.stderr.txt"
$transportExit = Invoke-CapturedProcess -FilePath $powershellExe -ArgumentList @("-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $root ".codex\transport\a1_git_transport.ps1"), "-SelfTest") -StdoutPath $transportStdout -StderrPath $transportStderr
if ($transportExit -ne 0) { throw "CQ_HOST_PREFLIGHT_A1_GIT_TRANSPORT_SELFTEST_EXIT:$($transportExit)" }
try { $transportPayload = Get-Content -LiteralPath $transportStdout -Raw -Encoding UTF8 | ConvertFrom-Json }
catch { throw "CQ_HOST_PREFLIGHT_A1_GIT_TRANSPORT_SELFTEST_JSON" }
if ($transportPayload.result -ne "PASS") { throw "CQ_HOST_PREFLIGHT_A1_GIT_TRANSPORT_SELFTEST_CONTRACT" }

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

foreach ($key in $sourcePaths.Keys) {
    $currentHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root $sourcePaths[$key])).Hash
    if ($currentHash -ne $sourceHashes[$key]) { throw "CQ_HOST_PREFLIGHT_SOURCE_CHANGED_DURING_VALIDATION:$key" }
}

$prEvidence = [ordered]@{ state = "DEFERRED_TO_EXTERNAL_ADJUDICATION"; source = "NONE" }
$gh = Get-Command "gh.exe" -ErrorAction SilentlyContinue
if ($gh) { try { $ghRaw = (& $gh.Source pr view 115 --repo Guimarais-R-Rodrigo/Ambiente_Databricks --json state,isDraft,mergedAt,headRefName,headRefOid 2>$null); if ($LASTEXITCODE -eq 0 -and $ghRaw) { $parsed = $ghRaw | ConvertFrom-Json; $prEvidence = [ordered]@{ state="OBSERVED_HOST_GH"; source="gh"; pr_state=$parsed.state; draft=$parsed.isDraft; merged_at=$parsed.mergedAt; head_ref=$parsed.headRefName; head_sha=$parsed.headRefOid } } } catch {} }
$recordedAt = [DateTimeOffset]::Now
$payload = [ordered]@{
    schema_version = "AC-R2-CLI-HOST-PREFLIGHT-1"
    result = "PASS"
    client_surface = "CODEX_CLI_WINDOWS_TUI"
    run_id = $runId
    launch_ready_path = $readyPath
    recorded_at = $recordedAt.ToString("o")
    recorded_at_unix_seconds = $recordedAt.ToUnixTimeSeconds()
    git = [ordered]@{ root=$root; checkout_mode=$checkoutMode; git_dir=$gitDir; git_common_dir=$gitCommonDir; branch=$branch; head=$head; tree=$tree; final_head=$finalHead; final_tree=$finalTree; origin_identity=$ExpectedRepoFragment; origin_tracking_ref=$originHead; fetch="PASS"; initial_clean=$true; final_clean=$true }
    python = [ordered]@{ executable=$python.executable; python_version=$python.python_version; implementation=$python.implementation; jsonschema_version=$python.jsonschema_version; execution_surface="HOST_ONLY" }
    project = [ordered]@{ config_path=$projectConfig; config_sha256=$sourceHashes.config; user_config_exists=$userConfigExists; user_config_sha256=$userConfigSha256; validator_git_mode="100755"; validator_blob=$validatorBlob }
    codex_cli = [ordered]@{ executable=$codexCli; version=$codexVersion; launcher="EXPLICIT_APPDATA_NPM_CODEX_CMD"; launcher_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $codexCli).Hash }
    source_sha256 = $sourceHashes
    host_validation = [ordered]@{
        validator = [ordered]@{ exit_code=$validatorExit; status=$validatorPayload.status; schema_version=$validatorPayload.schema_version; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $validatorStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $validatorStderr).Hash }
        metatests = [ordered]@{ exit_code=$metatestExit; result="PASS"; runtime_test_count=$runtimeTestCount; static_test_count=$staticTestCount; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $metatestStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $metatestStderr).Hash }
    }
    host_contract_selftests = [ordered]@{
        network_offline_runtime = [ordered]@{ result="PASS"; exit_code=$networkOfflineExit; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $networkOfflineStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $networkOfflineStderr).Hash }
        mcp_guard = [ordered]@{ result="PASS"; exit_code=$mcpGuardExit; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $mcpGuardStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $mcpGuardStderr).Hash }
        scope_guards = [ordered]@{ result="PASS"; pre_exit_code=$preGuardExit; post_exit_code=$postGuardExit }
        a1_operational_transport = [ordered]@{ result="PASS"; exit_code=$operationalTransportExit; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $operationalTransportStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $operationalTransportStderr).Hash }
        a1_git_transport = [ordered]@{ result="PASS"; exit_code=$transportExit; stdout_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $transportStdout).Hash; stderr_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $transportStderr).Hash }
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

$requestPath = Join-Path $outputRootFull "CQ_RUN_REQUEST.json"
$requestShaPath = Join-Path $outputRootFull "CQ_RUN_REQUEST.sha256"
$promptPath = Join-Path $outputRootFull "CQ_RUN_PROMPT.md"
$promptTemplatePath = Join-Path $root "docs\operations\CODEX_CLI_CQ_RUN_PROMPT_TEMPLATE.md"
$request = [ordered]@{
    schema_version = "SER-CODEX-CLI-CQ-REQUEST-1"
    client_surface = "CODEX_CLI_WINDOWS_TUI"
    run_id = $runId
    launch_ready_path = $readyPath
    checkout_mode = $checkoutMode
    branch = $branch
    candidate_head = $head
    candidate_tree = $tree
    host_preflight_schema = "AC-R2-CLI-HOST-PREFLIGHT-1"
    host_evidence_path = $jsonPath
    host_evidence_sha256 = $sha
    validator_schema = [string]$validatorPayload.schema_version
    validator_git_mode = "100755"
    validator_blob = $validatorBlob
    metatest_count = $runtimeTestCount
    codex_cli = $payload.codex_cli
    network = [ordered]@{ selected_ipv4=$networkProbeIp; port=$NetworkProbePort; host_baseline="PASS"; serialization_selftest="PASS"; offline_runtime_selftest="PASS" }
    tool_surface_policy = [ordered]@{ path="docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json"; source_sha256=$sourceHashes.tool_surface_policy; schema_version="SER-CODEX-CLI-TOOL-SURFACE-1"; mcp_invocation="DENY_EXTERNAL_SURFACES_ALLOW_INTERNAL_NODE_REPL"; absent_probeable_surface="NOT_APPLICABLE_ABSENT" }
    hook_trust = [ordered]@{
        project_hooks_sha256 = $sourceHashes.hooks
        requirement = "REVIEW_AND_TRUST_CURRENT_PROJECT_HOOKS_BEFORE_CQ"
        runtime_verification = "REQUIRED_BEFORE_CQ0"
    }
    restrictions = @("NO_B1_MATERIAL","NO_A2","NO_G6_GENIE_DATABRICKS_MATERIAL","NO_POLICY_PROMOTION","NO_READY","NO_MERGE")
}
$requestJson = $request | ConvertTo-Json -Depth 10
Write-Utf8NoBom $requestPath $requestJson
try { $requestRoundtrip = Get-Content -LiteralPath $requestPath -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop }
catch { throw "CQ_HOST_PREFLIGHT_RUN_REQUEST_INVALID_JSON" }
if (
    $requestRoundtrip.schema_version -ne "SER-CODEX-CLI-CQ-REQUEST-1" -or
    $requestRoundtrip.checkout_mode -ne "STANDALONE" -or
    $requestRoundtrip.candidate_head -ne $head -or
    $requestRoundtrip.candidate_tree -ne $tree -or
    $requestRoundtrip.host_evidence_sha256 -ne $sha
) { throw "CQ_HOST_PREFLIGHT_RUN_REQUEST_ROUNDTRIP_MISMATCH" }
$requestSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $requestPath).Hash
Write-Utf8NoBom $requestShaPath ($requestSha + "  CQ_RUN_REQUEST.json" + [Environment]::NewLine)

$promptTemplate = Get-Content -LiteralPath $promptTemplatePath -Raw -Encoding UTF8
$renderedPrompt = $promptTemplate.Replace("{{REQUEST_PATH}}",$requestPath).Replace("{{REQUEST_SHA256}}",$requestSha).Replace("{{EVIDENCE_SHA256}}",$sha).Replace("{{BRANCH}}",$branch).Replace("{{HEAD}}",$head).Replace("{{TREE}}",$tree).Replace("{{VALIDATOR_SCHEMA}}",[string]$validatorPayload.schema_version).Replace("{{METATEST_COUNT}}",[string]$runtimeTestCount).Replace("{{PREFLIGHT_SCHEMA}}","AC-R2-CLI-HOST-PREFLIGHT-1").Replace("{{HOOKS_SHA256}}",$sourceHashes.hooks).Replace("{{SURFACE_POLICY_SHA256}}",$sourceHashes.tool_surface_policy).Replace("{{CODEX_CLI_VERSION}}",$codexVersion).Replace("{{READY_PATH}}",$readyPath)
if ($renderedPrompt -match "\{\{[A-Z0-9_]+\}\}") { throw "CQ_HOST_PREFLIGHT_PROMPT_TEMPLATE_UNRESOLVED" }
Write-Utf8NoBom $promptPath $renderedPrompt
$promptSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $promptPath).Hash
$ready.result = "PASS"
$ready['recorded_at_unix_seconds'] = $payload.recorded_at_unix_seconds
$ready['head'] = $head
$ready['tree'] = $tree
$ready['request_sha256'] = $requestSha
$ready['evidence_sha256'] = $sha
$ready['prompt_sha256'] = $promptSha
Write-Utf8NoBom $readyPath ($ready | ConvertTo-Json -Depth 6)
Write-Host "CQ_HOST_PREFLIGHT = PASS"
Write-Host "HOST_VALIDATOR = PASS"
Write-Host "HOST_METATESTS = PASS ($runtimeTestCount/$staticTestCount)"
Write-Host "NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST = PASS"
Write-Host "MCP_GUARD_SELFTEST = PASS"
Write-Host "EXTERNAL_SURFACE_GUARD_SELFTEST = PASS"
Write-Host "SCOPE_GUARDS_SELFTEST = PASS"
Write-Host "A1_GIT_TRANSPORT_SELFTEST = PASS"
Write-Host "A1_OPERATIONAL_TRANSPORT_SELFTEST = PASS"
Write-Host "NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS (3/3; network_attempts=0)"
Write-Host ("HOST_NETWORK_BASELINE = PASS ({0}:{1})" -f $networkProbeIp, $NetworkProbePort)
Write-Host "CHECKOUT_MODE = STANDALONE"
Write-Host "CLIENT_SURFACE = CODEX_CLI_WINDOWS_TUI"
Write-Host "CODEX_CLI = $codexCli"
Write-Host "CODEX_CLI_VERSION = $codexVersion"
Write-Host "HEAD = $head"
Write-Host "TREE = $tree"
Write-Host "ORIGIN_HEAD = $originHead"
Write-Host "PYTHON = $($python.executable)"
Write-Host "JSONSCHEMA = $($python.jsonschema_version)"
Write-Host "EVIDENCE = $jsonPath"
Write-Host "EVIDENCE_SHA256 = $sha"
Write-Host "CQ_RUN_REQUEST = $requestPath"
Write-Host "CQ_RUN_REQUEST_SHA256 = $requestSha"
Write-Host "CQ_RUN_PROMPT = $promptPath"
Write-Host "CQ_RUN_PROMPT_SHA256 = $promptSha"
Write-Host "PROJECT_HOOKS_SHA256 = $($sourceHashes.hooks)"
Write-Host "HOOK_TRUST_REVIEW_REQUIRED = true"
Write-Host "CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST"

}
catch {
    $ready.result = "FAIL"
    $ready['error'] = [string]$_.Exception.Message
    Write-Utf8NoBom $readyPath ($ready | ConvertTo-Json -Depth 6)
    Write-Host "CQ_LAUNCH_READY = FAIL; do not reuse a previous CQ_RUN_PROMPT.md"
    throw
}
finally {
    if ($null -eq $previousPythonEncoding) {
        Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
    } else { $env:PYTHONIOENCODING = $previousPythonEncoding }
}
