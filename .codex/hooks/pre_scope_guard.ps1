param([switch]$SelfTest)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Normalize([string]$Path) {
    if ($null -eq $Path) { return "" }
    $n = ($Path -replace "\\","/")
    while ($n.StartsWith("./")) { $n = $n.Substring(2) }
    return $n
}
function MatchesAny([string]$Path, $Patterns) {
    $n = Normalize $Path
    foreach ($pat in $Patterns) { if ($n -like $pat) { return $true } }
    return $false
}
function Classify([string]$Path, $Scope) {
    if (MatchesAny $Path $Scope.protected_roots) { return "PROTECTED" }
    if (MatchesAny $Path $Scope.shared_roots_requiring_human_gate) { return "HUMAN_GATE_REQUIRED" }
    if (MatchesAny $Path $Scope.write_roots) { return "ALLOWED_A1" }
    return "OUTSIDE_A1"
}
function Deny([string]$Reason) {
    [Console]::Out.WriteLine((@{
        hookSpecificOutput=@{
            hookEventName="PreToolUse"
            permissionDecision="deny"
            permissionDecisionReason=$Reason
        }
    } | ConvertTo-Json -Depth 5 -Compress))
}
function Get-Root {
    $rootText = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $rootText) { throw "PRE_SCOPE_GUARD_NOT_GIT_REPO" }
    return [IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
}

try {
$root = Get-Root
$scope = (Get-Content -Encoding UTF8 -Raw (Join-Path $root "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json") | ConvertFrom-Json).repo_scope

if ($SelfTest) {
    $journal = "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl"
    if ((Normalize ("./" + $journal)) -ne $journal) { throw "PRE_SCOPE_GUARD_NORMALIZE" }
    if ((Classify $journal $scope) -ne "ALLOWED_A1") { throw "PRE_SCOPE_GUARD_ALLOWED" }
    if ((Classify ".codex/config.toml" $scope) -eq "ALLOWED_A1") { throw "PRE_SCOPE_GUARD_PROTECTED" }
    if ((Classify ("../" + $journal) $scope) -eq "ALLOWED_A1") { throw "PRE_SCOPE_GUARD_TRAVERSAL" }
    Write-Output (@{ schema_version="SER-CODEX-PRE-SCOPE-GUARD-SELFTEST-1"; result="PASS" } | ConvertTo-Json -Compress)
    exit 0
}

$raw = [Console]::In.ReadToEnd()
try { $event = $raw | ConvertFrom-Json -ErrorAction Stop }
catch { Deny "A1 scope guard cannot parse hook input"; exit 0 }

if ($null -eq $event -or $event -isnot [System.Management.Automation.PSCustomObject]) { throw "PRE_SCOPE_INPUT_OBJECT_REQUIRED" }
$inputProperty = $event.PSObject.Properties["tool_input"]
if ($null -eq $inputProperty -or $inputProperty.Value -isnot [System.Management.Automation.PSCustomObject]) { throw "PRE_SCOPE_TOOL_INPUT_REQUIRED" }
$inputObject = $inputProperty.Value
$paths = New-Object System.Collections.Generic.List[string]
foreach ($key in @("path","file_path","target_path","target_file")) {
    if ($null -ne $inputObject -and $null -ne $inputObject.PSObject.Properties[$key]) {
        $value = [string]$inputObject.$key
        if (-not [string]::IsNullOrWhiteSpace($value)) { $paths.Add($value.Trim()) }
    }
}
$command = if ($null -ne $inputObject -and $null -ne $inputObject.PSObject.Properties["command"]) { [string]$inputObject.command } else { "" }
foreach ($rx in @(
    '(?m)^\*\*\*\s+(?:Add|Update|Delete) File:\s*(.+?)\s*$',
    '(?m)^\*\*\*\s+Move to:\s*(.+?)\s*$'
)) {
    foreach ($m in [regex]::Matches($command,$rx)) { $paths.Add($m.Groups[1].Value.Trim()) }
}
if ($paths.Count -eq 0) {
    Deny ("A1 scope guard could not resolve target path for tool " + [string]$event.tool_name)
    exit 0
}
$violations=@()
foreach ($p in $paths) {
    $c=Classify $p $scope
    if ($c -ne "ALLOWED_A1") { $violations += "$p=$c" }
}
if ($violations.Count -gt 0) { Deny ("A1 scope violation: " + ($violations -join ", ")); exit 0 }
exit 0
}
catch {
    if ($SelfTest) { throw }
    Deny "A1 scope guard could not resolve repository, envelope or hook input"
    exit 0
}
