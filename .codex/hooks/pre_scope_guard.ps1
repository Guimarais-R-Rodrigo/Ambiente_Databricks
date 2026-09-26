$ErrorActionPreference = "Stop"
$raw = [Console]::In.ReadToEnd()
$event = $raw | ConvertFrom-Json
$command = [string]$event.tool_input.command
if ([string]::IsNullOrWhiteSpace($command)) { exit 0 }
$root = (& git rev-parse --show-toplevel).Trim()
$scope = (Get-Content -Raw (Join-Path $root "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json") | ConvertFrom-Json).repo_scope

function Normalize([string]$p) { return ($p -replace "\\","/").TrimStart("./") }
function MatchesAny([string]$p, $patterns) {
  $n = Normalize $p
  foreach ($pat in $patterns) { if ($n -like $pat) { return $true } }
  return $false
}
function Classify([string]$p) {
  if (MatchesAny $p $scope.protected_roots) { return "PROTECTED" }
  if (MatchesAny $p $scope.shared_roots_requiring_human_gate) { return "HUMAN_GATE_REQUIRED" }
  if (MatchesAny $p $scope.write_roots) { return "ALLOWED_A1" }
  return "OUTSIDE_A1"
}

$paths = New-Object System.Collections.Generic.List[string]
$regexes = @(
  '(?m)^\*\*\*\s+(?:Add|Update|Delete) File:\s*(.+?)\s*$',
  '(?m)^\*\*\*\s+Move to:\s*(.+?)\s*$'
)
foreach ($rx in $regexes) {
  foreach ($m in [regex]::Matches($command, $rx)) { $paths.Add($m.Groups[1].Value.Trim()) }
}
$violations = @()
foreach ($p in $paths) {
  $c = Classify $p
  if ($c -ne "ALLOWED_A1") { $violations += "$p=$c" }
}
if ($violations.Count -gt 0) {
  $out = @{
    hookSpecificOutput = @{
      hookEventName = "PreToolUse"
      permissionDecision = "deny"
      permissionDecisionReason = "A1 scope violation: " + ($violations -join ", ")
    }
  } | ConvertTo-Json -Depth 5 -Compress
  [Console]::Out.WriteLine($out)
}
