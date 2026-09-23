# Protocolo de certificação para MM02–MM13

**Data:** 2026-09-23  
**Origem:** lições operacionais da MM01 R1–R10.  
**Princípio:** rigor proporcional, SHA-bound, fail-closed e sem `retry-until-green`.

## 1. Objetivo

Separar diagnóstico barato de certificação cara. A FULL deve certificar uma candidata já congelada, não descobrir preconditions triviais.

Fluxo canônico:

```text
desenvolvimento
→ PRE_CERTIFICATION_SMOKE
→ CANDIDATE_FREEZE
→ FULL_CERTIFICATION
→ BUNDLE_LINT
→ AUDITORIA_INDEPENDENTE
→ CONTRADITORIO
→ DOC_CLOSE_MINIMO
→ FINAL_TREE_REVALIDATION
→ ACEITE_HUMANO
→ MERGE
```

Nenhuma etapa posterior reclassifica uma tentativa anterior.

## 2. Estados mínimos

Cada rodada registra explicitamente:

- repository;
- branch;
- candidate SHA/tree;
- `main` SHA;
- merge-base;
- ahead/behind;
- shallow;
- dirty/worktree;
- plataforma/runtime;
- comando/gate;
- exit/status;
- evidência/bundle;
- limitações.

Um PASS sem identidade Git suficiente não é certificação transferível.

## 3. `PRE_CERTIFICATION_SMOKE`

Executar antes de qualquer FULL.

### 3.1 Git

Confirmar:

- `fetch`/refs atuais;
- branch esperada;
- HEAD;
- `main`;
- merge-base;
- ahead/behind;
- clone não shallow;
- worktree;
- PRs concorrentes materiais.

Fail-closed se a candidata esperada não puder ser identificada.

### 3.2 Checkout e resíduos

Antes do gate:

- fast-forward-only da própria branch é permitido quando deliberado;
- merge/rebase espontâneo é proibido;
- resíduos ignorados conhecidos precisam estar ausentes ou classificados;
- não apagar evidência de falha para “limpar” a candidata.

### 3.3 Runtime

Probes baratos, conforme a sprint:

- Python e versão;
- Node;
- package manager;
- executables reais;
- PATH/shims Windows;
- encoding/UTF-8;
- dependências necessárias.

Não instalar/atualizar dependência modificando lockfile por conveniência durante certificação.

### 3.4 Certifier

Antes da candidata:

- self-tests;
- interruption;
- streaming;
- encoding;
- sanitização;
- output/evidence directory;
- guards de cleanup;
- pins de inputs/workflows, quando existirem.

O instrumento que produz a evidência deve ser testado antes de ser usado como autoridade.

### 3.5 Snapshot e documentação derivada

Executar validator rápido para:

- contadores derivados;
- links relativos;
- headings/fences quando aplicável;
- snapshot README;
- zero drift manual do derivado.

Snapshot stale reprova o smoke, não deve consumir uma FULL.

### 3.6 Workflow/gate drift

Se a sprint depende de workflows ou snippets de comando:

- conferir pins;
- conferir comandos;
- conferir snippets/allowlists;
- registrar qualquer mudança da `main`.

### 3.7 Infra compartilhada

Se a `main` mudou recentemente em:

- SEF;
- certifier;
- validator;
- workflow;
- testes transversais;
- inputs críticos;

executar smoke focal desses componentes antes da FULL.

## 4. `CANDIDATE_FREEZE`

O freeze existe quando:

- todos os smokes obrigatórios estão verdes;
- HEAD/tree estão identificados;
- `behind_by=0`;
- worktree está limpa;
- escopo da sprint está estável;
- não há mudança funcional planejada pendente.

Depois do freeze, evitar o ciclo:

```text
FAIL → markdown histórico → novo SHA → FULL → FAIL → markdown → novo SHA → FULL
```

Durante diagnóstico, preferir evidência externa, corpo da PR ou bundle. Se o histórico precisar ser versionado antes da certificação, agrupar os registros e congelar uma única nova candidata.

## 5. Concorrência com `main`

Antes da FULL final:

1. reconciliar a candidata com a `main`;
2. exigir `behind_by=0`;
3. identificar PRs concorrentes com potencial de tocar gates/inputs;
4. quando operacionalmente possível, usar uma janela curta sem integrar outra frente material durante FULL/auditoria.

Se `main` avançar:

### 5.1 Drift imaterial

Exemplo: documento isolado sem relação com inputs/gates. Registrar avaliação formal de materialidade. Não transportar automaticamente nem invalidar automaticamente a evidência.

### 5.2 Drift material

Exemplos:

- validator;
- workflow;
- policy;
- certifier;
- teste transversal executado;
- input crítico;
- contrato consumido pela sprint.

O PASS anterior permanece histórico; reconciliar e certificar a nova candidata.

## 6. Infraestrutura compartilhada

Quando uma sprint falhar em código que é simultaneamente:

- herdado da `main`;
- não modificado pela sprint;
- compartilhado por outras iniciativas;

classificar como:

`SHARED_INFRASTRUCTURE_FINDING`.

Tratamento:

- determinístico e bloqueante → manutenção separada;
- histórico/intermitente → preservar observação conforme protocolo da infraestrutura;
- integrar manutenção à `main`;
- reconciliar Micromodelos;
- recertificar somente quando material.

A branch de Micromodelos não vira branch de manutenção transversal.

## 7. `FULL_CERTIFICATION`

Pré-condição: smoke verde + candidata congelada.

A FULL é **uma execução single-shot** do SHA candidato.

Proibido:

- retry-until-green;
- patch durante a campanha;
- merge/rebase durante a campanha;
- omitir gate vermelho porque “já passou antes” em outro SHA;
- converter skip não autorizado em PASS.

Retry operacional, quando realmente necessário, é uma **nova rodada**, com justificativa e evidência da anterior preservada.

A composição da FULL é proporcional à sprint. Não copiar mecanicamente os 50 StepResults da MM01 quando a nova sprint tiver superfície menor; também não eliminar gates que protegem riscos reais da sprint.

## 8. `BUNDLE_LINT`

Antes de entregar à auditoria independente, conferir automaticamente:

- SHA externo/candidato;
- checksums internos;
- entries esperadas;
- duplicatas;
- traversal;
- hashes dos logs;
- UTF-8;
- U+FFFD;
- HOME/path local;
- REPO/path local;
- formas escapadas;
- credenciais/tokens;
- StepResults obrigatórios;
- skips autorizados;
- manifest coerente com bytes reais.

Manifest não é autoridade sobre si próprio. O lint precisa ler os bytes do bundle.

## 9. Auditoria independente

A auditoria:

- usa bytes reais do bundle;
- reconfirma GitHub vivo;
- usa a matriz/contrato congelado;
- não confia no manifest apenas por declaração;
- não expande threat model sem base em requisito aceito;
- distingue defeito funcional de limitação instrumental do auditor.

Se o auditor não consegue abrir um ZIP, resolver o acesso à evidência por complemento probatório; não reexecutar a sprint por reflexo.

## 10. Contraditório

O contraditório só trabalha sobre findings da auditoria:

- manter;
- refutar;
- reclassificar;
- ajustar framing.

Não é nova auditoria ilimitada e não cria requisito retrospectivo.

Finding confirmado que exige alteração funcional gera nova candidata e volta ao fluxo adequado. Finding probatório pode ser encerrado por evidência complementar sem inventar nova execução.

## 11. `DOC_CLOSE_MINIMO`

Depois de auditoria + contraditório, sincronizar apenas documentos deliberadamente postergados.

Provar o delta:

```text
certified SHA
→ final docs SHA
```

Classificar cada arquivo como:

- behavior-bearing;
- gate/input;
- documentação pura.

Se o delta tocar comportamento, gate ou input crítico, a certificação anterior pode ficar stale. Se for exclusivamente documental e não material aos gates, seguir para final-tree revalidation em vez de repetir automaticamente a FULL.

## 12. `FINAL_TREE_REVALIDATION`

Objetivo: provar que o fechamento documental não alterou o que foi certificado.

Mínimo:

- diff certificado → final;
- branch/main/merge-base/ahead/behind;
- merge-ref/tree quando aplicável;
- certifier self-test ou validator rápido proporcional;
- gates focais diretamente relacionados ao delta;
- snapshot/links;
- worktree/árvore limpa quando houver checkout local.

Resultado esperado deve declarar explicitamente algo equivalente a:

```text
DELTA_CERTIFIED_TO_FINAL = DOCUMENTATION_ONLY
FINAL_TREE_REVALIDATION = PASS
```

Uma FULL integral só é repetida se a materialidade do delta exigir.

## 13. Aceite e merge

Somente depois de:

- certificação aplicável;
- auditoria;
- contraditório;
- fechamento documental;
- final-tree revalidation;
- checkpoint final;

solicitar aceite humano explícito.

Aceite de uma sprint não autoriza automaticamente a seguinte. Merge não equivale a publicação Databricks, homologação corporativa ou promoção SEF.

## 14. Relação com SEF/PSEF/SER

Nas sprints que criam/consomem skills:

- reler `policy.json`;
- usar `current_level` real;
- reconsultar última PSEF integrada;
- reconsultar SER integrada;
- separar task correctness, agent adherence e canonical compliance;
- preservar entrypoints/Receipt/Postflight quando exigidos pelo nível vigente.

`target_level` não é evidência. Prompt não recebe policy própria.

## 15. Evidência por sprint

### MM02/MM03

Repo-side/sintético. A certificação deve priorizar contrato, testes metamórficos/metadata, determinismo, segurança e ausência de acesso real. Nenhum gate de prompt/skill deve ser inventado.

### MM04–MM06

Adicionar gates de SEF/PSEF e modelo de evidência conforme a revisão pós-SEF.

### MM08–MM10

Adicionar autoridade ambiental, behavior/canonical compliance e superfície de handoff/publicação.

### MM11–MM13

Reconsultar transversalmente estados integrados e maturidade observada; não transportar snapshots antigos.

## 16. Critério de eficiência

O protocolo é considerado bem aplicado quando uma FULL não descobre um problema que já era detectável por:

- Git preflight;
- runtime probe;
- certifier self-test;
- residue check;
- snapshot rápido;
- bundle lint preliminar;
- smoke focal de infraestrutura alterada.

Isso não garante uma única rodada funcional; garante que rodadas caras sejam reservadas para fatos que realmente exigem a campanha integral.
