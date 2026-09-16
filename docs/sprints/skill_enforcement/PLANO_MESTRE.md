# Plano Mestre — Skill Enforcement Framework (SEF)

**Data:** 2026-09-15  
**Status:** SE00 concluída e integrada; SE01 homologada, integração pendente; SE02–SE08 não iniciadas  
**Frente:** Skill Enforcement Framework (SEF)  
**Branch deste plano:** `sef/00-plano-mestre`  
**Baseline de criação:** `main@d106ef3158e5827a2eec3aa183dbb3b47885c960`  
**Laboratório de homologação primário:** Databricks pessoal / Free  
**Destino corporativo:** somente após homologação explícita no laboratório pessoal

---

## 1. Propósito desta frente

Esta frente existe para resolver uma lacuna específica do Hub: uma Agent Skill pode ser selecionada corretamente, conhecer os helpers e templates pertinentes e ainda assim gerar código próprio, ignorando `hub_snippets`, `hub_scripts`, templates e outros recursos prescritos pelo contrato da skill.

O objetivo do SEF não é tornar a resposta de um LLM matematicamente determinística. O objetivo é retirar do espaço probabilístico as decisões que já são conhecidas e estáveis e criar evidência verificável de aderência. Em particular, uma execução que não satisfaça os requisitos obrigatórios da skill não deve poder ser classificada como uma execução válida ou concluída daquela skill.

O piloto é `hub-ml-eda-profissional`, porque já existe uma falha real observada: o output foi produzido com aparência plausível, porém os helpers declarados pela skill não foram utilizados e parte da lógica foi reimplementada do zero.

---

## 2. Estado de partida e decisões que não devem ser desfeitas

O SEF deve evoluir a arquitetura vigente, não substituí-la.

A fonte canônica do produto continua sendo `ambiente_fonte/`. O espelho `Novo_Ambiente_Simulado/` continua sendo derivado por `tools/render_simulado.py --write` e nunca deve ser editado manualmente.

As skills continuam em `.assistant/skills/<nome>/SKILL.md`, com frontmatter conservador contendo somente `name` e `description`. O SEF não deve introduzir metadados experimentais no frontmatter sem decisão arquitetural separada.

Os helpers continuam em `hub_snippets` e `hub_scripts`. A lógica já existente não deve ser copiada para dentro das skills. Scripts de skill, quando necessários, serão orquestradores finos sobre APIs públicas existentes.

A publicação no Databricks Free continua sendo feita por `tools/publicar_free.py`. Não substituir esse fluxo por `databricks workspace import-dir` manual como procedimento principal: o publicador já contém guardrails para preservar módulos `.py` como arquivos, reenviar somente notebooks didáticos como `SOURCE`, validar o host/usuário e verificar a árvore remota.

A replicação para o workspace do trabalho continua separada da publicação no Free. `tools/publicar_free.py` possui proteção contra usuário de aparência corporativa e não deve ser contornado.

Os forward tests atuais continuam medindo roteamento de skills. O SEF criará uma segunda classe de teste, voltada para aderência de execução. Não renomear os testes antigos para fingir que eles cobrem algo que hoje não cobrem.

---

## 3. Escopo

### 3.1 Dentro do escopo

- reforçar a aderência de uma skill aos helpers, scripts, templates e gates declarados;
- diferenciar recursos obrigatórios, condicionais e opcionais;
- adicionar preflight antes da execução de lógica protegida;
- mover lógica repetível para runners determinísticos quando isso reduzir reinvenção;
- produzir evidência estruturada de quais recursos foram efetivamente utilizados;
- executar postflight e impedir conclusão homologada quando requisitos obrigatórios não tiverem sido satisfeitos;
- medir aderência por testes repetidos no Genie Code;
- integrar os novos contratos aos validadores, CI, renderer, publicação e auditoria do Hub;
- homologar primeiro no Databricks pessoal/Free;
- só depois preparar promoção controlada para o workspace de trabalho.

### 3.2 Fora do escopo inicial

- tornar todas as 14 skills igualmente rígidas desde o primeiro sprint;
- criar um novo catálogo duplicado de helpers;
- alterar cálculos internos dos helpers sem defeito comprovado;
- transformar toda interação simples com Genie Code em pipeline formal;
- publicar skills de workspace no ambiente corporativo sem governança administrativa;
- alterar permissões, ACLs, políticas do workspace ou controles corporativos;
- usar dados reais do trabalho para desenvolver ou validar o framework no Databricks pessoal;
- persistir dados, receipts ou outputs sem necessidade e sem autorização pertinente.

---

## 4. Princípios arquiteturais

### P1 — Fail closed para requisito obrigatório

Quando um recurso obrigatório estiver ausente, incompatível ou não verificável, a execução canônica deve ficar `BLOCKED` ou `FAIL`. O agente não deve substituir silenciosamente o recurso por implementação própria.

### P2 — LLM interpreta; código determinístico executa o que já é conhecido

O LLM deve permanecer responsável por contexto, hipóteses, interpretação, priorização e comunicação. Rotinas repetíveis, interfaces estáveis, checks e composição de helpers devem migrar progressivamente para código determinístico quando isso reduzir erro sem prejudicar flexibilidade.

### P3 — Evidência vale mais que declaração textual

Aderência precisa ser provada por evidência observável e reproduzível. A simples presença de texto em `SKILL.md` não comprova resolução, import, chamada ou conclusão de um helper.

### P4 — Fonte canônica única

Contratos, schemas, scripts e documentação técnica vivem no repositório. O ambiente simulado é derivado; o workspace Free é laboratório de homologação; o workspace corporativo é destino posterior e governado.

### P5 — Evolução por camadas

A frente evolui de contrato declarativo para preflight, runner, receipts, postflight e enforcement somente após cada camada demonstrar valor e permanecer compatível com a plataforma.

---

## 5. Arquitetura alvo

A arquitetura planejada é progressiva:

1. **L1 — Contract**: contrato machine-readable por skill;
2. **L2 — Preflight**: validação pré-execução e estado `PASS/BLOCKED`;
3. **L3 — Deterministic Runner**: execução de lógica repetível via APIs públicas canônicas;
4. **L4 — Execution Receipt**: evidência estruturada de recursos realmente usados;
5. **L5 — Postflight**: validação pós-execução e bloqueio de conclusão inválida;
6. **L6 — Enforcement Mode**: `WARN`/`ENFORCE` somente após homologação suficiente.

Cada camada deve ser implementada em sprint própria. Nenhuma sprint deve antecipar a arquitetura definitiva da seguinte sem necessidade comprovada.

---

## 6. Sequência de sprints

### SE00 — baseline observável

Objetivo: medir o comportamento pré-enforcement e construir o inventário real de recursos declarados versus utilizados.

Estado: concluída, homologada e integrada.

### SE01 — contrato verificável + capability experiment

Objetivo: introduzir L1 (`Contract`) em `mode="audit"`, validar estaticamente o contrato piloto e verificar no Databricks Free se scripts relativos de Agent Skills podem resolver/importar APIs públicas do Hub.

Estado: homologada em 2026-09-16; integração da PR #69 pendente.

### SE02 — preflight auditável

Objetivo: desenhar e implementar L2 sem ainda introduzir runner determinístico.

Estado: não iniciada.

### SE03 — deterministic runner piloto

Objetivo: implementar L3 para o fluxo EDA protegido, reduzindo reinvenção de lógica repetível.

Estado: não iniciada.

### SE04 — execution receipts

Objetivo: registrar evidência estruturada de resolução/chamada/conclusão dos recursos do contrato.

Estado: não iniciada.

### SE05 — postflight e fail-closed

Objetivo: impedir conclusão homologada quando requisitos obrigatórios não forem satisfeitos.

Estado: não iniciada.

### SE06 — modos WARN/ENFORCE

Objetivo: separar observação, advertência e bloqueio efetivo por política explícita.

Estado: não iniciada.

### SE07 — expansão para outras skills

Objetivo: avaliar valor marginal e generalizar o framework apenas para skills em que o custo de enforcement seja justificado.

Estado: não iniciada.

### SE08 — promoção corporativa controlada

Objetivo: preparar handoff, governança e promoção para o workspace de trabalho após homologação completa no Free.

Estado: não iniciada.

---

## 7. Critério de avanço

Uma sprint só pode ser encerrada quando:

- artefatos canônicos estiverem versionados;
- testes positivos e negativos relevantes estiverem verdes;
- `validate_assistant.py --conferir-readme` estiver verde;
- renderer canônico não deixar diff não esperado;
- CI aplicável estiver factual e observavelmente classificado;
- evidências do Databricks Free estiverem registradas quando a sprint depender delas;
- documentação/CHANGELOG estiverem reconciliados;
- houver aceite humano explícito quando exigido.

O início da sprint seguinte exige autorização separada. Homologação da sprint anterior não autoriza automaticamente a seguinte.

---

## 8. Guardrails permanentes

- nenhuma edição manual de `Novo_Ambiente_Simulado/` como fonte de verdade;
- nenhuma mutação no workspace corporativo por esta frente sem gate próprio;
- nenhuma promoção de `NOT_OBSERVABLE` para `PASS`;
- nenhum failure de infraestrutura deve ser chamado de failure funcional sem evidência;
- nenhum `PASS` de capability experiment deve ser reinterpretado como enforcement;
- nenhum dado corporativo deve ser usado no laboratório pessoal;
- nenhum bypass silencioso de requisito obrigatório é aceitável em modos futuros de enforcement.

---

## 9. Resultado esperado da frente

Ao final do programa SEF, a seleção correta de uma skill deve ser apenas o primeiro passo. A execução deve produzir evidência verificável de aderência aos recursos prescritos e impedir que uma resposta plausível, porém construída fora do contrato obrigatório, seja classificada como execução válida daquela skill.

Esse objetivo será perseguido incrementalmente, sem assumir que a plataforma fornece determinismo que ainda não foi demonstrado e sem confundir orientação textual com enforcement real.