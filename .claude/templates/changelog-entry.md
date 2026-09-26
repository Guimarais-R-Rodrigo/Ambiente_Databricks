# Template — Entrada de changelog

Adicione sob a seção da data corrente (crie `## YYYY-MM-DD` se não existir).
Subseções na ordem: Adicionado, Atualizado, Corrigido, Removido, Notas.
Cada item começa com a IA autora entre parênteses.

```markdown
## 2026-08-20

### Adicionado

1. (Claude) Skill `publicar-free` com integração ao engine do Hub.

### Atualizado

1. (Codex) `tools/validate_assistant.py`: novo check de descrições duplicadas
   entre skills (reduz colisão de auto-seleção).

### Notas

- Forward test da skill X falhou no caso negativo; investigação aberta.
```

Regras: itens curtos (1–3 linhas), sem identificadores corporativos/PII, citar
caminhos de arquivos afetados, e nunca reescrever entradas de datas passadas.
