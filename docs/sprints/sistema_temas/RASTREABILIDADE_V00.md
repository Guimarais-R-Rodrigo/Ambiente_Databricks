# Rastreabilidade V00 ao planejamento aprovado

Esta matriz se refere aos identificadores do catálogo de 198 cenários entregue
na conversa em 12/09/2026, base f748c144. Não declara todos esses cenários
executados: a V00 só implementa sua instrumentação inicial. Estado definitivo de
cada comando está no resumo da rodada. PARCIAL não equivale a PASS do requisito.

| Cenário | Evidência implementada | Limite de aceite |
|---|---|---|
| BASE-01 | Inventário nominal automático com caminho e linha | PARCIAL: falta classificação semântica completa e dono |
| BASE-02 | Consulta live de main e PR #5, refs e ADRs registrados | Documentado; reconferir antes da integração |
| BASE-03 | Mutantes de worktree suja e guardas antigas de empacotamento | Conferir logs; não houve promoção real |
| BASE-04 | Mutantes de Git/lista/produto sem ocorrências | Testes do inventariador |
| BASE-05 | AST, assinaturas, constantes, fachadas e imports | PARCIAL: relações dinâmicas/relativas e revisão nominal |
| BASE-06 | Fixtures fixas, arrays, Plotly e HTML antes/depois | PARCIAL: ampliar exemplos dos demais consumidores |
| BASE-07 | Hashes de arquivos, posição/seção de imagens e mutantes | PARCIAL: não é leitura de navegador |
| BASE-08 | Marcador oficial reutilizado e caso FILE/NOTEBOOK | Execução local; nenhum objeto importado no remoto |
| BASE-09 | Gates na base e candidata, logs e causa de falha separados | Falha global histórica registrada, não apagada |
| BASE-10 | Divergência do guia geral contra v2 registrada | PENDENTE de reconciliação documental |
| LEG-01 | Suíte antiga e chamadas legadas de Plotly/cabeçalho | PARCIAL: todos os imports afetados exigem revisão do inventário |
| ART-01 | Suíte existente do publicador e proteção por hashes | Revisor deve conferir aderência nominal dos mutantes |
| PUB-01 | Suíte de publicação com mocks, sem credenciais | Não é observação em destino remoto |
| DOC-01 | Guias distinguem vigente/candidata/histórico/derivado | PENDENTE de teste de leitura com pessoa nova |

V01, configuração de temas, widgets e integração App/AI-BI não foram antecipados.
Auditoria independente e aceite humano permanecem pendentes.
