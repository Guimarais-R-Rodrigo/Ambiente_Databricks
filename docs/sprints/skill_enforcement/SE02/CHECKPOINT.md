# SE02 — checkpoint

## Veredito atual

**CANDIDATA L2 EM RECONCILIAÇÃO LOCAL-FIRST / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE02 implementa exclusivamente L2 (`Preflight`) para `hub-ml-eda-profissional`. O contrato permanece `mode="audit"`; SE03, runner determinístico, `ExecutionTraceV0`, Execution Receipt formal e postflight não foram iniciados.

A partir de 2026-09-17, a frente segue a revisão `../REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`.

## Estados separados da candidata corrente

```text
LOCAL_CERTIFICATION        = NOT_RUN
SYNTHETIC_AGENT_SCREENING = MIXED
DATABRICKS_FREE            = NOT_RUN
GITHUB_ACTIONS             = DEFERRED_CREDIT
FULLY_CERTIFIED            = false
```

`LOCAL_CERTIFICATION=NOT_RUN` refere-se ao HEAD **corrigido depois** da primeira rodada local. O failure do HEAD anterior permanece registrado abaixo e não é apagado nem promovido.

## Primeira certificação local — HEAD `df240d056ca9b51318c6100c823eb40f6b42741d`

Ambiente observado: Windows 11, Python 3.12.10.

Resultado real:

- contrato v0.1: PASS, 1/1;
- regressão SE01: PASS, 14/14;
- suíte SE02: PASS, 22/22;
- validação estrutural: FAIL;
- renderer canônico: PASS, 556 arquivos;
- `render_diff`: FAIL, `DERIVED_STALE=true`;
- snapshot README: FAIL;
- resumo do certifier: `LOCAL_CERTIFICATION=FAIL`, 3 steps reprovados (`assistant_structure`, `render_diff`, `readme_snapshot`).

A causa primária da validação estrutural foi objetiva:

```text
.assistant\hub_scripts\skill_execution: módulo extra na pasta do objeto (resource_resolution.py)
```

O renderer e o snapshot foram executados depois desse achado pelo desenho atual do certifier e refletiram a mesma candidata inválida/stale. Eles não convertem a falha estrutural em outra coisa.

## Correção arquitetural

A resolução estática compartilhada L1/L2 permanece única, mas passa a viver como funções puras dentro do módulo canônico:

`ambiente_fonte/.assistant/hub_scripts/skill_execution/skill_execution.py`

O validador L1 reutiliza essas funções do próprio módulo principal. O arquivo peer `resource_resolution.py` é removido.

A correção preserva:

- uma única semântica para `__all__`, module path e símbolo público;
- ausência de import/execução dos helpers analíticos alvo durante resolução;
- a regra de um módulo principal por pasta de objeto;
- a API pública `hub_scripts.skill_execution.run_preflight`;
- a suíte SE02 de 22 casos;
- `mode="audit"`.

## Próximo gate local

A candidata corrigida precisa ser executada do zero; nenhum PASS parcial de `df240d0` é herdado automaticamente.

Antes de atualizar o clone, descartar **somente** o delta derivado produzido pelo renderer da rodada reprovada em `Novo_Ambiente_Simulado/`. Depois:

```powershell
git fetch origin --prune
git switch sef/SE02-preflight
git pull --ff-only origin sef/SE02-preflight
git status --short
python -B tools/skill_enforcement/certify_local.py --profile se02 --verbose
```

Critérios imediatos da próxima rodada:

1. `assistant_structure` não pode voltar a acusar módulo extra em `skill_execution`;
2. contrato, SE01 e os 22 testes SE02 devem continuar verdes;
3. se o renderer produzir somente o delta mecânico esperado, registrar `DERIVED_STALE` até materializá-lo canonicamente;
4. métricas do README só podem ser atualizadas a partir da saída real do validador;
5. somente depois seguir para `ci_local.py`, publicação/verify no Free e F02.

## Limites preservados

- sem runner determinístico;
- sem `ExecutionTraceV0` funcional;
- sem Execution Receipt formal;
- sem postflight;
- sem `mode="enforce"`;
- sem promoção corporativa;
- `.assistant_instructions.md` não alterado;
- SE03 não iniciada;
- sem merge sem aceite explícito.
