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
$BridgePaths = @(
    "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl",
    "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json",
    "docs/sprints/skill_enforcement_rollout/PARALELO/B1/CHANGELOG.md",
    "CHANGELOG.md"
)
$StatePath = "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json"
$RuntimeBlocker = "AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION"
$EvidencePath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.json"
$EvidenceSidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.sha256"
$CheckpointPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\A1_OPERATIONAL_CHECKPOINT.json"
$CheckpointSidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\A1_OPERATIONAL_CHECKPOINT.sha256"

$ControlSourcePaths = [ordered]@{
    config = ".codex\config.toml"
    envelope = "docs\operations\autonomy\B1_AUTONOMY_ENVELOPE.json"
    envelope_schema = "docs\operations\autonomy\autonomy-envelope.schema.json"
    agents_md = "AGENTS.md"
    controller_skill = ".agents\skills\ser-autonomous-controller\SKILL.md"
    validator = "tools\validate_codex_autonomy.py"
    metatests = "tools\tests\test_codex_autonomy.py"
    delta_checker = "tools\check_codex_autonomy_delta.py"
    network_probe_script = ".codex\probes\cq3_executor_network_probe.ps1"
    transport = ".codex\transport\a1_git_transport.ps1"
    operational_transport = ".codex\transport\a1_operational_git_transport.ps1"
    operational_policy = "docs\operations\autonomy\A1_OPERATIONAL_POLICY.json"
    rules = ".codex\rules\a1_git_transport.rules"
    executor_agent = ".codex\agents\executor.toml"
    explorer_agent = ".codex\agents\explorer.toml"
    domain_auditor_agent = ".codex\agents\domain-auditor.toml"
    evidence_auditor_agent = ".codex\agents\evidence-auditor.toml"
    architecture_auditor_agent = ".codex\agents\architecture-auditor.toml"
    hooks = ".codex\config.toml"
    pre_scope_guard = ".codex\hooks\pre_scope_guard.ps1"
    pre_scope_guard_python = ".codex\hooks\pre_scope_guard.py"
    post_scope_guard = ".codex\hooks\post_scope_guard.ps1"
    post_scope_guard_python = ".codex\hooks\post_scope_guard.py"
    external_surface_guard = ".codex\hooks\external_surface_guard.ps1"
    external_surface_guard_python = ".codex\hooks\external_surface_guard.py"
    tool_surface_policy = "docs\operations\autonomy\CODEX_DESKTOP_TOOL_SURFACE_POLICY.json"
    prompt_template = "docs\operations\CODEX_DESKTOP_CQ_RUN_PROMPT_TEMPLATE.md"
    protocol = "docs\operations\CODEX_AUTONOMOUS_PROTOCOL.md"
    runtime_contract = "docs\operations\CODEX_RUNTIME_QUALIFICATION.md"
    desktop_contract = "docs\operations\CODEX_DESKTOP_WINDOWS_CQ.md"
    start_prompt = "docs\operations\CODEX_AUTONOMOUS_START_PROMPT.md"
}

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
    if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) { throw "A1_OPERATIONAL_BRANCH_MISMATCH:$branch" }
    $origin = (& git remote get-url origin).Trim()
    if ($LASTEXITCODE -ne 0) { throw "A1_OPERATIONAL_REMOTE_READ_FAILED" }
    $pushOrigin = (& git remote get-url --push origin).Trim()
    if ($LASTEXITCODE -ne 0 -or $ExpectedRemotes -notcontains $origin -or $ExpectedRemotes -notcontains $pushOrigin) { throw "A1_OPERATIONAL_REMOTE_MISMATCH" }
    return [pscustomobject]@{branch=$branch;origin=$origin;push_origin=$pushOrigin}
}
function Require-Envelope([string]$Root) {
    $envelopePath = Join-Path $Root "docs\operations\autonomy\B1_AUTONOMY_ENVELOPE.json"
    $envelope = Get-Content -Raw -Encoding UTF8 $envelopePath | ConvertFrom-Json
    $declared = @($envelope.repo_scope.write_roots | Sort-Object)
    $expected = @($ExpectedPaths | Sort-Object)
    if ([string]::Join([Environment]::NewLine,$declared) -ne [string]::Join([Environment]::NewLine,$expected)) { throw "A1_OPERATIONAL_ENVELOPE_PATH_MISMATCH" }
}
function Load-Evidence {
    if (-not (Test-Path -LiteralPath $EvidencePath) -or -not (Test-Path -LiteralPath $EvidenceSidecarPath)) { throw "A1_OPERATIONAL_HOST_EVIDENCE_MISSING" }
    $sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $EvidencePath).Hash.ToUpperInvariant()
    $side=(((Get-Content -LiteralPath $EvidenceSidecarPath -Raw).Trim() -split "\s+")[0]).ToUpperInvariant()
    if($sha -ne $side){throw "A1_OPERATIONAL_HOST_EVIDENCE_SHA_MISMATCH"}
    try { $e=Get-Content -LiteralPath $EvidencePath -Raw|ConvertFrom-Json -ErrorAction Stop } catch { throw "A1_OPERATIONAL_HOST_EVIDENCE_INVALID_JSON" }
    if($e.schema_version -ne "AC-R2-DESKTOP-HOST-PREFLIGHT-6" -or $e.result -ne "PASS"){throw "A1_OPERATIONAL_HOST_EVIDENCE_INVALID"}
    return $e
}
function Require-ControlIdentity($Evidence,[string]$Root) {
    foreach($key in $ControlSourcePaths.Keys){
        $expectedProperty = $Evidence.source_sha256.PSObject.Properties[$key]
        if($null -eq $expectedProperty -or [string]::IsNullOrWhiteSpace([string]$expectedProperty.Value)){throw "A1_OPERATIONAL_CONTROL_HASH_MISSING:$key"}
        $path=Join-Path $Root $ControlSourcePaths[$key]
        if(-not(Test-Path -LiteralPath $path)){throw "A1_OPERATIONAL_CONTROL_SOURCE_MISSING:$key"}
        $actual=(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToUpperInvariant()
        if($actual -ne ([string]$expectedProperty.Value).ToUpperInvariant()){throw "A1_OPERATIONAL_CONTROL_IDENTITY_DRIFT:$key"}
    }
}
function Require-CanonicalRuntimePass([string]$Root) {
    $state=Get-Content -LiteralPath (Join-Path $Root $StatePath) -Raw|ConvertFrom-Json
    if($state.autonomous_controller.runtime_validation -ne "PASS"){throw "A1_OPERATIONAL_RUNTIME_NOT_CANONICAL_PASS"}
    if($state.autonomous_controller.effective_config_observation -ne "PASS"){throw "A1_OPERATIONAL_EFFECTIVE_CONFIG_NOT_CANONICAL_PASS"}
    if(@($state.blocked_by) -contains $RuntimeBlocker){throw "A1_OPERATIONAL_RUNTIME_BLOCKER_STILL_PRESENT"}
}
function Require-Ancestor([string]$Ancestor,[string]$Descendant,[string]$Code) {
    & git merge-base --is-ancestor $Ancestor $Descendant
    if($LASTEXITCODE -ne 0){throw $Code}
}
function Get-BridgePaths([string]$Base,[string]$Head) {
    $paths=@(& git diff --name-only $Base $Head)
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_BOOTSTRAP_DIFF_FAILED"}
    return @($paths|Where-Object{$_}|ForEach-Object{$_.Trim()}|Sort-Object -Unique)
}
function Get-ReconcileDecision([string]$Checkpoint,[string]$Local,[string]$Remote,[string]$LocalParent) {
    if($Local -eq $Checkpoint -and $Remote -eq $Checkpoint){return "NO_PENDING"}
    if($Local -eq $Remote -and $Local -ne $Checkpoint -and $LocalParent -eq $Checkpoint){return "PUBLISHED_SUCCESSOR"}
    if($Remote -eq $Checkpoint -and $Local -ne $Checkpoint -and $LocalParent -eq $Checkpoint){return "LOCAL_SUCCESSOR_PENDING_PUSH"}
    return "UNKNOWN_DIVERGENCE"
}
function Write-Checkpoint([string]$QualifiedHead,[string]$OperationalBase,[string]$Head,[string]$Tree,[int]$Sequence) {
    $payload=[ordered]@{
        schema_version="SER-A1-OPERATIONAL-CHECKPOINT-2"
        branch=$ExpectedBranch
        qualified_control_head=$QualifiedHead
        operational_base_head=$OperationalBase
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
    try { $cp=Get-Content -LiteralPath $CheckpointPath -Raw|ConvertFrom-Json -ErrorAction Stop } catch { throw "A1_OPERATIONAL_CHECKPOINT_INVALID_JSON" }
    if($cp.schema_version -ne "SER-A1-OPERATIONAL-CHECKPOINT-2" -or $cp.branch -ne $ExpectedBranch){throw "A1_OPERATIONAL_CHECKPOINT_INVALID"}
    return $cp
}

$root=Get-Root
Set-Location $root
$identity=Require-Identity $root
Require-Envelope $root

if($args.Count -ne 0){throw "A1_OPERATIONAL_EXTRA_ARGUMENTS"}
$switchCount=@($SelfTest,$InitializeCheckpoint,$ReconcileOnly|Where-Object{$_}).Count
if($switchCount -gt 1){throw "A1_OPERATIONAL_MUTUALLY_EXCLUSIVE_SWITCHES"}

if($SelfTest){
    $cases=[ordered]@{
        no_pending=(Get-ReconcileDecision "A" "A" "A" "P")
        published=(Get-ReconcileDecision "A" "B" "B" "A")
        pending=(Get-ReconcileDecision "A" "B" "A" "A")
        divergent=(Get-ReconcileDecision "A" "C" "B" "A")
    }
    if($cases.no_pending -ne "NO_PENDING" -or $cases.published -ne "PUBLISHED_SUCCESSOR" -or $cases.pending -ne "LOCAL_SUCCESSOR_PENDING_PUSH" -or $cases.divergent -ne "UNKNOWN_DIVERGENCE"){throw "A1_OPERATIONAL_SELFTEST_RECONCILIATION_MATRIX"}
    Write-Output (@{schema_version="SER-A1-OPERATIONAL-TRANSPORT-SELFTEST-2";result="PASS";cases=$cases}|ConvertTo-Json -Depth 5 -Compress)
    exit 0
}

$evidence=Load-Evidence
Require-ControlIdentity $evidence $root
$QualifiedPython=[string]$evidence.python.executable
if([string]::IsNullOrWhiteSpace($QualifiedPython)-or -not(Test-Path -LiteralPath $QualifiedPython)){throw "A1_OPERATIONAL_BOUND_PYTHON_MISSING"}

$localHead=(& git rev-parse HEAD).Trim()
$localTree=(& git rev-parse 'HEAD^{tree}').Trim()
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_LOCAL_IDENTITY_FAIL"}
& git fetch origin $ExpectedBranch
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_FETCH_FAIL"}
$remoteHead=(& git rev-parse "origin/$ExpectedBranch").Trim()
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_REMOTE_HEAD_FAIL"}

if($InitializeCheckpoint){
    Require-CanonicalRuntimePass $root
    if($localHead -ne $remoteHead){throw "A1_OPERATIONAL_INITIAL_CHECKPOINT_LOCAL_REMOTE_MISMATCH"}
    if(@(& git status --porcelain).Count -ne 0){throw "A1_OPERATIONAL_INITIAL_CHECKPOINT_DIRTY"}
    $qualifiedHead=[string]$evidence.git.head
    Require-Ancestor $qualifiedHead $localHead "A1_OPERATIONAL_QUALIFIED_HEAD_NOT_ANCESTOR"
    $bridge=Get-BridgePaths $qualifiedHead $localHead
    foreach($path in $bridge){if($BridgePaths -notcontains $path){throw "A1_OPERATIONAL_BOOTSTRAP_UNEXPECTED_PATH:$path"}}
    Write-Checkpoint $qualifiedHead $localHead $localHead $localTree 0
    Write-Output "A1_OPERATIONAL_CHECKPOINT=INITIALIZED"
    Write-Output "QUALIFIED_CONTROL_HEAD=$qualifiedHead"
    Write-Output "OPERATIONAL_BASE_HEAD=$localHead"
    exit 0
}

Require-CanonicalRuntimePass $root
$cp=Load-Checkpoint
if([string]$cp.qualified_control_head -ne [string]$evidence.git.head){throw "A1_OPERATIONAL_QUALIFIED_CONTROL_HEAD_MISMATCH"}
Require-Ancestor ([string]$cp.qualified_control_head) ([string]$cp.operational_base_head) "A1_OPERATIONAL_CHECKPOINT_BASE_NOT_DESCENDANT"
Require-Ancestor ([string]$cp.operational_base_head) ([string]$cp.last_published_head) "A1_OPERATIONAL_CHECKPOINT_HEAD_NOT_DESCENDANT"

$checkpointHead=[string]$cp.last_published_head
$checkpointTree=[string]$cp.last_published_tree
$operationalBase=[string]$cp.operational_base_head
$sequence=[int]$cp.sequence
$localParent=""
if($localHead -ne $checkpointHead){
    $localParent=(& git rev-parse "$localHead^" 2>$null).Trim()
    if($LASTEXITCODE -ne 0){$localParent=""}
}
$decision=Get-ReconcileDecision $checkpointHead $localHead $remoteHead $localParent

if($decision -eq "PUBLISHED_SUCCESSOR"){
    & $QualifiedPython -B tools/check_codex_autonomy_delta.py --base $checkpointHead --head $localHead
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_RECONCILE_REMOTE_DELTA_INVALID"}
    Write-Checkpoint ([string]$cp.qualified_control_head) $operationalBase $localHead $localTree ($sequence+1)
    Write-Output "A1_OPERATIONAL_RECONCILE=PUBLISHED_SUCCESSOR"
    Write-Output "HEAD=$localHead"
    exit 0
}
if($decision -eq "LOCAL_SUCCESSOR_PENDING_PUSH"){
    & $QualifiedPython -B tools/check_codex_autonomy_delta.py --base $checkpointHead --head $localHead
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_RECONCILE_LOCAL_DELTA_INVALID"}
    if(@(& git status --porcelain).Count -ne 0){throw "A1_OPERATIONAL_RECONCILE_LOCAL_SUCCESSOR_DIRTY"}
    & git -c core.hooksPath=.codex/transport/no-hooks push origin "HEAD:refs/heads/$ExpectedBranch"
    if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_RESUME_PUSH_FAILED"}
    $readback=(& git ls-remote origin "refs/heads/$ExpectedBranch").Trim()
    if($LASTEXITCODE -ne 0 -or (($readback -split "\s+")[0]) -ne $localHead){throw "A1_OPERATIONAL_RESUME_READBACK_UNKNOWN"}
    Write-Checkpoint ([string]$cp.qualified_control_head) $operationalBase $localHead $localTree ($sequence+1)
    Write-Output "A1_OPERATIONAL_RECONCILE=RESUMED_PUSH"
    Write-Output "HEAD=$localHead"
    exit 0
}
if($decision -eq "UNKNOWN_DIVERGENCE"){throw "A1_OPERATIONAL_UNKNOWN_DIVERGENCE"}
if($ReconcileOnly){
    Write-Output "A1_OPERATIONAL_RECONCILE=NO_PENDING_EFFECT"
    exit 0
}

& $QualifiedPython -B tools/check_codex_autonomy_delta.py --worktree
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_WORKTREE_SCOPE_FAIL"}
$changed=@()
$changed+=@(& git diff --name-only HEAD); if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_CHANGED_PATHS_FAIL"}
$changed+=@(& git diff --cached --name-only HEAD); if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_CHANGED_PATHS_FAIL"}
$changed+=@(& git ls-files --others --exclude-standard); if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_CHANGED_PATHS_FAIL"}
$changed=@($changed|Where-Object{$_}|ForEach-Object{$_.Trim()}|Sort-Object -Unique)
if($changed.Count -eq 0){Write-Output "A1_OPERATIONAL_NO_DELTA";exit 0}

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

& git fetch origin $ExpectedBranch
if($LASTEXITCODE -ne 0){throw "A1_OPERATIONAL_PREFLIGHT_PUSH_FETCH_FAIL"}
$remoteBeforePush=(& git rev-parse "origin/$ExpectedBranch").Trim()
if($remoteBeforePush -ne $checkpointHead){throw "A1_OPERATIONAL_REMOTE_ADVANCED_BEFORE_PUSH"}

& git -c core.hooksPath=.codex/transport/no-hooks push origin "HEAD:refs/heads/$ExpectedBranch"
if($LASTEXITCODE -ne 0){Write-Error "A1_OPERATIONAL_PUSH_FAILED_LOCAL_COMMIT_PRESERVED";exit 78}
$readback=(& git ls-remote origin "refs/heads/$ExpectedBranch").Trim()
if($LASTEXITCODE -ne 0 -or (($readback -split "\s+")[0]) -ne $newHead){Write-Error "A1_OPERATIONAL_PUSH_READBACK_UNKNOWN_LOCAL_COMMIT_PRESERVED";exit 90}
Write-Checkpoint ([string]$cp.qualified_control_head) $operationalBase $newHead $newTree ($sequence+1)
Write-Output "A1_OPERATIONAL_TRANSPORT=PASS"
Write-Output "BASE=$checkpointHead"
Write-Output "HEAD=$newHead"
Write-Output "TREE=$newTree"
Write-Output ("SEQUENCE="+($sequence+1))
