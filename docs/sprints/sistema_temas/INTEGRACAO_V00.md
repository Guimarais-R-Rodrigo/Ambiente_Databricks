# Integração Git da V00

## Para quem nunca entrou no Hub

Esta entrega acrescenta ferramentas de diagnóstico e proteção, testes e
documentação. Não muda cores nem exige executar células no Databricks. O uso
atual do Hub permanece igual. O seletor de temas ainda não foi implementado.

Rodrigo autorizou aprovar e integrar esta candidata. Integração Git significa
incorporar os arquivos na branch principal; não significa publicar no ambiente
do trabalho ou certificar a experiência de usuários iniciantes.

## Referências da rodada

- Main preservada: `5493f7db68f397ad7040485cb09bad53eb79be74`.
- Candidata anterior: `3f65e9414bc1e7bd52493b267ae4fe1cbd0f783d`.
- Ancestral comum: `8744157fe9c3e0603f689fb2bcad52445e96cb41`.
- GitHub Actions run: `34705527229`.

## Escopo e limites

Os oito gates existentes permanecem inalterados. Produto, espelho e Manual são
comparados byte a byte com a main. As evidências históricas não são reescritas.
A falha editorial global anteriormente reproduzida por referência ao catálogo
removido permanece registrada; não foi reclassificada como PASS nem corrigida
nesta integração. Os testes Node globais não são reexecutados por este workflow.
Spark, Databricks, Apps, AI/BI, leitura por iniciante e auditoria independente
continuam pendentes. A autorização de integração não substitui essas evidências.

## Recuperação

Não publicar ou sobrescrever workspaces a partir deste registro. Em caso de
regressão atribuída a esta integração, o mantenedor deve criar um PR de reversão
do merge #8, preservar alterações posteriores e repetir os gates. Não usar reset
ou force-push da main. O histórico do PR preserva base, candidata e commit final.

## Execução

O relatório de comandos abaixo é preenchido somente após execução. Os logs
completos ficam no artefato deste run, separado dos resultados históricos.
