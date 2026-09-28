# P2 R5 — handoff após ENV-04 PASS

## Objetivo

R5 é a primeira rodada P2 posterior à remediação ambiental concluída.

Ela deve usar exclusivamente o Python do venv ENV-04:

`<LOCALAPPDATA>\AmbienteDatabricks\venvs\ser-b1-p2-py312-env04\Scripts\python.exe`

Não executar o resolver V3. Não usar `python`, `py` ou `pymanager` como launcher dos gates.

## Pré-condições ambientais

Antes de P2-R5-01, observar sem modificar:

- Windows;
- NTFS;
- venv acima presente;
- CPython 3.12.10;
- venv isolado;
- hashes de `tools/requirements-dev.txt` e `tools/requirements-temas-dev.txt` iguais aos observados em ENV-04;
- imports de numpy/pandas/sklearn/plotly/jinja2/yaml/regex funcionais;
- worktree clean.

Essas checagens não são gates P2 e não podem instalar/corrigir nada.

## Gates formais

Se as pré-condições acima passarem, executar uma única vez e fail-fast:

1. P2-R5-01: `-B -m tools.skill_enforcement.real_campaigns.b1.preflight`
2. P2-R5-02: `-B -m unittest tools.tests.test_ser_b1_campaign -v`
3. P2-R5-03: `-B -m tools.skill_enforcement.real_campaigns.b1.prepare --output-dir <external-new-dir>`
4. P2-R5-04: executar exatamente `execution_argv` do `HANDOFF.json`
5. P2-R5-05: executar exatamente `post_run_package_argv` da primeira tentativa

O `RELEASE_SPEC.python_executable` deve ser o executável do venv ENV-04.

## Limites

R5 continua:
- read-only no repo;
- 2 total / 1 auditor;
- sem policy change;
- sem promoção;
- sem Databricks Free/Genie;
- sem Ready/merge;
- sem retry-until-green.
