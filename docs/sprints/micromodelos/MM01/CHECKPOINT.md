# MM01 — Checkpoint

Status: **CORRIGIDA APÓS A1; RETESTE TÉCNICO VERDE; REAUDITORIA A1 PENDENTE; NÃO ACEITA; NÃO INTEGRADA**

## Base e superfície

- `main` inicial da iniciativa MM01: `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- a candidata foi reconciliada sucessivamente com as bases pós-V10 e pós-V11 antes do reteste final;
- branch: `micromodelos/mm01-contrato-canonico`;
- PR: `#51`;
- MM00: encerrada e integrada;
- MM02: bloqueada até reauditoria A1, aceite explícito e merge desta sprint.

## O que a candidata entrega

1. schema formal `1.0.0` para `micromodelo.yaml`;
2. template YAML inicial válido e sanitizado;
3. máquina de fases com rework explícito e `PUBLICADO` terminal por versão;
4. comparação opcional com especificação anterior confiável (`--previous`) para verificar transição real, impedir rewind pós-`PUBLICADO` na mesma versão e recusar regressão de versão, sem antecipar fingerprint/MM02;
5. condições operacionais ortogonais (`ATIVO`, `BLOQUEADO`, `SUSPENSO`, `DEPRECATED`);
6. proveniência `DESCOBERTO`, `INFERIDO`, `PROPOSTO`, `APROVADO`, `MEDIDO` com gates próprios;
7. rejeição de referências auditáveis semanticamente vazias, incluindo whitespace e caracteres invisíveis;
8. proteção explícita de `FALSE` versus `INDETERMINADO`, inclusive contra equivalência apenas cosmeticamente diferente;
9. política estruturada de publicação que não permite contradizer o tratamento de `INDETERMINADO` com uma descrição que o converta implicitamente em `FALSE`;
10. score 0–100 com semântica/normalização e calibração medida antes de linguagem probabilística;
11. integridade referencial de `score.calibracao.evidencia_ref` contra experimento existente, executado e medido;
12. limiares e pesos podem permanecer `PROPOSTO` nas fases pré-gate e passam a exigir `APROVADO` a partir de `EM_VALIDACAO`;
13. gates humanos para validação, regras materiais e política de publicação;
14. escopo de fontes fail-closed em `CATALOGO_PRODUTO`, sem override de CLI;
15. recusa de chaves duplicadas em YAML/JSON e de IDs duplicados em coleções controladas;
16. conteúdo material mínimo obrigatório ao entrar em `EM_VALIDACAO`;
17. coerência entre fase e status da interface de publicação, com caminhos positivos testados até `PUBLICADO`;
18. fronteira de tracking preservada para MM06;
19. validador de referência/CI, fixtures sintéticos e suíte com **24 métodos de teste**;
20. gate permanente `.github/workflows/micromodelos-mm01-ci.yml`, read-only e sem acesso a ambiente corporativo;
21. pacote neutro para auditoria A1 independente.

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

A primeira A1 independente auditou o head pré-correção e concluiu `NAO_APTA`. Foram registrados cinco achados bloqueantes, todos confirmados como procedentes no contraditório:

1. proteção histórica insuficiente contra rewind de uma versão já `PUBLICADO`;
2. referências de aprovação, medição e publicação podiam ser semanticamente vazias;
3. `PROPOSTO` para limiares/pesos era rejeitado antes da fase que exige aprovação;
4. política de `INDETERMINADO` podia conter descrição contraditória com o tratamento estruturado;
5. calibração probabilística podia apontar para `evidencia_ref` órfã.

O relatório original permanece histórico e não será reclassificado ou reescrito.

## Correções e evidência técnica

As cinco correções foram implementadas dentro das fronteiras da MM01. O reteste transitório final `34909835696` concluiu com `success` depois de preparar a mesma árvore permanente que seria publicada:

- `python -B -m unittest tools/tests/test_micromodelo_mm01.py -v`: **24 métodos, OK**;
- `python -B tools/validate_assistant.py --root ambiente_fonte`: **APROVADO, 0 falhas, 0 avisos**;
- mecanismo transitório e script de aplicação removidos antes do commit das correções;
- nenhum artefato de MM02, MM03, MM06, publicação real, visual ou migração foi introduzido.

A métrica verificável do README raiz foi recalibrada para a árvore permanente final. Os workflows permanentes precisam ser observados novamente no HEAD documental final desta candidata; seus IDs ficarão na descrição da PR para evitar commit autorreferente.

## Gate independente pendente

A candidata corrigida precisa passar por **reauditoria A1 independente** em sessão separada. A reauditoria deve partir do novo HEAD e repetir os gates mínimos e os cinco adversariais que motivaram o primeiro veredito.

O pacote permanece em:

```text
docs/auditoria/2026-09-14_micromodelos-mm01/
├── 01_contexto.md
└── 02_prompt_auditoria.md
```

O auditor não deve implementar correções e não deve usar a documentação narrativa da sprint para confirmar a intenção do autor.

## Gates restantes

1. confirmar os checks permanentes do HEAD documental final e estabilidade da `main`;
2. executar reauditoria A1 em sessão independente;
3. confrontar eventual novo achado com a árvore;
4. corrigir/retestar somente se houver achado procedente;
5. apresentar checkpoint final para aceite explícito;
6. integrar a PR #51 somente após o aceite.

Enquanto qualquer item acima estiver pendente, **MM02 permanece bloqueada**.
