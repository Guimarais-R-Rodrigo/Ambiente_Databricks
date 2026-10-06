# Fontes, base examinada e compatibilidade

## Base interna

Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`.
Base da integração: `f748c144dbb6909c7437b53498b25dd4f4854ab7`.
Base histórica do protótipo: `9fa737104110354c0ec0ca5c4b6d3e5a0574c629`.
Reconferência para integração: 2026-09-12. A referência identifica o conteúdo examinado, não uma instalação remota.

Arquivos estruturantes consultados nesta elaboração ou na análise precedente desta conversa, com estado confirmado na referência acima:

- `CLAUDE.md`, `AGENTS.md` e `.claude/CLAUDE.md`: camadas e fluxo de trabalho.
- `.claude/rules/fonte-de-verdade.md` e `.claude/rules/docs-e-readmes.md`: isolamento e hierarquia editorial.
- `ambiente_fonte/.assistant/hub_padroes/skill/template.md`: corpo, frontmatter conservador, recursos relativos e testes.
- `docs/decisions/ADR-0004-declaracao-explicita-de-helpers.md`: risco da descoberta universal e declaração de helpers.
- `docs/decisions/ADR-0010-manual-tecnico-unificado.md`: inventário integrado e redação única.
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`, seções `catalogo-helpers` e `metodos`: mapa de recursos.
- READMEs de `.assistant`, `skills`, `hub_scripts`, `hub_snippets` e `hub_micromodelos`: escopos e formas de ativação.
- `tools/project_policy.py`, `tools/validate_assistant.py` e `docs/testes/forward/README.md`: integração futura e distinção dos gates.

Esses caminhos são referências no repositório, não promessas de disponibilidade dentro de um pacote instalado isoladamente. Na operação, o Concierge deve conferir o Hub efetivamente acessível.

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

O verificador local usa Python 3.10+ e biblioteca padrão. Não exige Spark, MLflow, credenciais ou conectores. Seu sucesso não certifica roteamento, qualidade de recomendações, permissões ou execução Databricks. Não houve homologação dessas superfícies nesta entrega.

Os testes e exemplos não contêm dados reais. Evidências futuras devem preservar essa separação e evitar identidades corporativas, segredos ou payloads de clientes.
