# Revisão transversal após 22 casos SD — 2026-09-29

(Codex) Revisão das correções já publicadas e das falhas observadas nas
primeiras 22 tentativas SD. [Revisão anterior](REVISAO_TRANSVERSAL_DADOS_AUSENTES_2026-09-29.md)
e [correções já aplicadas](CORRECOES_TRANSVERSAIS_2026-09-29.md) permanecem
históricas; esta rodada não as substitui. Dois auditores independentes
revisaram, somente em leitura, domínios/evidência e roteamento/arquitetura.

## Transferências com causa demonstrada

| Achado | Mecanismo anterior útil | Aplicação nesta rodada | Limite |
|---|---|---|---|
| SD-CE-P dispensou skill e executou Spark; SD-FE-N citou Cross-EDA sem indicador | Roteamento especializado e distinção resposta/execução | Instrução geral limita dispensa a dúvida conceitual curta; execução especializada exige skill/contrato | SD-FE-P era conta conceitual e SD-ST-N podia rotear ao Tutor; seus oráculos ficam históricos, sem forçar seleção |
| SD-FE-N escolheu tabelas e chave depois de perguntar, sem esperar resposta | Cross-EDA já separava proposta de entrada confirmada | Instrução geral explicita que tabela encontrada é candidata e pergunta material pendente interrompe execução | Não duplica gates de Cross-EDA nem proíbe descoberta autorizada |
| SD-BL-N ofereceu SER12 sintético para possível dado real de modelo implantado | SER04 já separou origem sintética de tabela real e passou em D01 | Instrução geral e SER12 exigem origem confirmada; dado real/amostrado/agregado não vira sintético | Não copia restrição “inline” de SER04 para perfis que aceitam objetos em memória; finalizador SER12 já existia |
| SD-ST-A atribuiu potência “quase nula” sem alternativa; SD-ST-B usou 64% sem independência | Monitoramento já distinguiu p-valor de potência | Estatística agora exige alternativa/desenho/cálculo para potência e condiciona `1−0,95^20` à independência | Cálculo D/p e recusa de seleção pós-hoc permanecem evidências positivas |
| SD-BL-P executou quando o pedido era planejar e extrapolou métricas da demonstração | Regra global já separa plano de efeito | Baseline reforça plano versus execução e delimita métricas de fixture ao request criado | `X|Y` sintético não é leakage automático; ver errata abaixo |
| SD-ST-P/T01 executou arquivo de verificador sem chamar a função; outros READMEs mostravam argumentos posicionais para API keyword-only | SER04 recebeu CLI explícita e passou D01 | READMEs Baseline/Monitoramento mostram chamada da função importada com argumentos nomeados, `valid=true` e retenção de payload | Não copiar CLI de SER04 para verificadores de objetos Spark/model sem necessidade demonstrada |

Não foram alterados runner, schema, policy, controller ou mecanismo de
autorização. A correção de linguagem do SER10 (autorização versus readback)
já estava na skill/README; a resposta SD-BL-A descumpriu essa distinção.
O finalizador SER12 também já era obrigatório. Esses achados exigem
reteste/observação, não duplicação de mecanismo.

## Errata de auditoria — SD-BL-P

A primeira análise classificou como leakage o gerador que sorteou `X`
condicionalmente ao rótulo sintético `Y`. Isso foi excessivo: uma simulação
conjunta pode ser construída como `P(Y)P(X|Y)` sem implicar que o rótulo
futuro estivesse disponível à decisão real. O notebook não traz fonte real
para avaliar proveniência operacional. A [evidência T01](genie_evidencias/SD-BL-P_T01.md)
ganhou errata explícita, e a matriz foi corrigida. Permanecem o pedido de
**planejamento** transformado em execução, dados demonstrativos criados pelo
Genie e a leitura excessiva de Brier/AUC em uma fixture diminuta. O `VALID`
do verificador certifica os bindings do request gerado, não generalização.

## Verificação local e limites

- 27 testes SER04/SER09/SER11/SER12 PASS; sem novos testes que apenas
  espelhem o texto.
- `tools/render_simulado.py --write`: 658 arquivos renderizados a partir do
  fonte; antes do render, a única diferença entre fonte/derivado era o
  conjunto de sete arquivos desta correção e o README de raiz não copiado.
- `tools/validate_assistant.py`: 15 skills, 14 contratos de enforcement,
  zero falhas/avisos; instruções 12.418/20.000 caracteres.
- Testes locais confirmam estrutura e contratos existentes, não adesão do
  Genie nem homologação. T01/T02 e retestes anteriores conservam as versões
  em que ocorreram. Próximos testes requerem nova versão publicada, chat
  novo e evidência vinculada ao hash da publicação.

Publicação Free/readback: **CONCLUÍDOS** após a reconciliação descrita abaixo.
Não houve promoção de policy, merge nem replicação no workspace de trabalho.

## Reconciliação remota antes da publicação

A pré-checagem integral do Free encontrou sete diferenças previstas por esta
revisão e uma atualização remota de `hub-ml-micromodelos/SKILL.md` feita pela
frente paralela. A publicação foi interrompida. O arquivo remoto acrescentava
distinções entre ambiente E1, fixture textual fornecida e execução de runtime,
além do caminho da policy integrada. A revisão remota foi incorporada
integralmente à fonte B1 e ao derivado pelo renderer, preservando uma cópia
local anterior na pasta privada de evidências. O novo SHA-256 do arquivo é
`93e51ac4ca25f2c3bd88c6cb6a40e7e494fd9bf1852824cd4575628cf24351f2`.
Após a reconciliação, o renderer e o validador passaram novamente. A nova
pré-checagem remota encontrou somente os sete ajustes planejados. A primeira
transferência caiu por conexão de rede; a leitura direta dos oito arquivos
críticos mostrou que MM04 permanecia idêntico e que os sete ajustes ainda não
haviam chegado. O reenvio concluiu com código zero. O readback direto dos
oito arquivos e o readback integral passaram: **657/657 conteúdos iguais, zero
ausentes, zero obsoletos, zero divergências**. Há um arquivo de plataforma
gerenciado separadamente (`.assistant/.mcp_servers.json`). Hash normalizado
do pacote publicado: `7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
Essa evidência comprova publicação e conteúdo; não substitui os testes Genie
em chat novo.
