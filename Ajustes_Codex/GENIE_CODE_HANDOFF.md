# Handoff para a Genie Code

> **CUSTOMIZADO — adicione este arquivo manualmente com `@` ou Add context.**
> Não trate `x_delivery` como diretório auto-descoberto.

## Objetivo

Validar e implantar gradualmente este ecossistema de 12 skills personalizadas no
Azure Databricks, sem confundir conteúdo do usuário com funcionalidade built-in.

## Autoridade e nomenclatura

Use prioritariamente a documentação oficial Azure Databricks atual. Termos vigentes:

- Genie Code;
- Agent Skills em `.assistant/skills/<skill>/SKILL.md`;
- instruções pessoais em `/Users/<username>/.assistant_instructions.md`;
- skills pessoais em `/Users/<username>/.assistant/skills/`;
- skills de workspace em `Workspace/.assistant/skills/`;
- contexto hierárquico por `AGENTS.md`/`CLAUDE.md`;
- Lakeflow Spark Declarative Pipelines;
- Lakeflow Jobs;
- Declarative Automation Bundles (nome anterior: Databricks Asset Bundles).

## Regras de interpretação

1. `rodrigo-*` é conteúdo personalizado em uma estrutura de descoberta suportada.
2. Todo diretório `x_` é extensão manual e não é auto-descoberto.
3. Use `@nome-da-skill` para seleção explícita. `/eda`, `/baseline` e similares são
   convenções humanas, não slash commands registrados.
4. `/findTables` é uma funcionalidade nativa distinta dessas convenções.
5. `x_prompts`/`x_projects` entram no contexto somente por `@`/Add context ou após
   copiar o modelo como `AGENTS.md` no projeto real.
6. Importar `x_snippets` afeta o runtime Python; não injeta o módulo no contexto.
7. `x_config/mcp_servers.legacy.json` não ativa MCP; configurar em Settings.

## Estado validado

- 12/12 skills estruturalmente válidas.
- 16 prompts completos.
- 61 arquivos Python parseiam.
- 13 testes driver-side passaram.
- Zero link relativo quebrado, PII/path pessoal ou mojibake detectado.
- Instruções pessoais: 7.371 caracteres.

## Sequência de implantação

1. Ler `.assistant/README.md`.
2. Copiar `.assistant_instructions.md` para `/Users/<username>/`.
3. Copiar as 12 pastas de `.assistant/skills/` para o escopo pessoal de
   desenvolvimento ou publicar em `Workspace/.assistant/skills/` com revisão/admin.
4. Abrir novo chat e testar relevância automática e `@menção` de cada skill.
5. Copiar `x_projects/AGENTS_TEMPLATE.md` como `AGENTS.md` no projeto consumidor.
6. Instalar/usar `x_snippets` e `x_scripts` somente quando o workflow exigir.
7. Fixar dependências no projeto/bundle e executar testes Spark/framework no runtime.
8. Promover por bundle/target após validação, aprovação e plano de rollback.

## Critérios de bloqueio

Não promover para produção se houver:

- path, catálogo, schema, tabela ou ambiente não confirmado;
- escrita não autorizada;
- teste Spark/runtime pendente para o componente utilizado;
- feature temporal sem point-in-time ou partição por entidade quando necessária;
- target/classe positiva/direção do score ambíguos;
- threshold tratado como padrão universal;
- afirmação regulatória sem fonte e revisão competente;
- dependência opcional não fixada/testada;
- skill não selecionável em novo chat por relevância e por `@menção`.

## Arquivos de decisão

- Guia: `.assistant/README.md`
- Instruções: `.assistant_instructions.md`
- Manifesto: `.assistant/x_docs/skills_manifest.md`
- Roadmap/gates: `.assistant/x_docs/ROADMAP_SKILLS.md`
- Relatório completo: `x_delivery/AUDIT_AND_IMPLEMENTATION_REPORT.md`
- Validação estruturada: `x_delivery/validation_results.json`
