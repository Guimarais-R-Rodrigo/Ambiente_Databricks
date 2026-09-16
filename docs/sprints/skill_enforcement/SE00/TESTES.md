# SE00 — Plano de testes

## Objetivo do teste

Comprovar que a baseline anterior ao enforcement foi medida de forma repetível e que a própria instrumentação da SE00 não alterou o comportamento operacional do Hub.

## Camadas de teste

### 1. Integridade documental/estática

Executar no HEAD final/reconciliado da branch `sef/SE00-baseline`:

```powershell
python tools/validate_assistant.py
python tools/validate_assistant.py --conferir-readme
```

Critério: `APROVADO: 0 falha(s), 0 aviso(s)` nos validadores aplicáveis.

A SE00 é documental/instrumental; não deve exigir alteração na árvore operacional `.assistant`. Se o renderer for executado no Windows, o conhecido efeito de EOL em `Novo_Ambiente_Simulado/README_GERADO.md` deve ser tratado separadamente e não confundido com mudança de produto.

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

Como a SE00 não altera `.assistant`, `.assistant_instructions.md`, helpers ou runtime, **não republicar** o ambiente apenas por causa dos documentos desta sprint.

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

## Estado atual da coleta

**16/16 concluída.** Não há runs conversacionais pendentes.

## Teste de não regressão da sprint

Antes de pedir aceite da SE00, revisar o diff da PR e confirmar:

- nenhuma alteração sob `ambiente_fonte/.assistant/`;
- nenhuma alteração em `.assistant_instructions.md`;
- nenhuma alteração em `tools/`;
- nenhuma mudança em helpers/snippets/scripts;
- somente documentação, inventário e instrumentação de baseline.

Qualquer arquivo comportamental no diff bloqueia o fechamento da SE00.

## Checks ainda obrigatórios

1. sincronizar/reconciliar a branch com a `main` atual sem reclassificar os runs;
2. executar/reexecutar `validate_assistant.py` e `--conferir-readme` no HEAD reconciliado;
3. registrar workflows/checks remotos aplicáveis;
4. revisar o diff final após reconciliação;
5. obter aceite explícito do usuário.

## Limitações conhecidas do ambiente Windows local

O gate local completo possui testes legados que podem falhar no Windows por razões já reproduzidas fora da SE00:

- criação de symlink sem privilégio (`WinError 1314`);
- mocks de V02 sensíveis a separador POSIX (`/`) quando `Path` produz `\\` no Windows.

Esses pontos não devem ser silenciosamente ignorados. A correção de portabilidade deve ocorrer em frente técnica própria, não nesta sprint documental.

## Saída esperada

Os resultados consolidados estão em [`RESULTADOS.md`](RESULTADOS.md), e o estado de governança em [`CHECKPOINT.md`](CHECKPOINT.md). **Não iniciar SE01 antes do aceite formal da SE00.**