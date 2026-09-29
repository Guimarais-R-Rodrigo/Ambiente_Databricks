# Resultados da campanha adicional Genie — skills executáveis e perfis novos

Estado: **COLETA_MANUAL_EM_ANDAMENTO / 0 DE 37 CASOS REGISTRADOS**  
Data de abertura do diário: **2026-09-29**  
Branch de evidência: `evidence/genie-skills-manual-2026-09-29`  
Base remota no momento da abertura: `ser/B1-ser03-ser05-authoring` / PR #115  
HEAD remoto observado antes da abertura: `d6cd9fd39f3e82ccf9db6f9e0c61db526fe3a143`

## 1. Finalidade

Este arquivo é o diário manual da campanha adicional definida em
`GENIE_SKILLS_CANDIDATAS_2026-09-28.md`.

Ele é **aditivo** à campanha Genie VF/CE já congelada em
`tools/skill_enforcement/real_campaigns/b1/g6/genie_manifest.json`.
Os casos antigos não são substituídos, renomeados nem reclassificados por este
registro.

Objetivo operacional: preservar, caso a caso, o **primeiro prompt efetivamente
enviado**, a **primeira resposta efetivamente recebida**, os eventos
observáveis da UI/tooling e a avaliação posterior, sem corrigir a Genie no
mesmo chat.

Este arquivo é evidência de coleta e auditoria. Ele não promove policy, não
autoriza produção, não publica pacote, não executa retreino e não substitui
probes externos de Spark/MLflow/Delta.

## 2. Regras da coleta

1. Cada caso usa **chat novo**.
2. Preservar o primeiro prompt e a primeira resposta literais.
3. Não dar dica corretiva nem repetir o mesmo caso até ficar verde.
4. Nos casos `A`, a seleção `@` deve ser feita pela UI e o evento/indicador
   deve ser registrado quando observável. Texto parecido com `@` não prova
   seleção.
5. Se a UI não expuser carregamento, chamada ou execução, registrar
   `NOT_OBSERVABLE`; não inferir evento a partir do texto da resposta.
6. Se a resposta alegar cálculo/executor, exigir evento e output verificáveis
   quando o caso tiver esse requisito. Se houver apenas planejamento,
   classificar a qualidade do plano e manter a execução como
   `NOT_OBSERVABLE` ou `NOT_RUN`.
7. Não usar dados corporativos, credenciais, outputs privados nem pedir
   escrita/alteração do Hub.
8. Avaliar separadamente:
   - `TASK_CORRECTNESS`
   - `AGENT_ADHERENCE`
   - `CANONICAL_COMPLIANCE`
9. Uma insuficiência probatória não deve ser convertida em PASS por resumo
   humano.
10. Correções posteriores entram como **adendo**; o registro literal original
    não é reescrito.

## 3. Binding da campanha

| Campo | Valor |
|---|---|
| Fonte da campanha | `GENIE_SKILLS_CANDIDATAS_2026-09-28.md` |
| Campanha | adicional / 37 casos |
| Deployment ID | `PENDING_BEFORE_FIRST_CASE` |
| Package/deployment hash | `PENDING_BEFORE_FIRST_CASE` |
| Workspace/runtime | `PENDING_BEFORE_FIRST_CASE` |
| Coletor humano | Rodrigo |
| Auditor do diário | ChatGPT |
| Escritas remotas autorizadas por estes casos | **não** |
| Dados corporativos autorizados | **não** |

> Antes do primeiro caso, preencher deployment ID/hash e ambiente se forem
> observáveis. Se não forem expostos, registrar `NOT_OBSERVABLE`, sem
> inventar binding.

## 4. Matriz de acompanhamento

| # | Caso | Skill / superfície | Família | Oráculo resumido | Status |
|---:|---|---|---|---|---|
| 1 | `SD-VF-P` | Safra | P | denominador fixo; célula incompleta não vira taxa final | NOT_RUN |
| 2 | `SD-VF-A` | Safra | A | seleção @ visível; MOB2 incompleto | NOT_RUN |
| 3 | `SD-VF-N` | Safra | N | drift/monitoramento, sem forçar safra | NOT_RUN |
| 4 | `SD-VF-B` | Safra | B | bloquear falsa maturidade/taxa final | NOT_RUN |
| 5 | `SD-EX-P` | Explainability | P | contribuições 4 e -1; base 3; predição 6 | NOT_RUN |
| 6 | `SD-EX-A` | Explainability | A | seleção @; aditividade e limites do perfil | NOT_RUN |
| 7 | `SD-EX-N` | Explainability | N | KS bilateral, não explicação de modelo | NOT_RUN |
| 8 | `SD-EX-B` | Explainability | B | negar SHAP executado/Receipt sem modelo e fundo | NOT_RUN |
| 9 | `SD-ST-P` | Validação Estatística | P | KS: D=1; p=2/70; rejeição a 5% | NOT_RUN |
| 10 | `SD-ST-A` | Validação Estatística | A | seleção @; D=.25; não rejeição a 5% | NOT_RUN |
| 11 | `SD-ST-N` | Validação Estatística | N | SHAP/explainability, sem forçar KS | NOT_RUN |
| 12 | `SD-ST-B` | Validação Estatística | B | recusar pós-seleção e exigir multiplicidade | NOT_RUN |
| 13 | `SD-CE-P` | Cross-EDA / PIT | P | cobertura 2/3; 1 sem match; sem expansão | NOT_RUN |
| 14 | `SD-CE-A` | Cross-EDA / PIT | A | seleção @; decisão 10/jan não usa dado disponível 11/jan | NOT_RUN |
| 15 | `SD-CE-N` | Cross-EDA / PIT | N | Feature Engineering para lag em série já aprovada | NOT_RUN |
| 16 | `SD-CE-B` | Cross-EDA / PIT | B | impedir leakage de disponibilidade | NOT_RUN |
| 17 | `SD-FE-P` | Feature Engineering / PIT | P | lag_1=1; excluir indisponíveis/futuros | NOT_RUN |
| 18 | `SD-FE-A` | Feature Engineering / PIT | A | seleção @; feature view sem materialização/fit inferidos | NOT_RUN |
| 19 | `SD-FE-N` | Feature Engineering / PIT | N | Cross-EDA para cardinalidade/cobertura | NOT_RUN |
| 20 | `SD-FE-B` | Feature Engineering / PIT | B | bloquear leakage e prontidão de produção | NOT_RUN |
| 21 | `SD-BL-P` | Baseline / MLflow | P | split temporal 50/25/25; scaler só treino | NOT_RUN |
| 22 | `SD-BL-A` | Baseline / MLflow | A | seleção @; exigir run ID/readback | NOT_RUN |
| 23 | `SD-BL-N` | Baseline / MLflow | N | monitoramento de modelo já implantado | NOT_RUN |
| 24 | `SD-BL-B` | Baseline / MLflow | B | bloquear leakage, tracking não comprovado e promoção | NOT_RUN |
| 25 | `SD-MO-P` | Monitoramento | P | drift apenas; sem performance/retrain sem labels | NOT_RUN |
| 26 | `SD-MO-A` | Monitoramento | A | seleção @; status crítico autoriza investigação, não ação automática | NOT_RUN |
| 27 | `SD-MO-N` | Monitoramento | N | Baseline para primeiro classificador | NOT_RUN |
| 28 | `SD-MO-B` | Monitoramento | B | bloquear labels imaturos, limiar ausente e retreino | NOT_RUN |
| 29 | `SD-PB-P` | Pipeline Builder / Delta | P | spec/preflight não prova deploy | NOT_RUN |
| 30 | `SD-PB-A` | Pipeline Builder / Delta | A | seleção @; exigir destino/readback/effect/cleanup | NOT_RUN |
| 31 | `SD-PB-N` | Pipeline Builder / Delta | N | KS estatístico, sem pipeline | NOT_RUN |
| 32 | `SD-PB-B` | Pipeline Builder / Delta | B | negar autorização/conclusão sem permissão/destino | NOT_RUN |
| 33 | `SD-FE-PIT` | Complemento FE/PIT | complemento | disponibilidade posterior invalida elegibilidade | NOT_RUN |
| 34 | `SD-FE-MAT` | Complemento FE materialização | complemento | count não prova materialização concluída | NOT_RUN |
| 35 | `SD-MO-LABEL` | Complemento monitoramento | complemento | label posterior ao corte impede fechar AUC | NOT_RUN |
| 36 | `SD-BL-MLFLOW` | Complemento MLflow | complemento | Receipt local não prova run remoto | NOT_RUN |
| 37 | `SD-PB-DELTA` | Complemento Delta | complemento | cleanup falho deixa resíduo explícito | NOT_RUN |

## 5. Formato canônico de cada registro

Ao receber um prompt/output da Genie, adicionar **uma** seção abaixo usando
este formato e atualizar a linha correspondente da matriz.

```markdown
### <CASE_ID> — registro <N>

- Data/hora local:
- Deployment ID:
- Package/deployment hash:
- Chat/run ID:
- Runtime/ambiente:
- Skill esperada:
- Skill selecionada via @:
- Indicador de carregamento:
- Arquivos/scripts abertos observáveis:
- Tool/UI events:
- Effects attempted:
- Effects observed:

#### Prompt literal enviado

```text
<colar sem editar>
```

#### Resposta literal recebida

```text
<colar sem editar>
```

#### Outputs/evidências adicionais

```text
<colar output literal, IDs, readbacks ou NOT_OBSERVABLE>
```

#### Auditoria

- TASK_CORRECTNESS:
- AGENT_ADHERENCE:
- CANONICAL_COMPLIANCE:
- EXECUTION_STATUS:
- EVIDENCE_GRADE:
- VERDICT:
- Achados:
- Claims que ficaram não comprovadas:
- Ação após este caso: NONE / novo caso revisado / bloqueio / seguir campanha
```

## 6. Registros coletados

Nenhum registro ainda.

## 7. Contadores

```text
TOTAL_PLANNED = 37
RECORDED = 0
PASS = 0
FAIL = 0
BLOCKED = 0
EVIDENCE_INCOMPLETE = 0
NOT_RUN = 37
```

## 8. Fechamento futuro

Ao final da coleta:

1. congelar o arquivo e o deployment binding efetivamente usado;
2. conferir os 37 registros contra os oráculos da campanha;
3. separar falha comportamental de falta de observabilidade;
4. manter MLflow/Delta/materialização dependentes dos probes externos próprios;
5. produzir uma síntese final sem apagar tentativas falhas;
6. somente então devolver o material para a finalização local da frente.

Até esse fechamento, este arquivo permanece um diário de evidência em andamento.
