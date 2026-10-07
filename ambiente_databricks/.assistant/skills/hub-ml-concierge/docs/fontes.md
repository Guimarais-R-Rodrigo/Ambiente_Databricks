# Fontes e compatibilidade de uso

Use o Hub efetivamente acessível na instalação autorizada. Confirme arquivos, contratos e versão; uma inspeção antiga de repositório não comprova o runtime atual.

## Fontes oficiais

**D1. Databricks — Extend Genie Code with agent skills.** Reconferida em 2026-09-12; documentação em inglês atualizada em 2026-09-11.
https://docs.databricks.com/gcp/en/genie-code/skills

Sustenta o mecanismo de seleção por relevância ou menção, os locais de instalação e o uso de recursos relativos. A documentação admite scripts, mas esta versão usa somente instruções e ferramentas de leitura já disponíveis.

**D2. Agent Skills — Specification.** Reconferida em 2026-09-12.
https://agentskills.io/specification

Sustenta o formato básico e a separação progressiva dos recursos. O padrão admite campos opcionais; o Hub adota um subconjunto conservador de frontmatter, preservado aqui.

## Convenções próprias, não recursos nativos

As rotas `DIRECT_ROUTE`, `HELPER_ROUTE`, `COMPOSITE_ROUTE`, `BRIEFING_FIRST`, `GAP` e `ACCESS_BLOCKED`, a variável conceitual `HUB_ROOT`, os templates, o limite inicial de shortlist e a rubrica de confiança são convenções deste pacote. Não são APIs nem garantias oficiais da Databricks.

## Limites de compatibilidade

O procedimento depende de leitura/pesquisa que o assistente realmente consiga realizar. A skill não cria essa capacidade, não garante acesso recursivo e não invoca outra skill por imprimir seu nome.

O verificador local usa Python 3.10+ e biblioteca padrão. Não exige Spark, MLflow, credenciais ou conectores. Seu sucesso não certifica roteamento, qualidade de recomendações, permissões ou execução Databricks. O registro de manutenção não confirma essas superfícies para uma instalação nova.

Os testes e exemplos não contêm dados reais. Evidências futuras devem preservar essa separação e evitar identidades corporativas, segredos ou payloads de clientes.

[Registro de manutenção e fonte anterior](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/readme-readequacao-20261006/docs/auditoria/2026-10-06_readmes/concierge/docs/fontes.md). Esse documento está no repositório externo, não no pacote de uso.
