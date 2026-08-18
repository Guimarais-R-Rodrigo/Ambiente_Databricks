# Checklist — objeto novo do Hub

Cole numa PR, num chamado ou no fim do notebook de trabalho. Cada linha é
verificável; se não for, ela não deveria estar aqui.

## Antes de escrever

- [ ] O tipo foi **confirmado com quem pediu** e é um dos seis: snippet, script,
      prompt, README, notebook, skill
- [ ] O template correspondente foi **anexado** ao chat (`@` ou Add context) —
      `hub_padroes/` não é auto-descoberto
- [ ] O nome não colide com objeto existente, nem fica a uma letra de um
      (`drift_detection` e `drift_detector` já convivem)

## A pasta

- [ ] Nome em `snake_case` — ou `hub-ml-<tema>`, com hífen, se for skill
- [ ] O módulo se chama **como a pasta**: `pit_join/pit_join.py`
- [ ] Existe `exemplo_<nome>.py`, mesmo que o objeto seja trivial
- [ ] `__init__.py` gerado por `python tools/api_publica.py`, sem edição manual

## O módulo

- [ ] Docstring diz **por que existe**, não o que faz
- [ ] Toda decisão não óbvia tem comentário com o **motivo**
- [ ] Docstring da função tem `Args`, `Returns` e `Raises`
- [ ] Entrada inválida falha cedo, com mensagem que diz o que fazer
- [ ] Limite calibrável está em constante nomeada no topo
- [ ] Sessão Spark obtida por `getActiveSession() or getOrCreate()`
- [ ] Sem `cache()`/`persist()` desprotegido, sem `toPandas()` sem limite, e sem
      sentinela numérica para sinalizar erro

## O notebook

- [ ] Cabeçalho abre com o **problema real**, não com a função
- [ ] Tabela de ambiente preenchida, inclusive a linha **Escrita**
- [ ] Se há erro típico associado, ele aparece **acontecendo** antes da correção
- [ ] A saída real está colada, **literal** — corte declarado, nunca completado
- [ ] A prosa cita o **número obtido**, não o pretendido
- [ ] Se instala biblioteca: `%pip install` e `%restart_python` na abertura, com
      o pin conferido em `requirements-optional.txt`
- [ ] Se algo não roda: bloco canônico, com motivo verificado e erro real citado
- [ ] Seção "quando **não** usar" existe e é específica deste objeto

## Se é conversão de objeto que já existe

- [ ] Assinatura, ordem e nome dos parâmetros **inalterados**
- [ ] Nomes devolvidos — colunas, chaves — **inalterados**
- [ ] Comportamento em base vazia, nulo e caso limite **inalterado**
- [ ] Nenhum identificador traduzido
- [ ] A melhoria, se houver, está em **commit separado**

## Antes de fechar

- [ ] `python tools/validate_assistant.py` aprovado
- [ ] O README da seção lista o objeto
- [ ] `CATALOGO_HELPERS.md` ganhou a linha, com a coluna de dependência
- [ ] O notebook **executou** no ambiente alvo
- [ ] Entrada no `CHANGELOG.md`

## O que este checklist não cobre

Roteamento, se o objeto for skill. Uma `description` nova compete com as
existentes, e isso só se mede em chat: caso positivo, caso negativo e `@menção`.
O roteiro está em `docs/testes/forward/`.
