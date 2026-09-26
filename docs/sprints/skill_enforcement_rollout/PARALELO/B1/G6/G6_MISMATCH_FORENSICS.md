# G6 mismatch forensics — análise local de evidência

## Escopo

Fonte única:
`remote_content_verify.json` já gerado na tentativa 2.

Operações permitidas:
- leitura local do JSON;
- parse/classificação;
- geração de resumo sanitizado fora do repo;
- Git read-only para mapear paths e blobs, se necessário.

Operações proibidas:
- qualquer comando `databricks`;
- nova tentativa de verify;
- publicação;
- import/export remoto;
- probes;
- Genie;
- cleanup.

## Saída exigida

Para cada erro:
- classe;
- path sanitizado relativo ao pacote;
- se também aparece em outra classe;
- object type esperado;
- área do pacote;
- se o path existe no R7/G6 local;
- classificação provável: `REMOTE_MISSING`, `REMOTE_STALE_CONTENT`, `REMOTE_READ_FAILURE_NON_MISSING`, `OTHER`.

Também produzir:
- número de paths únicos;
- interseção missing ∩ incomplete-read;
- paths incomplete-read fora de missing;
- path único de conteúdo divergente;
- se há objetos obsoletos/tipos errados/skills inesperadas (se presentes no errors[]).

Não inferir causa operacional além do que o relatório sustenta.
