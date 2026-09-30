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

## SE06 — benchmark/adversarial ampliado

A SE06 mede o produto integrado da SE05 sem alterar o runtime.

Especificação:

```text
docs/testes/skill_execution/se06_cases.json
```

Ferramenta:

```powershell
python -B tools/skill_enforcement/se06_eval.py --validate-spec
```

Criar bundle externo de coleta:

```powershell
python -B tools/skill_enforcement/se06_eval.py --validate-spec --init-results C:\temp\se06-results.json
```

Scoring final:

```powershell
python -B tools/skill_enforcement/se06_eval.py `
  --results C:\temp\se06-results.json `
  --certification-summary C:\temp\se06-cert\summary.json `
  --summary-out C:\temp\se06-summary.json
```

A ferramenta não chama Databricks e não executa chats; ela valida matriz, evidence bundle e DoD.

Testes:

```powershell
python -B tools/tests/test_skill_enforcement_se06.py -v
```

A suíte cobre 12 variantes estruturais e o scorer da coleta comportamental.

## SE07 — generalização por risco

Registry publicado:

`ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json`

Validação:

```powershell
python -B tools/skill_enforcement/se07_policy.py
python -B tools/tests/test_skill_enforcement_se07.py -v
```

O registry corrente cobre exatamente 15/15 skills após a reconciliação MM04 e separa `current_level` de `target_level`. O validator impede que uma skill alegue L1–L4 sem os artifacts mínimos correspondentes.

## SE08 — operação permanente

A SE08 incorpora o SEF aos gates permanentes do repositório sem promover níveis
por conveniência. O validador geral executa os checks estáticos de contratos e
policy; o `ci_local.py` chama o perfil cumulativo `se08` em modo parcial,
read-only e sem renderer; a certificação FULL usa o mesmo perfil sem essas
dispensas.

Regressões específicas:

```powershell
python -B tools/tests/test_skill_enforcement_policy_io.py -v
python -B tools/tests/test_skill_enforcement_se08.py -v
```

A suíte de I/O garante que a policy é lida/parseada uma única vez e que resumo e
veredito descrevem o mesmo snapshot. A suíte operacional protege integração com
validator/CI, o guardrail do publicador Free e a permanência de
`hub-ml-criar-objeto` em L2 global.

SE08 não transforma gate local em evidência de Free/Genie e não autoriza
promoção ao workspace do trabalho. O gate corporativo e o rollback permanecem
documentados separadamente.

## Certificação local reproduzível

Entry points:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se02
python -B tools/skill_enforcement/certify_local.py --profile se03
python -B tools/skill_enforcement/certify_local.py --profile se04
python -B tools/skill_enforcement/certify_local.py --profile se05
python -B tools/skill_enforcement/certify_local.py --profile se06
python -B tools/skill_enforcement/certify_local.py --profile se07
python -B tools/skill_enforcement/certify_local.py --profile se08
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

O perfil `se06` acrescenta `test_skill_enforcement_se06.py` ao conjunto SE05 e preserva os mesmos gates de estrutura, renderer, render-diff e snapshot. O perfil `se07` acrescenta o validador do registry e `test_skill_enforcement_se07.py`, mantendo todas as regressões anteriores. O perfil `se08` acrescenta `test_skill_enforcement_policy_io.py` e `test_skill_enforcement_se08.py`, preservando o restante da cadeia e os gates finais de renderer/diff/snapshot.

Por padrão o certifier exige worktree limpo antes de qualquer step mutável. O evidence bundle fica fora do repositório em:

```text
~/.ambiente_databricks/sef_certifications/<timestamp>_<identidade-ou-unknown>_<uuid>/
```

Exemplo de destino explícito:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se05 --evidence-dir C:\temp\sef-se05
```

A execução continua após falhas ordinárias de gates; timeout, interrupção ou falha de infraestrutura interrompem a sequência e registram os steps não iniciados. Qualquer falha impede sucesso. O diretório de evidência deve ser novo e externo, mesmo quando vazio. O SE07 inclui a suíte do certifier.

F-04 acrescenta limites finitos por processo, observação Git obrigatória e identidade final estável. Detalhes, opções, campos aditivos e limites: [F04_D10.md](../../docs/sprints/skill_enforcement/SE07/F04_D10.md).

### Subgate do CI local

`tools/ci_local.py` pode chamar o certifier em modo parcial/read-only com `--skip-render --no-evidence --allow-dirty`. Esse subgate **não substitui** a certificação FULL da sprint selecionada, porque não prova renderer/diff.

## Probes do Databricks Free

- `se02_free_probe.py`: preflight L2;
- `se03_free_probe.py`: entrypoint/trace L3;
- `se04_free_probe.py`: Receipt formal e adversarial cases;
- `se05_free_probe.py`: evidência histórica da autorização L4 original da SE05;
- `se06_correction_free_probe.py`: candidata corrigida após o early-stop P1, cobrindo contexto mínimo, PK opcional, fail-fast e finalizer estrito.

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
- desde a calibração SE06, `data_quality_check` é condicional à existência de `pk_columns` explicitamente estabelecidas; ausência de PK não autoriza inferi-la nem bloqueia os demais recursos da EDA;
- `run_enforced` aplica contexto profissional padrão quando o caller omite flags condicionais e, em modo estrito, levanta `CanonicalExecutionBlocked` quando a rota não fica em PASS;
- `finalize_or_raise` transforma ausência de autorização de completion em falha explícita;
- nenhum estado `NOT_RUN`, `BLOCKED` ou `DEFERRED_CREDIT` pode ser tratado como `FULLY_CERTIFIED`.

## SER — certificação prospectiva

O Skill Enforcement Rollout não reescreve `certify_local.py` nem os perfis históricos
SE01-SE08. O certifier prospectivo vive em:

```text
tools/skill_enforcement/ser_certify.py
```

Perfil inicial:

```powershell
python -B tools/skill_enforcement/ser_certify.py `
  --profile ser01-object-validation-pre-promotion `
  --evidence-dir C:\temp\ser01-object-validation `
  --evidence-authorized
```

`SER-CERT-1` exige worktree limpa/reconciliada, contrato/SKILL/manifest coerentes,
records e Receipts reais, bypass mínimo fechado, regressões, renderer sem drift,
snapshot e CI. O FULL SE08 é executado como canal histórico separado. O certifier
não autentica pessoas, não muda policy e não autoriza merge/promoção sozinho.

### SER01 A4 — probe Free de `object_validation`

Instrumento externo:

```text
tools/skill_enforcement/ser01_free_probe.py
```

O probe resolve a `.assistant` publicada, verifica o release manifest de `hub-ml-criar-objeto`, confirma que a primitive repo-side não é artifact publicado, executa o verifier com fixture sintética de integridade e testa ausência de `local_record`, Receipt ausente, tamper/replay e policy pré-promoção. Não executa a primitive repo-side, não escreve no produto e não transforma a fixture em prova de execução.

Runbook: `docs/sprints/skill_enforcement_rollout/SER01/A4_RUNBOOK_FREE.md`.
