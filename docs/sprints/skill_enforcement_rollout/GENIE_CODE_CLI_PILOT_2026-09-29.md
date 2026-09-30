# Piloto de automação Genie Code via Databricks CLI — 2026-09-29

(Codex) O usuário pediu verificar se as rodadas Genie Code poderiam ser
executadas pela Databricks CLI, para reduzir coleta manual. O teste usou apenas
um prompt conceitual sintético de Explainability, com instrução explícita de
responder em texto, sem executar código, editar arquivos ou acessar dados
externos. Nenhum job ou chat foi criado.

## O que foi observado

- A CLI instalada é `Databricks CLI v1.16.1`, perfil `FREE`.
- `databricks genie --help` oferece comandos de Genie Spaces/Agents, como
  `ask`, `start-conversation` e `create-message`; não há comando de chat
  Genie Code nesse grupo.
- A documentação oficial descreve uma tarefa **Genie Code em Lakeflow Jobs
  (Beta)** que inicia chat e devolve resposta/link, condicionada à habilitação
  de preview. Não fornece neste ponto do projeto um campo de payload Jobs
  confirmado para uso pela CLI.
- Foi preparado um `jobs submit` one-shot com uma tarefa candidata
  `genie_code_task` e prompt sintético. A CLI rejeitou o campo antes de enviar:
  `Warning: unknown field: genie_code_task` e
  `Error: No task defined for explainability_conceptual`.
- A mesma carga enviada pela CLI genérica `databricks api post` a
  `/api/2.2/jobs/runs/submit` recebeu `Error: No task defined for
  explainability_conceptual`. A API não aceitou essa forma da tarefa.

Esses retornos **não comprovam que a preview está desabilitada** nem que não
exista outro endpoint/formato não documentado; comprovam apenas que o tipo
testado não é aceito pela CLI e pelo Jobs API deste workspace. Não inferir
execução de Genie Code, seleção de skill ou evento de carregamento a partir
dessas tentativas rejeitadas.

## Consequência para a campanha

Scripts, runners e notebooks sintéticos podem continuar automatizados por CLI
e APIs Databricks, com outputs/Receipts inspecionados. Isso verifica o produto,
mas não testa o roteamento espontâneo nem o seletor `@` do Genie Code. As
rodadas conversacionais permanecem pela interface até surgir uma superfície
programática comprovada **e** evidência equivalente. Casos FG/SD não são
reclassificados pelo piloto. A estimativa de 72 rodadas manuais era nominal e
continua sujeita a equivalência documentada entre casos; este teste não a
reduziu.

Próxima verificação de disponibilidade: conferir na interface Free se
Jobs → Add task → Type oferece **Genie Code**. Se houver, um job Beta criado
pela interface com prompt parametrizado pode talvez ser acionado pela CLI;
isso exigirá piloto separado para confirmar resposta, link de chat, acesso às
skills e limites de observabilidade. Se a opção não aparecer, a preview não
está disponível por esse caminho no Free atual. Essa checagem foi solicitada
ao usuário, sem presumir resposta.

Evidência local não versionada:
`.artifacts/skills-delivery-evidence/genie-code-cli-pilot-20260929/job-pilot.json`.
Fontes oficiais consultadas:
[tarefa Genie Code em Jobs](https://docs.databricks.com/aws/en/jobs/tasks/genie-code),
[comandos CLI Genie](https://docs.databricks.com/aws/en/dev-tools/cli/reference/genie-commands),
[skills do Genie Code](https://docs.databricks.com/gcp/en/genie-code/skills).
