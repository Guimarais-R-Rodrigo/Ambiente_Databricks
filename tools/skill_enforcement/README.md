# Skill Enforcement — ferramentas

Ferramentas de desenvolvimento do Skill Enforcement Framework (SEF). Este diretório pertence ao repositório e **não é publicado como parte do Hub**.

A estratégia vigente é local-first: testes e validações determinísticas rodam localmente durante desenvolvimento; GitHub Actions é reservado para release candidate/Ready-for-review e pós-merge.

## SE01 — contrato verificável

Validação estática:

```powershell
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/validate_contracts.py --json
```

O validador lê o contrato, resolve módulos sob `ambiente_fonte/.assistant/`, inspeciona fachadas públicas por AST e confere templates relativos sem executar helpers analíticos.

## SE02 — preflight L2

Implementação publicada:

```text
ambiente_fonte/.assistant/hub_scripts/skill_execution/skill_execution.py
```

Fachada:

```python
from hub_scripts.skill_execution import run_preflight
```

Acionador fino da skill piloto:

```text
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/preflight.py
```

Testes:

```powershell
python -B tools/tests/test_skill_enforcement_se01.py
python -B tools/tests/test_skill_enforcement_se02.py -v
```

## SE03 — entrypoint estrutural L3

Runner da skill piloto:

```text
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/run.py
```

Ele verifica release, deriva provenance runtime, reutiliza o preflight, chama a primitive protegida `quick_profile` e produz `ExecutionTraceV0`.

Regressão:

```powershell
python -B tools/tests/test_skill_enforcement_se03.py -v
```

Os resultados comportamentais históricos E02/E12 pertencem à documentação SE03 e não são reclassificados pela SE04.

## SE04 — Execution Receipt formal

Engine publicada:

```text
ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt.py
```

Responsabilidades:

- serialização JSON canônica;
- `ExecutionReceiptV1`;
- bindings SHA-256 a trace/input/output;
- binding à release/contract/runner;
- distinção entre recurso chamado e concluído;
- verificação `VALID`/`ABSENT`/`MALFORMED`/`INVALID`/`INCOMPATIBLE`/`STALE_REPLAYED`/`UNSUPPORTED_VERSION`.

Testes dedicados:

```powershell
python -B tools/tests/test_skill_enforcement_se04.py -v
python -B tools/tests/test_skill_enforcement_se04_runner.py -v
```

O Receipt é evidência verificável. Ele **não** implementa o postflight fail-closed da SE05.

## Certificação local reproduzível

Entry points:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se02
python -B tools/skill_enforcement/certify_local.py --profile se03
python -B tools/skill_enforcement/certify_local.py --profile se04
```

O perfil `se04` executa:

1. contrato v0.1;
2. regressão SE01;
3. regressão SE02;
4. regressão SE03;
5. suíte do Receipt SE04;
6. suíte de integração runner/Receipt;
7. validação estrutural;
8. renderer canônico;
9. render-diff incluindo untracked;
10. snapshot README.

Por padrão o certifier exige worktree limpo antes de qualquer step mutável. O evidence bundle fica fora do repositório em:

```text
~/.ambiente_databricks/sef_certifications/<timestamp>_<sha>/
```

Exemplo de destino explícito:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se04 --evidence-dir C:\temp\sef-se04
```

A execução continua após failures para revelar achados adicionais; qualquer step reprovado mantém exit code final diferente de zero.

### Subgate do CI local

`tools/ci_local.py` pode chamar o certifier em modo parcial/read-only com `--skip-render --no-evidence --allow-dirty`. Esse subgate **não substitui** `FULL_SE04_LOCAL`, porque não prova renderer/diff.

## Probes do Databricks Free

- `se02_free_probe.py`: preflight L2;
- `se03_free_probe.py`: entrypoint/trace L3;
- `se04_free_probe.py`: Receipt formal e adversarial cases.

O probe SE04 usa somente view temporária sintética e cobre Receipt válido, tampering, stale run, manual/direct helper sem Receipt, release integrity em fixture temporária, provenance conflict e primitive failure sem fallback.

Runbook:

```text
docs/sprints/skill_enforcement/SE04/RUNBOOK_FREE.md
```

Preparar o probe não equivale a `DATABRICKS_FREE=PASS`; o estado só muda depois de execução real e evidência preservada.

## GitHub Actions

Actions permanece gate remoto final, não instrumento de desenvolvimento iterativo. Quando runners/créditos impedirem qualquer step de executar, use `GITHUB_ACTIONS=DEFERRED_CREDIT`, nunca PASS. Não faça rerun automático para contornar crédito.

## Limites vigentes

- `mode="audit"` continua vigente;
- SE04 permanece restrita à skill piloto e à primitive protegida atual;
- SHA-256 fornece tamper evidence/binding, não autenticação com segredo;
- não há postflight universal;
- SE05 não foi iniciada;
- nenhum estado `NOT_RUN` ou `DEFERRED_CREDIT` pode ser tratado como `FULLY_CERTIFIED`.
