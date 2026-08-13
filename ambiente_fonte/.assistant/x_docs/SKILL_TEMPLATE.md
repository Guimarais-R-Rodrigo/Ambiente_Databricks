# Template de Agent Skill

> **DOCUMENTAÇÃO CUSTOMIZADA (`x_docs`) — não auto-descoberta.** Copie a pasta
> criada para `.assistant/skills/<skill-name>/`, que é a estrutura nativa.

Crie uma pasta com nome em kebab-case e um `SKILL.md`. A Databricks exige `name` e
`description`. Este pacote omite campos extras por uma **convenção conservadora
local**, para maximizar portabilidade entre validadores:

```markdown
---
name: nome-da-skill
description: >-
  Faça X e entregue Y. Use quando o usuário pedir A, B ou C, quando existir o
  artefato D, ou quando mencionar os termos E e F. Não use para G.
---

# Nome legível

## Objetivo

Produza ...

## Entradas obrigatórias

- ...

## Fluxo

1. Valide ...
2. Execute ...
3. Verifique ...

## Contrato de saída

- ...

## Limites e segurança

- ...
```

## Progressive disclosure

Mantenha o `SKILL.md` preferencialmente abaixo de 500 linhas e 5.000 tokens.
Quando houver detalhes grandes, coloque-os a um nível de profundidade:

```text
nome-da-skill/
├── SKILL.md
├── references/
│   └── metodologia.md
├── scripts/
│   └── validar.py
└── assets/
    └── template.md
```

O `SKILL.md` deve explicar quando ler/executar cada recurso. Como preferência local,
use `references/`, `scripts/` e `assets/` em vez de nomes genéricos, e evite cadeias
de referências profundas. O padrão aceita outros diretórios quando fizerem sentido.

## Checklist

```text
[ ] name == nome da pasta
[ ] description explica o que faz e quando usar
[ ] YAML contém name e description; extras só com justificativa e suporte confirmado
[ ] instruções usam verbos no imperativo
[ ] entradas, permissões, escrita e output são explícitos
[ ] exemplos são realistas e sem paths/segredos pessoais
[ ] alegações Databricks têm nomenclatura oficial atual
[ ] scripts falham com diagnóstico e têm testes
[ ] links relativos existem
[ ] o validador local adotado pelo projeto passa
[ ] forward test em um novo chat confirma auto-seleção e @menção
```

Validador opcional do ambiente Codex usado para construir este pacote (não é uma
ferramenta da Databricks e pode não existir na máquina do consumidor):

```powershell
python C:\Users\<user>\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill-folder>
```

Quando o utilitário oficial de referência do padrão Agent Skills estiver instalado,
use também:

```text
skills-ref validate ./nome-da-skill
```

Na Genie Code, abra um novo chat depois de publicar/alterar a skill.
