# Contexto explícito por tarefa

Use esta rota para preparar uma leitura inicial pequena, com arquivos e motivos
verificáveis. O resultado é **contexto de tarefa, não auditoria integral**. Não
muda o que qualquer cliente carrega automaticamente, não executa testes e não
concede autorização de publicação, instalação ou operação.

## Escolher e ampliar

Da raiz do checkout Git completo, com Python e Git disponíveis:

```sh
python tools/bundle_para_auditoria.py --mode task --task instrucoes-ia
python tools/bundle_para_auditoria.py --mode task --task preparar-entrega
python tools/bundle_para_auditoria.py --mode task --task investigar-regressao \
  --include tools/skill_enforcement/parallel/coverage.py \
  --include tools/tests/test_ser_parallel_b0.py \
  --include docs/sprints/skill_enforcement_rollout/PARALELO/B0/README.md
```

As rotas revisadas ficam em [task-context.json](task-context.json). São listas
finitas de arquivos exatos com motivo, exclusões e direções de expansão:

- `alterar-objeto`: núcleo, fontes, contrato e checklist. Acrescente README,
  implementação, exemplo e testes específicos do objeto com `--include`.
- `preparar-entrega`: skill, runbook, checklist, empacotadores e regressões.
  O manifesto da release escolhida é outra evidência, a conferir separadamente.
- `instrucoes-ia`: owners, compatibilidade, regras e controles. Consulte o
  [mapa](control-map.json) por IDs pertinentes; ele não entra inteiro por padrão.
- `investigar-regressao`: classes de defeito, owners, decisões e localizador de
  história. Acrescente a guarda, o teste e a campanha específicos da falha.

`--include PATH` é repetível e relativo à raiz do repositório, mesmo quando o
comando é chamado de outra pasta. Espaços e Unicode são aceitos; use aspas no
shell. Não aceita diretórios, globs, paths absolutos, `..`, `.git`, symlinks ou
junctions. Só entram arquivos do inventário Git: rastreados e, exclusivamente
com `--allow-dirty`, não rastreados e não ignorados. Paths ignorados não são
liberados por `--include`; nunca force a inclusão de quarentena ou segredos.

Seleção inexistente, binária, não UTF-8 ou vazia falha sem gerar novo bundle.
Cada rota exige de 1 a 32 entradas exatas, além do núcleo comum e das ampliações
explícitas. Uma rota é ponto de partida; não é fechamento automático de imports,
links ou dependências. Se um arquivo mudar de lugar, atualize a rota e seus
testes na mesma alteração. Não substitua paths precisos por busca recursiva.

## Saída, integridade e proveniência

O modo `task` grava `.artifacts/contexto-<tarefa>.txt` e o respectivo
`.txt.manifest.json`. `--saida "caminho com espaços/contexto.txt"` escolhe outro
arquivo, relativo à raiz ou absoluto. O comando cria as pastas necessárias;
recusa sobrescrever paths rastreados, hardlinks e destinos via symlink/junction.
Não escolha a própria saída como input. Saídas do comando são retiradas da
seleção antes da leitura, evitando realimentação em execuções dirty repetidas.

O manifesto registra:

- SHA Git, worktree dirty, flag de revisão e paths/status Git observados,
  inclusive renomes e arquivos não rastreados;
- hash SHA-256 da configuração de rotas, paths incluídos, motivos, bytes e
  SHA-256 de cada arquivo efetivamente lido;
- todos os paths enumerados que ficaram fora do corpo, com motivo, e instruções
  para expandir a consulta; ignorados não fazem parte desse inventário;
- quantidade de arquivos e bytes UTF-8 incluídos, hash e bytes do bundle gerado.

Em `task`, bytes de conteúdo são a soma dos bytes dos arquivos incluídos, sem
cabeçalhos, separadores ou manifesto. Nos modos anteriores, a medida corresponde
ao corpo UTF-8 após a normalização histórica de CRLF/CR para LF. Os hashes sempre
identificam os bytes originais. Os bytes do bundle e do manifesto são exibidos
separadamente. **Não são tokens, custo, latência nem economia medida de cliente.**
O manifesto pode ser maior que o texto inicial: é uma prova de seleção, não uma
instrução para carregar todos os omitidos.

Sem `--allow-dirty`, alterações rastreadas ou não rastreadas impedem a geração.
Com a flag, o conteúdo vem do worktree e não deve ser atribuído só ao commit:
confira os hashes e a proveniência. A leitura não é snapshot atômico nem trava
outros editores. Para reprodução limpa, use checkout isolado do SHA e mantenha
saídas em `.artifacts/` ou fora do repositório. Não compartilhe manifestos dirty
sem conferir também nomes de arquivos e informações privadas.

## Recuperar o corpus amplo

As interfaces anteriores continuam disponíveis, sem ignore global de história:

```sh
python tools/bundle_para_auditoria.py
python tools/bundle_para_auditoria.py --mode canonical --saida .artifacts/canonical.txt
python tools/bundle_para_auditoria.py --mode security --saida .artifacts/security.txt
python tools/bundle_para_auditoria.py --mode full --saida .artifacts/full.txt
python tools/bundle_para_auditoria.py --incluir-espelho --saida .artifacts/full-compat.txt
```

- `canonical`, padrão antigo: texto UTF-8 de todos os paths enumerados, exceto
  espelho e referência congelada. História e auditorias continuam incluídas.
- `security`: mesmo corpo de `canonical`, com manifesto SHA-256 dos arquivos
  enumerados presentes, incluindo binários e camadas omitidas do texto.
- `full`: todas as camadas textuais enumeradas, preservando exclusões binárias
  e não UTF-8. `--incluir-espelho` continua equivalente a `full` e sobrescreve
  o `--mode` escolhido; não pode ser combinado com `--task`/`--include`.

O espelho antigo `Novo_Ambiente_Simulado/` e o derivado
`.artifacts/simulado/` não entram em `canonical` ou `task`.
`Ajustes_Codex/` conserva sua exclusão histórica. Nenhum modo inclui ignorados
por fora do Git; `full` não promete recuperar o espelho ignorado, um arquivo
apagado nem a história de commits. O corpo textual também não é pacote de
instalação ou prova de leitura de cada linha. Symlinks/junctions enumerados
reprovam a geração, em vez de permitir leitura fora da raiz.

## Verificação e manutenção

```sh
python -m unittest discover -s tools/tests -p 'test_bundle_para_auditoria.py' -v
```

A suíte exercita modos antigos e alias, SHA-256, worktree limpo/sujo, cópia limpa,
paths com espaços/Unicode, exclusões, configuração inválida, seleções vazias,
saída recorrente e escapes. Compare três tarefas reais contra `canonical` no
mesmo estado Git e declare cada path adicional. Preserve o histórico integral
e interprete redução como bytes de conteúdo selecionado, não como nova cobertura
de auditoria. [Regras de colaboração](rules/colaboracao.md) e
[fontes/derivados](rules/fontes-e-derivados.md) continuam regendo os efeitos.
