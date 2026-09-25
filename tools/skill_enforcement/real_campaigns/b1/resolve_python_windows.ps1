$ErrorActionPreference = "Stop"

$SchemaVersion = "SER-B1-WINDOWS-PYTHON-RESOLUTION-3"
$candidates = New-Object System.Collections.Generic.List[object]
$discoveryIssues = New-Object System.Collections.Generic.List[object]

trap {
    [pscustomobject]@{
        schema_version = $SchemaVersion
        status = "FAIL"
        issue = "RESOLVER_UNHANDLED_EXCEPTION"
        exception_type = $_.Exception.GetType().Name
        candidates_observed = $candidates.Count
        discovery_issues = $discoveryIssues
        writes_performed = $false
        formal_gate_executed = $false
    } | ConvertTo-Json -Depth 6 -Compress
    exit 1
}

function Add-Discovery-Issue {
    param([string]$Resolver,[string]$Result)
    $discoveryIssues.Add([pscustomobject]@{
        resolver = $Resolver
        result = $Result
    })
}

function Add-Candidate {
    param([string]$Path,[string]$Resolver)
    if ([string]::IsNullOrWhiteSpace($Path)) { return }
    try {
        $resolved = [System.IO.Path]::GetFullPath($Path)
        if ($resolved -match "\\Microsoft\\WindowsApps\\") {
            Add-Discovery-Issue -Resolver $Resolver -Result "APP_EXECUTION_ALIAS_SKIPPED"
            return
        }
        $exists = Test-Path -LiteralPath $resolved -PathType Leaf -ErrorAction Stop
        if (-not $exists) { return }
    } catch {
        Add-Discovery-Issue -Resolver $Resolver -Result ("PATH_REJECTED:" + $_.Exception.GetType().Name)
        return
    }
    if ($candidates | Where-Object { $_.Path -eq $resolved }) { return }
    $candidates.Add([pscustomobject]@{ Path = $resolved; Resolver = $Resolver })
}

function Add-RootPython {
    param([string]$Root,[string]$Resolver)
    if ([string]::IsNullOrWhiteSpace($Root)) { return }
    try {
        Add-Candidate -Path (Join-Path $Root "python.exe" -ErrorAction Stop) -Resolver $Resolver
        Add-Candidate -Path (Join-Path $Root "Scripts\python.exe" -ErrorAction Stop) -Resolver $Resolver
    } catch {
        Add-Discovery-Issue -Resolver $Resolver -Result ("ROOT_REJECTED:" + $_.Exception.GetType().Name)
    }
}

function Add-RecursivePython {
    param([string]$Root,[string]$Resolver,[int]$Max = 64)
    if ([string]::IsNullOrWhiteSpace($Root)) { return }
    try {
        if (-not (Test-Path -LiteralPath $Root -ErrorAction Stop)) { return }
        Get-ChildItem -LiteralPath $Root -Filter python.exe -File -Recurse -ErrorAction SilentlyContinue |
            Select-Object -First $Max |
            ForEach-Object { Add-Candidate -Path $_.FullName -Resolver $Resolver }
    } catch {
        Add-Discovery-Issue -Resolver $Resolver -Result ("RECURSIVE_ROOT_REJECTED:" + $_.Exception.GetType().Name)
    }
}

foreach ($envVar in @("VIRTUAL_ENV","CONDA_PREFIX","PYTHONHOME")) {
    Add-RootPython -Root ([Environment]::GetEnvironmentVariable($envVar)) -Resolver ("env:" + $envVar)
}

foreach ($name in @("python.exe","python3.exe")) {
    try {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -ne $cmd -and -not [string]::IsNullOrWhiteSpace($cmd.Source)) {
            Add-Candidate -Path $cmd.Source -Resolver ("Get-Command:" + $name)
        }
    } catch {
        Add-Discovery-Issue -Resolver ("Get-Command:" + $name) -Result ("LOOKUP_REJECTED:" + $_.Exception.GetType().Name)
    }
}

try {
    $py = Get-Command "py.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $py -and -not [string]::IsNullOrWhiteSpace($py.Source)) {
        try {
            $fromLauncher = & $py.Source -3 -c "import sys; print(sys.executable)" 2>$null
            if ($LASTEXITCODE -eq 0 -and $fromLauncher) {
                Add-Candidate -Path ([string]($fromLauncher | Select-Object -Last 1)).Trim() -Resolver "py.exe:-3"
            } else {
                Add-Discovery-Issue -Resolver "py.exe:-3" -Result "LAUNCHER_NONZERO"
            }
        } catch {
            Add-Discovery-Issue -Resolver "py.exe:-3" -Result ("LAUNCHER_REJECTED:" + $_.Exception.GetType().Name)
        }
    }
} catch {
    Add-Discovery-Issue -Resolver "Get-Command:py.exe" -Result ("LOOKUP_REJECTED:" + $_.Exception.GetType().Name)
}

foreach ($registryRoot in @(
    "HKCU:\Software\Python\PythonCore",
    "HKLM:\Software\Python\PythonCore",
    "HKLM:\Software\WOW6432Node\Python\PythonCore"
)) {
    try {
        if (-not (Test-Path -LiteralPath $registryRoot -ErrorAction Stop)) { continue }
        Get-ChildItem -LiteralPath $registryRoot -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                $installKeyPath = Join-Path $_.PSPath "InstallPath" -ErrorAction Stop
                if (Test-Path -LiteralPath $installKeyPath -ErrorAction Stop) {
                    $key = Get-Item -LiteralPath $installKeyPath -ErrorAction Stop
                    $install = [string]$key.GetValue("")
                    Add-RootPython -Root $install -Resolver ("registry:" + $_.PSChildName)
                }
            } catch {
                Add-Discovery-Issue -Resolver ("registry:" + $_.PSChildName) -Result ("REGISTRY_ENTRY_REJECTED:" + $_.Exception.GetType().Name)
            }
        }
    } catch {
        Add-Discovery-Issue -Resolver $registryRoot -Result ("REGISTRY_ROOT_REJECTED:" + $_.Exception.GetType().Name)
    }
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
            $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; result="NONZERO" }
            continue
        }
        $payload = ([string]($stdout | Select-Object -Last 1)) | ConvertFrom-Json
        if ($payload.major -ne 3 -or [string]::IsNullOrWhiteSpace($payload.executable)) {
            $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; result="INVALID_PYTHON3" }
            continue
        }
        try {
            if (-not (Test-Path -LiteralPath $payload.executable -PathType Leaf -ErrorAction Stop)) {
                $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; result="SYS_EXECUTABLE_MISSING" }
                continue
            }
        } catch {
            $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; result=("SYS_EXECUTABLE_REJECTED:" + $_.Exception.GetType().Name) }
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
            discovery_issues = $discoveryIssues
            writes_performed = $false
            formal_gate_executed = $false
        } | ConvertTo-Json -Depth 6 -Compress
        exit 0
    } catch {
        $attempts += [pscustomobject]@{ resolver=$candidate.Resolver; result=("EXCEPTION:" + $_.Exception.GetType().Name) }
    }
}

[pscustomobject]@{
    schema_version = $SchemaVersion
    status = "FAIL"
    issue = "PYTHON3_INTERPRETER_NOT_RESOLVED"
    candidates_observed = $candidates.Count
    attempts = $attempts
    discovery_issues = $discoveryIssues
    searched_authorities = @(
        "env:VIRTUAL_ENV/CONDA_PREFIX/PYTHONHOME",
        "PATH:Get-Command excluding WindowsApps aliases",
        "py.exe:-3",
        "Windows PythonCore registry",
        "USERPROFILE conda/miniforge/pyenv-win/rye/scoop",
        "PROGRAMDATA conda/miniforge",
        "LOCALAPPDATA Programs/Python + uv",
        "APPDATA uv",
        "ProgramFiles/ProgramFiles(x86)",
        "legacy C:\Python* and C:\tools"
    )
    writes_performed = $false
    formal_gate_executed = $false
} | ConvertTo-Json -Depth 6 -Compress
exit 1
