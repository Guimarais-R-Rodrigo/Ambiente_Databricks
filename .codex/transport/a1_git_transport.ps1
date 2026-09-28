param(
    [switch]$SelfTest
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
$JournalPath = "docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTONOMY/JOURNAL.jsonl"
$EvidencePath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.json"
$SidecarPath = Join-Path $HOME "codex-scratch\Ambiente_Databricks\CQ_HOST_PREFLIGHT.sha256"

function Resolve-RepositoryRoot {
    $rootText = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $rootText) {
        Write-Error "A1_GIT_TRANSPORT_NOT_A_GIT_REPOSITORY"
        exit 65
    }
    return [IO.Path]::GetFullPath(($rootText | Select-Object -First 1).Trim())
}

function Require-StandaloneCheckout([string]$Root) {
    $gitDirText = (& git rev-parse --path-format=absolute --git-dir 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $gitDirText) {
        Write-Error "A1_GIT_TRANSPORT_GIT_DIR_UNRESOLVED"
        exit 91
    }
    $commonDirText = (& git rev-parse --path-format=absolute --git-common-dir 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $commonDirText) {
        Write-Error "A1_GIT_TRANSPORT_COMMON_DIR_UNRESOLVED"
        exit 91
    }
    $trimChars = [char[]]@([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $gitDir = [IO.Path]::GetFullPath(($gitDirText | Select-Object -First 1).Trim()).TrimEnd($trimChars)
    $commonDir = [IO.Path]::GetFullPath(($commonDirText | Select-Object -First 1).Trim()).TrimEnd($trimChars)
    $expected = [IO.Path]::GetFullPath((Join-Path $Root ".git")).TrimEnd($trimChars)
    if (
        -not [string]::Equals($gitDir, $expected, [StringComparison]::OrdinalIgnoreCase) -or
        -not [string]::Equals($commonDir, $expected, [StringComparison]::OrdinalIgnoreCase)
    ) {
        Write-Error "A1_GIT_TRANSPORT_LINKED_WORKTREE_UNSUPPORTED"
        exit 91
    }
}

function Require-RepositoryIdentity([string]$Root) {
    Set-Location $Root
    $branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -ne $ExpectedBranch) {
        Write-Error "A1_GIT_TRANSPORT_BRANCH_MISMATCH:$branch"
        exit 67
    }
    $origin = (& git remote get-url origin).Trim()
    if ($LASTEXITCODE -ne 0) {
        Write-Error "A1_GIT_TRANSPORT_REMOTE_READ_FAILED"
        exit 68
    }
    $pushOrigin = (& git remote get-url --push origin).Trim()
    if ($LASTEXITCODE -ne 0 -or $ExpectedRemotes -notcontains $origin -or $ExpectedRemotes -notcontains $pushOrigin) {
        Write-Error "A1_GIT_TRANSPORT_REMOTE_MISMATCH"
        exit 68
    }
    return [pscustomobject]@{ branch=$branch; origin=$origin; push_origin=$pushOrigin }
}

function Require-Envelope([string]$Root) {
    $envelopePath = Join-Path $Root "docs\operations\autonomy\B1_AUTONOMY_ENVELOPE.json"
    $envelope = Get-Content -Raw -Encoding UTF8 $envelopePath | ConvertFrom-Json
    $declared = @($envelope.repo_scope.write_roots | Sort-Object)
    $expected = @($ExpectedPaths | Sort-Object)
    if ([string]::Join([Environment]::NewLine, $declared) -ne [string]::Join([Environment]::NewLine, $expected)) {
        Write-Error "A1_GIT_TRANSPORT_ENVELOPE_PATH_MISMATCH"
        exit 69
    }
}

$root = Resolve-RepositoryRoot
$actualScript = [IO.Path]::GetFullPath($PSCommandPath)
$expectedScript = [IO.Path]::GetFullPath((Join-Path $root ".codex\transport\a1_git_transport.ps1"))
if ($actualScript -ne $expectedScript) {
    Write-Error "A1_GIT_TRANSPORT_SCRIPT_NOT_FROM_REPO_ROOT"
    exit 66
}
Set-Location $root
Require-StandaloneCheckout $root

$identity = Require-RepositoryIdentity $root
Require-Envelope $root

if ($SelfTest) {
    Write-Output (@{
        schema_version = "SER-A1-GIT-TRANSPORT-SELFTEST-1"
        result = "PASS"
        branch = $identity.branch
        read_remote = $identity.origin
        push_remote = $identity.push_origin
    } | ConvertTo-Json -Compress)
    exit 0
}

if ($args.Count -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_EXTRA_ARGUMENTS"
    exit 64
}

if (-not (Test-Path -LiteralPath $EvidencePath) -or -not (Test-Path -LiteralPath $SidecarPath)) {
    Write-Error "A1_GIT_TRANSPORT_HOST_EVIDENCE_MISSING"
    exit 79
}
$actualEvidenceSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $EvidencePath).Hash.ToUpperInvariant()
$sidecarSha = (((Get-Content -LiteralPath $SidecarPath -Raw).Trim() -split "\s+")[0]).ToUpperInvariant()
if ($sidecarSha -ne $actualEvidenceSha) {
    Write-Error "A1_GIT_TRANSPORT_HOST_EVIDENCE_SHA_MISMATCH"
    exit 80
}
try { $evidence = Get-Content -LiteralPath $EvidencePath -Raw | ConvertFrom-Json -ErrorAction Stop }
catch {
    Write-Error "A1_GIT_TRANSPORT_HOST_EVIDENCE_INVALID_JSON"
    exit 81
}
if ($evidence.schema_version -ne "AC-R2-CLI-HOST-PREFLIGHT-1" -or $evidence.result -ne "PASS") {
    Write-Error "A1_GIT_TRANSPORT_HOST_EVIDENCE_INVALID"
    exit 81
}
if ([string]$evidence.git.checkout_mode -ne "STANDALONE") {
    Write-Error "A1_GIT_TRANSPORT_HOST_EVIDENCE_CHECKOUT_MODE"
    exit 92
}

$QualifiedPython = [string]$evidence.python.executable
if ([string]::IsNullOrWhiteSpace($QualifiedPython) -or -not (Test-Path -LiteralPath $QualifiedPython)) {
    Write-Error "A1_GIT_TRANSPORT_BOUND_PYTHON_MISSING"
    exit 82
}
$deltaPath = Join-Path $root "tools\check_codex_autonomy_delta.py"
$deltaHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $deltaPath).Hash.ToUpperInvariant()
if ($deltaHash -ne ([string]$evidence.source_sha256.delta_checker).ToUpperInvariant()) {
    Write-Error "A1_GIT_TRANSPORT_DELTA_CHECKER_SHA_MISMATCH"
    exit 83
}

$base = (& git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $base -ne [string]$evidence.git.head) {
    Write-Error "A1_GIT_TRANSPORT_BASE_NOT_PREFLIGHT_HEAD"
    exit 87
}

& $QualifiedPython -B tools/check_codex_autonomy_delta.py --worktree
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_WORKTREE_SCOPE_FAIL"
    exit 70
}

$changedPaths = @()
$changedPaths += @(& git diff --name-only HEAD)
if ($LASTEXITCODE -ne 0) { Write-Error "A1_GIT_TRANSPORT_CHANGED_PATHS_FAIL"; exit 84 }
$changedPaths += @(& git diff --cached --name-only HEAD)
if ($LASTEXITCODE -ne 0) { Write-Error "A1_GIT_TRANSPORT_CHANGED_PATHS_FAIL"; exit 84 }
$changedPaths += @(& git ls-files --others --exclude-standard)
if ($LASTEXITCODE -ne 0) { Write-Error "A1_GIT_TRANSPORT_CHANGED_PATHS_FAIL"; exit 84 }
$changedPaths = @($changedPaths | Where-Object { $_ } | ForEach-Object { $_.Trim() } | Sort-Object -Unique)

$cqJournalMode = $false
$lastJournal = $null
if (Test-Path -LiteralPath $JournalPath) {
    $journalLines = @(Get-Content -LiteralPath $JournalPath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($journalLines.Count -gt 0) {
        try { $lastJournal = $journalLines[-1] | ConvertFrom-Json -ErrorAction Stop } catch { $lastJournal = $null }
        if (
            $null -ne $lastJournal -and
            $lastJournal.event -eq "CQ3_A1_POSITIVE_PROBE" -and
            $lastJournal.authority -eq "CONTROLLER_RUNTIME_QUALIFICATION_ONLY"
        ) {
            $cqJournalMode = $true
        }
    }
}

if ($cqJournalMode) {
    if ($changedPaths.Count -ne 1 -or $changedPaths[0] -ne $JournalPath) {
        Write-Error "A1_GIT_TRANSPORT_CQ_JOURNAL_NOT_EXCLUSIVE"
        exit 85
    }
    if ([string]$lastJournal.candidate_head -ne [string]$evidence.git.head) {
        Write-Error "A1_GIT_TRANSPORT_CQ_CANDIDATE_HEAD_MISMATCH"
        exit 86
    }
    $StagePaths = @($JournalPath)
} else {
    $StagePaths = $ExpectedPaths
}

& git fetch origin $ExpectedBranch
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_FETCH_FAIL"
    exit 88
}
$originHead = (& git rev-parse "origin/$ExpectedBranch").Trim()
if ($LASTEXITCODE -ne 0 -or $originHead -ne $base) {
    Write-Error "A1_GIT_TRANSPORT_REMOTE_ADVANCED"
    exit 89
}

& git add -A -- @StagePaths
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_STAGE_FAIL"
    exit 71
}

& $QualifiedPython -B tools/check_codex_autonomy_delta.py --index
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

& git -c core.hooksPath=.codex/transport/no-hooks -c commit.gpgSign=false commit --no-gpg-sign --no-verify -m "SER B1 A1: autonomous causal update"
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_COMMIT_FAIL"
    exit 74
}
$head = (& git rev-parse HEAD).Trim()

& $QualifiedPython -B tools/check_codex_autonomy_delta.py --base $base --head $head
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_COMMITTED_DELTA_FAIL_NOT_PUSHED"
    exit 75
}

$status = @(& git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $status.Count -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_POST_COMMIT_WORKTREE_NOT_CLEAN"
    exit 76
}

$identityAfter = Require-RepositoryIdentity $root
if ($identityAfter.branch -ne $ExpectedBranch) {
    Write-Error "A1_GIT_TRANSPORT_IDENTITY_CHANGED"
    exit 77
}

& git -c core.hooksPath=.codex/transport/no-hooks push origin "HEAD:refs/heads/$ExpectedBranch"
if ($LASTEXITCODE -ne 0) {
    Write-Error "A1_GIT_TRANSPORT_PUSH_REJECTED_OR_FAILED"
    exit 78
}

$remoteReadback = (& git ls-remote origin "refs/heads/$ExpectedBranch").Trim()
if (
    $LASTEXITCODE -ne 0 -or
    [string]::IsNullOrWhiteSpace($remoteReadback) -or
    (($remoteReadback -split "\s+")[0]) -ne $head
) {
    Write-Error "A1_GIT_TRANSPORT_REMOTE_READBACK_FAIL"
    exit 90
}

$tree = (& git rev-parse 'HEAD^{tree}').Trim()
Write-Output "A1_GIT_TRANSPORT=PASS"
Write-Output ("MODE=" + $(if($cqJournalMode){"CQ_JOURNAL_ONLY"}else{"A1_GENERAL"}))
Write-Output "BASE=$base"
Write-Output "HEAD=$head"
Write-Output "TREE=$tree"
