param([switch]$SelfTest)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Normalize([string]$Path) {
    if ($null -eq $Path) { return "" }
    $n = ($Path -replace "\\","/")
    while ($n.StartsWith("./")) { $n = $n.Substring(2) }
    return $n
}
function MatchesAny([string]$Path,$Patterns) {
    $n=Normalize $Path
    foreach($pat in $Patterns){ if($n -like $pat){return $true} }
    return $false
}
function Classify([string]$Path,$Scope) {
    if(MatchesAny $Path $Scope.protected_roots){return "PROTECTED"}
    if(MatchesAny $Path $Scope.shared_roots_requiring_human_gate){return "HUMAN_GATE_REQUIRED"}
    if(MatchesAny $Path $Scope.write_roots){return "ALLOWED_A1"}
    return "OUTSIDE_A1"
}
function Ignored([string]$Path) {
    $n=Normalize $Path
    return ($n -match '(^|/)(__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache)(/|$)' -or $n -match '\.(pyc|pyo)$')
}
function Block([string]$Reason) { [Console]::Out.WriteLine((@{decision="block";reason=$Reason}|ConvertTo-Json -Compress)) }
function Git-Lines([string[]]$GitArguments,[string]$Failure) {
    $lines=@(& git @GitArguments 2>$null)
    if($LASTEXITCODE -ne 0){ Block $Failure; exit 0 }
    return $lines
}

try {
$rootText=(& git rev-parse --show-toplevel 2>$null)
if($LASTEXITCODE -ne 0 -or -not $rootText){ Block "A1 post-scope guard cannot resolve repository root"; exit 0 }
$root=[IO.Path]::GetFullPath(($rootText|Select-Object -First 1).Trim())
$scope=(Get-Content -Encoding UTF8 -Raw (Join-Path $root "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json")|ConvertFrom-Json).repo_scope

if($SelfTest){
    $journal="docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl"
    if((Classify $journal $scope)-ne "ALLOWED_A1"){throw "POST_SCOPE_GUARD_ALLOWED"}
    if((Classify "../CHANGELOG.md" $scope)-eq "ALLOWED_A1"){throw "POST_SCOPE_GUARD_TRAVERSAL"}
    Write-Output (@{schema_version="SER-CODEX-POST-SCOPE-GUARD-SELFTEST-1";result="PASS"}|ConvertTo-Json -Compress)
    exit 0
}
$null=[Console]::In.ReadToEnd()
Set-Location $root
$paths=New-Object System.Collections.Generic.HashSet[string]
foreach($line in (Git-Lines @("diff","--name-only","HEAD") "A1 post-scope guard git diff failed")){ if($line){$null=$paths.Add($line.Trim())} }
foreach($line in (Git-Lines @("diff","--cached","--name-only","HEAD") "A1 post-scope guard git cached diff failed")){ if($line){$null=$paths.Add($line.Trim())} }
foreach($line in (Git-Lines @("ls-files","--others","--exclude-standard") "A1 post-scope guard git untracked inspection failed")){ if($line){$null=$paths.Add($line.Trim())} }
$violations=@()
$qualificationRootProbeOnly = ($paths.Count -eq 1 -and (Normalize ([string]($paths | Select-Object -First 1))) -eq ".cq3_root_negative_probe.txt")
foreach($p in $paths){
    if(Ignored $p){continue}
    $c=Classify $p $scope
    if($c -ne "ALLOWED_A1"){$violations += "$p=$c"}
}
if($violations.Count -gt 0 -and -not $qualificationRootProbeOnly){ Block ("A1 worktree scope violation after tool use: " + ($violations -join ", ")); exit 0 }
exit 0
}
catch {
    if ($SelfTest) { throw }
    Block "A1 post-scope guard git inspection failed or envelope is unreadable"
    exit 0
}
