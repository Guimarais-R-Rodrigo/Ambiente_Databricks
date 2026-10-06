# Novas funcionalidades — área experimental

> **Arquivo histórico do protótipo.** Não instalar ou testar esta cópia como produto atual. Use a [versão canônica](../ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md). Comandos, próximos passos e resultados abaixo preservam a experiência original; não concedem autorização para nova execução.

Esta pasta reúne propostas implementadas para avaliação antes de qualquer promoção ao produto. Seu conteúdo é versionado no Git, mas **não é fonte canônica do Hub publicado**, não integra `ambiente_fonte/` e não deve ser copiado em bloco para um workspace.

## Por onde começar

Consulte [Skills experimentais](skills/README.md). A primeira entrega é o [Concierge Hub](skills/hub-ml-concierge/README.md): descoberta e composição dos recursos que já existem no Hub.

## Isolamento

Nada nesta pasta é automaticamente promovido para `.assistant/skills/`. A localização de descoberta nativa e as condições de teste estão documentadas no pacote. Esta entrega não modifica instruções, skills ativas, Manual Técnico, catálogo, ferramentas de publicação, ADRs aceitos nem o simulado.

A solicitação de manter a entrega fora dos arquivos canônicos prevalece sobre o fluxo ordinário de promoção. Por isso, a alteração é registrada no [CHANGELOG experimental](CHANGELOG.md), sem editar o `CHANGELOG.md` da raiz. Aprovar um protótipo não equivale a autorizar publicação no Free ou no trabalho.

## Próxima ação

Leia o README da funcionalidade, execute seus testes locais e revise as pendências humanas. Só depois de autorização específica faça a integração documentada em `ambiente_fonte/`.
