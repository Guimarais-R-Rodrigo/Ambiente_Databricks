# ADR-0004 — Declaração explícita de helpers nas skills, em vez de descoberta em tempo de chat

Data: 2026-08-14
Status: Aceito · **localização e forma supersedidas** pelo
[ADR-0007](ADR-0007-catalogo-e-pasta-de-objeto.md) (2026-08-17). A decisão de
fundo — declaração explícita de helpers — continua valendo e é reafirmada lá.
Os caminhos `x_snippets/`, `x_scripts/` e `x_docs/` descritos abaixo são de
14/08 e não existem mais.
Autor: Claude

## Contexto

O ecossistema mantém 54 helpers curados (47 módulos em `x_snippets/`, 7 em
`x_scripts/`) com lógica analítica não trivial: PSI com bins derivados da
referência, split temporal por período de calendário, WOE/IV, curvas de safra,
bandas de score com direção declarada. Essa lógica foi auditada, corrigida e
verificada no runtime (64 checks, 0 falhas).

Levantamento em 2026-08-14: **nenhum dos 12 `SKILL.md` cita um helper sequer**.
As únicas três referências do pacote estão em templates auxiliares. Na prática,
quando uma skill é acionada, o Genie Code não recebe informação de que a
biblioteca existe — e reescreve do zero a lógica que já está implementada e
testada. O ambiente anterior mostra o custo dessa lacuna: continha um cálculo de
PSI incorreto, baseado em média e desvio, gerado dessa forma.

Duas abordagens foram consideradas para fechar a lacuna.

## Decisão

Cada `SKILL.md` declara explicitamente os helpers do seu fluxo, em seção curta e
padronizada, com instrução de não reimplementar a lógica correspondente. Um
catálogo completo demanda → helper fica em `x_docs/catalogo_helpers.md`,
consultável sob demanda. A skill `rodrigo-auditoria-skills` ganha verificação de
aderência: output que reimplementa lógica disponível na biblioteca vira achado.

A decisão de qual helper serve a qual fluxo é tomada em tempo de engenharia,
registrada no repositório, e revisada por auditoria.

## Alternativas consideradas

- **Skill dedicada que varre a biblioteca e avalia aplicabilidade a cada
  demanda** — rejeitada por três motivos: (a) sua `description` se sobreporia à
  de todas as demais, degradando o roteamento que acabou de ser certificado em
  36/36; (b) exigiria leitura de dezenas de módulos dentro do chat, com custo de
  contexto proporcional e resultado não determinístico entre conversas; (c)
  reintroduziria no LLM uma decisão que já é conhecida e estável, contrariando a
  razão de existir da biblioteca.
- **Manter a referência apenas nos templates** — rejeitada: templates são
  carregados tarde ou não são carregados, e a evidência mostra cobertura de 3 em
  12 skills.

## Consequências

- O helper passa a ser sugerido no momento em que a skill é acionada, sem custo
  adicional de roteamento: a seleção automática lê apenas `name` e `description`
  do frontmatter, e a seção declarada fica no corpo. Os forward tests aprovados
  permanecem válidos.
- Cada skill nova ou alterada passa a exigir uma decisão consciente sobre
  helpers, verificável em auditoria.
- Custo assumido: a declaração precisa acompanhar mudanças na biblioteca. O
  catálogo centraliza a manutenção e a rubrica de auditoria detecta divergência.

## Referências

- Catálogo: `ambiente_fonte/.assistant/x_docs/catalogo_helpers.md`
- Verificação de runtime dos helpers: `docs/testes/spark/README.md`
- Certificação de roteamento: `docs/testes/forward/README.md`

## Atualização de status — 2026-09-12

O [ADR-0011](ADR-0011-concierge-hub.md) aceita descoberta solicitada, limitada e progressiva pelo Concierge, sem substituir declarações de helpers nas skills. A alternativa de varredura universal indiscriminada continua rejeitada. O corpo histórico acima permanece inalterado.
