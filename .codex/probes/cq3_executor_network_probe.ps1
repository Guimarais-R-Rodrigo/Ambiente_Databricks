param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$EvidencePath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.json"
$SidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.sha256"
$TimeoutMs = 5000

function Emit-And-Exit($Payload, [int]$Code) {
    $Payload | ConvertTo-Json -Depth 10 | Write-Output
    exit $Code
}

if (-not (Test-Path -LiteralPath $EvidencePath) -or -not (Test-Path -LiteralPath $SidecarPath)) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="HOST_EVIDENCE_MISSING"; attempt_count=0 }) 30
}

$actualEvidenceSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $EvidencePath).Hash.ToUpperInvariant()
$sidecarText = (Get-Content -LiteralPath $SidecarPath -Raw).Trim()
$sidecarSha = (($sidecarText -split "\s+")[0]).ToUpperInvariant()
if ($sidecarSha -ne $actualEvidenceSha) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="HOST_EVIDENCE_SHA_MISMATCH"; attempt_count=0; actual_sha256=$actualEvidenceSha; sidecar_sha256=$sidecarSha }) 31
}

try { $evidence = Get-Content -LiteralPath $EvidencePath -Raw | ConvertFrom-Json }
catch { Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="HOST_EVIDENCE_INVALID_JSON"; attempt_count=0 }) 32 }

if ($evidence.schema_version -ne "AC-R2-DESKTOP-HOST-PREFLIGHT-4" -or $evidence.result -ne "PASS") {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="HOST_EVIDENCE_SCHEMA_OR_RESULT"; attempt_count=0 }) 33
}

$probeSourceHash = [string]$evidence.source_sha256.network_probe_script
if ([string]::IsNullOrWhiteSpace($probeSourceHash)) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="NETWORK_PROBE_SOURCE_HASH_MISSING"; attempt_count=0 }) 34
}
$actualProbeHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToUpperInvariant()
if ($actualProbeHash -ne $probeSourceHash.ToUpperInvariant()) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="NETWORK_PROBE_SOURCE_HASH_MISMATCH"; attempt_count=0; actual_probe_sha256=$actualProbeHash; expected_probe_sha256=$probeSourceHash }) 35
}

$baseline = $evidence.network_probe
if ($null -eq $baseline -or $baseline.host_baseline.result -ne "PASS" -or [int]$baseline.host_baseline.attempt_count -ne 1 -or [int]$baseline.port -ne 443) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="HOST_NETWORK_BASELINE_INVALID"; attempt_count=0 }) 36
}

$rootText = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $rootText) { Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="NOT_GIT_REPOSITORY"; attempt_count=0 }) 37 }
$root = [System.IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
Set-Location $root
$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
$tree = (& git rev-parse 'HEAD^{tree}').Trim()
$status = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $branch -ne $evidence.git.branch -or $head -ne $evidence.git.head -or $tree -ne $evidence.git.tree -or $status.Count -ne 0) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="CURRENT_IDENTITY_NOT_BOUND_TO_HOST_EVIDENCE"; attempt_count=0; branch=$branch; head=$head; tree=$tree; dirty=($status.Count -ne 0) }) 38
}

try { $targetIp = [System.Net.IPAddress]::Parse([string]$baseline.selected_ipv4) }
catch { Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="INVALID_BASELINE_IPV4"; attempt_count=0 }) 39 }
if ($targetIp.AddressFamily -ne [System.Net.Sockets.AddressFamily]::InterNetwork) {
    Emit-And-Exit ([ordered]@{ result="NOT_PROVEN"; reason="BASELINE_NOT_IPV4"; attempt_count=0 }) 40
}
$targetPort = [int]$baseline.port

$client = New-Object System.Net.Sockets.TcpClient -ArgumentList ([System.Net.Sockets.AddressFamily]::InterNetwork)
$async = $null
$attemptCount = 1
$connected = $false
$classification = "NOT_PROVEN"
$reason = $null
$exceptionChain = New-Object System.Collections.Generic.List[object]
$socketErrorCode = $null
$nativeErrorCode = $null
$socketHResult = $null
try {
    $async = $client.BeginConnect($targetIp, $targetPort, $null, $null)
    if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs)) {
        $classification = "NOT_PROVEN"
        $reason = "TIMEOUT"
    } else {
        $client.EndConnect($async)
        $connected = $client.Connected
        if ($connected) { $classification = "FAIL_NETWORK_BOUNDARY_OPEN" }
    }
} catch {
    $ex = $_.Exception
    while ($null -ne $ex) {
        $row = [ordered]@{ type=$ex.GetType().FullName; message=$ex.Message; hresult=$ex.HResult }
        if ($ex -is [System.Net.Sockets.SocketException]) {
            $row.socket_error_code = [string]$ex.SocketErrorCode
            $row.native_error_code = $ex.NativeErrorCode
            if ($null -eq $socketErrorCode) {
                $socketErrorCode = [string]$ex.SocketErrorCode
                $nativeErrorCode = $ex.NativeErrorCode
                $socketHResult = $ex.HResult
            }
        }
        $exceptionChain.Add([pscustomobject]$row)
        $ex = $ex.InnerException
    }
    if ($socketErrorCode -eq "AccessDenied" -or $nativeErrorCode -eq 10013) {
        $classification = "PASS_NETWORK_DENIED"
        $reason = "SANDBOX_ACCESS_DENIED"
    } else {
        $classification = "NOT_PROVEN"
        $reason = "NON_ACCESS_DENIED_EXCEPTION"
    }
} finally {
    if ($async -and $async.AsyncWaitHandle) { $async.AsyncWaitHandle.Close() }
    $client.Close()
}

$payload = [ordered]@{
    schema_version = "AC-R2-CQ3-EXECUTOR-NETWORK-PROBE-1"
    result = $classification
    reason = $reason
    preflight_sha256 = $actualEvidenceSha
    network_probe_source_sha256 = $actualProbeHash
    target_hostname = [string]$baseline.hostname
    target_ipv4 = $targetIp.IPAddressToString
    target_port = $targetPort
    transport = "TCP_RAW"
    dns_in_sandbox = $false
    http = $false
    tls = $false
    authentication = $false
    attempt_count = $attemptCount
    timeout_ms = $TimeoutMs
    connected = $connected
    exception_type = $(if ($exceptionChain.Count -gt 0) { $exceptionChain[0].type } else { $null })
    socket_error_code = $socketErrorCode
    native_error_code = $nativeErrorCode
    hresult = $socketHResult
    exception_chain = @($exceptionChain)
}

if ($classification -eq "PASS_NETWORK_DENIED") { Emit-And-Exit $payload 0 }
if ($classification -eq "FAIL_NETWORK_BOUNDARY_OPEN") { Emit-And-Exit $payload 20 }
Emit-And-Exit $payload 21
