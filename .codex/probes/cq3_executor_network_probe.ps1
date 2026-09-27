param(
    [switch]$SelfTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$EvidencePath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.json"
$SidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.sha256"
$TimeoutMs = 5000

function Convert-ProbePayloadToJson($Payload) {
    try {
        $json = ConvertTo-Json -InputObject $Payload -Depth 12 -Compress -ErrorAction Stop
        if ([string]::IsNullOrWhiteSpace($json)) { throw "EMPTY_JSON" }
        $null = $json | ConvertFrom-Json -ErrorAction Stop
        return [string]$json
    }
    catch {
        throw "CQ3_NETWORK_PROBE_JSON_SERIALIZATION_FAILED:$($_.Exception.GetType().FullName):$($_.Exception.Message)"
    }
}

function New-ProbePayload(
    [string]$Result,
    [string]$Reason,
    [string]$PreflightSha256,
    [string]$ProbeSha256,
    [string]$TargetHostname,
    [string]$TargetIpv4,
    [int]$TargetPort,
    [int]$AttemptCount,
    [bool]$Connected,
    [string]$SocketErrorCode,
    [Nullable[int]]$NativeErrorCode,
    [Nullable[int]]$SocketHResult,
    [object[]]$ExceptionChain
) {
    $exceptionType = $null
    if ($null -ne $ExceptionChain -and $ExceptionChain.Count -gt 0) {
        $exceptionType = [string]$ExceptionChain[0].type
    }
    return [ordered]@{
        schema_version = "AC-R2-CQ3-EXECUTOR-NETWORK-PROBE-2"
        result = $Result
        reason = $Reason
        preflight_sha256 = $PreflightSha256
        network_probe_source_sha256 = $ProbeSha256
        target_hostname = $TargetHostname
        target_ipv4 = $TargetIpv4
        target_port = $TargetPort
        transport = "TCP_RAW"
        dns_in_sandbox = $false
        http = $false
        tls = $false
        authentication = $false
        attempt_count = $AttemptCount
        timeout_ms = $TimeoutMs
        connected = $Connected
        exception_type = $exceptionType
        socket_error_code = $SocketErrorCode
        native_error_code = $NativeErrorCode
        hresult = $SocketHResult
        exception_chain = [object[]]$ExceptionChain
    }
}

function Emit-And-Exit($Payload, [int]$Code) {
    $json = Convert-ProbePayloadToJson $Payload
    Write-Output $json
    exit $Code
}

function Invoke-SerializationSelfTest {
    $syntheticChain = [object[]]@(
        [pscustomobject][ordered]@{
            type = "System.Net.Sockets.SocketException"
            message = "synthetic access denied"
            hresult = -2147467259
            socket_error_code = "AccessDenied"
            native_error_code = 10013
        }
    )
    $cases = [object[]]@(
        (New-ProbePayload -Result "PASS_NETWORK_DENIED" -Reason "SANDBOX_ACCESS_DENIED" -PreflightSha256 ("A" * 64) -ProbeSha256 ("B" * 64) -TargetHostname "example.invalid" -TargetIpv4 "192.0.2.1" -TargetPort 443 -AttemptCount 1 -Connected $false -SocketErrorCode "AccessDenied" -NativeErrorCode 10013 -SocketHResult -2147467259 -ExceptionChain $syntheticChain),
        (New-ProbePayload -Result "FAIL_NETWORK_BOUNDARY_OPEN" -Reason "TCP_CONNECTED" -PreflightSha256 ("A" * 64) -ProbeSha256 ("B" * 64) -TargetHostname "example.invalid" -TargetIpv4 "192.0.2.1" -TargetPort 443 -AttemptCount 1 -Connected $true -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())),
        (New-ProbePayload -Result "NOT_PROVEN" -Reason "TIMEOUT" -PreflightSha256 ("A" * 64) -ProbeSha256 ("B" * 64) -TargetHostname "example.invalid" -TargetIpv4 "192.0.2.1" -TargetPort 443 -AttemptCount 1 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@()))
    )
    $roundtrips = @()
    foreach ($case in $cases) {
        $json = Convert-ProbePayloadToJson $case
        $parsed = $json | ConvertFrom-Json -ErrorAction Stop
        if ([string]$parsed.result -ne [string]$case.result -or [int]$parsed.attempt_count -ne 1) {
            throw "CQ3_NETWORK_PROBE_SELFTEST_ROUNDTRIP_MISMATCH:$($case.result)"
        }
        $roundtrips += [pscustomobject][ordered]@{ result=[string]$parsed.result; json_roundtrip=$true; attempt_count=[int]$parsed.attempt_count }
    }
    $summary = [ordered]@{
        schema_version = "AC-R2-CQ3-NETWORK-PROBE-SELFTEST-1"
        result = "PASS"
        network_attempt_count = 0
        case_count = $roundtrips.Count
        cases = [object[]]$roundtrips
    }
    Write-Output (Convert-ProbePayloadToJson $summary)
}

if ($SelfTest) {
    Invoke-SerializationSelfTest
    exit 0
}

if (-not (Test-Path -LiteralPath $EvidencePath) -or -not (Test-Path -LiteralPath $SidecarPath)) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "HOST_EVIDENCE_MISSING" -PreflightSha256 "" -ProbeSha256 "" -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 30
}

$actualEvidenceSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $EvidencePath).Hash.ToUpperInvariant()
$sidecarText = (Get-Content -LiteralPath $SidecarPath -Raw).Trim()
$sidecarSha = (($sidecarText -split "\s+")[0]).ToUpperInvariant()
if ($sidecarSha -ne $actualEvidenceSha) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "HOST_EVIDENCE_SHA_MISMATCH" -PreflightSha256 $actualEvidenceSha -ProbeSha256 "" -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 31
}

try { $evidence = Get-Content -LiteralPath $EvidencePath -Raw | ConvertFrom-Json }
catch {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "HOST_EVIDENCE_INVALID_JSON" -PreflightSha256 $actualEvidenceSha -ProbeSha256 "" -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 32
}

if ($evidence.schema_version -ne "AC-R2-DESKTOP-HOST-PREFLIGHT-5" -or $evidence.result -ne "PASS") {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "HOST_EVIDENCE_SCHEMA_OR_RESULT" -PreflightSha256 $actualEvidenceSha -ProbeSha256 "" -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 33
}

$hostSerializationSelfTestEvidence = $evidence.network_probe.serialization_selftest
if ($null -eq $hostSerializationSelfTestEvidence -or $hostSerializationSelfTestEvidence.result -ne "PASS" -or [int]$hostSerializationSelfTestEvidence.network_attempt_count -ne 0 -or [int]$hostSerializationSelfTestEvidence.case_count -ne 3) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "HOST_SERIALIZATION_SELFTEST_INVALID" -PreflightSha256 $actualEvidenceSha -ProbeSha256 "" -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 34
}

$probeSourceHash = [string]$evidence.source_sha256.network_probe_script
if ([string]::IsNullOrWhiteSpace($probeSourceHash)) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "NETWORK_PROBE_SOURCE_HASH_MISSING" -PreflightSha256 $actualEvidenceSha -ProbeSha256 "" -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 35
}
$actualProbeHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToUpperInvariant()
if ($actualProbeHash -ne $probeSourceHash.ToUpperInvariant()) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "NETWORK_PROBE_SOURCE_HASH_MISMATCH" -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 36
}

$baseline = $evidence.network_probe
if ($null -eq $baseline -or $baseline.host_baseline.result -ne "PASS" -or [int]$baseline.host_baseline.attempt_count -ne 1 -or [int]$baseline.port -ne 443) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "HOST_NETWORK_BASELINE_INVALID" -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname "" -TargetIpv4 "" -TargetPort 0 -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 37
}

$rootText = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $rootText) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "NOT_GIT_REPOSITORY" -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname ([string]$baseline.hostname) -TargetIpv4 ([string]$baseline.selected_ipv4) -TargetPort ([int]$baseline.port) -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 38
}
$root = [System.IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
Set-Location $root
$branch = (& git branch --show-current).Trim()
$head = (& git rev-parse HEAD).Trim()
$tree = (& git rev-parse 'HEAD^{tree}').Trim()
$status = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $branch -ne $evidence.git.branch -or $head -ne $evidence.git.head -or $tree -ne $evidence.git.tree -or $status.Count -ne 0) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "CURRENT_IDENTITY_NOT_BOUND_TO_HOST_EVIDENCE" -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname ([string]$baseline.hostname) -TargetIpv4 ([string]$baseline.selected_ipv4) -TargetPort ([int]$baseline.port) -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 39
}

try { $targetIp = [System.Net.IPAddress]::Parse([string]$baseline.selected_ipv4) }
catch {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "INVALID_BASELINE_IPV4" -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname ([string]$baseline.hostname) -TargetIpv4 ([string]$baseline.selected_ipv4) -TargetPort ([int]$baseline.port) -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 40
}
if ($targetIp.AddressFamily -ne [System.Net.Sockets.AddressFamily]::InterNetwork) {
    Emit-And-Exit (New-ProbePayload -Result "NOT_PROVEN" -Reason "BASELINE_NOT_IPV4" -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname ([string]$baseline.hostname) -TargetIpv4 ([string]$baseline.selected_ipv4) -TargetPort ([int]$baseline.port) -AttemptCount 0 -Connected $false -SocketErrorCode $null -NativeErrorCode $null -SocketHResult $null -ExceptionChain ([object[]]@())) 41
}
$targetPort = [int]$baseline.port

$client = New-Object System.Net.Sockets.TcpClient -ArgumentList ([System.Net.Sockets.AddressFamily]::InterNetwork)
$async = $null
$attemptCount = 1
$connected = $false
$classification = "NOT_PROVEN"
$reason = $null
$exceptionChain = @()
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
        if ($connected) {
            $classification = "FAIL_NETWORK_BOUNDARY_OPEN"
            $reason = "TCP_CONNECTED"
        }
    }
} catch {
    $ex = $_.Exception
    while ($null -ne $ex) {
        $row = [ordered]@{ type=$ex.GetType().FullName; message=$ex.Message; hresult=$ex.HResult }
        if ($ex -is [System.Net.Sockets.SocketException]) {
            $row.socket_error_code = [string]$ex.SocketErrorCode
            $row.native_error_code = [int]$ex.NativeErrorCode
            if ($null -eq $socketErrorCode) {
                $socketErrorCode = [string]$ex.SocketErrorCode
                $nativeErrorCode = [int]$ex.NativeErrorCode
                $socketHResult = [int]$ex.HResult
            }
        }
        $exceptionChain += [pscustomobject]$row
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

$payload = New-ProbePayload -Result $classification -Reason $reason -PreflightSha256 $actualEvidenceSha -ProbeSha256 $actualProbeHash -TargetHostname ([string]$baseline.hostname) -TargetIpv4 $targetIp.IPAddressToString -TargetPort $targetPort -AttemptCount $attemptCount -Connected $connected -SocketErrorCode $socketErrorCode -NativeErrorCode $nativeErrorCode -SocketHResult $socketHResult -ExceptionChain ([object[]]$exceptionChain)

if ($classification -eq "PASS_NETWORK_DENIED") { Emit-And-Exit $payload 0 }
if ($classification -eq "FAIL_NETWORK_BOUNDARY_OPEN") { Emit-And-Exit $payload 20 }
Emit-And-Exit $payload 21
