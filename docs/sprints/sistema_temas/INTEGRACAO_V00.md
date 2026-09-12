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

### Primeira rodada da composição

Commit executado: `718462e7090638903b9b752ed810bb504405fd48`.

- `python -B tools/ci_local.py --verbose`: PASS (código 0).
  - APROVADO: 0 falha(s), 0 aviso(s)
  - Ran 45 tests in 0.231s
  - OK
  - Ran 39 tests in 1.330s
  - OK
  - Ran 43 tests in 0.028s
  - OK (skipped=7)
  - Ran 49 tests in 0.260s
  - OK
  - Ran 14 tests in 0.141s
  - OK
  - Ran 12 tests in 0.175s
  - OK
  - alcance : gate local — não cobre Databricks, Spark nem Genie Code
  - APROVADO: 8 etapa(s)
- `python -B tools/tests/test_inventario_visual.py`: PASS (código 0).
  - Ran 27 tests in 0.678s
  - OK
- `python -B tools/tests/test_visual_legado_v00.py`: PASS (código 0).
  - Ran 12 tests in 0.380s
  - OK
- `python -B tools/tests/test_baseline_visual_runner.py`: PASS (código 0).
  - Ran 9 tests in 0.086s
  - OK
- `python -B -m unittest discover -s tools/readme_visuals/tests -p test_*.py -v`: PASS (código 0).
  - Ran 29 tests in 0.125s
  - OK

Após registrar os resultados, o mesmo conjunto é reexecutado sobre o commit
de documentação final antes do push. A comparação do inventário e das capturas
sintéticas com a main também é refeita, com JSONs próprios no artefato desta
rodada. O resultado dessas verificações está no run identificado acima. SKIPs
não significam homologação Spark. Revisão própria não é auditoria independente.
O workflow temporário com permissão de escrita e seu script foram removidos
antes do commit; permanece apenas o CI V00 com permissão de leitura.
