# Retirada do protótipo e catálogo de ferramentas — 07/10/2026

Autoria: Codex, executor delegado na mesma sessão; revisão de integração pertence
ao coordenador. Base Git: `8dd8da57de89122241890b8b6b059fd2f9be25d0`.
Escopo autorizado pelo usuário: eliminar `novas_funcionalidades/` e manter as
ferramentas úteis com orientação de função, estado e efeitos.

## Alterações

- Retirada dos 19 arquivos versionados do protótipo Concierge; nenhuma remoção
  do Concierge canônico, dos helpers ou das ferramentas gerais.
- Manifesto `docs/historico/concierge-manifest.json` conservado byte a byte;
  snapshots e decisões aceitas conservam os caminhos que existiam na época.
- Rota viva `docs/historico/concierge.md` explica consulta/recuperação em Git,
  distingue a disposição antiga no manifesto da situação atual e aponta ao produto.
- `tools/verify_concierge_history.py` verifica todos os blobs no commit original,
  SHA-256, tamanho, unicidade e inventário não vazio. Histórico ausente reprova.
- Teste de presença física substituído por prova de recuperabilidade com casos
  negativos de hash alterado, blob ausente, duplicação, vazio e path inseguro.
- Inventário visual perde a classificação experimental do diretório retirado.
- `tools/CATALOGO.md` documenta famílias, uso atual/histórico, efeitos e dependências;
  `tools/README.md` aponta ao catálogo e ao README dos workflows.

## Validação do executor

| Comando | Resultado observado |
|---|---|
| `python -B tools/verify_concierge_history.py` | PASS: 19 blobs; tamanhos e SHA-256; sem restauração |
| `python -B -m unittest discover -s tools/tests -p test_ai_history.py -v` | PASS: 17 testes |
| `python -B -m unittest discover -s tools/tests -p test_inventario_visual.py -q` | PASS: 27 testes, 2 skips declarados |
| `test_concierge_integracao.py` antes do render | FAIL: 2 de 12 por espelho inexistente no worktree isolado; não atribuir ao produto |
| `python -B tools/validate_assistant.py` após copiar documentos pares | FAIL: 1 link do relatório copiado já aponta a `ambiente_databricks`, ainda ausente neste executor; checks da fonte sem erros |
| Render e nova execução de integração | NOT_RUN neste executor: validação global depende da renomeação coordenada; executar na árvore integrada |

A integração precisa retirar as três exceções antigas de referências IA cuja
origem era `novas_funcionalidades/.../fontes.md` no mapa vivo; o snapshot datado
continua intacto. Precisa também conferir a composição com a renomeação da fonte
para `ambiente_databricks` e com a sucessão do Manual, executadas por outros agentes.
O README dos workflows e os documentos de análise/plano/inventário foram
copiados do destino principal ao clone isolado somente para conferir seus links
durante os gates; sua autoria e integração permanecem no coordenador. O relatório
copiado já aponta à fonte renomeada, ainda ausente nesta árvore isolada. A validação global final pertence
à árvore integrada com todos esses consumidores presentes.

## Recuperação e limites

A prova usa o commit fixo `126a2e125cca2251527f187a58696243414c6859`; leia a
[rota de recuperação](../historico/concierge.md). Não depende de GitHub, rede,
Databricks ou credencial. Um ZIP só de produto não conserva a história Git.
Nenhuma publicação, instalação, runtime, push ou merge foi realizada.
A recuperação de bytes não homologa a execução do protótipo antigo.
