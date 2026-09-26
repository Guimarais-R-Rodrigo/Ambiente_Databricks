# MM03 — testes e gates

Os IDs M01–M09 referem-se ao contrato nesta pasta. A suíte permanente é
`tools/tests/test_micromodelo_mm03_metadata.py`; só usa stdlib e fixture sintética.

| Superfície | Casos discriminantes |
|---|---|
| M01 | binding divergente, resposta de outro catálogo, referência lógica indevida, identificador com path/SQL |
| M02 | schemas sem objetos, objetos sem detalhes, shortlist exata, desconhecida, duplicada, vazia e anterior à descoberta |
| M03 | negado, indisponível, parcial após paginação, coleção observada sem claim global |
| M04 | paginação, limite de páginas/itens, ciclo, duplicatas, resposta oversized, limites inválidos |
| M05 | keys proibidas, tipo inválido, nullable indevido, tags duplicadas, referências de coluna inválidas |
| M06 | instruções em descrição/tag não mudam chamadas, socket/processo bloqueados nos testes, higiene rastreável |
| M07 | JSON duplicado, não finito, arquivo grande, operação desconhecida, stream duplicado |
| M08 | CLI real em subprocesso, arquivo intocado, mensagens sem eco, ordem determinística, ausência de imports executores |
| M09 | envelope sem autorização/claim de Databricks, constraints NOT_VERIFIED |

## Desenvolvimento observado

Linux / CPython 3.13.5, materialização parcial dos arquivos novos (não clone completo):
R1: 39 métodos PASS. R2: 45 métodos PASS após seis regressões adicionais e
endurecimento do tipo object_type/estado agregado de observação parcial.
Nenhum desses resultados é smoke Windows, FULL, auditoria independente ou teste
Databricks. Logs de desenvolvimento ficam no pacote externo da sessão.

## Próximo smoke canônico

Primeiro concluir PREPARACAO_LOCAL.md. No SHA posterior à preparação documental,
rodar serialmente, parando no primeiro FAIL obrigatório:

```text
python -B -m unittest discover -s tools/tests -p test_micromodelo_mm03_metadata.py -v
python -B -m unittest discover -s tools/tests -p test_micromodelo_mm02_fingerprint.py -v
python -B -m unittest discover -s tools/tests -p test_micromodelo_mm01.py -v
python -B -m unittest discover -s tools/tests -p test_micromodelo_mm01_r02.py -v
python -B -m unittest discover -s tools/tests -p test_micromodelo_mm01_r03.py -v
python -B tools/micromodelo_mm03_metadata.py --fixture tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json --catalog catalogo_sintetico --schema crm_sintetico --candidate crm_sintetico.eventos_sinteticos
python -B tools/validate_assistant.py --root ambiente_fonte
python -B tools/validate_assistant.py --conferir-readme
```

Esperados nesta candidata: 45 MM03; 30 MM02; 47+3+1 MM01. Zero testes coletados ou
skip em MM03 não é PASS. A CLI deve solicitar cinco operações no exemplo, deixar
apoio_sintetico sem detalhes e emitir ESCOPO_OBSERVADO/sem autorização de dados.

O snapshot deve ser medido na árvore preparada; não somar arquivos/links por
estimativa para chamá-los de saída do validator. Fonte e derivado não mudaram.

## Certificação posterior

Smoke verde apenas torna a candidata elegível ao freeze. Definir/executar FULL
proporcional single-shot separadamente, incluindo CI local transversal, estado
Git, logs reais, bundle externo e lint de bytes do ZIP com paths também escapados.
Não reexecutar a FULL MM01 por reflexo. Não alterar perfil histórico SEF.
Auditoria independente em contexto separado, contraditório, fechamento mínimo,
revalidação final e aceite humano precedem merge. MM04 permanece NOT_STARTED.

GitHub Actions: DEFERRED_NO_CREDITS; não disparar/reexecutar deliberadamente.
Databricks/Genie: NOT_RUN e fora da evidência sintética. Não converter isso em
homologação nem alegar que API real já esteja implementada.
