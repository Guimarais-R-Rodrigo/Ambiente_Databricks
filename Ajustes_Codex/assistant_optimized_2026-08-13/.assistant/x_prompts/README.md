# `x_prompts` — biblioteca personalizada de prompts para Genie Code

> **EXTENSÃO PERSONALIZADA (`x_`) — NÃO AUTO-DESCOBERTA.** Esta pasta não é uma
> estrutura institucional da Databricks e seu conteúdo não é carregado
> automaticamente pelo Genie Code. O prefixo `x_` torna essa diferença explícita.

## Para que serve

Estes arquivos são formulários reutilizáveis para preparar pedidos claros e
reprodutíveis. Eles complementam, mas não substituem:

- `.assistant_instructions.md`, usado para preferências globais do usuário;
- `AGENTS.md`, descoberto automaticamente no diretório do projeto e em seus
  diretórios ancestrais;
- `.assistant/skills/<nome>/SKILL.md`, carregado quando relevante ou quando a skill
  é mencionada com `@`.

## Uso recomendado

1. Abra o prompt adequado e substitua cada `{{CAMPO}}`. Use `NÃO INFORMADO` quando
   algo for desconhecido; não deixe placeholders sem intenção.
2. No painel do Genie Code, clique em **Add context** para anexar notebooks, queries,
   pipelines, tabelas ou arquivos. Alternativamente, digite `@<recurso>`.
3. Para uma skill específica, digite `@` e selecione a skill indicada no prompt.
4. Cole apenas o bloco **Prompt pronto para colar** no chat.
5. Revise o plano, os pressupostos e o impacto antes de autorizar execução ou escrita.

O contexto selecionado persiste no chat. Para um tema diferente, prefira um novo
chat para evitar que decisões antigas contaminem a resposta.

## Catálogo

| Tema | Arquivo | Skill recomendada |
|---|---|---|
| EDA completa | `eda_completa.md` | `@rodrigo-eda-profissional` |
| Perfil rápido | `eda_rapida.md` | `@rodrigo-eda-profissional` |
| Qualidade de dados | `data_quality.md` | `@rodrigo-eda-profissional` |
| Cross-EDA | `cross_eda.md` | `@rodrigo-cross-eda-ml` |
| Feature engineering | `feature_engineering.md` | `@rodrigo-feature-engineering` |
| Validação estatística | `stat_check.md` | `@rodrigo-validacao-estatistica` |
| Baseline de ML | `baseline_orchestration.md` | `@rodrigo-baseline-ml` |
| Explicabilidade | `explainability.md` | `@rodrigo-explainability` |
| Monitoramento | `monitoramento_modelo.md` | `@rodrigo-monitoramento-modelo` |
| Pipeline de dados | `pipeline.md` | `@rodrigo-pipeline-builder` |
| Safra/vintage | `safra.md` | `@rodrigo-analise-safra` |
| Auditoria de skills | `auditoria_skills.md` | `@rodrigo-auditoria-skills` |
| Documentar notebook | `comentar_notebook.md` | `@rodrigo-comentar-notebook` |
| Explicação/tutoria | `tutor_explicar.md` | `@rodrigo-tutor-databricks` |
| Comparar tabelas | `comparar_tabelas.md` | conforme o objetivo |
| Iniciar projeto | `novo_projeto.md` | conforme o projeto |

## Sobre os atalhos `/...`

Expressões como `/eda`, `/baseline` e `/stat-check` são **convenções pessoais de
texto** mantidas por compatibilidade. Não são comandos registrados do Genie Code.
O comando `/findTables` é uma funcionalidade documentada pela Databricks; os
demais atalhos deste catálogo dependem da interpretação do texto e não devem ser
usados como único mecanismo de roteamento. Para execução determinística, mencione
a skill com `@` e forneça o contexto explicitamente.

## Princípios incorporados

- pedido específico, nível de detalhe e formato de saída explícitos;
- recursos adicionados com **Add context** ou `@`;
- nomes de tabelas em três níveis (`catalog.schema.table`) quando conhecidos;
- pressupostos e campos ausentes sinalizados, nunca inventados;
- separação entre análise, geração de código, execução e mutação;
- amostragem/limites em exploração e processamento distribuído para volume alto;
- proteção de dados sensíveis e nenhuma exposição de valores identificáveis;
- validação técnica antes de recomendar produção.

## Fontes oficiais

- [Tips to improve Genie Code responses](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Extend Genie Code with agent skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Customize Genie Code with custom instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)

---

Última revisão: 2026-08-13.
