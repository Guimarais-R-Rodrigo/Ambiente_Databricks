param(
    [switch]$SelfTest,
    [switch]$InitializeCheckpoint,
    [switch]$ReconcileOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "ser/B1-ser03-ser05-authoring"
$ExpectedRemotes = @(
    "https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks.git",
    "https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks",
    "git@github.com:Guimarais-R-Rodrigo/Ambiente_Databricks.git",
    "ssh://git@github.com/Guimarais-R-Rodrigo/Ambiente_Databricks.git"
)
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
$EvidencePath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.json"
$EvidenceSidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.sha256"
$CheckpointPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\A1_OPERATIONAL_CHECKPOINT.json"
$CheckpointSidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\A1_OPERATIONAL_CHECKPOINT.sha256"

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false))
}
function Get-Root {
    $rootText = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $rootText) { throw "A1_OPERATIONAL_NOT_GIT_REPO" }
    return [IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
}
function Require-Identity([string]$Root) {
    Set-Location $Root
    $branch = (& git branch --show-current).Trim()
    $origin = (& git remote get-url origin).Trim()
    $pushOrigin = (& git remote get-url --push origin).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) { throw "A1_OPERATIONAL_BRANCH_MISMATCH:$branch" }
    if ($ExpectedRemotes -notcontains $origin -or $ExpectedRemotes -notcontains $pushOrigin) { throw "A1_OPERATIONAL_REMOTE_MISMATCH" }
    return [pscustomobject]@{branch=$branch;origin=$origin;push_origin=$pushOrigin}
}
function Load-Evidence {
    if (-not (Test-Path -LiteralPath $EvidencePath) -or -not (Test-Path -LiteralPath $EvidenceSidecarPath)) { throw "A1_OPERATIONAL_HOST_EVIDENCE_MISSING" }
    $sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $EvidencePath).Hash.ToUpperInvariant()
    $side=(((Get-Content -LiteralPath $EvidenceSidecarPath -Raw).Trim() -split "\s+")[0]).ToUpperInvariant()
    if($sha -ne $side){throw "A1_OPERATIONAL_HOST_EVIDENCE_SHA_MISMATCH"}
    $e=Get-Content -LiteralPath $EvidencePath -Raw | ConvertFrom-Json
    if($e.schema_version -ne "AC-R2-DESKTOP-HOST-PREFLIGHT-6" -or $e.result -ne "PASS"){throw "A1_OPERATIONAL_HOST_EVIDENCE_INVALID"}
    return $e
}
function Write-Checkpoint([string]$QualifiedHead,[string]$Head,[string]$Tree,[int]$Sequence) {
    $payload=[ordered]@{
        schema_version="SER-A1-OPERATIONAL-CHECKPOINT-1"
        branch=$ExpectedBranch
        qualified_control_head=$QualifiedHead
        last_published_head=$Head
        last_published_tree=$Tree
        sequence=$Sequence
        updated_at_unix_seconds=[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    }
    $json=$payload|ConvertTo-Json -Depth 5
    Write-Utf8NoBom $CheckpointPath $json
    $sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $CheckpointPath).Hash
    Write-Utf8NoBom $CheckpointSidecarPath ($sha+"  A1_OPERATIONAL_CHECKPOINT.json"+[Environment]::NewLine)
}
function Load-Checkpoint {
    if(-not(Test-Path -LiteralPath $CheckpointPath)-or -not(Test-Path -LiteralPath $CheckpointSidecarPath)){throw "A1_OPERATIONAL_CHECKPOINT_MISSING"}
    $sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $CheckpointPath).Hash.ToUpperInvariant()
    $side=(((Get-Content -LiteralPath $CheckpointSidecarPath -Raw).Trim() -split "\s+")[0]).ToUpperInvariant()
    if($sha -ne $side){throw "A1_OPERATIONAL_CHECKPOINT_SHA_MISMATCH"}
    $cp=Get-Content -LiteralPath $CheckpointPath -Raw|ConvertFrom-Json
    if($cp.schema_version -ne "SER-A1-OPERATIONAL-CHECKPOINT-1" -or $cp.branch -ne $ExpectedBranch){throw "A1_OPERATIONAL_CHECKPOINT_INVALID"}
    return $cp
}

$root=Get-Root
Set-Location $root
$identity=Require-Identity $root
$evidence=Load-Evidence
$QualifiedPython=[string]$evidence.python.executable
if([string]::IsNullOrWhiteSpace($QualifiedPython)-or -not(Test-Path -LiteralPath $QualifiedPython)){throw "A1_OPERATIONAL_BOUND_PYTHON_MISSING"}
$deltaPath=Join-Path $root "tools\check_codex_autonomy_delta.py"
$deltaHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $deltaPath).Hash.ToUpperInvariant()
if($deltaHash -ne ([string]$evidence.source_sha256.delta_checker).ToUpperInvariant()){throw "A1_OPERATIONAL_DELTA_CHECKER_SHA_MISMATCH"}

if($SelfTest){
    Write-Output (@{schema_version="SER-A1-OPERATIONAL-TRANSPORT-SELFTEST-1";result="PASS";branch=$identity.branch;read_remote=$identity.origin;push_remote=$identity.push_origin}|ConvertTo-Json -Compress)
    exit 0
}

$localHead=(& git rev-parse HEAD).Trim()
$localTree=(& git rev-parse 'HEAD^{tree}').Trim()
& git fetch origin $ExpectedBranch
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_FETCH_FAIL"}
$remoteHead=(& git rev-parse "origin/$ExpectedBranch").Trim()

if($InitializeCheckpoint){
    if($localHead -ne [string]$evidence.git.head -or $remoteHead -ne $localHead){throw "A1_OPERATIONAL_INITIAL_CHECKPOINT_IDENTITY_MISMATCH"}
    if(@(& git status --porcelain).Count -ne 0){throw "A1_OPERATIONAL_INITIAL_CHECKPOINT_DIRTY"}
    Write-Checkpoint ([string]$evidence.git.head) $localHead $localTree 0
    Write-Output "A1_OPERATIONAL_CHECKPOINT=INITIALIZED"
    Write-Output "HEAD=$localHead"
    exit 0
}

$cp=Load-Checkpoint
if([string]$cp.qualified_control_head -ne [string]$evidence.git.head){throw "A1_OPERATIONAL_QUALIFIED_CONTROL_HEAD_MISMATCH"}
$checkpointHead=[string]$cp.last_published_head
$checkpointTree=[string]$cp.last_published_tree
$sequence=[int]$cp.sequence

# Idempotent reconciliation before any new mutation.
if($localHead -eq $checkpointHead -and $remoteHead -eq $checkpointHead){
    if($ReconcileOnly){
        Write-Output "A1_OPERATIONAL_RECONCILE=NO_PENDING_EFFECT"
        exit 0
    }
} elseif($localHead -eq $remoteHead -and $localHead -ne $checkpointHead) {
    & $QualifiedPython -B tools/check_codex_autonomy_delta.py --base $checkpointHead --head $localHead
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_RECONCILE_REMOTE_DELTA_INVALID"}
    Write-Checkpoint ([string]$cp.qualified_control_head) $localHead $localTree ($sequence+1)
    Write-Output "A1_OPERATIONAL_RECONCILE=PUBLISHED_SUCCESSOR"
    Write-Output "HEAD=$localHead"
    exit 0
} elseif($remoteHead -eq $checkpointHead -and $localHead -ne $checkpointHead) {
    & $QualifiedPython -B tools/check_codex_autonomy_delta.py --base $checkpointHead --head $localHead
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_RECONCILE_LOCAL_DELTA_INVALID"}
    $parent=(& git rev-parse "$localHead^").Trim()
    if($parent -ne $checkpointHead){throw "A1_OPERATIONAL_RECONCILE_LOCAL_NOT_SINGLE_SUCCESSOR"}
    if(@(& git status --porcelain).Count -ne 0){throw "A1_OPERATIONAL_RECONCILE_LOCAL_SUCCESSOR_DIRTY"}
    & git -c core.hooksPath=.codex/transport/no-hooks push origin "HEAD:refs/heads/$ExpectedBranch"
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_RESUME_PUSH_FAILED"}
    $readback=(& git ls-remote origin "refs/heads/$ExpectedBranch").Trim()
    if($LASTEXITCODE -ne 0 -or (($readback -split "\s+")[0]) -ne $localHead){throw "A1_OPERATIONAL_RESUME_READBACK_UNKNOWN"}
    Write-Checkpoint ([string]$cp.qualified_control_head) $localHead $localTree ($sequence+1)
    Write-Output "A1_OPERATIONAL_RECONCILE=RESUMED_PUSH"
    Write-Output "HEAD=$localHead"
    exit 0
} else {
    throw "A1_OPERATIONAL_UNKNOWN_DIVERGENCE"
}

if($ReconcileOnly){
    Write-Output "A1_OPERATIONAL_RECONCILE=NO_PENDING_EFFECT"
    exit 0
}

& $QualifiedPython -B tools/check_codex_autonomy_delta.py --worktree
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_WORKTREE_SCOPE_FAIL"}

$changed=@()
$changed+=@(& git diff --name-only HEAD)
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_CHANGED_PATHS_FAIL"}
$changed+=@(& git diff --cached --name-only HEAD)
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_CHANGED_PATHS_FAIL"}
$changed+=@(& git ls-files --others --exclude-standard)
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_CHANGED_PATHS_FAIL"}
$changed=@($changed|Where-Object{$_}|ForEach-Object{$_.Trim()}|Sort-Object -Unique)
if($changed.Count -eq 0){
    Write-Output "A1_OPERATIONAL_NO_DELTA"
    exit 0
}

& git add -A -- @ExpectedPaths
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_STAGE_FAIL"}
& $QualifiedPython -B tools/check_codex_autonomy_delta.py --index
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_INDEX_SCOPE_FAIL"}

& git diff --cached --quiet
if($LASTEXITCODE -eq 0){Write-Output "A1_OPERATIONAL_NO_DELTA";exit 0}
if($LASTEXITCODE -ne 1){throw "A1_OPERATIONAL_INDEX_DIFF_ERROR"}

& git -c core.hooksPath=.codex/transport/no-hooks -c commit.gpgSign=false commit --no-gpg-sign --no-verify -m "SER B1 A1: autonomous causal update"
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_COMMIT_FAIL"}
$newHead=(& git rev-parse HEAD).Trim()
$newTree=(& git rev-parse 'HEAD^{tree}').Trim()
& $QualifiedPython -B tools/check_codex_autonomy_delta.py --base $checkpointHead --head $newHead
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_COMMITTED_DELTA_INVALID"}
if(@(& git status --porcelain).Count -ne 0){throw "A1_OPERATIONAL_POST_COMMIT_DIRTY"}

# Recheck remote immediately before push.
& git fetch origin $ExpectedBranch
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_PREFLIGHT_PUSH_FETCH_FAIL"}
$remoteBeforePush=(& git rev-parse "origin/$ExpectedBranch").Trim()
if($remoteBeforePush -ne $checkpointHead){throw "A1_OPERATIONAL_REMOTE_ADVANCED_BEFORE_PUSH"}

& git -c core.hooksPath=.codex/transport/no-hooks push origin "HEAD:refs/heads/$ExpectedBranch"
if($LASTEXITCODE -ne 0){
    Write-Error "A1_OPERATIONAL_PUSH_FAILED_LOCAL_COMMIT_PRESERVED"
    exit 78
}
$readback=(& git ls-remote origin "refs/heads/$ExpectedBranch").Trim()
if($LASTEXITCODE -ne 0 -or (($readback -split "\s+")[0]) -ne $newHead){
    Write-Error "A1_OPERATIONAL_PUSH_READBACK_UNKNOWN_LOCAL_COMMIT_PRESERVED"
    exit 90
}
Write-Checkpoint ([string]$cp.qualified_control_head) $newHead $newTree ($sequence+1)
Write-Output "A1_OPERATIONAL_TRANSPORT=PASS"
Write-Output "BASE=$checkpointHead"
Write-Output "HEAD=$newHead"
Write-Output "TREE=$newTree"
Write-Output ("SEQUENCE="+($sequence+1))
