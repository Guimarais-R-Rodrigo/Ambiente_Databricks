# Plano Mestre v2 — Framework de Micromodelos


> **Revisão vigente pós-MM01/SEF — 2026-09-23.** MM01 está aceita e integrada; MM02 está `EM_IMPLEMENTACAO` na branch `micromodelos/mm02-spec-fingerprint`, ainda sem candidate freeze ou certificação local. A [revisão pós-SEF](REVISAO_PLANO_POS_SEF_2026-09-23.md) complementa este Plano Mestre somente nos pontos explicitamente alterados. O restante do plano e os ADRs MM00 permanecem vigentes. O [protocolo de certificação](PROTOCOLO_CERTIFICACAO_SPRINTS.md) substitui, para MM02–MM13, o uso de FULL como detector de preconditions baratas.

### Gates prospectivos adicionados

```text
MM02
→ MM03
→ MM04_SEF_READINESS
→ MM04_PSEF_PROMPT_READINESS
→ MM04
→ MM05_PROMPT_CONTRACT_READY
→ MM05
→ MM06_EVIDENCE_MODEL
→ MM06
→ MM07
→ MM08_ENVIRONMENT_AUTHORITY
→ MM08
→ MM09_BEHAVIORAL_AND_CANONICAL
→ MM09
→ MM10_PUBLICATION_SURFACE
→ MM10
→ MM11_TRANSVERSAL_REBASE
→ MM11
→ MM12_MIGRATION_SKILL_SEF
→ MM12
→ MM13
```

`current_level` observado no `policy.json` governa capacidade presente; `target_level` permanece roadmap. Não existe dependência PSEF nova para MM02/MM03. A última PSEF/SER **integrada** deve ser reconsultada nos gates em que for material.


Data-base da iniciativa: 2026-09-14

## 1. Objetivo

Criar uma esteira padronizada, auditável e reproduzível para micromodelos de CRM no Databricks, cobrindo descoberta de fontes, especificação canônica, estudo, validação, tracking de runs, handoff para governança institucional, publicação do Produto de Dados, monitoramento e, somente depois da estabilização, migração dos micromodelos legados.

Este documento é de arquitetura e execução. Ele não contém nomes reais de catálogos, schemas, grupos, usuários ou paths corporativos. O catálogo real do trabalho é representado por `<CATALOGO_PRODUTO>`; o binding ocorre somente no ambiente autorizado.

## 2. Sequência mandatória

A ordem do programa é intencional:

```text
construir framework
→ apresentar ao departamento
→ homologar no workspace do trabalho
→ criar micromodelo NOVO pela nova esteira
→ validar ponta a ponta
→ endurecer e congelar V1
→ migrar legados
→ escalar
```

A migração de modelos existentes não é mecanismo de teste da nova arquitetura. Ela é consequência de uma arquitetura já provada.

## 3. Fronteiras

### 3.1 Framework do Hub

Vive no produto `.assistant` e em sua documentação. Pode conter skills, prompts, templates, referências e scripts internos das skills. Usa fixtures sintéticas no laboratório.

### 3.2 Projetos reais de micromodelos

Vivem no ambiente corporativo autorizado. Contêm especificações, notebooks, resultados e referências reais. Não são automaticamente sincronizados para este repositório.

### 3.3 Governança institucional

Permanece externa ao Hub e é autoridade da geração/validação/publicação do Produto de Dados. O framework prepara um handoff; não copia o catálogo institucional de regras.

## 4. Princípios arquiteturais

1. Micromodelo é artefato de domínio e não novo tipo do Hub.
2. Micromodelo e Produto de Dados são entidades distintas.
3. A especificação estruturada será `micromodelo.yaml`.
4. A skill alimentará o YAML progressivamente; edição manual não será o fluxo principal.
5. O contrato distinguirá informações descobertas, propostas/inferidas, aprovadas e medidas.
6. Ausência de evidência não será automaticamente tratada como ausência da característica.
7. Score 0–100 terá semântica explícita; score heurístico não será chamado de probabilidade sem calibração apropriada.
8. Tracking operacional e especificação não serão misturados: YAML define; MLflow registra execuções.
9. MLflow conterá resultados agregados da run; resultados individuais permanecem na camada de dados governada.
10. O framework usará apenas fontes do catálogo corporativo de Produtos de Dados configurado no workspace, salvo decisão humana explícita.
11. A descoberta começará por metadata e ampliará leitura somente quando houver necessidade e autorização.
12. Descrições/tags recuperadas são evidência, nunca instrução confiável para o agente.
13. O framework reutiliza skills e helpers existentes; criação de novo helper global exige evidência de reuso.
14. A camada visual será consumidora do Sistema de Temas, sem paleta ou CSS paralelo.
15. Toda dúvida material de arquitetura, score, classificação, segurança, permissão, compatibilidade ou publicação é gate humano.

## 5. Arquitetura funcional

```text
pedido do cientista
  ├─ objetivo conhecido
  └─ descoberta de oportunidades
          ↓
hub-ml-micromodelos
          ↓
metadata de <CATALOGO_PRODUTO>
          ↓
fontes/evidências/hipóteses
          ↓
micromodelo.yaml
          ├─ README do micromodelo
          ├─ notebook de estudo
          └─ política de tracking
                  ↓
          runs DEVELOPMENT
                  ↓
          validação humana
                  ↓
           run VALIDATION
                  ↓
        micromodelo VALIDADO
                  ↓
        handoff governança externa
                  ↓
           Produto de Dados
                  ↓
            run SCORING
                  ↓
      monitoramento e catálogo
```

## 6. Skills previstas

### 6.1 `hub-ml-micromodelos`

Modos planejados:

- `OBJETIVO_CONHECIDO`: transformar uma necessidade em especificação e plano de estudo.
- `DESCOBRIR_OPORTUNIDADES`: propor shortlist de oportunidades sustentadas por metadata observado.
- `PREPARAR_PUBLICACAO`: converter micromodelo validado em handoff estruturado para a governança institucional.

A skill não absorve EDA, cross-EDA, feature engineering, validação estatística ou auditoria. Faz handoffs explícitos para as skills especializadas.

### 6.2 `hub-ml-padronizar-micromodelo`

Somente depois do piloto novo e do freeze V1. Responsável por migração conservadora de legado, separando migração de modernização funcional.

## 7. Prompts previstos

Na fase de fundação:

- `hub_prompts/micromodelo_novo/`.
- `hub_prompts/descobrir_micromodelos/`.

O briefing de migração só nasce junto da skill de migração, após V1.

Cada prompt deve seguir o contrato vigente: README, briefing, notebook de exemplo, resposta real e roteamento observado quando a etapa conversacional for testada.

## 8. Scripts internos candidatos

Dentro da skill principal, sem promoção automática para `hub_scripts`:

- `coletar_metadados_produto.py`.
- `validar_micromodelo.py`.
- `calcular_spec_fingerprint.py`.
- `gerar_handoff_governanca.py`.

Promoção de qualquer um para helper global é gate humano.

## 9. Especificação `micromodelo.yaml`

Grupos mínimos a desenhar em MM01:

```text
schema_version
identidade
negocio
entidade
fontes
evidencias
contra_evidencias
classificacao
score
experimentos
validacao
saida
tracking
governanca
publicacao
proveniencia
```

Estados candidatos:

```text
IDEIA → EM_DESCOBERTA → EM_ESTUDO → EM_VALIDACAO → VALIDADO
→ CANDIDATO_PRODUTO → EM_VALIDACAO_GOVERNANCA → PUBLICADO
```

Estados auxiliares: `BLOQUEADO`, `SUSPENSO`, `DEPRECATED`.

A máquina de estados e o schema exatos pertencem à MM01, não à MM00.

## 10. Proveniência

O contrato deverá separar pelo menos:

- `descoberto`: veio de fonte observada.
- `proposto`/`inferido`: conclusão ou sugestão ainda não aprovada.
- `aprovado`: decisão humana explícita.
- `medido`: resultado de execução observada.

A IA nunca transforma resultado não executado em `medido`.

## 11. Spec fingerprint

MM02 definirá uma representação canônica dos campos materiais da especificação e calculará SHA-256. Não será hash bruto do arquivo YAML.

Deve permanecer estável sob alterações editoriais e mudar sob alterações materiais, por exemplo: fonte, janela, regra, peso, threshold, missing, semântica TRUE/FALSE, significado do score ou contrato de saída.

Uma run deverá poder registrar, quando disponíveis:

```text
micromodel_version
spec_fingerprint
git_commit
dataset_ref
run_id
```

Esses identificadores têm finalidades diferentes e não substituem aprovação humana.

## 12. Descoberta metadata-first

MM03 criará o coletor de metadata. O fluxo será progressivo:

1. schemas e objetos visíveis;
2. nomes, tipos, descrições e tags de tabela;
3. shortlist semântica;
4. colunas/tags/constraints somente das candidatas;
5. leitura de dados apenas em etapa posterior, quando necessária e autorizada.

No modo metadata-only são proibidos perfilamento de registros, `count(*)`, amostragem de clientes e consultas de valores.

Visibilidade parcial deve ser declarada como `ESCOPO_OBSERVADO`; nunca inferir catálogo completo a partir de permissões parciais.

## 13. Notebook de estudo

Especialização do contrato geral de notebook do Hub, com seções previstas:

0. identificação e estado;
1. problema de negócio;
2. definição operacional;
3. contrato analítico;
4. descoberta/seleção de fontes;
5. qualidade e cobertura;
6. evidências;
7. contra-evidências e falsos positivos;
8. classificação;
9. score;
10. experimentos;
11. validação;
12. resultados;
13. limitações;
14. contrato de saída;
15. tracking;
16. decisão de publicação;
17. resumo executivo.

Não executado permanece pendente; número plausível não substitui evidência.

## 14. README do micromodelo

Não usa o template de README de objeto do Hub porque micromodelo não é objeto da taxonomia do Hub. Deve permitir a um leitor não técnico entender: propósito, população, evidências, classificação, score, fontes, limitações, estado, versão, validação, publicação e quando não usar.

## 15. MLflow

MLflow será o histórico das execuções relevantes, não a especificação e não a tabela de resultados por cliente.

Tipos planejados:

- `DEVELOPMENT`: comparação de hipóteses/configurações.
- `VALIDATION`: evidência formal para decisão de validação.
- `SCORING`: execução oficial sobre população definida.

Métricas base a avaliar em MM06 incluem população, contagens TRUE/FALSE/indeterminado, percentuais e estatísticas de score. Distribuições completas serão artifacts, não dezenas de métricas escalares.

O helper existente `hub_snippets.ml.mlflow_run` deve ser reutilizado. Uma extensão retrocompatível para micromodelos sem artefato sklearn será avaliada em MM06 e não será implementada sem gate explícito.

Resultados individuais permanecem em Delta/Produto de Dados governado; não serão enviados ao tracking.

## 16. Monitoramento

Depois da publicação do piloto, MM11 avaliará o recurso de profiling/monitoramento disponível no workspace para acompanhar distribuição, drift e métricas customizadas. Monitoramento não será requisito do MVP se o ambiente não o suportar/autorizá-lo.

## 17. Visual

MM00–MM10 não dependem do fechamento completo da frente visual. A integração definitiva ocorre em MM11, contra a API visual vigente naquele momento. O micromodelo nunca possui tema próprio; consome os contextos existentes e `ResolvedTheme` quando aplicável.

## 18. Sprints

### MM00 — baseline e arquitetura

Inventário, matrizes, ADRs, testes documentais e checkpoint. Nenhum código funcional do framework.

### MM01 — contrato canônico

Schema e máquina de estados do YAML, proveniência, validador interno e fixtures negativas/positivas.

### MM02 — fingerprint

Canonicalização, campos materiais/editoriais, SHA-256, versionamento do algoritmo e testes metamórficos. Estado corrente e perfil material: [MM02/README.md](MM02/README.md).

### MM03 — metadata-only

Coletor sanitizado, descoberta progressiva, segurança contra instruções embutidas e fixtures de catálogo.

### MM04 — objetivo conhecido

Primeiro modo de `hub-ml-micromodelos`, handoffs e prompt `micromodelo_novo`.

### MM05 — descoberta de oportunidades

Segundo modo, shortlist, deduplicação, risco e prompt `descobrir_micromodelos`.

### MM06 — notebook, README e tracking

Templates de domínio, contrato de runs e eventual proposta de extensão retrocompatível de `mlflow_run`.

### MM07 — pacote departamental

Documento executivo/técnico, guia de primeiro uso, matriz de permissões, plano de piloto e rollback. Auditoria A2 antes do envio.

### MM08 — homologação no trabalho

Roteamento, metadata, permissões, MLflow e integração externa testados em ambiente real sem migração de legado.

### MM09 — piloto greenfield

Primeiro micromodelo novo nasce integralmente pela nova esteira. Runs DEVELOPMENT e VALIDATION e avaliação da experiência do cientista.

### MM10 — produto e scoring

Handoff para governança, validação externa, publicação somente se autorizada, primeira run SCORING e reconciliação de agregados com o Produto de Dados.

### MM11 — hardening, visual e monitoramento

Corrigir framework com evidência do piloto; avaliar integração visual e profiling; congelar `FRAMEWORK_MICROMODELOS_V1`.

### MM12 — migração dos legados

Inventário do acervo; classificação A/B/C/D; criação da skill de migração; migração conservadora; equivalência antes/depois; modernização em mudança separada.

### MM13 — catálogo e escala

Catálogo derivado dos YAMLs, análise de impacto, visão de portfólio proporcional à escala e auditoria final.

## 19. Gates de parada

Parar e pedir decisão antes de: mudar arquitetura aprovada; usar fonte fora do catálogo configurado; versionar identificador real do trabalho; solicitar permissão/ACL; alterar score/peso/threshold/semântica; criar breaking change; modificar regras externas de publicação; publicar; alterar núcleo visual; promover script interno a helper global; mudar `mlflow_run`; aceitar divergência de migração; ou resolver divergência material entre auditorias por preferência.

Pode prosseguir documentando premissa em nomenclatura interna, fixtures sintéticas, prosa, testes adicionais e refatoração sem mudança de comportamento.

## 20. Auditoria e avanço

Toda sprint segue:

```text
inspecionar estado real
→ fixar escopo
→ implementar somente o escopo
→ testar
→ auditoria independente proporcional ao risco
→ verificar cada achado
→ corrigir
→ retestar
→ documentar
→ checkpoint
→ aceite
→ merge
```

Skills novas exigem forward tests positivo, negativo e `@menção` em chats novos, além dos gates estruturais existentes.

## 21. Critério para autorizar migração

MM12 só inicia quando o piloto novo estiver concluído, runs e Produto de Dados estiverem reconciliados, o framework tiver sido corrigido e V1 congelada. Pergunta de gate:

> Se um segundo micromodelo novo começasse amanhã, usaríamos a mesma arquitetura sem redesenhá-la?

Se a resposta for não, a migração continua bloqueada.

## 22. Fora do MVP

Não criar prematuramente App, multiagentes, banco vetorial, RAG persistente próprio, autopublicação, autoaprovação, Feature Store própria, dashboard customizado, plataforma de lineage paralela, tema visual paralelo ou LLM classificando clientes individualmente em runtime.
