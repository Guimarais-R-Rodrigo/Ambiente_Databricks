param([switch]$SelfTest)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$PrivilegedLeaves = @(
    "a1_patch_transport.ps1",
    "a1_git_transport.ps1",
    "a1_operational_git_transport.ps1"
)

function New-Deny([string]$Reason) {
    return @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "deny"
            permissionDecisionReason = $Reason
        }
    }
}

function Test-PrivilegedCommand([string]$Command) {
    foreach ($leaf in $PrivilegedLeaves) {
        if ($Command.IndexOf($leaf, [StringComparison]::OrdinalIgnoreCase) -ge 0) { return $true }
    }
    return $false
}

function Test-RootMeta([object]$Meta, [string]$SessionId, [string]$Cwd) {
    if ($null -eq $Meta) { return $false }
    if ([string]$Meta.id -ne $SessionId) { return $false }
    $source = $Meta.PSObject.Properties["source"]
    if ($null -eq $source -or $source.Value -isnot [string] -or [string]$source.Value -cne "cli") { return $false }
    $parent = $Meta.PSObject.Properties["parent_thread_id"]
    if ($null -ne $parent -and -not [string]::IsNullOrWhiteSpace([string]$parent.Value)) { return $false }
    try {
        $metaCwd = [IO.Path]::GetFullPath([string]$Meta.cwd).TrimEnd('\','/')
        $eventCwd = [IO.Path]::GetFullPath($Cwd).TrimEnd('\','/')
    } catch { return $false }
    return [string]::Equals($metaCwd, $eventCwd, [StringComparison]::OrdinalIgnoreCase)
}

function Read-SessionMeta([string]$TranscriptPath) {
    if ([string]::IsNullOrWhiteSpace($TranscriptPath) -or -not (Test-Path -LiteralPath $TranscriptPath -PathType Leaf)) { return $null }
    $sessionsRoot = [IO.Path]::GetFullPath((Join-Path $HOME ".codex\sessions")).TrimEnd('\','/')
    try { $full = [IO.Path]::GetFullPath($TranscriptPath) } catch { return $null }
    if (-not $full.StartsWith($sessionsRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { return $null }
    foreach ($line in @(Get-Content -LiteralPath $full -Encoding UTF8 -TotalCount 200)) {
        if ([string]::IsNullOrWhiteSpace([string]$line)) { continue }
        try { $row = [string]$line | ConvertFrom-Json -ErrorAction Stop } catch { continue }
        if ([string]$row.type -eq "session_meta" -and $null -ne $row.payload) { return $row.payload }
    }
    return $null
}

if ($SelfTest) {
    if (-not (Test-PrivilegedCommand "powershell.exe -File .codex\transport\a1_patch_transport.ps1")) { throw "A1_BRIDGE_GUARD_SELFTEST_DETECT" }
    if (Test-PrivilegedCommand "git status --porcelain") { throw "A1_BRIDGE_GUARD_SELFTEST_FALSE_POSITIVE" }
    $rootMeta = [pscustomobject]@{id="00000000-0000-0000-0000-000000000001";source="cli";cwd="C:\repo";parent_thread_id=$null}
    if (-not (Test-RootMeta $rootMeta "00000000-0000-0000-0000-000000000001" "C:\repo")) { throw "A1_BRIDGE_GUARD_SELFTEST_ROOT" }
    $childMeta = [pscustomobject]@{id="00000000-0000-0000-0000-000000000002";source=[pscustomobject]@{subagent=@{}};cwd="C:\repo"}
    if (Test-RootMeta $childMeta "00000000-0000-0000-0000-000000000002" "C:\repo") { throw "A1_BRIDGE_GUARD_SELFTEST_CHILD" }
    $wire = New-Deny "synthetic"
    if ($wire.hookSpecificOutput.permissionDecision -ne "deny") { throw "A1_BRIDGE_GUARD_SELFTEST_WIRE" }
    Write-Output (@{schema_version="SER-A1-PRIVILEGED-BRIDGE-GUARD-SELFTEST-1";result="PASS";privileged_leaf_count=$PrivilegedLeaves.Count}|ConvertTo-Json -Compress)
    exit 0
}

try {
    $raw = [Console]::In.ReadToEnd()
    $event = $raw | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $event -or [string]$event.tool_name -ne "Bash") { exit 0 }
    $command = [string]$event.tool_input.command
    if (-not (Test-PrivilegedCommand $command)) { exit 0 }
    $meta = Read-SessionMeta ([string]$event.transcript_path)
    if (-not (Test-RootMeta $meta ([string]$event.session_id) ([string]$event.cwd))) {
        [Console]::Out.WriteLine((New-Deny "A1 privileged transports are root-controller-only; subagent or unproven origin denied."|ConvertTo-Json -Depth 6 -Compress))
    }
}
catch {
    [Console]::Out.WriteLine((New-Deny "A1 privileged bridge guard could not prove a root CLI origin."|ConvertTo-Json -Depth 6 -Compress))
}
exit 0
