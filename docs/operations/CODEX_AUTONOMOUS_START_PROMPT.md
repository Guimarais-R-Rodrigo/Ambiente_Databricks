# Prompt inicial — Codex Autonomous Controller

Para Codex Desktop Windows, executar primeiro no PowerShell do host:

```powershell
Set-Location "C:\b1_worktrees\b1_p1_4ba7f551_20260924"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\codex_desktop_cq_host_preflight.ps1
```

Só iniciar a conversa se `CQ_HOST_PREFLIGHT = PASS`.

Antes do chat, desabilitar temporariamente plugins externos write-capable em
Settings > Plugins, inclusive Creative Production se estiver habilitado.
Tools internos do próprio Codex app não precisam ser desinstalados; mutadores
não devem ser invocados durante CQ.

Use este prompt em uma nova conversa do projeto B1:

```text
Operate this repository in SER Autonomous Controller Mode.

CLIENT_SURFACE = CODEX_DESKTOP_WINDOWS

Read:
- AGENTS.md
- docs/operations/CODEX_RUNTIME_QUALIFICATION.md
- docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md
- docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md
- docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json
- the live state source referenced by the envelope

Do not load the full CHANGELOG.

Execute CQ0-CQ5 using the Desktop Windows profile. Read and verify the external
CQ_HOST_PREFLIGHT.json and its SHA256. Use the absolute Python executable bound
by that preflight. It must be inside ~\AppData\Local\Programs\Python\Python312,
which is read-enabled for A0/A1. Do not rely on the PATH token "python" and do
not install dependencies.

Codex CLI/version/strict/execpolicy commands are optional observations on this
surface. If inaccessible, record NOT_OBSERVABLE_DESKTOP rather than inventing
PASS or blocking solely for that reason. If the nominal project profile name is
not observable, record PROJECT_PROFILE_ACTIVE=NOT_OBSERVABLE_DESKTOP and
continue provisionally. Final PASS requires project-config hash plus CQ3/CQ4/CQ5
behavioral proof and PROJECT_PROFILE_EFFECTIVE=PASS_BEHAVIORALLY.

The host-side fetch evidence may prove the remote branch identity. PR metadata
may be DEFERRED_TO_EXTERNAL_ADJUDICATION and will be independently rechecked
outside this session.

Classify mcp__codex_app__* as INTERNAL_CLIENT_CONTROL_PLANE: inventory them but
do not invoke mutators. A loaded external persistent write-capable plugin is a
CQ blocker.

Do not use /permissions, Full Access, --yolo, sandbox widening,
request_permissions or another override.

Expected authority:
- Windows elevated A0/A1 includes :root=read (read visibility only);
- root/explorer/auditors = ser-controller-a0;
- A0 repo writes denied;
- executor = ser-b1-a1;
- A1 repo writes limited to the exact ten envelope files;
- direct .git write denied;
- A0/A1 command network disabled;
- Git commit/push only through .codex/transport/a1_git_transport.ps1.

Run real CQ3 spawned-role probes.

In CQ5 run the validator and metatests with the absolute Python from host
preflight.

If any controller gate fails, stop at CONTROLLER_MAINTENANCE. Do not self-repair.

If CQ0-CQ5 is technically green, do not write canonical PASS and do not remove
AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION. Record only
REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE for runtime/effective config,
preserve the blocker, create a sanitized evidence package outside the repo, and
STOP at CONTROLLER_MAINTENANCE.

No B1 material, A2, residual G6, Genie, policy promotion, Ready or merge is
authorized.
```
