# Integração R03-A/R03-B com a main V01

## Estado

Reconciliação e integração autorizadas explicitamente por Rodrigo em 12/09/2026. A bateria completa da composição foi executada no run `34712073970`; este passo apenas materializa remotamente a mesma árvore determinística já validada.

## Bases

- R03-B acumulada: `d61fedbf111075aa3f238b46d2d64834b185bc10`.
- main com V01 aceita/integrada e alinhamento documental: `836f23684cf76ee1f3d7898d44acb70d32a7ff59`.
- R03-B já contém a R03-A e o contrato de README 1.0.0.

## Conflitos e resolução

A composição encontrou somente `CHANGELOG.md`, `README.md` e `docs/sprints/README.md` em conflito. O changelog preserva as entradas exclusivas das duas frentes e uma única cópia do histórico comum; o README preserva a narrativa R03 e recebe contagens recalculadas; o índice de sprints preserva R03 e o estado vigente de V00/V01.

## Preservação

ADR-0013, contrato, fixtures, verificadores, testes e workflow V01 permanecem byte a byte iguais à main. Os 19 READMEs operacionais, três exemplares, contrato 1.0.0, conteúdo de produto/espelho e controle de migração permanecem iguais à R03-B. Nenhum helper, API, paleta/CSS, formulário, skill ou objeto analítico é alterado pela integração.

## Limites

Sem publicação Databricks, V02 ou R04-A. Sete testes opcionais Spark do gate continuam SKIP, não PASS. Auditoria independente e homologações operacionais continuam separadas.
