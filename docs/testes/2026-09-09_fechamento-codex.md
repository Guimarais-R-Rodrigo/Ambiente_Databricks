# Fechamento Codex — publicação, conteúdo, smoke e roteamento

Data: 09/09/2026 · Ambiente: Databricks Free · dados: sintéticos.

## Resultado

| Gate | Resultado |
|---|---:|
| gate local | 3/3 etapas aprovadas |
| regressões da biblioteca | 45 PASS |
| guardas de ferramentas | 33 PASS |
| pacote implantável | 316 arquivos + manifesto; commit `8187fac` |
| verify remoto aprofundado | 316/316 conteúdos comparados; 0 problemas |
| Agent Skills | 13/13 |
| extensões `hub_` | 4/4 |
| smoke Spark 4.2.0 | 146 total; 137 PASS; 0 FAIL; 8 opcionais; 1 bloqueio esperado |
| forward tests | 39/39 PASS |

O workspace contém ainda um `.assistant/.mcp_servers.json` gerenciado pela
plataforma. Ele ficou fora do pacote e foi preservado. A verificação aprofundada
comparou inventário, tipos e conteúdo exportado, com normalização limitada a fim
de linha e quebra terminal de notebook.

## Aprendizado das rodadas

O primeiro smoke encontrou duas falhas e foi rejeitado: `format="ISO8601"` não
era compatível com o pandas do runtime, e uma fixture Spark totalmente nula não
tinha schema explícito. O segundo eliminou ambas e revelou que um cenário legado
precisava optar por `on_duplicate_dates="keep"`. A terceira execução, run
`186787319038743` e task `791248932732477`, fechou com `fail=0`.

Resultado estruturado: [JSON resumido](spark/resultados/2026-09-09_smoke_codex_final.json).
Roteamento: [rodada 3](forward/resultados/2026-09-09_rodada3.md).

## Limites

- As 16 famílias de prompts mantêm contrato estático 16/16, mas ainda não têm
  uma rodada conversacional autocontida e comparável. A cota não está mais
  bloqueando; falta definir dados sintéticos e rubrica por família antes de
  chamar respostas heterogêneas de “teste”.
- O Free não prova ACLs, bibliotecas, políticas ou MLflow do workspace de
  trabalho. A replicação continua dependente do runbook e de aceite no destino.
- A proteção obrigatória de branch não pôde ser habilitada no repositório
  privado sob o plano atual; o workflow de CI foi adicionado e passa a executar
  em pull requests e pushes para `main`.
