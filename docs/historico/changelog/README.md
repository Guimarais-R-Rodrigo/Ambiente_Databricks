# Cronologia integral preservada

O [snapshot de 13/08 a 06/10/2026](2026-08-13_a_2026-10-06.md) conserva as
198 entradas e 4.501 linhas do CHANGELOG da base
`126a2e125cca2251527f187a58696243414c6859`, na ordem original. A entrada R09
permanece depois da entrada de 13/08, sem ordenação retroativa. É história,
não estado corrente nem autorização de execução.

## Integridade e recuperação

O [manifesto](manifest.json) registra commit, paths, SHA-256 do arquivo e de cada
entrada, ranges de linhas e as duas transformações de href. O original tem
306.701 bytes e SHA-256
`f2ce1cb816ff02e4f68e71379f77c7552b8452fcbc0dcd8048af9e7b57ddee1e`.
O snapshot tem 306.703 bytes e SHA-256
`1369e890eda968fd18f1a605ffe187fc4d0ea04e6940e6420744765a96ddcfd2`.

As únicas mudanças são os dois links relativos: `docs/sprints/` passa a
`../../sprints/`, e `docs/handoffs/` a `../../handoffs/`, nos hrefs completos
listados no manifesto. Reverter esses dois hrefs recupera os bytes originais;
não substituir strings gerais nem normalizar whitespace. Ambos os destinos
continuam existentes. O teste abaixo verifica recuperação, entradas, ordem,
hashes e as onze exceções históricas migradas por path + hash de linha + origem:

```bash
python -B tools/tests/test_ai_history.py -v
```

O snapshot é imutável. Nenhuma exceção geral foi criada para esta pasta:
referências novas, modificadas ou exceções obsoletas devem falhar. Os 87 demais
registros de exceção, snapshots e baseline da campanha IA anterior permanecem
inalterados. As revisões daquele mapa são históricas, não homologação desta mudança.

## Como encontrar a informação

- Mudança relevante atual: [marcos da raiz](../../../CHANGELOG.md).
- Estado vigente: [owners por frente](../../ai/context/projeto.md#owners-vivos).
- Razão arquitetural: [índice único de ADRs](../../decisions/README.md).
- Falha recorrente: [classes de defeito e guardas](../../auditoria/README.md#classes-de-defeito-que-viraram-guardas), depois a prova citada.
- Retomar leitura antiga que citava uma data/seção de `CHANGELOG.md`: procure
  o título correspondente no snapshot. Links históricos não são reescritos em massa.

Não é necessário ler este arquivo inteiro para iniciar manutenção. O bundle
integral pode incluí-lo; a redução do contexto por tarefa exige seleção explícita.

[Voltar ao histórico](../README.md)
