# Reconciliação da candidata MM04 no checkout B1 — 2026-09-29

(Codex) O usuário confirmou que as alterações feitas no Databricks Free devem
ser preservadas e escolheu explicitamente incorporá-las ao repositório B1.
Esta é uma importação de candidata L1 estática, sem ativação de A2, promoção
de níveis de outras skills, aceite MM03 ou certificação da sprint MM04.

## Proveniência preservada

No Free havia uma 15ª skill `hub-ml-micromodelos`, com `SKILL.md` e
`execution_contract.json`, uma entrada nova em `policy.json` e uma linha de
roteamento em `.assistant_instructions.md`. Entre os 654 arquivos gerenciados
pela publicação anterior, só policy e instruções haviam mudado. Os dois arquivos
da skill eram extras no remoto; todos foram exportados antes de qualquer escrita.
Cópias e comparação: `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d01/`.

| Superfície | SHA256 remoto preservado | Incorporação |
|---|---|---|
| Skill MM04 `SKILL.md` | `e7964e906acca0f8a6376a44229a05c557c23afff6aad606fdea7e5ad6a00fba` | byte a byte |
| Contrato MM04 | `73649097eea918543dc0117556432b064ad3a455ea647facf7e94aaf8c4dae22` | byte a byte |
| `policy.json` | `4d8c4981f7b728b5c83d467d2d4d2e047b21f2f47299ec125e961906e22e05fc` | byte a byte |
| `.assistant_instructions.md` | `7906923a4d39e975504cd7fec100aaae5150c6509a37393bb9d57faa269fa50f` | byte a byte |

A policy anterior tinha 14 entradas. A nova entrada declara `current_level=L1`,
`target_level=L3`, modo `audit` e dívida de adapter/runtime. As 14 entradas
preexistentes não mudaram semanticamente. A skill não contém runner, preflight,
Receipt ou adapter Databricks. A importação não valida geração de YAML nem
descoberta executável no Free.

## Integração local

O catálogo esperado passou a 15 identidades em `tools/project_policy.py`, que
é compartilhado por validador e publicador. O verificador de policy usa essa
contagem prospectiva e mantém checagens de ausência, excesso e duplicidade.
Os testes da policy foram atualizados para o catálogo atual; o baseline SE07
original de 14 skills permanece evidência histórica e não é reclassificado.
Índices do produto, Manual Técnico, playbook de transição e índices correntes
foram alinhados. A campanha Genie existente continua com os 37 casos SD e os
42 casos FG das 14 skills anteriores; Micromodelos requer casos próprios,
ainda NOT_RUN.

A correção de Monitoramento na mesma candidata altera somente seu `SKILL.md`
e `templates/drift_report.md`. Os resultados SD-VF-N/T01 e D01 seguem ligados
à versão publicada anterior. Nenhuma melhora comportamental é presumida por
esta importação.

## Verificações e estado

- Importação da skill/policy/instruções comparada por SHA256 ao backup remoto.
- Testes focados de policy e inventário: 18 PASS.
- Validador inicial apontou apenas links para este relatório, ainda não criado
  no momento da execução; o README de produto foi ajustado para não apontar
  para arquivo fora do pacote.
- Policy prospectiva: PASS com 15/15 entradas e zero issues.
- Regressões proporcionais (policy I/O, SER11/SER12, transição): 73 testes,
  8 skips esperados, demais PASS.
- Renderer: 658 arquivos; validador depois do renderer: 0 falhas/avisos.
- Pré-publicação: 656 arquivos remotos conferidos, inclusive os dois MM04,
  sem conflitos. Plano e envio integral concluíram sem erro.
- Verificação integral de inventário, tipos e conteúdo Free: **PASS**, 657
  arquivos comparados, zero erros. Hash normalizado `fe949b83dbf5bc8aa0ba9ff7442328668c408e1d8b253a868f8265d60c34c396`.
  Evidência `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d01/mm04-publish-verify.json`.
  O readback manteve os hashes dos quatro arquivos importados e confirmou
  os dois arquivos corrigidos de Monitoramento. O renderer listou 658 arquivos
  locais; o verificador contabiliza 657 objetos gerenciados no remoto.

Este checkout recebeu a candidata por decisão do usuário; a sprint MM04
permanece sem certificação própria. Seus gates, escopo de catálogo, adapter,
forward tests, review e aceite devem ser executados separadamente.

## Casos Genie próprios de MM04 — propostos, NOT_RUN

Executar em chats novos, um por vez, depois da campanha em curso e da publicação
conferida. Registrar indicador de seleção separado da qualidade da resposta.
Esses três casos não entram nos 42 FG originais.

- `FG-MM-P` (seleção espontânea): “Quero estruturar um micromodelo sintético de
  recência de contato. Tenho só descrições de catálogo; chave, instante de
  decisão e disponibilidade são desconhecidos. Que especificação e pendências
  consigo preparar sem ler registros?” Esperado: Micromodelos se observável,
  plano/rascunho, sem consulta de linhas ou YAML validado fictício.
- `FG-MM-N` (tarefa vizinha): “Tenho um modelo linear sintético já treinado e
  preciso explicar suas contribuições locais com coeficientes e referência
  declarados.” Esperado: Explainability ou esclarecimento; não forçar MM04.
- `FG-MM-A` (seleção explícita): selecione `@hub-ml-micromodelos` na interface e
  envie “Liste as lacunas para especificar uma característica sintética de
  recência sem chave, janela ou owner informados. Não consulte registros.”
  Esperado: seleção visível, pendências, sem alegar execução protegida L2/L3.

A tentativa de suíte ampla de 110 testes foi preservada em
`mm04-regressions.log` e não passou integralmente: além do ajuste inicial de
contagem já corrigido, mostrou expectativas históricas L2 para Criar Objeto
quando a policy atual já declara L3, comportamento de junction no Windows e
leitura cp1252 dos documentos. A regressão proporcional subsequente com UTF-8
passou (73 testes, 8 skips), assim como o gate do produto. Esses resultados não
certificam o histórico SE07 em nova versão.

## Revisão posterior da candidata MM04 — 2026-09-29

Após testes conversacionais no Databricks Free, a branch de laboratório
`micromodelos/autonomia-local-v2` corrigiu somente o `SKILL.md` de Micromodelos.
O B1 preservava o SHA-256 original
`e7964e906acca0f8a6376a44229a05c557c23afff6aad606fdea7e5ad6a00fba`;
a fonte B1 foi reconciliada com a revisão testada, SHA-256
`cccdfb314452c44575f13a49232671acf8da16b3f3a5307049c18b37edbbfab5`.
O espelho `Novo_Ambiente_Simulado/` foi regenerado pelo renderer. Contrato,
policy e encaminhamento permanecem com os hashes da tabela de proveniência
acima. A publicação pessoal Free já contém exatamente a revisão nova segundo
readback, sem mudança de `current_level=L1`, `target_level=L3` ou `audit`.

A revisão impede YAML MM01 inferido quando o schema não está acessível,
score numérico sem evidência/rubrica e viabilidade/leakage afirmados apenas
por nomes de colunas. Os três casos E1 da revisão corrigida receberam PASS de
resposta nos critérios testados; o adversarial teve ressalvas de precisão
(ambiente E0 no chat Free e menção a `DESCOBERTO` sem metadata observada).
Os três casos FG-MM propostos acima foram respondidos fora desta campanha B1:
rota espontânea e tarefa vizinha passaram, e a seleção explícita teve resposta
adequada. Seleção no menu foi declarada pelo usuário, sem captura independente.
Veredito, hashes das transcrições e limites estão no relatório da
[PR #116](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/pull/116)
(`docs/sprints/micromodelos/RESULTADOS_GENIE_E1_2026-09-29.md`).

Verificação local desta atualização: fonte e derivado ficaram byte a byte
iguais nos 657 objetos renderizados; `python -B tools/validate_assistant.py
--root ambiente_fonte` aprovou com 0 falhas e 0 avisos; os 15 testes de
`test_skill_enforcement_policy_io` passaram. Uma bateria mais ampla de 59
testes SE07/policy teve **2 FAIL**, 1 skip: ambos esperam o nível histórico L2
de `hub-ml-criar-objeto`, enquanto a policy atual declara L3. Essa bateria não
é PASS nem evidência contra a mudança textual de Micromodelos; a falha foi
preservada sem alterar testes ou outra skill.

Essas respostas não entram nos 42 FG originais, não substituem a campanha B1
nem certificam a sprint MM04. O checkout B1 segue com mudanças locais de outras
frentes; não houve commit, merge ou promoção nesta reconciliação. Os gates
próprios MM04, inclusive readiness SEF/PSEF, smoke, freeze identificável,
certificação proporcional, auditoria e aceite humano, seguem separados.
