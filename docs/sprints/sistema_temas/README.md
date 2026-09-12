# Sistema de Temas do Hub — execução por sprints

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
serão incorporadas quando a respectiva interface for implementada.

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
