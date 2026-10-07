# Checklist — objeto novo do Hub

Use no chamado ou na entrega do objeto. Este é o checklist canônico do contrato
do artefato; os templates de `hub_padroes/` apontam para cá. Marque apenas itens
com evidência. Verificação por terceiro e juízo do autor são coisas distintas.

`tools/validate_assistant.py`, `tools/api_publica.py` e
`tools/spark_smoke_test.py` vivem no repositório e não viajam com `.assistant/`.
No workspace, registrar dependências dessas ferramentas como “a conferir no
repositório” e encaminhar ao mantenedor; não declarar que foram executadas.
A contribuição, CI e publicação têm checklist próprio no repositório, em
`docs/manutencao/CHECKLIST_OBJETO_NOVO.md`.

## Pré-condições e evidência

- [ ] Tipo confirmado: snippet, script, prompt, README, notebook ou skill
- [ ] Demanda comparada ao catálogo; sobreposição resolvida explicitamente
- [ ] Template atual do tipo lido; destino e escopo de escrita autorizados
- [ ] Preflight, policy e gates exigidos pela [skill](../SKILL.md) respeitados
- [ ] Geração, validação estrutural, autorização e escrita reportadas separadamente
- [ ] Receipt/verificador aplicável observado, sem inferir runtime ou homologação
- [ ] Destino existente, overwrite, merge, remoção e conversão não autorizados pelo mero PASS de preflight
- [ ] Falha parcial conserva efeito e evidência; recuperação exige decisão, sem apagar ou repetir para sobrescrever

## Artefatos verificáveis

### Snippet, script ou prompt
- [ ] `README.md` segue o [contrato de objeto](../../../hub_padroes/readme/template_objeto.md)
- [ ] [Checklist editorial](../../../hub_padroes/readme/checklist_objeto.md) com evidência
- [ ] README e exemplo têm navegação recíproca e efeitos explícitos

### Snippet ou script
- [ ] Nome `snake_case`, identificador Python válido
- [ ] Snippet em `hub_snippets/<secao>/<nome>/`; script em `hub_scripts/<nome>/`, sem nível de seção
- [ ] Módulo com mesmo nome da pasta, `__init__.py` e `exemplo_<nome>.py`
- [ ] `exemplo_<nome>.py` abre com `# Databricks notebook source`
- [ ] `__init__.py` corresponde à API pública integral; geração/conferência repo-side pendente quando indisponível
- [ ] Docstrings com Args, Returns, Raises e armadilhas; assinatura e retornos conferidos no código
- [ ] Sem `cache()`/`persist()` desprotegido, `toPandas()` sem limite ou sentinela numérica para erro
- [ ] Sessão Spark via `getActiveSession() or getOrCreate()`, quando aplicável
- [ ] Imports e caso representativo verificados ou NÃO EXECUTADOS com motivo

### Script
- [ ] Entradas, retorno e efeitos seguem o contrato específico da tarefa
- [ ] Diagnóstico por endereço e somente leitura, quando esse for o perfil contratado
- [ ] Qualquer escrita, arquivo, tabela ou run é declarado e depende de autorização
- [ ] Exemplo demonstra sucesso, falha e limites aplicáveis, sem outputs inventados

### Notebook
- [ ] Abre com `# Databricks notebook source`
- [ ] Tabela de premissas do ambiente inclui **Escrita**, dependências e compute
- [ ] Bloco `text` contém saída literal ou bloco canônico de não executado
- [ ] Dependências opcionais e pins conferidos; instalação somente por mecanismo permitido e autorizado
- [ ] “Quando não usar” específico do objeto
- [ ] Execução no alvo: [resultado observado e fonte, NÃO EXECUTADO ou bloqueio]; forma válida não prova SUCCESS

### Skill
- [ ] Pasta igual a `name`; frontmatter conforme política local (`name`, `description`)
- [ ] Description com função e gatilhos; inclusão/exclusão claras
- [ ] `SKILL.md` com menos de 500 linhas, conforme o molde vigente
- [ ] Corpo conciso, com fluxo, helpers, proibições e formato de saída
- [ ] Helpers declarados por caminho de import e links resolvidos
- [ ] Roteamento positivo/negativo/menção: [evidência ou NÃO EXECUTADO], sem inferir descoberta por estrutura

### Conversão de objeto existente
- [ ] Assinatura, ordem/nome dos parâmetros e nomes devolvidos inalterados
- [ ] Comportamento em vazio, nulo e bordas preservado
- [ ] Nenhum identificador traduzido
- [ ] Melhorias funcionais separadas da conversão e dependentes de autorização própria

## Juízo de quem escreveu

Estes itens são declarações fundamentadas, não prova mecânica:
- [ ] Docstring explica por que o objeto existe
- [ ] Decisões não óbvias têm motivo; erros dizem como prosseguir
- [ ] Limites calibráveis são nomeados e sua autoridade é identificada
- [ ] Cabeçalho explica o problema; prosa usa resultados observados
- [ ] Saída literal preservada e qualquer corte declarado
- [ ] Limitações e “quando não usar” são específicas

## Limite da entrega

Forma, testes locais e Receipt estrutural não comprovam roteamento no Genie,
comportamento com dado real, ACL, publicação ou homologação. Cada pendência deve
indicar a evidência faltante e quem pode conduzir a próxima etapa.
