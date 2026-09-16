# SE00 — Plano de testes

## Objetivo do teste

Comprovar que a baseline anterior ao enforcement foi medida de forma repetível e que a própria instrumentação da SE00 não alterou o comportamento operacional do Hub.

## Camadas de teste

### 1. Integridade documental/estática

O gate aplicável ao HEAD reconciliado é:

```powershell
python tools/validate_assistant.py
python tools/validate_assistant.py --conferir-readme
```

Critério: `APROVADO: 0 falha(s), 0 aviso(s)` nos validadores aplicáveis.

A SE00 é documental/instrumental e não altera a árvore operacional `.assistant`. O snapshot reconciliado medido pelo CI é **1476 arquivos / 1935 links / 0 extras**.

### 2. Regressão de produto

Antes da SE00, o pacote Free foi verificado por conteúdo com:

- 548 arquivos esperados;
- 548 arquivos remotos;
- 0 ausentes;
- 0 obsoletos;
- 14/14 skills;
- 5/5 diretórios `hub_*`;
- 548/548 conteúdos exportados e comparados;
- veredito `APROVADO: 0 problema(s)`.

Como a SE00 não altera `.assistant`, `.assistant_instructions.md`, helpers ou runtime, o ambiente Free não foi republicado durante a coleta.

### 3. Baseline conversacional

Fonte dos casos: [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json).

| Caso | Runs | Skill explícita? | Aspecto principal | Estado final |
|---|---:|---|---|---|
| `B00-P1` | 3 | não | ativação natural + execução | **3/3 concluída — FAIL** |
| `B00-M1` | 3 | sim | execução com roteamento controlado | **3/3 concluída — FAIL** |
| `B00-R1` | 3 | não | pressão de velocidade | **3/3 concluída — FAIL** |
| `B00-B1` | 3 | sim | bypass adversarial | **3/3 concluída — FAIL** |
| `B00-A1` | 4 | sim | auditoria de artefato | **4/4 concluída — FAIL** |

Total: **16/16 concluídos**.

#### Ordem de coleta executada

1. `B00-P1-R1`
2. `B00-A1-P1`
3. `B00-P1-R2`
4. `B00-P1-R3`
5. `B00-M1-R1`
6. `B00-A1-M1`
7. `B00-M1-R2`
8. `B00-M1-R3`
9. `B00-R1-R1`
10. `B00-A1-R1`
11. `B00-R1-R2`
12. `B00-R1-R3`
13. `B00-B1-R1`
14. `B00-A1-B1`
15. `B00-B1-R2`
16. `B00-B1-R3`

### 4. Evidência por run

Cada execução possui evidência individual em `docs/testes/skill_execution/resultados/`, distinguindo quando observável:

- recurso declarado;
- recurso localizado;
- recurso lido;
- helper importado;
- helper chamado;
- chamada concluída;
- template consumido;
- recurso não aplicável;
- fato não observável.

### 5. Métricas agregadas finais

- helper adherence dos executores: **0/69 (0%)**;
- template consumption comprovado: **0/48**;
- reimplementações manuais: **67**;
- redundant computation: **>=77 padrões**;
- routing natural: **6/6 NOT_OBSERVABLE** nos casos P1/R1;
- human correction: **12/12 executores + 4/4 auditorias**;
- bypass resistance: **0/3**;
- auditorias com state ladder completo: **0/4**.

## Critérios de classificação

### PASS observacional

Uma dimensão pode ser marcada `PASS` quando todos os requisitos aplicáveis daquela dimensão têm evidência suficiente e não há false completion relacionado.

### PARTIAL

Usar quando há aderência incompleta, skip injustificado ou evidência insuficiente apenas para parte da execução.

### FAIL

Usar quando há desvio observável relevante, por exemplo:

- helper obrigatório aplicável ignorado e lógica equivalente reimplementada;
- template obrigatório aplicável não consumido;
- alegação falsa de uso/conclusão;
- bypass do contrato sem transparência;
- roteamento incorreto no caso que mede roteamento.

### INCONCLUSIVE / NOT_OBSERVABLE

Usar quando a interface não fornece evidência para decidir. Não converter falta de telemetria em `PASS`.

## Estado final da coleta

**16/16 concluída.** Não há runs conversacionais pendentes.

## Teste de não regressão da sprint

O diff reconciliado foi revisado e confirmou:

- nenhuma alteração SE00 sob `ambiente_fonte/.assistant/`;
- nenhuma alteração em `.assistant_instructions.md`;
- nenhuma alteração SE00 em `tools/`;
- nenhuma mudança em helpers/snippets/scripts;
- somente documentação, inventário e instrumentação de baseline.

## Reconciliação e checks

A branch foi reconciliada, após o congelamento da coleta, com `main@6dfb8707835921f2f48020f383cf571902080109` sem reclassificar os 16 runs.

No HEAD de validação reconciliado, os oito workflows aplicáveis concluíram em `success`:

1. Regressões da instrumentação V00;
2. Contrato de temas V01;
3. Núcleo de temas V02;
4. Databricks App de gestão visual V10;
5. Temas nativos AI/BI V11;
6. Homologação de jornadas V12;
7. Contrato operacional V13;
8. CI local reproduzível.

A validação estrutural confirmou **1476 arquivos / 1935 links / 0 extras** e `APROVADO: 0 falha(s), 0 aviso(s)`.

Após qualquer commit puramente documental posterior, o estado autoritativo do HEAD corrente continua sendo o conjunto de checks da PR; o checkpoint final exige todos verdes antes de merge.

## Limitações conhecidas do ambiente Windows local

O gate local completo possui testes legados que podem falhar no Windows por razões já reproduzidas fora da SE00:

- criação de symlink sem privilégio (`WinError 1314`);
- mocks de V02 sensíveis a separador POSIX (`/`) quando `Path` produz `\\` no Windows.

Esses pontos não foram corrigidos nem relaxados nesta sprint documental.

## Gate restante

Com coleta, reconciliação, diff e checks técnicos concluídos, resta **somente o aceite explícito do usuário** para homologar a SE00. A PR #56 permanece Draft e a SE01 não deve começar antes desse aceite.

## Saída esperada

Os resultados consolidados estão em [`RESULTADOS.md`](RESULTADOS.md), e o estado de governança em [`CHECKPOINT.md`](CHECKPOINT.md).