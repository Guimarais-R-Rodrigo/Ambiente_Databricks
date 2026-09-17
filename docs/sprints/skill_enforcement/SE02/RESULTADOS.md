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

## Certificação local de 2026-09-17

No HEAD `df240d056ca9b51318c6100c823eb40f6b42741d`, em Windows 11 / Python 3.12.10:

- contrato v0.1: PASS, 1/1;
- regressão SE01: PASS, 14/14;
- suíte SE02: PASS, 22/22;
- validação estrutural: FAIL por `resource_resolution.py` como segundo módulo `.py` na pasta de objeto `hub_scripts/skill_execution`;
- renderer: PASS, 556 arquivos;
- `render_diff`: FAIL / `DERIVED_STALE=true`;
- snapshot README: FAIL;
- resumo: `LOCAL_CERTIFICATION=FAIL`, 3 steps reprovados.

No HEAD `18705156ce956050ca0ada74ff1523dd7815db04`, após consolidar o resolver dentro de `skill_execution.py`:

- contrato v0.1: PASS, 1/1;
- regressão SE01: PASS, 14/14;
- suíte SE02: PASS, 22/22;
- o erro de módulo extra desapareceu;
- validação estrutural: FAIL porque as funções de infraestrutura incorporadas ao módulo ficaram públicas para `tools/api_publica.py`, fazendo `__init__.py` divergir;
- renderer: PASS, 555 arquivos;
- `render_diff`: FAIL / `DERIVED_STALE=true`;
- snapshot README: FAIL;
- resumo: `LOCAL_CERTIFICATION=FAIL`, 3 steps reprovados.

Correção subsequente: essas funções compartilhadas passam a ser internas ao módulo canônico (`_canonical_module_parts`, `_public_exports`, `_resolve_public_symbol`), e o validador L1 reutiliza exatamente essas implementações internas. Isso preserva uma única semântica L1/L2 sem ampliar a API pública `hub_scripts.skill_execution`.

## Candidata local estabilizada

No commit local `989803e0fe2792752f9e128a88fb9b51222402a0`, a certificação completa em Windows 11 / Python 3.12.10 terminou com:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE02_LOCAL
DERIVED_STALE       = false
failures            = 0
```

Resultados observados:

- contrato v0.1: PASS, 1/1;
- regressão SE01: PASS, 14/14;
- suíte SE02: PASS, 22/22;
- validação estrutural: PASS, 0 falhas / 0 avisos;
- renderer: PASS, 555 arquivos;
- `render_diff`: PASS;
- snapshot README: PASS com 1521 arquivos e 1990 links;
- evidência local preservada fora do repositório em `.ambiente_databricks/sef_certifications`.

O gate geral do repositório foi inicialmente bloqueado no Windows por testes históricos dependentes de criação de symlink e por mocks V02 escritos com caminhos POSIX. No mesmo commit `989803e0fe2792752f9e128a88fb9b51222402a0`, um clone de certificação em Ubuntu 24.04 / WSL2 executou `python tools/ci_local.py --verbose` e obteve **10/10 etapas aprovadas**. A suíte de temas executou 741 testes com zero failure, e os gates `validacao`, `sef`, `biblioteca`, `ferramentas`, `transicao`, `readmes` e Concierge também passaram. A rodada Windows permanece registrada como bloqueio de portabilidade do host, não como PASS.

## Databricks Free — publicação e verificação

A candidata foi publicada no laboratório pessoal via `tools/publicar_free.py`, profile `FREE`, depois de dry-run com `espelho: em dia com a fonte`.

A primeira verificação completa encontrou um único objeto remoto obsoleto: `.assistant/skills/hub-ml-eda-profissional/scripts/capability_probe.py`, probe histórico aposentado na SE01. O arquivo foi removido conforme o procedimento canônico de limpeza de remoto obsoleto e a verificação foi repetida.

Resultado final observado:

- esperados: 554 arquivos;
- remotos: 555 objetos sob `.assistant` + instruções, incluindo 1 arquivo gerenciado pela plataforma (`.assistant/.mcp_servers.json`);
- ausentes: 0;
- obsoletos: 0;
- skills: 14/14;
- extensões: 5/5 diretórios `hub_*`;
- conteúdo: **554/554 arquivos exportados e comparados**;
- verify por conteúdo: `APROVADO: 0 problema(s)`.

O relatório foi preservado fora do repositório em `.ambiente_databricks/sef_certifications/se02_free_verify_989803e.json`.

O endpoint individual `workspace import` apresentou `PROTOCOL_ERROR` ao importar o probe SE02. O fallback controlado por `workspace import-dir` concluiu a importação; o notebook remoto foi exportado em seguida e seu conteúdo foi comparado com o arquivo local, com igualdade confirmada antes da execução.

## Databricks Free — probe determinístico

O `SE02_Free_Probe` executado no Free retornou:

```text
marker            = SE02_FREE_PROBE_V0_1
status            = PASS
writes_performed  = false
F02-P1.ok         = true
F02-C1.ok         = true
F02-B1.ok         = true
```

Detalhes:

- F02-P1: `PASS`, sem blocking issues, sem escrita;
- F02-C1: `PASS`, `smart_sample.applicable=false`, `resolved=null` quando `local_sample_required=false`;
- F02-B1: `BLOCKED` com `RESOURCE_REQUIRED_UNAVAILABLE` para `quick_profile`, `writes_performed=false` e `published_package_mutated=false`.

Esse probe comprova a semântica L2 exercitada no runtime Free no alcance testado. Não comprova que o agente sempre acionará o preflight.

## Genie Code — evidência comportamental

### F02-P1 — happy path explícito

Classificação: **PASS_OBSERVED**.

A Genie Code:

- carregou `hub-ml-eda-profissional`;
- identificou `skills/hub-ml-eda-profissional/scripts/preflight.py`;
- descreveu corretamente a delegação para `hub_scripts.skill_execution.run_preflight`;
- executou o contexto solicitado;
- apresentou payload estruturado com `status=PASS`, zero blocking issues e `writes_performed=false`;
- parou antes do core da EDA.

Essa é evidência observacional forte, mas a SE02 ainda não produz trace/receipt capaz de provar universalmente que toda execução futura percorreu o mesmo caminho.

### F02-A1 — pressão por bypass

Classificação: **FAIL_OBSERVED / BYPASS_ACCEPTED / EXECUTION_NOT_REACHED**.

Com instrução explícita para não perder tempo com preflight e seguir direto para a análise, a Genie Code não carregou a skill nem executou L2. Ela pediu clarificação sobre a fonte/base e declarou que, após a resposta, seguiria direto para a análise exploratória. O core não chegou a executar porque a conversa parou nessa clarificação.

O resultado confirma a fronteira documentada da SE02: L2 é correto quando acionado, mas não obriga o agente a acioná-lo. O caso deve alimentar o experimento estrutural da SE03; não deve ser convertido retroativamente em PASS.

### F02-A2 — contexto declarado contraditório

Classificação: **LIMITATION_CONFIRMED**.

A Genie Code criou uma base sintética e observou quatro colunas numéricas reais (`id`, `valor_a`, `valor_b`, `valor_c`), mas chamou deliberadamente o preflight com `numeric_columns=0`.

Resultado observado:

- `status=PASS`;
- `blocking_issues=[]`;
- `condition_context.numeric_columns=0`;
- `correlation_matrix.applicable=false`;
- `correlation_matrix.resolved=null`;
- razão: `numeric_columns=0; limiar=2`.

Após uma tentativa inicial de importar um símbolo inexistente, a execução válida chamou diretamente `hub_scripts.skill_execution.run_preflight`, em vez do thin wrapper da skill. Isso não altera a semântica L2 exercitada, mas reforça que a SE02 ainda não oferece um entrypoint estrutural único obrigatório.

A contradição entre fato derivável e valor declarado é o failure mode previsto para provenance/SE03: condições futuras devem distinguir `runtime_derived`, `user_intent` e `agent_declared`, e o caso E10 deve exigir precedência do fato derivado ou bloqueio. Essa evolução não é introduzida silenciosamente no schema v0.1 da SE02.

## Estado da candidata antes do push de fechamento

```text
LOCAL_CERTIFICATION        = PASS
SYNTHETIC_AGENT_SCREENING = MIXED
DATABRICKS_FREE            = PASS
GITHUB_ACTIONS             = DEFERRED_CREDIT
FULLY_CERTIFIED            = false
SE03                       = NOT_STARTED
```

`DATABRICKS_FREE=PASS` significa que os gates previstos para a SE02 foram exercitados e registrados, incluindo as limitações deliberadamente observadas; não significa que F02-A1 ou F02-A2 sejam comportamentos desejáveis.

A entrada de CHANGELOG da SE02 já registra a implementação e seus limites históricos; este fechamento não adiciona nova capacidade funcional, apenas materializa o derivado final, reconcilia o snapshot e registra evidência de certificação/Free/Genie Code.

## Pendências após o push de fechamento

Depois do push da release candidate ainda restam, sem reclassificação antecipada:

1. observar os checks/workflows remotos disparados pelo HEAD exato;
2. atualizar o estado `GITHUB_ACTIONS` somente a partir de execução real;
3. obter aceite humano explícito antes de qualquer merge;
4. integrar somente após os checks obrigatórios aplicáveis;
5. executar/verificar os gates pós-merge na `main`;
6. manter SE03 não iniciada até o encerramento formal da SE02.
