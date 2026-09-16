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

No HEAD `e99b5ee6557bd8898c22986a2d1627f4942d132a`, os workflows funcionais e estruturais passaram, mas dois gates transversais detectaram pendências reais de governança:

1. `CI local reproduzível`, run `35148514349`: 8/9 etapas PASS; a única falha foi `ManualTecnicoTests.test_manual_inventory_covers_current_objects`, porque `hub_scripts.skill_execution` ainda não constava do Manual Técnico.
2. `Integração transversal V08`, run `35148514303`: 22 testes V08 PASS, regressão global de temas com 741 testes e zero failure funcional, compatibilidade visual PASS e snapshot PASS; a única falha foi o guard histórico `V08_RUNTIME_EDIT_FORBIDDEN`, que aplicava a proibição própria da V08 a qualquer evolução posterior em `hub_scripts`.

Nenhuma dessas duas falhas foi reclassificada como PASS.

## Correção transversal V08

O guard V08 foi corrigido fora da SE02 pela PR #75, com diff de um único workflow e sem alteração de produto. A regra continua fail-closed na própria frente `codex/temas-v08*`, mas fica `skipped` em `main` integrada e em iniciativas posteriores.

A PR #75, HEAD `72267f64c939a078a67ea7e0a192b622d6d305e1`, foi certificada com V00, V01, V02, `CI local reproduzível` e V08 em SUCCESS e integrada por squash na `main` em `ae9337204a7c769c0b28b33321c8b81afdff6bae`.

A branch SE02 foi reconciliada por merge normal, sem force-push, no commit `3fe1078e743f7e317d3a814d85d321d7b6f45d85`; após isso, `behind_by=0`.

## Reconciliação documental

A dívida documental pós-SE01 e o inventário criado pela SE02 foram reconciliados de forma aditiva/ancorada:

- Plano Mestre: SE00/SE01 integradas, SE02 em andamento, SE03–SE08 não iniciadas;
- Manual Técnico fonte: entrada `hub_scripts.skill_execution`;
- Manual Técnico raiz: cópia byte a byte da fonte;
- `hub_scripts/README.md`: oitavo objeto e catálogo do preflight;
- `skills/README.md`: EDA passa a listar `hub_scripts.skill_execution` entre os helpers recomendados.

A primeira tentativa de manutenção documental, run `35149060047`, aplicou os patches em memória mas falhou na própria guarda de conferência por `NameError: Path is not defined`; nenhum commit foi produzido. A correção adicionou apenas o import ausente. A segunda tentativa concluiu todos os steps em `success` e produziu o commit `a8c4284e6f8974e133bcf9c6866668fedb18a879`, removendo o workflow transitório.

Como esses documentos fonte também pertencem ao pacote publicado, o simulado foi rematerializado novamente pelo renderer. O workflow transitório `SE02 Rematerialize Docs`, run `35149573372`, conferiu que somente os três documentos derivados esperados mudaram e concluiu todos os steps em `success`, produzindo o commit `05017ad8fe60c7477d9fc20217e422efa5a0f1c1` e removendo a automação transitória.

## Evidência pendente

Ainda faltam a certificação completa da árvore documental/rematerializada, o snapshot definitivo pós-documentação, publicação/verify no Databricks Free, testes `PASS`/`BLOCKED` no Free, teste conversacional do Genie Code, CHANGELOG final e CI completo da candidata de fechamento.
