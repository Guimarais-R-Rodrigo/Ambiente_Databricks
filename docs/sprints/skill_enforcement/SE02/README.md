# SE02 — Preflight da EDA

## Estado

**EM CERTIFICAÇÃO / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE02 implementa o nível L2 (`Preflight`) do Skill Enforcement Framework sobre a skill piloto `hub-ml-eda-profissional`. Ela parte da SE01 integrada e do ADR-0021 aceito.

A revisão operacional vigente está em `../REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`.

SE03 não foi iniciada.

## Baseline

- `main` de abertura: `4ef1f8b927f1ba706076a2c330c74d66e44a1b3f`;
- `main` após reconciliação V08: `ae9337204a7c769c0b28b33321c8b81afdff6bae`;
- branch: `sef/SE02-preflight`;
- piloto: `hub-ml-eda-profissional`;
- contrato: `execution_contract.json` v0.1;
- modo preservado: `audit`.

## Objetivo

Resolver recursos e pré-condições antes que o agente escreva ou execute lógica analítica protegida, produzindo resultado estruturado `PASS` ou `BLOCKED` sem executar o core da EDA.

A SE02 é um building block de enforcement. Ela **não deve ser confundida com enforcement estrutural completo**: um agente ainda pode tentar ignorar o preflight. O objetivo de impedir que output produzido fora do caminho canônico seja homologado pertence às camadas estruturais posteriores, principalmente SE03–SE05.

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
- bloqueia `__all__` que declara nome sem import/definição real;
- exige module path Python canônico sob `hub_snippets.*` ou `hub_scripts.*`;
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

### Limitação conhecida de provenance

Parte desse contexto ainda é fornecida pelo chamador. A revisão do Plano Mestre passou a distinguir conceitualmente condições `runtime_derived`, `user_intent` e `agent_declared`. A SE02 deve documentar a limitação e preparar essa evolução, mas não deve alterar silenciosamente o schema v0.1.

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

## Aprendizado do laboratório sintético

Um laboratório isolado de 52 runs com coding agent comparou reinforcement textual, contrato, procedimento e entrypoint estrutural. Nos casos em que o caminho canônico estava adulterado ou falhava, o salto observável ocorreu apenas quando um entrypoint estrutural falsificável foi introduzido.

Esse resultado **não prova comportamento do Genie Code/Databricks**, mas muda a prioridade do projeto:

- não prolongar SE02 tentando resolver enforcement por redação cada vez mais forte;
- fechar o L2 corretamente;
- testar o maior valor marginal em SE03 com entrypoint estrutural + integridade + trace mínimo;
- levar uma pequena matriz adversarial para o critério de aceite da SE03.

## Certificação local-first

Durante desenvolvimento, GitHub Actions deixa de ser o mecanismo primário de descoberta de defeitos.

Estados separados:

- `LOCAL_CERTIFICATION`;
- `SYNTHETIC_AGENT_SCREENING`;
- `DATABRICKS_FREE`;
- `GITHUB_ACTIONS`;
- `FULLY_CERTIFIED`.

`GITHUB_ACTIONS = DEFERRED_CREDIT` não significa PASS nem failure funcional.

O entrypoint local canônico da frente passa a ser `tools/skill_enforcement/certify_local.py`. O workflow remoto deve chamar esse mesmo entrypoint somente quando a PR estiver Ready-for-review ou na `main` pós-merge.

## Fora do escopo

A SE02 não implementa:

- runner determinístico da EDA;
- chamadas do core analítico;
- `ExecutionTraceV0` do runner;
- Execution Receipt formal;
- postflight;
- `mode="enforce"`;
- manifest/fingerprint de release do runner;
- generalização às demais skills;
- mudança ampla em `.assistant_instructions.md`;
- promoção ao workspace corporativo.

## Gates revisados

1. contrato v0.1 válido;
2. resolução estática compartilhada entre contrato e preflight;
3. regressão SE01;
4. suíte SE02 com os adversariais de fachada/path;
5. validação estrutural;
6. renderer canônico e derivado sem diff;
7. snapshot README;
8. certificação local reproduzível;
9. `ci_local.py --verbose` com etapa SEF;
10. publicação e verify no Databricks Free;
11. um caso `PASS`, um `BLOCKED` e um teste deliberado de bypass/limitação no Free/Genie Code;
12. fechamento documental;
13. aceite explícito do usuário;
14. GitHub Actions final no HEAD candidato quando houver crédito/execução disponível e conforme checks obrigatórios reais do repositório.

## Regra de encerramento

Nenhuma execução canônica da EDA deve avançar silenciosamente quando o preflight reportar requisito obrigatório indisponível.

A SE02 pode encerrar reconhecendo explicitamente que L2 ainda não impede um agente de pular o gate. O objetivo da sprint é tornar o preflight correto, determinístico, observável e pronto para ser incorporado ao entrypoint estrutural da SE03 — não fabricar uma alegação de enforcement que ainda não existe.
