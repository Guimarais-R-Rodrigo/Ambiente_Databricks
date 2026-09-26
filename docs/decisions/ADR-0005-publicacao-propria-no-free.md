# ADR-0005 — Publicação própria no Free, adotando o padrão do engine do Hub sem consumi-lo

Data: 2026-08-14
Status: Aceito · supersede o ADR-0002 · **critério de conferência
supersedido** pelo [ADR-0008](ADR-0008-criterios-de-conferencia-da-publicacao.md)
(2026-08-17). As três fases e o gate `--execute` continuam valendo.
Autor: Claude

## Contexto

O ADR-0002 decidiu consumir o engine `databricks-genie` do Verg_Alchemy_Hub para
publicar no Databricks Free, evitando duplicar tooling testado. A decisão foi
tomada antes de examinar o engine em detalhe. A inspeção do código
(`src/databricks_genie/engine.py`) e dois testes no workspace produziram
evidência que inviabiliza o consumo direto para esta camada.

**Primeiro impedimento — `.py` viraria notebook.** O engine decide o formato de
importação em `_fmt_args`: arquivos `.py` são enviados com
`--format SOURCE --language PYTHON`. Teste no workspace, com o mesmo arquivo:

| Formato usado | `object_type` resultante |
|---|---|
| `--format AUTO` | `FILE` |
| `--format SOURCE --language PYTHON` | `NOTEBOOK` |

Os 47 módulos de `x_snippets` precisam ser `FILE`: como notebook,
`from x_snippets.spark.null_summary import null_summary` deixa de funcionar, e a
biblioteca inteira fica inacessível.

**Segundo impedimento — cabeçalho invalidaria as skills.** O engine antepõe um
cabeçalho de não-canonicidade ao conteúdo (`build_header`). Em um `SKILL.md`,
qualquer texto antes do `---` inicial descaracteriza o frontmatter YAML, e a
skill deixa de ser descoberta. Só o modo `nenhum` é utilizável aqui.

**Terceiro ponto — escala e forma da camada.** O manifesto do Hub descreve 9
arquivos de governança, majoritariamente Markdown, com limites de caracteres por
entrada. Esta camada tem 164 arquivos que formam uma árvore a ser espelhada
integralmente, sem limites por arquivo. Consumir o engine exigiria gerar 164
entradas de manifesto e desabilitar cabeçalho e limite em todas — ou seja,
usar apenas o laço de publicação, corrigindo antes um defeito que quebraria o
resultado.

## Decisão

Publicar a partir deste repositório, com `tools/publicar_free.py`, **adotando o
padrão de três fases do engine do Hub**: `render` (o simulado já existente),
`publish` com gate explícito `--execute`, e `verify` read-only. A resolução do
usuário por `databricks current-user me` também é herdada do engine.

O `ADR-0002` fica supersedido: o padrão foi reaproveitado, o código não.

## Alternativas consideradas

- **Corrigir o engine no Hub e consumi-lo** — rejeitada por ora: alterar
  `_fmt_args` muda o comportamento de publicação de outro projeto, cujo próprio
  `write_evidence.py` é hoje publicado como notebook. Mudança nesse repositório
  cabe ao dono dele, com testes próprios; fica registrada como observação a
  encaminhar.
- **Manter `import-dir` avulso, sem ferramenta** — rejeitada: sem plano prévio e
  sem verificação, o estado remoto diverge silenciosamente da fonte. Foi o que
  aconteceu antes desta decisão (ver consequência abaixo).

## Consequências

- A publicação passa a ter plano antes de agir, gate consciente e conferência
  independente após o fato.
- O `verify` cobre um ponto cego do `import-dir`: ele sobrescreve, mas nunca
  apaga. Na primeira execução detectou `.assistant/.mcp_servers.json` — arquivo
  legado inerte que a auditoria do Codex havia removido do pacote e que
  sobrevivera no workspace, reintroduzindo a confusão sobre configuração de MCP.
  Removido.
- Custo assumido: manter uma ferramenta local de ~180 linhas. Em troca, a
  publicação valida o que importa para esta camada — `.py` como `FILE`, 12
  skills, 6 diretórios de extensão, ausência de obsoletos.

## Referências

- Ferramenta: `tools/publicar_free.py`; skill: `.claude/skills/publicar-free/`
- Engine de origem do padrão: `Verg_Alchemy_Hub/src/databricks_genie/engine.py`
- ADR supersedido: [ADR-0002](ADR-0002-engine-databricks-genie-hub.md)
