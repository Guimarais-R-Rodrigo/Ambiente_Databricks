# Changelog experimental

## 2026-09-11 — Concierge Hub 0.1.0 (Codex)

**Pedido:** melhorar o uso do Hub, criando a skill, seus templates e documentação fora do conteúdo canônico.

**Entregue:** pacote `skills/hub-ml-concierge/` com procedimento de descoberta progressiva, composição mínima, evidências, tratamento de cobertura parcial e repasse para especialistas; templates de resposta, handoff e registro de busca; documentação de arquitetura, instalação e promoção; matriz de aceite e verificador estático com testes de regressão.

**Escopo:** somente `novas_funcionalidades/`. Não há agente independente, serviço MCP, banco vetorial, catálogo autoral concorrente, script de execução analítica ou alteração das skills existentes.

**Base examinada:** commit `9fa737104110354c0ec0ca5c4b6d3e5a0574c629` do repositório. Datas dos testes e limitações constam em [RESULTADOS](skills/hub-ml-concierge/tests/RESULTADOS.md). O número de versão é do protótipo, não do Hub.

**Não realizado:** instalação no Databricks, forward tests no Genie Code, validação de permissões corporativas, promoção canônica e homologação de produção.
