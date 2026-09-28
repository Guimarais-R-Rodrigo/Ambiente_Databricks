Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-A1SessionMetaFromTranscript([string]$TranscriptPath) {
    if ([string]::IsNullOrWhiteSpace($TranscriptPath) -or -not (Test-Path -LiteralPath $TranscriptPath -PathType Leaf)) {
        throw "A1_ROOT_GATE_TRANSCRIPT_MISSING"
    }
    $lines = @(Get-Content -LiteralPath $TranscriptPath -Encoding UTF8 -TotalCount 200)
    foreach ($line in $lines) {
        if ([string]::IsNullOrWhiteSpace([string]$line)) { continue }
        try { $row = [string]$line | ConvertFrom-Json -ErrorAction Stop } catch { continue }
        $typeProp = $row.PSObject.Properties["type"]
        $payloadProp = $row.PSObject.Properties["payload"]
        if ($null -ne $typeProp -and [string]$typeProp.Value -eq "session_meta" -and $null -ne $payloadProp) {
            return $payloadProp.Value
        }
    }
    throw "A1_ROOT_GATE_SESSION_META_NOT_FOUND"
}

function Assert-A1RootControllerInvocation([string]$RepositoryRoot) {
    $root = [IO.Path]::GetFullPath($RepositoryRoot).TrimEnd('\','/')
    $windowsIdentity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    if (
        $windowsIdentity -match '(?i)\\CodexSandboxOffline$' -or
        $windowsIdentity -match '(?i)\\CodexSandboxOnline$'
    ) {
        throw "A1_ROOT_GATE_CALLER_STILL_SANDBOXED:$windowsIdentity"
    }

    $threadId = [string]$env:CODEX_THREAD_ID
    $parsedThread = [Guid]::Empty
    if ([string]::IsNullOrWhiteSpace($threadId) -or -not [Guid]::TryParse($threadId, [ref]$parsedThread)) {
        throw "A1_ROOT_GATE_THREAD_ID_MISSING_OR_INVALID"
    }

    $sessionsRoot = [IO.Path]::GetFullPath((Join-Path $HOME ".codex\sessions")).TrimEnd('\','/')
    if (-not (Test-Path -LiteralPath $sessionsRoot -PathType Container)) {
        throw "A1_ROOT_GATE_SESSIONS_ROOT_MISSING"
    }
    $candidates = @(
        Get-ChildItem -LiteralPath $sessionsRoot -Recurse -File -Filter "*.jsonl" -ErrorAction Stop |
            Where-Object { $_.Name.IndexOf($threadId, [StringComparison]::OrdinalIgnoreCase) -ge 0 }
    )
    if ($candidates.Count -ne 1) {
        throw "A1_ROOT_GATE_TRANSCRIPT_COUNT:$($candidates.Count)"
    }
    $transcript = [IO.Path]::GetFullPath($candidates[0].FullName)
    if (-not $transcript.StartsWith($sessionsRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "A1_ROOT_GATE_TRANSCRIPT_OUTSIDE_SESSIONS"
    }

    $meta = Get-A1SessionMetaFromTranscript $transcript
    $metaId = [string]$meta.id
    if ($metaId -ne $threadId) { throw "A1_ROOT_GATE_SESSION_ID_MISMATCH" }

    $sourceProperty = $meta.PSObject.Properties["source"]
    if ($null -eq $sourceProperty -or $sourceProperty.Value -isnot [string] -or [string]$sourceProperty.Value -cne "cli") {
        throw "A1_ROOT_GATE_SOURCE_NOT_CLI"
    }
    $parentProperty = $meta.PSObject.Properties["parent_thread_id"]
    if ($null -ne $parentProperty -and -not [string]::IsNullOrWhiteSpace([string]$parentProperty.Value)) {
        throw "A1_ROOT_GATE_PARENT_THREAD_PRESENT"
    }
    $cwdProperty = $meta.PSObject.Properties["cwd"]
    if ($null -eq $cwdProperty -or [string]::IsNullOrWhiteSpace([string]$cwdProperty.Value)) {
        throw "A1_ROOT_GATE_SESSION_CWD_MISSING"
    }
    $sessionCwd = [IO.Path]::GetFullPath([string]$cwdProperty.Value).TrimEnd('\','/')
    if (-not [string]::Equals($sessionCwd, $root, [StringComparison]::OrdinalIgnoreCase)) {
        throw "A1_ROOT_GATE_SESSION_CWD_MISMATCH"
    }

    return [pscustomobject][ordered]@{
        result = "PASS"
        source = "cli"
        thread_id = $threadId
        transcript = $transcript
        windows_identity = $windowsIdentity
    }
}
