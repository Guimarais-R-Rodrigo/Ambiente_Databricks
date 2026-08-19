# Auditorias multi-LLM

Uma auditoria multi-LLM submete o mesmo material a mais de um modelo, cada um
trabalhando **sem ver a análise do outro**, e só depois confronta os resultados.
O ganho não é ter mais opiniões: é que modelos diferentes erram de formas
diferentes. O que um deixa passar por viés próprio, outro costuma apontar — e a
divergência entre eles é, por si só, o sinal mais útil, porque marca exatamente
onde o material é ambíguo.

Este projeto já se beneficiou disso antes de qualquer auditoria formal: a análise
do Codex encontrou no ambiente original seis skills sem frontmatter, um cálculo
de PSI incorreto e identificadores corporativos expostos.

## Os quatro níveis

| Nível | Modelos | Quando |
|---|---|---|
| `A0_light` | 1 | revisão de rotina, mudança contida |
| `A1_standard` | 2 | antes de compartilhar com a squad |
| `A2_strict` | 3 | mudança estrutural que vai para o trabalho |
| `A3_incident` | 3+ | algo deu errado e a causa não está clara |

Nunca reduza o nível quando houver dado sensível, publicação externa ou decisão
que afete outras pessoas. Divergência entre modelos sobre comportamento da
plataforma não se resolve por maioria — quem decide é a documentação oficial
(`.claude/rules/genie-code-oficial.md`).

Uma pasta por auditoria: `YYYY-MM-DD_<tema>/`, no padrão do template
`.claude/templates/auditoria.md` (rodadas individuais + consenso).

Gatilhos mínimos de auditoria `A1+` neste projeto (ver `.claude/rules/multi-llm.md`):

- antes de compartilhar o ecossistema com a squad;
- antes de replicar mudança estrutural no workspace do trabalho;
- quando duas IAs divergirem sobre comportamento da plataforma.

## Auditorias realizadas

| Data | Tema | Nível | Resultado |
|---|---|---|---|
| 2026-08-14 | [Biblioteca: `pit_join` e `join_diagnostics`](2026-08-14_biblioteca-pit-join/) | `A1` | 15 achados, **13 procedentes** — corrigidos |
| 2026-08-14 | [Documentação: 8 documentos](2026-08-14_documentacao/) | `A1` | 22 achados, **todos procedentes** — corrigidos |
| 2026-08-15 | [Documentação: 15 READMEs, segunda rodada](2026-08-15_documentacao-rodada2/) | `A1` | 25 achados, **todos procedentes** — corrigidos |
| 2026-08-16 | [Plano de reestruturação do Hub](2026-08-16_plano-hub/) | `A1` | 25 achados, **todos procedentes** — plano reescrito em v2 |
| 2026-08-18 | [Consistência residual e padrão didático](2026-08-18_consistencia-e-didatica/) | `A1` | 18 achados, **todos procedentes** — corrigidos; classe nova: norma publicada sem instrumento |
| 2026-08-19 | [Leitura em contexto longo](2026-08-19_leitura-contexto-longo/) | `A1` **segunda origem** | 3 achados (1 procedente, 1 parcial, 1 improcedente) — e 1 achado forte fora da lista: a regra de idioma contra a biblioteca |

**Esta tabela cobre só as auditorias temáticas.** As auditorias de sprint — uma
por sprint executada, treze até aqui — vivem junto do relatório que auditaram, em
`docs/sprints/`, e estão indexadas na coluna *Auditoria* do registro de execução
em [`PLANO_HUB.md`](../../PLANO_HUB.md). Quem pergunta "o que já foi auditado?"
precisa dos dois lugares.

As **cinco primeiras** rodadas acima usaram o mesmo modelo do autor, em sessão
sem contexto, com acesso ao sistema de arquivos e à CLI. A de 19/08 é a primeira
de **segunda origem**, e a primeira sem execução: outro modelo, lendo o corpus
inteiro numa janela só. O gate do `PLANO_HUB.md` §10 abriu com ela. Isso é `A1`, não `A2`: pontos cegos
compartilhados pelo modelo continuam de pé, e é por isso que a auditoria de
segunda origem sobre a biblioteca permanece como gate aberto antes de usar
`pit_join` em decisão que importe no trabalho.
