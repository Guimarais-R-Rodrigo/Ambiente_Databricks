param([switch]$SelfTest)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$BlockedNonMcp = @(
    "list_mcp_resources",
    "list_mcp_resource_templates",
    "read_mcp_resource",
    "web__run"
)

function Get-SurfaceDecision([string]$ToolName) {
    if ($ToolName -like "mcp__node_repl__*") { return "ALLOW_INTERNAL_NODE_REPL" }
    if ($ToolName -like "codex_app*" -or $ToolName -like "cua_repl*") { return "DENY" }
    if ($ToolName -like "mcp__*") { return "DENY" }
    if ($BlockedNonMcp -contains $ToolName) { return "DENY" }
    return "DENY_UNEXPECTED_MATCH"
}

function New-DenyPayload([string]$ToolName, [string]$Reason) {
    return @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "deny"
            permissionDecisionReason = $Reason
        }
        ser_controller = @{
            tool_name = $ToolName
            policy = "DENY_EXTERNAL_SURFACES_ALLOW_INTERNAL_NODE_REPL"
        }
    }
}

if ($SelfTest) {
    if ((Get-SurfaceDecision "mcp__node_repl__js") -ne "ALLOW_INTERNAL_NODE_REPL") { throw "EXTERNAL_SURFACE_GUARD_SELFTEST_NODE_REPL" }
    $deniedNames = @(
        "mcp__cua_repl.js",
        "cua_repljs",
        "mcp__codex_app__get_usage_limits",
        "codex_appget_usage_limits",
        "codex_app__get_usage_limits",
        "mcp__example__write",
        "list_mcp_resources",
        "read_mcp_resource",
        "web__run"
    )
    foreach ($name in $deniedNames) {
        if ((Get-SurfaceDecision $name) -ne "DENY") { throw "EXTERNAL_SURFACE_GUARD_SELFTEST_DENY:$name" }
    }
    Write-Output (@{
        schema_version="SER-CODEX-EXTERNAL-SURFACE-GUARD-SELFTEST-1"
        result="PASS"
        internal_node_repl="ALLOW"
        denied_cases=$deniedNames.Count
    } | ConvertTo-Json -Compress)
    exit 0
}

$raw = [Console]::In.ReadToEnd()
try { $event = $raw | ConvertFrom-Json -ErrorAction Stop }
catch {
    [Console]::Out.WriteLine((New-DenyPayload "<unparseable>" "SER controller surface guard could not parse hook input" | ConvertTo-Json -Depth 6 -Compress))
    exit 0
}

$toolName = [string]$event.tool_name
$decision = Get-SurfaceDecision $toolName
if ($decision -eq "ALLOW_INTERNAL_NODE_REPL") { exit 0 }

[Console]::Out.WriteLine((New-DenyPayload $toolName ("SER controller forbids this external/control surface during CQ/A0/A1: " + $toolName) | ConvertTo-Json -Depth 6 -Compress))
