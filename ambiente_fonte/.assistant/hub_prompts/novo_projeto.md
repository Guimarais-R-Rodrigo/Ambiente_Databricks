# Prompt: iniciar projeto analítico no Databricks

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Este prompt cria contexto e artefatos;
> ele não cria automaticamente diretórios nem configura memória. Para contexto
> hierárquico nativo, use um `AGENTS.md` no diretório real do projeto. Anexe recursos
> existentes com **Add context** ou `@`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Prompt pronto para colar

```text
Estruture um novo projeto analítico no Databricks com documentação mínima,
governança, plano de validação e contexto reutilizável.

BRIEFING
- Nome curto: {{NOME}}
- Problema/decisão: {{OBJETIVO}}
- Dono e stakeholders: {{DONOS}}
- Critério de sucesso e guardrails: {{METRICAS}}
- Fontes conhecidas: {{TABELAS_PIPELINES_NOTEBOOKS}}
- Entidade/target/horizonte: {{ENTIDADE_TARGET_HORIZONTE_OU_NAO_APLICAVEL}}
- Entregáveis e prazo: {{ENTREGAVEIS_E_TIMELINE}}
- Ambientes: {{DEV_STAGE_PROD_OU_NAO_INFORMADO}}
- Segurança, PII e compliance: {{RESTRICOES}}
- Repositório/Git folder: {{REPOSITORIO_OU_NAO_INFORMADO}}
- Modo: {{SOMENTE_PLANO_OU_GERAR_ARQUIVOS}}

INSTRUÇÕES
1. Verifique o contexto anexado e liste dúvidas que impedem definição segura.
2. Proponha uma árvore simples de projeto, separando código, testes, configuração e
   documentação. Não invente nomes de catálogos, credenciais ou owners.
3. Gere um `AGENTS.md` a partir do template de `x_projects`, com apenas instruções
   aplicáveis aos arquivos daquele diretório e descendentes.
4. Para implantação, proponha Declarative Automation Bundles com targets separados
   quando fizer sentido; não faça deploy nem crie recursos sem autorização.
5. Inclua riscos, decisões, definition of done, validações, rollback e observabilidade.
6. Não armazene segredos, PII, tokens ou caminhos pessoais em arquivos versionados.

CONTRATO DE SAÍDA
- Project charter curto e mensurável.
- Estrutura proposta com finalidade de cada item.
- `AGENTS.md` pronto para revisão, sem duplicar preferências globais.
- Backlog inicial priorizado, dependências e responsáveis sugeridos.
- Critérios de aceite/teste e plano de ambientes.
- Lista explícita de ações que exigem autorização.

VALIDAÇÃO FINAL
- Confirme que `AGENTS.md` será colocado no diretório ancestral correto.
- Diferencie estrutura oficial Databricks de convenções personalizadas `x_`.
- Verifique que nenhum placeholder, segredo ou path pessoal ficou no artefato final.
```

## Exemplo mínimo

Nome = `churn-previdencia`; objetivo = priorizar retenção em 90 dias; entregáveis =
EDA, baseline e job mensal; modo = SOMENTE_PLANO.

## Follow-ups úteis

- “Gere os arquivos depois que eu aprovar a árvore.”
- “Revise o AGENTS.md para remover instruções globais ou redundantes.”
- “Proponha o bundle e os targets dev/stage/prod sem fazer deploy.”
