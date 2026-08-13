---
name: validar-assistant
description: >-
  Valida o ecossistema ambiente_fonte/ (skills, instruções, extensões) com a
  bateria local que recria a auditoria do Codex. Use antes de qualquer commit
  que toque ambiente_fonte/, antes de renderizar o simulado e antes de publicar.
---

# Validar o ambiente_fonte

## Executar

```powershell
python tools/validate_assistant.py
```

Saída esperada: relatório por check com `PASS`/`FAIL`/`WARN` e resumo final.
Exit code 0 = aprovado; 1 = há falha bloqueante.

## Checks executados

| Check | Bloqueante? | Critério |
|---|---|---|
| Frontmatter das skills | sim | `name` + `description` presentes; `name` == nome da pasta |
| Tamanho de SKILL.md | não (warn) | alerta acima de 500 linhas (progressive disclosure) |
| Links Markdown relativos | sim | todo link relativo resolve para arquivo existente |
| Cercas de código | sim | blocos ``` balanceados em todos os .md |
| AST Python | sim | todos os .py compilam |
| Tamanho das instruções | sim | `.assistant_instructions.md` ≤ 20.000 caracteres |
| Mojibake/UTF-8 | sim | sem sequências `Ã©`-like ou erro de decodificação |
| Identificadores pessoais | sim | zero paths corporativos, e-mails ou usernames reais |

## Interpretar e agir

- `FAIL` em identificadores pessoais: remover/parametrizar o valor **antes** de
  commitar; nunca contornar o check.
- `WARN` de tamanho: aplicar progressive disclosure (mover detalhe para
  `templates/`/`references/` da skill) quando for editar aquela skill.
- Após qualquer correção, rodar de novo até PASS e registrar no CHANGELOG.
