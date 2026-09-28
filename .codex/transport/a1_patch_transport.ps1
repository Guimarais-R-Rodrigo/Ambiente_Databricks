param([switch]$SelfTest)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "ser/B1-ser03-ser05-authoring"
$ExpectedPaths = @(
    "tools/skill_enforcement/real_campaigns/b1/g6_recovery/README.md",
    "tools/skill_enforcement/real_campaigns/b1/g6_recovery/__init__.py",
    "tools/skill_enforcement/real_campaigns/b1/g6_recovery/adversarial_coverage.json",
    "tools/skill_enforcement/real_campaigns/b1/g6_recovery/manifest.json",
    "tools/skill_enforcement/real_campaigns/b1/g6_recovery/residual_probe_recovery.py",
    "tools/tests/test_ser_b1_g6_recovery.py",
    "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json",
    "docs/sprints/skill_enforcement_rollout/PARALELO/B1/CHANGELOG.md",
    "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl",
    "CHANGELOG.md"
)
$JournalPath = "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl"
$StatePath = "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json"
$ScratchRoot = Join-Path $HOME "codex-scratch\Ambiente_Databricks"
$RequestPath = Join-Path $ScratchRoot "A1_PATCH_REQUEST.json"
$PatchPath = Join-Path $ScratchRoot "A1_PATCH.patch"
$EvidencePath = Join-Path $ScratchRoot "CQ_HOST_PREFLIGHT.json"
$EvidenceSidecarPath = Join-Path $ScratchRoot "CQ_HOST_PREFLIGHT.sha256"
$CheckpointPath = Join-Path $ScratchRoot "A1_OPERATIONAL_CHECKPOINT.json"
$CheckpointSidecarPath = Join-Path $ScratchRoot "A1_OPERATIONAL_CHECKPOINT.sha256"
$MaxRequestAgeSeconds = 900

function Get-Root {
    $rootText = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $rootText) { throw "A1_PATCH_NOT_GIT_REPOSITORY" }
    return [IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
}

function Require-Standalone([string]$Root) {
    $gitDir = (& git rev-parse --path-format=absolute --git-dir 2>$null)
    $common = (& git rev-parse --path-format=absolute --git-common-dir 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $gitDir -or -not $common) { throw "A1_PATCH_GIT_METADATA_UNRESOLVED" }
    $trim=[char[]]@([IO.Path]::DirectorySeparatorChar,[IO.Path]::AltDirectorySeparatorChar)
    $g=[IO.Path]::GetFullPath(($gitDir|Select-Object -First 1).Trim()).TrimEnd($trim)
    $c=[IO.Path]::GetFullPath(($common|Select-Object -First 1).Trim()).TrimEnd($trim)
    $e=[IO.Path]::GetFullPath((Join-Path $Root ".git")).TrimEnd($trim)
    if(-not [string]::Equals($g,$e,[StringComparison]::OrdinalIgnoreCase)-or -not [string]::Equals($c,$e,[StringComparison]::OrdinalIgnoreCase)){
        throw "A1_PATCH_LINKED_WORKTREE_UNSUPPORTED"
    }
}

function Require-RepoIdentity([string]$Root) {
    Set-Location $Root
    $branch=(& git branch --show-current).Trim()
    if($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch){throw "A1_PATCH_BRANCH_MISMATCH:$branch"}
    $status=@(& git status --porcelain)
    if($LASTEXITCODE -ne 0 -or $status.Count -ne 0){throw "A1_PATCH_WORKTREE_NOT_CLEAN"}
    $head=(& git rev-parse HEAD).Trim()
    $tree=(& git rev-parse 'HEAD^{tree}').Trim()
    return [pscustomobject]@{branch=$branch;head=$head;tree=$tree}
}

function Read-SidecarSha([string]$Path) {
    $text=[string](Get-Content -LiteralPath $Path -Raw -Encoding UTF8)
    if([string]::IsNullOrWhiteSpace($text)){throw "A1_PATCH_SIDECAR_EMPTY:$Path"}
    return (($text.Trim() -split "\s+")[0]).ToUpperInvariant()
}

function Load-Evidence {
    if(-not(Test-Path -LiteralPath $EvidencePath)-or -not(Test-Path -LiteralPath $EvidenceSidecarPath)){throw "A1_PATCH_HOST_EVIDENCE_MISSING"}
    $sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $EvidencePath).Hash.ToUpperInvariant()
    if($sha -ne (Read-SidecarSha $EvidenceSidecarPath)){throw "A1_PATCH_HOST_EVIDENCE_SHA_MISMATCH"}
    try{$e=Get-Content -LiteralPath $EvidencePath -Raw -Encoding UTF8|ConvertFrom-Json -ErrorAction Stop}catch{throw "A1_PATCH_HOST_EVIDENCE_INVALID_JSON"}
    if($e.schema_version -ne "AC-R2-CLI-HOST-PREFLIGHT-1" -or $e.result -ne "PASS"){throw "A1_PATCH_HOST_EVIDENCE_INVALID"}
    if([string]$e.git.checkout_mode -ne "STANDALONE"){throw "A1_PATCH_HOST_EVIDENCE_CHECKOUT_MODE"}
    return $e
}

function Require-SourceHash([object]$Evidence,[string]$Key,[string]$RelativePath,[string]$Root) {
    $prop=$Evidence.source_sha256.PSObject.Properties[$Key]
    if($null -eq $prop -or [string]::IsNullOrWhiteSpace([string]$prop.Value)){throw "A1_PATCH_SOURCE_HASH_MISSING:$Key"}
    $actual=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $Root $RelativePath)).Hash.ToUpperInvariant()
    if($actual -ne ([string]$prop.Value).ToUpperInvariant()){throw "A1_PATCH_SOURCE_IDENTITY_DRIFT:$Key"}
}

function Load-Request {
    if(-not(Test-Path -LiteralPath $RequestPath -PathType Leaf)-or -not(Test-Path -LiteralPath $PatchPath -PathType Leaf)){throw "A1_PATCH_REQUEST_OR_PATCH_MISSING"}
    try{$r=Get-Content -LiteralPath $RequestPath -Raw -Encoding UTF8|ConvertFrom-Json -ErrorAction Stop}catch{throw "A1_PATCH_REQUEST_INVALID_JSON"}
    if($r.schema_version -ne "SER-A1-PATCH-REQUEST-1"){throw "A1_PATCH_REQUEST_SCHEMA"}
    if(@("CQ_JOURNAL_ONLY","OPERATIONAL_A1") -notcontains [string]$r.mode){throw "A1_PATCH_REQUEST_MODE"}
    $now=[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $created=[int64]$r.created_at_unix_seconds
    $age=$now-$created
    if($age -lt -60 -or $age -gt $MaxRequestAgeSeconds){throw "A1_PATCH_REQUEST_STALE_OR_FUTURE:$age"}
    $patchSha=(Get-FileHash -Algorithm SHA256 -LiteralPath $PatchPath).Hash.ToUpperInvariant()
    if($patchSha -ne ([string]$r.patch_sha256).ToUpperInvariant()){throw "A1_PATCH_SHA_MISMATCH"}
    $expected=@($r.expected_paths)
    if($expected.Count -lt 1 -or $expected.Count -ne @($expected|Sort-Object -Unique).Count){throw "A1_PATCH_EXPECTED_PATHS_INVALID"}
    foreach($path in $expected){if($ExpectedPaths -notcontains [string]$path){throw "A1_PATCH_EXPECTED_PATH_OUTSIDE_A1:$path"}}
    if([string]$r.mode -eq "CQ_JOURNAL_ONLY"){
        if($expected.Count -ne 1 -or [string]$expected[0] -ne $JournalPath){throw "A1_PATCH_CQ_MUST_BE_JOURNAL_ONLY"}
    }
    return $r
}

function Require-OperationalAuthority([string]$Root,[object]$Request,[object]$Identity) {
    $state=Get-Content -LiteralPath (Join-Path $Root $StatePath) -Raw -Encoding UTF8|ConvertFrom-Json
    if($state.autonomous_controller.runtime_validation -ne "PASS" -or $state.autonomous_controller.effective_config_observation -ne "PASS"){
        throw "A1_PATCH_OPERATIONAL_RUNTIME_NOT_CANONICAL_PASS"
    }
    if(@($state.blocked_by) -contains "AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION" -or @($state.blocked_by) -contains "AUTONOMOUS_CONTROLLER_A1_CAPABILITY_BRIDGE_REQUIRED"){
        throw "A1_PATCH_OPERATIONAL_RUNTIME_BLOCKER_PRESENT"
    }
    if(-not(Test-Path -LiteralPath $CheckpointPath)-or -not(Test-Path -LiteralPath $CheckpointSidecarPath)){throw "A1_PATCH_OPERATIONAL_CHECKPOINT_MISSING"}
    $sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $CheckpointPath).Hash.ToUpperInvariant()
    if($sha -ne (Read-SidecarSha $CheckpointSidecarPath)){throw "A1_PATCH_OPERATIONAL_CHECKPOINT_SHA_MISMATCH"}
    $cp=Get-Content -LiteralPath $CheckpointPath -Raw -Encoding UTF8|ConvertFrom-Json
    if($cp.schema_version -ne "SER-A1-OPERATIONAL-CHECKPOINT-2"){throw "A1_PATCH_OPERATIONAL_CHECKPOINT_SCHEMA"}
    if([string]$cp.last_published_head -ne [string]$Identity.head){throw "A1_PATCH_OPERATIONAL_PENDING_OR_DIVERGENT_HEAD"}
}

function Invoke-CodexSandbox([string]$CodexCli,[string]$Root,[string[]]$Command,[string]$Label) {
    $stdout=Join-Path $ScratchRoot ("A1_PATCH_"+$Label+".stdout.txt")
    $stderr=Join-Path $ScratchRoot ("A1_PATCH_"+$Label+".stderr.txt")
    Remove-Item -LiteralPath $stdout,$stderr -Force -ErrorAction SilentlyContinue
    & $CodexCli sandbox -P ser-b1-a1 -C $Root -- @Command 1> $stdout 2> $stderr
    $code=$LASTEXITCODE
    $out=[string](Get-Content -LiteralPath $stdout -Raw -Encoding UTF8 -ErrorAction SilentlyContinue)
    $err=[string](Get-Content -LiteralPath $stderr -Raw -Encoding UTF8 -ErrorAction SilentlyContinue)
    return [pscustomobject]@{exit_code=$code;stdout=$out;stderr=$err;stdout_path=$stdout;stderr_path=$stderr}
}

function Parse-LastJsonLine([string]$Text) {
    $lines=@(($Text -split "`r?`n")|Where-Object{-not [string]::IsNullOrWhiteSpace($_)})
    for($i=$lines.Count-1;$i-ge 0;$i--){
        try{return ([string]$lines[$i]|ConvertFrom-Json -ErrorAction Stop)}catch{}
    }
    return $null
}

$root=Get-Root
Set-Location $root
Require-Standalone $root
$identity=Require-RepoIdentity $root

if($SelfTest){
    if($ExpectedPaths.Count -ne 10 -or $ExpectedPaths -notcontains $JournalPath){throw "A1_PATCH_SELFTEST_PATH_SET"}
    Write-Output (@{schema_version="SER-A1-PATCH-TRANSPORT-SELFTEST-1";result="PASS";write_root_count=$ExpectedPaths.Count;request_schema="SER-A1-PATCH-REQUEST-1";modes=@("CQ_JOURNAL_ONLY","OPERATIONAL_A1")}|ConvertTo-Json -Depth 5 -Compress)
    exit 0
}
if($args.Count -ne 0){throw "A1_PATCH_EXTRA_ARGUMENTS"}

$rootGate=Join-Path $root ".codex\transport\a1_root_gate.ps1"
if(-not(Test-Path -LiteralPath $rootGate)){throw "A1_PATCH_ROOT_GATE_MISSING"}
. $rootGate
$origin=Assert-A1RootControllerInvocation $root
if($origin.result -ne "PASS"){throw "A1_PATCH_ROOT_GATE_FAIL"}

$evidence=Load-Evidence
foreach($binding in @(
    @("config",".codex\config.toml"),
    @("delta_checker","tools\check_codex_autonomy_delta.py"),
    @("network_probe_script",".codex\probes\cq3_executor_network_probe.ps1"),
    @("a1_filesystem_probe",".codex\probes\cq3_a1_filesystem_probe.ps1"),
    @("a1_patch_transport",".codex\transport\a1_patch_transport.ps1"),
    @("a1_root_gate",".codex\transport\a1_root_gate.ps1")
)){
    Require-SourceHash $evidence $binding[0] $binding[1] $root
}
$python=[string]$evidence.python.executable
$codexCli=[string]$evidence.codex_cli.executable
if([string]::IsNullOrWhiteSpace($python)-or -not(Test-Path -LiteralPath $python)){throw "A1_PATCH_BOUND_PYTHON_MISSING"}
if([string]::IsNullOrWhiteSpace($codexCli)-or -not(Test-Path -LiteralPath $codexCli)){throw "A1_PATCH_BOUND_CODEX_MISSING"}

$request=Load-Request
if([string]$request.candidate_head -ne [string]$identity.head -or [string]$request.candidate_tree -ne [string]$identity.tree){throw "A1_PATCH_REQUEST_CANDIDATE_MISMATCH"}
if([string]$request.mode -eq "CQ_JOURNAL_ONLY"){
    if([string]$evidence.git.head -ne [string]$identity.head -or [string]$evidence.git.tree -ne [string]$identity.tree){throw "A1_PATCH_CQ_NOT_PREFLIGHT_FREEZE"}
    $network=Invoke-CodexSandbox $codexCli $root @("powershell.exe","-NoProfile","-NonInteractive","-ExecutionPolicy","Bypass","-File",".codex\probes\cq3_executor_network_probe.ps1") "CQ_NETWORK"
    $networkPayload=Parse-LastJsonLine $network.stdout
    if($network.exit_code -eq 20 -or ($null -ne $networkPayload -and [string]$networkPayload.result -eq "FAIL_NETWORK_BOUNDARY_OPEN")){throw "SECURITY_STOP_A1_NETWORK_BOUNDARY_OPEN"}
    if($network.exit_code -ne 0 -or $null -eq $networkPayload -or [string]$networkPayload.result -ne "PASS_NETWORK_DENIED"){throw "A1_PATCH_CQ_NETWORK_NOT_PROVEN"}

    $fs=Invoke-CodexSandbox $codexCli $root @("powershell.exe","-NoProfile","-NonInteractive","-ExecutionPolicy","Bypass","-File",".codex\probes\cq3_a1_filesystem_probe.ps1") "CQ_FILESYSTEM"
    $fsPayload=Parse-LastJsonLine $fs.stdout
    if($fs.exit_code -eq 20 -or ($null -ne $fsPayload -and ([string]$fsPayload.result).StartsWith("FAIL"))){throw "SECURITY_STOP_A1_FILESYSTEM_BOUNDARY_OPEN"}
    if($fs.exit_code -ne 0 -or $null -eq $fsPayload -or [string]$fsPayload.result -ne "PASS_WRITE_DENIED"){throw "A1_PATCH_CQ_FILESYSTEM_NOT_PROVEN"}
}else{
    Require-OperationalAuthority $root $request $identity
}

& git apply --check --whitespace=nowarn $PatchPath
if($LASTEXITCODE -ne 0){throw "A1_PATCH_GIT_APPLY_CHECK_FAILED"}
$apply=Invoke-CodexSandbox $codexCli $root @("git","apply","--whitespace=nowarn",$PatchPath) "APPLY"
if($apply.exit_code -ne 0){throw "A1_PATCH_SANDBOXED_APPLY_FAILED"}

& $python -B tools/check_codex_autonomy_delta.py --worktree
if($LASTEXITCODE -ne 0){throw "SECURITY_STOP_A1_PATCH_DELTA_OUTSIDE_ENVELOPE"}
$changed=@()
$changed+=@(& git diff --name-only HEAD)
$changed+=@(& git ls-files --others --exclude-standard)
$changed=@($changed|Where-Object{$_}|ForEach-Object{$_.Trim()}|Sort-Object -Unique)
$expected=@($request.expected_paths|ForEach-Object{[string]$_}|Sort-Object -Unique)
if([string]::Join("`n",$changed) -ne [string]::Join("`n",$expected)){throw "SECURITY_STOP_A1_PATCH_CHANGED_PATH_MISMATCH"}

if([string]$request.mode -eq "CQ_JOURNAL_ONLY"){
    $lines=@(Get-Content -LiteralPath (Join-Path $root $JournalPath) -Encoding UTF8|Where-Object{-not [string]::IsNullOrWhiteSpace($_)})
    if($lines.Count -lt 1){throw "A1_PATCH_CQ_JOURNAL_EMPTY"}
    try{$last=$lines[-1]|ConvertFrom-Json -ErrorAction Stop}catch{throw "A1_PATCH_CQ_JOURNAL_INVALID_LAST_LINE"}
    if($last.event -ne "CQ3_A1_POSITIVE_PROBE" -or $last.authority -ne "CONTROLLER_RUNTIME_QUALIFICATION_ONLY" -or [string]$last.candidate_head -ne [string]$identity.head){
        throw "A1_PATCH_CQ_JOURNAL_CONTRACT"
    }
}

Write-Output (@{
    schema_version="SER-A1-PATCH-TRANSPORT-1"
    result="PASS"
    mode=[string]$request.mode
    base_head=[string]$identity.head
    changed_paths=@($changed)
    a1_profile="ser-b1-a1"
    root_origin="CLI"
}|ConvertTo-Json -Depth 6 -Compress)
