# SE02 — Preflight da EDA

## Estado

**EM IMPLEMENTAÇÃO / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE02 implementa o nível L2 (`Preflight`) do Skill Enforcement Framework sobre a skill piloto `hub-ml-eda-profissional`. Ela parte da SE01 integrada e do ADR-0021 aceito.

SE03 não foi iniciada.

## Baseline

- `main` de abertura: `4ef1f8b927f1ba706076a2c330c74d66e44a1b3f`;
- branch: `sef/SE02-preflight`;
- piloto: `hub-ml-eda-profissional`;
- contrato: `execution_contract.json` v0.1;
- modo preservado: `audit`.

## Objetivo

Resolver recursos e pré-condições antes que o agente escreva ou execute lógica analítica protegida, produzindo resultado estruturado `PASS` ou `BLOCKED` sem executar o core da EDA.

## Arquitetura implementada

A implementação separa três responsabilidades:

1. `hub_scripts.skill_execution`: API canônica e determinística de preflight;
2. `skills/hub-ml-eda-profissional/scripts/preflight.py`: acionador fino relativo à skill;
3. `SKILL.md`: instrução mínima que torna o gate parte do fluxo conversacional.

O preflight:

- carrega o contrato v0.1;
- resolve raiz `.assistant`, skill, versão e modo;
- classifica `required`, `conditional` e `optional`;
- avalia somente o vocabulário objetivo já aprovado no contrato;
- inspeciona APIs públicas por AST de `__init__.py`, sem importar indiscriminadamente a biblioteca;
- resolve templates relativos;
- produz decisões por item e issues bloqueantes;
- não executa Spark, helpers analíticos, runner, receipt ou postflight;
- não escreve no workspace.

## Contexto objetivo da EDA piloto

O acionador recebe explicitamente:

- `local_sample_required: bool`;
- `tabular_preview_required: bool`;
- `numeric_columns: int >= 0`;
- `numeric_distributions_requested: bool`;
- `resolved_theme_selected: bool`;
- `visual_diagnostics_requested: bool`.

Ausência ou tipo inválido de contexto usado por uma condição não vira `false` silencioso: o preflight retorna `BLOCKED`.

## Semântica de políticas

- `required`: aplicável sempre; indisponibilidade bloqueia;
- `conditional`: aplicável somente quando a condição objetiva é verdadeira; contexto não observável bloqueia;
- `optional`: disponibilidade é informativa e sua ausência não bloqueia.

## Saída estruturada

`PreflightResult` registra:

- skill, schema e mode;
- `status = PASS | BLOCKED`;
- `assistant_root_resolved`;
- decisões para recursos e templates;
- issues bloqueantes;
- contexto usado nas condições;
- `writes_performed=false`.

`PASS` não prova que os helpers serão chamados depois. Essa evidência pertence a sprints posteriores.

## Fora do escopo

A SE02 não implementa:

- runner determinístico da EDA;
- chamadas do core analítico;
- Execution Receipt;
- postflight;
- `mode="enforce"`;
- generalização às demais skills;
- mudança ampla em `.assistant_instructions.md`;
- promoção ao workspace corporativo.

## Gates previstos

1. contrato v0.1 válido;
2. regressão SE01;
3. suíte SE02;
4. validação estrutural;
5. renderer canônico e derivado sem diff;
6. snapshot README;
7. `ci_local.py --verbose`;
8. publicação e verify no Databricks Free;
9. teste de `PASS` e `BLOCKED` no Free;
10. teste conversacional em chat novo do Genie Code;
11. CI completo do HEAD candidato;
12. aceite explícito do usuário.

## Regra de encerramento

Nenhuma execução canônica da EDA deve avançar silenciosamente quando o preflight reportar requisito obrigatório indisponível. Isso ainda não equivale a enforcement completo, porque o comportamento de bypass do agente continua sendo objeto de medição.
