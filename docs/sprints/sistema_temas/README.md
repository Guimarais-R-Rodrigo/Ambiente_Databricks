# Sistema de Temas do Hub — execução por sprints

## Estado vigente — V05 candidata em fechamento; V00–V04 integradas no Git

V00–V04 estão integradas no Git. A documentação viva dessas versões foi reconciliada pela D05, integrada à `main` no commit `24ffce298ed543755eb15d5d7c553d02ce15e73e`. A V05 está em branch separada de fechamento e **não** possui aceite, merge ou publicação.

A [V05 — Visual Lab em notebook](V05/README.md) acrescenta uma superfície opt-in de autoria: escolha guiada de ponto de partida, edição de tokens, comparação com dados sintéticos e persistência/reabertura de sessão com base/proposta/histórico. O [checkpoint V05](V05/CHECKPOINT_V05.md) e o [registro de testes](V05/TESTES.md) distinguem contratos Python exercitados de homologação Databricks ainda pendente.

Para quem nunca entrou no Hub: nada é ativado automaticamente. O laboratório precisa ser aberto explicitamente no notebook, não muda o padrão da equipe e não publica temas. O [guia de primeiro uso](../../../ambiente_fonte/.assistant/hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md) explica o fluxo operacional da candidata.

Não houve publicação Databricks, auditoria independente ou homologação visual da V05. Browser/runtime, acessibilidade, p95, permissões reais da persistência e UAT por iniciante permanecem gates separados. A V06 não foi iniciada.

### Estado integrado anterior — V04 e D05

A V03 foi mesclada pelo PR #16 no commit `b83a7cde84d7a44fc8a1fed996fda4f8b5b1eec2`. A [V04 — componentes HTML, estilos e tabelas](V04/README.md) foi aceita por Rodrigo em 12/09/2026 e integrada pelo PR #21 no commit `5a7b33d7137f88c1ec80315de1b422293b3ba206`.

A V04 acrescentou somente rotas opt-in `_resolvido` para badges, divisores, KPI cards, cabeçalho, índice e tabela pandas, além da materialização central de CSS em `constants.styles`. As APIs legadas permanecem o default. A [D05 documental](RECONCILIACAO_DOCUMENTAL_D05.md) sincronizou os rótulos vivos pós-R13 e não constituiu entrega funcional V05.

### Entradas históricas preservadas

A evolução continua navegável pela [V01 — contrato e experiência](V01/README.md), pelo [guia de primeiro uso da V01](V01/GUIA_PRIMEIRO_USO.md), pela [V02](V02/README.md), pela [V03](V03/README.md) e pela [V04](V04/README.md). Esses arquivos registram seus próprios estados e não substituem o checkpoint corrente V05.

## Aceite de integração Git — V00, 12/09/2026

Rodrigo autorizou explicitamente “Pode aprovar e integrar” para a instrumentação V00. A autorização não equivalia a publicação no Databricks, auditoria independente ou homologação dos ambientes. A reconciliação e os testes ficaram registrados em [Integração V00](INTEGRACAO_V00.md) e no PR #8.

As notas abaixo são históricas. Classificação semântica completa, leitura por usuário iniciante, auditoria independente e capturas Databricks pertencem aos gates explicitados em cada sprint.

## Registro anterior (histórico)

Esta pasta registra a evolução da identidade visual. É documentação de manutenção; não é um novo catálogo de helpers nem uma interface instalada automaticamente no Databricks.

## Para quem nunca entrou no Hub

Na V00, a orientação era não alterar nem executar nada no Databricks: o objetivo inicial era registrar como o Hub se comportava para permitir comparações futuras sem perder compatibilidade.

Comece por [V00 — o que está sendo entregue](V00.md). Depois consulte [o resultado técnico da execução](../../testes/sistema_temas/V00/RELATORIO_TECNICO.md). A palavra PASS em uma execução significa apenas que aquele teste passou; não certifica seletor, visual ou publicação.

O [checkpoint V00](CHECKPOINT_V00.md) registra o estado daquela etapa, e o [registro de achados](ACHADOS_V00.md) separa problemas preexistentes da nova funcionalidade.

## Para o mantenedor

Leia [como reproduzir o diagnóstico](V00.md#reproduzir-o-diagnostico), use uma cópia Git limpa e mantenha as evidências fora da árvore do produto. `tools/` é manutenção local, não componente a publicar no workspace.

O Manual Técnico é a fonte operacional integrada do produto: [Manual Técnico](../../../MANUAL_TECNICO.md). As instruções específicas do Visual Lab estão no objeto V05 e devem permanecer coerentes com o inventário do Manual.

## Estado e limites

O plano aprovado distingue V00–V14. Cada sprint só autoriza seu próprio escopo; a existência de documentação futura não significa entrega antecipada. Integração Git e publicação/homologação Databricks são estados distintos.

Consulte também a [rastreabilidade ao plano](RASTREABILIDADE_V00.md).

## Testes permanentes da instrumentação

As regressões V00 podem ser executadas separadamente na raiz do checkout:

```powershell
python -B tools/tests/test_inventario_visual.py
python -B tools/tests/test_visual_legado_v00.py
python -B tools/tests/test_baseline_visual_runner.py
```

`.github/workflows/temas-v00-ci.yml` mantém essas regressões em pull requests e pushes na main, com permissão somente de leitura. Não substitui comparação visual global ou auditoria independente.

A automação temporária utilizada nas rodadas históricas foi removida da árvore final. Não há workflow de escrita recorrente, credencial Databricks ou publicação automática nesta entrega.

## Continuidade — V03/V04 (histórico)

A V03 foi aceita e integrada pelo PR #16; seu adaptador Plotly continua opt-in. A V04 estendeu a arquitetura aos componentes HTML e tabela pandas e foi aceita/integrada pelo PR #21. A frase histórica “V05 ainda não foi iniciada por este fechamento” descrevia o fechamento V04; o estado vigente está no início deste documento.
