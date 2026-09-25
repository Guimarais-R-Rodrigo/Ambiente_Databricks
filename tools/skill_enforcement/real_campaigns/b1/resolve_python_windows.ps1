$ErrorActionPreference = "Stop"

$SchemaVersion = "SER-B1-WINDOWS-PYTHON-RESOLUTION-1"
$candidates = New-Object System.Collections.Generic.List[object]

function Add-Candidate {
    param(
        [string]$Path,
        [string]$Resolver
    )
    if ([string]::IsNullOrWhiteSpace($Path)) { return }
    try {
        $resolved = [System.IO.Path]::GetFullPath($Path)
    } catch {
        return
    }
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { return }
    if ($candidates | Where-Object { $_.Path -eq $resolved }) { return }
    $candidates.Add([pscustomobject]@{ Path = $resolved; Resolver = $Resolver })
}

foreach ($envVar in @("VIRTUAL_ENV", "CONDA_PREFIX")) {
    $root = [Environment]::GetEnvironmentVariable($envVar)
    if (-not [string]::IsNullOrWhiteSpace($root)) {
        Add-Candidate -Path (Join-Path $root "Scripts\python.exe") -Resolver ("env:" + $envVar)
        Add-Candidate -Path (Join-Path $root "python.exe") -Resolver ("env:" + $envVar)
    }
}

foreach ($name in @("python.exe", "python3.exe")) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $cmd -and -not [string]::IsNullOrWhiteSpace($cmd.Source)) {
        Add-Candidate -Path $cmd.Source -Resolver ("Get-Command:" + $name)
    }
}

$py = Get-Command "py.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($null -ne $py -and -not [string]::IsNullOrWhiteSpace($py.Source)) {
    try {
        $fromLauncher = & $py.Source -3 -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $fromLauncher) {
            Add-Candidate -Path ([string]($fromLauncher | Select-Object -Last 1)).Trim() -Resolver "py.exe:-3"
        }
    } catch {
        # Discovery failure is non-fatal; other candidates remain eligible.
    }
}

$globRoots = @()
if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    $globRoots += (Join-Path $env:LOCALAPPDATA "Programs\Python")
}
if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
    $globRoots += $env:ProgramFiles
}
foreach ($root in $globRoots) {
    if (Test-Path -LiteralPath $root) {
        Get-ChildItem -Path $root -Filter python.exe -File -Recurse -ErrorAction SilentlyContinue |
            ForEach-Object { Add-Candidate -Path $_.FullName -Resolver "filesystem-discovery" }
    }
}

$probeCode = @'
import json, pathlib, sys
p = pathlib.Path(sys.executable).resolve()
print(json.dumps({
    "executable": str(p),
    "version": sys.version.split()[0],
    "major": sys.version_info.major,
    "minor": sys.version_info.minor
}, sort_keys=True))
'@

$attempts = @()
foreach ($candidate in $candidates) {
    try {
        $stdout = & $candidate.Path -B -c $probeCode 2>$null
        $exitCode = $LASTEXITCODE
        if ($exitCode -ne 0 -or -not $stdout) {
            $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; path=$candidate.Path; result="NONZERO" }
            continue
        }
        $payload = ([string]($stdout | Select-Object -Last 1)) | ConvertFrom-Json
        if ($payload.major -ne 3 -or [string]::IsNullOrWhiteSpace($payload.executable)) {
            $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; path=$candidate.Path; result="INVALID_PYTHON3" }
            continue
        }
        if (-not (Test-Path -LiteralPath $payload.executable -PathType Leaf)) {
            $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; path=$candidate.Path; result="SYS_EXECUTABLE_MISSING" }
            continue
        }
        [pscustomobject]@{
            schema_version = $SchemaVersion
            status = "PASS"
            python_executable = $payload.executable
            python_version = $payload.version
            resolver = $candidate.Resolver
            attempts_before_success = $attempts.Count
            writes_performed = $false
            formal_gate_executed = $false
        } | ConvertTo-Json -Compress
        exit 0
    } catch {
        $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; path=$candidate.Path; result=("EXCEPTION:" + $_.Exception.GetType().Name) }
    }
}

[pscustomobject]@{
    schema_version = $SchemaVersion
    status = "FAIL"
    issue = "PYTHON3_INTERPRETER_NOT_RESOLVED"
    attempts = $attempts
    writes_performed = $false
    formal_gate_executed = $false
} | ConvertTo-Json -Depth 5 -Compress
exit 1
