# Checkpoint V02 — candidata remota para aceite

## Estado para o usuário

A V02 está materializada na branch remota `codex/temas-v02-review-20260912` e no
PR #14. Ainda não foi integrada à `main` nem publicada no Databricks. O núcleo
funcional foi validado remotamente no commit
`921f898cbae859b8f6a91862a7b65291c9806906`; qualquer alteração posterior na PR,
mesmo documental, precisa repetir os checks no novo head antes do aceite.

O pedido de Rodrigo autorizou executar e evoluir a V02, não concedeu aceite para
merge desta candidata. A V01 e sua correção documental continuam preservadas. A
V03 não foi iniciada. Nenhum notebook legado precisa mudar por causa desta entrega.

## Conciliação vigente — 12/09/2026

Base reconciliada da candidata: `1be947b0a62c3b0b85fa3cd5692f474b9066d85f`,
após integração R03-A/R03-B. O PR #14 está quatro commits funcionais à frente dessa
base antes desta correção documental e zero atrás. O README novo usa o contrato
editorial 1.0.0 e conserva as quinze seções dos objetos afetados.

A validação remota do commit funcional executou CI geral, regressões V00, contrato
V01 e núcleo V02 com sucesso. O núcleo V02 executou 105 testes e o exemplo sintético;
o CI geral aprovou nove etapas e manteve sete casos dependentes de Spark como SKIP.
Esses SKIPs não contam como aprovação. O gate declara explicitamente que não homologa
Databricks, Spark ou Genie Code.

A branch local `codex/temas-v02-implementacao`, a branch auxiliar `codex/temas-v02`
e os baselines anteriores permanecem apenas como rastreabilidade histórica. Para
revisar a entrega atual, use o PR #14 e sua branch de revisão.

## Fonte e promoção — rodada inicial

Base inicial: `836f23684cf76ee1f3d7898d44acb70d32a7ff59`. O baseline preparatório
`34711683992` executou somente verificações anteriores e não comprovava o núcleo V02.
A fonte promovida permaneceu byte a byte no contrato 0.1.0; APIs novas são aditivas.
O schema antigo foi movido, não mantido como segunda fonte ativa. O
[relatório](../../../testes/sistema_temas/V02/RELATORIO_EXECUCAO.md) documenta as
rodadas, resultados e limites.

O transporte para o GitHub foi fail-closed. Tentativas de transporte que falharam
continuam registradas como falhas e não são usadas como evidência positiva. A branch
de revisão aponta para a candidata verificada; arquivos auxiliares de transporte não
fazem parte do diff do PR.

## Critérios e limites

Antes do aceite, o head vigente do PR precisa manter verdes os workflows de CI geral,
V00, V01 e V02. Conferir também que a mudança documental não introduziu links quebrados
nem divergência de renderer. Revisão do autor e code review automático não equivalem
a auditoria independente.

Avaliação com iniciante, Windows, Databricks, Spark, widgets, Apps e AI/BI permanecem
não homologados. A dívida editorial global não é encerrada por este núcleo. O aceite
da V02 autoriza no máximo sua integração Git quando explicitamente solicitado; não
implica publicação nem início da V03.

## Recuperação e retomada

Sem merge, arquive a candidata ou corrija na própria branch. Depois de eventual
integração, preparar reversão em branch preservando mudanças posteriores e o schema
consumido por cada versão; repetir validação, render e CI. Nunca resetar a `main`,
editar o espelho manualmente ou publicar pacote antigo para desfazer trabalho local.

A próxima ação é concluir os checks do head atual e apresentar a V02 para aceite
explícito. Não iniciar V03 antes dessa decisão.

[Escopo](README.md) · [Testes](TESTES.md)
