# Reconciliação documental pós-R13 — D01–D04

Objetivo: reconciliar a documentação viva com o encerramento R00–R13 sem reabrir os 75 READMEs de objeto nem reescrever evidências históricas.

- **D01:** contexto canônico, regra editorial, skill de validação e `tools/README.md`.
- **D02:** navegação do produto em `ambiente_fonte/` e coleções `.assistant`.
- **D03:** índices de governança, sprints, testes e ADR-0012.
- **D04:** procedência do Manual Técnico, cópia raiz idêntica e simulado regenerado.

Critérios: 75/75 operacionais, 3/3 exemplares, 0 pendências; 7/7 scripts e 16/16 prompts com guia local; seis índices de snippets preservados; nenhum relatório histórico R00–R13 alterado; `validate_assistant --conferir-readme`, `ci_local.py`, `git diff --check` e CIs permanentes verdes.

Limites: documentação apenas. Não publica no workspace, não homologa Databricks/Genie Code e não transforma R13 em auditoria independente. O Sistema de Temas é reconciliado separadamente em D05.
