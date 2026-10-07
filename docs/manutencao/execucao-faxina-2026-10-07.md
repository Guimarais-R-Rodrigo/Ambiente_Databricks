# Execução da faxina — 07/10/2026

Owner: Codex, coordenador desta sessão. Baseline:
`8dd8da57de89122241890b8b6b059fd2f9be25d0`.
Branch: `codex/plano-faxina-20261007`. Estado inicial: relatório, plano, inventário
e README de workflows locais, preservados nesta execução.

## Escopo autorizado e decisões

O usuário autorizou executar: documentação dos workflows; revisão de adaptadores
mantidos; rename confirmado para `ambiente_databricks`; remoção do protótipo;
catálogo/manutenção das ferramentas; Manual Técnico V2 como única edição vigente.
Autorizou executores e auditores auxiliares. Não houve pedido de publicação remota.

| Lote | Owner executor | Escopo | Integração |
|---|---|---|---|
| Fonte/caminhos/CI/adaptadores | Codex coordenador | checkout principal | owner único das rotas comuns |
| Manuais | executor_manuais | worktree isolada faxina-manuais | copiar somente diff permitido e revisar |
| Protótipo/tools | executor_tools_prototipo | worktree isolada faxina-tools-prototipo | copiar somente diff permitido e revisar |
| Revisão | auditoria_ia_ci | somente leitura, contexto completo | apoio de mesma sessão, não origem A1 |

## Uso atual e história

A fonte corrente é `ambiente_databricks/`. Não é um simulador: o espelho gerado
continua em `.artifacts/simulado/`. Código, workflows e rotas atuais usam o novo
nome. Relatórios fechados, snapshots, fixtures datadas e corpos de ADRs mantêm o
nome original para representar sua revisão. O inventário da análise anterior é
fotografia da baseline, não catálogo corrente.

O [manifesto de referências históricas](referencias-historicas-faxina.json)
enumera os hrefs antigos preservados. Cada entrada informa fonte/hash, destino,
objeto Git e SHA256 no commit original. Para navegar, abra o [snapshot completo
no GitHub](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/tree/8dd8da57de89122241890b8b6b059fd2f9be25d0)
e o caminho `source`/`target` da entrada. Localmente, use
`git show 8dd8da57de89122241890b8b6b059fd2f9be25d0:<target>` para arquivo.
Links históricos recuperáveis não são links locais funcionando, e o gate não
verifica fragmentos/âncoras. Histórico Git ausente bloqueia essa prova.

O protótipo será recuperável pelo [registro Concierge](../historico/concierge.md)
e manifesto original. Isso não recria uma segunda pasta de produto no checkout.

## Evidência e limites

Registro em andamento. Os resultados finais serão preenchidos após integração,
validação, render e revisão do diff. Apoios da mesma sessão não satisfazem
auditoria independente A1/A2. Copilot no VS Code do trabalho e runtime Databricks
permanecem NOT_RUN nesta execução local.

## Reversão

As mudanças permanecem revisáveis no Git local. Os worktrees isolados preservam
os lotes dos executores até a integração e podem ser arquivados com snapshot.
Não usar reset destrutivo: recuperar somente arquivos deste lote, preservando o
trabalho documental anterior e quaisquer alterações alheias.
