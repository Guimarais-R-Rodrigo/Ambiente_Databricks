# SE02 — resultados

## Estado

Registro vivo da sprint. Nenhum resultado abaixo deve ser promovido de intenção para evidência sem execução observável.

## Baseline

- `main` de abertura: `4ef1f8b927f1ba706076a2c330c74d66e44a1b3f`;
- SE01 integrada pela PR #69;
- ADR-0021: Aceito;
- contrato v0.1 em `mode="audit"`;
- SE03 não iniciada.

## Implementação inicial

Criados na branch SE02:

- `hub_scripts.skill_execution` com `run_preflight`;
- fachada pública gerada pelo contrato `api_publica.py`;
- README e exemplo do novo objeto;
- `skills/hub-ml-eda-profissional/scripts/preflight.py`;
- instrução mínima de preflight no `SKILL.md`;
- suíte `test_skill_enforcement_se02.py`;
- workflow dedicado `Skill Enforcement SE02`;
- documentação da sprint.

## Decisões da implementação

1. `mode="audit"` permanece inalterado.
2. O preflight não importa helpers analíticos; inspeciona a fachada pública por AST.
3. Condição sem contexto explícito bloqueia, em vez de assumir `false`.
4. Optional ausente não bloqueia.
5. `BLOCKED` encerra o gate canônico, mas a resistência real do Genie Code a bypass precisa ser medida no Free.
6. O script da skill é um acionador fino; a lógica canônica vive em `hub_scripts.skill_execution`.

## Primeira rodada executável — histórico

No run inicial `35147659671`:

- contrato v0.1: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02: 18/18 PASS;
- validação estrutural: FAIL por quatro convenções do novo objeto, sem failure da lógica do preflight.

Os quatro achados foram corrigidos sem mudar a semântica L2:

- módulo principal passou a se chamar `skill_execution.py`, igual à pasta;
- `__init__.py` passou a seguir `tools/api_publica.py`;
- README passou a apontar o módulo canônico;
- exemplo recebeu bloco `text` conferível, explicitamente delimitado como evidência automatizada e não como captura do Free.

Na rodada seguinte, run `35148053257`:

- contrato v0.1: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02: **18/18 PASS**;
- validação estrutural: PASS após o alinhamento final da API pública;
- renderer canônico: PASS;
- artifact `se02-preflight-renderizado`: publicado;
- diff do derivado: FAIL esperado porque a branch ainda não havia materializado a saída do renderer.

O artifact canônico foi baixado e conferido. A materialização foi feita pelo próprio `tools/render_simulado.py --write` no workflow transitório `SE02 Materialize Simulado`, run `35148184892`, com guarda que restringiu o diff aos dois diretórios derivados da SE02. Todos os steps desse workflow concluíram `success`, e o workflow transitório foi removido no mesmo commit `056c0fca8890777cb8d3e2ed78d964882a80e2ee`.

Os runs disparados diretamente por esse commit automático ficaram `action_required`/sem jobs por terem sido originados pelo próprio GitHub Actions. Isso é classificado como efeito de infraestrutura/identidade do push, não como PASS nem como regressão funcional.

## Snapshot e CI intermediário

No run `35148293591`, já sobre o derivado materializado:

- contrato: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02: 18/18 PASS;
- validação estrutural: PASS — 0 falhas / 0 avisos;
- renderer: 555 arquivos;
- artifact: PASS;
- derivado sem diff: PASS;
- snapshot: FAIL exclusivamente porque 14 métricas do README ainda refletiam a baseline SE01.

As métricas medidas nessa árvore foram: 93 helpers citados, 223 Markdown/1401 links, 81 notebooks/102 links, 77/77 objetos documentados, 63 pastas de objeto, 61 módulos com forma canônica, 225 arquivos Python e 1516 arquivos / 1985 links globais. A atualização foi aplicada por âncoras exatas e sem inventar contagens.

## Primeira certificação local no regime local-first

No HEAD `df240d056ca9b51318c6100c823eb40f6b42741d`, em Windows 11 / Python 3.12.10, o novo `certify_local.py` foi executado integralmente.

Resultados observados:

- contrato v0.1: PASS, 1/1;
- regressão SE01: PASS, 14/14;
- suíte SE02 ampliada: PASS, 22/22;
- validação estrutural: FAIL;
- renderer: PASS, 556 arquivos;
- `render_diff`: FAIL, `DERIVED_STALE=true`;
- snapshot README: FAIL;
- resumo final: `LOCAL_CERTIFICATION=FAIL`, com `assistant_structure`, `render_diff` e `readme_snapshot` reprovados.

A falha estrutural foi precisa: `resource_resolution.py` era um segundo módulo `.py` dentro da pasta de objeto `hub_scripts/skill_execution`, violando a forma canônica que o próprio validador protege. Esse achado é atribuído ao desenho da candidata, não ao ambiente do usuário.

A correção seguinte consolida `canonical_module_parts`, `public_exports` e `resolve_public_symbol` no módulo principal `skill_execution.py`, mantendo uma única semântica L1/L2 e removendo o módulo peer. O validador L1 passa a reutilizar as funções puras do módulo canônico. A candidata corrigida exige nova certificação completa; 22/22 do HEAD anterior não aprova automaticamente o HEAD novo.

## Correção transversal V08 e reconciliação documental

O guard V08 foi corrigido fora da SE02 pela PR #75, integrada na `main@ae9337204a7c769c0b28b33321c8b81afdff6bae`. A branch SE02 foi reconciliada por merge normal, sem force-push e permanece `behind_by=0` na baseline dessa reconciliação.

Plano Mestre, Manual Técnico, catálogo `hub_scripts`, `skills/README.md`, revisão local-first, certifier, probe Free e runbook SE02 permanecem como superfícies vivas desta frente.

## Evidência pendente

Para a candidata corrigida ainda faltam:

- nova certificação local completa;
- materialização canônica do derivado correspondente;
- snapshot README reconciliado a partir da medição real;
- `ci_local.py --verbose`;
- publicação/verify no Databricks Free;
- probe Free P1/C1/B1;
- testes conversacionais F02-P1/F02-A1/F02-A2;
- fechamento documental;
- Actions finais quando aplicáveis;
- aceite humano e merge.
