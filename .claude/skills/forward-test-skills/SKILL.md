---
name: forward-test-skills
description: >-
  Executa e registra os forward tests das Agent Skills no Genie Code do
  Databricks Free: caso positivo, caso negativo e @menção por skill, sempre em
  chat novo. Use após publicar/alterar skills no workspace e antes de replicar
  no trabalho.
---

# Forward tests das skills no Genie Code

## Pré-condições

- Workspace Free contém a réplica atual (`tools/render_simulado.py` + publicação).
- Roteiro atualizado em `docs/testes/forward/roteiro.md` — se as `description`
  das skills mudaram desde a última rodada, regenerar o roteiro antes.

## Método (inegociável)

1. **Um chat novo por teste.** Skills editadas não recarregam em chat ativo; um
   chat reaproveitado contamina o resultado seguinte.
2. Colar o prompt do roteiro **sem anexar contexto extra** (o teste mede a
   auto-seleção pela `description`, não a resposta em si).
3. Observar qual skill o Genie Code carrega (indicador na UI). A qualidade da
   resposta NÃO é objeto deste teste.
4. Se o comportamento parecer defasado (descrição antiga), hard refresh no
   navegador e repetir.

## Veredito por caso

| Caso | PASS quando |
|---|---|
| Positivo | a skill alvo é carregada por relevância |
| Negativo | a skill alvo NÃO é carregada (carregar a skill esperada do desvio é bônus) |
| `@menção` | a skill alvo é carregada deterministicamente |

## Registro e ação

- Preencher uma cópia de `docs/testes/forward/template_resultados.md` como
  `docs/testes/forward/resultados/<YYYY-MM-DD>_rodada<N>.md`.
- Falha em positivo/negativo → ajustar a `description` da skill em
  `ambiente_fonte/` (gatilhos mais específicos, exclusões "Não use para...").
  Depois: validar → renderizar → republicar → repetir SOMENTE os casos afetados
  em chat novo.
- Falha em `@menção` → checar path da skill no workspace e frontmatter.
- Fechar a rodada com entrada no `CHANGELOG.md` e, se houve mudança de
  description, listar quais skills mudaram.
