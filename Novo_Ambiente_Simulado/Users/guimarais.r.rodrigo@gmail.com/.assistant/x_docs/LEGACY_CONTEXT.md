# Contexto histórico migrado

> **EXTENSÃO CUSTOMIZADA (`x_`) — não auto-descoberta pela Genie Code.**

Este arquivo preserva o significado das seções específicas que foram retiradas de
`.assistant_instructions.md`. A migração mantém as instruções pessoais abaixo do
limite oficial, gerais e úteis em todas as respostas. Adicione este arquivo ao chat
com `@`/ **Add context** somente quando o histórico for necessário.

## Convenções históricas

- `/eda`, `/perfil`, `/qualidade`, `/cross-eda`, `/schema`, `/features`,
  `/stat-check`, `/baseline`, `/explain`, `/shap`, `/monitor`, `/drift`,
  `/pipeline`, `/safra`, `/vintage`, `/retreino`, `/comentar`, `/tutor`,
  `/rfv`, `/roadmap`, `/manifest`, `/sprint` e `/auditar` eram aliases humanos.
- Esses textos nunca constituíram comandos slash nativos. O mecanismo nativo para
  seleção explícita é mencionar a skill com `@nome-da-skill`.
- As sugestões pós-etapa (“hooks”) eram contratos editoriais, não automações
  executadas pela plataforma. Elas foram incorporadas às skills pertinentes.

## Plano de testes histórico

- O plano v3 previa 9 sprints, 22 notebooks e validação das 12 skills em ambiente
  Spark serverless, com amostragem reprodutível e cenários auxiliares para séries,
  ranking e survival.
- Os nomes, schemas, volumes, proxies de target, versões e caminhos do ambiente
  original são intencionalmente omitidos daqui. Mantenha-os no `AGENTS.md` do
  projeto de testes real para evitar contexto pessoal obsoleto em todas as conversas.
- Dependências opcionais citadas no histórico incluíam LightGBM, XGBoost, SHAP,
  Prophet, lifelines, PyTorch/TabNet e UMAP. Confirme compatibilidade e versões no
  runtime atual antes de instalar.

## Governança histórica

- As skills externas `pd-gerador-produto-dados` e
  `pd-validador-produto-dados` eram mantidas fora deste pacote. Use-as somente se
  realmente estiverem instaladas no workspace e trate suas regras como política da
  organização, não como comportamento nativo universal da Databricks.
- A antiga skill local de governança foi removida para evitar duplicidade.

## Auditoria

`rodrigo-auditoria-skills` continua sendo a skill de revisão de outputs. Sua rubrica
deve avaliar completude, reprodutibilidade, rigor, documentação, rastreabilidade,
governança, acionabilidade, apresentação, robustez e integração do ecossistema.
