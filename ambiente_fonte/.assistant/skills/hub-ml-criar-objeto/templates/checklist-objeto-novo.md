# Checklist — objeto novo do Hub

Cole numa PR, num chamado ou no fim do notebook de trabalho.

**A lista está dividida em duas naturezas**, e a distinção não é formalidade:
o primeiro grupo um terceiro consegue conferir sozinho, sem conversar com quem
escreveu; o segundo é juízo de quem escreveu, e vale como declaração, não como
prova. Um checklist que promete verificação e entrega opinião ensina a marcar
tudo — e aí as linhas boas perdem força junto.

Este é o checklist **canônico**. Os templates de `hub_padroes/` apontam para cá
em vez de repetir a lista.

---

> **Sobre os comandos deste checklist.** `tools/validate_assistant.py`,
> `tools/api_publica.py` e `tools/spark_smoke_test.py` vivem **no repositório**,
> não no workspace — eles não são publicados com o `.assistant/`. Quem estiver só
> no Genie Code marca os itens que dependem deles como "a conferir no
> repositório" e avisa quem for commitar.

## Parte 1 — verificável por terceiro

### Comum a todos os tipos

- [ ] O tipo é um dos seis: snippet, script, prompt, README, notebook, skill
      (`auditoria/` é molde de processo, não conta)
- [ ] Nenhum objeto do `CATALOGO_HELPERS.md` atende à mesma demanda
- [ ] `python tools/validate_assistant.py` aprovado
- [ ] `CATALOGO_HELPERS.md` ganhou a linha, com a coluna de dependência
- [ ] Entrada no `CHANGELOG.md`

### Se é snippet ou script

- [ ] Nome em `snake_case`, identificador Python válido
- [ ] Snippet mora em `hub_snippets/<secao>/<nome>/`; script mora em
      `hub_scripts/<nome>/`, **sem** nível de seção
- [ ] O módulo se chama **como a pasta**: `pit_join/pit_join.py`
- [ ] Existe `exemplo_<nome>.py`, mesmo que o objeto seja trivial
- [ ] **`exemplo_<nome>.py` abre com `# Databricks notebook source`**
- [ ] `__init__.py` idêntico à saída de `python tools/api_publica.py`
- [ ] Docstring da função tem `Args`, `Returns` e `Raises` (e `Note`, se houver
      armadilha)
- [ ] Sem `cache()`/`persist()` desprotegido, sem `toPandas()` sem limite, e sem
      sentinela numérica para sinalizar erro
- [ ] Sessão Spark obtida por `getActiveSession() or getOrCreate()`, se usa Spark
- [ ] A tabela de módulos em `hub_snippets/README.md` (ou `hub_scripts/README.md`)
      lista o objeto
- [ ] O objeto importa: `from hub_snippets.<secao>.<nome> import <api>`
- [ ] O smoke test continua verde (`tools/spark_smoke_test.py`)
- [ ] Se é conversão: `grep` mostra que quem importava o módulo continua
      importando

### Se é script, além do acima

- [ ] Recebe o **endereço** do que diagnostica — nome de tabela ou caminho —,
      não o dado já carregado
- [ ] Devolve veredito estruturado, com contagem do que foi varrido
- [ ] Não escreve nada: sem tabela, sem arquivo, sem run de MLflow
- [ ] O notebook mostra o caso que **passa** e o caso que **falha**

### Se é notebook

- [ ] Abre com `# Databricks notebook source`
- [ ] Tem tabela "o que este notebook assume do ambiente", com a linha **Escrita**
- [ ] Tem bloco de saída com a cerca `text` — ou o bloco canônico de não executado
- [ ] Se instala biblioteca: `%pip install` e `%restart_python` na abertura, com
      o pin conferido em `requirements-optional.txt`
- [ ] Tem seção "quando **não** usar"
- [ ] Executou no ambiente alvo, e o resultado foi SUCCESS

### Se é skill

- [ ] O nome da pasta é idêntico ao campo `name` do frontmatter
- [ ] O frontmatter tem só `name` e `description`
- [ ] A `description` declara o que a skill **não** cobre
- [ ] O `SKILL.md` tem menos de 500 linhas
- [ ] O corpo tem as cinco seções do template: quando se aplica, fluxo, helpers,
      o que nunca fazer, formato de saída
- [ ] Os helpers estão declarados por caminho de import, em tabela
- [ ] Todos os caminhos de helper citados resolvem para objeto existente
- [ ] `EXPECTED_SKILLS` em `tools/publicar_free.py` acompanha a contagem
- [ ] Os dois inventários listam a skill: `skills/README.md` e a tabela de
      invocação do `.assistant/README.md`
- [ ] O roteiro de forward test ganhou os três casos, e o formulário de
      resultados ganhou a linha
- [ ] **Forward test executado**: caso positivo, caso negativo e `@menção`, cada
      um em chat novo

### Se é conversão de objeto que já existe

- [ ] Assinatura, ordem e nome dos parâmetros **inalterados**
- [ ] Nomes devolvidos — colunas, chaves — **inalterados**
- [ ] Comportamento em base vazia, nulo e caso limite **inalterado**
- [ ] Nenhum identificador traduzido
- [ ] A melhoria, se houver, está em **commit separado**

---

## Parte 2 — juízo de quem escreveu

Ninguém confere isto por você. São declarações, e valem pelo que quem assina
souber sustentar.

- [ ] O tipo foi **confirmado** com quem pediu
- [ ] O template do tipo foi lido nesta sessão, não de memória
- [ ] A docstring do módulo diz **por que ele existe**, não o que ele faz
- [ ] Toda decisão de projeto não óbvia tem comentário com o **motivo**
- [ ] A mensagem de erro diz **o que fazer**, não só o que houve
- [ ] Todo limite calibrável virou constante nomeada
- [ ] O cabeçalho do notebook abre com o **problema**, não com a função
- [ ] A saída colada é **literal**; se foi cortada, o corte está declarado
- [ ] A prosa cita o número **obtido**, não o pretendido
- [ ] A seção "quando não usar" é específica **deste** objeto, e não genérica

---

## O que este checklist não cobre

**Roteamento**, se o objeto for skill. Uma `description` nova compete com as
existentes, e isso só se mede em chat: caso positivo, caso negativo e `@menção`.
O roteiro está em `docs/testes/forward/roteiro.md`.

**Comportamento em dado real.** Tudo aqui é sobre forma e sobre o laboratório. O
que só aparece com volume, permissão e dado governado é assunto do runbook de
replicação, em `docs/playbooks/`.
