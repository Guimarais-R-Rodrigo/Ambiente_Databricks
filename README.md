![CRM — Missão Modelos Analíticos CRM](ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Ambiente integrado de governança, biblioteca analítica e contexto para ajudar a Genie Code e a equipe a trabalhar com métodos, componentes e critérios de revisão consistentes.

> **Procedência.** Agent Skills e instruções são mecanismos reconhecidos pela Genie Code. Pastas `hub_*` e skills `hub-*` são implementações e convenções deste projeto; não são produtos institucionais da Databricks.

**Manual Técnico:** [APIs, Python, Spark, helpers e operação do Hub](MANUAL_TECNICO.md).

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

V00–V11 estão aceitas e integradas no Git. A V11 foi aceita em 14/09/2026 e integrada pelo PR #52 no merge `9305bc49eaf002caec042361bf35efa66af7ca18`. Os 11 workflows reais da PR concluíram com `success`; depois do merge, os 13 workflows disparados por `push` na `main` também concluíram com `success`. Nenhuma operação real de tema AI/BI foi executada no Databricks.

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
- tema do workspace e tema local do dashboard têm escopos distintos; reaplicação de workspace theme em dashboard existente é manual, não propagação universal;
- SHAP/Matplotlib e Kaplan–Meier continuam limites explícitos onde o contrato atual não representa a semântica necessária;
- nada disso publica automaticamente no Databricks.

Na V10, os gates Git/CI exercitam identidade sintética, isolamento, persistência V05, bundle implantável derivado e regressões locais. No head reconciliado `cb942ee955ff9236f19099e5ed4ceee9beb32000`, os dez workflows reais de PR concluíram com `success`; depois do merge `6245fa3c6ea7da6bfeaf6442f01f572f7f9bd00b`, os 12 workflows disparados por `push` na `main` também concluíram com `success`, incluindo o workflow V10 `34896944061`. Isso **não** comprova headers reais, permissões/grupos do workspace, UC Volume real, browser, acessibilidade, concorrência multiusuário ou UAT. Nenhuma criação/atualização de Databricks App foi executada por essa sprint.

Detalhes da etapa integrada mais recente: [V11](docs/sprints/sistema_temas/V11/README.md) e [checkpoint V11](docs/sprints/sistema_temas/V11/CHECKPOINT_V11.md). As etapas anteriores permanecem em [V10](docs/sprints/sistema_temas/V10/README.md), [checkpoint V10](docs/sprints/sistema_temas/V10/CHECKPOINT_V10.md) e [V09](docs/sprints/sistema_temas/V09/README.md).

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
skills             : 14 · 14/14 com as 5 seções estruturais
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 92 caminhos verificados
markdown / links   : 222 arquivos / 1395 links relativos
notebooks / links  : 80 notebooks / 101 links relativos
readmes de objeto  : 76/76 operacionais; 3/3 exemplares; 0 pendentes (estrutura, não aceite editorial)
pastas de objeto   : 62 conferidas (nome, arquivos, __init__)
forma da pasta     : 60 conferidas (o módulo tem o nome da pasta)
contrato de dados  : 62 pares (saída: o que o notebook consome)
contrato de entrada: 60 pares (entrada: o que o notebook passa)
saída colada       : 79 notebooks com bloco real, 0 sem
idioma da docstring: 62 módulos, 0 com docstring em inglês
normas do molde    : 72 arquivos, 0 violação(ões)
notebook exercita  : 60 objetos, 0 notebook(s) que só importam
python (AST)       : 221 arquivos
instrucoes         : 9043/20000 caracteres
repo (identidade)  : 1424 arquivos varridos no repositório editável/derivado
repo (links)       : 1904 links fora da raiz analisada
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

O histórico detalhado de sprints, iniciativas R00–R13, integrações e reconciliações documentais permanece no [índice de sprints](docs/sprints/README.md). O README raiz deixa de duplicar esse histórico para permanecer uma entrada operacional curta e atual.

Para instalação/replicação no trabalho, siga o [playbook de replicação](docs/playbooks/replicacao-trabalho.md).
