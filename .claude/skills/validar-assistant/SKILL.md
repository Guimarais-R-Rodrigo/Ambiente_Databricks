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
| Links Markdown relativos | sim | resolve para arquivo existente, **com a caixa exata** — NTFS ignora maiúsculas, o workspace Databricks não |
| Links dentro de notebook | sim | idem, para links escritos em célula `%md` de arquivo `.py` |
| Links fora da raiz analisada | sim | idem, para `README.md`, `docs/` e `.claude/` |
| Cercas de código | sim | blocos ``` balanceados em todos os .md |
| AST Python | sim | todos os .py compilam |
| Pastas de objeto | sim | nome identificador, módulo com o nome da pasta, notebook `exemplo_*`, e `__init__.py` idêntico à API pública derivada por AST |
| Sincronia do smoke test | sim | a cópia da regra de detecção de notebook em `spark_smoke_test.py` não divergiu de `notebook_marker.py` |
| Tamanho das instruções | sim | `.assistant_instructions.md` ≤ 20.000 caracteres |
| Mojibake/UTF-8 | sim | sem sequências `Ã©`-like ou erro de decodificação |
| Identificadores pessoais | sim | zero paths corporativos, e-mails ou usernames reais na raiz analisada |
| Identificador corporativo no repositório | sim | varredura do repositório inteiro; **varredura vazia reprova** |
| `__pycache__` no fonte | não (warn) | bytecode local; não quebra, mas viaja se alguém publicar fora do pipeline |

A saída **não** imprime `PASS` por check: imprime os contadores de cada um e,
abaixo, só as linhas de `WARN` e `FAIL`. Contador em zero onde deveria haver
volume é sinal de que o check não alcançou nada — foi assim que a varredura
corporativa desligou em silêncio uma vez.

**Esta tabela é declaração do que existe, não do que basta.** Um defeito que ela
não lista continua passando: link para documento errado que existe, caminho
citado em crase, e frase truncada não são detectáveis por nenhuma das linhas
acima.

## Interpretar e agir

- `FAIL` em identificadores pessoais: remover/parametrizar o valor **antes** de
  commitar; nunca contornar o check.
- `WARN` de tamanho: aplicar progressive disclosure (mover detalhe para
  `templates/`/`references/` da skill) quando for editar aquela skill.
- Após qualquer correção, rodar de novo até PASS e registrar no CHANGELOG.
