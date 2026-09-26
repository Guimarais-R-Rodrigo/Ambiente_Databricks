# ENV-02 — Python Install Manager instalado, mas `py` sombreado pelo launcher legado

## Estado observado

- controle SHA: `22236637e01489c4b636965fd1c76588b99bfba6`
- tree: `cff9689dac0f2bdc6e855417c34f86044127a209`
- host: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean
- `Add-AppxPackage`: disponível
- Python Install Manager oficial instalado com sucesso
- pacote: `PythonSoftwareFoundation.PythonManager`
- versão observada: `26.3.240.0`
- package family: `PythonSoftwareFoundation.PythonManager_3847v3x7pw1km`

## Falha

`Get-Command py.exe` resolveu o launcher legado já instalado, não o Python Install Manager. O comando `py.exe help` foi tratado pelo launcher legado como tentativa de executar um arquivo chamado `help`, selecionando um runtime Python 3.12 e retornando exit 2.

```text
ENV02 = FAIL
FIRST_FAILURE = PYTHON_INSTALL_MANAGER_HELP_FAILED
P2_GATES_EXECUTED = false
P2_RESOLVER_V3_EXECUTED = false
P2_R5_CREATED = false
REPO_MUTATION = false
```

## Reclassificação útil

O resultado revela duas informações independentes:

1. o Python Install Manager foi efetivamente instalado;
2. existe um runtime Python 3.12 que o launcher legado consegue selecionar.

A documentação oficial do Python descreve esse conflito: o launcher legado pode sombrear o comando `py`; para automação do Install Manager, o comando não ambíguo é `pymanager`.

Não é necessário remover o launcher legado nesta frente.

## Decisão para ENV-03

A P2 não exige Python 3.13. O repositório contém um certifier local que exige explicitamente Python 3.12 e múltiplas execuções históricas nessa série. Portanto ENV-03 não instala outro runtime: primeiro prova o CPython 3.12 já existente via launcher legado, captura `sys.executable`, cria venv externo e instala `tools/requirements-dev.txt`.

O Python Install Manager permanece instalado, mas não é pré-requisito para ENV-03.
