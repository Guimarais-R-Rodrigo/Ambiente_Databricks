# SE02 — checkpoint

## Veredito atual

**CANDIDATA L2 EM RECONCILIAÇÃO LOCAL-FIRST / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE02 implementa exclusivamente L2 (`Preflight`) para `hub-ml-eda-profissional`. O contrato permanece `mode="audit"`; SE03, runner determinístico, `ExecutionTraceV0`, Execution Receipt formal e postflight não foram iniciados.

A partir de 2026-09-17, a frente segue a revisão `../REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`.

## Estados separados de certificação

```text
LOCAL_CERTIFICATION        = NOT_RUN_NO_HEAD_CORRIGIDO
SYNTHETIC_AGENT_SCREENING = MIXED
DATABRICKS_FREE            = NOT_RUN
GITHUB_ACTIONS             = DEFERRED_CREDIT
FULLY_CERTIFIED            = false
```

O HEAD `df240d056ca9b51318c6100c823eb40f6b42741d` recebeu a primeira certificação local completa em Windows 11 / Python 3.12.10. O resultado foi **FAIL**, preservado como evidência histórica:

- contrato v0.1: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02: 22/22 PASS;
- validação estrutural: FAIL porque `resource_resolution.py` era um segundo módulo `.py` na pasta de objeto `hub_scripts/skill_execution`;
- renderer: PASS, 556 arquivos;
- `render_diff`: FAIL / `DERIVED_STALE=true`;
- snapshot README: FAIL em cascata pela estrutura inválida e métricas stale;
- resumo: `LOCAL_CERTIFICATION=FAIL`, 3 steps reprovados (`assistant_structure`, `render_diff`, `readme_snapshot`).

Esse failure não é reclassificado como PASS. Ele demonstrou que a suíte funcional estava verde, mas a candidata violava a forma canônica do Hub.

## Correção arquitetural após a primeira certificação

A resolução estática compartilhada L1/L2 permanece única, mas passa a viver como funções puras dentro do módulo canônico `hub_scripts/skill_execution/skill_execution.py`.

Isso preserva simultaneamente:

- a mesma semântica L1/L2 para `__all__`, module path e símbolo público;
- ausência de import/execução dos helpers analíticos alvo;
- a regra do Hub de um módulo principal por pasta de objeto;
- a API pública `hub_scripts.skill_execution.run_preflight`;
- os 22 casos da suíte SE02.

O arquivo peer `resource_resolution.py` foi removido da fonte. O validador L1 passa a reutilizar as funções puras do próprio módulo canônico `skill_execution.py`.

## Próximo gate local

O HEAD corrigido precisa de nova certificação; nenhum resultado de `df240d0` é promovido automaticamente.

Antes de puxar a correção, descartar somente o derivado produzido pelo renderer da rodada reprovada e preservar qualquer outro trabalho local. Depois:

```powershell
git fetch origin --prune
git switch sef/SE02-preflight
git pull --ff-only origin sef/SE02-preflight
git status --short
python -B tools/skill_enforcement/certify_local.py --profile se02 --verbose
```

O objetivo é que a validação estrutural deixe de apontar módulo extra. O renderer ainda pode produzir um delta legítimo em `Novo_Ambiente_Simulado`; esse delta só deve ser versionado depois de revisado e após todos os gates estruturais anteriores passarem.

## Limites preservados

- `mode="audit"`;
- sem runner determinístico;
- sem `ExecutionTraceV0` funcional;
- sem Execution Receipt formal;
- sem postflight;
- sem `mode="enforce"`;
- sem promoção corporativa;
- `.assistant_instructions.md` não alterado;
- SE03 não iniciada;
- sem merge sem aceite explícito.
