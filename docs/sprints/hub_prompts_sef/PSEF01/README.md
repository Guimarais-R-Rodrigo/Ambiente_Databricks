# PSEF01 — contrato editorial transversal e navegação policy-aware

**Base:** `main@11851e137dd7793b351ac08fc211c0be90005dee`  
**Branch:** `psef/PSEF01-contrato-editorial-policy-aware`  
**Estado:** `CANDIDATA_PARA_REVISAO`

## Objetivo

Tornar a documentação de entrada de `hub_prompts` compatível com o Skill Enforcement Framework vigente sem transformar prompts em um segundo sistema de enforcement.

## Escopo executado

A única superfície funcional alterada é:

`ambiente_fonte/.assistant/hub_prompts/README.md`

A sprint também acrescenta documentação probatória em `docs/sprints/hub_prompts_sef/PSEF01/` e atualiza o índice vivo da iniciativa.

Não foram alterados:
- os 16 briefings individuais;
- os 16 READMEs locais;
- os 16 notebooks de exemplo;
- skills;
- `policy.json`;
- `.assistant_instructions.md`;
- `MANUAL_TECNICO.md`;
- helpers/scripts;
- `Novo_Ambiente_Simulado/`.

## Contrato editorial estabelecido

O README raiz passa a representar explicitamente:

```text
Prompt / briefing
        ↓
Skill adequada
        ↓
Policy SEF / current_level
        ↓
rota realmente implementada
        ↓
helpers / snippets / scripts
        ↓
evidência proporcional ao nível vigente
```

Regras:
1. prompt continua briefing;
2. `current_level` descreve enforcement implementado hoje;
3. `target_level` continua roadmap;
4. `rollout_mode` pertence à skill/policy, não ao prompt;
5. entrypoint canônico de etapa protegida tem precedência sobre helper direto ou código manual;
6. prompts não recebem policy paralela, níveis L0–L4 próprios, Receipt ou Postflight;
7. níveis individuais não são hardcoded em cada briefing.

## Limite de escopo

A PSEF01 não corrige ainda os briefings EDA L4, `auditoria_skills`, `comparar_tabelas` ou os briefings L0. Essas correções continuam reservadas às PSEF02–PSEF04.

## Fonte e derivado

O renderer canônico `tools/render_simulado.py` faz cópia fiel byte a byte de `ambiente_fonte/` para `Novo_Ambiente_Simulado/`. Como esta execução não dispõe do checkout local completo necessário para regenerar toda a árvore e a regra do projeto proíbe editar o derivado manualmente, o espelho não foi tocado.

Assim:

```text
SOURCE_UPDATED      = true
DERIVED_UPDATED     = false
DERIVED_STALE       = true
DERIVED_STALE_CAUSE = PSEF01_SOURCE_CHANGE
MANUAL_DERIVED_EDIT = false
```

A candidata não deve ser mergeada isoladamente enquanto o derivado estiver stale. A rematerialização canônica permanece prevista para a PSEF06.
