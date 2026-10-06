# SE01 — contrato verificável e capability probe

> **Nota administrativa — 06/10/2026.** SE01 integrada pela PR #69 em `4ef1f8b9`. As pendências de abertura de PR, certificação e merge abaixo descrevem candidatas anteriores. [História SEF](../README.md) e [operação atual SER](../../skill_enforcement_rollout/README.md) distinguem o fechamento histórico da policy vigente. Esta nota não reclassifica resultados nem amplia o escopo certificado.

## Registro histórico preservado

## Estado

**CANDIDATA EM FECHAMENTO PARA HOMOLOGAÇÃO / NÃO HOMOLOGADA / PR #69 DRAFT.**

A SE01 implementa o nível L1 (`Contract`) do Skill Enforcement Framework para a skill piloto `hub-ml-eda-profissional`. O produto final da sprint mantém o contrato machine-readable, o schema e a validação estática em `mode="audit"`. O capability probe foi um instrumento experimental temporário: sua execução no Databricks Free permanece como evidência histórica, mas o script e a seção temporária foram retirados do produto antes da homologação.

SE02 não foi iniciada. A SE01 não contém preflight, runner determinístico, Execution Receipt ou postflight.

## Base e branch

- base de abertura: `main@99161fdeb9253c30a82243644ba89af8cd50d79e`;
- branch: `sef/SE01-contrato`;
- PR: #69, Draft;
- piloto: `hub-ml-eda-profissional`;
- laboratório obrigatório da experimentação: Databricks pessoal/Free;
- baseline de comparação: SE00, já encerrada/homologada/integrada.

Em 16/09/2026, a branch foi reconciliada sem force-push com `main@79f53ba1a131d93cbb0fea7bd885da32b82a7588` pelo commit `c824c8e973ed7b711ed654605166da794bcbde3c`. A reconciliação preservou integralmente as mudanças V14 da `main`; o único conflito material de conteúdo vivo era o `README.md` raiz, cuja versão da `main` foi preservada e depois atualizada somente com métricas novamente medidas.

## Evidência herdada da SE00

A SE01 parte de fatos medidos, não de hipótese:

- helper adherence: `0/69`;
- templates comprovados: `0/48`;
- reimplementações manuais: `67`;
- bypass resistance: `0/3`;
- auditorias A1 com state ladder completo: `0/4`.

Esses números são baseline histórico da SE00. Não são metas nem resultados atuais da SE01.

## Escopo final da sprint

1. ADR-0021 para execução verificável de skills.
2. `execution_contract` schema v0.1.
3. Contrato piloto da EDA em `mode="audit"`.
4. Validador estático que:
   - confere versão, skill, políticas e evidências;
   - resolve módulos do Hub até a pasta de objeto;
   - exige símbolo na API pública de `__init__.py`;
   - confere templates relativos e existentes;
   - recusa condições fora do vocabulário fechado;
   - não importa nem executa helpers para validar.
5. Testes positivos e mutantes negativos, incluindo consistência schema ↔ validator.
6. Compatibilidade do publicador Free exercitada por testes.
7. Workflow dedicado da SE01.
8. Experimento real de capability probe no Databricks Free, preservado apenas como evidência histórica.
9. Proteção de regressão que exige a aposentadoria do probe temporário no produto final.
10. Espelho regenerado pelo renderer canônico.
11. Reconciliação com a `main` vigente e snapshot raiz novamente medido.

## Contrato v0.1

O contrato canônico vive em:

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/execution_contract.json`

Recursos declaram `module` e `symbol` separadamente para tornar a API pública verificável. Em particular, `index_generator` resolve para `hub_snippets.visual.index_generator.gerar_indice_eda`; a SE01 não altera o inventário congelado da SE00 para corrigir retrospectivamente evidência histórica.

As políticas foram confrontadas com o inventário SE00. Para os templates da EDA, `roteiro_eda` e `relatorio_executivo_eda` permanecem `required`, enquanto `matriz_graficos_eda` e `estilo_visual_eda` permanecem `conditional`.

Políticas:

- `required`: obrigação declarada para o fluxo protegido;
- `conditional`: obrigação depende de condição objetiva do vocabulário v0.1;
- `optional`: permitido/recomendado, sem bloquear;
- `mode="audit"`: nesta sprint, nenhuma política implementa bloqueio runtime.

## Capability probe — experimento histórico encerrado

Durante a experimentação, o probe temporário existiu em:

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/capability_probe.py`

Ele era read-only e testava uma única capacidade: um script relativo da Agent Skill localizar `.assistant`, importar `hub_snippets.constants.format_br.fmt_int`, executar `fmt_int(1234)` e retornar o marcador `SEF_CAPABILITY_PROBE_V0_1` com `writes_performed=false`.

O experimento no Databricks Free produziu evidência observável de `PASS` no cenário testado. Esse resultado está preservado em `RESULTADOS.md` e não é reinterpretado como prova universal de execução determinística pelo Genie Code.

Decisão de fechamento da SE01:

- o script temporário foi removido da fonte;
- a seção temporária foi removida do `SKILL.md`;
- o renderer canônico removeu o script e a seção do simulado;
- o contrato, schema, validador, ADR e evidência histórica permanecem;
- a arquitetura continua `audit`;
- nenhuma arquitetura definitiva de preflight ou runner foi implementada.

## Evidência histórica intermediária

No commit `fda26d130e559d3fdb8ee69fcb785ffecc76a049`, antes dos testes finais no Free:

- contrato v0.1: **PASS — 1/1**;
- recursos: **10**;
- templates: **4**;
- testes SE01 naquele estágio: **11/11 PASS**;
- `validate_assistant.py`: **0 falhas / 0 avisos**;
- renderer: **sem diff** depois da materialização canônica do simulado.

Naquele estágio, o validador mediu **1494 arquivos / 1961 links**. Esses números permanecem históricos e não são reutilizados como snapshot atual.

Também houve incidente de infraestrutura do GitHub Actions em que jobs terminaram antes de alocar runner (`steps=[]`). Esses runs não foram classificados como falha funcional, mas também nunca foram promovidos a CI green.

## Reconciliação e materialização final do derivado

A `main` avançou com V14 durante a SE01. A reconciliação final foi feita por merge normal, sem force-push. Depois dela:

1. o workflow SE01 executou o renderer canônico e publicou `se01-skill-renderizado` como artifact;
2. a primeira execução pós-reconciliação reprovou corretamente porque o derivado ainda continha o probe histórico;
3. o artifact real do renderer foi usado como referência material para o commit `70c0f5beb8746502949188bf34e9ac2a557d1125`;
4. o `SKILL.md` derivado passou a ser byte a byte o produzido a partir da fonte e o probe derivado foi removido;
5. a execução seguinte confirmou `Renderer canônico não pode deixar diff = success`;
6. o snapshot real foi medido em **1501 arquivos / 1979 links**, sem alterar os demais campos verificáveis do README raiz;
7. o `README.md` raiz foi atualizado no commit `0af02feed197b789b00518da898dac3447dc7f37` e o workflow dedicado SE01 passou integralmente.

O `Novo_Ambiente_Simulado/` não foi tratado como segunda fonte de verdade.

## Fora de escopo

A SE01 **não** implementa:

- preflight `PASS/BLOCKED` da EDA;
- runner determinístico;
- Execution Receipt;
- postflight;
- bloqueio runtime de bypass;
- modo `WARN` ou `ENFORCE`;
- mudança em `.assistant_instructions.md` para enforcement;
- generalização às demais skills;
- promoção ao workspace corporativo.

Qualquer afirmação de que a EDA “está enforced” nesta sprint é incorreta.

## Artefatos vigentes

- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`;
- `tools/skill_enforcement/execution_contract.schema.json`;
- `tools/skill_enforcement/validate_contracts.py`;
- `tools/skill_enforcement/README.md`;
- `tools/tests/test_skill_enforcement_se01.py`;
- `ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/execution_contract.json`;
- `TESTES.md`, `RESULTADOS.md` e `CHECKPOINT.md`.

O capability probe temporário não faz parte dessa lista porque foi aposentado antes da homologação.

## Gate de encerramento

A SE01 só pode ser homologada quando, na árvore candidata final:

- contrato v0.1 e schema estiverem válidos;
- suíte SE01 estiver em PASS;
- fonte e simulado estiverem equivalentes pelo renderer canônico;
- `validate_assistant.py --conferir-readme` estiver em PASS;
- `ci_local.py --verbose` estiver em PASS ou sua impossibilidade estiver explicitamente classificada;
- workflows aplicáveis estiverem factual e observavelmente classificados;
- `CHANGELOG.md`, ADR, índice e documentos da sprint estiverem reconciliados;
- evidência histórica do Free continuar preservada sem ser tratada como atual;
- probe temporário continuar ausente do produto;
- `mode` continuar `audit`;
- houver aceite explícito do usuário.

SE02 não começa antes desse gate e exige nova autorização.