# ENV-01 — bloqueio por ausência de WinGet

## Estado observado

- controle SHA: `fbd47bbd019ef4b6a679c1a91dec8ce3d8278a29`
- tree: `a7e0366e7966dd8c2cd340c0b0732d80cd7ea203`
- host: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean
- `winget.exe`: não resolvido por `Get-Command`

```text
ENV01 = BLOCKED
FIRST_BLOCKER = WINGET_NOT_AVAILABLE
PYTHON_INSTALL_MANAGER = NOT_RUN
CPYTHON_313 = NOT_RUN
VENV = NOT_CREATED
REQUIREMENTS = NOT_RUN
IMPORT_SMOKE = NOT_RUN
P2_GATES_EXECUTED = false
P2_RESOLVER_V3_EXECUTED = false
REPO_MUTATION = false
```

ENV-01 permanece encerrada. Não houve tentativa de instalador alternativo.

## Classificação

A ausência de WinGet não é defeito de P2 e não é evidência contra SER03/SER05. É somente limitação do método de provisionamento escolhido em ENV-01.

A documentação oficial do Python prevê instalação do Python Install Manager sem WinGet por PowerShell usando o AppInstaller oficial do python.org:

`Add-AppxPackage -AppInstallerFile https://www.python.org/ftp/python/pymanager/pymanager.appinstaller`

A etapa sucessora recebe o nome ENV-02. Ela continua fora de qualquer round P2.
