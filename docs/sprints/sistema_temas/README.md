# Sistema de Temas do Hub — execução por sprints

## Etapa atual — V05 candidata em fechamento

V00–V04 estão aceitas e integradas no Git. A [V05 — Visual Lab](V05/README.md)
está em desenvolvimento/revisão na PR #26, atualmente reconciliada com a main
que já contém a R08. Não há aceite V05, merge, publicação Databricks ou início
da V06.

O [checkpoint vigente](V05/CHECKPOINT_V05.md) é a fonte do estado técnico da
candidata. O [guia de primeiro uso](../../../ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md)
explica a operação da prévia pessoal quando o mantenedor preparou pacote, caminho
e dependências. A interface candidata ainda não conclui escolha visual de presets,
linhagem automática até a base original nem reabertura autônoma pelo operador.

Os testes Python e de CI permanecem separados da homologação no Databricks,
da acessibilidade, do teste com pessoa iniciante e da publicação. Um JSON salvo
é rascunho: não equivale a submissão, aprovação ou padrão de equipe.

## Etapa concluída anterior — V04 aceita e integrada no Git

V00–V04 estão integradas no Git. A V03 foi mesclada pelo PR #16 no commit
`b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2`; depois, R04-A, R04-B, R05 e R06
foram incorporadas à `main` durante a evolução paralela do repositório. A V04 foi
reconciliada com essas mudanças antes de sua integração final.

A [V04 — componentes HTML, estilos e tabelas](V04/README.md) foi aceita por
Rodrigo em 12/09/2026 e integrada pelo PR #21 no commit
`5a7b33d7137f88c1ec80315de1b422293b3ba206`. Ela acrescenta apenas rotas opt-in
`_resolvido` para badges, divisores, KPI cards, cabeçalho, índice e tabela pandas,
além da materialização central de CSS em `constants.styles`. As APIs legadas
permanecem o default.

Para quem nunca entrou no Hub: não há nada para ativar no Databricks por causa
da V04. Ela não instala seletor, não cria CSS global e não migra notebooks
automaticamente. Leia o [README V04](V04/README.md), o
[checkpoint](V04/CHECKPOINT_V04.md) e o
[guia operacional](../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).

### Entradas históricas preservadas

A evolução continua navegável pela [V01 — contrato e experiência](V01/README.md)
e pelo [guia de primeiro uso da V01](V01/GUIA_PRIMEIRO_USO.md). Esses arquivos
são referência histórica/contratual; não substituem o estado corrente da V05.

Não houve publicação Databricks, auditoria independente ou homologação visual
pelo aceite Git da V04. A frase histórica de que V05 ainda não havia sido
iniciada descreve o fechamento daquela sprint, não o estado corrente.

## Aceite de integração Git — 12/09/2026

Rodrigo autorizou explicitamente: “Pode aprovar e integrar”. A autorização cobre
integrar a instrumentação V00 no Git; não equivale a publicação no Databricks,
auditoria independente ou homologação dos ambientes. A reconciliação e os testes
novos estão em [Integração V00](INTEGRACAO_V00.md). O estado efetivo do merge é
registrado no PR #8; não se presume merge pela existência deste documento.

As notas anteriores abaixo são históricas. Classificação semântica completa,
leitura por usuário iniciante, auditoria independente, capturas Databricks e
correção do validador editorial global continuam pendentes. A V01 pode seguir
como desenho e contrato conforme a orientação anterior de Rodrigo; não há
homologação integral nem entrega de funcionalidades visuais nesta integração.

## Registro anterior (histórico)

Esta pasta registra a evolução da identidade visual. É documentação de manutenção;
não é um novo catálogo de helpers nem uma interface já instalada no Databricks.

## Para quem nunca entrou no Hub

Nesta primeira sprint, **você não precisa alterar nem executar nada no Databricks**.
O trabalho é registrar como o Hub está hoje, para que mudanças futuras de cor,
título e imagem possam ser comparadas sem perder o funcionamento atual.

Comece por [V00 — o que está sendo entregue](V00.md). Depois consulte
[o resultado técnico da execução](../../testes/sistema_temas/V00/RELATORIO_TECNICO.md).
A palavra PASS em uma execução significa apenas que aquele teste passou. Não
significa que o seletor de temas já existe, que o visual foi aprovado ou que a
funcionalidade foi publicada.

O [checkpoint](CHECKPOINT_V00.md) é a referência para saber o que ainda impede
avançar à sprint seguinte. O [registro de achados](ACHADOS_V00.md) explica problemas
preexistentes e limitações sem atribuí-los à nova funcionalidade.

## Para o mantenedor

Leia [como reproduzir o diagnóstico](V00.md#reproduzir-o-diagnostico), use uma cópia
Git limpa e mantenha as evidências fora da árvore do produto. Não execute estes
scripts em um notebook corporativo. `tools/` é manutenção local, não componente
a publicar no workspace.

O Manual Técnico existente permanece dono da orientação operacional do produto:
[Manual Técnico](../../../MANUAL_TECNICO.md). V00 não o altera porque não entrega
uma nova operação ao usuário do Hub. As instruções de primeiro uso do laboratório
são parte da V05 e permanecem candidatas enquanto a PR #26 não for aceita.

## Estado e limites

A V00 é uma candidata de diagnóstico. A extração automatizada precisa de revisão
semântica independente e aceite antes da V01. Nada nesta seção histórica autoriza
publicação, troca de paleta ou alteração de arquivos congelados.

O plano aprovado na conversa distingue V00–V14. Esta documentação histórica não
substitui aquele plano por uma promessa de todas as sprints concluídas.

Consulte também a [rastreabilidade ao plano](RASTREABILIDADE_V00.md).

## Testes permanentes da instrumentação

Depois de preparar as dependências conforme o guia V00, as três suítes podem ser
executadas separadamente na raiz do checkout:

```powershell
python -B tools/tests/test_inventario_visual.py
python -B tools/tests/test_visual_legado_v00.py
python -B tools/tests/test_baseline_visual_runner.py
```

A primeira verifica o inventário e seus casos de recusa; a segunda exercita os
contratos antigos de Plotly e HTML; a terceira verifica contagens, logs, falhas e
timeouts do relatório. O runner comparativo executa as três automaticamente.

`.github/workflows/temas-v00-ci.yml` mantém essas regressões em pull requests e
pushes na main, com permissão somente de leitura. Não substitui as sete etapas
do gate existente, a comparação visual global ou a auditoria independente.

A automação temporária utilizada para preparar e registrar as evidências foi
removida da árvore final. Não há workflow de escrita recorrente, credencial
Databricks ou publicação automática nesta entrega.

## Continuidade — V03/V04

A V03 foi aceita e integrada pelo PR #16; seu adaptador Plotly continua opt-in. A
[V04](V04/README.md) estende a mesma arquitetura aos componentes HTML e à tabela
pandas e foi aceita/integrada pelo PR #21 no commit
`5a7b33d7137f88c1ec80315de1b422293b3ba206`. Sem publicação Databricks; a V05
passou a ser desenvolvida posteriormente na PR #26.