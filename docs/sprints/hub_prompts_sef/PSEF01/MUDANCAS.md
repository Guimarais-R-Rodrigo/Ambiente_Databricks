# PSEF01 — mudanças

## 1. Arquitetura do README raiz

A seção anterior `A Sinergia Triangular: Prompts, Skills e Helpers` foi substituída por `Fluxo Integrado: Prompt, Skill, Policy e Helpers`.

A redação nova introduz a policy SEF entre a skill e sua rota de execução e referencia diretamente:

`../hub_padroes/skill_enforcement/policy.json`

sem duplicar a tabela de níveis das 14 skills.

## 2. Semântica current × target

O README agora declara explicitamente que:
- `current_level` = enforcement realmente implementado;
- `target_level` = direção de evolução, sem provar implementação;
- `rollout_mode` pertence à policy da skill.

Isso resolve PSEF00-F03 sem antecipar PSEF04.

## 3. Precedência de rota

O passo operacional 4 foi alterado de `Revise o Plano antes de Executar` para:

`Revise o Plano e a Rota Vigente antes de Executar`.

Ele passa a exigir consulta à policy quando a skill foi selecionada e declara que, para etapa protegida, helper direto, PySpark/SQL manual, urgência ou disclaimer de execução fora do contrato não criam rota equivalente.

A regra é transversal e não menciona nenhuma skill específica.

## 4. FAQ

A pergunta sobre carregamento automático agora diferencia:
- seleção/carregamento da skill;
- consulta à policy;
- importação/chamada de snippets e scripts;
- função do prompt como contexto, não como substituto da rota da skill.

## 5. Itens deliberadamente não tratados

- detalhes L4 da EDA: PSEF02;
- fluxo L3 de `auditoria_skills`: PSEF03;
- semântica de helpers nos briefings L0: PSEF04;
- efeitos dos notebooks/READMEs locais: PSEF05;
- Manual, instruções globais, renderer e equivalência fonte→derivado: PSEF06.
