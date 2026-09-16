# SE02 — checkpoint

## Veredito atual

**CANDIDATA TÉCNICA EM CERTIFICAÇÃO / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE02 implementa exclusivamente L2 (`Preflight`) para `hub-ml-eda-profissional`. O contrato permanece `mode="audit"`; SE03, runner determinístico, Execution Receipt e postflight não foram iniciados.

## Estado Git atual

- `main`: `ae9337204a7c769c0b28b33321c8b81afdff6bae`;
- branch: `sef/SE02-preflight`;
- HEAD antes deste checkpoint: `fdfb3175d0facedd52a5a60ac587000e9df82be6`;
- merge-base: `ae9337204a7c769c0b28b33321c8b81afdff6bae`;
- `ahead_by=34`;
- `behind_by=0`;
- PR #74: aberta, Draft e mergeável.

A `main` avançou após a integração da SE01 por uma correção transversal da V08 (PR #75). A branch SE02 já foi reconciliada com essa `main` por merge normal, sem force-push.

## Implementado

- [x] contrato canônico da SE02 recuperado do Plano Mestre;
- [x] API pública `hub_scripts.skill_execution.run_preflight`;
- [x] script fino `skills/hub-ml-eda-profissional/scripts/preflight.py`;
- [x] instrução mínima no `SKILL.md` para executar o preflight antes do core;
- [x] `PASS`/`BLOCKED` estruturados;
- [x] required/conditional/optional tratados;
- [x] contexto condicional fail-closed quando condição necessária está ausente ou inválida;
- [x] resolução estática de APIs públicas por AST, sem importar helpers analíticos;
- [x] templates relativos resolvidos com proteção contra path inseguro;
- [x] `writes_performed=false` e teste de ausência de mutação;
- [x] suíte SE02 com 18 casos;
- [x] workflow dedicado SE02;
- [x] regressão SE01 preservada;
- [x] renderer executado canonicamente;
- [x] derivado materializado apenas pelo renderer;
- [x] Plano Mestre reconciliado para SE01 integrada / SE02 em andamento;
- [x] Manual Técnico e catálogo `hub_scripts` reconciliados com `skill_execution`;
- [x] `Novo_Ambiente_Simulado` atualizado a partir da fonte canônica;
- [ ] CI completo executado no HEAD de fechamento por runner real;
- [ ] Databricks Free publicado/verificado para a candidata final;
- [ ] testes Free de `PASS`/`BLOCKED`;
- [ ] teste conversacional do Genie Code;
- [ ] CHANGELOG final da SE02;
- [ ] aceite explícito do usuário;
- [ ] merge.

## Evidência histórica observada na branch

### Run inicial `35147659671`

- contrato v0.1: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02: 18/18 PASS;
- validação estrutural: FAIL por quatro convenções estruturais do novo objeto.

Os achados foram corrigidos sem mudar a semântica L2.

### Run `35148053257`

- contrato v0.1: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02: 18/18 PASS;
- validação estrutural: PASS;
- renderer: PASS;
- artifact publicado;
- diff do derivado: FAIL porque a saída do renderer ainda não estava materializada na branch.

O derivado foi então materializado exclusivamente pelo renderer no workflow transitório `SE02 Materialize Simulado`, run `35148184892`, com todos os steps em `success`.

### Run `35148293591`

- contrato: PASS;
- SE01: 14/14 PASS;
- SE02: 18/18 PASS;
- validação estrutural: PASS — 0 falhas / 0 avisos;
- renderer: 555 arquivos;
- artifact: PASS;
- derivado sem diff: PASS;
- snapshot: FAIL exclusivamente por métricas antigas no README.

As métricas foram novamente medidas e reconciliadas para 1516 arquivos / 1985 links, além das demais métricas do snapshot.

### Gates transversais intermediários

No HEAD `e99b5ee6557bd8898c22986a2d1627f4942d132a`:

- `CI local reproduzível`: 8/9 etapas PASS; única falha = inventário do Manual Técnico ainda sem `hub_scripts.skill_execution`;
- V08: testes funcionais e regressões passaram; única falha = guard histórico V08 aplicado indevidamente a evoluções posteriores de `hub_scripts`.

A dívida documental foi corrigida na SE02. O guard V08 foi corrigido fora da SE02 pela PR #75 e integrado na `main@ae9337204a7c769c0b28b33321c8b81afdff6bae`.

## Auditoria independente do desenho L2

O preflight atual é coerente com a fronteira da SE02:

- lê `execution_contract.json`;
- resolve `.assistant`, skill, schema e `mode`;
- resolve recursos via fachada pública por AST;
- resolve templates relativos;
- avalia condições objetivas fornecidas no `condition_context`;
- bloqueia se contexto necessário estiver ausente/for inválido;
- não executa helpers analíticos;
- não executa EDA;
- não cria runner/receipt/postflight;
- não altera `.assistant_instructions.md`.

### Limitação deliberada a validar no Free

Parte das condições (`local_sample_required`, `tabular_preview_required`, `numeric_distributions_requested`, `resolved_theme_selected`, `visual_diagnostics_requested`) é informada pelo chamador. `numeric_columns` também entra como contexto após inspeção de schema.

Isso é suficiente para um gate L2 determinístico quando o contexto foi estabelecido corretamente, mas ainda não prova que o Genie Code não tentará fornecer contexto falso para evitar uma condição. A SE02 não deve transformar essa limitação em alegação de enforcement completo. O comportamento de bypass precisa ser medido nos testes Free/adversariais e, depois, endurecido nas camadas previstas do SEF quando houver evidência.

## HEAD atual e Actions

O HEAD `fdfb3175d0facedd52a5a60ac587000e9df82be6` disparou 12 workflows com conclusão `action_required` e `jobs=[]`, por ter sido produzido por automação GitHub Actions. Esses runs não são PASS nem regressão funcional; não executaram testes.

Este checkpoint é um commit direto da frente e serve também para disparar nova rodada de CI com runner observável. A certificação só será considerada válida se os jobs realmente executarem steps.

## Limites preservados

- `mode="audit"`;
- sem runner determinístico;
- sem Execution Receipt;
- sem postflight;
- sem `mode="enforce"`;
- sem promoção corporativa;
- `.assistant_instructions.md` não alterado;
- SE03 não iniciada.

## Próximos gates

1. certificar o novo HEAD nos workflows aplicáveis, exigindo runner real;
2. reconciliar CHANGELOG final sem reescrever história;
3. publicar/verify a candidata no Databricks Free quando houver acesso ao CLI/ambiente autorizado;
4. executar casos Free `PASS` e `BLOCKED`;
5. executar o teste conversacional do Genie Code em chat novo;
6. atualizar RESULTADOS/PR com evidência observada;
7. apresentar a SE02 para aceite humano;
8. não fazer merge sem aceite; não iniciar SE03.
