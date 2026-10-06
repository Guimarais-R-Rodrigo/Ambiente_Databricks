# SE08 — runbook de materialização e certificação local

> **Leitura histórica da campanha.** Os comandos abaixo com `Novo_Ambiente_Simulado`,
> `git diff`, `git restore` ou `git add` sobre o espelho descrevem o layout versionado
> daquela campanha. Para uma release atual, use a [saída gerada vigente](../../../manutencao/saida-gerada.md):
> `.artifacts/simulado/` e `render_simulado.py --check`. Não use os comandos históricos
> para certificar paridade nem recupere/remova conteúdo atual por associação.

Este runbook pressupõe que a autoria repo-side foi concluída no GitHub. A missão
local é produzir a candidata materializada e a evidência que não pode ser
fabricada remotamente.

## 1. Reconciliar identidade

Atualizar refs sem alterar a branch e registrar:

```powershell
git fetch --all --prune
git switch sef/SE08-operacao
git status --short
git rev-parse HEAD
git rev-parse origin/main
git merge-base HEAD origin/main
git rev-list --left-right --count origin/main...HEAD
```

Exigir worktree limpa. Se houver commits novos, auditar antes de prosseguir.

## 2. Materializar somente pelo renderer

```powershell
python tools/validate_assistant.py
python tools/render_simulado.py --write
git status --short
git diff -- Novo_Ambiente_Simulado
```

O delta do simulado deve ser mecânico e corresponder às alterações de
`ambiente_fonte/`. Não editar arquivo derivado à mão.

## 3. Reconciliar snapshot verificável

```powershell
python tools/validate_assistant.py --conferir-readme
```

Se a saída colada do README raiz estiver desatualizada, atualizar apenas as
linhas derivadas da execução real. Versionar a rematerialização e o snapshot em
commit explícito. O novo SHA passa a ser a candidata; evidência anterior não é
herdada automaticamente.

## 4. Executar a bateria específica

No novo SHA, executar em ordem a matriz de [TESTES.md](TESTES.md). Não fazer
retry-until-green. Preservar stdout/stderr e exit de toda tentativa.

## 5. FULL SE08

Criar diretório externo novo e executar:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <DIRETORIO_NOVO>
```

A execução deve ocorrer com worktree limpa e sem flags de dispensa.

## 6. Gate geral

Preparar dependências conforme os arquivos do projeto e executar:

```powershell
python tools/ci_local.py --verbose
```

Registrar que o subgate SEF interno não substitui o FULL anterior.

## 7. Windows/NTFS

Na máquina Windows nativa, repetir no mesmo SHA as suítes de processos/cleanup e
demais comandos exigidos pela matriz. Registrar versão exata de Python, volume,
filesystem, comando, exit, contagens e diretórios de evidência.

Não reclassificar o residual histórico por ausência de reprodução.

## 8. Entrega do gate local

Entregar:

- SHA/tree congelados;
- parentage/merge-base/ahead-behind;
- diff final;
- comandos e exits;
- testes/failures/errors/skips;
- evidence bundle FULL;
- evidência Windows separada;
- falhas preservadas e análise causal;
- indicação explícita do que continua NOT_RUN.

Não abrir PR automaticamente. A decisão de seguir para Free/Genie deve ser
tomada depois da auditoria dessa evidência.
