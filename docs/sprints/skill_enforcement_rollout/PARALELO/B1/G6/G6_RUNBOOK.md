# B1 G6 — runbook externo congelável (NÃO AUTORIZADO)

## Estado

```text
R7_QUALIFIED_SHA = 08c2a93c4c9dede1e759abe28c07242b4116f47e
R7_QUALIFIED_TREE = a2b1b8c805044ff2e1898da3190414afab9140a7
G4_LOCAL_CERTIFICATION = PASS
G5_AUDIT = PASS
G6_EXECUTION = NOT_AUTHORIZED
```

Este runbook prepara a execução externa, mas não concede autorização.

## 1. Freeze local obrigatório antes de G6

No SHA de autoria G6, executar localmente:
1. `python -B -m tools.skill_enforcement.real_campaigns.b1.g6.validate_package`;
2. `python -B -m unittest tools.tests.test_ser_b1_g6_external -v`;
3. confirmar `git diff 08c2a93c4c9dede1e759abe28c07242b4116f47e..HEAD -- ambiente_fonte Novo_Ambiente_Simulado/Users/usuario-free/.assistant` vazio;
4. confirmar worktree clean;
5. registrar SHA/tree do pacote G6.

Nenhum PASS R7 é transportado ao novo SHA; a condição necessária é que os bytes do produto permaneçam idênticos ao SHA R7 qualificado.

## 2. G6-READ — reconciliação externa somente leitura

Somente após autorização para operações read-only no workspace pessoal Free:
- `databricks auth describe -o json`;
- `databricks current-user me -o json`;
- confirmar host/profile pessoal e não corporativo;
- executar `tools/publicar_free.py --verify --conteudo` com profile/host explícitos;
- preservar relatório literal.

Se o pacote remoto já corresponder ao produto local, NÃO republicar.

Se houver mismatch, parar. Publicação é efeito remoto separado e exige autorização específica.

## 3. G6-PUBLISH — somente se necessário e explicitamente autorizado

A sequência autorizável é:
- dry-run do publicador;
- uma única execução `--execute`;
- verify rápido;
- verify completo;
- verify por conteúdo.

Falha de transporte com efeito possivelmente criado não recebe retry. Fazer apenas reconciliação read-only.

## 4. G6-PROBE-IMPORT — efeito temporário separado

Os probes externos são:
- `tools/skill_enforcement/real_campaigns/b1/g6/ser03_free_probe.py`;
- `tools/skill_enforcement/real_campaigns/b1/g6/ser05_l2_free_probe.py`.

Antes de importar:
- resolver usuário pessoal;
- escolher diretório novo, SHA-bound, sob `/Users/<user>/ser-b1-g6-tests/08c2a93c4c9d`;
- confirmar via get-status/list que os destinos não existem.

Importar uma vez cada, exportar de volta e comparar conteúdo normalizado. Não usar overwrite sobre objeto existente.

A criação dos probes é efeito `TEMPORARY_WORKSPACE_OBJECT_CREATE`; não está coberta por autorização read-only.

## 5. Execução Free

Cada probe é executado Run all UMA vez. Preservar JSON literal completo e run/notebook ID quando exposto.

SER03 exige:
- cumulative real core PASS;
- event real core PASS;
- Receipt/verifier válidos;
- ausência/maturidade preservadas;
- monetary estimand bloqueado;
- release unchanged;
- policy pré-promoção.

SER05 L2 exige:
- temporal context PASS;
- static NOT_APPLICABLE context PASS;
- variable lag/bitemporal/timezone negativos bloqueados;
- release bindings exatos;
- join_executed=false;
- coverage_measured=false;
- ml_readiness=NOT_EVALUATED;
- protected bytes unchanged;
- policy pré-promoção.

Após os probes, executar verify por conteúdo novamente. Não republicar.

## 6. Genie

Usar `genie_manifest.json`.

Há 8 case_ids canônicos por skill e 10 variantes congeladas por skill. Cada variante usa chat novo. Preservar primeiro resultado literal.

Não preencher evidência antes da execução. `NOT_OBSERVABLE` permanece válido quando a UI não expuser indicador.

Os três eixos permanecem separados:
- TASK_CORRECTNESS;
- AGENT_ADHERENCE;
- CANONICAL_COMPLIANCE.

## 7. Cleanup opcional pós-evidência

Não apagar os notebooks temporários antes de preservar:
- output literal;
- export do probe;
- IDs observáveis;
- verify de conteúdo pós-probe;
- evidência necessária à auditoria.

A remoção dos dois notebooks SHA-bound é um efeito separado `TEMPORARY_WORKSPACE_OBJECT_DELETE` e exige autorização específica posterior. Ausência dessa autorização deixa os objetos temporários presentes; não converte G6 em FAIL.

## 8. Encerramento

G6 PASS por skill exige somente as claims externas congeladas e observáveis. Resultado correto sem prova de rota não prova chamada; rota observada sem resultado correto não prova domínio.

Nenhuma saída de G6 altera policy ou promove skill automaticamente.
