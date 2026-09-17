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

Os resultados comportamentais históricos E02/E12 pertencem à documentação SE03 e não são reclassificados pelas sprints posteriores.

## SE04 — Execution Receipt formal

Engine publicada:

```text
ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt/__init__.py
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

O Receipt é evidência verificável. Isoladamente ele não autoriza conclusão L4.

## SE05 — postflight fail-closed L4

Componentes publicados:

```text
ambiente_fonte/.assistant/hub_scripts/skill_execution/postflight/__init__.py
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/run_enforced.py
ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/postflight.py
```

A rota L4 reutiliza `run.py::run`, coleta evidência adicional de imports, calls/completions e templates carregados, reemite o Receipt vinculando o trace enriquecido e só autoriza `completion.status=COMPLETED` quando `PostflightV1.status=PASS`.

O postflight valida:

- Receipt `VALID` contra a release corrente;
- binding da skill e do entrypoint L4;
- required resources e conditional resources aplicáveis;
- skips condicionais e justificativas;
- templates carregados e seus digests;
- integridade dos artifacts;
- handoff obrigatório;
- consistência de qualquer claim de conclusão.

Estados do postflight:

```text
PASS
FAIL
BLOCKED
REVIEW
```

Somente `PASS` pode produzir `completion_authorized=true`.

Testes:

```powershell
python -B tools/tests/test_skill_enforcement_se05.py -v
python -B tools/tests/test_skill_enforcement_se05_runner.py -v
```

## Certificação local reproduzível

Entry points:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se02
python -B tools/skill_enforcement/certify_local.py --profile se03
python -B tools/skill_enforcement/certify_local.py --profile se04
python -B tools/skill_enforcement/certify_local.py --profile se05
```

O perfil `se05` executa:

1. contrato v0.1;
2. regressão SE01;
3. regressão SE02;
4. regressão SE03;
5. Receipt SE04;
6. integração runner/Receipt SE04;
7. postflight SE05;
8. integração L4/Receipt/Postflight;
9. validação estrutural;
10. renderer canônico;
11. render-diff incluindo untracked;
12. snapshot README.

Por padrão o certifier exige worktree limpo antes de qualquer step mutável. O evidence bundle fica fora do repositório em:

```text
~/.ambiente_databricks/sef_certifications/<timestamp>_<sha>/
```

Exemplo de destino explícito:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se05 --evidence-dir C:\temp\sef-se05
```

A execução continua após failures para revelar achados adicionais; qualquer step reprovado mantém exit code final diferente de zero.

### Subgate do CI local

`tools/ci_local.py` pode chamar o certifier em modo parcial/read-only com `--skip-render --no-evidence --allow-dirty`. Esse subgate **não substitui** `FULL_SE05_LOCAL`, porque não prova renderer/diff.

## Probes do Databricks Free

- `se02_free_probe.py`: preflight L2;
- `se03_free_probe.py`: entrypoint/trace L3;
- `se04_free_probe.py`: Receipt formal e adversarial cases;
- `se05_free_probe.py`: autorização L4 e postflight fail-closed.

O probe SE05 usa somente view temporária sintética e cobre:

- happy path L4 com Receipt válido, Postflight PASS e conclusão autorizada;
- payload L3/SE04 sem L4, que não pode ser homologado como concluído;
- input obrigatório ausente (`pk_columns`), mantendo conclusão negada;
- handoff incompleto, classificado para revisão e sem conclusão;
- adulteração posterior do claim de conclusão;
- ausência de escrita persistente e de mutação do pacote publicado.

Runbook:

```text
docs/sprints/skill_enforcement/SE05/RUNBOOK_FREE.md
```

Preparar o probe não equivale a `DATABRICKS_FREE=PASS`; o estado só muda depois de execução real e evidência preservada.

## GitHub Actions

Actions permanece gate remoto final, não instrumento de desenvolvimento iterativo. Quando runners/créditos impedirem qualquer step de executar, use `GITHUB_ACTIONS=DEFERRED_CREDIT`, nunca PASS. Não faça rerun automático para contornar crédito.

## Limites vigentes

- `mode="audit"` continua vigente; a SE05 adiciona fail-closed de homologação, não muda silenciosamente o schema para `enforce`;
- a implementação continua restrita à skill piloto;
- SHA-256 fornece tamper evidence/binding, não autenticação com segredo;
- `run.py` continua o core L3 histórico; `run_enforced.py` é a rota L4 exigida para conclusão homologada;
- recursos sem entrada suficiente não recebem evidência fabricada e impedem PASS quando aplicáveis;
- nenhum estado `NOT_RUN`, `BLOCKED` ou `DEFERRED_CREDIT` pode ser tratado como `FULLY_CERTIFIED`.
