# MM01 — Checkpoint

Status: **CORRIGIDA APÓS SEGUNDA A1; RETESTE DE CONSTRUÇÃO VERDE; TERCEIRA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**

## Base e superfície

- `main` inicial da iniciativa MM01: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- a candidata foi reconciliada sucessivamente com as bases pós-V10 e pós-V11;
- base vigente na segunda A1: `d106ef3158e5827a2eec3aa183dbb3b47885c960`;
- branch: `micromodelos/mm01-contrato-canonico`;
- PR: `#51`;
- MM00: encerrada e integrada;
- MM02: bloqueada até nova A1, aceite explícito e merge desta sprint.

## O que a candidata entrega

1. schema formal `1.0.0` para `micromodelo.yaml`;
2. template YAML inicial válido e sanitizado;
3. máquina de fases com rework explícito e `PUBLICADO` terminal por versão;
4. comparação opcional com especificação anterior confiável (`--previous`) para verificar transição real, impedir rewind pós-`PUBLICADO` na mesma versão e recusar regressão de versão, sem antecipar fingerprint/MM02;
5. condições operacionais ortogonais (`ATIVO`, `BLOQUEADO`, `SUSPENSO`, `DEPRECATED`);
6. proveniência `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO`, `MEDIDO` com gates próprios;
7. regra positiva de materialidade textual: referências auditáveis precisam conter letra/número Unicode após NFKC; whitespace, controles, zero-width, variation selectors e marcas combinantes isoladas não contam;
8. proteção explícita de `FALSE` versus `INDETERMINADO`, inclusive contra equivalência apenas cosmeticamente diferente;
9. política de ausência de evidência totalmente estruturada por `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência, sem prosa normativa livre;
10. política de publicação de `INDETERMINADO` totalmente estruturada, com `indeterminado_vira_false=false` e `regra_ref` somente para `OUTRA_APROVADA`;
11. score 0–100 cuja natureza é determinada exclusivamente por `tipo_semantica`; campo livre `score.semantica` não faz parte do schema;
12. normalização de score estruturada por método/referência/proveniência, sem frase livre normativa;
13. calibração probabilística somente para `PROBABILIDADE_CALIBRADA`, com integridade referencial contra experimento existente, executado e medido;
14. limiares e pesos podem permanecer `PROPOSTO` nas fases pré-gate e passam a exigir `APROVADO` a partir de `EM_VALIDACAO`;
15. gates humanos para validação e demais decisões materiais;
16. escopo de fontes fail-closed em `CATALOGO_PRODUTO`, sem override de CLI;
17. recusa de chaves duplicadas em YAML/JSON e de IDs duplicados em coleções controladas;
18. conteúdo material mínimo obrigatório ao entrar em `EM_VALIDACAO`;
19. coerência entre fase e status da interface de publicação, com caminhos positivos testados até `PUBLICADO`;
20. fronteira de tracking preservada para MM06;
21. validador de referência/CI, fixtures sintéticos e suíte com **26 métodos de teste**;
22. gate permanente `.github/workflows/micromodelos-mm01-ci.yml`, read-only e sem acesso a ambiente corporativo;
23. pacote neutro de auditoria com os resultados históricos da primeira e segunda A1 preservados.

## O que não foi feito

- não foi criada `hub-ml-micromodelos`;
- não foi alterada a lista de skills roteáveis;
- não foi criado sétimo tipo em `hub_padroes`;
- não foi criado fingerprint nem qualquer hash material da especificação;
- não houve descoberta de metadata;
- não houve leitura de dados;
- não houve alteração de `mlflow_run`;
- não houve integração visual específica da MM01; V11 foi absorvida apenas como base do repositório;
- não houve handoff/publicação real;
- não houve migração de legado.

## Primeira auditoria A1

A primeira A1 independente auditou o head pré-correção e concluiu `NAO_APTA`. Cinco achados bloqueantes foram confirmados como procedentes: proteção histórica contra rewind, referências semanticamente vazias, gate prematuro para `PROPOSTO`, contradição de `INDETERMINADO` por prosa e calibração com referência órfã. O relatório permanece em `03_resultado_a1.md`.

As cinco correções foram implementadas, a suíte passou a 24 métodos e o reteste de construção `34909835696` ficou verde.

## Segunda auditoria A1

A reauditoria independente sobre `2783bcbd6ad7f07f9f3893c66c9dc36d0557f57e` também concluiu `NAO_APTA`. Três novos achados bloqueantes foram confirmados como procedentes:

1. referências compostas exclusivamente por marcas Unicode `M*` ainda satisfaziam materialidade;
2. `FALSE` × `INDETERMINADO` ainda dependia parcialmente de interpretação de prosa livre por regex;
3. semântica probabilística ainda podia ser escondida por sinônimos não cobertos pela regex.

O resultado está preservado em `04_resultado_a1_reauditoria.md` e não foi reclassificado.

## Correções da segunda A1

As três correções foram estruturais, sem ampliar escopo:

- `_has_material_text` passou a exigir positivamente letra/número Unicode após NFKC;
- campos de descrição normativa foram removidos das políticas de ausência e publicação; comportamento executável ficou fechado em campos estruturados;
- `score.tipo_semantica` passou a ser a única autoridade executável sobre natureza probabilística; `score.semantica` livre foi removido e `score.normalizacao` virou contrato estruturado.

O workflow transitório `34912665666` preparou a árvore sem os próprios mecanismos temporários e então executou:

- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`: **26 métodos, OK**;
- `python -B tools/validate_assistant.py --root ambiente_fonte`: **APROVADO, 0 falhas, 0 avisos**;
- commit permanente das correções: `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`.

Esse run comprova a construção da correção, mas não substitui os workflows permanentes do próximo HEAD documental congelado.

## Dívida documental antes do merge

O bloco MM01 do `CHANGELOG.md` ainda descreve a candidata pré-A1. Ele deve ser sincronizado **antes do merge**, por operação que preserve byte a byte o histórico anterior. Essa pendência não deve ser usada para apagar ou reclassificar as auditorias históricas.

## Gate independente pendente

Como a candidata mudou materialmente após a segunda A1, é obrigatória uma **terceira A1 independente** sobre o próximo HEAD congelado. O auditor deve repetir os gates mínimos e construir adversariais próprios, sem usar `03_resultado_a1.md` ou `04_resultado_a1_reauditoria.md` como prova da correção.

## Gates restantes

1. congelar e validar os workflows permanentes do HEAD documental final;
2. executar terceira A1 em sessão independente;
3. confrontar qualquer novo achado com a árvore e corrigir/retestar somente se procedente;
4. sincronizar o bloco MM01 do `CHANGELOG.md` preservando o histórico;
5. revalidar a árvore exata depois dessa sincronização;
6. apresentar checkpoint final para aceite explícito;
7. integrar a PR #51 somente após o aceite.

Enquanto qualquer item acima estiver pendente, **MM02 permanece bloqueada**.
