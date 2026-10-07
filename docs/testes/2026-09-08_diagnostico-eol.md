# Diagnóstico de fim de linha — 08/09/2026

Registro datado do estado observado antes da normalização, conforme o pacote T0 do
plano consolidado. Executado a partir do commit `bdf33ee`, na worktree da máquina
`rodrigo-ryzen9`, através da ponte de arquivos (shell Linux com a pasta montada).

## Estado antes

| Medida | Valor |
|---|---|
| branch / HEAD | `main` / `bdf33ee` |
| arquivos versionados | 911 |
| staged | 0 |
| unstaged | 648 |
| untracked | 0 |

`git ls-files --eol` na entrada:

```text
647 i/lf w/crlf
247 i/lf w/lf
 16 i/none w/none
  1 i/lf w/mixed
```

O índice estava **inteiramente LF**. A divergência era exclusivamente de árvore de
trabalho. Verificação byte a byte nos 648 arquivos: **0 com diferença de conteúdo** —
todos coincidem com `HEAD` após remover `\r`.

O único arquivo com EOL misto era `docs/sprints/sprint-11-hub-ml-criar-objeto.md`
(125 de 281 linhas com CR), também idêntico ao `HEAD` ignorando `\r`.

Distribuição por diretório de topo (worktree CRLF):

| Diretório | CRLF | LF |
|---|---:|---:|
| `Novo_Ambiente_Simulado/` | 314 | 3 |
| `ambiente_databricks/` | 262 | 55 |
| `docs/` | 42 | 24 |
| `.claude/` | 12 | 7 |
| `tools/` | 10 | 1 |
| `Ajustes_Codex/` | 3 | 171 |
| raiz | 5 | 2 |

## Causa e limite da observação

Não havia `.gitattributes` versionado. Pela ponte Linux, `core.autocrlf`, `core.eol` e
`core.safecrlf` aparecem **não definidos** — mas essa é a configuração do ambiente da
ponte, **não** a do Git for Windows do usuário, que tem `core.autocrlf=true` por padrão
de instalação. Com essa configuração, o `git status` no Windows aparece limpo e apenas
um leitor externo enxerga a divergência.

**O que isso não prova:** não foi possível ler a configuração efetiva do Git no Windows
a partir desta sessão. A hipótese acima é compatível com todos os fatos observados, mas
permanece hipótese. O que está provado é o estado da árvore e a ausência de diferença de
conteúdo.

## Por que corrigir mesmo sem defeito de conteúdo

1. `bundle_implantacao.py` e `bundle_para_auditoria.py` **recusam worktree suja** por
   padrão. Qualquer agente ou máquina que enxergue os 648 arquivos como modificados não
   consegue gerar o pacote de implantação.
2. O diff de qualquer PR fica ilegível (69.414 inserções contra 69.414 deleções).
3. As IAs do projeto passam a trabalhar sobre representações diferentes da mesma árvore,
   o que contraria a regra de fonte única de verdade.

## Ação aplicada

`.gitattributes` versionado com `* text=auto eol=lf`, exceção `-text` para
`Ajustes_Codex/**` (material congelado, preservado byte a byte) e marcação `binary`
para extensões binárias conhecidas.

A árvore de trabalho foi convertida de CRLF para LF nos 648 arquivos afetados. A
conversão remove apenas `\r` em fim de linha; nenhuma outra transformação foi aplicada.

Um `index.lock` órfão, resultante de um comando interrompido durante o diagnóstico,
precisou ser renomeado para `.git/index.lock.orfao-20260908` porque a ponte de arquivos
não permite exclusão. O arquivo é interno ao `.git` e pode ser apagado manualmente.

## Estado depois

| Medida | Valor |
|---|---|
| arquivos com CRLF na worktree | 0 |
| staged | 0 |
| unstaged | 0 |
| untracked | apenas `.gitattributes`, antes de ser versionado |

Nenhuma alteração funcional foi feita neste pacote. A normalização está isolada em
commit próprio, separada das correções de código.

## Conferência recomendada na máquina Windows

```powershell
git config --show-origin core.autocrlf
git status
git ls-files --eol | Select-String "w/crlf" | Measure-Object
```

Após o merge deste branch, um checkout novo deve produzir árvore LF e `git status` limpo.
