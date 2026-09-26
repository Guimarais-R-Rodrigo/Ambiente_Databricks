# Checkpoint V02 — aceita e integrada

## Estado para o usuário

A V02 foi aceita explicitamente por Rodrigo em 12/09/2026 e integrada à `main`
pelo PR #14 no commit `d4cabdca4ac68c0a2edbd7f9f621f68962c8f6b8`.
O merge preservou exatamente a árvore do head validado
`cda22c2963660ecd94e77698fcd7a5e56eca7092`.

Os quatro workflows pós-merge na `main` concluíram com sucesso: CI geral,
regressões V00, contrato V01 e núcleo V02. Isso confirma a integração Git, mas não
homologa Databricks, Spark, widgets, Apps, AI/BI ou qualquer tema operacional.
A V03 ainda não foi iniciada. Nenhum notebook legado precisa mudar por causa da V02.

## Aceite e integração — 12/09/2026

Rodrigo declarou: “Também é o meu aceite, siga”. O aceite cobriu a V02 tecnicamente
validada e autorizou sua integração Git. A autorização não incluiu publicação no
Databricks, mudança de aparência, homologação operacional ou início da V03.

Antes do merge, o head final `cda22c2963660ecd94e77698fcd7a5e56eca7092`
passou os quatro workflows permanentes e o code review automático final. O único
achado remoto anterior, P2 sobre registro no `CHANGELOG.md`, foi corrigido,
respondido e encerrado antes do merge.

## Conciliação vigente

A V02 partiu da base reconciliada
`1be947b0a62c3b0b85fa3cd5692f474b9066d85f`, após integração R03-A/R03-B. A
integração foi feita com merge explícito do PR #14 e SHA esperado do head. A árvore
do merge é `d67f05b3cd1b5b829443aeabfcb284de1a5b25e3`, idêntica à árvore do head
candidato validado.

A validação final executou CI geral, regressões V00, contrato V01 e núcleo V02 com
sucesso. O núcleo V02 executou sua suíte e o exemplo sintético; o CI geral manteve
os casos dependentes de Spark como SKIP. SKIP não conta como aprovação. O gate
continua declarando que não homologa Databricks, Spark ou Genie Code.

## Fonte e promoção

O schema ativo permanece em
`ambiente_fonte/.assistant/hub_padroes/identidade_visual/theme.schema.json`, sem
segunda fonte editável concorrente. As APIs novas da V02 são aditivas e não migram
consumidores legados automaticamente.

O [relatório](../../../testes/sistema_temas/V02/RELATORIO_EXECUCAO.md) documenta as
rodadas anteriores, inclusive falhas de transporte e correções encontradas durante
a revisão. Essas falhas permanecem históricas e não são reclassificadas como PASS.

## Critérios e limites

Integração Git: CONCLUÍDA. Aceite do usuário: CONCEDIDO. Publicação Databricks:
NÃO EXECUTADA. Auditoria independente: PENDENTE. Avaliação com usuário iniciante:
PENDENTE. Windows, Spark, widgets, Apps e AI/BI: NÃO HOMOLOGADOS.

A V02 entrega o núcleo de carga, validação e resolução; não aplica aparência, não
registra template Plotly automaticamente, não altera HTML existente e não publica
um tema operacional. Esses próximos consumidores pertencem a sprints posteriores.

## Recuperação e retomada

Para desfazer a integração, preparar uma reversão em branch a partir da `main`,
preservar alterações posteriores e repetir validação, render e CI. Nunca resetar a
`main`, editar o espelho manualmente ou publicar um pacote antigo para desfazer a V02.

A próxima sprint planejada é V03 — integração explícita do núcleo com Plotly,
preservando o comportamento legado por padrão. A V03 ainda não foi iniciada.

[Escopo](README.md) · [Testes](TESTES.md)
