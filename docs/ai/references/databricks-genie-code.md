# Databricks Genie Code: fontes e limites

## Politica

Leia ao afirmar nomenclatura/capacidade, editar instruções ou orientar teste no
Databricks. Separe documentação oficial, customização Hub, observação local e
hipótese. Registro desta consulta: **2026-10-06, 19:06 UTC**; páginas públicas
consultadas, sem sessão autenticada ou execução no workspace. Estado destes
claims: DOCUMENTED; observação no destino e suporte não foram demonstrados.
URLs e títulos abaixo são fontes, não autorização para ativar recursos.

Revalide ao tocar um claim, mudar versão/superfície/configuração ou encontrar
contradição, e antes de promover suporte. Política local da camada IA: revisão
com mais de 30 dias fica STALE para nova alegação de compatibilidade; aviso não
bloqueia edição alheia à camada, mas bloqueia release de claim vencido. Mudança
material conhecida invalida antes disso. Registre mudança de nome/limite no
changelog. Não criar scheduler nem atualizar adapters/settings automaticamente.

Para revisões de assunto, consulte skills, instructions, tips e MCP; pipelines e
best practices; bundles; MLflow tracking e ciclo de modelos quando pertinentes.
[Registro oficial](../standards/registry.json) e [compatibilidade](../compatibility.md)
separam DOCUMENTED, OBSERVED e SUPPORTED; não transferir evidência entre produtos.
Hashes de páginas/revisões estáveis não foram obtidos por esta consulta de texto;
não há digest inventado nem cópia integral da documentação.

## Documentado

- **Instruções:** `/Users/<username>/.assistant_instructions.md` e
  `Workspace/.assistant_workspace_instructions.md`; a segunda requer admin.
  A página limita arquivos de instrução a 20.000 caracteres e exclui Quick Fix e
  Autocomplete de sua aplicação. Documenta descoberta hierárquica de AGENTS.md e
  CLAUDE.md ao abrir arquivos/notebooks no workspace. Isso não transporta
  automaticamente os arquivos deste Git para aquele workspace.
  [Customize Genie Code with custom instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
  (página atualizada em 2026-09-23).
- **Agent Skills:** mecanismo aberto; cada skill tem pasta e `SKILL.md` com
  `name`/`description`. Defaults: `Workspace/.assistant/skills/` e
  `/Users/<username>/.assistant/skills/`; pastas extras podem ser registradas.
  Seleção por descrição e `@` são documentadas. Após editar, usar chat novo;
  metadata antiga pode exigir hard refresh. Isso não prova roteamento infalível.
  [Extend Genie Code with agent skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
  (2026-10-01).
- **Contexto explícito:** `@` e imagens ajudam a fornecer contexto. No Hub,
  imagem complementa nomes, grão, restrições e aceite escritos, sem substituí-los.
  [Tips to improve Genie Code responses](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips).
- **Modo agente:** ações estão sujeitas a permissões UC e modos de aprovação.
  O próprio fornecedor diz que auto-approve não é uma fronteira de segurança.
  Não tratar prompt/classificador como ACL ou autorização de negócio, nem mudar
  configurações para obter PASS.
  [Agent mode](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode)
  (2026-09-25).
- **MCP/conectores:** conexões e ferramentas dependem de permissões, fontes
  habilitadas e fluxo de configuração/autenticação do workspace. A página
  descreve conectores nativos e adição de servidores. Disponibilidade não é
  promessa do Hub nem autorização para login, conexão ou acesso persistente.
  [Connect Genie Code to MCP servers](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp).

## Nomenclatura

Use **Genie Code**, **Agent Skills**, **Lakeflow Jobs** e **Declarative Automation
Bundles** (antes Databricks Asset Bundles). A documentação consultada de pipelines
se intitula **Spark Declarative Pipelines**, distinguindo o framework Apache das
**Lakeflow pipelines**. Preserve a expressão histórica “Lakeflow Spark Declarative
Pipelines” em relatos antigos, sem impor como único nome atual.
Fontes: [Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
e [Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/),
ambas atualizadas em 2026-09-11. Não renomear APIs/identificadores do produto por
uma atualização editorial sem escopo próprio.

## Limites revalidados

- A antiga negativa de memória automática não é preservada como regra: a fonte
  agora documenta memória construída e recuperada entre sessões, separada das
  instruções. Isso é documentação do produto, sem observação na conta usada pelo
  projeto. [Remember context across sessions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/memory)
  (2026-09-30).
- A página Free Edition documenta compute serverless, Jobs e model serving com
  limites. Assim, “sem jobs permanentes”/“sem serving” não são impossibilidades
  universais sustentadas hoje. Quota, plano e recurso efetivo precisam confirmação;
  uso do laboratório continua sintético e não certifica políticas do trabalho.
  [Databricks Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations)
  (2026-09-29).
- Nas páginas consultadas acima não foi estabelecido um contrato para registrar
  slash commands personalizados nem hooks genéricos pós-resposta. Não prometer
  esses mecanismos sem fonte específica/teste; “não estabelecido nesta consulta”
  não quer dizer “impossível”. `/eda` pode ser convenção humana; o exemplo antigo
  `/findTables` não é prova de catálogo atual. Use a seleção de skill `@` documentada.
- Não foi estabelecido nas fontes consultadas um contrato de configuração por
  criar manualmente `.mcp_servers.json`. Siga a interface documentada e o fluxo
  autorizado; não inferir semântica universal de uma observação de arquivo.

## Convencao Hub

`hub_`/`hub-` identifica conteúdo local. READMEs explicam o que exige `@`/Add
context, import ou execução manual. Uma skill `hub-ml-*` usa o mecanismo nativo;
uma skill de manutenção em `.agents/skills/` pertence ao mantenedor e não regula
automaticamente Genie Code. Transporte não comprova instalação/ativação.

Segredos de MCP/conector/API nunca entram em prompt, instrução, skill, Git ou
logs; use o mecanismo de credenciais autorizado. Arquivos MCP e conteúdo alheio
são preservados por publicação/replicação.

## Observacao local

Em **2026-08-15**, o controle anterior registrou que abrir Settings de MCP
escreveu `/Users/<username>/.assistant/.mcp_servers.json`; tratou esse arquivo
como saída de configuração. É relato da versão/sessão antiga, não prova de
semântica atual. Preserve-o: não versionar, criar à mão como suposta instalação,
apagar ou sobrescrever esse arquivo para publicar o Hub. Fonte histórica:
[controle C08 na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/f2843eafae84d44cd751f307101de84f11981bd7/.claude/rules/genie-code-oficial.md#L33-L37).

Hipóteses sobre carregamento/permissões exigem experimento autorizado, sintético
e identificado. Nesta migração, ausência de cliente/workspace é BLOCKED; texto
ou resposta “entendi” não fecha gate de comportamento.
