# Histórico — o que saiu do produto e por quê

Documentos que estavam publicados no workspace e deixaram de estar. Não são
lixo: registram decisões, estado e contexto que ainda explicam por que o Hub é
como é. Saíram porque são **governança**, e governança não precisa viajar junto
do produto para dentro do Databricks.

## O que tem aqui

| Arquivo | O que registra | Quando consultar |
|---|---|---|
| [ROADMAP_SKILLS.md](ROADMAP_SKILLS.md) | backlog priorizado por P1–P3 e o que foi concluído na revisão do Codex | ao planejar o próximo passo da biblioteca |
| [LEGACY_CONTEXT.md](LEGACY_CONTEXT.md) | como era o ambiente pessoal antes da auditoria do Codex | investigando por que alguma decisão foi tomada |
| [skills_manifest.md](skills_manifest.md) | manifesto funcional das skills, escrito antes da reestruturação | comparando o escopo declarado de cada skill com o atual |
| [AGENTS_TEMPLATE.md](AGENTS_TEMPLATE.md) | modelo de `AGENTS.md` para um projeto real | ao criar contexto de projeto no workspace |
| `x_original_export_manifest.json` | evidência da exportação original do ambiente | rastreabilidade; consulta rara |

## Por que saíram, um a um

**Roadmap, contexto legado e manifesto** descrevem o projeto, não o ecossistema.
Quem usa o Hub dentro do Databricks nunca precisa deles; quem mantém o Hub tem o
repositório.

**O template de `AGENTS.md`** veio de `x_projects/`, removida na Sprint 2 porque
guardar o arquivo lá dentro nunca fez ele ser descoberto — o mecanismo exige que
ele esteja na árvore do projeto real. O modelo continua útil, e é isso que ele é:
um modelo, não parte do produto.

**O manifesto de exportação** é evidência de origem. Cumpriu o papel.

## Nomenclatura

Estes documentos usam `x_*` e `rodrigo-*`, os nomes que existiam quando foram
escritos. Não são reescritos: descrevem o que era, não o que é. A correspondência
com os nomes atuais está no ADR da reestruturação.

## O que **não** vem para cá

Registro datado — `CHANGELOG.md`, ADRs, auditorias, evidência de teste — fica
onde está. Esta pasta é para conteúdo que era produto e deixou de ser, não para
arquivar histórico que já tem lugar próprio.
