$ErrorActionPreference = "Stop"

$SchemaVersion = "SER-B1-WINDOWS-PYTHON-RESOLUTION-2"
$candidates = New-Object System.Collections.Generic.List[object]

function Add-Candidate {
    param([string]$Path,[string]$Resolver)
    if ([string]::IsNullOrWhiteSpace($Path)) { return }
    try { $resolved = [System.IO.Path]::GetFullPath($Path) } catch { return }
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { return }
    if ($candidates | Where-Object { $_.Path -eq $resolved }) { return }
    $candidates.Add([pscustomobject]@{ Path = $resolved; Resolver = $Resolver })
}

function Add-RootPython {
    param([string]$Root,[string]$Resolver)
    if ([string]::IsNullOrWhiteSpace($Root)) { return }
    Add-Candidate -Path (Join-Path $Root "python.exe") -Resolver $Resolver
    Add-Candidate -Path (Join-Path $Root "Scripts\python.exe") -Resolver $Resolver
}

function Add-RecursivePython {
    param([string]$Root,[string]$Resolver,[int]$Max = 64)
    if ([string]::IsNullOrWhiteSpace($Root) -or -not (Test-Path -LiteralPath $Root)) { return }
    try {
        Get-ChildItem -LiteralPath $Root -Filter python.exe -File -Recurse -ErrorAction SilentlyContinue |
            Select-Object -First $Max |
            ForEach-Object { Add-Candidate -Path $_.FullName -Resolver $Resolver }
    } catch {}
}

foreach ($envVar in @("VIRTUAL_ENV","CONDA_PREFIX","PYTHONHOME")) {
    Add-RootPython -Root ([Environment]::GetEnvironmentVariable($envVar)) -Resolver ("env:" + $envVar)
}

foreach ($name in @("python.exe","python3.exe")) {
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
    } catch {}
}

foreach ($registryRoot in @(
    "HKCU:\Software\Python\PythonCore",
    "HKLM:\Software\Python\PythonCore",
    "HKLM:\Software\WOW6432Node\Python\PythonCore"
)) {
    if (-not (Test-Path -LiteralPath $registryRoot)) { continue }
    try {
        Get-ChildItem -LiteralPath $registryRoot -ErrorAction SilentlyContinue | ForEach-Object {
            $installKeyPath = Join-Path $_.PSPath "InstallPath"
            if (Test-Path -LiteralPath $installKeyPath) {
                $key = Get-Item -LiteralPath $installKeyPath
                $install = [string]$key.GetValue("")
                Add-RootPython -Root $install -Resolver ("registry:" + $_.PSChildName)
            }
        }
    } catch {}
}

$knownRoots = New-Object System.Collections.Generic.List[object]
function Add-KnownRoot {
    param([string]$Path,[string]$Resolver,[bool]$Recursive = $false)
    if ([string]::IsNullOrWhiteSpace($Path)) { return }
    $knownRoots.Add([pscustomobject]@{ Path=$Path; Resolver=$Resolver; Recursive=$Recursive })
}

if ($env:USERPROFILE) {
    foreach ($name in @("anaconda3","miniconda3","miniforge3","mambaforge")) {
        Add-KnownRoot -Path (Join-Path $env:USERPROFILE $name) -Resolver ("user-root:" + $name)
    }
    Add-KnownRoot -Path (Join-Path $env:USERPROFILE ".pyenv\pyenv-win\versions") -Resolver "pyenv-win" -Recursive $true
    Add-KnownRoot -Path (Join-Path $env:USERPROFILE ".rye\py") -Resolver "rye-managed" -Recursive $true
    Add-KnownRoot -Path (Join-Path $env:USERPROFILE "scoop\apps") -Resolver "scoop" -Recursive $true
}
if ($env:PROGRAMDATA) {
    foreach ($name in @("Anaconda3","Miniconda3","Miniforge3","Mambaforge")) {
        Add-KnownRoot -Path (Join-Path $env:PROGRAMDATA $name) -Resolver ("programdata:" + $name)
    }
}
if ($env:LOCALAPPDATA) {
    Add-KnownRoot -Path (Join-Path $env:LOCALAPPDATA "Programs\Python") -Resolver "localappdata-python" -Recursive $true
    Add-KnownRoot -Path (Join-Path $env:LOCALAPPDATA "uv\python") -Resolver "uv-managed-local" -Recursive $true
    Add-KnownRoot -Path (Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps") -Resolver "windows-app-alias"
}
if ($env:APPDATA) {
    Add-KnownRoot -Path (Join-Path $env:APPDATA "uv\python") -Resolver "uv-managed-roaming" -Recursive $true
}
if ($env:ProgramFiles) {
    Add-KnownRoot -Path $env:ProgramFiles -Resolver "program-files" -Recursive $true
}
$ProgramFilesX86 = [Environment]::GetEnvironmentVariable("ProgramFiles(x86)")
if ($ProgramFilesX86) {
    Add-KnownRoot -Path $ProgramFilesX86 -Resolver "program-files-x86" -Recursive $true
}
foreach ($root in @("C:\Python3","C:\Python310","C:\Python311","C:\Python312","C:\Python313","C:\tools")) {
    Add-KnownRoot -Path $root -Resolver "legacy-root" -Recursive $true
}

foreach ($item in $knownRoots) {
    if ($item.Recursive) { Add-RecursivePython -Root $item.Path -Resolver $item.Resolver }
    else { Add-RootPython -Root $item.Path -Resolver $item.Resolver }
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
            candidates_observed = $candidates.Count
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
    candidates_observed = $candidates.Count
    attempts = $attempts
    searched_authorities = @(
        "env:VIRTUAL_ENV/CONDA_PREFIX/PYTHONHOME",
        "PATH:Get-Command",
        "py.exe:-3",
        "Windows PythonCore registry",
        "USERPROFILE conda/miniforge/pyenv-win/rye/scoop",
        "PROGRAMDATA conda/miniforge",
        "LOCALAPPDATA Programs/Python + uv + WindowsApps",
        "APPDATA uv",
        "ProgramFiles/ProgramFiles(x86)",
        "legacy C:\Python* and C:\tools"
    )
    writes_performed = $false
    formal_gate_executed = $false
} | ConvertTo-Json -Depth 6 -Compress
exit 1
