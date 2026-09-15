# SE00 — Plano de testes

## Objetivo do teste

Comprovar que a baseline anterior ao enforcement foi medida de forma repetível e que a própria instrumentação da SE00 não alterou o comportamento operacional do Hub.

## Camadas de teste

### 1. Integridade documental/estática

Executar após sincronizar a branch `sef/SE00-baseline`:

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

Como a SE00 não altera `.assistant`, `.assistant_instructions.md`, helpers ou runtime, **não republicar** o ambiente apenas por causa dos documentos desta sprint. A baseline Free precisa permanecer congelada.

### 3. Baseline conversacional

Fonte dos casos: [`../../../testes/skill_execution/casos_eda.json`](../../../testes/skill_execution/casos_eda.json).

Executar obrigatoriamente em chats novos:

| Caso | Runs | Skill explícita? | Aspecto principal |
|---|---:|---|---|
| `B00-P1` | 3 | não | ativação natural + execução |
| `B00-M1` | 3 | sim | execução com roteamento controlado |
| `B00-R1` | 3 | não | pressão de velocidade |
| `B00-B1` | 3 | sim | bypass adversarial |
| `B00-A1` | 4 | sim | auditoria de artefato |

Total: 16.

### 4. Evidência por run

Para cada execução, preencher uma cópia de [`../../../testes/skill_execution/template_resultado.md`](../../../testes/skill_execution/template_resultado.md).

A evidência deve distinguir:

- recurso declarado;
- recurso localizado;
- recurso lido;
- helper importado;
- helper chamado;
- chamada concluída;
- template consumido;
- recurso não aplicável;
- fato não observável.

### 5. Métricas agregadas

Calcular por família e no total:

- helper adherence;
- template adherence;
- silent reimplementation;
- false completion;
- redundant computation;
- routing success quando aplicável;
- human correction rate.

Percentuais sem numerador/denominador não são aceitos como evidência final.

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

## Teste de não regressão da sprint

Antes de pedir aceite da SE00, revisar o diff da PR e confirmar:

- nenhuma alteração sob `ambiente_fonte/.assistant/`;
- nenhuma alteração em `.assistant_instructions.md`;
- nenhuma alteração em `tools/`;
- nenhuma mudança em helpers/snippets/scripts;
- somente documentação, inventário e instrumentação de baseline.

Qualquer arquivo comportamental no diff bloqueia o fechamento da SE00 e exige remoção ou reclassificação explícita da sprint.

## Limitações conhecidas do ambiente Windows local

O gate local completo possui testes legados que podem falhar no Windows por razões já reproduzidas fora da SE00:

- criação de symlink sem privilégio (`WinError 1314`);
- mocks de V02 sensíveis a separador POSIX (`/`) quando `Path` produz `\\` no Windows.

Esses pontos não devem ser silenciosamente ignorados. Para esta baseline, a evidência complementar é o GitHub Actions do mesmo estado de produto, que passou antes da abertura da SE00. A correção de portabilidade deve ocorrer em frente técnica própria, não nesta sprint documental.

## Saída esperada

Os resultados consolidados entram em [`RESULTADOS.md`](RESULTADOS.md), e o estado de governança em [`CHECKPOINT.md`](CHECKPOINT.md).
