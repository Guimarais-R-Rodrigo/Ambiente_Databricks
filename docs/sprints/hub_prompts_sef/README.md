# Hub Prompts × Skill Enforcement Framework — PSEF

**Iniciativa:** reconciliação pós-SE08 da camada `hub_prompts` com skills e Skill Enforcement Framework.

**Regime operacional:** `LOCAL_FIRST`.

```text
EXECUTION_REGIME = LOCAL_FIRST
GITHUB_ACTIONS    = DEFERRED_NO_CREDITS
```

GitHub Actions não é gate obrigatório desta iniciativa enquanto os créditos estiverem indisponíveis. Testes locais e Actions são canais distintos; nenhum PASS local deve ser descrito como PASS de Actions.

## Estado

| Bloco | Estado |
|---|---|
| PSEF00 — reconciliação, inventário, baseline e freeze | CANDIDATA_PARA_REVISAO |
| PSEF01–PSEF07 | NOT_STARTED |
| PSEF-ACTIONS-RECERTIFICATION | DEFERRED_NO_CREDITS |
| promoção ao workspace corporativo | NÃO_AUTORIZADA |

A PSEF não reabre a SE08, não altera retrospectivamente suas evidências e não promove `current_level`, `target_level` ou `rollout_mode`.

## Princípio arquitetural

```text
Prompt / briefing
        ↓
Skill adequada
        ↓
policy.json / current_level
        ↓
rota realmente implementada
        ↓
helpers/scripts canônicos
        ↓
evidência proporcional ao nível vigente
```

- **Prompt**: briefing da tarefa concreta.
- **Skill**: método, fluxo e guardrails.
- **SEF**: política e mecanismos de enforcement da skill.
- **Helper/snippet/script**: implementação reutilizável.
- **Receipt/Postflight**: evidência mecânica somente quando o `current_level` vigente a implementa/exige.
- **README/Manual**: documentação humana.

Não existe, nesta iniciativa, um segundo framework de enforcement próprio para prompts.

## Documentos

- [Plano Mestre](PLANO_MESTRE.md)
- [PSEF00](PSEF00/README.md)
- [Inventário PSEF00](PSEF00/INVENTARIO.md)
- [Matriz Prompt × Skill × SEF](PSEF00/MATRIZ_PROMPT_SKILL_SEF.md)
- [Achados](PSEF00/ACHADOS.md)
- [Checkpoint](PSEF00/CHECKPOINT.md)

## Fonte e derivado

A fonte editável continua em `ambiente_fonte/`. `Novo_Ambiente_Simulado/` é derivado e só deve mudar por renderer canônico quando uma sprint futura efetivamente alterar fonte.

PSEF00 é documental: não modifica prompts produtivos, skills, policy, instruções globais, Manual Técnico ou derivado.
