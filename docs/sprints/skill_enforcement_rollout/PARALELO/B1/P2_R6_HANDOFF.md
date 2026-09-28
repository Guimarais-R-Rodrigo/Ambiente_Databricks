# P2 R6 — modelo de identidade do interpretador corrigido

R6 sucede R5 e não reaproveita seu round/output.

Prepare exige:

`--python-launcher <ENV04_VENV_PYTHON>`

O release schema é `SER-B1-RELEASE-SPEC-2` e o handoff é `SER-B1-HANDOFF-2`.

O launcher autorizado e o runtime físico observado podem ter paths diferentes sob virtualização Codex. Essa diferença só é aceita se:
- probe direto do launcher selecionar o mesmo runtime observado;
- SHA-256 do launcher = SHA-256 do runtime;
- versão/implementação/isolamento coincidirem;
- o adapter reobservar o mesmo runtime físico e hashes antes da campanha.

`execution_argv[0]` e `post_run_package_argv[0]` devem ser o launcher literal autorizado, não o path redirecionado.

R6 mantém 2/1, read-only, uma tentativa por gate, sem policy/promoção/Ready/merge.
