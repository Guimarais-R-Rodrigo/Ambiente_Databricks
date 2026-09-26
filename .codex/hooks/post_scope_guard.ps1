$ErrorActionPreference = "Stop"
$null = [Console]::In.ReadToEnd()
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
function Ignored([string]$p) {
  $n = Normalize $p
  return ($n -match '(^|/)(__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache)(/|$)' -or $n -match '\.(pyc|pyo)$')
}

$paths = New-Object System.Collections.Generic.HashSet[string]
foreach ($line in (& git -C $root diff --name-only HEAD)) { if ($line) { $null = $paths.Add($line.Trim()) } }
foreach ($line in (& git -C $root diff --cached --name-only HEAD)) { if ($line) { $null = $paths.Add($line.Trim()) } }
foreach ($line in (& git -C $root ls-files --others --exclude-standard)) { if ($line) { $null = $paths.Add($line.Trim()) } }

$violations = @()
foreach ($p in $paths) {
  if (Ignored $p) { continue }
  $c = Classify $p
  if ($c -ne "ALLOWED_A1") { $violations += "$p=$c" }
}
if ($violations.Count -gt 0) {
  @{ decision = "block"; reason = "A1 worktree scope violation after tool use: " + ($violations -join ", ") } |
    ConvertTo-Json -Depth 4 -Compress | Write-Output
}
