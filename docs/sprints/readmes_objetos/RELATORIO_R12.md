# Relatório R12 — integração de navegação por categoria

R12 cria seis índices locais em `hub_snippets`: `constants`, `display`, `ml`, `spark`, `testing` e `visual`, e reconcilia o catálogo geral, a entrada `.assistant` e o Manual Técnico. Não cria objetos nem altera os 75 READMEs operacionais. `hub_snippets/tests/` permanece infraestrutura interna. O freeze exige cobertura exata, links válidos, equivalência fonte/simulado, snapshot real e `ci_local`. Não cobre publicação, Databricks Runtime, Genie Code ou auditoria independente.
