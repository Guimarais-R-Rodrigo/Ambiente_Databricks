# Revisão paralela da candidata de laboratório de Micromodelos

**Data:** 2026-09-29. **Candidata lida pelos três revisores:** branch `micromodelos/autonomia-local-v2`, commit `2bc23dad021ed5e798af80cfe862699d4cc2a416`, tree `a98670ac3d23ba54c0515f93e66139bf4174dfa6`, base `origin/main@4ba7f551767d847381df1556ed937116258fa77d`. O [plano](PLANO_PARALELIZACAO_LAB.md) separou três superfícies e manteve arquivos compartilhados sob integração serial.

Três agentes novos revisaram os arquivos diretamente em modo somente leitura. Os autores das correções eram depois diferentes dos agentes que conferiram cada patch: B revisou A, C revisou B e A revisou C. Isto é revisão cruzada interna proporcional ao laboratório, sem pretensão de auditoria institucional externa ou homologação E2.

## Achados e resolução

| ID | Achado | Resolução nesta candidata | Limite |
|---|---|---|---|
| A1 | Fluxo MM04 devolvia a spec MM01 dentro do JSON, sem artefato YAML na CLI. | `known --output-yaml <dir>/micromodelo.yaml` agora é opt-in, valida round-trip MM01, grava sem sobrescrever e remove somente arquivo recém-criado se escrita/readback falhar. O modo discover recusa essa opção. | Isso comprova YAML local E0, não YAML criado pelo Genie. |
| A2 | Campos de briefing alterados não entravam em `proveniencia.registros`. | Criação/revisão registram apenas campos fornecidos que mudaram, com `PROPOSTO`, origem `briefing fornecido` e `request_ref`; aprovação/medição permanecem vazias. | Fonte observada MM03 conserva `DESCOBERTO` e snapshot próprio. |
| A3 | P1/P2c têm ressalvas de redação/proveniência; P2/P2b tiveram FAILs. | Classificação histórica preservada em [briefings](TESTE_BRIEFINGS_MM04_E1.md). | Sem captura independente de chamadas internas do Genie; não promover PASS de resposta a certificação. |
| A4 | `CLAUDE.md` e plano vivo traziam estado Genie/prompt anterior aos retestes. | Corrigidos com a sequência P1/P2/P2b/P2c e seus limites. | Relatórios históricos não foram reescritos. |
| A5 | Skill L1/audit não possui runner ou Receipt. | Fronteira confirmada na policy e no contrato estático. | L2/L3 e E2 dependem de gates futuros. |
| B1 | Runs com `score_mean` não guardavam denominador/cobertura de score. | `score_count` integra a allowlist, é validado contra população e trio de estatísticas, e recebe `scores_emitidos` dos dois callers. | Média continua heurística; run não mede holdout independente. |
| B2 | `score_habilitado` podia contradizer métricas/contrato e ainda fechar run. | Rejeição em ambas as ordens de chamada; `True` sem campo de score também é recusado antes de log_params. Falhas não marcam `mm06.complete=true`. | Wrapper legado `run_governado` mantém sua rota separada. |
| B3 | Célula opcional Free fazia só descoberta de schema/objetos. | `RUN_METADATA_CHECK` exige catálogo, schema e `LAB_TABLE` sintéticos; confirma objeto `TABLE` observado antes de details e informa status de columns, tags e constraints. | A prova Free anterior do adapter permanece histórica; este novo código requer nova execução E1 para prova remota. |
| B4 | README do tracking dizia que Free não fora executado. | Atualizado com a prova sintética anterior, data, limites e sem link que escape do produto publicado. | A versão nova com `score_count` só tem readback MLflow E0 nesta rodada. |
| C1 | Classificação não hashável em MM12 lançava TypeError instável. | Tipo validado antes de membership; lista/dict em ambos os lados geram `MigrationLabError('INVALID_CLASSIFICATION')`. | Ensaio segue restrito a legado fictício. |
| C2–C3 | MM10 agregado fornecido não vincula run/janela/fingerprint; MM12 só compara saídas fictícias. | Mantidos `SUPPLIED_UNVERIFIED`, `DRAFT` e `corporate_v1_verified=false`; registrados como dependências E2, sem prometer integração real. | Exigem produto governado, piloto real, V1 congelada e proveniência do legado. |
| C4–C5 | MM11 aparecia amplamente como N/A e `CLAUDE.md` dizia Genie pendente. | O scoring E0 foi delimitado; integração visual e monitoramento pós-publicação permanecem `NOT_RUN`. Estado Genie vivo corrigido. | MM11 corporativa não foi dispensada. |

Na revisão cruzada, B encontrou um risco de arquivo YAML parcial em A1, corrigido com teste de falha de readback; C encontrou duas contradições adicionais no patch B, corrigidas com testes para `score_habilitado=True` sem campo e VIEW homônima. Os três revisores terminaram com PASS por inspeção sobre os patches finais de outros autores, sem executar testes na rechecagem. Achados E2 e ressalvas conversacionais permanecem visíveis.

## Validação local da integração

- `PYTHONUTF8=1; python -B -m unittest discover -s tools/tests -p 'test_micromodelo_*.py'`: **192/192 PASS**, sem skip.
- `python -B tools/validate_assistant.py --root ambiente_fonte`: primeira execução detectou link do README para fora do produto; após correção, **APROVADO, 0 falhas, 1 aviso** de nove diretórios locais `__pycache__`.
- Renderer canônico: **583 arquivos**. Comparação da árvore de usuário: **582/582 arquivos iguais byte a byte**, nenhum faltante/extra.
- MLflow E0 em virtualenv local: três runs DEVELOPMENT/VALIDATION/SCORING concluídas; readback dos três confirmou `mm06.complete=true`, `population=6`, `score_count=4` e `score_mean=57.5`, iguais ao agregado do piloto. O primeiro script avulso de readback não declarou o opt-in do backend de arquivos; outra verificação assumiu incorretamente dois scores, embora a fixture emita quatro. A inspeção do agregado resolveu a expectativa e o readback final passou. São diagnósticos de verificação, não falha de produto.
- `git diff --check`: PASS antes do fechamento documental.

Os testes focais dos autores passaram: A 15, B 24, C 3. As baterias integradas acima são o gate local principal; testes focais são evidência adicional, sem somar contagens como se fossem execuções independentes de cobertura total.

## Reexecução E1 dos bytes revisados

Após a integração local no commit `29bc5a75bb979e37bacf9a7fe2b1bffe7bcb72cc`, o kit r4 foi gerado da allowlist sintética: 32 arquivos de conteúdo, `manifest.json` e ZIP SHA-256 `87880472161a132787598d6b88d2ccabd4af316ad0146228cfc72f1a92992532`. O perfil `FREE` passou o guard de host/usuário não corporativo. O pacote foi importado em pasta pessoal nova; readback **33/33 PASS** com comparação integral dos arquivos, normalizando apenas quebras de linha de notebooks como faz o Workspace.

Três jobs one-shot, em notebooks derivados apenas por ativação das células opcionais, terminaram `SUCCESS`: código sintético; tracking MLflow com DEVELOPMENT, VALIDATION e SCORING, `mm06.complete=true` relido para cada run e `score_count=4` igual a `scores_emitidos`; metadata somente leitura da tabela sintética já criada no Free, observada como `TABLE`, com colunas, tags e constraints em `OBSERVED` e cobertura `ESCOPO_OBSERVADO`. IDs de jobs e runs ficam em `.artifacts/r4_run_*.json` e no resultado do Free, fora do Git. O job de código concluiu todos os asserts do notebook; o tracking e a metadata emitiram `R4_TRACKING_PASS` e `R4_METADATA_PASS`. Não houve leitura de linhas de cliente, execução corporativa nem teste novo de Genie nesta reexecução.

Esta prova E1 vale para os bytes do kit r4; não converte os resultados históricos de Genie em certificação da skill nem concede publicação ou promoção de nível.

## Integração B1 e estado externo

Na conferência somente leitura, fonte e derivado B1 de skill, contrato e policy MM04 tinham hashes idênticos aos da PR #116; a linha de encaminhamento MM04 nas instruções também coincidia. O checkout B1 continua com alterações extensas de outras frentes e não foi alterado por esta rodada. O [registro B1](RECONCILIACAO_B1_PRE_GATES_MM04_2026-09-29.md) preserva a observação anterior e a atualização posterior.

GitHub Actions está indisponível por saldo da conta; seus jobs não iniciados continuam `BLOCKED_EXTERNAL_CI`, sem PASS presumido. O laboratório usa testes locais e revisão proporcional conforme o [plano operacional](PLANO_EXECUCAO_LAB.md). E2, publicação institucional, promoção L3 e migração real permanecem fora deste fechamento.
