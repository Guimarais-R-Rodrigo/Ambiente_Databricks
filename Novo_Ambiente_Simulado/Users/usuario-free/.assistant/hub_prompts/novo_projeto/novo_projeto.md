# Prompt: iniciar projeto analítico no Databricks

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Este prompt cria contexto e artefatos;
> ele não cria automaticamente diretórios nem configura memória. Para contexto
> hierárquico nativo, use um `AGENTS.md` no diretório real do projeto. Anexe recursos
> existentes com **Add context** ou `@`.

Não há uma skill analítica única nesta etapa. O objetivo é criar o charter e o
`AGENTS.md`; depois, mencione com `@` a skill que corresponde ao trabalho
definido. O mapa de capacidades e helpers está em
[CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md).

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{NOME}}` | Use nome curto, estável e sem dado pessoal. | Serve de identificador do charter. | propensao-consorcio |
| `{{OBJETIVO}}` | Escreva problema e decisão, não a solução. | Evita arquitetura prematura. | priorizar contatos elegíveis |
| `{{DONOS}}` | Liste responsável, aprovador e consumidores. | Define governança e handoffs. | PO CRM; Risco aprova |
| `{{METRICAS}}` | Defina sucesso, unidade, horizonte e guardrails. | Evita otimizar só uma métrica. | conversão +2 p.p.; reclamação não aumenta |
| `{{TABELAS_PIPELINES_NOTEBOOKS}}` | Anexe fontes conhecidas e owners. | Mapeia contexto sem inventar. | `@main.crm.clientes`; pipeline eventos |
| `{{ENTIDADE_TARGET_HORIZONTE_OU_NAO_APLICAVEL}}` | Defina unidade, evento e janela. | Alinha dados e avaliação. | cliente; contratação em 60 dias |
| `{{ENTREGAVEIS_E_TIMELINE}}` | Liste artefatos, marcos e prazo. | Torna escopo verificável. | EDA, baseline, piloto em 6 semanas |
| `{{DEV_STAGE_PROD_OU_NAO_INFORMADO}}` | Mapeie ambientes e catálogos. | Evita escrita no ambiente errado. | dev e prod; catálogos separados |
| `{{RESTRICOES}}` | Declare PII, compliance, custo e permissões. | Impõe limites desde o desenho. | sem atributo sensível; revisão Risco |
| `{{REPOSITORIO_OU_NAO_INFORMADO}}` | Informe repo e pasta do projeto. | Permite gerar estrutura no local certo. | repo squad, `projects/propensao` |
| `{{SOMENTE_PLANO_OU_GERAR_ARQUIVOS}}` | Escolha plano ou geração autorizada. | Separa desenho de mutação. | somente plano |

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
3. Gere um `AGENTS.md` do zero, com apenas instruções
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
- Diferencie estrutura oficial Databricks das convenções do Hub (`hub_`/`hub-`).
- Verifique que nenhum placeholder, segredo ou path pessoal ficou no artefato final.
```

## Exemplo mínimo

Nome = `churn-previdencia`; objetivo = priorizar retenção em 90 dias; entregáveis =
EDA, baseline e job mensal; modo = SOMENTE_PLANO.

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Gere os arquivos depois que eu aprovar a árvore.”
- “Revise o AGENTS.md para remover instruções globais ou redundantes.”
- “Proponha o bundle e os targets dev/stage/prod sem fazer deploy.”
