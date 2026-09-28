# P2 R2 — bloqueio ambiental antes dos gates formais

- candidate SHA: `a4edc6cd51a73365b6a93697789057531454cb92`
- candidate tree: `bcfa547d93c4fc1e3ce891bb913406179f516136`
- main/merge-base: `4ba7f551767d847381df1556ed937116258fa77d`
- host: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean

```text
status = FAIL
exit_code = 1
issue = PYTHON3_INTERPRETER_NOT_RESOLVED
formal_gate_executed = false
writes_performed = false
P2_R2_01..P2_R2_05 = NOT_RUN
```

R2 é `BLOCKED_ENVIRONMENT`, não FAIL de candidata. Nenhum Python da P2/B0/skills foi executado.

O resolver V1 não cobria todas as autoridades Windows comuns. R3 amplia somente a descoberta pré-gate, sem instalar/baixar runtime, para PythonCore Registry, roots Conda/Miniforge em USERPROFILE/ProgramData, pyenv-win, Scoop, Rye, uv, ProgramFiles(x86) e roots legados.

Se V2 também falhar, não criar nova corretiva automática: tratar como ausência de Python 3 utilizável observável e exigir remediação ambiental explícita fora da campanha.
