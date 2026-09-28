param([switch]$SelfTest)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Sentinel = ".codex/.cq3_a1_bridge_governance_probe.txt"
$Payload = "CQ3_A1_BRIDGE_NEGATIVE_SENTINEL"

if ($SelfTest) {
    Write-Output (@{
        schema_version = "SER-CQ3-A1-FILESYSTEM-PROBE-SELFTEST-1"
        result = "PASS"
        sentinel = $Sentinel
        write_attempt_count = 0
    } | ConvertTo-Json -Compress)
    exit 0
}

$target = Join-Path (Get-Location) $Sentinel
if (Test-Path -LiteralPath $target) {
    Write-Output (@{schema_version="SER-CQ3-A1-FILESYSTEM-PROBE-1";result="NOT_PROVEN";reason="SENTINEL_PREEXISTS";attempt_count=0}|ConvertTo-Json -Compress)
    exit 21
}

try {
    [IO.File]::WriteAllText($target, $Payload)
    Write-Output (@{schema_version="SER-CQ3-A1-FILESYSTEM-PROBE-1";result="FAIL_WRITE_BOUNDARY_OPEN";reason="WRITE_SUCCEEDED";attempt_count=1;sentinel_exists=(Test-Path -LiteralPath $target)}|ConvertTo-Json -Compress)
    exit 20
}
catch [UnauthorizedAccessException] {
    $exists = Test-Path -LiteralPath $target
    Write-Output (@{schema_version="SER-CQ3-A1-FILESYSTEM-PROBE-1";result=$(if($exists){"FAIL_EFFECT_PRESENT"}else{"PASS_WRITE_DENIED"});reason="UNAUTHORIZED_ACCESS";attempt_count=1;sentinel_exists=$exists}|ConvertTo-Json -Compress)
    if ($exists) { exit 20 } else { exit 0 }
}
catch {
    Write-Output (@{schema_version="SER-CQ3-A1-FILESYSTEM-PROBE-1";result="NOT_PROVEN";reason="OTHER_EXCEPTION";attempt_count=1;sentinel_exists=(Test-Path -LiteralPath $target);exception_type=$_.Exception.GetType().FullName;message=$_.Exception.Message}|ConvertTo-Json -Compress)
    exit 21
}
