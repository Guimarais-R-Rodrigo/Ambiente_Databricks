# Aceite editorial, integração e contrato 1.0.0

**Data:** 2026-09-12. **Registro:** ChatGPT. **Decisão humana:** Rodrigo, nesta
conversa, respondeu “Aprovo, pode seguir” após a entrega da candidata R02-I,
com recomendação explícita de integrar o PR nº 7, registrar o aceite, estabilizar
o contrato e iniciar a R03-A. Não foi simulada uma aprovação de revisor no GitHub.

## Integração efetivamente realizada

Main `8744157fe9c3e0603f689fb2bcad52445e96cb41` e head
`494ab7c210c9aa95ea2e1e405f484ea09b4e3e7a` foram reconferidas; a CI
permanente `34702547585` estava concluída com sucesso. O PR nº 7 saiu de
rascunho e foi integrado pelo método merge, com proteção por head SHA esperado.
GitHub confirmou `merged: true`, commit
`5493f7db68f397ad7040485cb09bad53eb79be74`. O comentário
`5647015898` no PR registra a autorização e o resultado.

O PR nº 7 acumula as entregas dos PRs nº 5 e nº 6. Eles não devem ser integrados
novamente como frentes independentes. Seus registros e branches foram
preservados; este aceite não exige apagar histórico.

## Efeito editorial

O ADR-0012 recebe ratificação datada. O texto explicativo e os quinze títulos
do contrato continuam iguais: versão **1.0.0**, em vez de candidata. Os nove
READMEs anteriores (três exemplares e seis pilotos) mudam somente no marcador
de versão. O checklist e as entradas de navegação passam a indicar a fase
atual. O controle de migração permanece ancorado em seu baseline original.

## Limites e próxima parada

Aceite editorial do padrão e dos pilotos não é teste de compreensão observado
com usuários, auditoria A1+ nem homologação Databricks. R03-A produz sete novos
textos para revisão própria e posterior aceite; não recebem aprovação humana
antecipada. Não há publicação, alteração de modelo, paleta ou CSS.

A estabilização e a R03-A são preparadas em `codex/readmes-r03a`, separadas da
main já integrada. Seu PR deve ser revisto antes de novo merge. A R03-B não
inicia automaticamente. [Estado e entregas](README.md).
