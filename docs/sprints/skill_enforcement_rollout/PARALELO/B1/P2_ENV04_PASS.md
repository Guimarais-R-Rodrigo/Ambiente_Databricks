# ENV-04 — remediação ambiental concluída

## Identidade

- controle SHA: `b5f8553dd3e1ed4f846b30dc61e9106a71ac94b1`
- tree: `082905112a3a09b88fc8a7b292d39ab7fb5e5841`
- main/merge-base: `4ba7f551767d847381df1556ed937116258fa77d`
- host: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean

## Runtime observado

O launcher legado no path observado em ENV-02 foi invocado diretamente e selecionou:

```text
implementation = CPython
python_version = 3.12.10
architecture = 64bit
machine = AMD64
probe_exit_code = 0
```

O executável real foi provado diretamente antes da criação do venv.

## Venv

Foi criado um venv externo ao repositório em:

`<LOCALAPPDATA>\AmbienteDatabricks\venvs\ser-b1-p2-py312-env04`

```text
existed_before = false
create_exit_code = 0
python_version = 3.12.10
isolated = true
```

Nenhum path absoluto de perfil do usuário é versionado neste documento.

## Dependências

```text
tools/requirements-dev.txt SHA256 =
5df30220f76f9d3fe34512d03446a405fe703223442db4cf72a29ba72693bd9a

tools/requirements-temas-dev.txt SHA256 =
eab43ce8b26d15e11186f735ef885b4b3fe844479894190fdb23d16db4a3a294

pip =
25.0.1

requirements install exit =
0
```

## Smoke ambiental

```text
python = 3.12.10
numpy = 2.5.3
pandas = 3.0.6
sklearn = 1.9.1
plotly = 7.1.0
jinja2 = 3.1.6
pyyaml = 6.0.3
regex = 2026.9.10
exit_code = 0
```

## Autoridade

```text
ENV04 = PASS
P2_GATES_EXECUTED = false
P2_RESOLVER_V3_EXECUTED = false
P2_R5_CREATED_AT_TIME_OF_ENV04 = false
REPO_MUTATION = false
POLICY_CHANGED = false
B0_SHARED_MECHANISM_CHANGED = false
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

ENV-04 autoriza apenas a criação de uma rodada P2 sucessora usando o venv já provisionado. Não transporta PASS para nenhum gate P2.
