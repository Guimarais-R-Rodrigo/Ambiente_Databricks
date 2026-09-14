# V05 — evidências e limites de teste

## Fechamento técnico pré-registro final — PR #37

No head limpo `efb9dd3270ac0f5240612cf3b7e9e39111e51c46`, o run V05 `34832202757` concluiu com **success** em todas as etapas: 31/31 testes específicos V05, 14/14 testes de sessões, 359/359 regressões `test_temas*.py`, 12/12 regressões visuais V00, validação estrutural/documental e gate de escopo.

A PR final #37 foi aberta em draft contra a `main` pós-D05 `24ffce298ed543755eb15d5d7c553d02ce15e73e`. Os checks iniciais da PR concluíram com **success**:

| Execução | Workflow | Resultado |
|---|---|---|
| 34832408423 | CI local reproduzível | success |
| 34832408496 | Regressões da instrumentação V00 | success |
| 34832408407 | Contrato de temas V01 | success |
| 34832408460 | Núcleo de temas V02 | success |
| 34832408426 | Visual Lab notebook V05 | success |

V03 e V04 possuem workflows com filtros de caminho próprios e não foram disparados por esta PR. Seus testes continuam dentro da regressão `test_temas*.py` executada pelo workflow V05. O run `34831939535`, imediatamente anterior à atualização numérica, mediu as contagens finais do README raiz; a única reprovação naquele head eram as 14 linhas ainda antigas, posteriormente substituídas pelos valores medidos.

Este registro não transforma PASS de GitHub Actions em homologação Databricks. Browser/runtime, frontend de widgets, acessibilidade, p95, ACL real, reinício e UAT continuam fora do alcance automatizado descrito aqui. A alteração documental deste registro requer seus próprios checks no head subsequente da PR.

## Fechamento pós-D05/R13 — 14/09/2026

A candidata corrente está em `codex/temas-v05-fechamento-r13-20260913`, reconciliada com a `main` `24ffce298ed543755eb15d5d7c553d02ce15e73e`, que já incorpora a D05 documental. A comparação confirmou merge-base nessa `main`, `behind=0` e diff líquido restrito aos artefatos V05 antes das atualizações documentais de fechamento.

### Execuções desta retomada

| Execução | Head | Resultado e alcance |
|---|---|---|
| 34797774791 | `147541a5` | FAILURE no gate específico: 30/31 testes V05 passaram; a única falha era a asserção documental literal `não publica`. Não houve evidência de regressão funcional. |
| 34798200237 | `4447fb28` | V05 específica 31/31 e sessões 14/14; regressão `test_temas*.py` 359/359; V00 legado 12/12. O workflow terminou FAILURE no validador documental: o README `theme_lab` ainda não obedecia às 15 seções do contrato 1.0.0 e as métricas coladas no README raiz estavam desatualizadas. |

O run `34798200237` usou Python 3.12.14 e instalou ipywidgets 8.1.9 no runner. Os testes de launcher confirmaram seleção de preset, salvamento/reabertura sem código do operador, roundtrip de base/proposta/histórico/revisão e recusa de proposta adulterada. Isso fecha as lacunas funcionais que constavam nos checkpoints anteriores **para o contrato Python testado**; não transfere a conclusão para browser/runtime Databricks.

A migração do README do objeto ao contrato editorial 1.0.0 foi aplicada depois desse run. Portanto `34798200237` permanece corretamente registrado como FAILURE e não é evidência da árvore documental posterior.

### Métricas medidas antes da migração editorial final

No head `4447fb28`, o validador mediu 14 skills; 16 prompts/161 campos; 88 helpers; 217 Markdown/1367 links relativos; 80 notebooks/101 links; 76/76 READMEs operacionais + 3/3 exemplares; 62 pastas de objeto; 60 formas de pasta; 62 contratos de dados; 60 contratos de entrada; 79 notebooks com saída real; 62 módulos com docstring em português; 72 arquivos do molde; 60 objetos exercitados; 217 arquivos Python AST; 1334 arquivos na identidade do repositório e 1814 links fora da raiz analisada.

Essas contagens **não devem ser copiadas como finais** após novas edições. O README raiz só pode ser atualizado com a saída medida na árvore de fechamento.

## Limites da evidência automatizada

Os testes Python exercitam objetos ipywidgets, callbacks no kernel, serialização, hashes e filesystem temporário do runner. Eles não provam:

- renderização/callbacks no navegador Databricks;
- teclado, leitor de tela, contraste percebido ou zoom;
- p95 de interação no workspace real;
- ACL real da pasta de persistência;
- comportamento operacional após reinício do ambiente;
- UAT por pessoa iniciante;
- submissão, aprovação ou publicação.

Mocks de permissão testam tratamento de erro, não permissões Databricks reais.

---

## Histórico preservado — reconciliação R08 em 13/09/2026

A main `d5945e04328609878f63857cc15cf5e5039b3e75` foi incorporada à branch V05 pela composição `5cace7f876b2bdb2a1eecaa73e3f7958dfd2764e`. O conflito consistia nas contagens do README, que foram atualizadas no commit `57062e86e0741e88fcd0b30c902ff57ece4be1c8` a partir da execução real. Nenhuma asserção ou implementação foi alterada nessa reconciliação.

| Execução | Composição | Resultado e alcance |
|---|---|---|
| 34761074646 | Head 5cace7f; checkout de teste eacbe44 | 31/31 V05, 345/345 temas e 12/12 legado visual aprovados; FAILURE por 14 divergências de contagem no README. |
| 34761250018 | Head 57062e8 | Workflow V05 completo com success após atualização das contagens. Não é homologação Databricks. |
| 34761250014 / 34761250034 / 34761250027 | Head 57062e8 | Workflows V00, V01 e V02 com success. |
| 34761250016 | Head 57062e8; checkout de teste 1d83a94 | CI geral FAILURE: oito de nove etapas passaram; falta a seção do objeto no inventário do Manual Técnico. Validador estrutural: zero falhas e zero avisos. |

Os 345 casos do primeiro run incluem os 31 originais V05 e as 16 regressões adicionais, além de V01–V04. Não somar as execuções repetidas. Essa rodada usou Python 3.12.14, pandas 3.0.5, Plotly 7.0.0 e ipywidgets 8.1.9 no runner. Os seis casos de UI pulados no CI geral permanecem SKIP nesse run; o workflow específico instala ipywidgets e executa os testes da interface Python. Os sete SKIPs do gate de transição dependem de Spark e não são aprovações.

O log do CI após as contagens confirmou como única falha `test_manual_inventory_covers_current_objects`, procurando a seção `hub_snippets.visual.theme_lab`. Não remover ou enfraquecer essa guarda. A aprovação estrutural do pacote não substitui a completude do Manual.

A comparação main → composição confirmou somente 16 arquivos acrescentados, sem alteração de qualquer arquivo anterior da main. A comparação candidata anterior → composição preservou todos os arquivos próprios V05. As cópias previamente geradas do objeto foram herdadas byte a byte por seus blobs. Não foi executado novo render completo, smoke Databricks, benchmark, publicador ou auditoria independente nessa rodada.

## Rodadas anteriores

| Execução | Árvore/commit examinado | Resultado |
|---|---|---|
| 34733481224 | 5245c0f | 30 de 31 casos V05 aprovados; falha na frase explícita do README. Rodada reprovada. |
| 34733554922 | a45ebd6 | 31/31 V05, 329/329 temas e 12/12 legado visual aprovados; validador reprovado por links, contrato do exemplo, falta de saída e contagens. Rodada reprovada. |

Os 329 casos incluem os 31 da V05. Não somar reexecuções ou subTest como novos casos. As bibliotecas ipywidgets foram reais no runner; não houve browser Databricks.

## Retomada R07 — histórico

A main avançou com R07 para `b73bbb91961f9ba5f9031d648c42ec0891b63347`. A composição precisou repetir os gates; resultados anteriores não eram aprovação da nova árvore. O snapshot auxiliar por workflow foi recusado antes da criação do arquivo. A branch auxiliar permaneceu sem mudanças e nenhuma proteção foi relaxada.

## Bateria necessária para a árvore final

Preservar os testes específicos V05 e sessões; executar V00, V01–V05, CI geral, conferência de API, fonte/derivado, documentação, exemplo sintético e preservação da `main` corrente. Toda edição documental posterior exige nova execução; resultados de heads anteriores permanecem históricos.

## Evidência que continua faltando

Runtime e interface Databricks, navegador, teclado/leitor de tela, zoom, contraste percebido, p95 da prévia, autorização real do diretório e uso por iniciante sem ajuda não foram homologados. Nenhum PASS Python substitui esses gates.

[Estado e bloqueios](CHECKPOINT_V05.md)
