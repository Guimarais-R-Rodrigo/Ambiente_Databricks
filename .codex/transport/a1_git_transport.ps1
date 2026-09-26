Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($args.Count -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_EXTRA_ARGUMENTS"
    exit 64
}

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

$rootText = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $rootText) {
    Write-Error "A1_GIT_TRANSPORT_NOT_A_GIT_REPOSITORY"
    exit 65
}
$root = [IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
$actualScript = [IO.Path]::GetFullPath($PSCommandPath)
$expectedScript = [IO.Path]::GetFullPath((Join-Path $root ".codex\transport\a1_git_transport.ps1"))
if ($actualScript -ne $expectedScript) {
    Write-Error "A1_GIT_TRANSPORT_SCRIPT_NOT_FROM_REPO_ROOT"
    exit 66
}
Set-Location $root

$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) {
    Write-Error "A1_GIT_TRANSPORT_BRANCH_MISMATCH:$branch"
    exit 67
}

$origin = (& git remote get-url origin).Trim()
if ($LASTEXITCODE -ne 0 -or $ExpectedRemotes -notcontains $origin) {
    Write-Error "A1_GIT_TRANSPORT_REMOTE_MISMATCH"
    exit 68
}

$envelopePath = "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json"
$envelope = Get-Content -Raw -Encoding UTF8 $envelopePath | ConvertFrom-Json
$declared = @($envelope.repo_scope.write_roots | Sort-Object)
$expected = @($ExpectedPaths | Sort-Object)
if ([string]::Join([Environment]::NewLine, $declared) -ne [string]::Join([Environment]::NewLine, $expected)) {
    Write-Error "A1_GIT_TRANSPORT_ENVELOPE_PATH_MISMATCH"
    exit 69
}

& python -B tools/check_codex_autonomy_delta.py --worktree
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_WORKTREE_SCOPE_FAIL"
    exit 70
}

& git add -A -- @ExpectedPaths
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_STAGE_FAIL"
    exit 71
}

& python -B tools/check_codex_autonomy_delta.py --index
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_INDEX_SCOPE_FAIL"
    exit 72
}

& git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Output "A1_GIT_TRANSPORT_NO_DELTA"
    exit 0
}
if ($LASTEXITCODE -ne 1) {
    Write-Error "A1_GIT_TRANSPORT_INDEX_DIFF_ERROR"
    exit 73
}

$base = (& git rev-parse HEAD).Trim()
& git -c core.hooksPath=.codex/transport/no-hooks -c commit.gpgSign=false commit --no-gpg-sign --no-verify -m "SER B1 A1: autonomous causal update"
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_COMMIT_FAIL"
    exit 74
}
$head = (& git rev-parse HEAD).Trim()

& python -B tools/check_codex_autonomy_delta.py --base $base --head $head
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_COMMITTED_DELTA_FAIL_NOT_PUSHED"
    exit 75
}

$status = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $status.Count -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_POST_COMMIT_WORKTREE_NOT_CLEAN"
    exit 76
}

$branchAfter = (& git branch --show-current).Trim()
$originAfter = (& git remote get-url origin).Trim()
if ($branchAfter -ne $ExpectedBranch -or $ExpectedRemotes -notcontains $originAfter) {
    Write-Error "A1_GIT_TRANSPORT_IDENTITY_CHANGED"
    exit 77
}

& git -c core.hooksPath=.codex/transport/no-hooks push origin "HEAD:refs/heads/$ExpectedBranch"
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_PUSH_REJECTED_OR_FAILED"
    exit 78
}

Write-Output "A1_GIT_TRANSPORT=PASS"
Write-Output "BASE=$base"
Write-Output "HEAD=$head"
