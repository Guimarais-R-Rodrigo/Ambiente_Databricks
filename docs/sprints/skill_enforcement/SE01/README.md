# SE01 — contrato verificável e capability probe

## Estado

**EM EXECUÇÃO / NÃO HOMOLOGADA.**

A SE01 inicia o nível L1 (`Contract`) do Skill Enforcement Framework. Ela cria
uma representação machine-readable das obrigações da skill piloto e mede uma
capacidade concreta do Genie Code: executar, de forma previsível, um script
relativo à própria Agent Skill.

## Base e branch

- base de abertura: `main@99161fdeb9253c30a82243644ba89af8cd50d79e`;
- branch: `sef/SE01-contrato`;
- piloto: `hub-ml-eda-profissional`;
- laboratório obrigatório: Databricks pessoal/Free;
- baseline de comparação: SE00, já encerrada/homologada/integrada.

A branch nasceu da `main` vigente. Antes de eventual merge, qualquer novo avanço
da `main` deverá ser reconciliado e revalidado.

## Evidência herdada da SE00

A SE01 parte de fatos medidos, não de hipótese:

- helper adherence: `0/69`;
- templates comprovados: `0/48`;
- reimplementações manuais: `67`;
- bypass resistance: `0/3`;
- auditorias A1 com state ladder completo: `0/4`.

Esses números não são metas da SE01; são a justificativa para criar contrato
estruturado e prova de capacidade antes de implementar preflight/runner.

## Escopo implementado nesta sprint

1. ADR-0021 para execução verificável de skills.
2. `execution_contract` schema v0.1.
3. Contrato piloto da EDA em `mode="audit"`.
4. Validador estático que:
   - confere versão, skill, políticas e evidências;
   - resolve cada módulo do Hub até a pasta de objeto;
   - exige que o símbolo esteja na API pública de `__init__.py`;
   - confere templates relativos e existentes;
   - recusa condições fora do vocabulário fechado;
   - não importa nem executa helpers para validar.
5. Testes positivos e mutantes negativos.
6. Capability probe read-only dentro da skill piloto.
7. Instrução temporária e estritamente acionada por pedido explícito de probe.

## Fora de escopo

A SE01 **não** implementa:

- preflight `PASS/BLOCKED` da EDA;
- runner determinístico;
- Execution Receipt;
- postflight;
- bloqueio de bypass;
- modo `WARN` ou `ENFORCE`;
- mudança em `.assistant_instructions.md`;
- generalização às demais skills;
- promoção ao workspace corporativo.

Qualquer afirmação de que a EDA “está enforced” nesta sprint é incorreta.

## Contrato v0.1

O contrato canônico vive em:

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/execution_contract.json`

Recursos declaram `module` e `symbol` separadamente para tornar a API pública
verificável. Em particular, `index_generator` resolve para o objeto real
`hub_snippets.visual.index_generator.gerar_indice_eda`; a SE01 não altera o
inventário congelado da SE00 para corrigir retrospectivamente evidência
histórica.

Políticas:

- `required`: obrigação declarada para o fluxo protegido;
- `conditional`: obrigação depende de condição objetiva do vocabulário v0.1;
- `optional`: permitido/recomendado, sem bloquear;
- `mode="audit"`: nesta sprint, nenhuma dessas políticas bloqueia execução.

## Capability probe

O probe está em:

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/capability_probe.py`

Ele não executa EDA e não escreve arquivos. O único objetivo é comprovar que o
Genie Code consegue usar um script relativo da skill para:

1. localizar uma raiz `.assistant` válida;
2. adicionar essa raiz temporariamente ao `sys.path`;
3. importar `hub_snippets.constants.format_br.fmt_int`;
4. executar `fmt_int(1234)`;
5. devolver o marcador estruturado `SEF_CAPABILITY_PROBE_V0_1`;
6. declarar `writes_performed=false`.

Passar localmente não homologa a capacidade do Genie Code. O gate real ocorre no
Free em chat novo e está descrito em `TESTES.md`.

## Decisões deliberadas

- O frontmatter da skill não foi ampliado.
- O validador usa AST e arquivo `__init__.py`, não imports de runtime.
- Condições são tokens fechados, sem `eval`/Python arbitrário.
- A SE01 começa em `audit`; fail-closed pertence à SE02/SE05.
- A forma definitiva do runner continua em aberto até o probe real.

## Artefatos

- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`;
- `tools/skill_enforcement/execution_contract.schema.json`;
- `tools/skill_enforcement/validate_contracts.py`;
- `tools/tests/test_skill_enforcement_se01.py`;
- contrato e probe da `hub-ml-eda-profissional`;
- `TESTES.md`, `RESULTADOS.md` e `CHECKPOINT.md`.

## Gate de encerramento

A SE01 só pode fechar quando:

- ADR e schema estiverem revisados;
- contrato canônico passar no validador;
- todos os mutantes negativos pertinentes forem rejeitados;
- fonte e simulado estiverem equivalentes pelo renderer canônico;
- CI aplicável estiver verde;
- candidata tiver sido publicada no Free e verificada por conteúdo;
- capability probe tiver sido realmente executado em chat novo;
- uma execução normal de EDA confirmar que o contrato/probe não degradou o uso
  da skill;
- limitações reais forem registradas;
- probe for removido ou promovido conscientemente ao desenho definitivo;
- houver aceite explícito do usuário.

SE02 não começa antes desse gate.
