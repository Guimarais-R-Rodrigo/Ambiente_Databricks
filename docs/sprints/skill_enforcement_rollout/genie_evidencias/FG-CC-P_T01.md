# FG-CC-P/T01 — descoberta de nulos e chaves — 2026-09-30

(Codex) Primeira resposta original preservada em
`.artifacts/skills-delivery-evidence/genie-20260930-concierge-14p/response-original.txt`;
SHA-256 `37bdd144447c050922521aff2b53e2539bb0e7c8eb9882cc95e79e298cdd6dc6`.
O usuário confirmou chat novo sem `@` e indicador separado de
`hub-ml-concierge` carregada. Foi enviada a primeira mensagem literal do caso
14P; a segunda mensagem histórica apenas pedia registrar o resultado no
workspace e foi substituída por este registro externo.

## Versão e observabilidade

O último pacote B1 conferido antes deste teste tinha 657 arquivos e hash
normalizado `7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário relatou publicação paralela posterior da frente de micromodelos;
portanto, **não atribuímos aquele hash à instalação efetiva desta conversa**.
O Genie também marcou a versão do Hub como `NÃO VERIFICADA`. A transcrição
colada não contém eventos de ferramenta/arquivo nem export de notebook; as
declarações textuais do Genie sobre arquivos lidos não são prova independente
dessas leituras. Nenhum cálculo sobre tabelas ou escrita foi relatado.

## Vereditos separados

- Roteamento P: **PASS por indicador relatado pelo usuário**. O Concierge
  carregou espontaneamente para uma pergunta de descoberta de recursos.
- Recomendação: **PASS no escopo principal**. Escolheu
  `hub_scripts.data_quality_check` para nulos e duplicidade de chave em uma
  tabela, separando `null_summary` para DataFrame já carregado,
  `quick_profile` para perfil amplo e `join_diagnostics` para risco de
  expansão em junção. O Codex conferiu esses símbolos, assinaturas e
  capacidades no código local `ambiente_fonte/.assistant/`.
- Precisão/aderência: **ressalva parcial**. A resposta presumiu uma tabela
  Unity Catalog embora o prompt dissesse apenas “tabela”; a rota é adequada
  se for uma tabela Spark acessível ao helper. O texto diz ter consultado
  implementação e exports, mas só o relato textual está disponível. O Manual
  foi consultado apenas no índice/sumário, conforme a própria resposta; não
  há evidência de inventário das cinco famílias no nível de índice. A
  conclusão `TOTAL_PARA_ESCOPO` vale para a necessidade de descoberta
  descrita, condicionada a confirmar tabela e colunas de chave para executar.
- Execução/efeitos: **NOT_RUN na evidência fornecida**. Não há consulta a
  dados, saída analítica ou registro de efeito apresentado; a resposta
  propôs execução futura somente se o usuário fornecer tabela e chave.

**Veredito T01: PASS do positivo de roteamento e da rota principal; verificação
das leituras internas NOT_OBSERVABLE, com ressalva de escopo.** A prova
independente do Codex limita-se aos arquivos locais; ela não demonstra quais
bytes o Genie abriu no workspace. Nenhuma edição de produto ou publicação foi
feita nesta coleta.
