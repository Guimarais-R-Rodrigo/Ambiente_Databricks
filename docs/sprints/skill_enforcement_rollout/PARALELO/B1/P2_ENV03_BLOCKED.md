# ENV-03 — launcher legado não resolvido pelo PATH da sessão

## Estado observado

- controle SHA: `4887ba45ec1bd39c2a2365f536128f7b42d424dd`
- tree: `77cd2c5a010edbf3a8527eb20ca7ea903df25dbe`
- host: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean
- `Get-Command py.exe`: não resolvido na sessão ENV-03

```text
ENV03 = BLOCKED
FIRST_FAILURE = LEGACY_PY_LAUNCHER_NOT_RESOLVED
CPYTHON_312_PROBE = NOT_RUN
VENV = NOT_CREATED
REQUIREMENTS = NOT_RUN
IMPORT_SMOKE = NOT_RUN
P2_GATES_EXECUTED = false
P2_R5_CREATED = false
REPO_MUTATION = false
```

## Relação com ENV-02

ENV-02 observou explicitamente:

```text
legacy launcher =
%LOCALAPPDATA%\Programs\Python\Launcher\py.exe

selected runtime =
Python 3.12
```

Portanto ENV-03 não demonstra que o launcher ou Python 3.12 desapareceram. Demonstra somente que o diretório do launcher não estava resolvível por `Get-Command` naquela sessão.

## ENV-04

ENV-04 deixa de depender do PATH. Ela constrói o path observado a partir de `%LOCALAPPDATA%`, exige que o arquivo exista e o invoca diretamente com `-3.12 -c`. Se o probe passar, captura `sys.executable`, abandona o launcher para os passos seguintes e prepara o venv externo.

Nenhum fallback de instalação ocorre em ENV-04. Se o path observado não existir ou `-3.12` não puder provar CPython 3.12, a etapa encerra e volta para decisão humana.
