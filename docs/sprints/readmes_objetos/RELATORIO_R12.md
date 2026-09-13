# Relatório R12 — integração de navegação por categoria

R12 cria seis índices locais em `hub_snippets`: `constants`, `display`, `ml`, `spark`, `testing` e `visual`, e reconcilia o catálogo geral, a entrada `.assistant` e o Manual Técnico. Não cria objetos nem altera os 75 READMEs operacionais. `hub_snippets/tests/` permanece infraestrutura interna. O freeze exige cobertura exata, links válidos, equivalência fonte/simulado, snapshot real e `ci_local`. Não cobre publicação, Databricks Runtime, Genie Code ou auditoria independente.

## Correção pós-freeze do snapshot — 2026-09-13

A CI permanente do PR observou `repo (identidade) = 1303`, enquanto o freeze havia registrado 1302 porque `FREEZE_R12.txt` foi criado depois da captura do snapshot. A correção altera somente o snapshot do README raiz; o arquivo histórico de freeze permanece intacto. Links, cobertura 75/75 e demais métricas permaneceram iguais.
