# Pacote otimizado para Databricks Genie Code

Este diretório contém a entrega pronta para revisão. Implante somente depois de
executar o checklist no runtime e no workspace Azure Databricks de destino:

- `.assistant_instructions.md`: arquivo nativo de instruções pessoais;
- `.assistant/skills/`: 12 skills personalizadas na estrutura nativa de descoberta;
- `.assistant/x_*`: extensões customizadas, sempre manuais;
- `.assistant/README.md`: guia completo de instalação, uso, arquitetura e testes.
- `x_delivery/`: relatório, handoff da Genie Code e resultados estruturados.

Comece pelo [guia do ecossistema](.assistant/README.md). O prefixo `x_` foi criado
deliberadamente para não sugerir que prompts, projetos, snippets ou scripts sejam
interfaces auto-descobertas pela Genie Code.

O arquivo `manifest.mf` da exportação original foi preservado apenas como evidência
de origem em `.assistant/x_docs/x_original_export_manifest.json`; ele não é
necessário para implantar as skills em um Git folder.

Leia também:

- [relatório completo](x_delivery/AUDIT_AND_IMPLEMENTATION_REPORT.md);
- [handoff para a Genie Code](x_delivery/GENIE_CODE_HANDOFF.md);
- [resultados de validação](x_delivery/validation_results.json).
