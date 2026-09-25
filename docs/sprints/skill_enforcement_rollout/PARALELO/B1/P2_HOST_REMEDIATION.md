# P2 — remediação ambiental Windows antes da próxima rodada

## Estado de entrada

Esta etapa NÃO é uma campanha P2 e não altera o resultado das rodadas anteriores.

```text
R1 = FAIL_PREPROCESS
R2 = BLOCKED_ENVIRONMENT
R3 = BLOCKED_BOOTSTRAP_DEFECT
R4 = BLOCKED_ENVIRONMENT_PYTHON3_NOT_RESOLVED

P2_FORMAL_GATES_EXECUTED_SINCE_R1 = 0
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
POLICY_CHANGED = false
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

## Objetivo

Provisionar fora do repositório um runtime CPython utilizável e um ambiente virtual dedicado aos gates locais.

O repositório possui histórico de execução em Python 3.11, 3.12 e 3.13. Para esta remediação, usar a série CPython 3.13 estável corrente, que mantém compatibilidade próxima das execuções locais 3.13 já observadas e possui distribuição Windows oficial atual.

Não instalar pacotes globais no runtime base além do necessário para criar o venv.

## Autoridade das dependências

Após criar o venv, instalar o arquivo já versionado:

`tools/requirements-dev.txt`

Esse arquivo declara explicitamente que contém as dependências para rodar o gate local em checkout limpo e referencia `requirements-temas-dev.txt`.

Não usar `requirements-optional.txt` inteiro: ele é inventário de dependências opcionais do runtime de produto e contém combinações/pins específicos do Databricks, não é o requirements do gate local.

## Sequência ENV-01

1. Confirmar Windows + NTFS e worktree limpo.
2. Confirmar que a etapa está fora de qualquer round P2.
3. Instalar o Python Install Manager oficial, preferencialmente por WinGet.
4. Consultar o índice online para o tag `3.13`.
5. Instalar explicitamente o runtime `3.13`.
6. Resolver o executável real por `py list --one --format=exe 3.13`.
7. Provar `sys.executable`, versão e arquitetura.
8. Criar venv dedicado fora do repositório.
9. Usar exclusivamente o Python do venv para instalar `tools/requirements-dev.txt`.
10. Rodar apenas smoke ambiental: import de numpy/pandas/sklearn/plotly/jinja2/yaml/regex e leitura das versões.
11. Não executar preflight P2, metatestes P2 ou campanha durante ENV-01.
12. Verificar que o repositório terminou clean.

## Critério de saída

```text
ENV01 =
PASS

python_series =
3.13

venv =
OUTSIDE_REPOSITORY

repo_mutation =
false

P2_GATES =
NOT_RUN
```

Após ENV-01 PASS, abrir uma nova rodada P2 em SHA posterior que registre a remediação e use o resolver V3. Não reaproveitar R4.
