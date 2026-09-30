# G6 B1: reconciliação do legado e prova Free da versão atual

(Codex) A investigação de 2026-09-30 separa o **G6 congelado do PR #115** da
**entrega de skills atual do PR #117**. Não reclassifica o FAIL histórico, não
muda o manifesto congelado e não promove policy.

## Estado do G6 congelado

- `g6_recovery --validate-local`: `PASS`, sem acesso remoto. Manifesto SHA-256
  `b8880e08f37e3ada04f14150c040362620f0fb94741d6022fec461debab70f93`;
  pacote de recuperação SHA-256
  `015368427080f63620c02e3d4ae39a99fef678b36348384e4b17cc2a7d55fec7`.
- `g6_recovery --reconcile`: `PASS` somente de leitura no Databricks Free.
  Diretório histórico contém exatamente o probe SER03, com hash normalizado
  idêntico ao fonte; o probe SER05 está ausente. Nenhum write foi feito nesse
  diretório nesta investigação.
- O manifesto original vincula G6 ao candidato R7
  `08c2a93c4c9dede1e759abe28c07242b4116f47e` e exige que os bytes do
  produto permaneçam iguais. O PR #117 alterou **90 arquivos de
  `ambiente_fonte/.assistant`** desde R7. Logo, criar o probe SER05 ausente,
  isoladamente, não fecha a identidade de produto do G6 original.
- O verificador congelado exige **20 variantes Genie literais**, cada uma em
  chat novo, além dos dois outputs Free. Uma busca dos prompts exatos nas
  evidências `.md`/`.txt` versionadas encontrou **0/20**; resultados de chats
  semanticamente próximos não foram reclassificados como variantes congeladas.

## Prova sintética da versão atual, separada do G6 formal

Os dois probes congelados passaram localmente contra o produto atual (5/5
casos em Safra e 5/5 em Cross-EDA). A primeira submissão Free
`842694405929853` não produziu output literal: o Jobs tratou o
`SystemExit(0)` terminal de cada notebook como falha e tentou cada tarefa
duas vezes. O job terminou `INTERNAL_ERROR`; essa tentativa permanece FAIL.

Para distinguir falha de transporte de falha analítica, um adaptador
determinístico manteve todo o corpo de cada probe e substituiu **somente** o
bloco terminal por `run_probe()` + `dbutils.notebook.exit(JSON)`. Os dois
notebooks adaptados foram importados em caminhos novos da pasta pessoal
`hub_lab`, com readback normalizado. O job sintético
`193650374713787` terminou `SUCCESS` sem retry configurado:

| Skill | Casos internos | Output Free | Verificador de output congelado |
|---|---:|---|---|
| Safra / SER03 | 5/5 PASS | [JSON derivado do resultado](g6_reconciliacao_evidencias/ser03_free_output.json) | `VALID` |
| Cross-EDA / SER05 | 5/5 PASS | [JSON derivado do resultado](g6_reconciliacao_evidencias/ser05_free_output.json) | `VALID` |

A [proveniência](g6_reconciliacao_evidencias/proveniencia.json) fixa o commit
fonte, os hashes dos probes e adaptadores, os IDs das tarefas, o readback e os
hashes dos outputs. O campo `notebook_output.result` do Jobs foi convertido em
objeto JSON e reformatado para os relatórios locais; os arquivos versionados
derivam desses relatórios e também normalizam CRLF para LF. A proveniência
distingue os hashes do resultado literal, do envelope Jobs, do relatório local
e do arquivo versionado. Os três
notebooks temporários criados nesta investigação
continuam na pasta pessoal para inspeção; nenhuma tabela, policy ou pacote do
produto foi alterado. O job não é homologação Genie nem prova de que o produto
remoto ainda possui os bytes R7.

## Decisão da trilha atual

Em 2026-09-30, o usuário escolheu **requalificar a versão atual**, aproveitando
as evidências Free/Genie que resistem à revisão e testando somente lacunas.
Esta escolha não altera o G6 congelado nem lhe atribui PASS. A matriz de aceite
da versão atual será registrada separadamente, com identidade do produto e
grau de cada evidência.

## Trilhas consideradas

Há duas trilhas distintas:

1. **G6 histórico literal:** restaurar/qualificar o produto R7 em ambiente
   isolado, concluir a criação residual do probe SER05 sob autorização vinculada
   e coletar as 20 variantes Genie exatas. Isso preserva o contrato antigo,
   mas repete trabalho conversacional e não certifica automaticamente a versão
   mais nova do PR #117.
2. **Requalificar a versão atual:** criar um novo contrato de aceite, sem editar
   o G6 congelado, que vincule o head atual e avalie quais evidências Genie
   existentes são suficientes, antes de pedir novos prompts. Os dois outputs
   Free acima podem compor essa requalificação, sujeitos a verificação da
   identidade do pacote remoto e do adaptador.

O G6 histórico permanece `FAIL_PARTIAL_RECOVERY_AUTHORED`; nenhum merge ou
promoção decorre desta decisão de requalificação.
