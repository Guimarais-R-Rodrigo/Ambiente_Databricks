# Histórico — conteúdo retirado do produto

Esta coleção preserva documentos que já viajaram com o `.assistant` e deixaram
de ser produto. Ela explica origem e nomenclatura antiga, mas não é manual
vigente.

> **Leitura histórica:** não atualize nomes antigos apenas para parecerem atuais.
> Se um fato vigente precisar de correção, faça-a no documento canônico e
> registre a relação no changelog.

## Inventário

| Arquivo | Registra | Consulte quando |
|---|---|---|
| [`ROADMAP_SKILLS.md`](ROADMAP_SKILLS.md) | backlog anterior e entregas da revisão inicial | reconstruir prioridade histórica |
| [`LEGACY_CONTEXT.md`](LEGACY_CONTEXT.md) | ambiente pessoal antes da reestruturação | investigar origem de uma decisão |
| [`skills_manifest.md`](skills_manifest.md) | escopo funcional antigo das skills | comparar intenção antiga e contrato atual |
| [`AGENTS_TEMPLATE.md`](AGENTS_TEMPLATE.md) | modelo de contexto de projeto | criar `AGENTS.md` em um projeto real |
| `x_original_export_manifest.json` | manifesto da exportação de origem | rastreabilidade rara |

## Por que não ficam no produto

Roadmap, contexto legado e manifesto descrevem a manutenção do ecossistema, não
o uso no Databricks. O modelo de `AGENTS.md` só funciona quando é colocado na
árvore do projeto real; guardá-lo dentro de `.assistant` não cria contexto
automático.

## Fronteiras

- Resultados datados ficam em [testes](../testes/README.md).
- Decisões ficam em [ADRs](../decisions/README.md).
- Auditorias ficam em [auditoria](../auditoria/README.md).
- Relatórios de execução ficam em [sprints](../sprints/README.md).
- Nomes `x_*` e `rodrigo-*` permanecem como evidência da época; o
  [ADR-0006](../decisions/ADR-0006-identidade-hub.md) faz a correspondência.

[Voltar ao índice de documentação](../README.md)
