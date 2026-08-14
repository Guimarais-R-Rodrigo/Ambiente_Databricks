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

| Data | Tema | Nível | Resultado |
|---|---|---|---|
| — | (nenhuma auditoria formal registrada ainda) | — | — |
