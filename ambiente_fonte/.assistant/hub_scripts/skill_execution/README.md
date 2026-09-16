# `skill_execution` — preflight verificável antes da lógica protegida

<!-- readme-objeto: 1.0.0 -->

`hub_scripts.skill_execution` é a camada determinística do Skill Enforcement Framework usada para resolver o contrato de execução antes do core analítico. Na SE02, sua API pública é `run_preflight`; ela não executa a EDA, não chama os helpers declarados e não escreve no workspace.

## Visão rápida

| Item | Resumo |
|---|---|
| O que é | preflight L2 para `execution_contract.json` |
| Serve para | decidir `PASS` ou `BLOCKED` antes da lógica protegida |
| Usa | filesystem local da `.assistant`, JSON e AST da biblioteca padrão |
| Não faz | runner, receipt, postflight, análise Spark ou publicação |
| Entrada principal | contrato, raiz `.assistant` e contexto objetivo de condições |
| Saída | `PreflightResult` estruturado e determinístico |

Exemplo: [exemplo_skill_execution.py](exemplo_skill_execution.py). Implementação: [preflight.py](preflight.py).

## 1. O que é?

É um resolvedor estático de pré-condições. Ele lê o contrato v0.1 da skill, classifica recursos `required`, `conditional` e `optional`, confere APIs públicas/templates aplicáveis e produz um estado estruturado. A SE02 continua em `mode="audit"`; ter preflight não equivale a enforcement completo.

## 2. Que problema este recurso resolve?

Antes da SE02, a skill podia declarar helpers e templates sem um gate reproduzível que dissesse se os requisitos aplicáveis estavam disponíveis. O preflight transforma essa verificação em uma decisão observável antes do core analítico.

## 3. Quando faz sentido usar?

Use antes de uma execução protegida por `execution_contract.json`, especialmente quando requisitos obrigatórios ou condicionais precisam ser resolvidos antes de o agente escrever ou executar lógica analítica. O piloto é `hub-ml-eda-profissional`.

## 4. Quando não usar?

Não use como runner da EDA, para interpretar resultados, para validar qualidade dos dados ou como prova de que um helper foi de fato chamado. Um `PASS` indica que o plano prévio é resolvível; não prova aderência durante ou após a execução.

## 5. Como funciona, intuitivamente?

O preflight lê o contrato, avalia condições explícitas do contexto, resolve somente os itens aplicáveis e bloqueia quando um requisito obrigatório não pode ser comprovado. A resolução de helpers é estática: o `__init__.py` da pasta de objeto é analisado por AST, sem importar a biblioteca inteira.

## 6. Exemplo de situação

Uma EDA pede visualizações e possui quatro colunas numéricas. O contexto informa `visual_diagnostics_requested=true` e `numeric_columns=4`; correlação, distribuições e templates visuais tornam-se aplicáveis. Se a fachada pública de um helper requerido estiver ausente, o resultado é `BLOCKED` antes da análise.

## 7. O que você precisa antes de usar?

É necessário um contrato v0.1 válido, uma raiz `.assistant` acessível, a pasta da skill correspondente e valores explícitos para as condições referenciadas. Na EDA piloto, o contexto usa booleanos objetivos e `numeric_columns` inteiro não negativo. O preflight não descobre esses fatos executando a análise.

## 8. O que este recurso entrega?

`PreflightResult` contém `status`, skill, versão, modo, decisões de recursos/templates, issues bloqueantes, contexto de condições e `writes_performed=false`. `PASS` significa que não houve issue bloqueante; `BLOCKED` significa que a execução canônica não deve prosseguir silenciosamente.

## 9. Como usar este recurso no Hub?

Importe pela fachada pública:

```python
from hub_scripts.skill_execution import run_preflight
```

Passe `contract_path`, `assistant_root` e um contexto explícito. O notebook de exemplo demonstra o uso sem executar Spark nem escrever no workspace.

## 10. Decisões e configurações que mais importam

A política do item define o bloqueio: `required` sempre é aplicável; `conditional` depende do contexto objetivo; `optional` pode ser inspecionado sem bloquear. Condição sem contexto suficiente resulta em `BLOCKED`, evitando que ausência de evidência seja tratada como `false` silenciosamente.

## 11. Limitações, riscos e armadilhas

A SE02 não impede um agente de ignorar o script; esse comportamento só pode ser medido no Genie Code real. O preflight também não prova chamada de helper, não produz Execution Receipt e não detecta bypass posterior. Paths e disponibilidade refletem o pacote presente no momento da execução.

## 12. Quais são as alternativas?

`tools/skill_enforcement/validate_contracts.py` valida contratos no repositório e é um gate de desenvolvimento, não um componente publicado do Hub. A SE03 poderá introduzir runner determinístico, mas ele tem responsabilidade diferente e não deve ser antecipado aqui.

## 13. Como saber se o resultado faz sentido?

Teste happy path, recurso obrigatório removido, condição verdadeira/falsa, template ausente e contexto incompleto. Rode o mesmo input duas vezes e confira saída idêntica. Em `BLOCKED`, a issue deve identificar o item e a razão sem executar análise nem produzir escrita.

## 14. Arquivos relacionados e próximos passos

- [preflight.py](preflight.py): implementação L2.
- [__init__.py](__init__.py): fachada pública.
- [exemplo_skill_execution.py](exemplo_skill_execution.py): demonstração read-only.
- `skills/hub-ml-eda-profissional/execution_contract.json`: contrato piloto.
- `skills/hub-ml-eda-profissional/scripts/preflight.py`: acionador fino da skill.

SE03 é o próximo estágio arquitetural, mas não faz parte deste objeto nesta sprint.

## 15. Referências

- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`.
- `docs/sprints/skill_enforcement/PLANO_MESTRE.md` — SE02.
- implementação local e testes `tools/tests/test_skill_enforcement_se02.py`.
- Databricks Genie Code Agent Skills, verificada em 16/09/2026: scripts executáveis e recursos relativos à raiz da skill são superfícies suportadas.

Estado desta revisão: documentação e implementação SE02 em validação; homologação de runtime no Databricks Free é gate separado.
