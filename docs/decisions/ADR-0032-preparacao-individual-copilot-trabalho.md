# ADR-0032 — Preparação individual para Copilot e Databricks no trabalho

Data: 08/10/2026. Estado: execução local autorizada por Rodrigo. Autoria: Codex.
Base: `8ee3a61bfa9b638e15bcc5de41a8f87c10e37682`.
Supersede: geração e conservação do adaptador Claude Code do ADR-0025;
demais invariantes, evidências e contratos continuam aplicáveis.

## Decisão

Cada colega usa seu clone, perfil nativo e instalação pessoal. O Git recebe um
modelo sintético; configuração real fica em `config/workspace.local.json`,
ignorada e recusada pelo leitor se adicionada ao índice. O leitor valida schema,
host do perfil e raízes pessoais distintas. Credenciais continuam na autenticação
nativa, fora do contrato de configuração. O ignore não é barreira contra leitura
por ferramentas de uma IA.

Desenvolvimento da extensão e instalação do Hub têm destinos distintos. A primeira
ferramenta resolve paths e inventário offline, sem criar configuração nativa nem
realizar transferência. A alternativa CLI para instalação precisa de versão,
tipos FILE/NOTEBOOK, ACL e staging observados no trabalho; até lá permanece o
runbook manual. O publicador Free não é adaptado para aceitar host corporativo.

Copilot no VS Code é a superfície escolhida. Remover `CLAUDE.md` e os cinco
adaptadores versionados, incluindo manifesto. Remover o escritor de outputs;
a opção antiga `--generate` permanece apenas como erro de migração sem escrita.
O gate valida diretamente oito skills canônicas. Os testes exclusivos do escritor
retirado são substituídos por testes da retirada e preservação das guardas de
fonte, identidade, requisitos, links, inventário e payload. Fontes Git, citações,
revisões de identidade e decisões históricas permanecem preservadas.

Três novas skills cobrem preparação do trabalho, evolução e revisão. Dois agentes
Copilot declaram somente ferramentas de busca/leitura. Modelo não é fixado;
nenhum login, instalação de extensão, MCP, hook ou setting foi aplicado.

Dois links locais em sprints congelados recuperam o adaptador pelo Git com ledger
restrito a pares exatos, base fixa e hashes. Não reescrever evidência datada para
parecer atual. Arquivos pessoais ignorados na família retirada são preservados.

## Verificação e continuidade

Testes locais cobrem schema, host divergente, raízes amplas/sobrepostas, isolamento
Git, payload, dois usuários e retirada do gerador. Gates existentes continuam
medindo fonte e paridade. Não há alteração de produto nesta execução, portanto
não há render a regenerar. Confirmações nativas e auditoria A1 antes de compartilhar
continuam pendentes, com roteiro no [guia](../playbooks/copilot-trabalho.md).

Rollback recupera arquivos e controles deste lote pela base Git, preservando
mudanças posteriores e arquivos pessoais. Remover a configuração local não revoga
credenciais nem desfaz efeitos externos.

[Execução](../manutencao/execucao-adaptacao-trabalho-2026-10-08.md) · [Índice](README.md)
