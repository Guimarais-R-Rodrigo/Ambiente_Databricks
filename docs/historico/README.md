# Histórico — snapshots e localizadores

- [Cronologia integral de 13/08 a 06/10/2026](changelog/README.md): 198 entradas na ordem original, manifesto e recuperação dos bytes.
- [Protótipo Concierge](concierge.md): localização congelada e rota canônica atual.
- [Construção histórica consolidada](../../CHANGELOG.md): intenção do plano, trajetória e marcos; única entrada inicial para conhecer a evolução. [Decisões](../decisions/README.md) e [owners vivos](../ai/context/projeto.md#owners-vivos) continuam responsáveis pelos contratos e pelo estado corrente.

- [Plano integral congelado](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd/PLANO_HUB.md): original de 911 linhas, retirado da árvore corrente. Dois hrefs em relatos antigos são recuperados pelo manifesto específico; para leitura, use este link Git, pois o arquivo local foi excluído.

A [readequação documental de 06/10/2026](readequacao_readmes_2026-10-06/README_RAIZ_TEMAS.md) preserva a cronologia transferida do README raiz e o [ciclo de vida anterior](readequacao_readmes_2026-10-06/CICLO_DE_VIDA_ANTERIOR.md).

Esta coleção preserva snapshots encerrados e documentos que já viajaram com o
`.assistant` e deixaram de ser produto. Ela explica origem e nomenclatura antiga, mas não é manual
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
| [x_original_export_manifest.json](x_original_export_manifest.json) | manifesto da exportação de origem | rastreabilidade rara |

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
