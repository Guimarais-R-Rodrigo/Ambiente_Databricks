# Regra — Nomenclatura e capacidades oficiais do Genie Code

Política: estar na vanguarda do que a Databricks lança **sem afirmar recurso que
não existe**. Em dúvida, verificar a documentação oficial antes de afirmar.

## Nomenclatura vigente (verificada em 2026-08-13)

- **Genie Code** — assistente de código do Databricks (Azure: docs em
  `learn.microsoft.com/en-us/azure/databricks/genie-code/`).
- **Agent Skills** — padrão aberto (agentskills.io). Workspace:
  `Workspace/.assistant/skills/`; usuário: `/Users/<username>/.assistant/skills/`.
  `SKILL.md` obrigatório com frontmatter `name` + `description`.
- Instruções pessoais: `/Users/<username>/.assistant_instructions.md` (≤ 20.000
  caracteres). Instruções de workspace:
  `Workspace/.assistant_workspace_instructions.md` (só admins).
- `AGENTS.md`/`CLAUDE.md`: descoberta hierárquica automática ao abrir arquivo.
- **Lakeflow Spark Declarative Pipelines**, **Lakeflow Jobs**,
  **Declarative Automation Bundles** (nome anterior: Databricks Asset Bundles).

## Capacidades que NÃO existem (não prometa)

- Slash commands registrados pelo usuário (`/eda` etc. são convenção humana;
  `/findTables` é nativo). Seleção explícita suportada: `@nome-da-skill`.
- Hooks/automação pós-resposta; memória automática além dos mecanismos acima.
- MCP por arquivo JSON no workspace — MCP configura-se em Genie Code → Settings.
  Cuidado com a inversão: abrir esse painel **escreve**
  `/Users/<username>/.assistant/.mcp_servers.json` (verificado em 2026-08-15).
  O arquivo é saída da configuração, nunca entrada — criá-lo à mão não configura
  nada, e ele não deve ser versionado nem removido do workspace.
- Instruções aplicadas a Quick Fix e Autocomplete (exceção oficial).

## Convenção local

- Conteúdo não auto-descoberto usa prefixo `x_` e READMEs explicam que exige
  `@`/Add context, import ou execução manual.
- Após editar skill publicada: chat novo; se metadata cachear, hard refresh.

## Revisão de vanguarda

Ao tocar em afirmações de plataforma, ou pelo menos trimestralmente, revisitar:
skills, instructions, tips, mcp (genie-code/*), ldp/best-practices,
dev-tools/bundles, mlflow/tracking, manage-model-lifecycle. Registrar no
CHANGELOG qualquer mudança de nomenclatura/limite detectada.
