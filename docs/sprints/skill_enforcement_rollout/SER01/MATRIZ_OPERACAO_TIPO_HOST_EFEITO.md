# SER01 — matriz operação × tipo × host × efeito

Base: `dedde0741ed4c387c3a500adfbf7de2c6166aba5`. Esta matriz descreve a candidata A1, não amplia o escopo L3 aprovado. `IMPLEMENTADO_CANDIDATO` significa código escrito, não integração provada.

## Estados e hospedeiros

`L2_EXISTENTE` refere-se ao preflight histórico, sem atribuir nova certificação. `IMPLEMENTADO_CANDIDATO/NOT_RUN` refere-se à nova primitive aguardando clone completo. `BLOCKED` é recusa deliberada, não PASS. O host desta autoria executou testes de desenvolvimento em Linux/Python 3.13.5; isso não provou a integração de nenhuma das rotas abaixo.

H-CLONE: Linux ou Windows observado, checkout completo, ferramentas canônicas e evidência externa. A implementação usa o supervisor existente; cada host que vier a compor o envelope promovido precisa de prova própria.

H-WIN-PILOTO: writer anterior de README agregador, Windows/NTFS histórico, sem alterações em A1 e sem transporte de PASS para código modificado.

H-FREE: Databricks Free/Genie, sem executar nesta rodada. `tools/` não é publicado pelo renderer; a nova primitive não pode ser alegada como executada automaticamente no workspace.

## Operações, artefatos e efeitos no clone completo

| Operação | Tipo/escala | Preflight | Geração nesta A1 | Validação candidata | Apply/move no original | Prova atual |
|---|---|---|---|---|---|---|
| create | snippet | L2 existente + envelope | recebe 4 arquivos; não gera código | api_publica + validator canônico | não implementado nesta primitive | PROVEN H-WIN R4 · estrutural local |
| create | script | L2 existente + envelope | recebe 4 arquivos | api_publica + validator canônico | não implementado nesta primitive | PROVEN H-WIN R4 · estrutural local |
| create | prompt | L2 existente + envelope | recebe 3 arquivos | validator canônico | não implementado nesta primitive | PROVEN H-WIN R4 · estrutural local |
| create | notebook | L2 existente + envelope | recebe 1 arquivo | validator canônico; não executa notebook | não implementado nesta primitive | PROVEN H-WIN R4 · estrutural local; runtime NOT_RUN |
| create | README agregador | L2 existente + envelope | recebe bytes + document | checks do agregador existente + validator | não chama apply do piloto | PROVEN H-WIN R4 · estrutural local |
| create | README Objeto avulso | L2 histórico não ampliado | fora de A1 | BLOCKED; README Objeto de pacote é verificado nos 3 tipos acima | BLOCKED | recusa unitária exercitada |
| create | skill | L2 histórico não ampliado | fora de A1 | BLOCKED: cardinalidade/policy exigem decisão | BLOCKED | recusa unitária exercitada |
| convert | snippet | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |
| convert | script | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |
| convert | prompt | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |
| convert | notebook | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |
| convert | README agregador | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |
| convert | README Objeto | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |
| convert | skill | L2 histórico não ampliado | fora de A1 | BLOCKED antes de I/O | nenhum move | recusa unitária exercitada |

As recusas de operação são comuns ao envelope; não representam execução positiva dos seis domínios. A validação de README Objeto é consumida pelo validator de pacotes, não por uma implementação editorial paralela.

## Matriz por host para cada rota candidata

| Rota | Linux com clone integral | Windows/NTFS com clone integral | Databricks Free/Genie |
|---|---|---|---|
| snippet/create/validate | NOT_RUN | PROVEN R4 · estrutural local | NOT_AVAILABLE: primitive repo-side |
| script/create/validate | NOT_RUN | PROVEN R4 · estrutural local | NOT_AVAILABLE: primitive repo-side |
| prompt/create/validate | NOT_RUN | PROVEN R4 · estrutural local | NOT_AVAILABLE: primitive repo-side |
| notebook/create/validate | NOT_RUN | PROVEN R4 · estrutura; runtime NOT_RUN | NOT_AVAILABLE: não executa notebook |
| README agregador/create/validate | NOT_RUN | PROVEN R4 · estrutural local | NOT_AVAILABLE: primitive repo-side |
| README Objeto avulso/create | BLOCKED em A1 | BLOCKED em A1 | BLOCKED em A1 |
| skill/create | BLOCKED em A1 | BLOCKED em A1 | BLOCKED em A1 |
| convert de qualquer tipo | BLOCKED em A1 | BLOCKED em A1 | BLOCKED em A1 |
| write/apply novo da A1 | não implementado | não implementado | não implementado |
| piloto antigo create/readme/agregador/apply | não ampliado; fora da nova primitive | H-WIN-PILOTO histórico, não recertificado nesta autoria | não provado por A1 |

## Autoridade e decisão de promoção

A persistência de evidência/overlay requer `evidence_authorized=True`, mas essa flag não autentica a pessoa. O resultado não autoriza aplicação, homologação ou promoção de policy. Destino, conteúdo, operação e base ficam vinculados ao registro; host real é observado no processo e no bundle externo.

Nenhuma célula candidata está marcada `PROVEN` agora. O retorno do laboratório poderá provar validação estrutural no host utilizado; não fecha automaticamente os gaps de execução de exemplos, ligação ao produto, Free/Genie, conversão, skill ou composição da certificação SER. `current_level` permanece L2.

## Atualização A2

A R4 converte somente as células Windows/NTFS de validação estrutural local acima
para `PROVEN`. Linux permanece `NOT_RUN`; Free/Genie permanece `NOT_AVAILABLE`
para a primitive repo-side. A2 adiciona Receipt de domínio para essas mesmas
células, mas o Receipt da nova candidata ainda é `NOT_PROVEN` até recertificação.
Nenhuma célula de write/apply foi promovida.
