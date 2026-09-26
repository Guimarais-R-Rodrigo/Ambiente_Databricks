# P2 R3 — resolver V2 interrompido por WindowsApps alias

- candidate SHA: `4abbac3078ab1520a8b38689abc6756db3199c3f`
- candidate tree: `273b9331fb0a3f10e91a5dc321b20485c16fbaf7`
- main/merge-base: `4ba7f551767d847381df1556ed937116258fa77d`
- host: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean

```text
P2_R3_LOCAL_QUALIFICATION = BLOCKED_ENVIRONMENT
bootstrap = SER-B1-WINDOWS-PYTHON-RESOLUTION-2
exit_code = 1
json_emitted = false
first_issue = PermissionDenied evaluating WindowsApps/python.exe
formal_gates_started = false
P2_R3_01..P2_R3_05 = NOT_RUN
```

A falha não prova ausência de Python 3: o resolver abortou durante descoberta ao avaliar um App Execution Alias inacessível. Isso é defeito do bootstrap V2.

R3 permanece encerrada e não será reexecutada.

R4 altera somente o resolver: aliases WindowsApps são explicitamente ignorados; operações de filesystem/registry são isoladas por candidato; discovery errors viram dados; um trap top-level garante JSON estruturado para qualquer exceção residual. Nenhuma instalação/download é autorizada.

Se V3 emitir JSON `PYTHON3_INTERPRETER_NOT_RESOLVED` após completar a busca, aí sim tratar como ausência ambiental observável e exigir remediação explícita do host.
