# ADR-0031 — Retirada do localizador do plano do Hub

Data: 08/10/2026. Estado: execução local autorizada por Rodrigo. Autoria: Codex.
Base: `a50f35c1a9602d0bb0b05dd9afb020d42e7fda4b`.
Supersede: somente a conservação do localizador prevista no ADR-0030.

## Contexto e decisão

A história e a decisão vigente da paleta já pertencem ao CHANGELOG. O arquivo
local de 15 linhas existia apenas para compatibilidade. O usuário autorizou a
execução do plano e sua exclusão em 08/10/2026.

1. Excluir `PLANO_HUB.md` da árvore corrente. AGENTS, regra de fontes, comentário
   vigente do validador e índices de sprints/auditoria passam ao consolidado.
   A exceção de paleta e `CORPORATE_RE` mantêm exatamente seu alcance.
2. Manter fontes e citações históricas, ADRs aceitos, snapshots, quotes de origem
   e scripts de campanhas encerradas. Atualizar a rota documental da docstring
   do validador sem mudar a guarda de saída colada.
3. Acrescentar um ledger separado para exatamente dois hrefs históricos, sem
   modificar as 30 referências ou o contrato da faxina. Suas fontes são o
   handoff de 09/09 e o diagnóstico de ferramentas de 07/10; nenhuma pasta
   inteira passa a ser dispensada de validar links.
4. O novo ledger exige os dois pares específicos de fonte/href, fonte Git
   `6ac0060dfcd09134634abe204474debb5757e231`, destino Git
   `09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd`, target `PLANO_HUB.md`, blob e
   SHA-256 do plano integral de 911 linhas. Fonte atual deve ser idêntica ao
   original; inventário incompleto, alterado ou obsoleto é erro.
5. Atualizar somente hash/revisão da entrada AGENTS no inventário nativo. Fontes
   capturadas e identidades de requisitos permanecem iguais; a validação
   demonstra que não se exige revisão da cadeia de rastreabilidade para esta
   troca de referência. Adaptadores não dependem dos bytes do núcleo e continuam
   idênticos; não há conteúdo de produto a renderizar.
6. Acrescentar marco datado; condensar somente a síntese editorial da trajetória,
   mantendo relatos datados anteriores e a meta de 200 linhas no consolidado.

## Recuperação e limites de navegação

[Plano integral no Git](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd/PLANO_HUB.md).
Manifesto: `docs/manutencao/referencias-historicas-plano-hub.json`.
SHA-256: `4307e9c3dd6301b7b04733f6ebaebaa8d6ab41215550e6817bb0b68b39ac125f`.

Os dois hrefs antigos continuam texto histórico; não são links locais clicáveis
em ZIP. O índice histórico e o consolidado fornecem a URL congelada para leitura.
O validador identifica 32 referências históricas recuperáveis no Git, das quais
30 pertencem à faxina anterior. Clone completo é necessário para conferir as
fontes/objetos; commit ou blob ausente não é aprovação.

Não há mudança de runtime, policy, payload ou YAML de workflow. Validação local
não certifica CI remoto, Copilot, Databricks ou homologação corporativa.

[Execução e verificações](../manutencao/execucao-retirada-plano-hub-2026-10-08.md) · [Índice](README.md)
