# ADR-0002 — Reutilizar o engine databricks-genie do Verg_Alchemy_Hub

Data: 2026-08-13
Status: **Supersedido pelo [ADR-0005](ADR-0005-publicacao-propria-no-free.md)** (2026-08-14)
Autor: Claude (aprovado por Rodrigo)

> A inspeção do engine mostrou dois impedimentos técnicos para consumi-lo nesta
> camada: `.py` importado como notebook (quebra os imports de `x_snippets`) e
> cabeçalho anteposto ao conteúdo (invalida o frontmatter das skills). O padrão
> de três fases foi mantido; o código não é consumido. Ver ADR-0005.

## Contexto

A publicação no Databricks Free precisa de tooling: render com validação,
publicação gated e verificação do remoto. O Verg_Alchemy_Hub já possui um engine
maduro (`src/databricks_genie/`, CLI `databricks-genie`) com exatamente esse
ciclo (render/publish/verify), manifesto declarativo, cabeçalhos de
não-canonicidade e guardrails (dry-run por padrão, nunca lê segredos, resolve
usuário via `databricks current-user me`). O Verg_Learning já o consome como
package editable com manifesto fino próprio.

## Decisão

Este projeto consome o engine do Hub em vez de construir publicador próprio
(fase 3 do roadmap): `pip install -e ../../Verg_Projects/Verg_Alchemy_Hub --no-deps`
+ manifesto fino em `tools/` + wrappers `render/publish/verify` para a camada
deste projeto. Coordenar targets com a camada global `global-*` que o Hub já
publica no mesmo workspace Free, sem sobrescrevê-la.

## Alternativas consideradas

- Scripts próprios de publicação — rejeitada: duplica engine testado e cria
  segunda implementação para manter.
- Publicação manual pela UI no Free — rejeitada: sem verify nem trilha; manual
  fica reservado ao trabalho, onde não há CLI.

## Consequências

- Ganho imediato de dry-run, gating `--execute` e verify.
- Dependência do repo do Hub presente na máquina; o runbook do trabalho não
  depende do engine (cópia manual da subárvore renderizada).

## Referências

- Hub: `docs/decisions/0004-databricks-genie-global-layer.md`,
  `docs/playbooks/databricks-genie.md`, `.claude/rules/databricks-genie.md`.
