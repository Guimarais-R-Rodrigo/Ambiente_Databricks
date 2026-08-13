# Roadmap de manutenção

> **DOCUMENTAÇÃO CUSTOMIZADA (`x_docs`) — não auto-descoberta.**

## Concluído nesta revisão

- [x] Separar estruturas nativas e extensões `x_`.
- [x] Manter as 12 skills em `.assistant/skills/`.
- [x] Adicionar/reparar frontmatter e progressive disclosure.
- [x] Transformar prompts em briefings reproduzíveis.
- [x] Migrar contexto de projeto para um template `AGENTS.md`.
- [x] Remover claims de slash commands, memória automática e MCP por arquivo.
- [x] Parametrizar caminhos pessoais.
- [x] Corrigir bugs críticos em PSI, RFV, profiling, qualidade, features temporais,
  vintage e decisão de retreino.
- [x] Adicionar testes de regressão driver-side.

## Antes da implantação no workspace

- [ ] Executar testes Spark com as versões reais do runtime Databricks.
- [ ] Validar as 12 skills em chats novos: um caso positivo, um negativo e uma
  `@menção` explícita por skill.
- [ ] Fixar dependências opcionais por workflow após teste no runtime alvo.
- [ ] Implantar primeiro em um usuário/target de desenvolvimento.
- [ ] Revisar permissões, PII, custos e efeitos de escrita.

## Backlog priorizado

### P1 — confiabilidade

- Criar testes Spark pequenos para cada helper em `x_scripts` e `x_snippets/spark`.
- Criar fixtures sintéticas por suite de baseline (tabular, temporal, ranking,
  clustering e survival).
- Adicionar CI para frontmatter, links, UTF-8, compilação e testes.

### P2 — operação Databricks

- Criar um Declarative Automation Bundle de exemplo com targets dev/hml/prod.
- Adicionar exemplos de Lakeflow expectations e consulta ao event log.
- Adicionar exemplo governado de MLflow/Models in Unity Catalog e monitoramento.

### P3 — experiência

- Criar uma matriz de forward tests para reduzir colisão de descrições entre skills.
- Medir quais recursos de referência cada skill realmente precisa e remover excesso.
- Revisar trimestralmente os links e nomenclaturas oficiais.

## Política de versão

Versione o pacote em Git. Uma alteração de comportamento deve incluir:

1. justificativa e risco;
2. teste ou cenário de validação;
3. atualização do README/manifesto pertinente;
4. novo chat de forward test;
5. estratégia de rollback por commit/tag.
