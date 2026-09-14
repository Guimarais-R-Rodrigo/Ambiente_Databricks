# Sistema de Temas do Hub — execução por sprints

## Estado vigente — V00–V08 integradas no Git

A V08 foi aceita por Rodrigo em 14/09/2026 e integrada pelo PR #42. O head final validado foi `9af5615d79b02cbd86f5a6d084444c83f203ae03` e o merge efetivo na `main` é `622d2c962a80998cf990b57036f7ae503bfc0458`. A árvore do merge é idêntica à árvore da candidata testada.

A [V08 — integração transversal com skills, padrões e Manual](V08/README.md) reconcilia orientação e roteamento com as capacidades V02–V07 já integradas. Skills deixam de competir com o contrato visual, o template EDA deixa de possuir política própria de tema e o Manual/padrões passam a descrever `ResolvedTheme`, Visual Lab, geração editorial, consumidores V07 e limites atuais de forma consistente.

A [matriz transversal](V08/MATRIZ_INTEGRACAO.json), o [registro de testes](V08/TESTES.md) e o [checkpoint V08](V08/CHECKPOINT_V08.md) distinguem superfícies alteradas, decisões de não edição, failures preservados e a proibição de mudança runtime. A V08 não altera módulos Python de `hub_snippets` ou `hub_scripts`.

Antes do merge, o gate final comprovou V08 **22/22**, regressões V01–V08 **405/405**, V00 **12/12**, validador **0 falhas / 0 avisos** e `V08_RUNTIME_EDIT=0`. Depois do merge, os dez workflows da `main` — CI geral e V00–V08 — concluíram com `success`.

Nenhuma publicação Databricks, alteração de ACL/compute, execução remota Spark/SQL/MLflow, promoção visual ou homologação de browser/acessibilidade/UAT foi realizada. A V08 também não prova seleção determinística de skill pela Genie Code. A V09 não foi iniciada.

## Estado integrado anterior — V06 integrada no Git

A V06 foi aceita por Rodrigo em 14/09/2026 e integrada pelo PR #38. O head final validado foi `70499e1803ce0d61a148a0da975c4f52611046e0` e o merge efetivo na `main` é `418946de8d1e95e87cbfd9df528ddcced5075237`. A árvore do merge é idêntica à árvore do head final testado.

A [V06 — assets e geração orientados por tema](V06/README.md) evolui o compositor editorial v2 sem criar uma segunda fonte de verdade: `theme_id` é resolvido pelo núcleo V02, o renderer recebe um derivado controlado do `ResolvedTheme`, recursos congelados continuam protegidos por SHA-256 e variantes candidatas ficam em `.artifacts/`, fora do pacote visual ativo.

No head final da PR, CI geral, V00, V01, V02, V04, V05 e V06 concluíram com `success`. Depois do merge, os oito workflows disparados por `push` — CI geral e V00–V06, incluindo V03 — também concluíram com `success`. As evidências e IDs estão no [registro de testes V06](V06/TESTES.md) e no [checkpoint V06](V06/CHECKPOINT_V06.md).

Essa integração Git não equivale a publicação Databricks nem às homologações de navegador/runtime, acessibilidade, ACL, promoção visual ou UAT. Nenhuma publicação Databricks foi executada; naquele fechamento, a V07 ainda não havia sido iniciada.

## Registro anterior — V05 candidata em fechamento

V00–V04 estavam integradas no Git e a documentação viva dessas versões havia
sido reconciliada pela D05, integrada à `main` no commit
`24ffce298ed543755eb15d5d7c553d02ce15e73e`. Naquele checkpoint, a V05 estava em
branch separada de fechamento e ainda não possuía aceite, merge ou publicação.

A [V05 — Visual Lab em notebook](V05/README.md) acrescenta uma superfície opt-in
de autoria: escolha guiada de ponto de partida, edição de tokens, comparação com
dados sintéticos e persistência/reabertura de sessão com base, proposta e
histórico. O [checkpoint V05](V05/CHECKPOINT_V05.md) e o
[registro de testes](V05/TESTES.md) distinguem contratos Python exercitados de
homologação Databricks ainda pendente.

Para quem nunca entrou no Hub: nada é ativado automaticamente. O laboratório
precisa ser aberto explicitamente no notebook, não muda o padrão da equipe e não
publica temas. O
[guia de primeiro uso](../../../ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md)
explica o fluxo operacional da V05.

Não houve publicação Databricks, auditoria independente ou homologação visual da
V05. Browser/runtime, acessibilidade, p95, permissões reais da persistência e UAT
por iniciante permanecem gates separados. A frase histórica de que a V06 não
havia sido iniciada descreve esse checkpoint anterior.

## Estado integrado anterior — V04 aceita e integrada no Git; documentação viva reconciliada em D05

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

Para quem nunca entrou no Hub: não há nada para ativar no Databricks. A V04 não
instala seletor, não cria CSS global e não migra notebooks automaticamente. Leia o
[README V04](V04/README.md), o [checkpoint](V04/CHECKPOINT_V04.md) e o
[guia operacional](../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).

### Entradas históricas preservadas

A evolução continua navegável pela [V01 — contrato e experiência](V01/README.md) e pelo [guia de primeiro uso da V01](V01/GUIA_PRIMEIRO_USO.md). Esses arquivos são referência histórica/contratual e não substituem o estado corrente da iniciativa.

Não houve publicação Databricks, auditoria independente ou homologação visual.
O aceite e a integração Git da V04 estão concluídos; esses gates operacionais
permanecem separados. A [D05 documental](RECONCILIACAO_DOCUMENTAL_D05.md) sincroniza os rótulos vivos pós-merge e **não** constitui entrega funcional da V05.

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
foram incorporadas na V05; os parágrafos históricos abaixo permanecem como
registro do estado observado em seus respectivos fechamentos.

## Estado e limites

A V00 é uma candidata de diagnóstico. A extração automatizada precisa de revisão
semântica independente e aceite antes da V01. Nada nesta pasta autoriza merge,
publicação, troca de paleta ou alteração de arquivos congelados.

O plano aprovado na conversa distingue V00–V14. Esta entrega cobre apenas V00;
não substitui aquele plano por uma promessa de todas as sprints concluídas.

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
`5a7b33d7137f88c1ec80315de1b422293b3ba206`. Sem publicação Databricks; a frase
histórica de que “V05 ainda não foi iniciada por este fechamento” descreve o
fechamento V04. O estado corrente da iniciativa está no início deste documento.
