# Sistema de Temas do Hub — execução por sprints

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
