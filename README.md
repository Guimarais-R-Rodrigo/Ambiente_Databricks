![CRM — Missão Modelos Analíticos CRM](ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Ambiente integrado de governança, biblioteca analítica e contexto para ajudar a Genie Code e a equipe a trabalhar com métodos, componentes e critérios de revisão consistentes.

> **Procedência.** Agent Skills e instruções são mecanismos reconhecidos pela Genie Code. Pastas `hub_*` e skills `hub-*` são implementações e convenções deste projeto; não são produtos institucionais da Databricks.

**Manual Técnico:** [APIs, Python, Spark, helpers e operação do Hub](MANUAL_TECNICO.md).

**Candidata em reconciliação:** `hub-ml-micromodelos` foi incorporada como
contrato L1 estático a partir do Free; [estado e evidências](docs/sprints/skill_enforcement_rollout/RECONCILIACAO_MM04_2026-09-29.md).

---

## 🧭 Por onde começar

| Objetivo | Abra |
|---|---|
| entender o ecossistema e o primeiro uso | [guia `.assistant`](ambiente_fonte/.assistant/README.md) |
| consultar APIs, arquitetura e operação | [Manual Técnico](MANUAL_TECNICO.md) |
| usar funções/classes reutilizáveis | [Hub Snippets](ambiente_fonte/.assistant/hub_snippets/README.md) |
| usar utilitários técnicos | [Hub Scripts](ambiente_fonte/.assistant/hub_scripts/README.md) |
| escolher uma Agent Skill | [Skills](ambiente_fonte/.assistant/skills/README.md) |
| preencher um briefing | [Hub Prompts](ambiente_fonte/.assistant/hub_prompts/README.md) |
| criar ou manter objetos do Hub | [Hub Padrões](ambiente_fonte/.assistant/hub_padroes/README.md) |
| acompanhar sprints e histórico | [Índice de sprints](docs/sprints/README.md) |

## 🌟 O que é este ecossistema

Projetos de Machine Learning em Big Data exigem decisões recorrentes sobre grão, tempo, amostragem, leakage, métricas, visualização, monitoramento e governança. Sem o contexto do projeto, um assistente pode propor fórmulas, bibliotecas ou convenções diferentes das usadas pela equipe.

O ecossistema `.assistant` organiza esse contexto em camadas separadas:

- **Agent Skills:** orientam tarefas completas, guardrails, recursos e formatos de saída;
- **Hub Snippets:** funções e classes Python reutilizáveis;
- **Hub Scripts:** utilitários explícitos de inspeção, transformação e governança;
- **Hub Prompts:** briefings estruturados preenchidos pelo usuário;
- **Hub Padrões:** moldes arquiteturais, editoriais e de criação/manutenção.

A pasta `hub_readmes_visual_assets/` é infraestrutura editorial para diagramas e cabeçalhos. Ela não é um sexto componente funcional nem fornece contexto automaticamente à Genie Code.

## 🏛️ Arquitetura e responsabilidade

![Corte arquitetural entre fonte versionada, workspace, contexto da Genie Code, notebook e runtime.](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

A separação principal é entre **contexto** e **execução**:

- Agent Skills e instruções orientam a Genie Code;
- prompts e padrões são fornecidos quando necessários;
- `hub_snippets` e `hub_scripts` pertencem ao runtime Python e precisam ser importados explicitamente;
- a existência de um arquivo dentro de `.assistant` não o coloca automaticamente no `sys.path`;
- publicar, executar, revisar e promover são gates distintos.

`ambiente_fonte/` é a fonte editável. `Novo_Ambiente_Simulado/` é uma representação derivada e deve permanecer sincronizada por ferramenta/gates, não por edição manual concorrente.

## 🎨 Sistema de Temas

V00–V13 estão aceitas e integradas no Git. A V12 foi integrada pela PR #54 no merge `a6309a4d0b3a3530c52330e65ee5a18674118378`, preservando estados honestos distintos: `DOC-02`, `DOC-03`, `SEC-01`, `UAT-01` e `V12-AIBI-01` possuem PASS no alcance documentado; `A11-01` permanece **FAIL** rastreado na issue #57; `V12-LAB-01`, `V12-APP-01` e `V12-AIBI-02` permanecem **BLOQUEADO_AUTORIZACAO**. Esses estados não são intercambiáveis.

O Plano Mestre V13 foi aceito e integrado pela PR #58 no merge `c339ed177f4b901a907ea6ad43f0803f5b7ccc09`. S0–S6 foram integradas pelas PRs #59–#65. A **S7 — handoff operacional e fechamento** foi aceita e integrada pela PR #66 no merge `62e9404851d6a7902371bd5b6531a113d521311c`; os **15/15 workflows de `push`** desse SHA concluíram em `success`. A homologação humana S7 está registrada como `HUMAN-01 = PASS`, com participante sanitizado `Tester`, duração de 5 minutos, zero ajuda, zero erros de interpretação e H1–H6 em PASS. Esse resultado é formativo: não constitui production readiness, não autoriza Databricks e não fecha #57. A [auditoria pós-merge V13](docs/sprints/sistema_temas/V13/AUDITORIA_POS_MERGE.md) registra a certificação e o drift documental dos índices vivos encontrado após o merge.

A V11 projeta um `ResolvedTheme` `notebook` para capacidades documentadas de temas nativos AI/BI sem criar uma segunda fonte de verdade. `context="aibi"` continua reservado no schema central. A matriz integrada cobre os 48 tokens notebook como **3 traduzidos, 23 aproximados e 22 não suportados**. Como as fontes oficiais verificadas não publicam um schema completo e versionado do JSON produzido por `Export theme`, a V11 não inventa campos nativos: um candidato de importação só pode ser construído sobre um export real fixado por SHA-256 e um binding revisado para campos já existentes.

Regras atuais:

- `ResolvedTheme` continua sendo a fonte configurável de verdade;
- consumidores visuais usam rotas explícitas `_resolvido` quando suportadas;
- aparência não pode alterar cálculo, amostragem, embedding, política de monitoramento ou métricas;
- o template EDA não mantém paleta ou dicionário de tema paralelos;
- o kit V09 exige `theme_contract` v1 com nove caminhos canônicos protegidos por hash;
- transporte é obrigatório, ativação continua `manual_opt_in` e publicação continua `not_performed`;
- a V10 não implementa `context="app"`; o App gerencia propostas `notebook` existentes;
- a V11 não implementa `context="aibi"`, não chama SDK/REST/CLI Databricks e não publica dashboard;
- a V12 não converte CI em homologação de ambiente ou UAT e falha fechado sem autorização, identidade, classificação de dados, evidência ou rollback aplicável;
- o PASS real `V12-AIBI-01` cobre somente import de tema em dashboard draft de teste, e `SEC-01` cobre somente identidade/permissão efetiva observadas; workspace theme, ACL, deploy de App e `Publish` continuam não autorizados;
- tema do workspace e tema local do dashboard têm escopos distintos; reaplicação de workspace theme em dashboard existente é manual, não propagação universal;
- SHAP/Matplotlib e Kaplan–Meier continuam limites explícitos onde o contrato atual não representa a semântica necessária;
- nada disso publica automaticamente no Databricks.

Na V10, os gates Git/CI exercitam identidade sintética, isolamento, persistência V05, bundle implantável derivado e regressões locais. No head reconciliado `cb942ee955ff9236f19099e5ed4ceee9beb32000`, os dez workflows reais de PR concluíram com `success`; depois do merge `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`, os 12 workflows disparados por `push` na `main` também concluíram em `success`, incluindo o workflow V10 `34896944061`. Isso **não** comprova headers reais, permissões/grupos do workspace, UC Volume real, browser, acessibilidade, concorrência multiusuário ou UAT. Nenhuma criação/atualização de Databricks App foi executada por essa sprint.

Estado corrente: [V13](docs/sprints/sistema_temas/V13/README.md) está encerrada no Git e sua [auditoria pós-merge](docs/sprints/sistema_temas/V13/AUDITORIA_POS_MERGE.md) preserva os limites e dívidas transferíveis. O [Plano Mestre V14](docs/sprints/sistema_temas/V14/PLANO_MESTRE.md) foi aceito e integrado pela PR #70 no merge `350dcf0b37e730042ef961f12f11b30b2660d2c6`. A **S0 V14 foi aceita e integrada pela PR #71** no merge `e89ef4f79d9f9b7c901f1bbf490259ee5ce3d493`; os **16/16 workflows de `push`** desse SHA concluíram em `success`. A V14 está agora na **S1 — ownership, autoridade e modelo operacional**, documentada no [README V14](docs/sprints/sistema_temas/V14/README.md), na [matriz de ownership](docs/sprints/sistema_temas/V14/MATRIZ_OWNERSHIP.json), no [runbook S1](docs/sprints/sistema_temas/V14/S1_MODELO_OPERACIONAL.md) e no [checkpoint S1](docs/sprints/sistema_temas/V14/CHECKPOINT_S1.md). A S1 mantém owner/backup/autoridade não evidenciados em `BLOCKED`; **S2–S8 não foram iniciadas**, nenhuma decisão de production readiness/go-live foi tomada e nenhuma autorização Databricks decorre da S1. O fechamento herdado permanece em [V12](docs/sprints/sistema_temas/V12/README.md) e [escopo/aceite V12](docs/sprints/sistema_temas/V12/ESCOPO_E_ACEITE.md).

## 🔄 Como o contexto chega à Genie Code

1. Você descreve a demanda, anexa os recursos necessários e pode selecionar uma skill com `@hub-ml-*`.
2. As instruções aplicáveis e a skill orientam método, riscos, recursos e formato.
3. Helpers recomendados continuam sendo importados e executados explicitamente no notebook/runtime.
4. A pessoa revisa código, dados, custo, resultado e qualquer operação persistente antes de aceitar a entrega.

Não existe uma leitura automática única de toda a pasta `.assistant`. A ativação de uma skill por relevância não significa que snippets, scripts, prompts e padrões foram automaticamente executados ou importados.

## 🧭 Como evitar duas fontes de verdade

| Camada | Papel | Regra |
|---|---|---|
| `ambiente_fonte/` | fonte do produto | editar aqui |
| `Novo_Ambiente_Simulado/` | derivado de verificação | manter equivalente à fonte |
| `tools/` | testes, gates e automação | executar antes de promover |
| `docs/` | decisões e evidências | registrar escopo e limites |
| workspace | cópia operacional | validar separadamente antes de uso |

O gate local, a comparação fonte/simulado, smoke tests, regressões e forward tests cobrem riscos diferentes; nenhum substitui os demais.

### Estado verificável do gate local

O bloco abaixo é conferido por `python tools/validate_assistant.py --conferir-readme`. Se qualquer linha divergir da execução real, o gate reprova.

```text
raiz analisada     : /home/runner/work/Ambiente_Databricks/Ambiente_Databricks/ambiente_fonte
skills             : 15 · 15/15 com as 5 seções estruturais
skill enforcement  : 14/14 contratos válidos · 0 issue(s) de policy
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 102 caminhos verificados
markdown / links   : 235 arquivos / 1452 links relativos
notebooks / links  : 82 notebooks / 102 links relativos
readmes de objeto  : 77/77 operacionais; 3/3 exemplares; 0 pendentes (estrutura, não aceite editorial)
pastas de objeto   : 63 conferidas (nome, arquivos, __init__)
forma da pasta     : 61 conferidas (o módulo tem o nome da pasta)
contrato de dados  : 63 pares (saída: o que o notebook consome)
contrato de entrada: 61 pares (entrada: o que o notebook passa)
saída colada       : 81 notebooks com bloco real, 0 sem
idioma da docstring: 62 módulos, 0 com docstring em inglês
normas do molde    : 76 arquivos, 0 violação(ões)
notebook exercita  : 61 objetos, 0 notebook(s) que só importam
python (AST)       : 272 arquivos
instrucoes         : 12418/20000 caracteres
repo (identidade)  : 2234 arquivos varridos no repositório editável/derivado
repo (links)       : 2640 links fora da raiz analisada
worktree (extras)  : 0 arquivos locais examinados, fora da contagem versionada

APROVADO: 0 falha(s), 0 aviso(s)
```

## ❓ Perguntas frequentes

**A Genie Code lê tudo automaticamente?** Não. Instruções e skills usam mecanismos próprios; prompts/padrões precisam ser fornecidos quando necessários, e código Python precisa ser importado no runtime.

**Como disponibilizo `hub_snippets` no Python?** Garanta que a raiz que contém `hub_snippets/` esteja no ambiente Python adotado e então faça o import explícito. Dependências opcionais precisam ser declaradas e validadas no compute usado.

**Skill, Prompt, Snippet e Script são a mesma coisa?** Não. Skill orienta metodologia; Prompt é briefing; Snippet é função/classe importável; Script é utilitário explícito com contrato próprio.

**O Hub elimina leakage ou erros analíticos?** Não. Ele torna contratos e verificações mais explícitos, mas a pessoa continua responsável por revisar entidade, instante de decisão, janelas, disponibilidade e resultado.

**Posso criar novos objetos?** Sim. Use [Hub Padrões](ambiente_fonte/.assistant/hub_padroes/README.md) e `@hub-ml-criar-objeto`, mantendo API pública, README, exemplo, testes e gates.

**Código gerado pode ser executado sem revisão?** Não é recomendado. Revise recursos, filtros, plano, coletas, dependências, permissões e ações persistentes.

## 🔗 Continuidade e histórico

O histórico detalhado de sprints, iniciativas R00–R13, integrações e reconciliações documentais permanece no [índice de sprints](docs/sprints/README.md). Para instalação/replicação no trabalho, siga o [playbook de replicação](docs/playbooks/replicacao-trabalho.md).
