# SE01 — resultados

## Estado

**EVIDÊNCIA LOCAL/CI PARCIAL REGISTRADA; DATABRICKS FREE AINDA PENDENTE.**

Este arquivo recebe somente resultados realmente observados. Implementação, PR e autorrelato não são promovidos a evidência do Genie Code.

## Candidata observada

- branch: `sef/SE01-contrato`;
- commit que materializou fonte + simulado: `fda26d130e559d3fdb8ee69fcb785ffecc76a049`;
- commit de snapshot medido: `264981cb4ce1a5aff8d3c1f6dd54caa1fa57c174`;
- PR: #69, Draft;
- skill piloto: `hub-ml-eda-profissional`;
- modo do contrato: `audit`.

## Evidência estática confirmada

No workflow dedicado SE01 do commit `fda26d130e559d3fdb8ee69fcb785ffecc76a049`, antes do gate de snapshot:

- contrato v0.1: **PASS — 1/1 contrato válido**;
- recursos declarados: **10**;
- templates declarados: **4**;
- suíte `test_skill_enforcement_se01.py`: **11/11 PASS**;
- `validate_assistant.py`: **APROVADO — 0 falhas / 0 avisos**;
- renderer canônico: **limpo após materialização do espelho**;
- `__pycache__` gerado pelo primeiro subprocesso do probe: corrigido com execução filha `python -B` e não incorporado ao produto.

A suíte cobre explicitamente:

1. contrato canônico válido;
2. módulo/helper inexistente;
3. símbolo não exportado pela API pública;
4. template ausente;
5. `schema_version` não suportada;
6. resource duplicado;
7. condition fora do vocabulário;
8. skill divergente da pasta;
9. tentativa prematura de `mode="enforce"`;
10. resolução pública real de `index_generator`;
11. execução local read-only do capability probe.

## Snapshot medido

O mesmo gate mediu a árvore completa da candidata, já com o simulado materializado:

- Markdown: **222 arquivos / 1396 links relativos**;
- Python AST: **222 arquivos**;
- repo identidade: **1494 arquivos**;
- repo links: **1961**;
- worktree extras: **0**;
- instruções: **9043/20000 caracteres**.

O README raiz foi atualizado no commit `264981cb4ce1a5aff8d3c1f6dd54caa1fa57c174` com esses valores medidos, não estimados.

## Incidente operacional do GitHub Actions

A rodada automática disparada pelo commit de snapshot `264981cb4ce1a5aff8d3c1f6dd54caa1fa57c174` não chegou a executar testes.

Observado em todos os workflows acionados nessa rodada:

- conclusão reportada pelo GitHub: `failure`;
- job sem runner alocado: `runner_id=0`, `runner_name=""`;
- `steps=[]` / `steps=null`;
- duração aproximada de poucos segundos;
- logs de job indisponíveis porque nenhum step iniciou.

Foi feito rerun somente do job SE01, sem alterar a branch. O rerun repetiu o mesmo estado: runner não alocado e zero steps.

**Classificação:** indisponibilidade/recusa operacional do GitHub Actions naquela rodada. Não é classificada como regressão do contrato, dos testes ou do snapshot, porque nenhum desses comandos foi executado.

O gate de CI final permanece **PENDENTE** até existir execução real dos jobs no HEAD vigente.

## Capability probe no Free

- status: **PENDENTE**;
- branch/commit publicado: —;
- verify por conteúdo: —;
- chat novo: —;
- prompt exato: definido em `TESTES.md`;
- marcador bruto: —;
- execução do script observável: —;
- limitações: —;
- veredito: **PENDENTE**.

## Regressão de uso da EDA

- status: **PENDENTE**;
- prompt natural SE00-P1: congelado em `TESTES.md`;
- skill observada: —;
- degradação atribuível ao contrato/probe: —;
- veredito: **PENDENTE**.

## Regra

Não preencher lacunas por inferência. `NOT_OBSERVABLE` é resultado válido e distinto de `PASS`. Uma falha de infraestrutura antes da alocação de runner também não é convertida em `PASS` nem em falha funcional da candidata.