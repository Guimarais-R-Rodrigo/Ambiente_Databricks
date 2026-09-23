# Retrospectiva operacional da MM01

**Data:** 2026-09-23  
**Objeto:** campanha de estabilização e certificação R1–R10 da MM01.  
**Regra:** resultados históricos não são reclassificados.

## 1. Objetivo

A MM01 pagou um custo elevado de descoberta de preconditions, portabilidade e infraestrutura compartilhada. Esta retrospectiva transforma esse custo em controles reutilizáveis para MM02–MM13 sem reduzir rigor.

A pergunta operacional não é “como evitar qualquer FAIL”, e sim:

> qual problema barato poderia ter sido detectado antes de uma FULL cara, e qual finding pertence à sprint versus à infraestrutura compartilhada?

## 2. Linha final preservada

```text
R1  = FAIL — portabilidade Windows npm/pnpm
R2  = FAIL — drift da main / precondition
R3  = FAIL — interrupção externa durante bootstrap
R4  = FAIL — CI_LOCAL / snapshot README stale
R5  = MECHANICAL_PASS / BUNDLE_NONCONFORMANT
R6  = MECHANICAL_FAIL / BUNDLE_SANITIZATION_PASS
R7  = MECHANICAL_FAIL / BUNDLE_SANITIZATION_PASS
R8  = MECHANICAL_FAIL / BUNDLE_SANITIZATION_PASS / UNICODE_STREAMING_PASS
R9  = PASS integral no baseline anterior, depois stale por drift material
R10 = PASS integral pós-reconciliação
```

R10 foi executada em `c43273fbb0cf40c1b9a3bc176cc1d4fd11d781a6` contra `main@515e673b17f21d4c912d9ae866a7e31967fd4488`: 50 StepResults, 49 PASS, `V12_SCOPE_STRICT=SKIP_ALLOWED`, CI local 10/10, V00–V13 executáveis PASS e snapshot `1682/2109/0`. O bundle possui SHA-256 `34f0ea4518eb8d2c8042871b40451e8c956710b95ccc097d9cc23ca2b14ad6ab`.

Depois vieram auditoria independente final, auditoria complementar probatória, contraditório, fechamento documental, nova reconciliação com a manutenção A07/PR #105, aceite humano e merge da PR #51. Esse fechamento posterior não reclassifica R1–R9.

## 3. Classificação das rodadas

| Rodada | Classe | Causa observada | Smoke barato antes da FULL? | Infra reutilizável? | Continua no certifier? | Deve virar preflight? | Owner principal | Política preventiva |
|---|---|---|---|---|---|---|---|---|
| R1 | portabilidade/runtime | resolução npm/pnpm incompatível com shims Windows | **sim** | sim: resolução explícita de executáveis | sim | **sim** | certifier compartilhado | probe de Python/Node/package manager/PATH antes de gates |
| R2 | drift/precondition | branch ficou behind da `main` | **sim** | regra Git, não código funcional | sim | **sim** | processo de certificação | fetch + merge-base + ahead/behind + fail-closed |
| R3 | observabilidade/interrupção | interrupção externa durante bootstrap sem encerramento probatório completo | parcial | sim: interrupção/streaming estruturados | **sim** | smoke do certifier | certifier compartilhado | self-test de interruption e emissão parcial antes da candidata |
| R4 | snapshot derivado stale | README tinha contadores antigos; CI detectou apenas durante campanha | **sim** | sim: snapshot/validator rápido | sim | **sim** | documentação/infra compartilhada | medir contadores e links antes do freeze |
| R5 | conformidade do bundle | gates mecânicos passaram, mas logs continham paths locais escapados | não depende de FULL funcional | **sim**: sanitização/bundle lint | **sim** | self-test pré-FULL | certifier compartilhado | bundle lint obrigatório antes de auditoria |
| R6 | resíduos ambientais | diretórios ignorados preexistentes bloquearam preflight | **sim** | regra de limpeza controlada | sim | **sim** | checkout operacional | inventário explícito de resíduos antes do freeze |
| R7 | encoding/console | bytes Windows → replacement → console charmap causou `UnicodeEncodeError` | **sim** | **sim**: UTF-8 determinístico + fallback de console | **sim** | self-test de encoding | certifier compartilhado | probe UTF-8/streaming em console host antes de gates |
| R8 | infraestrutura transversal compartilhada | WinError32 em teste SEF herdado, blob idêntico à `main` | **sim, focal** quando main/infra mudou | sim, mas fora da MM01 | sim como gate transversal | smoke de infra quando material | manutenção SEF/certifier | classificar `SHARED_INFRASTRUCTURE_FINDING`; não corrigir na sprint consumidora |
| R9 | PASS + drift posterior | candidata passou; depois a `main` mudou testes/infra materiais | não é defeito da FULL | regra de concorrência | sim | **sim, antes do freeze final** | coordenação Git | PASS fica histórico; drift material exige reconciliação + nova candidata |
| R10 | certificação final pós-reconciliação | candidata reconciliada executou campanha integral verde | n/a | consolidou o protocolo | referência histórica | freeze já satisfeito | sprint MM01 | uma FULL single-shot após smoke verde e freeze estável |

## 4. Lições por classe

### 4.1 Preconditions baratas não pertencem ao fim da FULL

Git, runtime, PATH/shims, resíduos, snapshot e self-tests do certifier devem falhar antes da campanha integral.

A FULL continua fail-closed, mas deixa de ser a ferramenta primária para descobrir:

- branch behind;
- pacote ausente;
- executable não resolvido;
- lixo ignorado;
- snapshot stale;
- problema básico de encoding do próprio instrumento.

### 4.2 Instrumentação é parte do objeto probatório

R3, R5 e R7 mostraram que resultado analítico verde não basta se a evidência não puder ser:

- concluída após interrupção;
- transmitida sem corrupção;
- serializada em UTF-8;
- sanitizada;
- verificada por hashes.

Esses controles permanecem no certifier; não são “higiene opcional”.

### 4.3 Infra compartilhada não vira scope creep da sprint

R8 não foi causada por código MM01. A resposta correta foi preservar o FAIL, classificar o finding como transversal, tratar a manutenção separadamente e reconciliar depois.

Regra permanente:

```text
falha em código herdado da main
+ não modificado pela sprint
+ compartilhado por outras iniciativas
= SHARED_INFRASTRUCTURE_FINDING
```

Não corrigir automaticamente dentro da branch de Micromodelos.

### 4.4 PASS pertence a um SHA e a uma baseline

R9 continua PASS do seu baseline. O avanço material da `main` não “apaga” o PASS; ele torna a evidência insuficiente para uma candidata nova.

Logo:

- preservar bundle e SHA;
- classificar drift;
- reconciliar;
- recertificar somente quando o drift for material para inputs/gates.

### 4.5 Histórico documental dentro do freeze pode criar loop artificial

Registrar cada FAIL em Markdown dentro da própria branch, depois gerar novo SHA e repetir a FULL, pode produzir ciclo sem mudança funcional.

Para próximas sprints:

1. preservar tentativa externamente durante diagnóstico;
2. agrupar registros versionados antes do freeze final;
3. executar uma FULL sobre o SHA realmente candidato;
4. depois da auditoria, aceitar somente fechamento documental mínimo e revalidar a árvore proporcionalmente.

## 5. Anti-patterns a não repetir

- usar FULL para descobrir `behind_by>0`;
- `retry-until-green`;
- transportar PASS entre SHAs;
- corrigir infraestrutura compartilhada dentro da branch funcional por conveniência;
- chamar bundle “válido” porque o manifest diz que é;
- confiar em console/encoding do host sem self-test;
- transformar toda tentativa diagnóstica em commit antes do freeze;
- executar nova FULL integral depois de um delta puramente documental que não toca inputs/gates;
- tratar ausência de reprodução de WinError32 como prova de root cause corrigida;
- usar `target_level` como se fosse enforcement atual.

## 6. Infraestrutura reutilizável que deve permanecer

A campanha MM01 deixou controles que agora devem ser considerados patrimônio transversal:

- resolução Windows de comandos/package manager;
- self-tests do certifier;
- interrupção estruturada;
- streaming de stdout/stderr;
- UTF-8 determinístico;
- fallback seguro de console;
- sanitização de bundles;
- checksums internos e hashes de logs;
- guards contra resíduos;
- snapshot rápido;
- classificação de drift da `main`;
- separação entre finding da sprint e infraestrutura compartilhada.

Esses controles não justificam copiar o certifier MM01 inteiro para cada sprint. O protocolo futuro compõe apenas os gates proporcionais ao objeto da sprint.

## 7. Resultado operacional

A política para MM02–MM13 passa a ser:

```text
desenvolvimento
→ smoke barato
→ candidate freeze
→ uma FULL da candidata congelada
→ bundle lint
→ auditoria independente
→ contraditório
→ fechamento documental mínimo
→ final-tree revalidation
→ aceite
→ merge
```

O ganho esperado é reduzir rodadas caras sem reduzir evidência, fail-closed ou independência da auditoria.
